#!/usr/bin/env python3
"""Validate trusted PR evidence and publish an exact-head owner authorization.

The workflow runs from the trusted default branch on issue_comment. PR files are
read through the GitHub API as inert data; no PR code or validator is executed.
The status is published by a separate GitHub App identity, never GITHUB_TOKEN.
"""
from __future__ import annotations

import base64
import binascii
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from check_merge_evidence import section, strip_fenced_code_blocks, validate_record

API = "https://api.github.com"
CONTEXT = "Explicit maintainer merge authorization"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
COMMAND_RE = re.compile(r"^/(authorize-merge|authorize-policy-change|revoke-merge)\s+([0-9a-f]{40})\s*$")
MAX_EVIDENCE_BYTES = 1_000_000


class AuthorizationError(RuntimeError):
    pass


def api_request(method: str, path: str, token: str, payload: dict | None = None) -> dict | list:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise AuthorizationError(f"GitHub API returned HTTP {exc.code}: {detail}") from exc


def authorized_logins(repository: dict, configured: str) -> set[str]:
    if configured.strip():
        return {item.strip().lower() for item in configured.split(",") if item.strip()}
    owner = repository.get("owner", {})
    if owner.get("type") == "User" and owner.get("login"):
        return {owner["login"].lower()}
    raise AuthorizationError(
        "Set the repository variable MERGE_AUTHORIZER_LOGINS to an explicit comma-separated maintainer allowlist."
    )


def unresolved_threads(owner: str, repo: str, number: int, token: str) -> bool:
    query = """query($owner:String!, $repo:String!, $number:Int!) {
      repository(owner:$owner, name:$repo) {
        pullRequest(number:$number) {
          reviewThreads(first:100) {
            nodes { isResolved }
            pageInfo { hasNextPage }
          }
        }
      }
    }"""
    result = api_request("POST", "/graphql", token, {
        "query": query,
        "variables": {"owner": owner, "repo": repo, "number": number},
    })
    if result.get("errors"):
        raise AuthorizationError("GitHub GraphQL returned errors; refusing to authorize.")
    try:
        threads = result["data"]["repository"]["pullRequest"]["reviewThreads"]
    except (KeyError, TypeError) as exc:
        raise AuthorizationError(
            "Could not verify pull-request review threads; authorization fails closed."
        ) from exc
    if threads["pageInfo"]["hasNextPage"]:
        raise AuthorizationError(
            "More than 100 review threads exist; resolve and inspect them before authorization."
        )
    return any(not node["isResolved"] for node in threads["nodes"])


PROTECTED_POLICY_PATHS = {
    "AGENTS.md",
    "AI_SAFETY_AND_MODEL_SPEC.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "MERGE_AND_CHANGE_ASSURANCE.md",
    "PRIVACY_AND_PUBLICATION.md",
    "PROJECT_RISK_AND_RELEASE_READINESS.md",
    "SECURITY.md",
    "UPDATE_AND_RELEASE_SECURITY.md",
    "docs/DEVELOPMENT_WORKFLOW.md",
    "docs/INDEPENDENT_AGENT_REVIEW.md",
    "docs/PR_ASSURANCE_RECORD_TEMPLATE.md",
    "docs/PRIVATE_GITHUB_SETUP.md",
    "docs/REVIEW_CHECKLIST.md",
    "scripts/authorize_merge.py",
    "scripts/check_merge_evidence.py",
    "scripts/check_repo_hygiene.py",
    "tests/test_authorize_merge.py",
    "tests/test_check_merge_evidence.py",
    "tests/test_check_repo_hygiene.py",
    ".gitleaks.toml",
    ".gitleaksignore",
    "gitleaks.toml",
    "gitleaksignore",
    ".secretlintignore",
    ".trufflehog.yml",
}


