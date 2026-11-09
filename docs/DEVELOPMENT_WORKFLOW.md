# Collaborative Development Workflow

Use this workflow as a practical guide, not a checklist to repeat mechanically. Adapt it to the project's size, risks, team, and release model.

## 1. Understand before changing

- Read the README, contributor instructions, relevant architecture notes, and latest handover.
- Check the current branch, working-tree state, recent commits, relevant files, dependencies, and existing conventions.
- Confirm the user-visible goal, constraints, acceptance criteria, and non-goals.
- Trace effects across related modules, interfaces, data, settings, and controls before editing.
- Separate verified facts from assumptions and open questions.

## 2. Research before implementation

Before building equivalent functionality, look for suitable existing tools, libraries, and projects. The assistant should discover plausible options; the user should not need to know what to search for.

For meaningful or high-impact changes, use the research standard in [Change, Review, and Merge Assurance](../MERGE_AND_CHANGE_ASSURANCE.md): prioritize peer-reviewed research, applicable standards, law, and primary official documentation; record methods, limitations, applicability, alternatives, and evidence gaps. Research effort should be thorough enough to support the decision, not limited by a speed target. Keep genuinely trivial choices proportionate.

## 3. Prepare for remote collaboration

Do not delay discovery, design, or safe local work because GitHub is not ready. Before the first remote commit or push, follow [the Private GitHub Project Setup Guide](PRIVATE_GITHUB_SETUP.md).

- Check whether a suitable repository already exists.
- For a new GitHub project repository, use **Private** by default. Public visibility requires the user's informed, explicit choice.
- Explain that commit author name and email may be visible in public commits. Let each contributor choose whether to use a public email or GitHub's `noreply` address.
- If a contributor chooses `noreply`, help configure the exact address shown in their GitHub settings. Never guess it or ask them to share it in chat.
- Check the author details attached to the saved change (name and email) against the contributor's informed choice before pushing. Do not make email concealment a universal requirement.
- Verify repository visibility and review files for secrets, personal data, and confidential material before remote publication.
- Ask before account connections, permission changes, collaborator invitations, repository creation, or other external changes.

These checks protect remote publication; they are not a reason to block safe local development.

## 4. Implement safely

- Work on a focused branch and keep changes reviewable.
- Verify the actual GitHub plan, repository visibility, active rulesets, required status checks, expected check sources, bypass actors, and administrative permissions. GitHub Free supports rulesets for public repositories; private-repository availability differs by plan. Never infer enforcement merely because a workflow or policy document exists.
- Preserve existing architecture and conventions. Avoid unrelated refactors and parallel systems.
- Inspect commands and scripts before running them.
- Do not install software, grant permissions, or change machine configuration without authorization.
- Never put secrets in code, tests, logs, or examples.

## 5. Validate

For meaningful changes, compare documentation, requirements, implementation, tests, workflows, live repository settings, and user-facing claims. Record traceability and the five-perspective assessment in a PR-specific assurance record as described in [Change, Review, and Merge Assurance](../MERGE_AND_CHANGE_ASSURANCE.md). A serious procedural defect triggers a project-wide search for analogous weaknesses and regression controls.

For a substantial change, compare the result with the pre-change baseline and acceptance criteria. Check that only intended files and behavior changed, and look for regressions, omissions, broken links/references, conflicting documentation, and new risks. Re-run the checks affected by the change; reuse earlier evidence only when it still applies to the exact code, configuration, permissions, and environment.

Choose checks based on the change and its risks. Reuse a passing result only when it applies to the exact code, configuration, and environment being assessed.

- Run relevant tests, checks, builds, and accessibility or security reviews.
- Add a regression test when fixing a demonstrated defect.
- Review dependency and licence changes.
- Inspect the complete diff for accidental changes, secrets, personal data, unsafe behavior, and unsupported claims.
- Report exactly what was and was not checked. A passing automated check is not proof of complete security or legal compliance.

## 6. Review and integrate

Summarize the change, reason, user impact, risks, and validation evidence. Use a pull request for substantive changes. Resolve review comments and require the applicable automated gates. For single-maintainer projects, do not invent a second human approval; use an exact-head owner authorization gate if the platform can enforce it. A changed head SHA invalidates prior authorization. Never merge without explicit owner authorization. Follow [Change, Review, and Merge Assurance](../MERGE_AND_CHANGE_ASSURANCE.md).

## 7. Keep downstream template updates safe

A repository created from this template is a separate copy; it does not receive later changes automatically. Record the upstream source and exact applied release/tag or commit in `docs/PROJECT_MEMORY.md` when known. Mark an unknown baseline honestly.

At meaningful maintenance checkpoints, check for relevant upstream changes when repository access is available. If an active project has gone about 30 days without a check, raise it at the next useful checkpoint. Distinguish published releases from unreleased branch changes. Explain relevance and local conflicts, then offer a focused patch. Never silently apply, push, merge, overwrite, install, or migrate an update. Urgent safety, security, or legal concerns require an evidence-based warning and narrow mitigation advice—not bypassing approval. See [Update and Release Security](../UPDATE_AND_RELEASE_SECURITY.md) for updater design.

## 8. Maintain project memory

Every downstream project must keep a durable `docs/PROJECT_MEMORY.md`, or document the equivalent canonical file already used by the project. Initialize it from [the project memory template](../PROJECT_MEMORY_TEMPLATE.md).

- Read it at the start of each work session and verify important facts against the live project.
- Update it after meaningful changes to scope, decisions, architecture, verified work, research, risks, lessons, or next steps.
- Keep it concise. Link to detailed decision, research, risk, and test records rather than copying them.
- Label facts, user decisions, assumptions, experiments, and recommendations clearly.
- Never store secrets, sensitive personal data, confidential third-party information, or raw chat transcripts.
- If write access is unavailable, prepare the update and say clearly that it remains unsaved.

**Template-repository exception:** the template itself is not a downstream project. Do not add `docs/PROJECT_MEMORY.md` here; use the private maintainer handover and records instead.

## 9. Track human-dependent actions only when needed

When progress genuinely depends on a user decision, test, account permission, or external action, explain why and what it unlocks. Offer step-by-step help or deferral.

If the action remains outstanding beyond the current interaction, record it in `docs/PENDING_ACTIONS.md` or the project's existing tracker. Do not create an empty register or duplicate an existing task list. Mark safety, privacy, security, legal, data-loss, and irreversible-risk checks as critical blockers. Pause only work affected by a blocker; continue independent work. A register does not send notifications by itself.

## 10. Handover and learning

When work is being transferred or a session is ending, record only what the next person or session needs:

- current branch and commit;
- completed work and important changed files;
- checks run and not run;
- known risks, limitations, and unresolved decisions;
- next safe action and any genuinely blocking human action.

Put durable decisions, research, and risks in their canonical records and link to them. Do not duplicate their contents in every handover. Preserve reusable learning only after removing project-specific and private information.

## 11. Avoid repeated work

When a material process failure or near miss occurs, perform the systemic recurrence review in [Change, Review, and Merge Assurance](../MERGE_AND_CHANGE_ASSURANCE.md) across all related procedures and technical controls. Do not limit remediation to the immediate file or incident.


- Verify a setting or requirement once and reuse the evidence while it remains valid.
- Do not repeat GitHub walkthroughs or ask again for a decision already made for the same scope.
- Select tests based on the change; run broader checks at meaningful integration or release points.
- Batch related reading, edits, and checks.
- Recheck only when relevant code, configuration, environment, requirements, evidence, or risk has changed.
- Explain why a repeat check is needed.

Efficiency must remove duplicate effort, not safety-critical verification.
