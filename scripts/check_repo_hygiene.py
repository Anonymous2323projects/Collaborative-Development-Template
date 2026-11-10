#!/usr/bin/env python3
"""Check repository paths, local Markdown links/anchors, and workflow safety conventions.

Uses only the Python standard library. This is a focused static hygiene check,
not a Markdown renderer, YAML validator, secret scanner, or complete security audit.
"""
from __future__ import annotations
import html
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\((<[^>]+>|[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
HTML_ID_RE = re.compile(r"""\b(?:id|name)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
ALLOWED_ENV_FILES = {".env.example"}
WORKFLOW_DIR = Path(".github/workflows")

def tracked_files() -> list[Path]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, stdout=subprocess.PIPE)
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
    return name in {"id_rsa", "id_ed25519", "id_ecdsa"}

def strip_html_comments(text: str) -> str:
    """Remove HTML comments because GitHub does not render their contents."""
    return re.sub(
        r"<!--[\s\S]*?(?:-->|$)",
        lambda match: "".join("\n" if char == "\n" else "" for char in match.group(0)),
        text,
    )


def strip_fenced_code(content: str) -> str:
    output = []
    fence_char = None
    fence_length = 0
    for line in content.splitlines():
        match = re.match(r"^\s{0,3}([\x60]{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char, fence_length = marker[0], len(marker)
                output.append("")
                continue
            if marker[0] == fence_char and len(marker) >= fence_length:
                fence_char, fence_length = None, 0
                output.append("")
                continue
        output.append(line if fence_char is None else "")
    return strip_html_comments("\n".join(output))

def github_slug(heading: str) -> str:
    value = html.unescape(heading).strip().lower()
    value = re.sub(r"!?(\[([^\]]*)\])\([^)]*\)", r"\2", value)
    value = re.sub(r"\x60([^\x60]*)\x60", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[*_~]", "", value)
    chars = []
    for char in value:
        category = unicodedata.category(char)
        if char.isspace():
            chars.append("-")
        elif char == "-" or category[0] in {"L", "N"}:
            chars.append(char)
    return re.sub(r"-+", "-", "".join(chars)).strip("-")

def markdown_anchors(content: str) -> set[str]:
    body = strip_fenced_code(content)
    anchors = set(HTML_ID_RE.findall(body))
    counts = {}
    for match in HEADING_RE.finditer(body):
        slug = github_slug(match.group(1))
        if not slug:
            continue
        count = counts.get(slug, 0)
        anchors.add(slug if count == 0 else f"{slug}-{count}")
        counts[slug] = count + 1
    return anchors

def markdown_link_errors(path: Path, content: str, file_cache: dict[Path, str]) -> list[str]:
    errors = []
    body = strip_fenced_code(content)
    for match in LINK_RE.finditer(body):
        target = match.group(1).strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        local_path = unquote(parsed.path)
        fragment = unquote(parsed.fragment)
        if not local_path:
            target_path = path
        else:
            resolved = (ROOT / path.parent / local_path).resolve()
            try:
                target_path = Path(resolved.relative_to(ROOT.resolve()))
            except ValueError:
                errors.append(f"{path}: link escapes repository")
                continue
        absolute = ROOT / target_path
        # Never echo raw link targets: query strings and fragments may contain
        # credentials or other sensitive values supplied by repository content.
        if not absolute.exists():
            errors.append(f"{path}: missing local link target")
            continue
        if fragment and absolute.is_file() and absolute.suffix.lower() == ".md":
            if target_path not in file_cache:
                try:
                    file_cache[target_path] = absolute.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    errors.append(f"{path}: cannot read Markdown link target")
                    continue
            if fragment not in markdown_anchors(file_cache[target_path]):
                errors.append(f"{path}: missing Markdown heading anchor")
    return errors

def workflow_events(content: str) -> list[str]:
    lines = content.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == "on:"), None)
    if start is None:
        return []
    events = []
    for line in lines[start + 1:]:
        if line and not line[0].isspace() and not line.lstrip().startswith("#"):
            break
        match = re.match(r"^[ \t]{2}([A-Za-z0-9_-]+):", line)
        if match:
            events.append(match.group(1))
    return events

def workflow_environment_errors(path: Path, content: str) -> list[str]:
    """Keep the App-key environment exclusive to the trusted authorization workflow."""
    errors = []
    lines = content.splitlines()
    blocks = []
    for index, line in enumerate(lines):
        match = re.match(r"^([ \t]*)environment:\s*(.*?)\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        block_lines = [match.group(2)] if match.group(2) else []
        cursor = index + 1
        while cursor < len(lines):
            candidate = lines[cursor]
            if not candidate.strip():
                cursor += 1
                continue
            candidate_indent = len(candidate) - len(candidate.lstrip(" \t"))
            if candidate_indent <= indent:
                break
            block_lines.append(candidate.strip())
            cursor += 1
        blocks.append("\n".join(block_lines))

    trusted_path = path.as_posix() == ".github/workflows/merge-authorization.yml"
    if trusted_path:
        if len(blocks) != 1 or not re.search(r"(?m)^name:\s*merge-authorizer\s*$", blocks[0]):
            errors.append(f"{path}: the trusted authorization workflow must use exactly one literal merge-authorizer environment")
        if blocks and "$" + "{{" in blocks[0]:
            errors.append(f"{path}: the trusted App-key environment name must not be dynamically constructed")
    else:
        if "merge-authorizer" in content:
            errors.append(f"{path}: only the trusted authorization workflow may reference the merge-authorizer environment")
        if any("$" + "{{" in block for block in blocks):
            errors.append(f"{path}: dynamic environment names are not allowed in untrusted workflows")
    return errors


def workflow_job_blocks(content: str) -> dict[str, str]:
    """Return top-level job blocks without parsing or executing YAML."""
    lines = content.splitlines()
    in_jobs = False
    current_name = None
    current = []
    jobs = {}
    for line in lines:
        if not in_jobs:
            if line.strip() == "jobs:":
                in_jobs = True
            continue
        if line and not line[0].isspace() and not line.lstrip().startswith("#"):
            break
        match = re.match(r"^  ([A-Za-z0-9_-]+):[ \t]*$", line)
        if match:
            if current_name is not None:
                jobs[current_name] = "\n".join(current)
            current_name = match.group(1)
            current = [line]
            continue
        if current_name is not None:
            current.append(line)
    if current_name is not None:
        jobs[current_name] = "\n".join(current)
    return jobs


def workflow_step_blocks(content: str) -> list[str]:
    """Return top-level job step blocks without parsing or executing YAML."""
    lines = content.splitlines()
    in_steps = False
    step_indent = None
    current = []
    blocks = []
    for line in lines:
        if not in_steps:
            if line.strip() == "steps:":
                in_steps = True
            continue
        if not line.strip():
            if current:
                current.append(line)
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        match = re.match(r"^([ \t]*)-[ \t]+", line)
        if match and (step_indent is None or len(match.group(1)) == step_indent):
            if current:
                blocks.append("\n".join(current))
            current = [line]
            step_indent = len(match.group(1))
            continue
        if current and indent <= step_indent:
            blocks.append("\n".join(current))
            current = []
            step_indent = None
            in_steps = False
            continue
        if current:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def trusted_authorizer_workflow_errors(path: Path, content: str) -> list[str]:
    """Enforce the separate status App and read-only GITHUB_TOKEN design."""
    trusted_path = path.as_posix() == ".github/workflows/merge-authorization.yml"
    errors = []
    if not trusted_path:
        if "MERGE_AUTH_APP" in content:
            errors.append(f"{path}: only the trusted authorization workflow may reference the merge App credentials")
        return errors
    if workflow_events(content) != ["issue_comment"]:
        errors.append(f"{path}: trusted authorization workflow must trigger only on issue_comment")
    permissions = re.search(r"(?m)^permissions:[ \t]*\n((?:[ \t]+[^\n]*\n)*)", content)
    if not permissions:
        errors.append(f"{path}: trusted authorization workflow requires explicit read-only GITHUB_TOKEN permissions")
    else:
        block = permissions.group(1)
        if not re.search(r"(?m)^[ \t]+contents:\s*read\s*$", block):
            errors.append(f"{path}: GITHUB_TOKEN must have contents: read")
        if not re.search(r"(?m)^[ \t]+pull-requests:\s*read\s*$", block):
            errors.append(f"{path}: GITHUB_TOKEN must have pull-requests: read")
        if re.search(r"(?m)^[ \t]+[A-Za-z_-]+:[ \t]*['\"]?(?:write|write-all)['\"]?[ \t]*(?:#.*)?$", block):
            errors.append(f"{path}: GITHUB_TOKEN must not have write permissions")
    required = (
        "github.event.repository.default_branch",
        "persist-credentials: false",
        "MERGE_AUTH_APP_PRIVATE_KEY",
        "MERGE_AUTH_APP_CLIENT_ID",
        "client-id: " + "$" + "{{ vars.MERGE_AUTH_APP_CLIENT_ID }}",
        "private-key: " + "$" + "{{ secrets.MERGE_AUTH_APP_PRIVATE_KEY }}",
        "owner: " + "$" + "{{ github.repository_owner }}",
        "repositories: " + "$" + "{{ github.event.repository.name }}",
        "permission-statuses: write",
        "skip-token-revoke: false",
    )
    for item in required:
        if item not in content:
            errors.append(f"{path}: trusted authorization workflow is missing required control: {item}")
    permission_inputs = [line.strip() for line in re.findall(r"(?m)^[ \t]*['\"]?permission-[A-Za-z0-9_-]+['\"]?:.*$", content)]
    if permission_inputs != ["permission-statuses: write"]:
        errors.append(f"{path}: installation token must request only permission-statuses: write")

    jobs = workflow_job_blocks(content)
    preflight_job = jobs.get("preflight", "")
    authorize_job = jobs.get("authorize", "")
    if not preflight_job or not authorize_job:
        errors.append(f"{path}: require separate preflight and environment-protected authorization jobs")
        return errors
    if re.search(r"(?m)^    environment:", preflight_job):
        errors.append(f"{path}: untrusted-comment preflight job must not request a protected environment")
    if "MERGE_AUTHORIZER_LOGINS: " + "$" + "{{ vars.MERGE_AUTHORIZER_LOGINS }}" not in preflight_job:
        errors.append(f"{path}: preflight must read the non-secret maintainer allowlist from a repository-level variable")
    if "secrets." in preflight_job or "MERGE_AUTH_APP" in preflight_job:
        errors.append(f"{path}: preflight must not access secrets or merge App credentials")
    if "outputs:" not in preflight_job or "authorized: " + "$" + "{{ steps.preflight.outputs.authorized }}" not in preflight_job:
        errors.append(f"{path}: preflight job must expose its authorized output")
    if "needs: preflight" not in authorize_job or "if: needs.preflight.outputs.authorized == 'true'" not in authorize_job:
        errors.append(f"{path}: environment-protected authorization job must run only after an authorized preflight output")

    preflight_steps = workflow_step_blocks(preflight_job)
    authorize_steps = workflow_step_blocks(authorize_job)
    preflight_checkouts = [block for block in preflight_steps if "uses: actions/checkout@" in block]
    preflight_blocks = [block for block in preflight_steps if "run: python3 scripts/authorize_merge.py --preflight" in block]
    auth_checkouts = [block for block in authorize_steps if "uses: actions/checkout@" in block]
    token_blocks = [block for block in authorize_steps if "actions/create-github-app-token@" in block]
    validation_blocks = [
        block for block in authorize_steps
        if "run: python3 scripts/authorize_merge.py" in block and "--preflight" not in block
    ]
    if len(preflight_checkouts) != 1 or len(preflight_blocks) != 1 or len(auth_checkouts) != 1 or len(token_blocks) != 1 or len(validation_blocks) != 1:
        errors.append(f"{path}: require one trusted checkout and preflight in the unprivileged job, then one trusted checkout, App-token creation and authorization in the protected job")
    else:
        if preflight_steps.index(preflight_checkouts[0]) >= preflight_steps.index(preflight_blocks[0]):
            errors.append(f"{path}: preflight job must check out trusted code before maintainer preflight")
        if authorize_steps.index(auth_checkouts[0]) >= authorize_steps.index(token_blocks[0]) or authorize_steps.index(token_blocks[0]) >= authorize_steps.index(validation_blocks[0]):
            errors.append(f"{path}: protected job must check out trusted code, create the App token, then validate authorization")
        for checkout in (preflight_checkouts[0], auth_checkouts[0]):
            if "ref: " + "$" + "{{ github.event.repository.default_branch }}" not in checkout:
                errors.append(f"{path}: both trusted jobs must check out the default branch")
            if "persist-credentials: false" not in checkout:
                errors.append(f"{path}: both trusted checkouts must set persist-credentials: false")
        for item in ("GITHUB_EVENT_PATH: " + "$" + "{{ github.event_path }}", "MERGE_AUTHORIZER_LOGINS: " + "$" + "{{ vars.MERGE_AUTHORIZER_LOGINS }}"):
            if item not in preflight_blocks[0]:
                errors.append(f"{path}: maintainer preflight is missing required input: {item}")
        if "id: status-token" not in token_blocks[0]:
            errors.append(f"{path}: App token creation must use the status-token ID")
        if not re.search(r"uses:\s*actions/create-github-app-token@[0-9a-fA-F]{40}(?:\s|$)", token_blocks[0]):
            errors.append(f"{path}: dedicated status App action must be pinned to a full commit SHA")
        for item in (
            "client-id: " + "$" + "{{ vars.MERGE_AUTH_APP_CLIENT_ID }}",
            "private-key: " + "$" + "{{ secrets.MERGE_AUTH_APP_PRIVATE_KEY }}",
            "owner: " + "$" + "{{ github.repository_owner }}",
            "repositories: " + "$" + "{{ github.event.repository.name }}",
            "permission-statuses: write",
            "skip-token-revoke: false",
        ):
            if item not in token_blocks[0]:
                errors.append(f"{path}: App-token step is missing required control: {item}")
        for item in (
            "GITHUB_TOKEN: " + "$" + "{{ secrets.GITHUB_TOKEN }}",
            "MERGE_AUTH_TOKEN: " + "$" + "{{ steps.status-token.outputs.token }}",
            "GITHUB_EVENT_PATH: " + "$" + "{{ github.event_path }}",
            "MERGE_AUTHORIZER_LOGINS: " + "$" + "{{ vars.MERGE_AUTHORIZER_LOGINS }}",
        ):
            if item not in validation_blocks[0]:
                errors.append(f"{path}: authorization step is missing required token input: {item}")
        for block in preflight_steps + authorize_steps:
            if block not in token_blocks and "MERGE_AUTH_APP" in block:
                errors.append(f"{path}: App credentials may be referenced only by the guarded status-token step")
    return errors


def secret_scan_workflow_errors(path: Path, content: str) -> list[str]:
    """Require a complete, exact-SHA Gitleaks range instead of a paginated PR API list."""
    if path.as_posix() != ".github/workflows/repository-hygiene.yml":
        return []
    errors = []
    job = workflow_job_blocks(content).get("secret-scan", "")
    if not job:
        return [f"{path}: required secret-scan job is missing"]
    required = (
        "fetch-depth: 0",
        "BASE_SHA: " + "$" + "{{ github.event.pull_request.base.sha }}",
        "HEAD_SHA: " + "$" + "{{ github.event.pull_request.head.sha }}",
        'git cat-file -e "${BASE_SHA}^{commit}"',
        'git cat-file -e "${HEAD_SHA}^{commit}"',
        'git rev-list --count "${BASE_SHA}..${HEAD_SHA}"',
        'gitleaks/gitleaks@sha256:',
        'git --log-opts="${BASE_SHA}..${HEAD_SHA} --diff-merges=first-parent" --redact --verbose .',
        '--volume "$GITHUB_WORKSPACE:/repo:ro"',
        "grep -Eo '[1-9][0-9]* commits scanned'",
    )
    for item in required:
        if item not in job:
            errors.append(f"{path}: secret scanning is missing required full-range control: {item}")
    if re.search(r"gitleaks/gitleaks-action@", job):
        errors.append(f"{path}: the paginated Gitleaks Action must not be used for pull-request scanning")
    images = re.findall(r"ghcr\.io/gitleaks/gitleaks(?:@[^\s\\]+|:[^\s\\]+)", job)
    if not images or any(re.fullmatch(r"ghcr\.io/gitleaks/gitleaks@sha256:[0-9a-f]{64}", image) is None for image in images):
        errors.append(f"{path}: every Gitleaks invocation must use a full SHA-256 image digest")
    range_guard = re.search(
        r'if \[\[ "\$commit_count" -lt 1 \]\]; then([\s\S]*?)(?:^\s*fi\s*$|;\s*fi\b)',
        job,
        re.MULTILINE,
    )
    if not range_guard or not re.search(r"\bexit 1\b", range_guard.group(1)):
        errors.append(f"{path}: empty pull-request scan ranges must fail closed")
    scanned_guard = re.search(
        r'if \[\[ -z "\$scanned" \]\]; then([\s\S]*?)(?:^\s*fi\s*$|;\s*fi\b)',
        job,
        re.MULTILINE,
    )
    if not scanned_guard or not re.search(r"\bexit 1\b", scanned_guard.group(1)):
        errors.append(f"{path}: a zero-commit scanner result must fail closed")
    if "detailed scanner output is suppressed" not in job or ' > "$scan_log" 2>&1' not in job:
        errors.append(f"{path}: raw Gitleaks output must be captured and suppressed")
    if "--first-parent" in job or "--no-merges" in job:
        errors.append(f"{path}: secret scanning must include commits reachable through all parent paths")
    return errors


def workflow_policy_errors(path: Path, content: str) -> list[str]:
    errors = workflow_environment_errors(path, content)
    errors.extend(trusted_authorizer_workflow_errors(path, content))
    errors.extend(secret_scan_workflow_errors(path, content))
    if not re.search(r"^permissions\s*:", content, re.MULTILINE):
        errors.append(f"{path}: explicit top-level GITHUB_TOKEN permissions are required")
    if re.search(r"^\s*(?:-\s*)?uses:\s*[^\s#]+@(?![0-9a-fA-F]{40}(?:\s|$))", content, re.MULTILINE):
        errors.append(f"{path}: external actions must be pinned to a full 40-character commit SHA")
    if re.search(r"^\s*permissions:\s*write-all\s*$", content, re.MULTILINE):
        errors.append(f"{path}: permissions: write-all is not allowed")
    if re.search(r"^\s*pull_request_target\s*:", content, re.MULTILINE):
        errors.append(f"{path}: pull_request_target requires a separate security design review and is disallowed by default")
    if re.search(r"(?m)^[ \t]*['\"]?statuses['\"]?:[ \t]*['\"]?write(?:-all)?['\"]?[ \t]*(?:#.*)?$", content):
        errors.append(f"{path}: GITHUB_TOKEN statuses: write is prohibited; publish through the dedicated status App token")
    return errors


REQUIRED_ASSURANCE_SECTIONS = (
    "1. Scope and risk-based depth",
    "2. Research standard",
    "3. Hazard and system analysis",
    "4. Five-perspective assessment",
    "5. Systemic recurrence rule",
    "6. Documentation-to-implementation assurance",
    "7. Technical enforcement architecture",
)
ASSURANCE_REFERENCES = {
    Path("AGENTS.md"): "MERGE_AND_CHANGE_ASSURANCE.md",
    Path("docs/DEVELOPMENT_WORKFLOW.md"): "MERGE_AND_CHANGE_ASSURANCE.md",
    Path("PROJECT_RISK_AND_RELEASE_READINESS.md"): "MERGE_AND_CHANGE_ASSURANCE.md",
    Path("docs/EXACT_HEAD_AUTHORIZATION_SETUP.md"): "../MERGE_AND_CHANGE_ASSURANCE.md",
}

def assurance_document_errors(root: Path = ROOT) -> list[str]:
    """Keep the canonical assurance standard and its governing references present."""
    errors = []
    standard = root / "MERGE_AND_CHANGE_ASSURANCE.md"
    if not standard.is_file():
        errors.append("MERGE_AND_CHANGE_ASSURANCE.md: required canonical assurance standard is missing")
    else:
        try:
            content = strip_fenced_code(standard.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"MERGE_AND_CHANGE_ASSURANCE.md: cannot read canonical standard: {exc}")
        else:
            for section in REQUIRED_ASSURANCE_SECTIONS:
                pattern = rf"^## {re.escape(section)}\s*$"
                if not re.search(pattern, content, re.MULTILINE):
                    errors.append(f"MERGE_AND_CHANGE_ASSURANCE.md: required core section is missing: {section}")
            if "recoverable snapshot of the exact pre-merge head" not in content.lower():
                errors.append("MERGE_AND_CHANGE_ASSURANCE.md: require a verified recoverable snapshot of the exact pre-merge head for high-impact or hard-to-reverse merges")
            setup_link = r"\]\(docs/EXACT_HEAD_AUTHORIZATION_SETUP\.md(?:#[^)]*)?\)"
            if not re.search(setup_link, content):
                errors.append("MERGE_AND_CHANGE_ASSURANCE.md: must link to docs/EXACT_HEAD_AUTHORIZATION_SETUP.md")
    for path, reference in ASSURANCE_REFERENCES.items():
        target = root / path
        if not target.is_file():
            errors.append(f"{path}: required governing document is missing")
            continue
        try:
            content = strip_fenced_code(target.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: cannot read governing document: {exc}")
            continue
        link_pattern = rf"\]\([^)]*{re.escape(reference)}(?:#[^)]*)?\)"
        if not re.search(link_pattern, content):
            errors.append(f"{path}: must contain a Markdown link to the canonical {reference}")
    return errors

def safe_error_categories(errors: list[str]) -> dict[str, int]:
    """Return fixed, non-sensitive issue categories without echoing repository-controlled text."""
    counts = {
        "documentation links and anchors": 0,
        "workflow and authorization policy": 0,
        "sensitive paths": 0,
        "assurance documentation": 0,
        "file access and encoding": 0,
        "other": 0,
    }
    for error in errors:
        lowered = error.lower()
        if "link" in lowered or "anchor" in lowered:
            category = "documentation links and anchors"
        elif any(term in lowered for term in ("workflow", "gitleaks", "secret scanning", "authorization", "protected policy")):
            category = "workflow and authorization policy"
        elif "sensitive" in lowered or "credential" in lowered:
            category = "sensitive paths"
        elif "assurance" in lowered:
            category = "assurance documentation"
        elif "cannot read" in lowered or "cannot decode" in lowered:
            category = "file access and encoding"
        else:
            category = "other"
        counts[category] += 1
    return {name: count for name, count in counts.items() if count}


def main() -> int:
    files = tracked_files()
    errors = assurance_document_errors(ROOT)
    file_cache = {}
    for path in files:
        if sensitive_path(path):
            errors.append(f"{path}: potentially sensitive filename or directory")
        if path.suffix.lower() == ".md":
            full_path = ROOT / path
            try:
                content = full_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{path}: cannot read as UTF-8: {exc}")
                continue
            file_cache[path] = content
            errors.extend(markdown_link_errors(path, content, file_cache))
        if path.parts[:2] == WORKFLOW_DIR.parts and path.suffix.lower() in {".yml", ".yaml"}:
            try:
                content = (ROOT / path).read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{path}: cannot read workflow: {exc}")
                continue
            errors.extend(workflow_policy_errors(path, content))
    if errors:
        print("Repository hygiene checks failed.")
        print(
            f"{len(errors)} issue(s) detected; detailed diagnostics are suppressed "
            "to prevent untrusted repository content from entering CI logs."
        )
        categories = safe_error_categories(errors)
        if categories:
            summary = ", ".join(f"{name}: {count}" for name, count in categories.items())
            print(f"Safe issue categories: {summary}.")
        return 1
    workflow_count = sum(1 for path in files if path.parts[:2] == WORKFLOW_DIR.parts and path.suffix.lower() in {".yml", ".yaml"})
    print(f"Repository hygiene checks passed for {len(files)} tracked files.")
    print("Checked sensitive paths, local Markdown links and heading anchors,")
    print(f"and baseline workflow safety conventions in {workflow_count} workflow file(s).")
    print("This does not parse YAML, render Markdown, scan file contents for secrets, verify action provenance,")
    print("check remote URLs, or constitute a complete security, privacy, or legal audit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
