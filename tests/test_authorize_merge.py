"""Unit tests for exact-head maintainer authorization policy."""
import importlib.util
import unittest
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

    def test_only_full_sha_command_is_accepted(self):
        self.assertIsNotNone(auth.COMMAND_RE.fullmatch("/authorize-merge " + "a" * 40))
        self.assertIsNotNone(auth.COMMAND_RE.fullmatch("/revoke-merge " + "b" * 40))
        self.assertIsNone(auth.COMMAND_RE.fullmatch("/authorize-merge abc"))

if __name__ == "__main__":
    unittest.main()