def reject_policy_changes(owner: str, repo: str, number: int, token: str) -> list[str]:
    """Return protected policy paths; caller selects the explicit policy-change route."""
    files = api_request(
        "GET",
        f"/repos/{owner}/{repo}/pulls/{number}/files?per_page=100",
        token,
    )
    if not isinstance(files, list) or len(files) >= 100:
        raise AuthorizationError("Could not completely enumerate PR files; policy-change check fails closed.")
    protected = []
    for item in files:
        path = item.get("filename", "")
        if path.startswith(".github/") or path in PROTECTED_POLICY_PATHS:
            protected.append(path)
    return sorted(set(protected))


def enforce_policy_change_command(command: str, protected_paths: list[str]) -> None:
    if command == "authorize-policy-change" and not protected_paths:
        raise AuthorizationError("No protected policy files changed; use /authorize-merge for an ordinary PR.")
    if command == "authorize-merge" and protected_paths:
        raise AuthorizationError(
            "This PR changes protected policy files; use /authorize-policy-change with the additional evidence fields: "
            + ", ".join(protected_paths)
        )


def validate_policy_change_record(record: str, protected_paths: list[str], base_sha: str) -> None:
    """Require explicit, evidence-backed owner review for protected policy changes."""
    clean = strip_fenced_code_blocks(record)
    headings = re.findall(r"^## Protected policy change review\s*$", clean, re.MULTILINE)
    if len(headings) != 1:
        raise AuthorizationError("Policy-change evidence must contain exactly one Protected policy change review section.")
    policy_section = section(clean, "## Protected policy change review")

    def unique_field(name: str) -> str:
        matches = re.findall(rf"(?m)^-\s*{re.escape(name)}:\s*(.*?)\s*$", policy_section)
        if len(matches) != 1:
            raise AuthorizationError(f"Policy-change evidence must contain exactly one '{name}' field.")
        return matches[0].strip().strip(chr(96))

    listed_paths = [item.strip().strip(chr(96)) for item in unique_field("Changed policy paths").split(",") if item.strip()]
    if len(listed_paths) != len(set(listed_paths)) or set(listed_paths) != set(protected_paths):
        raise AuthorizationError("Policy-change evidence must list every protected path exactly once.")
    if unique_field("Base SHA") != base_sha:
        raise AuthorizationError("Policy-change evidence base SHA does not match the current PR base.")
    for name in ("Reason for change", "Adversarial tests", "Rollback/recovery", "Independent review reference"):
        value = unique_field(name)
        if len(value) < 12 or value.lower() in {"todo", "tbd", "n/a", "none", "pending"}:
            raise AuthorizationError(f"Policy-change evidence field '{name}' must contain concrete evidence.")
    if unique_field("Owner decision") != "APPROVED":
        raise AuthorizationError("Policy-change evidence must state Owner decision: APPROVED.")


