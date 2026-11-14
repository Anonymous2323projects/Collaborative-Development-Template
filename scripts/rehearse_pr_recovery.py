#!/usr/bin/env python3
"""Rehearse a pull-request patch forward and backward without changing the source checkout.

Only proves that the Git trees for two commits can be round-tripped via a
temporary local clone using a separate index (no working-tree checkout). It
does not back up the repository, execute tests,
authorize merges, or account for external effects.

Run only with a *trusted* local repository, Git binary and OS environment:
local repository config and working-tree attributes are NOT a security
sandbox. Git 2.46.0+ with a working --no-lazy-fetch option is required and checked
before reading the source repository. All referenced base/head commit, tree and blob objects
must already be available locally; all leaf blobs are checked in a batch,
including those inside unchanged subtrees. Git subprocesses prohibit promisor lazy
fetching; missing objects fail the rehearsal rather than fetching from a remote. This checks
the specific pair of trees, not the completeness of unrelated history.
Source refs and unrelated local work must remain unchanged.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}\Z")


class RecoveryError(Exception):
    """A recovery precondition or tree reconstruction failed."""

    def __init__(self, message: str, *, phase: str = "verification"):
        super().__init__(message)
        self.phase = phase


def isolated_git_env() -> dict[str, str]:
    """Avoid inherited Git config and helpers in a read-only tree rehearsal."""
    env = {key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")}
    # Source-local repository config is still trusted; suppress inherited global,
    # system, attribute, replacement-ref and promisor auto-fetch overrides.
    env.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_ATTR_NOSYSTEM="1",
        GIT_NO_LAZY_FETCH="1",
        GIT_NO_REPLACE_OBJECTS="1",
        GIT_ALLOW_PROTOCOL="file",  # No HTTP(S), SSH, git:// or custom transports.
        GIT_TERMINAL_PROMPT="0",
        GIT_PROTOCOL_FROM_USER="0",
    )
    return env


MIN_GIT_VERSION = (2, 46, 0)


def require_offline_git() -> None:
    """Reject known-unsafe Git 2.45.0 even when its option probe succeeds.

    The --no-lazy-fetch flag exists in 2.45.0, but its promisor prefetch path
    can still fetch. The fix is present by 2.45.1; 2.46.0 is a conservative
    supported floor. The local-file-only transport allowlist adds a second
    defense against Git's non-file transports, not OS-level network shares or
    trusted local helper execution.
    """
    try:
        probe = subprocess.run(
            ["git", "--no-lazy-fetch", "--version"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            env=isolated_git_env(),
        )
    except OSError as exc:
        raise RecoveryError("Git is unavailable", phase="git-version") from exc
    if probe.returncode:
        raise RecoveryError("Git with --no-lazy-fetch support is required", phase="git-version")
    match = re.match(rb"^git version ([0-9]+)\.([0-9]+)\.([0-9]+)(?:\D|$)",
                     probe.stdout.strip())
    if match is None or tuple(int(x) for x in match.groups()) < MIN_GIT_VERSION:
        raise RecoveryError(
            "Git 2.46.0 or newer is required (2.45.0 may fetch promisor objects)",
            phase="git-version",
        )


def git(root: Path, *args: str, stdout=None, index: Path | None = None) -> str:
    env = isolated_git_env()
    if index is not None:
        # Only the synthetic index is mutable; the source worktree/index is not.
        env["GIT_INDEX_FILE"] = str(index)
    completed = subprocess.run(
        ["git", "-C", str(root), "-c", "core.autocrlf=false",
         "-c", f"core.attributesFile={os.devnull}", *args],
        stdout=subprocess.PIPE if stdout is None else stdout,
        stderr=subprocess.PIPE,
        check=False,
        env=env,
    )
    if completed.returncode:
        raise RecoveryError("Git command failed; verify trusted config and local objects",
                            phase=args[0])
    return completed.stdout.decode("utf-8").strip() if stdout is None else ""


def verify(base: str, head: str, repository: Path) -> tuple[str, str]:
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise RecoveryError("Expected two complete lowercase 40-character commit IDs")
    require_offline_git()  # Prove the guard works before touching repository data.
    source = repository.resolve()
    git(source, "rev-parse", "--is-inside-work-tree")
    # A tree or annotated tag ID must not masquerade as a reviewed PR commit.
    for label, commit_oid in (("base", base), ("head", head)):
        try:
            kind = git(source, "cat-file", "-t", commit_oid)
        except RecoveryError as exc:
            raise RecoveryError(f"{label} must be an available commit",
                                phase="commit-type") from exc
        if kind != "commit":
            raise RecoveryError(f"{label} must be a commit, not {kind}",
                                phase="commit-type")
    base_tree = git(source, "rev-parse", f"{base}^{{tree}}")
    head_tree = git(source, "rev-parse", f"{head}^{{tree}}")
    # Inventory every leaf of BOTH trees, not only the changed paths. Git's
    # index may reuse an unchanged cached subtree without opening its blobs.
    # Filenames are arbitrary bytes on POSIX, so only parse NUL-separated
    # ls-tree metadata, never decode filename bytes as UTF-8.
    def tree_blob_ids(revision: str) -> set[bytes]:
        completed = subprocess.run(
            ["git", "-C", str(source), "-c", "core.autocrlf=false",
             "-c", f"core.attributesFile={os.devnull}",
             "ls-tree", "-r", "-z", revision],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            env=isolated_git_env(),
        )
        if completed.returncode:
            raise RecoveryError("Tree inventory failed; local objects are uncertain",
                                phase="ls-tree")
        blobs: set[bytes] = set()
        for record in completed.stdout.split(b"\0"):
            if not record:
                continue
            metadata, separator, _filename = record.partition(b"\t")
            fields = metadata.split(b" ")
            if not separator or len(fields) != 3:
                raise RecoveryError("Unexpected tree inventory record", phase="ls-tree")
            mode, kind, oid = fields
            if mode == b"160000":
                raise RecoveryError("Git submodules require a separate recovery assessment",
                                    phase="gitlink")
            if kind != b"blob" or re.fullmatch(rb"[0-9a-f]{40}", oid) is None:
                raise RecoveryError("Unexpected Git object in tree inventory",
                                    phase="ls-tree")
            blobs.add(oid)
        return blobs

    required_blobs = sorted(tree_blob_ids(base) | tree_blob_ids(head))
    if required_blobs:
        checked = subprocess.run(
            ["git", "--no-lazy-fetch", "-C", str(source),
             "-c", "core.autocrlf=false",
             "-c", f"core.attributesFile={os.devnull}", "cat-file",
             "--batch-check=%(objectname) %(objecttype)", "--buffer"],
            input=b"\n".join(required_blobs) + b"\n",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            env=isolated_git_env(),
        )
        # cat-file --batch-check can exit ZERO while printing "<oid> missing".
        # Require one exact "oid blob" record for every requested object.
        if checked.returncode or checked.stdout.splitlines() != [
                oid + b" blob" for oid in required_blobs]:
            raise RecoveryError("Required local blob is missing or invalid",
                                phase="blob-availability")
    # An empty patch is a legitimate no-op for distinct commits with the same
    # tree. Do not bypass object availability or gitlink checks to accept it.
    if base_tree == head_tree:
        return base_tree, head_tree

    with tempfile.TemporaryDirectory(prefix="cdt-recovery-") as location:
        tmp = Path(location)
        scratch = tmp / "checkout"
        empty_template = tmp / "empty-template"
        empty_template.mkdir()
        # A local-path clone copies objects without checkout; Git transports
        # are limited to local-file only and lazy fetching remains disabled.
        # Only trusted source .git config is supported.
        clone = subprocess.run(
            ["git", "-c", f"core.attributesFile={os.devnull}",
             "clone", "--quiet", "--no-checkout", "--no-hardlinks",
             "--template", str(empty_template), str(source), str(scratch)],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=isolated_git_env(),
        )
        if clone.returncode:
            raise RecoveryError("Local clone failed", phase="clone")
        # read-tree / apply --cached / write-tree is independent of filesystem
        # executable bits, filters, line endings and checkout capabilities.
        # Keep this index outside the source and scratch repositories.
        index = tmp / "rehearsal-index"
        git(scratch, "read-tree", base_tree, index=index)
        if git(scratch, "write-tree", index=index) != base_tree:
            raise RecoveryError("Initial synthetic base index mismatch")
        patch = tmp / "change.patch"
        with patch.open("wb") as out:
            # Never run executable diff or textconv drivers during the rehearsal.
            git(source, "diff", "--no-ext-diff", "--no-textconv", "--binary",
                "--full-index", base, head, "--", stdout=out)
        git(scratch, "apply", "--cached", "--check", str(patch), index=index)
        git(scratch, "apply", "--cached", str(patch), index=index)
        if git(scratch, "write-tree", index=index) != head_tree:
            raise RecoveryError("Forward patch does not reproduce the exact head tree")
        git(scratch, "apply", "--cached", "--reverse", "--check", str(patch), index=index)
        git(scratch, "apply", "--cached", "--reverse", str(patch), index=index)
        if git(scratch, "write-tree", index=index) != base_tree:
            raise RecoveryError("Reverse patch does not reproduce the exact base tree")
    return base_tree, head_tree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Exact base commit SHA")
    parser.add_argument("--head", required=True, help="Exact PR head commit SHA")
    parser.add_argument("--repository", type=Path, default=Path.cwd(), help="Existing local Git repository")
    args = parser.parse_args()
    try:
        before, after = verify(args.base, args.head, args.repository)
    except RecoveryError as exc:
        # Only hardcoded operation names reach stdout/stderr, never Git stderr,
        # remote URLs, file paths, or local configuration values.
        print(f"Recovery rehearsal FAILED in {exc.phase} (details suppressed)", file=sys.stderr)
        return 1
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Recovery rehearsal FAILED: {type(exc).__name__} (details suppressed)", file=sys.stderr)
        return 1
    print(f"Recovery rehearsal PASS: forward tree {after}; restored base tree {before}")
    print("Trusted local Git/repository required; missing objects are not fetched.")
    print("No branch/ref was changed. Git-only test, not an offsite backup or merge authorization.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
