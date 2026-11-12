#!/usr/bin/env python3
"""Rehearse a pull-request patch forward and backward without changing the source checkout.

Only proves that the Git trees for two commits can be round-tripped via a
temporary local clone. It does not back up the repository, execute tests,
authorize merges, or account for external effects.

Run only with a *trusted* local repository, Git binary and OS environment:
local repository config and working-tree attributes are NOT a security
sandbox. All needed base/head commit, tree and blob objects must already be
available locally. Git subprocesses prohibit promisor lazy fetching; missing
objects fail the rehearsal rather than fetching from a remote. This checks
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
    )
    return env


def git(root: Path, *args: str, stdout=None) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), "-c", "core.autocrlf=false",
         "-c", f"core.attributesFile={os.devnull}", *args],
        stdout=subprocess.PIPE if stdout is None else stdout,
        stderr=subprocess.PIPE,
        check=False,
        env=isolated_git_env(),
    )
    if completed.returncode:
        raise RecoveryError("Git command failed; verify trusted config and local objects", phase=args[0])
    return completed.stdout.decode("utf-8").strip() if stdout is None else ""


def verify(base: str, head: str, repository: Path) -> tuple[str, str]:
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise RecoveryError("Expected two complete lowercase 40-character commit IDs")
    source = repository.resolve()
    git(source, "rev-parse", "--is-inside-work-tree")
    base_tree = git(source, "rev-parse", f"{base}^{{tree}}")
    head_tree = git(source, "rev-parse", f"{head}^{{tree}}")
    # Git paths are arbitrary bytes on POSIX. Parse only the ASCII mode from raw,
    # NUL-delimited ls-tree records; never decode filename bytes as UTF-8.
    def has_gitlinks(revision: str) -> bool:
        completed = subprocess.run(
            ["git", "-C", str(source), "-c", "core.autocrlf=false",
             "-c", f"core.attributesFile={os.devnull}",
             "ls-tree", "-r", "-z", revision],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            env=isolated_git_env(),
        )
        if completed.returncode:
            raise RecoveryError("git ls-tree failed; local objects are uncertain", phase="ls-tree")
        for record in completed.stdout.split(b"\0"):
            if not record:
                continue
            metadata, separator, _filename = record.partition(b"\t")
            if not separator:
                raise RecoveryError("Unexpected git ls-tree record format")
            if metadata.split(b" ", 1)[0] == b"160000":
                return True
        return False

    if has_gitlinks(base) or has_gitlinks(head):
        raise RecoveryError("Git submodules require a separate recovery assessment")
    with tempfile.TemporaryDirectory(prefix="cdt-recovery-") as location:
        tmp = Path(location)
        scratch = tmp / "checkout"
        empty_template = tmp / "empty-template"
        empty_template.mkdir()
        # A local-path clone uses local object copying; no hook template or
        # remote-object lazy fetch is allowed. Do not use an untrusted .git dir.
        clone = subprocess.run(
            ["git", "-c", f"core.attributesFile={os.devnull}",
             "clone", "--quiet", "--no-checkout", "--no-hardlinks",
             "--template", str(empty_template), str(source), str(scratch)],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=isolated_git_env(),
        )
        if clone.returncode:
            raise RecoveryError("Local clone failed", phase="clone")
        git(scratch, "checkout", "--detach", base)
        if git(scratch, "write-tree") != base_tree:
            raise RecoveryError("Initial clean base tree mismatch")
        patch = tmp / "change.patch"
        with patch.open("wb") as out:
            # A recovery patch must not use executable diff or textconv drivers.
            git(source, "diff", "--no-ext-diff", "--no-textconv", "--binary", "--full-index", base, head, "--", stdout=out)
        git(scratch, "apply", "--check", str(patch))
        git(scratch, "apply", str(patch))
        git(scratch, "add", "--all", "--force")
        if git(scratch, "write-tree") != head_tree:
            raise RecoveryError("Forward patch does not reproduce the exact head tree")
        git(scratch, "apply", "--reverse", "--check", str(patch))
        git(scratch, "apply", "--reverse", str(patch))
        git(scratch, "add", "--all", "--force")
        if git(scratch, "write-tree") != base_tree:
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
