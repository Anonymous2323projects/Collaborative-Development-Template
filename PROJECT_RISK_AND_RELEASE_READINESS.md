# Project Risk and Release Readiness Standard

## Purpose

This standard helps a project identify and manage avoidable legal, privacy, licensing, security, safety, and operational risks before public release. It applies to this template repository and to every project that adopts it.

It is a decision and evidence framework, not a guarantee of safety or legal compliance and not a substitute for qualified professional advice. No checklist, audit, scan, or review can eliminate all risk.

## Priority order for decisions

Apply the template's five priorities in this order: **1. Safety, 2. Legal solidity, 3. Usability, 4. Trust, 5. Freedom.** Safety and applicable legal obligations are constraints, not optional trade-offs for convenience. Within those constraints, make the process easy to understand and use. Build trust through accurate disclosures, documented evidence, and reliable behavior; never through unsupported assurances. Preserve user autonomy, choice, ownership, portability, and control wherever possible. Prefer open standards and interoperability, avoid unnecessary lock-in and data collection, and use the least restrictive effective safeguards. Freedom does not require enabling unsafe or unlawful conduct. Scale the depth of controls to the project's actual risk.

## Core release principle

Do not publish or distribute a release while a known, material risk remains unassessed or while a critical issue remains unresolved. A release may proceed with lower-level residual risks only when:
- the risk, impact, likelihood, and affected users are documented;
- reasonable mitigations have been applied;
- the remaining risk is explicitly accepted by an authorized project owner;
- any required user disclosure, consent, support, or mitigation is in place; and
- the decision is revisited when facts or the product change.

Do not describe a project as "100% safe", "fully secure", or "legally compliant" based only on completion of this checklist.

## Change impact and reversibility

The more difficult a change is to undo, the more carefully it must be researched before it is made. This applies to code and documentation as well as data, publication, account settings, access permissions, migrations, releases, and integrations.

Before a high-impact or hard-to-reverse change:

1. Verify the current state and identify everything that could be affected.
2. Research current official documentation, relevant standards and law, and other credible sources where useful. Compare reasonable alternatives.
3. Assess likely benefits, failure scenarios, privacy/security/legal effects, compatibility, cost, and impact on users and contributors.
4. Make and verify a backup or export where possible. Prepare and test a recovery or rollback route; do not assume that a Git commit or a backup exists unless verified.
5. Prefer a small, reversible trial (branch, draft, dry run, copy, or test environment) before a wider change.
6. Record evidence, assumptions, unresolved questions, the selected approach, and validation results.
7. Obtain explicit approval from the appropriate owner before irreversible deletion, history rewriting, public release, visibility/ownership/access changes, or other material external effects.

If recovery is not practical, do not proceed silently. Explain the consequences and alternatives and wait for the required decision. Routine, low-risk, reversible work should remain efficient and should not require repeated approval. Technical research and execution are the AI collaborator's responsibility where tools and authorization permit.

## Risk areas to assess

Tailor the depth of review to the project's features, audience, jurisdiction, architecture, distribution model, and risk profile.

### 1. Legal and regulatory

- Identify the responsible publisher/operator and the jurisdictions and user groups involved.
- Determine which laws and product obligations may apply, including consumer, contract, privacy, cybersecurity, accessibility, tax, advertising, and product-safety rules where relevant.
- Review terms, notices, warranties, disclaimers, refund/cancellation flows, support commitments, and update commitments for accuracy and enforceability.
- Do not use blanket disclaimers to suggest mandatory statutory rights or liability can simply be excluded.
- Obtain qualified legal advice for material uncertainty, regulated activities, consumer-facing commercial releases, or high-impact obligations.
- Record open questions; do not invent publisher identity, business model, data practices, or legal conclusions.

### 2. Privacy and data protection

- Map what personal data is collected, generated, stored, shared, and deleted, including telemetry, crash reports, analytics, support, accounts, payments, and update checks.
- Establish purpose, lawful basis where required, minimization, retention, access controls, security, user rights, and processor/vendor responsibilities.
- Review cookies, local storage, device identifiers, analytics, and cross-border transfers where applicable.
- Make notices and consent mechanisms match actual product behavior. Do not claim "no data collected" without verifying all network and local data flows.
- For projects using GitHub and ChatGPT Projects, assess repository visibility, collaborator/app access, Project sharing, project memory behavior, and account data controls separately. Do not treat one privacy setting as a substitute for the others.
- Ensure user-facing disclaimers explain realistic risks and user-controlled settings without suggesting that users waive mandatory rights or that the maintainer has excluded every possible responsibility.
- Avoid collecting data that the product does not need.

