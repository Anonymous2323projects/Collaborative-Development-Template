# Repository Instructions

These instructions apply to every contributor and AI coding assistant working in this repository.

## Non-negotiable rules

1. **Public-repository privacy:** Treat every change as permanently public. Never add personal data, private communications, credentials, confidential information, or identifying details about repository owners, friends, contributors, or third parties.
2. **No automatic context transfer:** Never copy content from private chats, private repositories, local files, screenshots, logs, or other projects into this template. First establish that an insight is genuinely reusable, then rewrite it as a neutral, fictional, project-agnostic pattern.
3. **Security before execution:** Do not blindly run commands, scripts, installers, build steps, package lifecycle scripts, or downloaded tools. Inspect their source and effects first. Ask before any action with unclear scope, elevated privileges, destructive effects, external data transfer, or changes to the user's machine.
4. **No secrets:** Never request, print, commit, or expose tokens, passwords, private keys, signing keys, recovery codes, or secret environment values. Use placeholders and secret stores.
5. **No unreviewed dependencies or automation:** Inspect dependency provenance, maintenance, licences, install scripts, transitive dependencies, and permissions. Pin CI actions to full commit SHAs where practical; grant least privilege.
6. **No destructive Git operations:** Never force-push, rewrite shared history, delete branches, discard user work, or merge to a protected/default branch without explicit authorization.
7. **Evidence-based claims:** Do not claim a control is enabled, a test passed, a vulnerability is absent, or a project is compliant unless verified.
8. **Project-specific review:** This is a template, not a universal prescription. Check applicability, threat model, stack, jurisdiction, distribution model, and user needs before adopting controls.
9. **Release-readiness gate:** Before a project is publicly released, use `PROJECT_RISK_AND_RELEASE_READINESS.md` to assess legal/regulatory, privacy, licensing/IP, security/supply-chain, and operational risks. Do not claim compliance or complete safety. Block release for unresolved critical risks or material unassessed obligations; document evidence, residual risks, and explicit go/no-go approval.

## AI onboarding behavior

When a user shares this repository as the starting point for a project, read `START_HERE.md` and follow its conversation flow. The first visible response must be exactly **"What are you dreaming of?"** Do not prepend a greeting or explanation. If repository access is unavailable, do not pretend to have read the guide; ask the user to paste it while preserving the intended first-question experience when possible.

## Required workflow

- Inspect repository status, branch, relevant files, and existing conventions before editing.
- Clarify consequential ambiguity; otherwise make the smallest reversible change.
- Work on a descriptive feature branch and keep changes focused.
- Explain the intended change and security/privacy implications before risky operations.
- Review the complete diff for correctness, secrets, personal data, unsafe commands, licence issues, and accidental project-specific content.
- Run relevant tests and checks; report exactly what was and was not run.
- Update documentation and handover notes when durable decisions or workflows change.
- Open a pull request for review. Do not merge to the default branch without explicit approval.

## Public-data review

Before every commit and release, inspect:
- file contents, filenames, paths, examples, comments, and metadata;
- screenshots, images, archives, logs, test fixtures, and generated files;
- URLs, usernames, email-like strings, tokens, keys, and environment values;
- commit messages and release notes.

Use fictional placeholders such as `<OWNER>`, `<PROJECT>`, `developer-a`, and `user@example.invalid`. Never use a real person's details as an example.

## When in doubt

Stop before publishing or executing. Describe the uncertainty, possible impact, and a safe next step. Never silently weaken these rules.
