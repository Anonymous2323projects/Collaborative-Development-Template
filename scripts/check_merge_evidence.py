#!/usr/bin/env python3
"""Fail-closed structural validator for PR-specific assurance records.

This validates presence, identity, and basic completeness only. It cannot
establish that the review is correct, sources are authoritative, evidence is
truthful, or risks have been understood.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.IGNORECASE)
RISK_LEVELS = {"LOW", "MODERATE", "HIGH", "CRITICAL"}
ASSESSMENTS = {"PASS", "PASS WITH RESIDUAL RISK", "BLOCKED", "NOT APPLICABLE"}
LENSES = (
    "Safety and security",
    "Legal solidity and privacy",
    "Usability",
    "Trust and human impact",
    "Freedom and ownership",
)
REQUIRED_SECTIONS = (
    "## Change identity",
    "## Research and evidence",
    "## Five-perspective assessment",
    "## Documentation-to-implementation traceability",
    "## Validation evidence",
    "## Systemic recurrence review",
    "## Efficiency audit",
    "## Residual risk and approval",
)

class GateError(ValueError):
    pass

def section(text: str, heading: str) -> str:
    level = len(heading) - len(heading.lstrip("#"))
    match = re.search(
        rf"^{re.escape(heading)}\s*$([\s\S]*?)(?=^#{{1,{level}}}\s|\Z)",
        text,
        re.MULTILINE,
    )
    return match.group(1).strip() if match else ""

def field(text: str, name: str) -> str:
    matches = re.findall(rf"^-\s*{re.escape(name)}:\s*(.*?)\s*$", text, re.MULTILINE)
    return matches[0].strip() if len(matches) == 1 else ""

def non_placeholder(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip().lower()
    return normalized not in {"", "todo", "tbd", "n/a", "none", "?", "—", "-", "[fill in]"} and not (
        normalized.startswith("[") and normalized.endswith("]")
    )

def source_hosts(value: str) -> set[str]:
    hosts: set[str] = set()
    for candidate in URL_RE.findall(value):
        try:
            host = urlsplit(candidate).hostname
        except ValueError:
            host = None
        if host:
            hosts.add(host.lower().rstrip("."))
    return hosts

def host_is_in(hosts: set[str], domain: str) -> bool:
    return any(host == domain or host.endswith("." + domain) for host in hosts)

def validate_record(text: str, pr_number: int, base_ref: str, base_sha: str, reviewed_code_sha: str) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED_SECTIONS:
        occurrences = re.findall(rf"^{re.escape(heading)}\s*$", text, re.MULTILINE)
        if len(occurrences) != 1:
            errors.append(f"Required section must appear exactly once: {heading}")

    identity = section(text, "## Change identity")
    expected = {
        "PR number": f"#{pr_number}",
        "Base branch": base_ref,
        "Base SHA (40 characters)": base_sha,
        "Reviewed code SHA (parent of this evidence-only commit)": reviewed_code_sha,
    }
    for name, value in expected.items():
        actual = field(identity, name)
        if actual != value:
            errors.append(f"{name} must exactly match the pull request ({value}).")

    risk = field(identity, "Risk")
    if risk not in RISK_LEVELS:
        errors.append("Risk must be LOW, MODERATE, HIGH, or CRITICAL.")

    for lens in LENSES:
        heading = f"### {lens}"
        perspective_section = section(text, "## Five-perspective assessment")
        lens_occurrences = re.findall(rf"^{re.escape(heading)}\s*$", perspective_section, re.MULTILINE)
        body = section(perspective_section, heading)
        if len(lens_occurrences) != 1 or not body:
            errors.append(f"Assessment heading must appear exactly once for: {lens}")
            continue
        assessment = field(body, "Assessment")
        if assessment not in ASSESSMENTS:
            errors.append(f"{lens}: invalid or missing assessment.")
            continue
        if assessment == "BLOCKED":
            errors.append(f"{lens}: BLOCKED assessment prevents merge.")
        evidence = field(body, "Evidence")
        if not non_placeholder(evidence):
            errors.append(f"{lens}: evidence is required.")
        residual = field(body, "Residual risk and mitigation")
        not_applicable = field(body, "If not applicable, why")
        if assessment == "NOT APPLICABLE" and not non_placeholder(not_applicable):
            errors.append(f"{lens}: explain why this perspective is not applicable.")
        if assessment == "PASS WITH RESIDUAL RISK" and not non_placeholder(residual):
            errors.append(f"{lens}: document residual risk and mitigation.")

    research = section(text, "## Research and evidence")
    sources = field(research, "Sources (prefer DOI/peer-reviewed research, standards, law, and official platform documentation)")
    research_rationale = field(research, "If external research was not needed, explain why the change is genuinely low risk")
    hosts = source_hosts(sources)
    has_source = bool(URL_RE.search(sources) or DOI_RE.search(sources))
    peer_reviewed = bool(DOI_RE.search(sources) or host_is_in(hosts, "springer.com") or host_is_in(hosts, "ieeexplore.ieee.org"))
    official_source = any(host_is_in(hosts, domain) for domain in (
        "nist.gov", "docs.github.com", "europa.eu", "eur-lex.europa.eu",
        "owasp.org", "slsa.dev", "iso.org",
    ))
    if risk in {"HIGH", "CRITICAL"}:
        if not has_source:
            errors.append("HIGH/CRITICAL changes require cited source URLs or DOIs.")
        if not peer_reviewed:
            errors.append("HIGH/CRITICAL changes require a peer-reviewed research source or a documented literature gap.")
        if not official_source:
            errors.append("HIGH/CRITICAL changes require an authoritative standard, law, or official technical source.")
    elif not has_source and not non_placeholder(research_rationale):
        errors.append("Provide source URLs/DOIs or explain why external research is not needed.")

    for label in (
        "Research question",
        "What each source supports",
        "Publication/version/date and applicability",
        "Methodological limits, conflicts, or evidence gaps",
        "Alternatives considered and why this option was selected",
    ):
        if not non_placeholder(field(research, label)):
            errors.append(f"Research section is incomplete: {label}.")

    docs = section(text, "## Documentation-to-implementation traceability")
    if "|" not in docs or "Requirement or policy" not in docs:
        errors.append("Include a documentation-to-implementation traceability table.")
    if not non_placeholder(field(docs, "Result")):
        errors.append("Record the result of the contradiction/paradox review.")

    validation = section(text, "## Validation evidence")
    if "|" not in validation or "Command/check" not in validation:
        errors.append("Include a validation evidence table.")
    if not non_placeholder(field(validation, "Complete diff reviewed")):
        errors.append("Confirm whether the complete diff was reviewed.")
    tested_sha = field(validation, "Exact commit SHA tested")
    if tested_sha != reviewed_code_sha:
        errors.append("The exact commit SHA tested must equal the reviewed code SHA.")

    systemic = section(text, "## Systemic recurrence review")
    for label in (
        "Was this change prompted by a defect, incident, near miss, or procedural weakness? YES / NO",
        "Related procedures, instructions, templates, workflows, permissions, and tests searched",
        "Similar weaknesses found",
        "Changes made to prevent recurrence",
    ):
        if not non_placeholder(field(systemic, label)):
            errors.append(f"Systemic recurrence section is incomplete: {label}.")

    efficiency = section(text, "## Efficiency audit")
    for label in (
        "Duplicate work or contradictory sources removed",
        "Existing evidence reused and why still valid",
        "Tests selected and why they cover the affected risk",
        "Runtime/maintenance/user burden",
        "Safety-critical work intentionally retained",
    ):
        if not non_placeholder(field(efficiency, label)):
            errors.append(f"Efficiency audit is incomplete: {label}.")

    approval = section(text, "## Residual risk and approval")
    if field(approval, "Merge authorization state") != "AWAITING EXPLICIT OWNER AUTHORIZATION":
        errors.append("Merge authorization must remain awaiting the separate exact-head owner gate.")
    blockers = field(approval, "Critical blockers")
    if not blockers or blockers.strip().startswith("[") or blockers.strip().upper() != "NONE":
        errors.append(f"Critical blockers remain or are not explicitly cleared: {blockers or 'not recorded'}.")
    return errors

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python scripts/check_merge_evidence.py <event.json>")
        return 2
    event_path = Path(argv[1])
    try:
        event = json.loads(event_path.read_text(encoding="utf-8"))
        pr = event["pull_request"]
        number = int(pr["number"] if "number" in pr else event["number"])
        base_ref = pr["base"]["ref"]
        base_sha = pr["base"]["sha"]
        event_head_sha = pr["head"]["sha"]
        if not SHA_RE.fullmatch(base_sha) or not SHA_RE.fullmatch(event_head_sha):
            raise GateError("GitHub event did not contain valid full commit SHAs.")
        import subprocess
        commit_line = subprocess.check_output(["git", "rev-list", "--parents", "-n", "1", "HEAD"], text=True).strip().split()
        if len(commit_line) != 2 or commit_line[0] != event_head_sha:
            raise GateError("The PR head must be a single-parent evidence-only commit checked out by exact SHA.")
        changed_paths = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"], text=True).splitlines()
        expected_path = f"reviews/PR-{number}.md"
        if changed_paths != [expected_path]:
            raise GateError(f"The final PR commit must change only {expected_path}; put all code changes before the evidence-only commit.")
        reviewed_code_sha = commit_line[1]
        path = ROOT / "reviews" / f"PR-{number}.md"
        if not path.is_file():
            raise GateError(f"Missing required PR assurance record: reviews/PR-{number}.md")
        text = path.read_text(encoding="utf-8")
        errors = validate_record(text, number, base_ref, base_sha, reviewed_code_sha)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Merge evidence gate failed closed: {exc}")
        return 1
    if errors:
        print("Merge evidence gate failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Merge evidence structure passed for PR #{number}; reviewed code SHA {reviewed_code_sha} is the parent of the evidence-only head commit.")
    print("This validates structure and identity only, not the truth or quality of the review.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
