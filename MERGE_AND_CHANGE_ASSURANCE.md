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

Use defense in depth. Prefer controls that block an unsafe state over controls that merely remind a person. Operational setup and acceptance steps are in [Exact-Head Authorization App Setup](docs/EXACT_HEAD_AUTHORIZATION_SETUP.md).

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
- PR-specific assurance-record validation through the trusted default-branch authorizer (not a PR-controlled validator workflow);
- build, integration, compatibility, accessibility, and artifact checks where relevant.

Pin third-party actions to full commit SHAs, use least-privilege token permissions, avoid privileged execution of untrusted PR code, and keep secrets out of untrusted workflows. Treat all issue/PR content and downloaded artifacts as untrusted data.

A CI job must fail closed on missing evidence, mismatched PR/base/head identity, blocked perspective, unresolved required fields, or policy violations. The CI job validates presence and structure; human/AI reviewers remain responsible for the quality and truth of the analysis.

### Exact-head authorization

A merge authorization must refer to the exact 40-character PR head SHA. Use a distinct, independently authenticated status source; a workflow name or the shared GitHub Actions App identity is not a workflow-level trust boundary.

- A trusted workflow on the default branch accepts /authorize-merge <full-40-character-head-SHA> for ordinary PRs, /authorize-policy-change <full-40-character-head-SHA> for protected policy changes, and /revoke-merge <full-40-character-head-SHA> to revoke authorization. Each command must be posted by an authorized owner on the PR itself.
- It checks the actor against an explicit maintainer allowlist (or the repository owner for a user-owned repository), verifies that the PR is open, ready for review, and targets the default branch, and checks the exact current head and base SHAs.
- It checks that required review threads are resolved and validates the PR-specific assurance record using validator code from the trusted default branch.
- It fetches the evidence commit and evidence file through the GitHub API at the exact PR head. The evidence commit must have exactly one parent and change only reviews/PR-<number>.md. The validator receives the file as inert text; no PR checkout, script, workflow, or executable content is run.
- The evidence record must identify the current PR number, base branch/SHA, and parent code SHA; contain all five perspective assessments, source/evidence details, traceability, validation, systemic recurrence review, efficiency audit, and residual-risk/approval state; and contain no unresolved critical blocker. It must also record open findings, the required owner decision, verified backup/recovery evidence, and a concrete post-merge verification plan. For a bootstrap change, the record must identify the gate that cannot yet apply, existing and compensating controls, the manual owner-approval state, a named post-merge configuration/acceptance-test owner, a concrete date or bounded deadline, and a stop/rollback condition. A bootstrap exception is a time-limited residual risk, never a claim that the missing technical control has passed.
- The trusted workflow re-fetches PR state/head/base and review threads immediately before publishing success. A changed head or base during validation fails closed.
- It publishes a pending status before validation, then a success or failure status for the exact head. A new head requires a new owner command. A revoke command publishes a failing status. If the status source is unavailable, the merge remains blocked unless an older successful status still exists; in that exceptional case, the owner must explicitly revoke it or invalidate the old head. Statuses do not expire automatically.
- The required status must be restricted to a dedicated GitHub App identity, not the GitHub Actions App. Install that App only on the relevant repository and grant Commit statuses: read/write plus GitHub's Metadata: read-only baseline, with no other permissions. Mint an installation token scoped to that repository and statuses:write; use it only for status publication. Keep the read-only GITHUB_TOKEN separate for PR/commit/content/review-thread reads. Before configuring the expected-source rule, publish a test status from the App and verify the exact App/context is selectable in the ruleset UI. GitHub's ruleset documentation also refers to a recent check run as a prerequisite; if the commit-status implementation does not satisfy the UI prerequisite, stop and review a Checks API alternative rather than broadening permissions by assumption.
- Run maintainer identity preflight in a separate unprivileged job with no protected environment and no secret/App credential access. Expose only its boolean authorization result as a job output. The environment-protected authorization job must declare `needs: preflight` and run only when `needs.preflight.outputs.authorized == 'true'`; this prevents arbitrary commenters from generating protected-environment approval requests before identity rejection. Store the optional non-secret `MERGE_AUTHORIZER_LOGINS` allowlist as a repository-level Actions variable so preflight can read it without environment access; retain the App Client ID and private key only in the protected environment. Store the App private key only in a dedicated Actions environment secret, not a repository-level secret. Restrict that environment to the exact default branch (for example, main) and disable administrator bypass. GitHub documents that issue_comment workflows run from the default branch, ordinary pull_request workflows use refs/pull/<number>/merge, and environment branch policies are matched against GITHUB_REF. This prevents PR-controlled workflows on pull-request refs from accessing the App key. The repository-hygiene validator requires exactly one literal merge-authorizer environment reference in the trusted authorization workflow, rejects references to that environment or dynamically constructed environment names in other workflows, and prevents other workflows from referencing the merge App client ID/private-key secret. The trusted workflow must not add workflow_dispatch, pull_request_target, or workflow_run paths that let untrusted refs reach that environment.
- Use a pinned, reviewed GitHub-maintained action to mint the short-lived installation token; scope its permission explicitly and allow the action to revoke the token after the job. The installation token expires after one hour. The App private key itself does not expire automatically and requires secure storage, rotation, and manual revocation.
- Require the dedicated App status in the live ruleset and require the PR branch to be up to date with the base. Without strict up-to-date enforcement, a base-branch change can leave an old success status attached to an unchanged PR head.
- The authorizer must reject ordinary automated authorization when the PR changes trusted policy files: any .github configuration, secret-scanner configuration (including .gitleaks.toml, .gitleaksignore, gitleaks.toml, gitleaksignore, .secretlintignore and .trufflehog.yml), authorization/evidence/repository-hygiene validators and their tests, the canonical assurance standard or record template, and core governance/security/privacy/development-policy documents (including AGENTS.md, CODEOWNERS, CODE_OF_CONDUCT.md, LICENSE, GOVERNANCE.md, SECURITY.md, CHATGPT_ONBOARDING.md, START_HERE.md, INCIDENT_RESPONSE.md, docs/HANDOVER_TEMPLATE.md, docs/TEMPLATE_UPDATE_GUIDE.md, docs/EXACT_HEAD_AUTHORIZATION_SETUP.md, and the project risk standard). To keep this gate from deadlocking future policy maintenance, a separately allowlisted owner can use /authorize-policy-change followed by the exact 40-character head SHA. That route requires the change to be classified HIGH or CRITICAL and a dedicated Protected policy change review section in the evidence record with every protected path listed exactly once, the current base SHA, concrete reason, adversarial tests, rollback/recovery, independent review reference, and Owner decision: APPROVED. The normal /authorize-merge command remains blocked for those paths. This prevents a PR from changing the workflow or validator that is supposed to judge it, changing scanner exclusions, or adding PR workflows that impersonate required check contexts.
- Do not use pull_request_target or workflow_run to check out or execute untrusted PR code. Treat issue/PR content and downloaded artifacts as untrusted data.

