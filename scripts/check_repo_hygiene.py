#!/usr/bin/env python3
"""Check tracked repository paths and local Markdown links without third-party packages."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\((<[^>]+>|[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
ALLOWED_ENV_FILES = {".env.example"}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def sensitive_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    if name in ALLOWED_ENV_FILES:
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    if parts.intersection({"secrets", "credentials"}):
        return True
    if name.endswith((".pem", ".key", ".p12", ".pfx")):
        return True
    if name in {"id_rsa", "id_ed25519", "id_ecdsa"}:
        return True
    return False


def markdown_link_errors(path: Path, content: str) -> list[str]:
    errors: list[str] = []
    for match in LINK_RE.finditer(content):
        target = match.group(1).strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith("#"):
            continue
        local_path = unquote(parsed.path)
        if not local_path:
            continue
        resolved = (ROOT / path.parent / local_path).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path}: missing local link target: {target}")
    return errors


def main() -> int:
    files = tracked_files()
    errors: list[str] = []
    for path in files:
        if sensitive_path(path):
            errors.append(f"{path}: potentially sensitive filename or directory")
        if path.suffix.lower() == ".md":
            full_path = ROOT / path
            errors.extend(markdown_link_errors(path, full_path.read_text(encoding="utf-8")))

    if errors:
        print("Repository hygiene checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Repository hygiene checks passed for {len(files)} tracked files.")
    print("Checked sensitive path patterns and local Markdown link targets.")
    print("This does not scan file contents for secrets or verify remote URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
