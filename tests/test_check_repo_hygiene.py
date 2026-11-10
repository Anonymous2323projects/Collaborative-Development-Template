"""Unit tests for the repository hygiene helper functions.

Run with: python3 -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path
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

    def test_html_comment_headings_are_removed_before_anchor_scan(self):
        content = "# Real heading\n\n<!--\n# Hidden heading\n-->\n"
        anchors = hygiene.markdown_anchors(content)
        self.assertIn("real-heading", anchors)
        self.assertNotIn("hidden-heading", anchors)

    def test_duplicate_heading_anchors_are_numbered(self):
        content = "# Setup\n\n# Setup\n"
        anchors = hygiene.markdown_anchors(content)
        self.assertIn("setup", anchors)
        self.assertIn("setup-1", anchors)

    def test_slug_strips_markdown_and_punctuation(self):
        self.assertEqual(hygiene.github_slug("**AI & Safety**"), "ai-safety")

    def test_missing_link_error_redacts_query_and_fragment(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(hygiene, "ROOT", Path(temp_dir)):
                errors = hygiene.markdown_link_errors(
                    Path("README.md"),
                    "[broken](missing.md?token=CANARY_REVIEW_ONLY_123456#private-fragment)",
                    {},
                )
        self.assertEqual(len(errors), 1)
        self.assertIn("missing.md", errors[0])
        self.assertNotIn("CANARY_REVIEW_ONLY_123456", errors[0])
        self.assertNotIn("private-fragment", errors[0])

    def test_missing_anchor_error_redacts_query_and_fragment(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Public heading\\n", encoding="utf-8")
            with patch.object(hygiene, "ROOT", root):
                errors = hygiene.markdown_link_errors(
                    Path("README.md"),
                    "[broken](docs/guide.md?token=CANARY_REVIEW_ONLY_654321#secret-fragment)",
                    {},
                )
        self.assertEqual(len(errors), 1)
        self.assertIn("docs/guide.md", errors[0])
        self.assertNotIn("CANARY_REVIEW_ONLY_654321", errors[0])
        self.assertNotIn("secret-fragment", errors[0])


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

    def trusted_authorizer_workflow_fixture(self):
        content = """permissions:
  contents: read
  pull-requests: read
on:
  issue_comment:
    types: [created]
jobs:
  preflight:
    outputs:
      authorized: PREFLIGHT_OUTPUT
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          ref: DEFAULT_BRANCH_EXPR
          persist-credentials: false
      - id: preflight
        env:
          GITHUB_EVENT_PATH: EVENT_PATH_EXPR
          MERGE_AUTHORIZER_LOGINS: LOGINS_EXPR
        run: python3 scripts/authorize_merge.py --preflight
  authorize:
    needs: preflight
    if: PREFLIGHT_JOB_CONDITION
    environment:
      name: merge-authorizer
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          ref: DEFAULT_BRANCH_EXPR
          persist-credentials: false
      - id: status-token
        uses: actions/create-github-app-token@0123456789abcdef0123456789abcdef01234567
        with:
          permission-statuses: write
          skip-token-revoke: false
          client-id: APP_CLIENT_ID_EXPR
          private-key: APP_PRIVATE_KEY_EXPR
          owner: OWNER_EXPR
          repositories: REPOSITORY_EXPR
      - name: validate
        env:
          GITHUB_TOKEN: GITHUB_TOKEN_EXPR
          MERGE_AUTH_TOKEN: MERGE_TOKEN_EXPR
          GITHUB_EVENT_PATH: EVENT_PATH_EXPR
          MERGE_AUTHORIZER_LOGINS: LOGINS_EXPR
        run: python3 scripts/authorize_merge.py
