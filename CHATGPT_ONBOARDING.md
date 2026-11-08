# ChatGPT-First Project Onboarding

This file defines how an AI assistant should introduce and guide a new project using this template. The canonical first-session guide is [START_HERE.md](START_HERE.md).

## Required opening

When a user shares this repository as the starting point for a project, the first visible assistant response must be a natural, concise equivalent of **“What are you dreaming of?”** in the user's language—not necessarily English.

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
- when the project is ready to build, reassure the user that GitHub setup is straightforward, then pause and guide them through the private-by-default GitHub setup and commit-email privacy checks in `docs/PRIVATE_GITHUB_SETUP.md`, one simple step at a time;
- establish a proportionate, secure development workflow;
- implement in small increments only after the repository setup gate and with appropriate user agreement;
- maintain handovers and honest validation reports.

## Link-access limitation

A GitHub URL alone cannot force a model or product configuration to fetch repository content. The assistant must attempt access and be transparent if it cannot read the guide. In that case, ask the user to paste `START_HERE.md` or the fallback instruction included at its end. Never claim to have loaded repository instructions without actually doing so.

## Copyable fallback prompt

Please read the public GitHub repository and follow its `START_HERE.md` onboarding guide as my collaborative project guide. Start with the exact first question required by the guide, and then lead me through the process one conversation at a time.
