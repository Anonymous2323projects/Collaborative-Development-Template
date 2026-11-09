# Change, Review, and Merge Assurance Standard

## Purpose and status

This standard defines how meaningful changes are researched, assessed, implemented, verified, and authorized. It applies across the project lifecycle: requirements, design, code, configuration, documentation, dependencies, automation, privacy, security, collaboration, release, incident response, and governance.

The standard is designed around five project priorities: **Safety, Legal solidity and privacy, Usability, Trust and human impact, and Freedom and ownership**. It is not a guarantee that a project is safe, secure, lawful, or defect-free. A completed form is not proof that its claims are true.

The governing principle is **evidence before confidence; technical enforcement before procedural promises; safety before speed**.

## 1. Scope and risk-based depth

Apply this process to:
- new or changed functionality, architecture, data flows, permissions, integrations, dependencies, CI/CD, deployment, release, and update mechanisms;
- changes to project instructions, governance, security/privacy/legal policy, review or merge procedures, and automation;
- incidents, near misses, review failures, process exceptions, and discoveries that reveal a systemic weakness.

Classify the change:
- **Low:** localized, readily reversible, no material security/privacy/legal/user-data effect.
- **Moderate:** affects multiple components, users, workflows, dependencies, or operational behavior.
- **High:** changes trust boundaries, authentication/authorization, sensitive data, release/update paths, security controls, legal/privacy commitments, or other high-impact behavior.
- **Critical:** credible severe harm, active exploitation/compromise, irreversible data loss, or a change that could disable essential safeguards.

Risk classification determines depth, not whether the five perspectives apply. All five are considered for every meaningful change. For high and critical changes, use deeper hazard analysis, current authoritative sources, independent review, and explicit evidence. Low-risk work remains proportionate, but still receives a scope and regression check.

## 2. Research standard

Research is a required engineering activity, not a speed bump to skip.

1. Define the question, system boundary, affected assets/users, decision to be made, and what evidence would change the decision.
2. Search first for primary evidence: applicable law/regulation, standards, official platform/product documentation, specifications, advisories, and original research.
3. Prefer peer-reviewed systematic reviews, empirical studies, standards, and primary sources. Use reputable secondary analysis only to clarify or triangulate. Do not treat blogs, vendor marketing, search snippets, or AI-generated summaries as authoritative evidence.
4. For high/critical decisions, triangulate with at least two independent source classes, normally an authoritative standard/official specification and relevant peer-reviewed research. Explain when no directly applicable academic literature exists.
5. Check publication date, scope, methodology, population, assumptions, conflicts of interest, limitations, and applicability to this project. Prefer the newest authoritative version while retaining older foundational research when still relevant.
6. Record the exact source URL/DOI, publication/version/date, the claim it supports, and limitations. Distinguish evidence from interpretation and recommendation.
7. Compare viable alternatives, including doing nothing, using an established solution, and building custom controls. Assess security, privacy, licence, compatibility, maintenance, cost, complexity, and failure modes.
8. Continue research until the decision is sufficiently supported or a genuine evidence gap is identified. Do not stop merely because the first plausible answer is convenient.

Academic evidence is not automatically transferable. State the study design and external-validity limits. For example, a systematic review can establish the state of research but may also show that practitioner tooling and validation remain immature. Do not turn a promising method into a guaranteed control.

## 3. Hazard and system analysis

For moderate, high, and critical changes, model the relevant system rather than reviewing a file in isolation.

- Identify system goals, stakeholders, assets, trust boundaries, external dependencies, controllers/decision-makers, controlled processes, feedback, and assumptions.
- Identify hazards and unsafe control actions: a required action not provided, an unsafe action provided, an action at the wrong time/order, or an action applied for too long/too early/too late.
- Identify threats, misuse cases, failure modes, cascading effects, human error paths, degraded modes, recovery needs, and common-cause failures.
- Trace each material hazard to preventive controls, detective controls, recovery controls, tests, owners/roles, and residual risk.
- Check whether a control can be bypassed, disabled, misconfigured, or rendered ineffective by another workflow.
- Revisit the analysis when architecture, assumptions, dependencies, users, or operational context change.

Use STPA-style system-theoretic hazard analysis where it adds value; use threat modelling, FMEA, attack trees, fault trees, privacy impact analysis, or other suitable methods as complementary techniques. Do not claim a formal STPA or safety case was performed unless its method and artefacts were actually completed.