**Status-source threat boundary:** GitHub's expected-source setting identifies an App, not a specific workflow. All GitHub Actions workflows share the Actions App identity, so an expected-source rule pointing at Actions cannot distinguish a trusted authorizer from a PR-controlled workflow. A separate App identity is required for a robust owner-authorization status. The repository's writer population and Actions token defaults should still be verified; fork PR tokens must remain read-only.

**Bootstrap limitation:** a newly introduced default-branch authorization workflow cannot authorize the PR that first adds it, because issue_comment runs only the workflow definition already present on the default branch. The initial policy/workflow change therefore requires a separate manual owner review and explicit approval. A local owner-run status publication is not part of this implementation. Do not claim that the bootstrap was technically gated. After the trusted workflow is on the default branch and the App/environment/ruleset are configured, the automated gate can protect subsequent eligible PRs.

### Bootstrap exception and staged enforcement

A bootstrap PR is a change that introduces the authorization workflow, trusted validator, independent status source, or ruleset requirement itself. The new gate cannot authorize that PR before its workflow is present on the default branch. Apply this bounded sequence:

1. **Pre-merge review:** complete the full exact-head diff review, independent review where warranted, five-perspective assessment, exact-head CI, documentation-to-implementation review, public privacy scan, and the PR-specific assurance record. Inspect the existing live ruleset and record which new controls are not yet active.
2. **Manual bootstrap approval:** obtain the owner's explicit approval for that exact PR head. The initial merge is a one-time manual bootstrap exception, not evidence that the new technical gate already worked. Do not invent or publish a success status from a not-yet-configured App.
3. **Post-merge configuration:** only after the trusted workflow is on the default branch may the owner configure/install the dedicated App, protect its key in the restricted environment, add the App as the expected status source, and enable strict up-to-date checks.
4. **Post-merge proof:** re-fetch the live ruleset and run adversarial acceptance tests on a separate test PR. Verify that missing evidence, stale SHAs, unauthorized actors, changed heads, policy-path changes, and failed checks are blocked. Only then may the system be described as technically enforced.
5. **No recurring bypass:** later policy/workflow changes use the normal protected-policy review route and live required checks. The bootstrap exception applies only to the initial installation of the gate.

The assurance record must distinguish the pre-merge bootstrap review from post-merge enforcement work. A known configuration gap may be accepted only as an explicit, time-bounded bootstrap limitation with an owner and post-merge acceptance plan; it must never be described as a passed technical control.

**Protected deployment environments:** environments can provide a native approval UI, but a successful deployment record alone does not prove exact PR-head owner authorization. Keep this as an alternative only if an end-to-end exact-SHA binding and reviewer gate are independently demonstrated; do not substitute a deployment record for the distinct status App without that proof.

If the repository cannot securely implement the exact-head gate, retain a manual explicit approval step and state that technical enforcement is incomplete.

## 8. PR-specific assurance record

Each pull request must include `reviews/PR-<number>.md`, copied from [the PR assurance record template](docs/PR_ASSURANCE_RECORD_TEMPLATE.md). It records:
- PR number, base branch/SHA, head SHA, risk level, scope, and non-goals;
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

For every substantive change, the primary reviewer must explicitly confirm that the complete exact-head diff was reviewed. For HIGH/CRITICAL changes, the independent review scope must also cover the complete diff and relevant surrounding implementation; a partial-file review does not satisfy the high-impact gate. The PR evidence validator enforces both statements.

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
- before a high-impact or hard-to-reverse merge, create and verify a recoverable snapshot of the exact pre-merge head and any user-owned work that could be affected; record the backup reference and a realistic rollback/recovery route; a Git commit alone is not assumed to be an independent backup;
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
- GitHub Docs, *Deployments and environments* (required reviewers, deployment branch policies, administrator bypass). https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- GitHub Docs, *Workflow syntax: GITHUB_TOKEN permissions and pull-request trust behavior*. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

## 13. Public/private boundary

This public standard contains only generic reusable process guidance. Keep project-specific memory, private decisions, personal preferences, internal incidents, operational details, credentials, and private coordination records in their appropriate private repositories. Public template content must remain generic, sanitized, and suitable for unrelated users.