def verify_evidence(owner: str, repo: str, number: int, pr: dict, token: str) -> tuple[str, str]:
    """Validate the exact-head evidence file using trusted validator code.

    The PR's head commit must be a single-parent, evidence-only commit. The
    evidence file is fetched by exact SHA through the API and treated only as
    text. No PR checkout, import, script, workflow, or executable content runs.
    Returns the parent SHA whose code was reviewed.
    """
    current_sha = pr.get("head", {}).get("sha", "")
    base_ref = pr.get("base", {}).get("ref", "")
    base_sha = pr.get("base", {}).get("sha", "")
    if not SHA_RE.fullmatch(current_sha) or not SHA_RE.fullmatch(base_sha):
        raise AuthorizationError("PR metadata did not contain valid full base/head SHAs.")

    commit = api_request("GET", f"/repos/{owner}/{repo}/commits/{current_sha}", token)
    if commit.get("sha") != current_sha:
        raise AuthorizationError("GitHub commit response did not match the exact current PR head.")
    parents = commit.get("parents")
    if not isinstance(parents, list) or len(parents) != 1:
        raise AuthorizationError("The evidence-only head commit must have exactly one parent.")
    reviewed_code_sha = parents[0].get("sha", "")
    if not SHA_RE.fullmatch(reviewed_code_sha):
        raise AuthorizationError("The evidence-only commit parent SHA is invalid.")

    expected_path = f"reviews/PR-{number}.md"
    changed_files = commit.get("files")
    if not isinstance(changed_files, list) or len(changed_files) != 1:
        raise AuthorizationError("The PR head commit must change exactly one evidence file.")
    changed = changed_files[0]
    if changed.get("filename") != expected_path or changed.get("status") not in {"added", "modified"}:
        raise AuthorizationError(
            f"The PR head commit must add or update only {expected_path}; no code changes may follow the evidence record."
        )

    encoded_path = quote(expected_path, safe="/")
    file_data = api_request(
        "GET",
        f"/repos/{owner}/{repo}/contents/{encoded_path}?ref={current_sha}",
        token,
    )
    if file_data.get("type") != "file" or file_data.get("encoding") != "base64":
        raise AuthorizationError("GitHub did not return the evidence file as base64 content.")
    if file_data.get("size", MAX_EVIDENCE_BYTES + 1) > MAX_EVIDENCE_BYTES:
        raise AuthorizationError("The evidence file exceeds the 1 MB validation limit.")
    encoded = re.sub(r"\s+", "", file_data.get("content", ""))
    if not encoded:
        raise AuthorizationError("The exact-head evidence file is empty or unavailable.")
    try:
        record = base64.b64decode(encoded, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise AuthorizationError("The exact-head evidence file is not valid base64 UTF-8.") from exc

    errors = validate_record(record, number, base_ref, base_sha, reviewed_code_sha)
    if errors:
        raise AuthorizationError("Evidence validation failed: " + "; ".join(errors[:3]))
    return reviewed_code_sha, record


def publish_status(
    owner: str,
    repo: str,
    sha: str,
    token: str,
    state: str,
    description: str,
    target_url: str | None = None,
) -> None:
    payload = {
        "state": state,
        "context": CONTEXT,
        "description": description[:140],
    }
    if target_url and target_url.startswith("https://github.com/"):
        payload["target_url"] = target_url
    api_request("POST", f"/repos/{owner}/{repo}/statuses/{sha}", token, payload)


def write_preflight_output(authorized: bool) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as handle:
            handle.write(f"authorized={'true' if authorized else 'false'}\n")


def preflight() -> int:
    """Check the comment author before the workflow loads the App private key."""
    try:
        with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as handle:
            event = json.load(handle)
        issue = event.get("issue", {})
        comment = event.get("comment", {})
        if not issue.get("pull_request") or not COMMAND_RE.fullmatch(comment.get("body", "").strip()):
            write_preflight_output(False)
            print("No valid PR authorization command; no status App token will be created.")
            return 0
        allowed = authorized_logins(
            event["repository"],
            os.getenv("MERGE_AUTHORIZER_LOGINS", ""),
        )
        actor = comment.get("user", {}).get("login", "").lower()
        authorized = actor in allowed
        write_preflight_output(authorized)
        if not authorized:
            print("Comment author is not an authorized maintainer; no status App token will be created.")
        return 0
    except (AuthorizationError, KeyError, TypeError, ValueError, OSError) as exc:
        write_preflight_output(False)
        print(f"Authorization preflight failed closed: {exc}", file=sys.stderr)
        return 0


def main() -> int:
    event_path = os.environ["GITHUB_EVENT_PATH"]
    read_token = os.environ["GITHUB_TOKEN"]
    status_token = os.environ["MERGE_AUTH_TOKEN"]
    with open(event_path, encoding="utf-8") as handle:
        event = json.load(handle)

    issue = event.get("issue", {})
    if not issue.get("pull_request"):
        raise AuthorizationError("The command must be posted on a pull request.")
    comment = event.get("comment", {})
    match = COMMAND_RE.fullmatch(comment.get("body", "").strip())
    if not match:
        print("No recognized exact-head authorization command; no status changed.")
        return 0

    repository = event["repository"]
    owner = repository["owner"]["login"]
    repo = repository["name"]
    number = int(issue["number"])
    actor = comment.get("user", {}).get("login", "").lower()
    command, requested_sha = match.groups()
    allowed = authorized_logins(repository, os.getenv("MERGE_AUTHORIZER_LOGINS", ""))
    if actor not in allowed:
        raise AuthorizationError("Comment author is not an authorized maintainer; no status was changed.")

    pr = api_request("GET", f"/repos/{owner}/{repo}/pulls/{number}", read_token)
    current_sha = pr.get("head", {}).get("sha", "")
    if not SHA_RE.fullmatch(current_sha):
        raise AuthorizationError("GitHub did not return a valid current head SHA.")

    # Reset any previous success before revalidating this authorization request.
    # If later API/evidence validation fails, the status remains blocked.
    target_url = comment.get("html_url")
    publish_status(
        owner, repo, current_sha, status_token, "pending",
        "Revalidating exact PR head, evidence, review threads and owner authorization.",
        target_url,
    )

    state = "failure"
    description = "Authorization was not granted."
    if command == "revoke-merge":
        description = (
            "Maintainer revoked authorization for this exact PR head."
            if requested_sha == current_sha
            else "Revocation request SHA was stale; current head remains unauthorized."
        )
    elif requested_sha != current_sha:
        description = "Authorization SHA did not match the current PR head; authorize the new exact SHA."
    elif pr.get("state") != "open" or pr.get("draft"):
        description = "Pull request must be open and ready for review."
    elif pr.get("base", {}).get("ref") != repository.get("default_branch"):
        description = "Pull request must target the repository default branch."
    elif not SHA_RE.fullmatch(pr.get("base", {}).get("sha", "")):
        description = "GitHub did not return a valid current base SHA."
    else:
        try:
            protected_paths = reject_policy_changes(owner, repo, number, read_token)
            enforce_policy_change_command(command, protected_paths)
            if unresolved_threads(owner, repo, number, read_token):
                description = "Unresolved review threads remain; resolve them and authorize again."
            else:
                reviewed_code_sha, evidence_record = verify_evidence(owner, repo, number, pr, read_token)
                if command == "authorize-policy-change":
                    validate_policy_change_record(evidence_record, protected_paths, pr["base"]["sha"])
                latest = api_request("GET", f"/repos/{owner}/{repo}/pulls/{number}", read_token)
                if (
                    latest.get("head", {}).get("sha") != current_sha
                    or latest.get("base", {}).get("sha") != pr.get("base", {}).get("sha")
                    or latest.get("state") != "open"
                    or latest.get("draft")
                    or latest.get("base", {}).get("ref") != repository.get("default_branch")
                ):
                    description = "PR head/base/state changed during validation; re-run authorization on the current exact head."
                elif unresolved_threads(owner, repo, number, read_token):
                    description = "Review threads changed during validation; resolve and authorize again."
                else:
                    state = "success"
                    description = (
                        "Policy evidence validated; owner authorized this exact PR head."
                        if command == "authorize-policy-change"
                        else "Evidence validated; maintainer authorized this exact PR head."
                    )
        except AuthorizationError as exc:
            description = str(exc)

    publish_status(owner, repo, current_sha, status_token, state, description, target_url)
    print(f"Set '{CONTEXT}' to {state} for {current_sha}.")
    return 0 if state == "success" else 1


if __name__ == "__main__":
    try:
        if "--preflight" in sys.argv[1:]:
            raise SystemExit(preflight())
        raise SystemExit(main())
    except (AuthorizationError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"Authorization gate failed closed: {exc}", file=sys.stderr)
        raise SystemExit(1)
