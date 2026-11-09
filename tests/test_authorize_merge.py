"""Unit tests for exact-head maintainer authorization policy."""
import base64
import importlib.util
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
        self.assertIsNotNone(auth.COMMAND_RE.fullmatch("/revoke-merge " + "b" * 40))
        self.assertIsNone(auth.COMMAND_RE.fullmatch("/authorize-merge abc"))

    def test_exact_head_evidence_is_fetched_as_inert_api_data(self):
        with patch.object(auth, "api_request", side_effect=[commit_response(), content_response()]) as api, \
             patch.object(auth, "validate_record", return_value=[]) as validator:
            parent = auth.verify_evidence("owner", "repo", 12, valid_pr(), "read-token")
        self.assertEqual(parent, PARENT)
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
            with self.assertRaisesRegex(auth.AuthorizationError, "must change exactly one evidence file"):
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

    def test_workflow_uses_trusted_default_branch_and_isolated_status_app(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "merge-authorization.yml").read_text(encoding="utf-8")
        self.assertIn("issue_comment:", workflow)
        self.assertIn("ref: " + "$" + "{{ github.event.repository.default_branch }}", workflow)
        self.assertIn("name: merge-authorizer", workflow)
        self.assertIn("actions/create-github-app-token@64ab729a6294000f5aa4a4bc0b73d1f32bc45510", workflow)
        self.assertIn("permission-statuses: write", workflow)
        self.assertIn("MERGE_AUTH_TOKEN:", workflow)
        self.assertNotIn("statuses: write", workflow.split("jobs:", 1)[0])
        self.assertNotIn("github.event.pull_request.head.sha", workflow)
        self.assertNotIn("pull_request_target:", workflow)


if __name__ == "__main__":
    unittest.main()
