"""Functional Gitleaks regression for second-parent and merge-only secrets.

Runs in the secret-scan job after the existing action installs Gitleaks.
The baseline unit job may skip these integration tests when Gitleaks is absent.
All credentials below are intentionally fictitious and use a fixture-only rule.
"""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(shutil.which("gitleaks"), "Gitleaks is installed only in the secret-scan job")
class SecretScanMergeHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "--initial-branch=main", "--quiet")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Synthetic fixture")
        (self.repo / "README.md").write_text("harmless starting point\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "--quiet", "-m", "base")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.config = Path(self.temp.name) / "synthetic-gitleaks.toml"
        self.config.write_text(
            'title = "Synthetic Git merge regression"\n'
            '[[rules]]\n'
            'id = "synthetic-merge-secret"\n'
            'description = "Never an actual credential"\n'
            "regex = '''CDT_FAKE_CREDENTIAL_[A-Z]{24}'''\n",
            encoding="utf-8",
        )

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, capture_output=True, text=True, check=True,
        )

    def diverge(self, *, secret_on_side):
        self.git("checkout", "--quiet", "-b", "side")
        if secret_on_side:
            (self.repo / "example.txt").write_text(
                "CDT_FAKE_CREDENTIAL_" + "Q" * 24 + "\n", encoding="utf-8",
            )
        else:
            (self.repo / "example.txt").write_text("harmless side change\n", encoding="utf-8")
        self.git("add", "example.txt")
        self.git("commit", "--quiet", "-m", "side")
        self.side = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "--quiet", "main")
        (self.repo / "main.txt").write_text("harmless main change\n", encoding="utf-8")
        self.git("add", "main.txt")
        self.git("commit", "--quiet", "-m", "main")
        self.git("merge", "--quiet", "--no-ff", "--no-commit", "side")
        if not secret_on_side:
            (self.repo / "merge-only.txt").write_text(
                "CDT_FAKE_CREDENTIAL_" + "R" * 24 + "\n", encoding="utf-8",
            )
            self.git("add", "merge-only.txt")
        self.git("commit", "--quiet", "-m", "merge")
        self.head = self.git("rev-parse", "HEAD").stdout.strip()

    def scan(self, opts, report_name):
        return subprocess.run(
            [
                "gitleaks", "git", "--config", str(self.config), "--redact",
                "--exit-code", "2", "--report-format", "json",
                "--report-path", str(Path(self.temp.name) / report_name),
                "--log-opts", opts, ".",
            ],
            cwd=self.repo, capture_output=True, text=True, check=False,
        ).returncode

    def test_second_parent_secret_is_detected_but_old_traversal_misses_it(self):
        self.diverge(secret_on_side=True)
        selected = self.git("log", "--full-history", "-m", "--format=%H", f"{self.base}..{self.head}").stdout.splitlines()
        self.assertIn(self.side, selected)
        old = f"--first-parent --no-merges {self.base}..{self.head}"
        self.assertEqual(self.scan(old, "old.json"), 0, "old traversal unexpectedly reached the side branch")
        complete = f"--full-history -m --no-ext-diff --no-textconv {self.base}..{self.head}"
        self.assertEqual(self.scan(complete, "complete.json"), 2, "full history did not flag the side-branch fixture")

    def test_merge_resolution_only_secret_requires_merge_diffs(self):
        self.diverge(secret_on_side=False)
        without_merge_diff = f"--full-history --no-ext-diff --no-textconv {self.base}..{self.head}"
        self.assertEqual(self.scan(without_merge_diff, "no-merge.json"), 0)
        with_merge_diff = f"--full-history -m --no-ext-diff --no-textconv {self.base}..{self.head}"
        self.assertEqual(self.scan(with_merge_diff, "merge.json"), 2, "merge-only fixture was not detected")


if __name__ == "__main__":
    unittest.main()
