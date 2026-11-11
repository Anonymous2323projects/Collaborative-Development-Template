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

## 7. Practical checks and explicit owner decision

### What the platform enforces

Inspect the **live** repository ruleset, branch protections, bypass actors, required checks, check origins, and whether checks apply to the head or the tested merge revision. A workflow file or a passing check does not prove that a check is required. GitHub Free supports useful protections for public repositories; private-repository feature availability depends on the plan and ownership model. Verify rather than assume.

Where supported and proportionate, require pull requests, appropriate tests and scanners, resolved review threads, a current branch or merge queue, and safeguards against force pushes and deletion. Pin CI actions, minimize permissions, and do not execute untrusted pull-request code with privileged tokens or secrets. If the platform cannot enforce a particular protection, document the limitation and keep a human decision point; do not claim it is enforced.

### Review evidence and CI

For substantive or higher-risk work, document the exact base/head commits, affected trust boundaries, five-perspective assessment, complete diff review, tests and their actual evaluated revision, independent review where warranted, open findings, and recovery plan. The [assurance-record template](docs/PR_ASSURANCE_RECORD_TEMPLATE.md) is a reusable format; a PR description or equivalent private project record may be appropriate when it preserves the same evidence. Keep sensitive project records out of public repositories.

Run stack-appropriate unit/regression tests, repository hygiene, secret scanning, static analysis, licence/dependency and workflow checks. A passing check proves only its stated scope. An optional evidence validator may help with formatting and identity checks, but it does not authenticate reviewer claims or owner approval. **This template does not currently provide an automated owner-authorization gate or a required assurance-record validation check.**

### Manual exact-head owner approval (procedural fallback)

Until a separately reviewed, configured, and adversarially tested technical owner gate is proven to work, use a transparent manual procedure:

1. Re-fetch the live PR number, target branch, base SHA, head SHA, status, checks, and unresolved review threads immediately before deciding.
2. Inspect the full current diff, any protected-policy changes, and the applicable assurance evidence. Stop for unresolved critical findings, incomplete checks, stale reviews, or inadequate recovery.
3. Ask the authorized owner to explicitly approve **that PR and full 40-character head SHA**, recording the decision in an appropriate audit trail. Approval of a draft, plan, or previous SHA is not merge authorization.
4. Immediately before merging, re-fetch head **and base** and check the tested revision, ruleset, review threads, and approval scope. If anything material changed, stop and request renewed review/approval. Do not rely on an old approval.
5. Only the owner or an explicitly authorized operator performs the merge. Afterward, verify the default-branch result and checks, and update the handover.

**Important:** a manual approval comment does **not** create a GitHub-required status, cannot block a maintainer from clicking Merge, and does not automatically expire or revoke a prior decision. This is a procedural control, not a platform-enforced authorization boundary. Never present an ordinary GitHub Actions check as an independently authenticated owner-approval check.

### Optional future technical gate — not part of this change

A dedicated GitHub App, Checks API, protected deployment, or similar design needs its own threat model, minimal-permission review, trusted-source separation, exact evaluated-SHA binding, strict base freshness, replay/revocation semantics, protected-credential analysis, safe bootstrap, and disposable positive/negative acceptance tests on the actual GitHub plan. No such mechanism is installed or authorized by this standard. Do not create Apps, secrets, environments, or rulesets without a separate owner decision.

## 8. PR-specific assurance record

For substantive changes, keep a concise PR-specific assurance record, using [the PR assurance record template](docs/PR_ASSURANCE_RECORD_TEMPLATE.md) where useful. High/critical changes should retain a full auditable record; low-risk changes may document the same essentials in the PR description. A record includes:
- PR number, base branch/SHA, exact reviewed head SHA, risk level, scope, and non-goals;
- for HIGH/CRITICAL changes, an independent review record naming the primary reviewer and distinct independent reviewer/agent, reviewer type, exact code SHA reviewed, scope, report reference, findings/disposition, and independence limitations; for lower-risk changes, record whether independent review was not required and why;
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

For every substantive change, the primary reviewer must explicitly confirm that the complete exact-head diff was reviewed. For HIGH/CRITICAL changes, independent review must also cover the complete diff and relevant surrounding implementation. A partial-file review does not satisfy the high-impact gate. A written record alone does not enforce these requirements.

## 10. Merge and release gates

A change is ready for merge only when:
- scope and exact base/head SHAs are known;
- the full diff and affected system context have been reviewed;
- research is adequate for the risk;
- all five perspective assessments are complete;
- documentation matches implementation and tests;
- systemic recurrence checks are complete where triggered;
- required CI checks pass on the exact revision GitHub evaluates for the current PR (head or tested merge ref); verify the relationship to the current head and base;
- review threads are resolved;
- before a high-impact or hard-to-reverse merge, create and verify a recoverable snapshot of the exact pre-merge head and any user-owned work that could be affected; record the backup reference and a realistic rollback/recovery route; a Git commit alone is not assumed to be an independent backup;
- residual risks are documented and acceptable;
- the owner has separately authorized the exact current PR head and scope, with manual authorization clearly labeled procedural unless a verified technical gate exists;
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
- GitHub Docs, *Deployments and environments* (required reviewers, deployment branch policies, administrator bypass). https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- GitHub Docs, *Workflow syntax: GITHUB_TOKEN permissions and pull-request trust behavior*. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

## 13. Public/private boundary

This public standard contains only generic reusable process guidance. Keep project-specific memory, confidential decisions, private discussions, operational details, credentials, and other non-public records in an appropriate access-restricted private location. Public template content must remain generic, sanitized, and suitable for unrelated users.