### 3. Intellectual property and open-source licensing

- Inventory first-party and third-party code, libraries, assets, fonts, icons, samples, datasets, models, firmware, and documentation.
- Record exact versions, sources, licences, notices, attribution, modification status, and applicable obligations.
- Check compatibility between licences and the intended distribution and commercial model.
- Verify rights to distribute every included asset. Public availability is not permission to reuse.
- Resolve unknown, incompatible, or restricted rights before release; seek specialist advice when needed.

### 4. Software and supply-chain security

- Review architecture, trust boundaries, permissions, network access, file access, subprocesses, plugins, scripts, installers, build tooling, dependencies, and CI/CD.
- Use proportionate threat modelling, secure defaults, least privilege, dependency and secret scanning, static analysis, tests, and artifact verification.
- Inspect automated workflows and third-party actions; pin and restrict them appropriately.
- Protect credentials and signing keys; verify release provenance and signatures.
- Review the updater under [Update and Release Security Policy](UPDATE_AND_RELEASE_SECURITY.md).
- Document what was actually tested and what remains unverified. A clean scan is not proof of safety.

### 5. Product, operations, and user impact

- Check installation, upgrades, uninstall, backup, restore, rollback, failure states, accessibility, compatibility, and support paths.
- Identify foreseeable misuse, data loss, security abuse, and failure modes.
- Provide clear release notes, known issues, support/reporting channels, and incident response.
- Confirm that user-facing claims match tested behavior.

## Risk register

Maintain a project-specific risk register. For each material risk record:
- unique ID and date;
- description, affected assets/users, and plausible scenario;
- likelihood and impact, with rationale;
- severity and priority;
- existing controls and evidence;
- mitigation, owner/role, and target date;
- residual risk and explicit acceptance decision;
- status and review date.

Use role names rather than personal information in public examples. Keep confidential vulnerability details and personal data out of public issue trackers.

## Release gates

A release owner should confirm the following gates before public release. Adapt or omit items only with a recorded reason.

- [ ] Project scope, intended users, distribution model, and supported platforms are documented.
- [ ] Applicable legal and regulatory questions have been assessed; material uncertainties have qualified review or a documented release block.
- [ ] Privacy/data-flow inventory and user-facing notices match actual behavior.
- [ ] Third-party code and asset inventory, licences, notices, and attribution have been checked.
- [ ] Threat model and security review are proportionate to the product's exposure and impact.
- [ ] Critical and high-severity security issues are fixed or the release is blocked; any exception is explicitly justified by an authorized owner and does not expose users to an unacceptable risk.
- [ ] Tests, builds, dependency checks, secret scans, and release-artifact checks have been run where applicable; results and omissions are recorded.
- [ ] Update, signing, recovery, and incident-response procedures are documented and tested where applicable.
- [ ] User documentation, limitations, support/reporting route, release notes, and required disclosures are ready.
- [ ] Public files, metadata, screenshots, logs, commit messages, and release artifacts have been reviewed for secrets, personal data, confidential information, and unintended files.
- [ ] Residual risks are documented and accepted by the appropriate project owner.
- [ ] A named release decision (go / no-go), date, scope, evidence, and approver role are recorded.

## Stop-release conditions

Stop publication or distribution and escalate when:
- a credible critical vulnerability or active compromise is unresolved;
- release artifacts cannot be authenticated or their provenance is uncertain;
- secrets, personal data, or confidential information may be exposed;
- distribution rights or licence obligations are materially unclear;
- a material legal or safety obligation has not been assessed;
- test evidence is missing for a safety- or security-critical change; or
- user data could be irreversibly lost without adequate warning or recovery.

Containment, disabling an affected feature, withdrawing a release, or publishing a corrected release may be safer than proceeding. Preserve evidence and follow the incident-response plan.

## Ongoing obligations

Release approval is not a one-time finish line. Reassess risks when adding features, changing data flows, adding dependencies, changing monetization or distribution, entering new jurisdictions, changing update behavior, or responding to a vulnerability or incident. Maintain supported versions, vulnerability intake, security updates, privacy notices, licence records, and user support as appropriate.

## Evidence and honesty

For every review, record:
- reviewer role and date;
- scope and versions examined;
- sources, tools, commands, and tests used;
- results, limitations, and items not checked;
- findings, remediation, and residual risks.

Never claim an audit, legal review, scan, setting, or test occurred unless there is evidence it did. This standard is a reusable baseline and must be tailored to each project.
