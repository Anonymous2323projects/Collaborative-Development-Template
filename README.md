# Collaborative Development Template

![Collaborative Development Template — manifesto banner](assets/manifesto-banner.png)

A ChatGPT-first framework for turning an idea into a secure, maintainable project—with clear guidance, human control, and GitHub as an optional durable work record.

## Start a project

Share this repository with ChatGPT and ask it to use the template. If it can read the repository, its first response should be only a natural equivalent of **“What are you dreaming of?”** in your language. It must read [START_HERE.md](START_HERE.md) first and be honest if it cannot access the guide.

You do not need programming experience to begin. The guide helps you explore the idea, agree on a useful first step, and build at a manageable pace.

**Before adding private project information:** this is a public starter template, not your private workspace. When you create your own project from it, choose **Private** for the new project repository. Also check your ChatGPT Project's sharing settings separately and use **Only those invited** unless you intentionally want others with the link to join. The setup guide explains both.

**Required when using a ChatGPT Project:** have ChatGPT prepare one complete, project-specific set of Project Instructions. Paste it into **Project settings → Project instructions** and save it. GitHub files and uploads do not install instructions automatically. Follow the full setup and verification steps in [START_HERE.md](START_HERE.md).

Private is the strong default, not a requirement for every project. One private repository normally suffices for a private project. If code/product will be **public**, keep non-public memory and coordination **outside** that public repository in a suitable restricted private location. Reuse secure local storage, an existing private repository or a trusted other-hosted workspace where continuity, access and backup can be managed; a separate private GitHub repository is an option, **not mandatory**. Review the [privacy guide](PRIVACY_AND_PUBLICATION.md) before publication. Multi-project coordination does not itself require extra repositories.

An existing suitable repository or a local/alternative-host workflow is also valid. Before the first remote push, explain publication risks and let each contributor choose how their own commit name and email appear.

## Find what you need

### Start and update

- [Start here — complete project guide](START_HERE.md)
- [ChatGPT onboarding — short ChatGPT-specific rules](CHATGPT_ONBOARDING.md)
- [Safe template update guide](docs/TEMPLATE_UPDATE_GUIDE.md)
- [Reusable update prompt](docs/TEMPLATE_UPDATE_PROMPT.md)
- [Template version record to copy into a downstream project](docs/TEMPLATE_VERSION_TEMPLATE.md)

### Set up and build

- [Private GitHub setup and commit identity choices](docs/PRIVATE_GITHUB_SETUP.md)
- [Development workflow](docs/DEVELOPMENT_WORKFLOW.md)
- [Project brief — normal starting point](PROJECT_BRIEF_TEMPLATE.md)
- [Project memory — required for downstream projects](PROJECT_MEMORY_TEMPLATE.md)
- [Pending actions — only when human follow-up is needed](PENDING_ACTIONS_TEMPLATE.md)
- [Handover — when work changes hands](docs/HANDOVER_TEMPLATE.md)

### Optional planning and specialist references

Use these when the project needs them; they are not all required for every project.

- [Decision log](DECISION_LOG_TEMPLATE.md) — material decisions and their reasons
- [Research note](RESEARCH_TEMPLATE.md) — evidence behind a meaningful choice
- [Risk register](RISK_REGISTER_TEMPLATE.md) — a separate record for complex or higher-risk work
- [Milestone plan](MILESTONE_PLAN_TEMPLATE.md) — multiple milestones or coordination needs
- [Review checklist](docs/REVIEW_CHECKLIST.md)
- [Independent agent review](docs/INDEPENDENT_AGENT_REVIEW.md)

### Safety, privacy, and release

- [Important notice and disclaimer](DISCLAIMER.md)

These policies cover different responsibilities. Read the relevant one when the work reaches that area. **The risk and release-readiness assessment is required before public release.**

- [AI safety and instruction authority](AI_SAFETY_AND_MODEL_SPEC.md)
- [Security policy and vulnerability reporting](SECURITY.md)
- [Privacy and public publication](PRIVACY_AND_PUBLICATION.md)
- [Incident response](INCIDENT_RESPONSE.md)
- [Project risk and release readiness](PROJECT_RISK_AND_RELEASE_READINESS.md)
- [Update and release security](UPDATE_AND_RELEASE_SECURITY.md)

### Contributing and project information

- [Contributor guide](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Maintainer governance](GOVERNANCE.md)
- [Changelog](CHANGELOG.md)
- [Asset provenance and notices](assets/README.md)
- [AI and contributor repository instructions](AGENTS.md)

## The five priorities

Apply these priorities in order:

1. **Safety** — protect people, data, devices, and project integrity.
2. **Legal solidity** — identify applicable legal, privacy, consumer, intellectual-property, and licence obligations.
3. **Usability** — make the safe and responsible path understandable and practical.
4. **Trust** — be transparent, predictable, and evidence-based.
5. **Freedom** — preserve user choice, ownership, portability, and control within necessary safety and legal boundaries.

Do not weaken necessary safeguards for convenience. Use the least restrictive effective approach, and keep process overhead proportionate to the project's real needs.

## Access, privacy, and verification

A repository URL does not guarantee that ChatGPT can read or change GitHub. If access is unavailable, the assistant must say so and ask for only the files needed. It must never claim a change or check succeeded without evidence.

This repository is public. Do not add secrets, personal information, private conversations, confidential project material, or another person's identifying details. Use fictional examples and placeholders. If sensitive information is exposed, follow [the incident response playbook](INCIDENT_RESPONSE.md).

Automated checks cover only their documented scope. Passing checks do not prove complete security, privacy, or legal compliance.

## Licence

This project is licensed under the [MIT License](LICENSE). Third-party components and contributions may remain subject to their own rights and notices.
