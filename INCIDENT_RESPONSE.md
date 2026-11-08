# Incident Response Playbook

> Adapt this playbook to the project's size, hosting, data, jurisdiction, and support model. It is an operational starting point, not legal advice. Do not put secrets or unnecessary personal data in incident records.

## 1. First response

1. **Protect people and systems.** If harm or active compromise may be occurring, prioritize containment.
2. **Pause affected activity.** Stop a release, deployment, workflow, integration, or publication when this can be done safely.
3. **Preserve evidence.** Record timestamps, affected versions, relevant logs, and actions taken. Restrict access and avoid copying sensitive payloads into tickets.
4. **Notify the responsible maintainer privately.** Use an established private channel.
5. **Assign roles.** Identify an incident lead and technical, communications, and privacy/legal support as appropriate. For a small project, one person may hold multiple roles.

Do not destroy logs, wipe systems, rewrite Git history, or make speculative public statements before considering evidence preservation and impact.

## 2. Accidental secret or credential exposure

- Revoke or disable the exposed credential immediately; rotate related credentials if compromise could extend beyond the visible value.
- Identify its permissions, systems, access window, and likely exposure. Review provider audit logs where available.
- Remove the secret from the current working tree and prevent further publication.
- Assess Git history, forks, caches, build artifacts, logs, package registries, and other copies. A new commit deleting the value does not invalidate it or erase historical copies.
- Coordinate history cleanup only after preserving necessary evidence; communicate that third-party copies may remain.
- Restore service using a newly issued credential stored in an approved secret manager.
- Record the cause and preventive action without reproducing the secret.

## 3. Suspicious dependency or malicious contribution

- Stop installation, execution, merge, release, or deployment of the suspect material.
- Identify affected versions, commits, build jobs, artifacts, and environments.
- Preserve package metadata, lockfiles, hashes, commit references, logs, and relevant artifacts.
- Revoke exposed tokens and isolate affected runners or systems if compromise is plausible.
- Verify provenance through trusted upstream channels; do not rely solely on claims from the suspect package or contributor.
- Remove or pin the affected dependency only after assessing compatibility and safe recovery.
- Review downstream releases and notify affected users when warranted.

## 4. Vulnerability report

- Do not ask a reporter to publish exploit details, personal data, or credentials in a public issue.
- Use GitHub private vulnerability reporting only after confirming that it is enabled in repository settings. Otherwise provide a private maintainer contact route.
- Acknowledge receipt privately when possible; clarify affected versions, prerequisites, impact, and safe reproduction details.
- Triage severity based on evidence, exploitability, impact, and exposure. Avoid unsupported severity claims.
- Develop and test a fix or mitigation, coordinate disclosure, and publish an advisory when appropriate.
- Credit reporters only with their permission. Do not disclose identifying information without authorization.

## 5. Unsafe release or active compromise

- Pause distribution and update mechanisms where safe; mark affected versions clearly.
- Determine whether the issue is in source, build infrastructure, signing keys, metadata, hosting, or the artifact itself.
- If signing keys or release infrastructure may be compromised, stop trusting new artifacts from that channel until trust is re-established.
- Publish a concise warning through trusted channels with affected versions, known impact, and safe mitigation steps.
- Prefer disabling the affected feature or withdrawing the artifact over pushing an unverified replacement.
- Prepare a verified replacement, integrity/provenance evidence, recovery guidance, and rollback plan.
- Preserve user data; do not use an incident as justification for unrelated destructive changes.

## 6. Privacy and legal assessment

Where personal data, confidential information, consumer impact, or regulated activity may be involved:
- establish what data and people are affected, what was exposed, when, and to whom;
- contain further access and preserve evidence;
- assess contractual, regulatory, and statutory duties with qualified support where needed;
- determine whether affected people, customers, regulators, partners, or platforms must be notified and within what timeframe;
- document the basis for decisions and avoid making unsupported assurances.

Do not assume every incident is legally notifiable or that none is. The facts and applicable jurisdiction determine the obligations.

## 7. Communications

Communications should state:
- what is known and what remains under investigation;
- affected products, versions, data, or users where established;
- actions users should take, with safe and verifiable instructions;
- what the project team is doing and when the next update is expected;
- where to report additional information privately.

Do not speculate, blame individuals prematurely, disclose exploit details unnecessarily, or promise that all copies or impacts have been eliminated.

## 8. Recovery and follow-up

- Restore from trusted sources and verify integrity before reconnecting systems.
- Rotate credentials and rebuild compromised environments where warranted.
- Validate fixes, monitoring, backup, recovery, and release controls.
- Record root causes, contributing factors, timeline, impact, decisions, and residual uncertainty.
- Create prioritized corrective actions with an owner role and due date.
- Review the playbook and risk register; share sanitized lessons without exposing people or sensitive details.

## Incident record (sanitized)

- **Incident ID:** <ID>
- **Detected:** <DATE / TIME / TIME ZONE>
- **Incident lead role:** <ROLE>
- **Category:** Secret exposure / Dependency / Vulnerability / Release / Privacy / Other
- **Affected scope:** <SYSTEMS / VERSIONS>
- **Known impact:** <FACTS ONLY>
- **Containment actions:** <ACTIONS AND TIMES>
- **Notifications / assessments:** <WHAT WAS ASSESSED, NOT PRIVATE DETAILS>
- **Recovery and validation:** <EVIDENCE>
- **Root cause and follow-up:** <ACTIONS>
- **Open questions:** <UNCERTAINTY>
