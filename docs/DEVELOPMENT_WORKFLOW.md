# Collaborative Development Workflow

This workflow is a starting point. Adapt it to the project's risk, team size, stack, and release model.

## 1. Understand before changing

- Read the README, contributor instructions, architecture notes, and current handover.
- Inspect the working tree, active branch, recent commits, and relevant implementation.
- Identify the user-visible goal, constraints, acceptance criteria, and non-goals.
- Separate verified facts from assumptions and open questions.

## 2. Research and plan

- Prefer primary documentation, source code, specifications, and maintained upstream repositories.
- Record source URLs, versions, dates, licence terms, and what was actually verified.
- Distinguish inspiration from direct reuse; preserve required notices and licence obligations.
- Propose a small implementation plan with risks and validation steps.

## 3. Implement safely

- Work on a focused branch.
- Keep changes small and reviewable.
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

## 6. Handover

Record the current branch and commit, completed work, changed files, tests run, known limitations, unresolved questions, and the next safe action.
