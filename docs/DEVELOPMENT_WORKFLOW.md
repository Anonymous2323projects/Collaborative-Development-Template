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

## 3. Implement safely

- Work on a focused branch.
- Keep changes small and reviewable.
- Preserve existing architecture and conventions; avoid parallel systems where an existing one can be extended appropriately.
- Evaluate system-wide effects across modules, interfaces, workflows, dependencies, data, and existing behavior.
- Avoid unrelated refactors and hidden behavior changes.
- Inspect commands and scripts before running them.
- Do not install software, grant permissions, or change machine configuration without authorization.
- Never put secrets in code, tests, logs, or examples.

## 4. Validate

- Run formatting, linting, type checks, unit/integration tests, and builds where applicable.
- Add regression tests for bug fixes.
- Review dependency and licence changes.
- Inspect the complete diff for accidental changes, personal data, secrets, unsafe behavior, and unsupported claims.
- Report exact commands and outcomes. Never imply that an unrun check passed.

## 5. Review and integrate

- Open a pull request with a concise summary, rationale, risks, and test evidence.
- Review behavior, security, privacy, accessibility, maintainability, and documentation.
- Resolve review comments explicitly.
- Merge only with the required approval.

## 6. Handover and continuous learning

Record the current branch and commit, completed work, changed files, tests run, known limitations, unresolved questions, and the next safe action.

When useful, also preserve:
- important user preferences and confirmed project decisions;
- research findings and their sources;
- technical facts verified from the actual system;
- assumptions, experiments, results, and open questions;
- joint insights that may improve the project or general collaboration methods.

Documentation exists to preserve useful knowledge, not to create administration. Update the most relevant existing document, avoid duplication, and keep the record proportionate. If a lesson may benefit other projects, generalize and sanitize it, explain its wider value, and propose a Template improvement through normal review rather than changing the shared Template automatically.
