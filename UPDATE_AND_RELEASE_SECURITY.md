# Update and Release Security Policy

## Purpose

Updates are a security-sensitive change to a user's software, not merely a convenience feature. A release can fix vulnerabilities, but it can also introduce regressions, unwanted behavior, compromised dependencies, or malicious code. Projects adopting this template must define and document an update policy before shipping an update mechanism. Apply [Change, Review, and Merge Assurance](MERGE_AND_CHANGE_ASSURANCE.md) to meaningful updater, signing, deployment, and release changes. Verify that the controls described here exist in code, CI, repository settings, and the release environment; documentation alone is not enforcement. If an update/release control fails or a near miss occurs, perform a systemic recurrence review of related procedures and technical controls.

## User-consent principles

For software where users control the installed version:

- **Notify separately from installing.** Checking for or displaying an update must not silently install it.
- **Require informed approval.** Explain what is being updated, the version, the release date, the important changes, compatibility requirements, and any material risks before installation.
- **Make the choice clear.** Offer actions such as Install, Remind me later, and View release notes. Do not use deceptive wording, preselected consent, or pressure tactics.
- **Respect deferral.** A user may postpone a normal update. Explain any loss of support or exposure to known vulnerabilities when relevant.
- **No silent replacement.** Do not replace application binaries, execute downloaded installers, migrate user data, or change security-sensitive settings without the consent required by the product's clearly disclosed update policy.
- **Be transparent about mandatory updates.** If a version must be blocked for a substantiated security, safety, legal, or service-compatibility reason, explain why, what data or functionality is affected, and what options remain. Do not label ordinary feature releases as mandatory security updates.
- **Keep user data safe.** Back up or make migrations recoverable where practical. Explain irreversible migrations before approval.

A project may offer an optional automatic-update setting, but it must be explicit, off by default unless the product's clearly disclosed installation model and applicable law justify otherwise, and easy to change. The user must be able to distinguish update notifications, automatic download, and automatic installation.

## Verify updates before applying them

An approval prompt is not a substitute for technical verification. Before installation:

1. Obtain update metadata and artifacts only from the project's trusted release infrastructure over authenticated transport.
2. Verify cryptographic signatures and artifact integrity against trusted keys or roots established independently of the downloaded artifact. A checksum downloaded from the same untrusted location is not sufficient by itself.
3. Prefer established secure update frameworks and documented signing/provenance practices (for example, The Update Framework / TUF) over custom cryptographic protocols.
4. Validate product identity, version, target platform, release channel, expiry/freshness metadata where supported, and compatibility before applying an update.
5. Reject unsigned, incorrectly signed, tampered, unexpected, or downgrade/replay artifacts. Define a safe key-rotation and signing-key compromise procedure.
6. Protect signing keys using restricted access, secure storage, separation of duties where proportionate, and auditable release procedures. Never commit private signing keys or tokens.
7. Build and publish from reviewed source and controlled CI. Pin CI actions and dependencies appropriately, restrict workflow permissions, and do not expose secrets to untrusted pull requests.
8. Publish release notes and, where proportionate, provenance attestations and a software bill of materials (SBOM).

Do not execute downloaded code merely to inspect it. Review the updater itself as security-critical code, including its network, filesystem, process, privilege, and rollback behavior.

## Safe installation and recovery

- Verify all artifacts before making changes.
- Use atomic installation or another recoverable strategy where practical.
- Preserve user projects, settings, and data; separate application updates from user-content migrations.
- Provide a tested recovery or rollback path where technically feasible. Do not roll back into a version with a known actively exploited vulnerability without a clear warning and informed decision.
- Prevent unauthorized downgrades and replay of old vulnerable releases.
- Run compatibility checks and appropriate tests before declaring an update successful.
- If installation fails, leave the application in a known safe state and explain how to recover.
- Never delete user data as an automatic cleanup step without clear disclosure and consent.

## Release communication

Every release should have, at minimum:

- A unique version and release date.
- Human-readable release notes describing user-visible changes.
- Security advisories for security fixes, without publishing exploit details prematurely.
- Compatibility and migration notes.
- Known issues and any required user action.
- A clear indication whether the release is optional, recommended, or genuinely mandatory, with the reason.

Security fixes should be prioritized and communicated responsibly. Avoid exposing sensitive vulnerability details before users have a reasonable opportunity to update.


## Security severity and emergency response

Classify security releases based on the actual exploitability, impact, exposure, and availability of mitigations. Do not classify a release as mandatory merely to accelerate ordinary feature adoption.

