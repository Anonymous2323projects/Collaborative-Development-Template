# Collaborative Development Template

Turn an idea into a project with ChatGPT, one manageable step at a time. This public starter is for beginners and experienced builders; no programming experience or paid AI plan is required to begin.

**You need:** access to ChatGPT (Free is enough) and a web browser. GitHub is useful when you want to save code or project records, but it is **not required to explore an idea**. This public template is not a place to put private notes or passwords.

## Start in five steps

1. **Check privacy first.** If you use a ChatGPT Project, check who can see its chats and files; choose **Only those invited** unless you deliberately want wider sharing. Do not share passwords, secret keys, or confidential data. For separate projects, consider **Project settings → Memory → Project-only memory** for context isolation; sharing and connected-app access still need their own checks. GitHub privacy and ChatGPT sharing are separate settings.
2. **Open a ChatGPT conversation.** Share the [public template link](https://github.com/Anonymous2323projects/Collaborative-Development-Template) and ask ChatGPT to read `START_HERE.md` and `AGENTS.md` on the current default branch. If it cannot read them, it must tell you; provide only the relevant public text instead. The template's opening question is **“What are you dreaming of?”**
3. **Describe your idea without secrets.** ChatGPT helps you clarify the goal, intended users, risks, and one small first result. You do not need to decide the programming language or buy a service yet.
4. **Set up continuity if you use a ChatGPT Project.** Ask for **one complete, project-specific Project Instructions block**, then open **Project settings → Project instructions**, paste it, and save it yourself. GitHub files do not install these instructions automatically. If Project Instructions are unavailable, continue in an ordinary chat using this guide and a short written handover.
5. **Save work when you are ready.** You can use an existing suitable repository. For a new GitHub repository, choose **Use this template → Create a new repository**, give it a name, and normally choose **Private** before creating it. Create project memory from [the memory template](PROJECT_MEMORY_TEMPLATE.md) in a suitable private record location. If you intentionally publish code, keep private notes and coordination **outside** that public repository. Ask for explicit approval before publishing, changing access, or merging.

**First success:** you and ChatGPT have agreed on a short project goal, a privacy-conscious place for any records, and the next verifiable action. No code or GitHub repository is required just to reach that point.

**No Python, scripts, or local Git installation is required for the standard ChatGPT-first workflow.** The template also includes optional developer/maintainer tooling for automated checks and Git recovery rehearsals. Those tools are **not** onboarding prerequisites: running the Python recovery script locally requires Python and a compatible Git installation; GitHub Actions can run configured checks on its own hosted runner without a local Python installation. A successful Git-tree rehearsal does not replace an independent backup or authorize a merge. See [merge and recovery assurance](MERGE_AND_CHANGE_ASSURANCE.md) only if you choose those advanced checks.

![Collaborative Development Template — manifesto banner](assets/manifesto-banner.png)

For a guided explanation and troubleshooting, continue with [Start Here](START_HERE.md). The references below are for the stages when you actually need them; you do not need to read every policy before discussing an idea.

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
- [Change, review, and merge assurance](MERGE_AND_CHANGE_ASSURANCE.md) — risk-based review, evidence, and explicit owner decisions (no automated owner-authorization gate)
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
