# Integration and Merge Review Standard

Use this standard for substantial, cross-cutting, security/privacy/legal-sensitive, user-facing, or hard-to-reverse changes. Scale the depth to the change; do not turn a typo fix into a release ceremony. This is an AI-assisted review framework, not a guarantee and not a claim that five human specialists were consulted.

## 1. Establish the exact scope and baseline

Before editing or approving a merge, record:
- target repository, branch, current base SHA, proposed head SHA, and working-tree state where relevant;
- goal, acceptance criteria, non-goals, affected components, files, users, data flows, dependencies, permissions, and external effects;
- existing behavior and documentation that must remain true;
- required user approvals, irreversible actions, and recovery options.

Review the complete diff against the exact current base. Do not rely on a PR title, summary, old review, stale check, or a branch name as evidence. Recheck the head and base SHAs immediately before merging.

## 2. Trace implementation to documentation

For every changed or affected user-visible behavior, API, configuration, permission, workflow, data flow, installation step, limitation, or recovery path:
- identify the implementing code/configuration and its tests;
- identify the documentation that describes it;
- compare actual behavior with the documented claim, including defaults, prerequisites, exceptions, failure behavior, and platform/plan limitations;
- update both sides when they diverge, or explicitly explain why no documentation change is needed.

Check the reverse direction too: important instructions and promises in documentation must have an implementation, supported platform capability, or clearly labelled manual procedure behind them. Do not document aspirational behavior as if it already exists.

## 3. Detect contradictions, paradoxes, and duplication

Read affected documents together, not one file at a time. Search for:
- conflicting requirements, priorities, approval rules, privacy defaults, retention statements, supported platforms, version numbers, paths, commands, or role responsibilities;
- rules that cancel each other out, create circular dependencies, demand mutually impossible actions, or make a promised workflow impossible;
- exceptions that silently undermine a mandatory safeguard;
- repeated instructions that have drifted apart or create competing sources of truth;
- claims stronger than the evidence or automation can support;
- obsolete links, examples, screenshots, and references.

Prefer one canonical rule with short links from other documents. Record a justified exception at the point where it applies. Resolve material contradictions before merge; do not hide them in a changelog or handover.

## 4. Verify behavior, not just prose

Choose validation from the changed behavior and risk:
- run focused unit/regression tests and relevant integration/build checks;
- test critical instructions and commands in a clean or representative environment where practical;
- verify links, anchors, examples, file paths, workflow syntax, action pins, permissions, and configuration with suitable automated checks;
- inspect failure paths, error messages, defaults, rollback/recovery, accessibility, and platform differences where relevant;
- verify that a test actually exercises the changed behavior; a passing unrelated test is not evidence.

Run checks against the exact PR head SHA before merge. After merge, verify the merge commit and run or inspect the relevant checks on that exact merge SHA. A green PR check is not automatically proof that the merge commit itself passed. Report pending checks as pending, not passed.

## 5. Apply all five review lenses

Assess each lens separately. These are disciplined perspectives, not claims that separate human experts or legal professionals were consulted.

1. **Safety and security:** threat paths, abuse, data loss, credentials, dependency/workflow permissions, supply chain, recovery, and foreseeable harm.
2. **Legal solidity and privacy:** applicable law, licences, rights, confidentiality, data minimization, retention, consent, access, jurisdiction, and whether specialist advice is needed.
3. **Usability:** clarity, accessibility, beginner comprehension, setup burden, error recovery, and whether the documented safe path works in practice.
4. **Trust and human impact:** truthfulness of claims, evidence and uncertainty, consent, fairness, affected people, support expectations, and consequences of failure.
5. **Freedom and ownership:** user choice, control, portability, interoperability, reversibility, lock-in, and the least restrictive effective safeguard.

A serious failure in one lens cannot be averaged away by strengths in another. Record findings, mitigations, residual risks, and any user-owned decision.

## 6. Merge gate and post-merge verification

Before merging:
- verify exact base/head SHAs, complete file list and diff, mergeability, review threads, required approvals, and all relevant checks;
- verify branch protection/ruleset settings when possible; if inaccessible, state that they are unverified and do not infer enforcement from a successful merge;
- verify all material documentation/code consistency and contradiction findings are resolved;
- create and verify a recoverable snapshot of the exact pre-merge head and any user-owned work that could be affected;
- obtain explicit approval for the specific consequential merge and method where required.

After merging:
- verify PR state, merge commit SHA, resulting default-branch SHA, and exact changed paths;
- inspect post-merge checks on the merge SHA, including any still running;
- check for unintended changes, broken links, regressions, and drift between implementation and documentation;
- record backup reference, validation evidence, limitations, residual risks, and next actions in the canonical project record.

Never infer that a successful merge means every post-merge check passed. Never delete the recovery snapshot as routine cleanup.

## 7. Evidence, efficiency, and honest reporting

Record the minimum evidence needed to reproduce the decision: scope, SHAs, files, sources, checks and versions, outcomes, reviewer lenses, limitations, and approvals. Distinguish verified facts, assumptions, recommendations, and unresolved questions.

Reuse evidence only while its exact code, configuration, permissions, environment, requirements, and risk remain unchanged. Re-run only checks invalidated by a change or needed at an integration/release boundary. Batch related work and avoid duplicate trackers. Never skip a safety-critical check for speed.

Automated checks can enforce mechanical properties such as links, required files, workflow permissions, pinned actions, and the presence of review records. They cannot reliably prove that prose is non-contradictory, legally sound, usable, fair, or aligned with runtime behavior. Those require explicit evidence-based review. State this limitation rather than presenting a checklist as an automated guarantee.