## 4. Five-perspective assessment

Each perspective must have its own finding, evidence, residual risk, and disposition. One strong perspective cannot compensate for a critical failure in another.

1. **Safety and security:** harm scenarios, threat model, trust boundaries, least privilege, input validation, data integrity, resilience, secrets, supply chain, incident response, backup/recovery, and abuse potential.
2. **Legal solidity and privacy:** jurisdiction and applicable obligations, personal data lifecycle, lawful basis where relevant, purpose limitation, minimization, retention, access, consent, confidentiality, intellectual property, licensing, consumer rights, and accurate claims.
3. **Usability:** understandable behavior, accessibility, error prevention, safe defaults, discoverability, reversibility, recovery, Free-plan compatibility where applicable, and operational burden.
4. **Trust and human impact:** truthful claims, provenance, evidence quality, uncertainty, explainability, consent, fairness, human oversight, foreseeable effects on users/contributors, and transparent incident handling.
5. **Freedom and ownership:** user agency, choice, control, portability, interoperability, ownership, non-coercive defaults, and least-restrictive effective safeguards.

Record **PASS**, **PASS WITH RESIDUAL RISK**, **BLOCKED**, or **NOT APPLICABLE** for each lens. “Not applicable” requires a reason. “Pass with residual risk” requires a named risk and mitigation/acceptance route. Any unresolved critical hazard, material legal/privacy uncertainty, unverified security-critical behavior, or missing mandatory approval blocks the affected merge/release.

These are review perspectives, not a claim that five independent human specialists were consulted. Where independent review is required, identify the actual reviewer and scope.

## 5. Systemic recurrence rule

A serious defect in a procedure, control, review, or merge is not treated as an isolated incident.

When a material procedural failure, paradox, omission, or unsafe outcome is found:

1. Preserve evidence and define the failure precisely; do not speculate about blame.
2. Identify the failed control, missing control, ineffective control, incorrect assumption, and the path by which the failure passed.
3. Search the entire affected project for the same pattern and for analogous controls—not only the file where it was found.
4. Review every related procedure, instruction, template, automation, workflow, permission, test, handover, release rule, and user-facing claim.
5. Check dependencies and adjacent projects only where a shared control or explicit integration makes them relevant. Keep private project context private.
6. Determine root and contributing causes, including human factors, unclear ownership, conflicting instructions, automation gaps, and incentive/efficiency pressure.
7. Update the canonical procedure and every dependent copy or implementation; remove contradictions and obsolete instructions.
8. Add a regression test or technical control that would have detected or prevented recurrence. Test both the failure case and the legitimate safe case.
9. Re-run the five-perspective review on the systemic remediation and verify the resulting implementation, not just its documentation.
10. Record scope, evidence, affected components, fixes, residual risks, and follow-up checks. Do not close the incident merely because a document was edited.

If the scope is unclear, widen the investigation until the boundary is evidence-based. Continue safe independent work; pause only the unsafe operation or a genuinely user-gated decision.

## 6. Documentation-to-implementation assurance

For every meaningful change, compare:
- stated requirements and project instructions;
- actual source code and configuration;
- automated tests and CI workflows;
- GitHub repository settings and permissions;
- user-facing documentation, onboarding, templates, and examples;
- operational, incident, backup, and recovery procedures.

Create a traceability matrix for material requirements: requirement/policy → implementation/control → test/evidence → user documentation → residual risk/owner. Search for contradictions, stale claims, duplicated authority, ambiguous priority, impossible requirements, missing edge cases, unsafe exceptions, and undocumented behavior.

A documentation statement such as “merges are protected” is not accepted until the live repository rules, required checks, permissions, and bypass configuration have been inspected. A workflow file is not proof that the workflow ran. A successful workflow is not proof that the check is required by the branch ruleset. A passing static validator is not proof that its evidence is truthful.

## 7. Technical enforcement architecture

Use defense in depth. Prefer controls that block an unsafe state over controls that merely remind a person.

### Repository and merge controls

