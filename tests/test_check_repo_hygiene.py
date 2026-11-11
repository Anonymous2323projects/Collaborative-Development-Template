"""Unit tests for the repository hygiene helper functions.

Run with: python3 -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_repo_hygiene as hygiene


class SensitivePathTests(unittest.TestCase):
    def test_env_example_is_allowed(self):
        self.assertFalse(hygiene.sensitive_path(Path(".env.example")))

    def test_env_file_is_rejected(self):
        self.assertTrue(hygiene.sensitive_path(Path("config/.env.production")))

    def test_private_key_extension_is_rejected(self):
        self.assertTrue(hygiene.sensitive_path(Path("certs/service.pem")))

    def test_credentials_directory_is_rejected(self):
        self.assertTrue(hygiene.sensitive_path(Path("credentials/example.txt")))


class MarkdownHelperTests(unittest.TestCase):
    def test_fenced_code_is_removed_before_anchor_scan(self):
        content = "# Real heading\n\n```md\n# Not a heading\n```\n"
        anchors = hygiene.markdown_anchors(content)
        self.assertIn("real-heading", anchors)
        self.assertNotIn("not-a-heading", anchors)

    def test_duplicate_heading_anchors_are_numbered(self):
        content = "# Setup\n\n# Setup\n"
        anchors = hygiene.markdown_anchors(content)
        self.assertIn("setup", anchors)
        self.assertIn("setup-1", anchors)

    def test_slug_strips_markdown_and_punctuation(self):
        self.assertEqual(hygiene.github_slug("**AI & Safety**"), "ai-safety")


class MarkdownDiagnosticSafetyTests(unittest.TestCase):
    def test_hidden_html_comment_is_not_checked(self):
        content = "# Visible\n<!-- [hidden](does-not-exist.md)\n# Hidden\n-->\n"
        self.assertIn("visible", hygiene.markdown_anchors(content))
        self.assertNotIn("hidden", hygiene.markdown_anchors(content))
        self.assertEqual(hygiene.markdown_link_errors(Path("README.md"), content, {}), [])

    def test_unclosed_comment_hides_links(self):
        content = "# Visible\n<!--\n[hidden](does-not-exist.md)\n"
        self.assertEqual(hygiene.markdown_link_errors(Path("README.md"), content, {}), [])

    def test_missing_link_diagnostic_does_not_echo_target(self):
        with TemporaryDirectory() as tmp, patch.object(hygiene, "ROOT", Path(tmp)):
            errors = hygiene.markdown_link_errors(
                Path("README.md"),
                "[broken](missing.md?credential=private-placeholder)",
                {},
            )
        self.assertEqual(len(errors), 1)
        self.assertIn("missing local link target", errors[0])
        self.assertNotIn("credential", errors[0])
        self.assertNotIn("private-placeholder", errors[0])

    def test_escaping_link_diagnostic_does_not_echo_target(self):
        with TemporaryDirectory() as tmp, patch.object(hygiene, "ROOT", Path(tmp)):
            errors = hygiene.markdown_link_errors(
                Path("README.md"),
                "[escape](../outside.md?credential=private-placeholder)",
                {},
            )
        self.assertEqual(len(errors), 1)
        self.assertIn("link escapes repository", errors[0])
        self.assertNotIn("private-placeholder", errors[0])

    def test_valid_local_link_still_passes(self):
        with TemporaryDirectory() as tmp, patch.object(hygiene, "ROOT", Path(tmp)):
            (Path(tmp) / "guide.md").write_text("# Real heading\n", encoding="utf-8")
            errors = hygiene.markdown_link_errors(
                Path("README.md"), "[guide](guide.md#real-heading)", {}
            )
        self.assertEqual(errors, [])


class WorkflowPolicyTests(unittest.TestCase):
    def test_valid_minimal_workflow_passes(self):
        content = """name: check
permissions:
  contents: read
jobs:
  check:
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
"""
        self.assertEqual(hygiene.workflow_policy_errors(Path(".github/workflows/test.yml"), content), [])

    def test_missing_permissions_is_rejected(self):
        content = "name: check\njobs: {}\n"
        errors = hygiene.workflow_policy_errors(Path("workflow.yml"), content)
        self.assertTrue(any("explicit top-level" in error for error in errors))

    def test_unpinned_action_is_rejected(self):
        content = """permissions:
  contents: read
steps:
  - uses: actions/checkout@v4
"""
        errors = hygiene.workflow_policy_errors(Path("workflow.yml"), content)
        self.assertTrue(any("full 40-character" in error for error in errors))

    def test_pull_request_target_is_rejected_by_default(self):
        content = """permissions:
  contents: read
on:
  pull_request_target:
"""
        errors = hygiene.workflow_policy_errors(Path("workflow.yml"), content)
        self.assertTrue(any("pull_request_target" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
