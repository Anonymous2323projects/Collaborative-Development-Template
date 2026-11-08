# ChatGPT-First Project Onboarding

This file defines how ChatGPT should introduce and guide a new project using this template. The canonical first-session guide is [START_HERE.md](START_HERE.md).

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

## Free-plan-first ChatGPT setup

The complete workflow must work with ChatGPT Free and an ordinary GitHub account. Paid features are optional enhancements, never prerequisites.

- **Projects are optional but useful:** ChatGPT Projects are available on Free. Free projects currently allow up to 5 files, and Free file uploads are limited to 3 per day; limits can change. Do not ask users to upload the whole repository. Prefer reading the GitHub files directly when access works. If it does not, request only the smallest relevant set of files. Uploaded project files are snapshots, not a live GitHub sync; refresh them after repository changes and verify their commit/date before relying on them.
- **Free-plan privacy:** content from Free projects may be used to improve OpenAI models when **Improve the model for everyone** is enabled. Check Data Controls before adding project material, and do not upload secrets or confidential content. Respect the project's privacy and legal requirements.
- **Do not rely on cross-chat recall:** Memory and project chat-reference behavior varies by plan, region, settings, and rollout. Even when enabled, Memory does not retain every detail. Start each new session from the canonical GitHub project memory and latest handover; verify facts against the repository.
- **Project instructions are not repository instructions:** ChatGPT does not automatically execute or load `AGENTS.md` merely because it exists in GitHub. Read it explicitly, and where useful place a short project-specific summary in ChatGPT Project instructions. Keep the full authoritative instructions in the repository. On Free, use the five Project file slots sparingly: current project memory, latest handover, the pending-action register if it exists, and only the active specifications needed for the task. Do not upload every template or policy.
- **GitHub access is conditional and read-only through the ChatGPT GitHub app:** availability depends on plan and product surface. The GitHub app can read permitted repository content but does not push commits or edit files. Never assume a Free account has repository-connector access or write access. If direct write tools are unavailable, prepare the exact changes and guide the user through applying them; verify only after GitHub confirms the result.
- **No paid automation dependency:** ChatGPT Work, event-triggered tasks, Scheduled Tasks, deep research, and other paid or limited tools are optional. The action register is a review cue, not a notification service. Continue without them.

## ChatGPT memory and project features (optional)

Use ChatGPT's built-in features as a convenience layer, never as the only durable project record:

- **Memory and chat-history reference:** use ChatGPT Memory for durable preferences and relevant context from earlier chats when enabled. It does not retain or retrieve every detail. Check the Memory summary and available source references when accuracy or provenance matters; correct stale information.
- **ChatGPT Projects:** keep project chats, files, and project instructions together. Choose a memory mode only if it is offered and its behavior fits the privacy needs. Do not promise that Free can recall previous project chats; use the repository files as the reliable continuity layer. Neither mode replaces checked-in records.
- **Custom instructions:** use account-level custom instructions for stable response and collaboration preferences across chats. Put project-specific rules in the Project instructions, and changing project facts in the repository files. Keep account instructions concise; they are not a substitute for project files.
- **Scheduled tasks and Work:** use a scheduled reminder only if the feature is available and the user explicitly authorizes it. A task created inside a ChatGPT Project cannot access files uploaded to or stored in that Project, so it cannot independently read `PENDING_ACTIONS.md`. Work-based GitHub event monitoring is a separate, plan-dependent feature and is not part of the Free baseline.

Feature availability and behavior change by plan, region, platform, and workspace. Check current official documentation rather than assuming every user has the same controls:
- [Memory in ChatGPT](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
- [Custom Instructions in ChatGPT](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions)
- [Scheduled tasks in ChatGPT](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt)
- [Connecting GitHub to ChatGPT](https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt)
- [ChatGPT Free Tier FAQ](https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq)
- [File uploads and limits](https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt)

## Open actions, testing, and reminders

Use `PENDING_ACTIONS_TEMPLATE.md` to initialize a project action register when useful, or integrate with an existing canonical tracker. At each new session, inspect the existing action register if one has been created and reconcile it with the live project. Do not create an empty register just to perform this check. When a test or decision requires the user, offer to guide it step by step or defer it; record deferred or still-outstanding actions with their impact, owner, evidence, and next review trigger.

Do not repeatedly interrupt the user for non-blocking checks. Continue independent work while a dependency is pending. Pause only the affected work for critical safety/privacy/security/legal risks or genuine blockers. ChatGPT Memory and scheduled tasks can improve continuity and notification delivery, but neither replaces the durable project record. Never claim a future reminder is active unless it was explicitly authorized, created, and verified.

## Link-access limitation

A GitHub URL alone cannot force ChatGPT to fetch repository content. Attempt access and be transparent if it fails. The ChatGPT GitHub app, where available, is read-only; it does not write commits or edit repository files. If repository access is unavailable, ask for `START_HERE.md` and only the other files needed for the current task. Never claim to have loaded or changed repository content without verifying it.

## Copyable fallback prompt

Please use the Collaborative Development Template as my ChatGPT-first project guide. Read `START_HERE.md` and `AGENTS.md` from the repository if you can access them. If the repository is private or you cannot access it, do not ask me to make it public; tell me which files you need and I will provide them. Start with the exact first question required by the guide, then lead me through the process one conversation at a time.

## Persistent project memory

**Template-repository exception:** The Collaborative Development Template repository itself is not a consuming project and is excluded from this requirement. Do not add a `PROJECT_MEMORY.md` to the template repository; maintain its continuity through the maintainer handover and development documentation. The requirement applies to projects created with or using the template.

Each project must have a durable docs/PROJECT_MEMORY.md (or a documented equivalent in an established project structure). Create it from PROJECT_MEMORY_TEMPLATE.md during project setup. Read it at the beginning of every session and maintain it after meaningful changes and before substantial handovers. Keep it concise, factual, current, and linked to detailed records. Do not store secrets, sensitive personal data, confidential third-party material, or raw chat transcripts. A private repository is not a secret store. If write access is unavailable, state that the update has not been saved.
