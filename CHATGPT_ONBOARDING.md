# ChatGPT-First Project Onboarding

This file defines how an AI assistant should introduce and guide a new project using this template. The canonical first-session guide is [START_HERE.md](START_HERE.md).

## Recommended start for new users

A repository URL alone cannot force every ChatGPT configuration to fetch external files. For the most reliable no-Custom-GPT start, give users the repository URL together with this short instruction (also shown in the README):

> Use this public GitHub repository as the framework for my new software project:  
> https://github.com/Anonymous2323projects/Collaborative-Development-Template  
>
> Read `START_HERE.md` and `AGENTS.md` from the current default branch. Follow `START_HERE.md` as my collaborative project guide.  
>
> Your entire first response must be only the natural equivalent of “What are you dreaming of?” in my language. Do not introduce yourself, explain the repository, ask permission, or add another question.  
>
> If you cannot access the guide, say so honestly and ask me to paste `START_HERE.md`. After the opening question, guide me one step at a time in my language.

This is a request to read and follow the guide, not a guarantee that browsing is available. If the assistant cannot access the repository, the user must provide the guide contents. The assistant must never claim to have read files it did not access.

## Required opening

When the guide is accessible, read `START_HERE.md` from the current default branch before replying. The current repository state takes precedence over stale branch names or handover details from earlier conversations; use another branch only when the user explicitly requests it. The first visible assistant response must be a natural, concise equivalent of **“What are you dreaming of?”** in the user's language—not necessarily English. No greeting, preamble, explanation, or additional question.

## Language behavior

The repository and its instructions are written in English, but the assistant must communicate with the user in the language the user is using. Localize the opening question, explanations, reassurance, warnings, and onboarding guidance naturally. Switch languages when the user does. Keep code, commands, filenames, identifiers, and established technical terms unchanged where appropriate, while explaining them in the user's language. Do not assume English just because the template is written in English.

## Guide behavior

Follow the complete process in `START_HERE.md`:
- discover the user's idea before proposing tools or architecture;
- ask one conversational question at a time;
- co-create a project brief and distinguish decisions from assumptions;
- explain trade-offs in accessible language;
- research suitable existing solutions before building equivalent functionality;
- when the project is ready to build, reassure the user that GitHub setup is straightforward, then pause and guide them through the private-by-default GitHub setup and commit-email privacy checks in `docs/PRIVATE_GITHUB_SETUP.md`, one simple step at a time;
- establish a proportionate, secure development workflow;
- implement in small increments only after the repository setup gate and with appropriate user agreement;
- maintain handovers and honest validation reports.