"""
        for source, replacement in (
            ("DEFAULT_BRANCH_EXPR", "$" + "{{ github.event.repository.default_branch }}"),
            ("PREFLIGHT_OUTPUT", "$" + "{{ steps.preflight.outputs.authorized }}"),
            ("PREFLIGHT_JOB_CONDITION", "needs.preflight.outputs.authorized == 'true'"),
            ("GITHUB_TOKEN_EXPR", "$" + "{{ secrets.GITHUB_TOKEN }}"),
            ("MERGE_TOKEN_EXPR", "$" + "{{ steps.status-token.outputs.token }}"),
            ("EVENT_PATH_EXPR", "$" + "{{ github.event_path }}"),
            ("LOGINS_EXPR", "$" + "{{ vars.MERGE_AUTHORIZER_LOGINS }}"),
            ("APP_CLIENT_ID_EXPR", "$" + "{{ vars.MERGE_AUTH_APP_CLIENT_ID }}"),
            ("APP_PRIVATE_KEY_EXPR", "$" + "{{ secrets.MERGE_AUTH_APP_PRIVATE_KEY }}"),
            ("OWNER_EXPR", "$" + "{{ github.repository_owner }}"),
            ("REPOSITORY_EXPR", "$" + "{{ github.event.repository.name }}"),
        ):
            content = content.replace(source, replacement)
        return content

    def test_trusted_authorizer_requires_separate_app_token_and_read_only_github_token(self):
        content = self.trusted_authorizer_workflow_fixture()
        self.assertEqual(
            hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content),
            [],
        )

    def test_token_creation_job_itself_requires_authorized_preflight(self):
        content = self.trusted_authorizer_workflow_fixture().replace(
            "if: needs.preflight.outputs.authorized == 'true'",
            "if: always()",
        )
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content)
        self.assertTrue(any("environment-protected authorization job must run only after an authorized preflight output" in error for error in errors))

    def test_authorization_job_requires_preflight_dependency(self):
        content = self.trusted_authorizer_workflow_fixture().replace("    needs: preflight\n", "    needs: []\n")
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content)
        self.assertTrue(any("environment-protected authorization job must run only after an authorized preflight output" in error for error in errors))

    def test_github_token_status_write_is_rejected_even_in_trusted_workflow(self):
        content = """permissions:
  contents: read
  pull-requests: read
  statuses: "write"
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
        content = self.trusted_authorizer_workflow_fixture().replace(
            "jobs:",
            "  pull_request:\\n    types: [opened]\\njobs:",
            1,
        )
        errors = hygiene.workflow_policy_errors(Path(".github/workflows/merge-authorization.yml"), content)
        self.assertTrue(any("must trigger only on issue_comment" in error for error in errors))

    def test_only_trusted_authorizer_may_reference_app_key_environment(self):
        trusted = """permissions:
  contents: read
  pull-requests: read
jobs:
  authorize:
    environment:
      name: merge-authorizer
"""
        self.assertEqual(
            hygiene.workflow_environment_errors(Path(".github/workflows/merge-authorization.yml"), trusted),
            [],
        )
        untrusted = """permissions:
  contents: read
jobs:
  deploy:
    environment: merge-authorizer
"""
        errors = hygiene.workflow_environment_errors(Path(".github/workflows/untrusted.yml"), untrusted)
        self.assertTrue(any("only the trusted authorization workflow" in error for error in errors))

    def test_untrusted_workflow_cannot_construct_dynamic_environment_name(self):
        content = """permissions:
  contents: read
jobs:
  deploy:
    environment:
      name: ENV_EXPR
"""
        content = content.replace("ENV_EXPR", "$" + "{{ vars.DEPLOY_ENV }}")
        errors = hygiene.workflow_environment_errors(Path(".github/workflows/untrusted.yml"), content)
        self.assertTrue(any("dynamic environment names" in error for error in errors))

    def test_other_static_deployment_environments_remain_allowed(self):
        content = """permissions:
  contents: read
jobs:
  deploy:
    environment: staging
"""
        self.assertEqual(
            hygiene.workflow_environment_errors(Path(".github/workflows/deploy.yml"), content),
            [],
        )

    def test_trusted_authorizer_requires_literal_environment_name(self):
        content = """permissions:
  contents: read
jobs:
  authorize:
    environment:
      name: ENV_EXPR
"""
        content = content.replace("ENV_EXPR", "$" + "{{ vars.MERGE_ENV }}")
        errors = hygiene.workflow_environment_errors(Path(".github/workflows/merge-authorization.yml"), content)
        self.assertTrue(any("must use exactly one literal merge-authorizer environment" in error for error in errors))
        self.assertTrue(any("must not be dynamically constructed" in error for error in errors))

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
            "\n".join(f"## {section}" for section in hygiene.REQUIRED_ASSURANCE_SECTIONS)
            + "\n\n[Setup guide](docs/EXACT_HEAD_AUTHORIZATION_SETUP.md)\n\nBefore high-impact merges, create a recoverable snapshot of the exact pre-merge head and record the rollback route.\n",
            encoding="utf-8",
        )
        for path, reference in hygiene.ASSURANCE_REFERENCES.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"[Assurance]({reference})\n", encoding="utf-8")

    def test_complete_assurance_contract_passes(self):
        self.write_valid_fixture()
        self.assertEqual(hygiene.assurance_document_errors(self.root), [])

    def test_missing_verified_pre_merge_snapshot_requirement_is_rejected(self):
        self.write_valid_fixture()
        path = self.root / "MERGE_AND_CHANGE_ASSURANCE.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace(
            "recoverable snapshot of the exact pre-merge head",
            "backup where practical",
        )
        path.write_text(content, encoding="utf-8")
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("recoverable snapshot of the exact pre-merge head" in error for error in errors))

    def test_missing_authorization_setup_guide_is_rejected(self):
        self.write_valid_fixture()
        (self.root / "docs/EXACT_HEAD_AUTHORIZATION_SETUP.md").unlink()
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("EXACT_HEAD_AUTHORIZATION_SETUP.md: required governing document is missing" in error for error in errors))

    def test_canonical_standard_must_link_to_authorization_setup_guide(self):
        self.write_valid_fixture()
        path = self.root / "MERGE_AND_CHANGE_ASSURANCE.md"
        content = path.read_text(encoding="utf-8").replace(
            "[Setup guide](docs/EXACT_HEAD_AUTHORIZATION_SETUP.md)",
            "docs/EXACT_HEAD_AUTHORIZATION_SETUP.md",
        )
        path.write_text(content, encoding="utf-8")
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("must link to docs/EXACT_HEAD_AUTHORIZATION_SETUP.md" in error for error in errors))

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

    def test_headings_and_links_inside_html_comments_do_not_satisfy_contract(self):
        self.write_valid_fixture()
        standard = self.root / "MERGE_AND_CHANGE_ASSURANCE.md"
        content = standard.read_text(encoding="utf-8").replace(
            "## 4. Five-perspective assessment",
            "<!--\n## 4. Five-perspective assessment\n-->",
        )
        standard.write_text(content, encoding="utf-8")
        agents = self.root / "AGENTS.md"
        agents.write_text("<!--\n[Assurance](MERGE_AND_CHANGE_ASSURANCE.md)\n-->\n", encoding="utf-8")
        errors = hygiene.assurance_document_errors(self.root)
        self.assertTrue(any("Five-perspective assessment" in error for error in errors))
        self.assertTrue(any("AGENTS.md" in error and "Markdown link" in error for error in errors))

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
