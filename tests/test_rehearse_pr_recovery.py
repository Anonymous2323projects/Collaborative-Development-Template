"""Synthetic offline recovery round-trip tests; no network or real user repository."""
import sys
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import rehearse_pr_recovery as recovery


def run(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class RecoveryRehearsalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "fixture"
        self.root.mkdir()
        run(self.root, "init", "--quiet")
        run(self.root, "config", "user.name", "Synthetic Tester")
        run(self.root, "config", "user.email", "fixture@example.invalid")
        (self.root / "README.md").write_text("original\n", encoding="utf-8")
        (self.root / ".hidden").write_text("invisible\n", encoding="utf-8")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "base")
        self.base = run(self.root, "rev-parse", "HEAD")
        (self.root / "README.md").write_text("changed\n", encoding="utf-8")
        (self.root / ".hidden").unlink()
        (self.root / "binary.bin").write_bytes(bytes(range(256)))
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "head")
        self.head = run(self.root, "rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def test_binary_add_delete_edit_round_trip(self):
        before, after = recovery.verify(self.base, self.head, self.root)
        self.assertEqual(before, run(self.root, "rev-parse", self.base + "^{tree}"))
        self.assertEqual(after, run(self.root, "rev-parse", self.head + "^{tree}"))

    def test_existing_binary_edit_and_delete_round_trip(self):
        existing = self.root / "existing.bin"
        deleted = self.root / "deleted.bin"
        existing.write_bytes(bytes(range(256)))
        deleted.write_bytes(b"\x00\xff\x80\x01")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "add existing binary fixtures")
        before = run(self.root, "rev-parse", "HEAD")
        existing.write_bytes(bytes(reversed(range(256))) + b"\x00")
        deleted.unlink()
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "modify and delete binary fixtures")
        after = run(self.root, "rev-parse", "HEAD")
        patch = run(self.root, "diff", "--binary", before, after)
        self.assertIn("GIT binary patch", patch)
        self.assertEqual(
            recovery.verify(before, after, self.root),
            (run(self.root, "rev-parse", before + "^{tree}"),
             run(self.root, "rev-parse", after + "^{tree}")),
        )

    def test_reverse_direction_is_also_valid(self):
        before, after = recovery.verify(self.head, self.base, self.root)
        self.assertEqual(before, run(self.root, "rev-parse", self.head + "^{tree}"))
        self.assertEqual(after, run(self.root, "rev-parse", self.base + "^{tree}"))

    def test_does_not_modify_source_branch_or_local_work(self):
        (self.root / "local-untracked.txt").write_text("keep my work")
        revision = run(self.root, "rev-parse", "HEAD")
        recovery.verify(self.base, self.head, self.root)
        self.assertEqual(revision, run(self.root, "rev-parse", "HEAD"))
        self.assertEqual((self.root / "local-untracked.txt").read_text(), "keep my work")

    @unittest.skipIf(os.name == "nt", "external diff fixture requires a POSIX shell")
    def test_custom_external_diff_helper_is_not_executed(self):
        """A maintainer's Git config must not run an external helper during rehearsal."""
        marker = Path(self.tmp.name) / "external-diff-executed.txt"
        helper = Path(self.tmp.name) / "safe-diff-fixture.py"
        helper.write_text(
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('ran', encoding='utf-8')\n",
            encoding="utf-8",
        )
        run(self.root, "config", "diff.external", f'"{sys.executable}" "{helper}"')

        # Demonstrate that the synthetic helper is actually active without the guard.
        run(self.root, "diff", "--binary", "--full-index", self.base, self.head, "--")
        self.assertTrue(marker.exists(), "test precondition: Git external diff is active")
        marker.unlink()

        expected = (
            run(self.root, "rev-parse", self.base + "^{tree}"),
            run(self.root, "rev-parse", self.head + "^{tree}"),
        )
        self.assertEqual(recovery.verify(self.base, self.head, self.root), expected)
        self.assertFalse(marker.exists(), "recovery executed an external diff helper")

    @unittest.skipIf(os.name == "nt", "textconv fixture requires POSIX-style helper")
    def test_custom_textconv_helper_is_not_executed(self):
        marker = Path(self.tmp.name) / "textconv-executed.txt"
        helper = Path(self.tmp.name) / "textconv-fixture.py"
        helper.write_text(
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('ran', encoding='utf-8')\n"
            "print('converted')\n",
            encoding="utf-8",
        )
        (self.root / ".gitattributes").write_text("*.dat diff=fixture\n", encoding="utf-8")
        (self.root / "sample.dat").write_bytes(b"\x00before\x00")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "textconv before")
        before = run(self.root, "rev-parse", "HEAD")
        (self.root / "sample.dat").write_bytes(b"\x00after\x00")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "textconv after")
        after = run(self.root, "rev-parse", "HEAD")
        run(self.root, "config", "diff.fixture.textconv", f'"{sys.executable}" "{helper}"')
        # Demonstrate that --no-ext-diff alone still permits textconv execution.
        run(self.root, "diff", "--no-ext-diff", "--binary", "--full-index", before, after, "--")
        self.assertTrue(marker.exists(), "test precondition: textconv is active")
        marker.unlink()
        self.assertEqual(
            recovery.verify(before, after, self.root),
            (run(self.root, "rev-parse", before + "^{tree}"),
             run(self.root, "rev-parse", after + "^{tree}")),
        )
        self.assertFalse(marker.exists(), "recovery executed a textconv helper")

    @unittest.skipIf(os.name == "nt", "synthetic filter fixture requires POSIX shell")
    def test_inherited_global_smudge_filter_does_not_run(self):
        marker = Path(self.tmp.name) / "global-filter-executed.txt"
        helper = Path(self.tmp.name) / "filter-fixture.sh"
        helper.write_text(
            "#!/bin/sh\n"
            f'printf triggered >> "{marker}"\n'
            "cat\n",
            encoding="utf-8",
        )
        helper.chmod(0o755)
        (self.root / ".gitattributes").write_text("*.txt filter=fixture\n", encoding="utf-8")
        (self.root / "filtered.txt").write_text("before\n", encoding="utf-8")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "filter before")
        before = run(self.root, "rev-parse", "HEAD")
        (self.root / "filtered.txt").write_text("after\n", encoding="utf-8")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "filter after")
        after = run(self.root, "rev-parse", "HEAD")
        global_cfg = Path(self.tmp.name) / "synthetic-global.cfg"
        run(self.root, "config", "--file", str(global_cfg), "filter.fixture.smudge", f'"{helper}"')
        run(self.root, "config", "--file", str(global_cfg), "filter.fixture.clean", f'"{helper}"')

        with patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(global_cfg)}):
            # The unisolated checkout demonstrates the synthetic filter is active.
            scratch = Path(self.tmp.name) / "unsafe-control"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-checkout", str(self.root), str(scratch)],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            run(scratch, "checkout", "--detach", before)
            self.assertTrue(marker.exists(), "test precondition: smudge filter is active")
            marker.unlink()
            (scratch / "filtered.txt").write_text("dirty control\n", encoding="utf-8")
            run(scratch, "add", "filtered.txt")
            self.assertTrue(marker.exists(), "test precondition: clean filter is active")
            marker.unlink()
            self.assertEqual(
                recovery.verify(before, after, self.root),
                (run(self.root, "rev-parse", before + "^{tree}"),
                 run(self.root, "rev-parse", after + "^{tree}")),
            )
            self.assertFalse(marker.exists(), "recovery executed an inherited filter")

    def test_git_subprocess_environment_discards_git_overrides(self):
        with patch.dict(os.environ, {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "diff.external",
            "GIT_CONFIG_VALUE_0": "fixture",
            "GIT_EXTERNAL_DIFF": "fixture",
            "GIT_INDEX_FILE": "synthetic-index",
        }):
            safe = recovery.isolated_git_env()
            self.assertEqual(safe["GIT_CONFIG_NOSYSTEM"], "1")
            self.assertEqual(safe["GIT_CONFIG_GLOBAL"], os.devnull)
            self.assertEqual(safe["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(safe["GIT_NO_REPLACE_OBJECTS"], "1")
            self.assertEqual(safe["GIT_ATTR_NOSYSTEM"], "1")
            allowlist = {"GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL",
                         "GIT_ATTR_NOSYSTEM", "GIT_NO_LAZY_FETCH", "GIT_NO_REPLACE_OBJECTS"}
            self.assertFalse(any(k.upper().startswith("GIT_") for k in safe
                                 if k not in allowlist))

    def test_missing_promisor_blob_fails_closed_without_fetching(self):
        """An object held only by a local promisor remote must not be fetched."""
        remote = Path(self.tmp.name) / "complete-local-remote.git"
        run(self.root, "clone", "--bare", str(self.root), str(remote))
        run(self.root, "remote", "add", "origin", str(remote))
        run(self.root, "config", "extensions.partialClone", "origin")
        run(self.root, "config", "remote.origin.promisor", "true")
        run(self.root, "config", "remote.origin.partialclonefilter", "blob:none")
        missing_blob = run(self.root, "rev-parse", f"{self.base}:README.md")
        object_path = self.root / ".git" / "objects" / missing_blob[:2] / missing_blob[2:]
        self.assertTrue(object_path.exists(), "test precondition: loose object exists")
        object_path.unlink()  # Only the synthetic, disposable test repository.
        self.assertFalse(object_path.exists())

        with self.assertRaises(recovery.RecoveryError):
            recovery.verify(self.base, self.head, self.root)
        self.assertFalse(object_path.exists(), "recovery fetched a missing object")
        # Positive control: the only remote is another local disposable fixture.
        # With the guard absent, Git can lazily retrieve exactly this blob.
        self.assertEqual(run(self.root, "cat-file", "-p", missing_blob), "original")

    @unittest.skipIf(os.name == "nt", "POSIX executable-hook fixture")
    def test_inherited_template_hook_is_not_executed(self):
        template = Path(self.tmp.name) / "inherited-template"
        hooks = template / "hooks"
        hooks.mkdir(parents=True)
        marker = Path(self.tmp.name) / "template-hook-executed"
        hook = hooks / "post-checkout"
        hook.write_text(
            "#!/bin/sh\n"
            f'printf ran > "{marker}"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)
        with patch.dict(os.environ, {"GIT_TEMPLATE_DIR": str(template)}):
            control = Path(self.tmp.name) / "unsafe-template-control"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-checkout",
                 str(self.root), str(control)],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            run(control, "checkout", "--detach", self.base)
            self.assertTrue(marker.exists(), "test precondition: template hook executes")
            marker.unlink()
            recovery.verify(self.base, self.head, self.root)
            self.assertFalse(marker.exists(), "recovery executed an inherited template hook")

    def test_failure_message_has_allowlisted_stage_not_local_path(self):
        from contextlib import redirect_stderr
        from io import StringIO

        stream = StringIO()
        with patch.object(sys, "argv", [
            "rehearse_pr_recovery.py", "--repository", str(self.root),
            "--base", "f" * 40, "--head", self.head,
        ]), redirect_stderr(stream):
            self.assertEqual(recovery.main(), 1)
        self.assertIn("FAILED in rev-parse", stream.getvalue())
        self.assertNotIn(str(self.root), stream.getvalue())
        self.assertNotIn("f" * 40, stream.getvalue())

    def test_rejects_invalid_sha(self):
        for value in ("short", "a" * 39, "f" * 40 + "; echo bad", "A" * 40):
            with self.subTest(value=value), self.assertRaises(recovery.RecoveryError):
                recovery.verify(value, self.head, self.root)

    def test_missing_commit_fails_closed(self):
        with self.assertRaises(recovery.RecoveryError):
            recovery.verify("f" * 40, self.head, self.root)

    def test_missing_repository_fails_closed(self):
        with self.assertRaises(recovery.RecoveryError):
            recovery.verify(self.base, self.head, Path(self.tmp.name))

    def test_gitlink_looking_filename_is_regular_file(self):
        (self.root / "160000 commit ordinary.txt").write_text("ordinary\n")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "ordinary filename containing gitlink text")
        after = run(self.root, "rev-parse", "HEAD")
        self.assertEqual(
            recovery.verify(self.head, after, self.root),
            (run(self.root, "rev-parse", self.head + "^{tree}"),
             run(self.root, "rev-parse", after + "^{tree}")),
        )

    @unittest.skipIf(os.name == "nt", "newlines are not valid in Windows filenames")
    def test_gitlink_looking_filename_with_newline_on_posix(self):
        (self.root / "header\n160000 commit").write_text("newline in name\n")
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "POSIX filename with newline")
        after = run(self.root, "rev-parse", "HEAD")
        self.assertEqual(
            recovery.verify(self.head, after, self.root),
            (run(self.root, "rev-parse", self.head + "^{tree}"),
             run(self.root, "rev-parse", after + "^{tree}")),
        )

    @unittest.skipUnless(sys.platform.startswith("linux"), "raw non-UTF-8 filename test requires Linux")
    def test_non_utf8_filename_does_not_break_gitlink_parser(self):
        invalid_path = os.path.join(os.fsencode(self.root), b"raw-\xff-160000 commit.dat")
        with open(invalid_path, "wb") as output:
            output.write(bytes(range(256)))
        run(self.root, "add", "--all")
        run(self.root, "commit", "--quiet", "-m", "raw non-UTF-8 filename")
        after = run(self.root, "rev-parse", "HEAD")
        self.assertEqual(
            recovery.verify(self.head, after, self.root),
            (run(self.root, "rev-parse", self.head + "^{tree}"),
             run(self.root, "rev-parse", after + "^{tree}")),
        )

    def test_gitlink_requires_separate_assessment(self):
        run(self.root, "update-index", "--add", "--cacheinfo", f"160000,{self.head},example-submodule")
        run(self.root, "commit", "--quiet", "-m", "add gitlink")
        with self.assertRaises(recovery.RecoveryError):
            recovery.verify(self.base, run(self.root, "rev-parse", "HEAD"), self.root)


if __name__ == "__main__":
    unittest.main()
