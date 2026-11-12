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
- [ ] For significant changes, preserve the exact pre-merge **target tip/base**, affected paths, intended integration and separate PR-head evidence; verify a realistic recovery/rehearsal route. The optional `scripts/rehearse_pr_recovery.py` Git-tree test requires **Git 2.46.0 or newer** (a syntax-only `--no-lazy-fetch` probe wrongly accepted vulnerable Git 2.45.0), a trusted local Git installation and repository/configuration, and all necessary base/head commit, tree and blob objects already available locally. It uses a temporary clone and index-only `read-tree`/`apply --cached`/`write-tree` round-trip, does not check out files, blocks Git network transports (local-file protocol only) and disables promisor lazy fetching. Git subprocess transport blocking does **not** sandbox untrusted local Git configuration or the OS, and this proof is **not** an external backup or a later-work-safe rollback. Its status is not automatically required by branch rules; checkout steps preceding the rehearsal may themselves use the network.

## Merge and release
- [ ] For ordinary PRs, required GitHub rulesets and status checks are verified live, not inferred from workflow files.
- [ ] A manual exact-head owner decision is recorded as procedural; do not claim it is a required GitHub status check.
- [ ] Required checks are successful for the current PR's evaluated revision (head or test-merge ref), linked to the exact reviewed base/head; final evidence is recorded after the last commit, outside a self-changing PR-branch file.
- [ ] Review threads are resolved; the owner has separately approved the PR number, target branch and **exact base/head SHA pair**. Any base/head movement voids approval.
- [ ] The owner has explicitly authorized the merge/release where required.
- [ ] Post-merge verification and handover updates are planned.

For low-risk changes, use one short record with links or N/A for irrelevant fields. Do not omit a perspective; explain why deeper checks are unnecessary. Mark independent review as REQUIRED/PENDING/COMPLETED separately where applicable; a filled checklist is not proof of completion or safety.
