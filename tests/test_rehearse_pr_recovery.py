"""Synthetic offline recovery round-trip tests; no network or real user repository."""
import sys
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

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
