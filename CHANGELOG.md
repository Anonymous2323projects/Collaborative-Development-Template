# Changelog

Notable user-facing changes to the template are recorded here. This is a curated summary, not a full commit history.

## Unreleased

- Tightened PR assurance evidence: high-impact merges require a verified pre-merge recovery snapshot, and bootstrap exceptions require explicit compensating controls, owner state, deadline, post-merge owner, and stop/rollback conditions.

- Added a project-wide change-assurance standard with risk-based research, system-level hazard analysis, five separate review perspectives, documentation-to-implementation traceability, systemic recurrence review, and an efficiency audit.
- Added a PR-specific fail-closed evidence validator and exact-head maintainer authorization workflow. The validator binds the assurance record to the reviewed code commit and requires a separate evidence-only final commit to avoid self-referential SHA claims.
- Updated contributor, governance, development, security, review, risk, and downstream-update guidance to require evidence-backed procedures and verified technical enforcement. The corresponding GitHub ruleset still requires configuration of the new check contexts before these gates are fully enforced.


- Added a clear review-before-work and verification-after-substantial-change cadence, with checks scaled to impact and evidence reused only while still valid.
- Streamlined onboarding, project records, README navigation, and the downstream update guide and reusable prompt; clarified when specialist templates are needed without weakening mandatory project memory or public-release risk assessment.
- Resolved conflicting commit-email instructions: contributors choose how their own identity appears, and the workflow checks the author details attached to saved changes against that choice.
- Consolidated Project Instructions setup into one complete project-specific block, including continuity; removed the competing short continuity block.
- Simplified development workflow guidance to avoid repeated administration and checks while preserving approval, privacy, security, and validation safeguards.

- Added a safe downstream template-update guide, reusable update prompt, and copyable exact-SHA version record. Clarified manual updates, preservation of project-specific work, and separate Project Instructions installation.
- Made beginner-friendly explanations and efficient, non-repetitive collaboration universal requirements. Reduced unnecessary repeated GitHub checks, setup walkthroughs, confirmations, and duplicate records while retaining meaningful safeguards.

- Added project-specific OpenAI Model Spec alignment, instruction-hierarchy and prompt-injection safeguards, plus updated shared-Project privacy wording.
- Added unit tests for repository hygiene helpers and CodeQL analysis for the Python maintenance script.
- Documented the reported Google AI Studio free-plan origin and limitations of the manifesto banner's rights/provenance evidence.

- Updated ChatGPT Free and Project-memory guidance against current OpenAI documentation, including conditional same-Project chat reference and the fresh-conversation rollover acceptance scenario.
- Added lightweight community governance and a project-specific Code of Conduct.
- Expanded repository hygiene checks to validate local Markdown heading fragments and GitHub Actions workflow safety conventions.
- Added Dependabot configuration for GitHub Actions and a GitHub release-notes category template.

## Release policy

A changelog entry does not mean a release has been published. Versioned releases are created only when the maintainer intentionally marks a stable, useful template milestone. See [Project Governance](GOVERNANCE.md) and [GitHub's release documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
