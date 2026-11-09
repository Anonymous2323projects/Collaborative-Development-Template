"""Unit tests for the repository hygiene helper functions.

Run with: python3 -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

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


class IntegrationReviewContractTests(unittest.TestCase):
    def test_complete_canonical_review_contract_passes(self):
        doc = hygiene.INTEGRATION_REVIEW_DOC
        contents = {
            doc: "\n".join(hygiene.INTEGRATION_REVIEW_HEADINGS),
            Path("AGENTS.md"): "docs/INTEGRATION_AND_MERGE_REVIEW.md",
            Path("docs/DEVELOPMENT_WORKFLOW.md"): "INTEGRATION_AND_MERGE_REVIEW.md",
            Path("PROJECT_RISK_AND_RELEASE_READINESS.md"): "docs/INTEGRATION_AND_MERGE_REVIEW.md",
        }
        files = list(contents)
        self.assertEqual(hygiene.integration_review_contract_errors(files, contents), [])

    def test_missing_canonical_document_is_rejected(self):
        errors = hygiene.integration_review_contract_errors([], {})
        self.assertTrue(any("required integration and merge review standard is missing" in error for error in errors))

    def test_missing_cross_document_reference_is_rejected(self):
        doc = hygiene.INTEGRATION_REVIEW_DOC
        contents = {
            doc: "\n".join(hygiene.INTEGRATION_REVIEW_HEADINGS),
            Path("AGENTS.md"): "",
            Path("docs/DEVELOPMENT_WORKFLOW.md"): "INTEGRATION_AND_MERGE_REVIEW.md",
            Path("PROJECT_RISK_AND_RELEASE_READINESS.md"): "docs/INTEGRATION_AND_MERGE_REVIEW.md",
        }
        errors = hygiene.integration_review_contract_errors(list(contents), contents)
        self.assertTrue(any("AGENTS.md" in error for error in errors))

    def test_missing_review_gate_section_is_rejected(self):
        doc = hygiene.INTEGRATION_REVIEW_DOC
        contents = {
            doc: "\n".join(hygiene.INTEGRATION_REVIEW_HEADINGS[:-1]),
            Path("AGENTS.md"): "docs/INTEGRATION_AND_MERGE_REVIEW.md",
            Path("docs/DEVELOPMENT_WORKFLOW.md"): "INTEGRATION_AND_MERGE_REVIEW.md",
            Path("PROJECT_RISK_AND_RELEASE_READINESS.md"): "docs/INTEGRATION_AND_MERGE_REVIEW.md",
        }
        errors = hygiene.integration_review_contract_errors(list(contents), contents)
        self.assertTrue(any("Evidence, efficiency, and honest reporting" in error for error in errors))


if __name__ == "__main__":
    unittest.main()