Where the platform supports them and the project risk justifies them:
- protect the default branch with an active ruleset;
- require pull requests and block direct pushes, deletion, and non-fast-forward updates;
- require relevant status checks from the expected trusted integration;
- require the branch to be up to date with the base branch (strict checks) or use an appropriate merge queue;
- require review-thread resolution;
- require signed commits where the signing model is practical and verified;
- prohibit bypass actors or document a narrowly scoped emergency bypass with audit evidence;
- require an exact-head maintainer authorization for consequential merges when a separate reviewer approval is impractical;
- ensure a changed head SHA invalidates prior authorization;
- protect workflow files and policy files with focused ownership/review where feasible.

Do not set a required human approval count that makes a single-maintainer repository impossible to operate. Instead, preserve an explicit owner decision through a platform-enforced, exact-commit authorization gate. For organization-owned repositories, configure an explicit authorized-maintainer allowlist. For user-owned repositories, the repository owner may be the default authorizer. Fail closed if the authorized identity cannot be established.

### CI and automated evidence

At minimum, configure the checks relevant to the repository's actual stack:
- unit and regression tests;
- repository hygiene and documentation/link checks;
- secret scanning;
- static analysis/security scanning (for example, CodeQL for supported languages);
- dependency/licence and workflow-policy checks where applicable;
- PR-specific assurance-record validation;
- build, integration, compatibility, accessibility, and artifact checks where relevant.

Pin third-party actions to full commit SHAs, use least-privilege token permissions, avoid privileged execution of untrusted PR code, and keep secrets out of untrusted workflows. Treat all issue/PR content and downloaded artifacts as untrusted data.

A CI job must fail closed on missing evidence, mismatched PR/base/head identity, blocked perspective, unresolved required fields, or policy violations. The CI job validates presence and structure; human/AI reviewers remain responsible for the quality and truth of the analysis.

### Exact-head authorization

A merge authorization must refer to the exact 40-character PR head SHA. A maintainer command such as `/authorize-merge <SHA>` may create a required commit status only after verifying:
- the actor is on the configured authorized-maintainer list (or is the repository owner under the user-repository fallback);
- the PR is open, not a draft, and targets the default branch;
- the PR head exactly matches the supplied SHA;
- all review threads are resolved;
- the PR-specific assurance record exists and its required CI check is successful or pending in the expected state.

The authorization status is attached to that exact commit. Any new commit requires a new authorization. A corresponding revoke command should set a failing status. The workflow must not check out or execute code from the untrusted PR head and must use minimal permissions. If the platform cannot securely implement this, retain a manual explicit approval step and state that it is not technically enforced.

## 8. PR-specific assurance record

Each pull request must include `reviews/PR-<number>.md`, copied from [the PR assurance record template](docs/PR_ASSURANCE_RECORD_TEMPLATE.md). It records:
- PR number, base branch/SHA, head SHA, risk level, scope, and non-goals;
- research question, source quality, DOI/official sources, and applicability limits;
- each of the five perspective assessments, evidence, findings, and residual risks;
- documentation-to-implementation traceability;
- commands/tests/checks and exact results, including what was not run;
- systemic recurrence search and affected procedures reviewed;
- efficiency audit: duplicate work removed, evidence reused, and why selected checks were sufficient;
- outstanding blockers and the exact owner-authorization state.

For low-risk changes, keep the record concise and explain why deeper analysis is unnecessary. For high/critical changes, include substantive hazard analysis and independent review evidence. Never fill the record with generic “passed” statements.

## 9. Independent AI and human review

Use a second agent such as Codex when it can provide meaningful independent analysis, especially for high/critical changes, systemic procedure failures, security-sensitive code, and large merges.

Give the second agent:
- exact repository, branch, base/head SHA, scope, and non-goals;
- the five review perspectives and specific threat/hazard questions;
- instructions to inspect the full diff and relevant surrounding implementation;
- instructions to verify documentation/code parity, contradictions, paradoxes, and tests;
- a requirement to preserve local changes and avoid destructive operations;
- a requirement to report evidence, limitations, commands, and exact SHAs.

Do not treat two AI reviews as independent human approval or proof of correctness. Reconcile disagreements explicitly. The primary reviewer remains responsible for verification. Human owner authorization remains separate from AI analysis.

## 10. Merge and release gates