| Level | Typical situation | Expected response |
|---|---|---|
| Normal | Features, improvements, routine fixes | User chooses when to install. |
| Security | Meaningful vulnerability without evidence of active exploitation or immediate severe impact | Clearly recommend the patch and explain the risk; allow reasonable deferral. |
| Critical | Severe exploitable vulnerability, such as a remotely exploitable code-execution flaw, especially where exposure is broad or mitigation is limited | Issue an expedited security release, prominently warn users, set a short and justified deferral window where appropriate, and explain support consequences. |
| Emergency | Credible active exploitation, compromise of a release/signing channel, or an imminent severe risk that cannot reasonably be mitigated otherwise | Take proportionate containment action immediately; this may include disabling the affected feature, blocking a vulnerable version or requiring an emergency update where technically and legally justified. |

These are response categories, not automatic severity labels. A qualified maintainer should document the evidence, affected versions, exploitability, impact, mitigations, and reason for the chosen response. Reassess the decision as facts change.

### Proportionate lockdown

Prefer the narrowest effective protective action:

1. Disable or restrict only the vulnerable feature, endpoint, plugin, or integration where that safely contains the risk.
2. If feature-level containment is insufficient, prevent the vulnerable version from accessing affected services or performing the dangerous operation, with a clear explanation and recovery path.
3. Require an emergency update only when the risk justifies it and a verified, trustworthy update is available. If no trustworthy patch is available, do not install an unverified replacement; isolate or disable the affected functionality and communicate the mitigation.
4. Preserve user-created projects and data. Do not use a security incident as a reason to erase user content or perform unrelated migrations.
5. Provide an appeal/support path or documented manual recovery where feasible, and record the incident and decision.

A forced update must never mean silently executing arbitrary code from a server. The update artifact and metadata must pass the signature, integrity, product, platform, and anti-rollback checks in this policy before installation. Where installation consent is overridden for a genuine emergency, the product must disclose that possibility in advance, explain the specific incident and action, minimize the scope, and comply with applicable law and platform rules.

## Different deployment models

This policy must be adapted to the delivery model:

- **Desktop/mobile applications:** users should normally approve installation; optional auto-update must be explicit and transparent.
- **Self-hosted software:** administrators control deployment timing, but should receive clear release and security notices and supported upgrade instructions.
- **Web services hosted by the project:** operators may deploy server-side changes centrally, so per-user install approval may not be technically meaningful. Disclose the deployment model, communicate material changes, protect availability, and provide rollback/mitigation where feasible.
- **Libraries and developer tools:** consumers or maintainers choose when to upgrade; publish versioning, breaking-change, dependency, and security information.

## Minimum project decisions before implementation

Record these in the project's decision log or security documentation:

- Who signs releases and how signing keys are protected and rotated.
- Where update metadata and artifacts are hosted.
- How signatures, provenance, integrity, freshness, and downgrade protection are verified.
- Whether update checks are manual or periodic, and what network data is sent.
- Whether download and installation are separate actions.
- Whether automatic updates exist, their default, and how users disable them.
- How users defer updates and how unsupported/vulnerable versions are handled.
- How migrations, backups, rollback, and failed updates are handled.
- How security advisories and vulnerability reports are communicated.
- Which platforms and versions remain supported.

## Release checklist

Before publishing an update:

- [ ] Changes have been reviewed and tested.
- [ ] Dependencies, build scripts, CI workflows, and release artifacts have been reviewed.
- [ ] Release artifacts and metadata are signed and independently verifiable.
- [ ] Version, platform, channel, and compatibility metadata are correct.
- [ ] Release notes and security advisories are prepared.
- [ ] Update prompts clearly describe the change and preserve user choice.
- [ ] No installation, data migration, or privileged action occurs before the required approval.
- [ ] Backup/recovery and rollback behavior has been tested where applicable.
- [ ] No secrets, personal data, private metadata, or unintended files are included in release artifacts.
- [ ] The update mechanism itself has been tested against tampered, invalid, expired, replayed, and incompatible update metadata/artifacts.

## Limitations

No signature, scanner, review, CI pipeline, or update policy guarantees that a release is harmless or vulnerability-free. Signatures establish that an artifact was signed by a trusted key and was not altered after signing; they do not prove that the signed code is benign. Users must retain clear information and meaningful control, and projects must maintain an incident-response process for compromised releases and signing keys.

This document is a reusable engineering baseline, not legal advice. Adapt it to the product, deployment model, supported platforms, threat model, and applicable consumer, privacy, cybersecurity, and accessibility requirements.
