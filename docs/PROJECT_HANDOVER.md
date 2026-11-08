# Template Maintainer Handover

> Maintainer-facing continuity note for the Collaborative Development Template repository. This is not a downstream project handover and is not part of the starter pack. Keep it factual, current, minimal, and free of private conversations or personal data.

## Repository

- **Name:** Collaborative Development Template
- **Repository:** https://github.com/Anonymous2323projects/Collaborative-Development-Template
- **Default branch:** `main`
- **Purpose:** Maintain a ChatGPT-first, privacy-first framework for collaborative software development, using GitHub as the durable project record.
- **Core priorities:** Safety, legal solidity, usability, trust, freedom.
- **Core components:** Memory, roadmap, handover, research records, development workflow.

## Current baseline

- The reusable onboarding guide is `START_HERE.md`.
- The repository-specific instructions are in `AGENTS.md`.
- Downstream projects must maintain `docs/PROJECT_MEMORY.md`; this template repository is explicitly exempt to prevent recursive self-application.
- The README banner is stored at `assets/manifesto-banner.png` and referenced locally from `README.md`.
- Reusable project resources are maintained separately from this repository's own maintenance records.
- `PENDING_ACTIONS_TEMPLATE.md` is an optional register for meaningful human-dependent actions in downstream projects.
- ChatGPT Free compatibility is the baseline; Projects, Memory, GitHub connections, and automation are convenience features with plan-dependent limits.
- The public repository must not contain private conversations, personal data, credentials, or project-specific material from unrelated work.

## Recent verified repository milestones

- Proactive copilot-style execution and collaboration guidance was integrated through PR #11.
- The downstream persistent project-memory requirement and explicit template-repository exception were integrated through PR #12.
- Maintainer-record separation and onboarding/privacy-boundary corrections were integrated through PR #13 (merge commit `21a29a6fad66c6e3c82e2ab20eda78c864595864`).
- The README banner was switched to the repository-local asset in commit `fac8578787ea5d414bae98c81ad0f9309337525b`.

These entries describe repository changes only; they are not evidence of a complete security, privacy, or legal audit.

## Maintenance rules

1. Keep public onboarding focused on using the template, not on this repository's own history.
2. Keep maintainer QA records separate from reusable project templates and starter resources.
3. Generalize and sanitize any cross-project learning before proposing it for this public repository.
4. Do not copy raw chat transcripts, private files, personal data, or confidential third-party material.
5. Verify claims against the current default branch and current tool output; remove stale statuses promptly.
6. Use focused branches and pull requests. Do not merge to `main`, rewrite history, or perform destructive Git operations without explicit authorization.
7. Record only meaningful decisions, evidence, unresolved risks, and next actions. Avoid duplicating the detailed workflow or policies.

## Current maintenance focus

- Enable GitHub's repository-level **Template repository** setting before advertising the “Use this template” workflow. Current verified API state: `is_template: false`. A maintainer must open **Settings → General → Template repository** and enable **Template repository**; verify afterward that the repository API reports `is_template: true`. The available GitHub connection cannot change this repository setting.
- Complete review and merge decision for PR #14; it adds Free-plan-first ChatGPT continuity and the human-dependent action register.
- Keep README and onboarding links aligned with the actual starter-pack contents.
- Keep onboarding acceptance criteria generic and maintainable; record any future test results separately and only in sanitized form.
- Review the distinction between mandatory safeguards, recommended practices, and user-selectable workflow choices.
- Ensure automated checks are described according to what they actually test; do not treat hygiene or secret scanning as a complete content or security review.

## Handover checklist

Before a substantial maintainer handover, verify:

- [ ] Current branch and commit.
- [ ] Open pull requests and unresolved review comments.
- [ ] Changed files and rationale.
- [ ] Checks actually run and their results.
- [ ] Known limitations and unresolved risks.
- [ ] Next safe action and any approval required.
- [ ] Public content, metadata, assets, and history reviewed for accidental disclosure.

Do not store credentials, sensitive personal data, raw conversations, or confidential material in this file.
