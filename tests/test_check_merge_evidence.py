"""Tests for the fail-closed PR assurance-record validator."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_merge_evidence.py"
SPEC = importlib.util.spec_from_file_location("merge_evidence", SCRIPT)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

BASE = "a" * 40
REVIEWED = "b" * 40

def valid_record():
    lenses = []
    for name in gate.LENSES:
        lenses.append(f"""### {name}
- Assessment: PASS
- Evidence: tests and source review recorded in this PR
- Hazards/threats and controls: reviewed
- Residual risk and mitigation: none identified
- If not applicable, why: not applicable
""")
    return f"""# Pull Request Assurance Record
## Change identity
- PR number: #12
- Base branch: main
- Base SHA (40 characters): {BASE}
- Reviewed code SHA (parent of this evidence-only commit): {REVIEWED}
- Risk: HIGH
- Goal and user outcome: improve a merge control
- Scope and non-goals: scoped
- Affected components, users, data, and trust boundaries: repository policy

## Research and evidence
- Research question: how to technically enforce the gate
- Sources (prefer DOI/peer-reviewed research, standards, law, and official platform documentation): https://link.springer.com/article/10.1000/example and https://csrc.nist.gov/pubs/sp/800/218/final https://docs.github.com/en/repositories/configuring-branches-and-merges
- What each source supports: assurance cases and merge rules
- Publication/version/date and applicability: checked for this repository
- Methodological limits, conflicts, or evidence gaps: noted
- Alternatives considered and why this option was selected: least privilege and exact-head status

## Five-perspective assessment
{''.join(lenses)}
## Documentation-to-implementation traceability
| Requirement or policy | Implementation/control | Test or evidence | User documentation | Residual risk |
|---|---|---|---|---|
| Gate | CI | tests | docs | low |
- Contradictions, stale statements, paradoxes, missing edge cases, or duplicate authority checked: yes
- Result: no unresolved contradictions

## Validation evidence
| Command/check | Exact version/environment | Result | Evidence or run URL |
|---|---|---|---|
| unittest | Python | PASS | run |
- Complete diff reviewed: yes
- Checks not run and why: none
- Exact commit SHA tested: {REVIEWED}

## Systemic recurrence review
- Was this change prompted by a defect, incident, near miss, or procedural weakness? YES / NO: YES
- Related procedures, instructions, templates, workflows, permissions, and tests searched: all affected
- Similar weaknesses found: one
- Changes made to prevent recurrence: CI gate

## Efficiency audit
- Duplicate work or contradictory sources removed: no duplicate authoritative source remained after the cross-file audit
- Existing evidence reused and why still valid: no prior evidence reused; every relevant setting and check was re-fetched
- Tests selected and why they cover the affected risk: relevant unit tests
- Runtime/maintenance/user burden: low
- Safety-critical work intentionally retained: exact SHA authorization

