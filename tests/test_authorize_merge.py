"""Unit tests for exact-head maintainer authorization policy."""
import importlib.util
import unittest
from unittest.mock import patch
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "authorize_merge.py"
SPEC = importlib.util.spec_from_file_location("authorize_merge", SCRIPT)
auth = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(auth)

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

if __name__ == "__main__":
    unittest.main()
