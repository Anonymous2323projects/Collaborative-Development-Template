#!/usr/bin/env python3
"""Rehearse a pull-request patch forward and backward without changing the source checkout.

Only proves that the Git trees for two commits can be round-tripped via an isolated
local clone. It does not back up the repository, execute tests, authorize merges,
or account for external effects. Requires Git and a complete local object history.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}\Z")


class RecoveryError(Exception):
    """A recovery precondition or tree reconstruction failed."""


def git(root: Path, *args: str, stdout=None) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), "-c", "core.autocrlf=false", *args],
        stdout=subprocess.PIPE if stdout is None else stdout,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise RecoveryError(f"git {args[0]} failed (exit {completed.returncode}); see local Git configuration and object availability")
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
             "ls-tree", "-r", "-z", revision],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if completed.returncode:
            raise RecoveryError("git ls-tree failed; object availability is uncertain")
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
        # Clone from a local path only: never fetch a remote or modify the source.
        subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--no-hardlinks", str(source), str(scratch)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git(scratch, "checkout", "--detach", base)
        if git(scratch, "write-tree") != base_tree:
            raise RecoveryError("Initial clean base tree mismatch")
        patch = tmp / "change.patch"
        with patch.open("wb") as out:
            # A locally configured diff.external helper must never run during recovery.
            git(source, "diff", "--no-ext-diff", "--binary", "--full-index", base, head, "--", stdout=out)
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
    except (RecoveryError, OSError, subprocess.SubprocessError) as exc:
        print(f"Recovery rehearsal FAILED: {type(exc).__name__} (details suppressed)", file=sys.stderr)
        return 1
    print(f"Recovery rehearsal PASS: forward tree {after}; restored base tree {before}")
    print("No branch/ref was changed. Git-only test, not an offsite backup or merge authorization.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
