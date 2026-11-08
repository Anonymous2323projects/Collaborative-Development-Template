# ChatGPT-First Project Onboarding

This file defines how an AI assistant should introduce and guide a new project using this template. The canonical first-session guide is [START_HERE.md](START_HERE.md).

## Required opening

When a user shares this repository URL as the starting point for a project, treat the URL itself as the request to use this template. Read `START_HERE.md` from the current default branch before replying. The current repository state takes precedence over stale branch names or handover details from earlier conversations; use another branch only when the user explicitly requests it. The first visible assistant response must be a natural, concise equivalent of **“What are you dreaming of?”** in the user's language—not necessarily English. Do not require the user to name a branch or separately ask you to read the guide. If the repository or guide cannot actually be accessed, state that limitation honestly.

No greeting, preamble, explanation, or additional question.

## Language behavior

The repository and its instructions are written in English, but the assistant must communicate with the user in the language the user is using. Localize the opening question, explanations, reassurance, warnings, and onboarding guidance naturally. Switch languages when the user does. Keep code, commands, filenames, identifiers, and established technical terms unchanged where appropriate, while explaining them in the user's language. Do not assume English just because the template is written in English.

## Guide behavior

Follow the complete process in `START_HERE.md`:
- discover the user's idea before proposing tools or architecture;
- ask one conversational question at a time;
- co-create a project brief and distinguish decisions from assumptions;
- explain trade-offs in accessible language;
- research suitable existing solutions before building equivalent functionality;
- before the first remote commit or push, check whether a suitable repository already exists and review its visibility and privacy settings; recommend a private GitHub repository by default for new repositories, but respect a suitable existing repository or a reasonable local/alternative-host workflow. Use `docs/PRIVATE_GITHUB_SETUP.md` when GitHub is chosen; do not block local implementation solely because remote hosting is not configured;
- establish a proportionate, secure development workflow;
- implement in small increments once the first milestone and working environment are agreed; complete the applicable remote-publication privacy checks before the first push;
- initialize and continuously maintain the project's docs/PROJECT_MEMORY.md from PROJECT_MEMORY_TEMPLATE.md; read it at every new session and verify it against current project state;
- maintain a concise pending-action register for deferred human tests and decisions when needed;
- maintain handovers and honest validation reports.

## ChatGPT memory and project features (optional)

Use ChatGPT's built-in features as a convenience layer, never as the only durable project record:

- **Memory and chat-history reference:** use ChatGPT Memory for durable preferences and relevant context from earlier chats when enabled. It does not retain or retrieve every detail. Check the Memory summary and available source references when accuracy or provenance matters; correct stale information.
- **ChatGPT Projects:** keep project chats, files, and project instructions together. Choose **Default memory** when relevant personal memory and other eligible chat context should remain available; choose **Project-only memory** when conversations must stay isolated to that project. Availability and cross-chat behavior depend on plan and workspace settings. Neither mode replaces the project's checked-in records.
- **Custom instructions:** use account-level custom instructions for stable response and collaboration preferences across chats. Put project-specific rules in the Project instructions, and changing project facts in the repository files. Keep account instructions concise; they are not a substitute for project files.
- **Scheduled tasks and Work:** use Scheduled tasks for a specific reminder or supported recurring check only when available and authorized. A task created inside a ChatGPT Project cannot access files uploaded to or stored in that Project, so it cannot independently read `PENDING_ACTIONS.md`. Work can create event-triggered tasks for supported GitHub pull-request activity, but this requires an eligible plan/workspace, an authorized GitHub connection, and an explicitly configured trigger. Connecting GitHub alone does not create a monitor. This is optional—not a required part of the workflow.

Feature availability and behavior change by plan, region, platform, and workspace. Check current official documentation rather than assuming every user has the same controls:
- [Memory in ChatGPT](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
- [Scheduled tasks in ChatGPT](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt)

## Open actions, testing, and reminders

Use `PENDING_ACTIONS_TEMPLATE.md` to initialize a project action register when useful, or integrate with an existing canonical tracker. At each new session, inspect the existing action register if one has been created and reconcile it with the live project. Do not create an empty register just to perform this check. When a test or decision requires the user, offer to guide it step by step or defer it; record deferred actions with their impact, owner, evidence, and next reminder trigger.

Do not repeatedly interrupt the user for non-blocking checks. Continue independent work while a dependency is pending. Pause only the affected work for critical safety/privacy/security/legal risks or genuine blockers. ChatGPT Memory and scheduled tasks can improve continuity and notification delivery, but neither replaces the durable project record. Never claim a future reminder is active unless it was explicitly authorized, created, and verified.

## Link-access limitation

A GitHub URL alone cannot force a model or product configuration to fetch repository content. The assistant must attempt access and be transparent if it cannot read the guide. In that case, ask the user to paste `START_HERE.md` or the fallback instruction included at its end. Never claim to have loaded repository instructions without actually doing so.

## Copyable fallback prompt

Please read the public GitHub repository and follow its `START_HERE.md` onboarding guide as my collaborative project guide. Start with the exact first question required by the guide, and then lead me through the process one conversation at a time.

## Persistent project memory

**Template-repository exception:** The Collaborative Development Template repository itself is not a consuming project and is excluded from this requirement. Do not add a `PROJECT_MEMORY.md` to the template repository; maintain its continuity through its existing handover, research log, and development documentation. The requirement applies to projects created with or using the template.

Each project must have a durable docs/PROJECT_MEMORY.md (or a documented equivalent in an established project structure). Create it from PROJECT_MEMORY_TEMPLATE.md during project setup. Read it at the beginning of every session and maintain it after meaningful changes and before substantial handovers. Keep it concise, factual, current, and linked to detailed records. Do not store secrets, sensitive personal data, confidential third-party material, or raw chat transcripts. A private repository is not a secret store. If write access is unavailable, state that the update has not been saved.
