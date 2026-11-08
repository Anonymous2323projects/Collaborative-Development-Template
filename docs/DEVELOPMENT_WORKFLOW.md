# Collaborative Development Workflow

This workflow is a starting point. Adapt it to the project's risk, team size, stack, and release model.

## 1. Understand before changing

- Read the README, contributor instructions, architecture notes, and current handover.
- Inspect the working tree, active branch, recent commits, relevant implementation, dependencies, and established conventions.
- Identify the user-visible goal, constraints, acceptance criteria, and non-goals.
- Understand how existing modules, interfaces, data, settings, parameters, and controls relate to one another; do not treat meaningful values as arbitrary numbers or names.
- Separate verified facts from assumptions and open questions.

## 2. Research before implementation: reuse before rebuild

Before building equivalent functionality, investigate existing open-source projects, libraries, tools, and implementations. The AI should proactively discover plausible options; the user should not need to know what to search for.

For each serious candidate, assess proportionately:
- licence, attribution, and compatibility with the project's intended use and distribution;
- provenance, security posture, known vulnerabilities, trustworthiness, and permissions;
- maintenance activity, release history, project health, and support expectations;
- code quality, reliability, documentation, and relevant test evidence;
- compatibility with the existing architecture and the meaning of the data or controls it will operate on;
- direct and transitive dependencies, integration effort, limitations, operational impact, and long-term maintenance cost.

Prefer integrating, adapting, or extending an established solution when it meets the requirement without creating disproportionate risk or complexity. Do not add dependencies indiscriminately. Build from scratch when research shows that available options are unsuitable, cannot reasonably be integrated, or introduce unacceptable legal, security, architectural, maintenance, or cost risks.

Record the important sources, versions, licence terms, what was verified, and the reasoning behind significant reuse-versus-build decisions. Distinguish evidence from inference and state material unknowns. For a small or obvious change, keep this research lightweight and proportionate.

- Prefer primary documentation, source code, specifications, and maintained upstream repositories.
- Record source URLs, versions, dates, licence terms, and what was actually verified.
- Distinguish inspiration from direct reuse; preserve required notices and licence obligations.
- Propose a small implementation plan with risks and validation steps.

## 3. Project bootstrap gate: private GitHub setup before the first build

When the project brief, initial scope, technical direction, and first milestone are clear enough to begin implementation, pause before coding. Follow [the Private GitHub Project Setup Guide](PRIVATE_GITHUB_SETUP.md).

- Check whether the user has a GitHub account and whether an appropriate project repository already exists.
- For a new project repository, default to **Private**. Public visibility requires the user's explicit, informed choice.
- Guide the user through GitHub's **Keep my email addresses private** setting and, where available, **Block command line pushes that expose my email**.
- Help the user configure the exact GitHub-provided `noreply` address for command-line commits; never guess the address or ask the user to paste it into chat.
- Verify repository visibility and privacy setup before the first commit or push. Do not claim settings are enabled unless verified.
- Ask before account connections, permissions, collaborator invitations, repository creation through a connected tool, or other external changes.
- If the assistant cannot create a repository, guide the user through GitHub's interface one step at a time.

This is a deliberate transition gate, not a demand to create a repository during early brainstorming. Keep the user's project private while it is being developed unless the user explicitly chooses otherwise.

## 4. Implement safely

- Work on a focused branch.
- Keep changes small and reviewable.
- Preserve existing architecture and conventions; avoid parallel systems where an existing one can be extended appropriately.
- Evaluate system-wide effects across modules, interfaces, workflows, dependencies, data, and existing behavior.
- Avoid unrelated refactors and hidden behavior changes.
- Inspect commands and scripts before running them.
- Do not install software, grant permissions, or change machine configuration without authorization.
- Never put secrets in code, tests, logs, or examples.

## 5. Validate

- Run formatting, linting, type checks, unit/integration tests, and builds where applicable.
- Add regression tests for bug fixes.
- Review dependency and licence changes.
- Inspect the complete diff for accidental changes, personal data, secrets, unsafe behavior, and unsupported claims.
- Report exact commands and outcomes. Never imply that an unrun check passed.

## 6. Review and integrate

- Open a pull request with a concise summary, rationale, risks, and test evidence.
- Review behavior, security, privacy, accessibility, maintainability, and documentation.
- Resolve review comments explicitly.
- Merge only with the required approval.

## 7. Persistent project memory

**Scope exception:** This requirement is for projects that use the template. It does not apply to the Collaborative Development Template repository itself; do not create a `PROJECT_MEMORY.md` in the template repository. Its own continuity is maintained through the existing handover, research log, and development documentation.

Every project repository must maintain docs/PROJECT_MEMORY.md, initialized from the shared PROJECT_MEMORY_TEMPLATE.md during project setup. For an existing project with an equivalent canonical knowledge file, retain that file and document its location rather than creating a duplicate.

- Read the memory at the start of each work session; cross-check critical facts against current code, configuration, tests, and Git state.
- Update it throughout the project whenever durable context changes: vision, goals, constraints, decisions, architecture, verified implementation, research, risks, lessons, relevant user preferences, milestone status, or next actions.
- Reconcile it before substantial handovers and after meaningful milestones. Do not wait until the end of a project.
- Keep it compact and navigable. Put detailed decisions, evidence, experiments, and risks in their specialist logs and link to them.
- Label facts, decisions, assumptions, experiments, and recommendations distinctly. Correct or remove outdated information.
- Never store secrets, credentials, sensitive personal data, confidential third-party information, or raw chat transcripts. A private repository is not a secret store.
- If write access is unavailable, prepare the update and explicitly report that it remains unsaved.

## 8. Human-dependent actions and reminders

When progress depends on a user test, decision, account permission, external action, or real-world verification, do not leave the request buried in chat.

- Offer two practical paths: work through the action together one step at a time, or defer it.
- When deferred, record it in `docs/PENDING_ACTIONS.md` (initialized from `PENDING_ACTIONS_TEMPLATE.md`) or the project's existing canonical tracker.
- Record the exact action, reason, affected work, priority, owner, status, evidence, due/revisit trigger, and when it was last surfaced.
- Mark safety, privacy, security, legal, data-loss, and irreversible-risk checks as critical blockers. Pause the affected operation until verified.
- For ordinary blockers, pause only dependent work and continue unrelated implementation, research, and documentation.
- For non-blocking checks, proceed autonomously and raise them at a useful checkpoint or agreed interval.
- At each new session and handover, reconcile the register with current code and evidence. Do not ask for tests already passed unless relevant conditions changed.
- Scheduled ChatGPT tasks may deliver reminders when available and authorized, but they are optional. The action register remains authoritative. Never claim a future reminder exists without verified creation. Note that ChatGPT tasks created inside a Project cannot access that Project's uploaded/stored files.

## 9. Handover and continuous learning

Record the current branch and commit, completed work, changed files, tests run, known limitations, unresolved questions, and the next safe action.

When useful, also preserve:
- important user preferences and confirmed project decisions;
- research findings and their sources;
- technical facts verified from the actual system;
- assumptions, experiments, results, and open questions;
- joint insights that may improve the project or general collaboration methods.

Documentation exists to preserve useful knowledge, not to create administration. Update the most relevant existing document, avoid duplication, and keep the record proportionate. If a lesson may benefit other projects, generalize and sanitize it, explain its wider value, and propose a Template improvement through normal review rather than changing the shared Template automatically.
