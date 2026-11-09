"""Unit tests for exact-head maintainer authorization policy."""
import base64
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "authorize_merge.py"
SPEC = importlib.util.spec_from_file_location("authorize_merge", SCRIPT)
auth = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(auth)

BASE = "a" * 40
HEAD = "b" * 40
PARENT = "c" * 40
EVIDENCE_PATH = "reviews/PR-12.md"


def valid_pr():
    return {
        "state": "open",
        "draft": False,
        "base": {"ref": "main", "sha": BASE},
        "head": {"sha": HEAD},
    }


def commit_response(path=EVIDENCE_PATH, parents=None):
    return {
        "sha": HEAD,
        "parents": parents if parents is not None else [{"sha": PARENT}],
        "files": [{"filename": path, "status": "added"}],
    }


def content_response(text="evidence record"):
    return {
        "type": "file",
        "encoding": "base64",
        "size": len(text.encode("utf-8")),
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
    }


class AuthorizationPolicyTests(unittest.TestCase):
    def test_user_repository_owner_is_default_authorizer(self):
        allowed = auth.authorized_logins({"owner": {"type": "User", "login": "maintainer"}}, "")
        self.assertEqual(allowed, {"maintainer"})

    def test_organization_requires_explicit_allowlist(self):
        with self.assertRaises(auth.AuthorizationError):
            auth.authorized_logins({"owner": {"type": "Organization", "login": "example"}}, "")

    def test_configured_allowlist_is_case_insensitive(self):
        allowed = auth.authorized_logins({"owner": {"type": "Organization", "login": "example"}}, "Alice, BOB")
        self.assertEqual(allowed, {"alice", "bob"})

    def test_graphql_errors_fail_closed(self):
        with patch.object(auth, "api_request", return_value={"errors": [{"message": "partial response"}]}):
            with self.assertRaises(auth.AuthorizationError):
                auth.unresolved_threads("owner", "repo", 1, "token")

    def test_unresolved_review_thread_blocks_authorization(self):
        payload = {"data": {"repository": {"pullRequest": {"reviewThreads": {
            "nodes": [{"isResolved": False}],
            "pageInfo": {"hasNextPage": False},
        }}}}}
        with patch.object(auth, "api_request", return_value=payload):
            self.assertTrue(auth.unresolved_threads("owner", "repo", 1, "token"))

    def test_all_resolved_review_threads_allow_progress(self):
        payload = {"data": {"repository": {"pullRequest": {"reviewThreads": {
            "nodes": [{"isResolved": True}],
            "pageInfo": {"hasNextPage": False},
        }}}}}
        with patch.object(auth, "api_request", return_value=payload):
            self.assertFalse(auth.unresolved_threads("owner", "repo", 1, "token"))

    def test_only_full_sha_command_is_accepted(self):
        self.assertIsNotNone(auth.COMMAND_RE.fullmatch("/authorize-merge " + "a" * 40))
        self.assertIsNotNone(auth.COMMAND_RE.fullmatch("/authorize-policy-change " + "c" * 40))
        self.assertIsNotNone(auth.COMMAND_RE.fullmatch("/revoke-merge " + "b" * 40))
        self.assertIsNone(auth.COMMAND_RE.fullmatch("/authorize-merge abc"))

    def test_exact_head_evidence_is_fetched_as_inert_api_data(self):
        with patch.object(auth, "api_request", side_effect=[commit_response(), content_response()]) as api, \
             patch.object(auth, "validate_record", return_value=[]) as validator:
            parent, record = auth.verify_evidence("owner", "repo", 12, valid_pr(), "read-token")
        self.assertEqual(parent, PARENT)
        self.assertEqual(record, "evidence record")
        self.assertEqual(api.call_count, 2)
        self.assertEqual(api.call_args_list[0].args, ("GET", f"/repos/owner/repo/commits/{HEAD}", "read-token"))
        self.assertIn(f"ref={HEAD}", api.call_args_list[1].args[1])
        validator.assert_called_once_with("evidence record", 12, "main", BASE, PARENT)

    def test_evidence_commit_must_have_exactly_one_parent(self):
        with patch.object(auth, "api_request", return_value=commit_response(parents=[{"sha": PARENT}, {"sha": BASE}])):
            with self.assertRaisesRegex(auth.AuthorizationError, "exactly one parent"):
                auth.verify_evidence("owner", "repo", 12, valid_pr(), "read-token")

    def test_evidence_commit_must_change_only_the_pr_record(self):
        with patch.object(auth, "api_request", return_value=commit_response(path="scripts/authorize_merge.py")):
            with self.assertRaisesRegex(auth.AuthorizationError, "must add or update only"):
                auth.verify_evidence("owner", "repo", 12, valid_pr(), "read-token")

    def test_evidence_content_must_be_base64(self):
        bad_content = {"type": "file", "encoding": "utf-8", "size": 10, "content": "not base64"}
        with patch.object(auth, "api_request", side_effect=[commit_response(), bad_content]):
            with self.assertRaisesRegex(auth.AuthorizationError, "base64 content"):
                auth.verify_evidence("owner", "repo", 12, valid_pr(), "read-token")

    def test_invalid_evidence_record_blocks_authorization(self):
        with patch.object(auth, "api_request", side_effect=[commit_response(), content_response()]), \
             patch.object(auth, "validate_record", return_value=["critical blocker remains"]):
            with self.assertRaisesRegex(auth.AuthorizationError, "critical blocker remains"):
                auth.verify_evidence("owner", "repo", 12, valid_pr(), "read-token")

    def test_invalid_base_sha_fails_closed(self):
        pr = valid_pr()
        pr["base"]["sha"] = "not-a-sha"
        with self.assertRaisesRegex(auth.AuthorizationError, "valid full base/head SHAs"):
            auth.verify_evidence("owner", "repo", 12, pr, "read-token")

    def test_trusted_policy_file_changes_require_manual_review(self):
        changed = [
            {"filename": ".github/workflows/new-workflow.yml"},
            {"filename": "scripts/authorize_merge.py"},
            {"filename": "MERGE_AND_CHANGE_ASSURANCE.md"},
            {"filename": "GOVERNANCE.md"},
            {"filename": "CODEOWNERS"},
            {"filename": "SECURITY.md"},
            {"filename": "CHATGPT_ONBOARDING.md"},
            {"filename": "START_HERE.md"},
            {"filename": "INCIDENT_RESPONSE.md"},
            {"filename": "docs/DEVELOPMENT_WORKFLOW.md"},
            {"filename": "docs/HANDOVER_TEMPLATE.md"},
            {"filename": "docs/TEMPLATE_UPDATE_GUIDE.md"},
            {"filename": ".gitleaks.toml"},
        ]
        with patch.object(auth, "api_request", return_value=changed):
            protected = auth.reject_policy_changes("owner", "repo", 12, "read-token")
        self.assertEqual(protected, sorted(item["filename"] for item in changed))

    def test_renaming_a_protected_file_outside_its_path_still_requires_policy_review(self):
        changed = [
            {
                "filename": "scripts/legacy_authorizer.py",
                "previous_filename": "scripts/authorize_merge.py",
                "status": "renamed",
            },
            {
                "filename": "workflows/legacy.yml",
                "previous_filename": ".github/workflows/merge-authorization.yml",
                "status": "renamed",
            },
            {
                "filename": "docs/owners.md",
                "previous_filename": "CODEOWNERS",
                "status": "renamed",
            },
        ]
        with patch.object(auth, "api_request", return_value=changed):
            protected = auth.reject_policy_changes("owner", "repo", 12, "read-token")
        self.assertEqual(
            protected,
            [".github/workflows/merge-authorization.yml", "CODEOWNERS", "scripts/authorize_merge.py"],
        )

    def test_ordinary_source_and_documentation_changes_do_not_trigger_policy_block(self):
        changed = [
            {"filename": "src/application.py"},
            {"filename": "README.md"},
            {"filename": "docs/USER_GUIDE.md"},
        ]
        with patch.object(auth, "api_request", return_value=changed):
            self.assertEqual(auth.reject_policy_changes("owner", "repo", 12, "read-token"), [])

    def test_ordinary_authorization_rejects_protected_policy_changes(self):
        with self.assertRaisesRegex(auth.AuthorizationError, "use /authorize-policy-change"):
            auth.enforce_policy_change_command("authorize-merge", ["GOVERNANCE.md"])

    def test_policy_change_command_requires_protected_policy_changes(self):
        with self.assertRaisesRegex(auth.AuthorizationError, "use /authorize-merge"):
            auth.enforce_policy_change_command("authorize-policy-change", [])

    def test_policy_change_command_accepts_protected_paths_for_deeper_evidence_review(self):
        auth.enforce_policy_change_command("authorize-policy-change", ["GOVERNANCE.md"])

    def test_policy_change_record_requires_exact_paths_base_and_approval(self):
        record = f"""## Change identity
- Risk: HIGH

## Protected policy change review
- Changed policy paths: .github/workflows/policy.yml, GOVERNANCE.md
- Base SHA: {BASE}
- Reason for change: Close a documented workflow trust-boundary gap.
- Adversarial tests: Fork and same-repository PR cases plus validator-tampering tests.
- Rollback/recovery: Revert the dedicated policy commit and restore the previous ruleset.
- Independent review reference: independent technical review report and exact-head test run.
- Owner decision: APPROVED
"""
        auth.validate_policy_change_record(
            record,
            [".github/workflows/policy.yml", "GOVERNANCE.md"],
            BASE,
        )

    def test_policy_change_record_rejects_missing_paths_or_unapproved_owner_decision(self):
        record = f"""## Change identity
- Risk: HIGH

## Protected policy change review
- Changed policy paths: GOVERNANCE.md
- Base SHA: {BASE}
- Reason for change: Update governance policy with explicit rationale.
- Adversarial tests: Fork and same-repository workflow spoof tests executed.
- Rollback/recovery: Revert the policy commit and restore the previous gate.
- Independent review reference: independent technical review report and exact-head test evidence.
- Owner decision: PENDING
"""
        with self.assertRaisesRegex(auth.AuthorizationError, "must list every protected path"):
            auth.validate_policy_change_record(record, ["GOVERNANCE.md", "SECURITY.md"], BASE)

        record = record.replace("GOVERNANCE.md", "GOVERNANCE.md, SECURITY.md")
        record = record.replace("Owner decision: PENDING", "Owner decision: APPROVED")
        auth.validate_policy_change_record(record, ["GOVERNANCE.md", "SECURITY.md"], BASE)

    def test_fenced_policy_change_fields_cannot_satisfy_the_gate(self):
        record = """~~~markdown
## Protected policy change review
- Changed policy paths: GOVERNANCE.md
- Base SHA: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
- Reason for change: This is only an example in a code fence.
- Adversarial tests: These are not executed tests.
- Rollback/recovery: These are not recovery steps.
- Independent review reference: This is not a real report.
- Owner decision: APPROVED
~~~"""
        with self.assertRaisesRegex(auth.AuthorizationError, "exactly one Protected policy change review"):
            auth.validate_policy_change_record(record, ["GOVERNANCE.md"], BASE)

    def test_policy_change_record_rejects_low_risk_classification(self):
        record = f"""## Change identity
- Risk: LOW

## Protected policy change review
- Changed policy paths: GOVERNANCE.md
- Base SHA: {BASE}
- Reason for change: Update governance policy with explicit rationale.
- Adversarial tests: Fork and same-repository workflow spoof tests executed.
- Rollback/recovery: Revert the policy commit and restore the previous gate.
- Independent review reference: independent technical review report and exact-head test evidence.
- Owner decision: APPROVED
"""
        with self.assertRaisesRegex(auth.AuthorizationError, "HIGH or CRITICAL"):
            auth.validate_policy_change_record(record, ["GOVERNANCE.md"], BASE)

    def test_policy_change_record_rejects_stale_base_sha(self):
        record = f"""## Change identity
- Risk: HIGH

## Protected policy change review
- Changed policy paths: GOVERNANCE.md
- Base SHA: {"d" * 40}
- Reason for change: Update governance.
- Adversarial tests: Tests run.
- Rollback/recovery: Revert.
- Independent review reference: report #1.
- Owner decision: APPROVED
"""
        with self.assertRaisesRegex(auth.AuthorizationError, "base SHA does not match"):
            auth.validate_policy_change_record(record, ["GOVERNANCE.md"], BASE)

    def test_incomplete_pr_file_listing_fails_closed(self):
        with patch.object(auth, "api_request", return_value=[{"filename": f"file-{i}.txt"} for i in range(100)]):
            with self.assertRaisesRegex(auth.AuthorizationError, "completely enumerate PR files"):
                auth.reject_policy_changes("owner", "repo", 12, "read-token")

    def test_authorized_preflight_runs_before_status_token_creation(self):
        event = {
            "issue": {"number": 12, "pull_request": {"url": "https://api.github.com/repos/owner/repo/pulls/12"}},
            "comment": {"body": "/authorize-merge " + HEAD, "user": {"login": "maintainer"}},
            "repository": {"owner": {"type": "User", "login": "maintainer"}},
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as event_file, \
             tempfile.NamedTemporaryFile("r", encoding="utf-8", delete=False) as output_file:
            json.dump(event, event_file)
            event_path, output_path = event_file.name, output_file.name
        try:
            with patch.dict(os.environ, {
                "GITHUB_EVENT_PATH": event_path,
                "GITHUB_OUTPUT": output_path,
                "MERGE_AUTHORIZER_LOGINS": "",
            }):
                self.assertEqual(auth.preflight(), 0)
            self.assertIn("authorized=true", Path(output_path).read_text(encoding="utf-8"))
        finally:
            Path(event_path).unlink(missing_ok=True)
            Path(output_path).unlink(missing_ok=True)

    def test_unauthorized_preflight_does_not_enable_status_token(self):
        event = {
            "issue": {"number": 12, "pull_request": {"url": "https://api.github.com/repos/owner/repo/pulls/12"}},
            "comment": {"body": "/authorize-merge " + HEAD, "user": {"login": "outsider"}},
            "repository": {"owner": {"type": "User", "login": "maintainer"}},
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as event_file, \
             tempfile.NamedTemporaryFile("r", encoding="utf-8", delete=False) as output_file:
            json.dump(event, event_file)
            event_path, output_path = event_file.name, output_file.name
        try:
            with patch.dict(os.environ, {
                "GITHUB_EVENT_PATH": event_path,
                "GITHUB_OUTPUT": output_path,
                "MERGE_AUTHORIZER_LOGINS": "",
            }):
                self.assertEqual(auth.preflight(), 0)
            self.assertIn("authorized=false", Path(output_path).read_text(encoding="utf-8"))
        finally:
            Path(event_path).unlink(missing_ok=True)
            Path(output_path).unlink(missing_ok=True)

    def test_policy_change_template_has_fail_closed_defaults(self):
        template = (Path(__file__).resolve().parents[1] / "docs" / "PR_ASSURANCE_RECORD_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertEqual(template.count("## Protected policy change review"), 1)
        self.assertIn("- Owner decision: NOT APPLICABLE", template)
        for field in (
            "- Changed policy paths: TBD",
            "- Base SHA: TBD",
            "- Reason for change: TBD",
            "- Adversarial tests: TBD",
            "- Rollback/recovery: TBD",
            "- Independent review reference: TBD",
        ):
            self.assertIn(field, template)

    def test_untrusted_pr_checkout_evidence_workflow_is_absent(self):
        workflow_dir = Path(__file__).resolve().parents[1] / ".github" / "workflows"
        self.assertFalse((workflow_dir / "merge-evidence.yml").exists())

    def test_workflow_uses_trusted_default_branch_and_isolated_status_app(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "merge-authorization.yml").read_text(encoding="utf-8")
        self.assertIn("issue_comment:", workflow)
        self.assertIn("ref: " + "$" + "{{ github.event.repository.default_branch }}", workflow)
        self.assertIn("name: merge-authorizer", workflow)
        self.assertIn("run: python3 scripts/authorize_merge.py --preflight", workflow)
        self.assertIn("/authorize-policy-change ", workflow)
        self.assertIn("if: steps.preflight.outputs.authorized == 'true'", workflow)
        self.assertLess(workflow.index("--preflight"), workflow.index("actions/create-github-app-token"))
        self.assertIn("actions/create-github-app-token@64ab729a6294000f5aa4a4bc0b73d1f32bc45510", workflow)
        self.assertIn("permission-statuses: write", workflow)
        self.assertIn("skip-token-revoke: false", workflow)
        self.assertIn("MERGE_AUTH_TOKEN:", workflow)
        self.assertNotIn("statuses: write", workflow.split("jobs:", 1)[0])
        self.assertNotIn("github.event.pull_request.head.sha", workflow)
        self.assertNotIn("pull_request_target:", workflow)


if __name__ == "__main__":
    unittest.main()
