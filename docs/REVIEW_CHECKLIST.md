# Lightweight Review Checklist

Use this checklist for routine changes. For substantive changes, the complete method and required PR evidence are in [Change, Review, and Merge Assurance](../MERGE_AND_CHANGE_ASSURANCE.md).

## Purpose and scope
- [ ] The change addresses a clear problem or user outcome.
- [ ] Scope, non-goals, affected components, and acceptance criteria are known.
- [ ] Verified facts, assumptions, and unresolved questions are distinguished.

## Five required perspectives
- [ ] Safety and security: hazards, threats, trust boundaries, safeguards, recovery, and abuse cases.
- [ ] Legal solidity and privacy: applicable duties, personal data, confidentiality, rights, and licences.
- [ ] Usability: safe defaults, accessibility, clarity, and recovery.
- [ ] Trust and human impact: truthful claims, evidence, consent, fairness, and affected parties.
- [ ] Freedom and ownership: user choice, control, portability, and least-restrictive safeguards.

## Implementation and evidence
- [ ] Requirements and documentation match code, configuration, tests, workflows, and live settings.
- [ ] Relevant research and authoritative sources were checked for the risk level.
- [ ] Complete diff, dependencies, scripts, workflows, secrets, and public metadata were reviewed.
- [ ] Tests/checks ran on the exact reviewed code; omissions are explicit.
- [ ] Similar weaknesses in related procedures were searched when a systemic issue was found.
- [ ] Residual risks and recovery steps are documented.

## Merge and release
- [ ] For ordinary PRs, required GitHub rulesets and status checks are verified live, not inferred from workflow files.
- [ ] A manual exact-head owner decision is recorded as procedural; do not claim it is a required GitHub status check.
- [ ] Required checks are successful on the current exact PR head.
- [ ] Review threads are resolved; the owner has separately approved the exact current PR head before any merge.
- [ ] The owner has explicitly authorized the merge/release where required.
- [ ] Post-merge verification and handover updates are planned.

For low-risk changes, keep the evidence concise. Do not omit a perspective; explain why a deeper check is unnecessary. A completed checklist is not proof of correctness or safety.
