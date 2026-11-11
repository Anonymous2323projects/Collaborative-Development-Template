# Pull Request Assurance Record

> For substantive changes, copy this template to an appropriate PR record (for example `reviews/PR-<number>.md`) or adapt it into the PR description. Replace prompts with verified facts. Keep private project details in restricted storage. This is review evidence, not proof that the claims are true or that owner approval is technically enforced. Use proportionate depth.

## Change identity

- PR number:
- Base branch:
- Base SHA (40 characters):
- Exact reviewed PR head SHA (40 characters):
- Risk: LOW / MODERATE / HIGH / CRITICAL
- Goal and user outcome:
- Scope and non-goals:
- Affected components, users, data, and trust boundaries:

## Research and evidence

- Research question:
- Sources (prefer DOI/peer-reviewed research, standards, law, and official platform documentation):
- What each source supports:
- Publication/version/date and applicability:
- Methodological limits, conflicts, or evidence gaps:
- Alternatives considered and why this option was selected:
- If external research was not needed, explain why the change is genuinely low risk:

## Independent review

- Independent review status: REQUIRED / NOT REQUIRED
- Primary reviewer/coordinator identity:
- Reviewer/agent identity (distinct from the primary reviewer):
- Reviewer type: HUMAN / AI / NOT REQUIRED
- Exact code SHA reviewed:
- Scope reviewed: state whether the complete exact-head diff and relevant surrounding implementation were reviewed; HIGH/CRITICAL changes must cover the complete diff. Record any unreviewed areas honestly.
- Report/reference:
- Findings and disposition:
- Independence and limitations:
- If not required, why:

## Five-perspective assessment

### Safety and security

- Assessment: PASS / PASS WITH RESIDUAL RISK / BLOCKED / NOT APPLICABLE
- Evidence:
- Hazards/threats and controls:
- Residual risk and mitigation:
- If not applicable, why:

### Legal solidity and privacy

- Assessment: PASS / PASS WITH RESIDUAL RISK / BLOCKED / NOT APPLICABLE
- Evidence:
- Data, legal, licence, rights, and confidentiality implications:
- Residual risk and mitigation:
- If not applicable, why:

### Usability

- Assessment: PASS / PASS WITH RESIDUAL RISK / BLOCKED / NOT APPLICABLE
- Evidence:
- User workflow, accessibility, recovery, and compatibility:
- Residual risk and mitigation:
- If not applicable, why:

### Trust and human impact

- Assessment: PASS / PASS WITH RESIDUAL RISK / BLOCKED / NOT APPLICABLE
- Evidence:
- Truthfulness, consent, fairness, transparency, and affected parties:
- Residual risk and mitigation:
- If not applicable, why:

### Freedom and ownership

- Assessment: PASS / PASS WITH RESIDUAL RISK / BLOCKED / NOT APPLICABLE
- Evidence:
- User control, portability, choice, and ownership:
- Residual risk and mitigation:
- If not applicable, why:

## Documentation-to-implementation traceability

| Requirement or policy | Implementation/control | Test or evidence | User documentation | Residual risk |
|---|---|---|---|---|
| | | | | |

- Contradictions, stale statements, paradoxes, missing edge cases, or duplicate authority checked:
- Result:

## Validation evidence

| Command/check | Exact version/environment | Result | Evidence or run URL |
|---|---|---|---|
| | | PASS / FAIL / NOT RUN | |

- Complete diff reviewed: YES / NO — for substantive changes, the primary reviewer must inspect the complete exact-head diff before requesting merge approval.
- Checks not run and why:
- Exact commit SHA tested:

## Systemic recurrence review

- Was this change prompted by a defect, incident, near miss, or procedural weakness? YES / NO:
- Related procedures, instructions, templates, workflows, permissions, and tests searched:
- Similar weaknesses found:
- Changes made to prevent recurrence:
- If no systemic review was needed, explain why:

## Efficiency audit

- Duplicate work or contradictory sources removed:
- Existing evidence reused and why still valid:
- Tests selected and why they cover the affected risk:
- Runtime/maintenance/user burden:
- Safety-critical work intentionally retained:

## Residual risk and approval

- Open findings and residual risks:
- Critical blockers: NONE / describe blockers
- Required user/owner decision:
- Merge authorization state: PENDING EXPLICIT OWNER DECISION / APPROVED FOR EXACT HEAD (with evidence)
- Authorization mechanism: MANUAL PROCEDURE / independently verified platform gate (describe evidence)
- Base/head freshness rechecked at: PENDING
- Changes to security policy or merge controls and extra review required:
- Any backup/recovery evidence required and verified:
- Post-merge verification plan:
