# Pull Request Assurance Record

> Copy this file to `reviews/PR-<number>.md` in the pull request. Replace every prompt. This is evidence of the review, not proof that the claims are true. Keep the record concise for low-risk changes and substantive for high-risk changes.

## Change identity

- PR number:
- Base branch:
- Base SHA (40 characters):
- Reviewed code SHA (parent of this evidence-only commit):
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

- Complete diff reviewed:
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

## Protected policy change review

> Required only when using /authorize-policy-change. For ordinary PRs, leave this section marked NOT APPLICABLE. The command itself must be posted by an authorized owner on the PR and include the exact current 40-character head SHA.

- Changed policy paths: [comma-separated exact paths; list every protected path exactly once]
- Base SHA: [exact current 40-character base SHA]
- Reason for change: [concrete rationale]
- Adversarial tests: [specific tests and results]
- Rollback/recovery: [concrete recovery steps]
- Independent review reference: [link or durable review identifier]
- Owner decision: NOT APPLICABLE

## Residual risk and approval

- Open findings and residual risks:
- Critical blockers: [NONE or describe blockers]
- Required user/owner decision:
- Merge authorization state: AWAITING EXPLICIT OWNER AUTHORIZATION
- Any backup/recovery evidence required and verified:
- Post-merge verification plan:
