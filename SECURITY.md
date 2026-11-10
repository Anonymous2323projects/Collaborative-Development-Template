# Security Policy

## Scope

This policy covers this public template repository and provides a baseline that adopting projects must tailor to their own architecture and threat model.

## Reporting a vulnerability

Do not publish exploit details, credentials, private data, or an unpatched vulnerability in a public issue or pull request. Use GitHub's private vulnerability reporting feature if it is enabled for this repository. If it is unavailable, contact the repository maintainer through a private channel without including secrets in the message.

Do not assume a report channel is configured until it has been checked in repository settings. See [Incident Response](INCIDENT_RESPONSE.md) for triage, containment, communication, and recovery guidance.

## Secure development baseline

- Inspect scripts, build tools, package lifecycle hooks, dependencies, CI workflows, and downloaded binaries before execution or adoption.
- Prefer official registries and upstream release channels; verify provenance, integrity hashes, signatures, and licences where available.
- Use supported dependency versions and committed lockfiles for applications. Review and update dependencies deliberately.
- Apply least privilege to local processes, CI jobs, tokens, deployment credentials, and third-party integrations.
- Never expose secrets in source, logs, artifacts, test output, screenshots, or issue reports.
- Keep untrusted pull-request code away from privileged secrets and deployment environments.
- Validate inputs and outputs at trust boundaries; use safe defaults and explicit permissions.
- Review network listeners, file-system access, subprocess execution, update mechanisms, and generated binaries.
- Add appropriate static analysis, dependency scanning, secret scanning, tests, and build verification for the adopted stack. This template runs CodeQL against its Python maintenance script and GitHub Actions workflows, plus unit tests for its repository-hygiene helpers. These checks cover only their configured languages and query scope; they do not scan every document for semantic errors or establish that the repository is vulnerability-free.
- Maintain a vulnerability response and update process appropriate to the project.
- Follow [the Update and Release Security Policy](UPDATE_AND_RELEASE_SECURITY.md): verify update provenance and signatures, communicate changes clearly, and obtain the user's informed approval before installing updates unless a clearly disclosed and justified deployment model requires otherwise.

## Automated checks in this template

The PR-specific assurance-record validator is invoked only when an authorized maintainer submits the exact-head `/authorize-merge` or `/authorize-policy-change` command. It is not an automatic check on every pull request. A separate issue-comment workflow can create an exact-head maintainer authorization status after checking the authorized actor, PR state, target branch, exact SHA, protected policy paths, evidence record, and unresolved review threads. These controls require the corresponding status context to be configured as required in the live repository ruleset; a workflow existing in the repository is not sufficient. The validator checks structure and identity, not the truth or quality of the review. Verify the live ruleset and workflow runs before relying on the gate.

The public repository uses GitHub CodeQL for Python and GitHub Actions workflow analysis, Gitleaks for secret-pattern scanning, repository-hygiene checks, and unit tests for the hygiene helper functions. The pull-request Gitleaks job scans the exact base-to-head commit range with a digest-pinned scanner image, checks that the range is non-empty and that the scanner confirms a non-zero commit count, traverses all parent paths, and includes first-parent diffs for merge commits. It uses a fixed trusted configuration that extends Gitleaks' built-in rules, an empty ignore directory, and the --ignore-gitleaks-allow option; it does not load PR-controlled .gitleaks.toml or .gitleaksignore files and does not honor PR-added gitleaks:allow comments. These scanner configuration and ignore files are protected policy paths. Gitleaks reports commits with additions; its reported count can therefore be lower than Git's commit-object count when a commit adds no content. A lower count is not by itself a skipped-commit failure, but a zero scan count always fails closed. Review each workflow's current triggers, permissions, pinned action revisions, image digests, and query scope before relying on it. A successful run means only that those configured checks completed without reporting a failure; it is not a full security review.

## Important limitations

No checklist, scanner, AI assistant, code review, or CI pipeline can guarantee that software is free of malicious code or vulnerabilities. Controls reduce risk; they do not eliminate it. A clean scan is not proof of safety.

## Adoption

Before using this policy in another project, define its assets, trust boundaries, threat actors, deployment model, supported versions, reporting contact, response expectations, and applicable legal obligations.