A change is ready for merge only when:
- scope and exact base/head SHAs are known;
- the full diff and affected system context have been reviewed;
- research is adequate for the risk;
- all five perspective assessments are complete;
- documentation matches implementation and tests;
- systemic recurrence checks are complete where triggered;
- required CI checks pass on the exact current head;
- review threads are resolved;
- backup/recovery is verified where the change is high-impact or hard to reverse;
- residual risks are documented and acceptable;
- the exact-head owner authorization is present where required;
- no unresolved critical blocker or explicit approval boundary remains.

A change may be prepared and brought to PR-ready status autonomously within scope. Do not merge, release, delete data/history, change repository visibility/ownership/access, or take other reserved irreversible actions without explicit authorization. A user authorization to research or implement is not automatically merge authorization.

After merge, verify the resulting default-branch SHA, exact changed files, CI runs on the merge commit, release status, and any required rollback/monitoring. Update canonical memory and handover records.

## 11. Efficiency without weakening safety

Efficiency means eliminating waste, not shortening necessary research.

- Read and compare related procedures in batches.
- Maintain one canonical source for each rule and link to it elsewhere.
- Reuse evidence only while the exact code, configuration, permission, environment, and risk assumptions remain unchanged.
- Select tests based on changed behavior and risk; run broad integration checks at system boundaries and release points.
- Automate deterministic checks and test the validators themselves with negative and positive cases.
- Avoid repeated generic checklists, duplicate trackers, unnecessary dependencies, and manual copying of facts already available through tools.
- Measure false positives, false negatives, runtime, maintenance burden, and user effort. A faster process that misses hazards is not an improvement.
- Do not optimize away independent review, backup, required research, or exact-head verification for high-impact changes.

## 12. Research basis and limitations

The approach draws on:
- NIST SP 800-218 (SSDF) for integrating secure-development practices throughout the lifecycle and addressing root causes;
- NIST SP 800-204D for integrating software supply-chain security into CI/CD;
- STPA research by Nancy Leveson for system-level hazards, unsafe control actions, lifecycle traceability, and refinement of safety constraints;
- empirical secure-code-review research showing that concerns may be acknowledged without being fixed and that unresolved security concerns can still reach merged code;
- systematic literature review of security assurance cases, which supports structured claims and evidence but also warns that practitioner validation and tool support remain immature;
- SLSA provenance specifications for verifiable build origin and inputs;
- current GitHub ruleset documentation for enforceable branch, review, status-check, and bypass controls.

These sources support the principles, not a claim that this template is certified or that the proposed process is formally proven. Record the source versions and re-check them at meaningful maintenance checkpoints.

### References

**Peer-reviewed research**
- Mohamad, M., Steghöfer, J.-P., & Scandariato, R. (2021). *Security assurance cases—state of the art of an emerging approach*. Empirical Software Engineering, 26, 70. Systematic literature review of 51 papers; identifies a gap between proposed assurance-case approaches and their validation/tool support. https://doi.org/10.1007/s10664-021-09971-7
- Charoenwet, W., Thongtanunam, P., Pham, V.-T., et al. (2024). *Toward effective secure code reviews: an empirical study of security-related coding weaknesses*. Empirical Software Engineering, 29, 88. Empirical analysis of 135,560 review comments in OpenSSL and PHP; reports that some security concerns are acknowledged but remain unresolved, and some unresolved concerns reach merged code. https://doi.org/10.1007/s10664-024-10496-y
- Leveson, N. G. (2018). *Safety Analysis in Early Concept Development and Requirements Generation*. INCOSE International Symposium, 28(1), 441–455. Describes STPA as a lifecycle method for deriving safety constraints and maintaining traceability as designs evolve. https://doi.org/10.1002/j.2334-5837.2018.00492.x

**Standards and primary technical sources**
- NIST SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1* (2022). https://csrc.nist.gov/pubs/sp/800/218/final
- NIST SP 800-204D, *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines* (2024). https://doi.org/10.6028/NIST.SP.800-204D
- SLSA v1.0, Build Track Basics and Build Provenance. https://slsa.dev/spec/v1.0/levels and https://slsa.dev/spec/v1.0/provenance
- GitHub Docs, *Available rules for rulesets*. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Docs, *About protected branches*. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches

## 13. Public/private boundary

This public standard contains only generic reusable process guidance. Keep project-specific memory, private decisions, personal preferences, internal incidents, operational details, credentials, and private coordination records in their appropriate private repositories. Public template content must remain generic, sanitized, and suitable for unrelated users.