## Residual risk and approval
- Open findings and residual risks: none identified
- Critical blockers: NONE
- Required user/owner decision: explicit authorization of the exact PR head
- Merge authorization state: AWAITING EXPLICIT OWNER AUTHORIZATION
- Bootstrap change?: NO
- Gate that cannot yet apply: NOT APPLICABLE
- Existing live controls and compensating manual controls: NOT APPLICABLE
- Manual owner approval evidence/state: NOT APPLICABLE
- Post-merge configuration and acceptance-test owner: NOT APPLICABLE
- Bootstrap deadline/expiry: NOT APPLICABLE
- Rollback/stop condition if the bootstrap deadline is missed: NOT APPLICABLE
- Any backup/recovery evidence required and verified: verified recoverable snapshot of the exact pre-merge head and affected user-owned work; rollback route recorded
- Post-merge verification plan: verify main and required workflows on the resulting merge commit
"""

class MergeEvidenceTests(unittest.TestCase):
    def test_complete_record_passes(self):
        errors = gate.validate_record(valid_record(), 12, "main", BASE, REVIEWED)
        self.assertEqual(errors, [])

    def test_fenced_fake_record_is_rejected(self):
        for fence, closing in (("```", "````"), ("~~~", "~~~~")):
            with self.subTest(fence=fence):
                errors = gate.validate_record(f"{fence}markdown\n{valid_record()}\n{closing}\n", 12, "main", BASE, REVIEWED)
                self.assertTrue(any("Required section" in error for error in errors))

    def test_fenced_fields_cannot_fill_missing_real_field(self):
        record = valid_record().replace("- Evidence: tests and source review recorded in this PR\n", "", 1)
        record = record.replace("### Safety and security\n", "### Safety and security\n```text\n- Evidence: fabricated from example\n```\n", 1)
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Safety and security: evidence is required" in error for error in errors))

    def test_html_comment_fields_cannot_satisfy_missing_evidence(self):
        record = valid_record().replace(
            "- Evidence: tests and source review recorded in this PR\n",
            "<!--\n- Evidence: hidden evidence\n-->\n",
            1,
        )
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Safety and security: evidence is required" in error for error in errors))

    def test_unclosed_fence_fails_closed(self):
        errors = gate.validate_record("```markdown\n" + valid_record(), 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Required section" in error for error in errors))

    def test_duplicate_required_section_fails(self):
        record = valid_record() + "\n## Change identity\n"
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("exactly once" in error for error in errors))

    def test_duplicate_field_fails_closed(self):
        record = valid_record().replace(
            "- Research question: how to technically enforce the gate",
            "- Research question: how to technically enforce the gate\n- Research question: duplicate value",
        )
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Research question" in error for error in errors))

    def test_documented_literature_gap_is_explicit_exception(self):
        record = valid_record().replace("https://link.springer.com/article/10.1000/example and ", "")
        record = record.replace(
            "- Methodological limits, conflicts, or evidence gaps: noted",
            "- Methodological limits, conflicts, or evidence gaps: no directly applicable peer-reviewed research; documented literature gap",
        )
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertEqual(errors, [])

    def test_missing_lens_fails(self):
        record = valid_record().replace("### Trust and human impact", "### Trust perspective")
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Trust and human impact" in error for error in errors))

    def test_blocked_lens_fails(self):
        record = valid_record().replace("- Assessment: PASS\n- Evidence:", "- Assessment: BLOCKED\n- Evidence:", 1)
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("BLOCKED" in error for error in errors))

    def test_identity_mismatch_fails(self):
        record = valid_record().replace(f"- Reviewed code SHA (parent of this evidence-only commit): {REVIEWED}", f"- Reviewed code SHA (parent of this evidence-only commit): {BASE}")
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Reviewed code SHA" in error for error in errors))

    def test_high_risk_requires_research_and_official_source(self):
        record = valid_record().replace("https://link.springer.com/article/10.1000/example", "no citation")
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("peer-reviewed" in error for error in errors))

    def test_bootstrap_exception_requires_complete_time_bound_controls(self):
        record = valid_record().replace(
            "- Bootstrap change?: NO",
            "- Bootstrap change?: YES",
        )
        replacements = {
            "Gate that cannot yet apply: NOT APPLICABLE": "Gate that cannot yet apply: the exact-head App status cannot run until the trusted workflow is on the default branch",
            "Existing live controls and compensating manual controls: NOT APPLICABLE": "Existing live controls and compensating manual controls: current hygiene, secret scanning, CodeQL, complete diff review and exact-head manual owner approval",
            "Manual owner approval evidence/state: NOT APPLICABLE": "Manual owner approval evidence/state: pending; explicit owner approval of this exact PR head is required before merge",
            "Post-merge configuration and acceptance-test owner: NOT APPLICABLE": "Post-merge configuration and acceptance-test owner: repository owner",
            "Bootstrap deadline/expiry: NOT APPLICABLE": "Bootstrap deadline/expiry: within 24 hours after merge",
            "Rollback/stop condition if the bootstrap deadline is missed: NOT APPLICABLE": "Rollback/stop condition if the bootstrap deadline is missed: freeze further merges and revert the bootstrap change until the App and ruleset gates are verified",
        }
        for old, new in replacements.items():
            record = record.replace(old, new)
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertEqual(errors, [])

    def test_bootstrap_exception_without_deadline_fails_closed(self):
        record = valid_record().replace(
            "- Bootstrap change?: NO",
            "- Bootstrap change?: YES",
        ).replace(
            "Bootstrap deadline/expiry: NOT APPLICABLE",
            "Bootstrap deadline/expiry: when convenient",
        )
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("concrete date or bounded duration" in error for error in errors))

    def test_non_bootstrap_cannot_hide_bootstrap_controls(self):
        record = valid_record().replace(
            "Gate that cannot yet apply: NOT APPLICABLE",
            "Gate that cannot yet apply: a live ruleset check",
        )
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Non-bootstrap change must mark" in error for error in errors))

    def test_missing_residual_approval_fields_fail_closed(self):
        record = valid_record().replace("- Post-merge verification plan: verify main and required workflows on the resulting merge commit\n", "")
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Post-merge verification plan" in error for error in errors))

    def test_high_risk_requires_verified_recovery_snapshot(self):
        record = valid_record().replace(
            "- Any backup/recovery evidence required and verified: verified recoverable snapshot of the exact pre-merge head and affected user-owned work; rollback route recorded",
            "- Any backup/recovery evidence required and verified: no backup required",
        )
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("verified recoverable pre-merge snapshot or backup" in error for error in errors))

    def test_critical_blocker_fails_closed_without_echoing_untrusted_value(self):
        canary = "CANARY_UNTRUSTED_EVIDENCE_987654"
        record = valid_record().replace("- Critical blockers: NONE", f"- Critical blockers: {canary}")
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("Critical blockers remain" in error for error in errors))
        self.assertNotIn(canary, "\n".join(errors))

    def test_source_host_matching_rejects_suffix_spoof(self):
        self.assertFalse(gate.host_is_in({"docs.github.com.attacker.invalid"}, "docs.github.com"))
        self.assertTrue(gate.host_is_in({"api.docs.github.com"}, "docs.github.com"))

    def test_missing_residual_risk_fails(self):
        record = valid_record().replace("- Assessment: PASS", "- Assessment: PASS WITH RESIDUAL RISK", 1).replace("- Residual risk and mitigation: none identified", "- Residual risk and mitigation: TODO", 1)
        errors = gate.validate_record(record, 12, "main", BASE, REVIEWED)
        self.assertTrue(any("residual risk" in error.lower() for error in errors))

if __name__ == "__main__":
    unittest.main()
