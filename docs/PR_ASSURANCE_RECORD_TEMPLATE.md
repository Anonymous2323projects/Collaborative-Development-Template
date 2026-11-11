# Pull Request Assurance Record

> For substantive changes, use **one record**, preferably the PR description or an external/restricted record, and update its **final** base/head/CI/review status **after the last candidate commit**. If a versioned file such as `reviews/PR-<number>.md` is placed inside the PR branch, it changes the head and cannot contain its own final head SHA: distinguish the reviewed code revision there and record final head/base/approval outside the branch. Do not require an unimplemented evidence-only-commit validator. For low-risk work, a short summary with links or N/A for irrelevant sections is sufficient. A filled form is not proof of review, approval, or technical enforcement.

## Change identity

- PR number:
- Target/base branch:
- Exact target-tip/base SHA (40 characters):
- Reviewed code SHA (if different from final head):
- Final PR head SHA (40 characters; record externally after last commit):
- Tested integration SHA (test-merge or head, with corresponding base/head):
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

- Independent review requirement: REQUIRED / NOT REQUIRED (justify if not required)
- Independent review execution: PENDING / COMPLETED / NOT APPLICABLE (a required but pending review is **not** completed)
- Primary reviewer/coordinator identity:
- Reviewer/agent identity (distinct from the primary reviewer):
- Reviewer type: HUMAN / AI / NOT REQUIRED
- Exact code/head SHA reviewed (and base SHA):
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
- Exact SHA evaluated by each check (head or test merge), its paired base/head and check source:

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
- Merge authorization state: PENDING EXPLICIT OWNER DECISION / APPROVED FOR EXACT BASE AND HEAD (with external evidence)
- Authorization mechanism: MANUAL PROCEDURE / independently verified platform gate (describe evidence)
- Approved PR, target branch, exact base SHA, final head SHA, owner and decision reference (outside branch):
- Base/head and integration freshness rechecked at: PENDING (any target/base or head movement voids prior authorization)
- Changes to security policy or merge controls and extra review required:
- Pre-merge target-tip/base SHA and affected paths preserved (separately from PR head):
- Recoverable baseline/backup and actual restoration verification or rehearsal (include limitations):
- Any affected user-owned work or external side effects and recovery approach:
- Post-merge verification plan:
