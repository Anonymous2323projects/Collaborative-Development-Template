#!/usr/bin/env python3
"""Create an exact-head merge-authorization commit status from a trusted issue comment.

This workflow runs from the default branch on issue_comment. It never checks out
or executes pull-request code. Configure MERGE_AUTHORIZER_LOGINS for organization
repositories; user-owned repositories default to the repository owner.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
CONTEXT = "Explicit maintainer merge authorization"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
COMMAND_RE = re.compile(r"^/(authorize-merge|revoke-merge)\s+([0-9a-f]{40})\s*$")

class AuthorizationError(RuntimeError):
    pass

def api_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
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
    raise AuthorizationError("Set the repository variable MERGE_AUTHORIZER_LOGINS to an explicit comma-separated maintainer allowlist.")

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
    try:
        threads = result["data"]["repository"]["pullRequest"]["reviewThreads"]
    except (KeyError, TypeError) as exc:
        raise AuthorizationError("Could not verify pull-request review threads; authorization fails closed.") from exc
    if threads["pageInfo"]["hasNextPage"]:
        raise AuthorizationError("More than 100 review threads exist; resolve and inspect them before authorization.")
    return any(not node["isResolved"] for node in threads["nodes"])

def main() -> int:
    event_path = os.environ["GITHUB_EVENT_PATH"]
    token = os.environ["GITHUB_TOKEN"]
    event = json.loads(open(event_path, encoding="utf-8").read())
    comment = event.get("comment", {})
    match = COMMAND_RE.fullmatch(comment.get("body", "").strip())
    if not match:
        print("No recognized exact-head authorization command; no status changed.")
        return 0

    repository = event["repository"]
    owner = repository["owner"]["login"]
    repo = repository["name"]
    number = int(event["issue"]["number"])
    actor = comment.get("user", {}).get("login", "").lower()
    command, requested_sha = match.groups()
    allowed = authorized_logins(repository, os.getenv("MERGE_AUTHORIZER_LOGINS", ""))
    if actor not in allowed:
        raise AuthorizationError("Comment author is not an authorized maintainer; no commit status was changed.")

    pr = api_request("GET", f"/repos/{owner}/{repo}/pulls/{number}", token)
    if pr.get("state") != "open" or pr.get("draft"):
        raise AuthorizationError("Pull request must be open and ready for review.")
    if pr.get("base", {}).get("ref") != repository.get("default_branch"):
        raise AuthorizationError("Pull request must target the repository default branch.")
    current_sha = pr.get("head", {}).get("sha", "")
    if not SHA_RE.fullmatch(current_sha):
        raise AuthorizationError("GitHub did not return a valid current head SHA.")

    state = "success"
    description = "Authorized by repository maintainer for this exact PR head."
    if command == "authorize-merge":
        if requested_sha != current_sha:
            state = "failure"
            description = "Authorization SHA did not match the current PR head; authorize the new exact SHA."
        elif unresolved_threads(owner, repo, number, token):
            state = "failure"
            description = "Unresolved review threads remain; resolve them and authorize again."
    else:
        if requested_sha != current_sha:
            state = "failure"
            description = "Revocation SHA did not match the current PR head."
        else:
            state = "failure"
            description = "Maintainer revoked merge authorization for this exact PR head."

    api_request("POST", f"/repos/{owner}/{repo}/statuses/{current_sha}", token, {
        "state": state,
        "context": CONTEXT,
        "description": description[:140],
        "target_url": comment.get("html_url"),
    })
    print(f"Set '{CONTEXT}' to {state} for {current_sha}.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AuthorizationError, KeyError, ValueError, OSError) as exc:
        print(f"Authorization gate failed closed: {exc}", file=sys.stderr)
        raise SystemExit(1)
