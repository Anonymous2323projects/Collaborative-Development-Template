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

    def test_trusted_authorizer_requires_separate_app_token_and_read_only_github_token(self):
        content = """permissions:
  contents: read
  pull-requests: read
on:
  issue_comment:
    types: [created]
jobs:
  authorize:
    environment:
      name: merge-authorizer
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          ref: DEFAULT_BRANCH_EXPR
          persist-credentials: false
      - id: preflight
        run: python3 scripts/authorize_merge.py --preflight
      - id: status-token
        if: steps.preflight.outputs.authorized == 'true'
        uses: actions/create-github-app-token@0123456789abcdef0123456789abcdef01234567
        with:
          permission-statuses: write
          skip-token-revoke: false
          app-id: APP_CLIENT_ID_EXPR
          private-key: APP_PRIVATE_KEY_EXPR
      - name: validate
        if: steps.preflight.outputs.authorized == 'true'
        env:
          GITHUB_TOKEN: GITHUB_TOKEN_EXPR
          MERGE_AUTH_TOKEN: MERGE_TOKEN_EXPR
"""
        content = content.replace("DEFAULT_BRANCH_EXPR", "$" + "{{ github.event.repository.default_branch }}")
        content = content.replace("GITHUB_TOKEN_EXPR", "$" + "{{ secrets.GITHUB_TOKEN }}")
        content = content.replace("MERGE_TOKEN_EXPR", "$" + "{{ steps.status-token.outputs.token }}")
        content = content.replace("APP_CLIENT_ID_EXPR", "$" + "{{ vars.MERGE_AUTH_APP_CLIENT_ID }}")
        content = content.replace("APP_PRIVATE_KEY_EXPR", "$" + "{{ secrets.MERGE_AUTH_APP_PRIVATE_KEY }}")
        self.assertEqual(
            hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content),
            [],
        )

    def test_github_token_status_write_is_rejected_even_in_trusted_workflow(self):
        content = """permissions:
  contents: read
  pull-requests: read
  statuses: write
on:
  issue_comment:
    types: [created]
jobs:
  authorize:
    environment:
      name: merge-authorizer
"""
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content)
        self.assertTrue(any("GITHUB_TOKEN statuses: write is prohibited" in error for error in errors))

    def test_github_token_status_write_is_rejected_in_untrusted_workflow(self):
        content = """permissions:
  contents: read
  statuses: write
on:
  pull_request:
jobs:
  check:
    steps: []
"""
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/untrusted.yml"), content)
        self.assertTrue(any("GITHUB_TOKEN statuses: write is prohibited" in error for error in errors))

    def test_trusted_authorizer_rejects_additional_triggers(self):
        content = """permissions:
  contents: read
  pull-requests: read
on:
  issue_comment:
    types: [created]
  pull_request:
    types: [opened]
jobs:
  authorize:
    environment:
      name: merge-authorizer
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          ref: DEFAULT_BRANCH_EXPR
          persist-credentials: false
      - id: preflight
        run: python3 scripts/authorize_merge.py --preflight
      - id: status-token
        if: steps.preflight.outputs.authorized == 'true'
        uses: actions/create-github-app-token@0123456789abcdef0123456789abcdef01234567
        with:
          permission-statuses: write
          skip-token-revoke: false
      - name: validate
        if: steps.preflight.outputs.authorized == 'true'
        env:
          GITHUB_TOKEN: GITHUB_TOKEN_EXPR
          MERGE_AUTH_TOKEN: MERGE_TOKEN_EXPR
"""
        content = content.replace("DEFAULT_BRANCH_EXPR", "$" + "{{ github.event.repository.default_branch }}")
        content = content.replace("GITHUB_TOKEN_EXPR", "$" + "{{ secrets.GITHUB_TOKEN }}")
        content = content.replace("MERGE_TOKEN_EXPR", "$" + "{{ steps.status-token.outputs.token }}")
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content)
        self.assertTrue(any("must trigger only on issue_comment" in error for error in errors))

    def test_app_credentials_cannot_be_referenced_by_other_workflows(self):
        content = """permissions:
  contents: read
jobs:
  check:
    steps:
      - run: echo MERGE_AUTH_APP_PRIVATE_KEY
"""
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/untrusted.yml"), content)
        self.assertTrue(any("only the trusted authorization workflow may reference the merge App credentials" in error for error in errors))

    def test_pull_request_target_is_rejected_by_default(self):
        content = """permissions:
  contents: read
on:
  pull_request_target:
"""
        errors = hygiene.workflow_policy_errors(Path("workflow.yml"), content)
        self.assertTrue(any("pull_request_target" in error for error in errors))



class AssuranceDocumentTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_valid_fixture(self):
        (self.root / "MERGE_AND_CHANGE_ASSURANCE.md").write_text(
            "\n".join(f"## {section}" for section in hygiene.REQUIRED_ASSURANCE_SECTIONS),
            encoding="utf-8",
        )
        for path in hygiene.ASSURANCE_REFERENCES:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("[Assurance](MERGE_AND_CHANGE_ASSURANCE.md)\n", encoding="utf-8")

    def test_complete_assurance_contract_passes(self):
        self.write_valid_fixture()
        self.assertEqual(hygiene.assurance_document_errors(self.root), [])

    def test_missing_canonical_document_is_rejected(self):
        self.write_valid_fixture()
        (self.root / "MERGE_AND_CHANGE_ASSURANCE.md").unlink()
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("canonical assurance standard is missing" in error for error in errors))

    def test_missing_core_section_is_rejected(self):
        self.write_valid_fixture()
        path = self.root / "MERGE_AND_CHANGE_ASSURANCE.md"
        content = path.read_text(encoding="utf-8").replace(
            "## 4. Five-perspective assessment", "## 4. Omitted assessment"
        )
        path.write_text(content, encoding="utf-8")
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("Five-perspective assessment" in error for error in errors))

    def test_missing_governing_reference_is_rejected(self):
        self.write_valid_fixture()
        path = self.root / "docs/DEVELOPMENT_WORKFLOW.md"
        path.write_text("No assurance link here\n", encoding="utf-8")
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("DEVELOPMENT_WORKFLOW.md" in error and "must contain a Markdown link" in error for error in errors))


    def test_plain_or_fenced_mentions_do_not_satisfy_governing_links(self):
        self.write_valid_fixture()
        path = self.root / "AGENTS.md"
        path.write_text(
            "MERGE_AND_CHANGE_ASSURANCE.md\n\n```md\n[Assurance](MERGE_AND_CHANGE_ASSURANCE.md)\n```\n",
            encoding="utf-8",
        )
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("AGENTS.md" in error and "Markdown link" in error for error in errors))

    def test_headings_inside_fenced_code_do_not_satisfy_contract(self):
        self.write_valid_fixture()
        path = self.root / "MERGE_AND_CHANGE_ASSURANCE.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace(
            "## 4. Five-perspective assessment",
            "```md\n## 4. Five-perspective assessment\n```",
        )
        path.write_text(content, encoding="utf-8")
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("Five-perspective assessment" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
