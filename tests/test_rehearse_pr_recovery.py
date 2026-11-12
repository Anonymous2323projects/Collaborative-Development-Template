"""Synthetic offline recovery round-trip tests; no network or real user repository."""
import sys
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

    def test_gitlink_requires_separate_assessment(self):
        run(self.root, "update-index", "--add", "--cacheinfo", f"160000,{self.head},example-submodule")
        run(self.root, "commit", "--quiet", "-m", "add gitlink")
        with self.assertRaises(recovery.RecoveryError):
            recovery.verify(self.base, run(self.root, "rev-parse", "HEAD"), self.root)


if __name__ == "__main__":
    unittest.main()
