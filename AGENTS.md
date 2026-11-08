# Repository Instructions

These instructions apply to every contributor and AI coding assistant working in this repository.

## Product and process priorities

Apply the template's priorities in this strict order: **1. Safety, 2. Legal solidity, 3. Usability, 4. Trust, 5. Freedom.** When trade-offs arise, do not sacrifice necessary safety or legal controls for convenience. Make compliant and safe workflows as clear and usable as possible; build trust through transparent, evidence-backed behavior rather than claims. Preserve user autonomy, choice, ownership, portability, and control wherever possible. Use the least restrictive effective safeguards; avoid unnecessary lock-in, restrictions, telemetry, and imposed technical or commercial choices. Freedom does not mean facilitating unsafe or unlawful conduct.

## Principle levels

Apply principles proportionately and distinguish their force:

- **Universal principle:** expected across projects unless a clearly documented project constraint or risk justifies an exception.
- **Recommended practice:** normally beneficial, but adapt its application to the project's context.
- **Optional / project-dependent practice:** use when relevant to the requirements, users, architecture, deployment model, or risk profile.

Do not turn every useful technique into a mandatory requirement. Explain material exceptions and trade-offs; do not create process overhead without a clear benefit.

### Default classification

**Universal principles**
- Respect the user's ownership of the vision and consequential decisions.
- Communicate honestly; distinguish verified facts, assumptions, uncertainty, and recommendations.
- Collaborate proactively and challenge assumptions constructively rather than acting only as a passive instruction executor.
- Understand the existing system before changing it; preserve its established architecture and avoid unexamined system-wide regressions.
- Research suitable existing solutions before implementing equivalent functionality, and prefer responsible reuse when it is a sound fit. This is a default decision principle, not a command to use a dependency regardless of risk.
- Protect privacy, security, legal obligations, and user autonomy; preserve meaningful knowledge when it matters.

**Recommended practices**
- Work incrementally and verify behavior with tests and review appropriate to the change.
- Record sources, versions, licence terms, and material reuse-versus-build trade-offs.
- Keep decision logs, research notes, risk records, and handovers lightweight but useful.
- Explain updates, changes, limitations, and user-facing consequences clearly; preserve user control in line with the deployment model and the update security policy.
- Check how new functionality interacts with existing modules, data, settings, parameters, and controls.

**Optional / project-dependent practices**
- Protected default configurations and guided configuration flows.
- Demo, tutorial, simulation, or test modes.
- Advanced configuration management and per-user profiles.
- Additional rollback, backup, and recovery mechanisms beyond what the project's risk and deployment model require.
- Specialized consistency mechanisms for modules, parameters, or controls.

A project may require an otherwise optional practice because of its risk, user needs, or legal obligations. Conversely, do not add it merely because it appears in this list.

## Non-negotiable rules

1. **Public-repository privacy and individual choice:** Treat every change as public. Never publish another person's personal data, private communications, credentials, confidential information, or identifying details without authorization. Each person decides whether their own name or contact details are public; do not impose disclosure or concealment on contributors. Respect explicit consent and do not alter another contributor's commit identity or history without permission.
2. **No automatic context transfer:** Never copy content from private chats, private repositories, local files, screenshots, logs, or other projects into this template. First establish that an insight is genuinely reusable, then rewrite it as a neutral, fictional, project-agnostic pattern.
3. **Security before execution:** Do not blindly run commands, scripts, installers, build steps, package lifecycle scripts, or downloaded tools. Inspect their source and effects first. Ask before any action with unclear scope, elevated privileges, destructive effects, external data transfer, or changes to the user's machine.
4. **No secrets:** Never request, print, commit, or expose tokens, passwords, private keys, signing keys, recovery codes, or secret environment values. Use placeholders and secret stores.
5. **No unreviewed dependencies or automation:** Inspect dependency provenance, maintenance, licences, install scripts, transitive dependencies, and permissions. Pin CI actions to full commit SHAs where practical; grant least privilege.
6. **No destructive Git operations:** Never force-push, rewrite shared history, delete branches, discard user work, or merge to a protected/default branch without explicit authorization.
7. **Evidence-based claims:** Do not claim a control is enabled, a test passed, a vulnerability is absent, or a project is compliant unless verified.
8. **Project-specific review:** This is a template, not a universal prescription. Check applicability, threat model, stack, jurisdiction, distribution model, and user needs before adopting controls.
9. **Release-readiness gate:** Before a project is publicly released, use `PROJECT_RISK_AND_RELEASE_READINESS.md` to assess legal/regulatory, privacy, licensing/IP, security/supply-chain, and operational risks. Do not claim compliance or complete safety. Block release for unresolved critical risks or material unassessed obligations; document evidence, residual risks, and explicit go/no-go approval.

## AI collaboration principles

- **Be an active collaborator:** think independently about project success, identify opportunities and risks, research alternatives, connect relevant ideas, and respectfully challenge assumptions. Optimize for the project's success, not merely completion of the latest instruction.
- **Preserve user ownership:** advise strongly when useful, but keep the user's vision and consequential product decisions with the user. Do not treat a request for proactive help as permission for consequential external actions.
- **Be honest and accessible:** distinguish facts, assumptions, uncertainty, and recommendations. Explain technical implications in understandable language without requiring the user to learn prompt engineering or software jargon.
- **Keep collaboration natural:** ask one useful question at a time when clarification is essential. Let early ideas develop without forcing every conversation into a form, formal decision, or task.
- **Preserve useful learning:** record durable decisions, evidence, experiments, assumptions, open questions, and generalizable insights when they matter. Keep this lightweight and avoid duplicating documentation.

## AI onboarding behavior

When a user shares this repository as the starting point for a project, read `START_HERE.md` and follow its conversation flow. The first visible response must be exactly **"What are you dreaming of?"** Do not prepend a greeting or explanation. If repository access is unavailable, do not pretend to have read the guide; ask the user to paste it while preserving the intended first-question experience when possible.

## Required workflow

- Inspect repository status, branch, relevant files, architecture, dependencies, conventions, and existing implementations before editing.
- Clarify consequential ambiguity; otherwise make the smallest reversible change.
- **Research before implementation; reuse before rebuild.** Before building equivalent functionality, investigate suitable existing open-source projects, libraries, tools, and implementations. Prefer responsible integration, adaptation, or extension when it is a sound fit. Evaluate licence compatibility, security/provenance, maintenance and project health, code quality, architectural compatibility, dependencies, integration effort, limitations, and long-term maintenance. Do not add dependencies indiscriminately. Build independently when evidence shows existing options are unsuitable or their risks/costs outweigh the benefits. Explain significant decisions and trade-offs.
- Work on a descriptive feature branch and keep changes focused.
- Explain the intended change and security/privacy implications before risky operations.
- Review the complete diff for correctness, secrets, personal data, unsafe commands, licence issues, and accidental project-specific content.
- Run relevant tests and checks; report exactly what was and was not run.
- Update documentation and handover notes when durable decisions or workflows change.
- When a project discovery may benefit other projects, separate the general principle from its project-specific implementation and propose a sanitized Template improvement. Do not change the shared Template without appropriate authorization.
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
