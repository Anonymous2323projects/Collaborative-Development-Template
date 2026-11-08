# Private GitHub Project Setup Guide

This guide defines the default repository-bootstrap procedure for a new project using the Collaborative Development Template.

## Mandatory transition gate: ready to build

Do not create a repository merely because a user has an early idea. First understand the idea, agree the project brief and initial scope, research the technical direction, and identify a sensible first milestone.

When the AI determines that the project is sufficiently clear and the user is ready to begin implementation, it must pause before coding and initiate this setup phase. Explain why GitHub is being prepared and guide the user through it one manageable step at a time.

**Default: create a new private repository for the project.** Do not make it public unless the user makes an informed, explicit choice to do so after the privacy implications have been explained. A public template repository, such as the Collaborative Development Template itself, must not be made private as part of setting up a user's separate project.

## 1. Check the user's starting point

Ask one question at a time:

1. Does the user already have a GitHub account?
2. Can the user sign in successfully?
3. Is the user already using GitHub for this project, or does a suitable repository already exist?

If the user has no account, guide them to [GitHub sign-up](https://github.com/signup). Explain each step in plain language and wait for the user to complete it. Do not request passwords, authentication codes, recovery codes, or other secrets in chat.

If the user already has an appropriate repository, inspect its visibility and configuration before proposing changes. Do not create duplicates or change an existing repository's visibility without explicit approval.

## 2. Secure the account's commit email privacy

Before the first project commit, guide the user to review GitHub's email privacy settings:

1. Open [GitHub email settings](https://github.com/settings/emails).
2. Enable **Keep my email addresses private**.
3. Enable **Block command line pushes that expose my email**, where this option is available.
4. Find and copy the exact GitHub-provided `noreply` email address shown in the account's email settings.
5. Explain that this protects the email address in future GitHub web-based operations and, when Git is configured correctly, future command-line commits.

For command-line Git commits, configure Git to use the exact `noreply` address shown in that user's own GitHub settings. Never guess, construct, or substitute an example address. If the user is using a graphical Git client or an IDE, guide them to its equivalent author-email setting.

For GitHub web-based commits, the privacy setting makes GitHub use the noreply address. The command-line block setting is an additional safeguard; it does not configure Git by itself.

**Important limits:**
- Email privacy is not anonymity. The GitHub username, commit author name, project content, and other activity may still identify the contributor.
- Changing the setting does not remove a personal email address from commits already created or pushed.
- Do not rewrite existing Git history to change commit identity without explaining the consequences and obtaining explicit permission.
- Never ask the user to paste their personal email address or noreply address into the conversation. The user can configure it locally or show only a redacted confirmation.

Official guidance:
- [Keeping command-line pushes from exposing a personal email](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address)
- [Setting the commit email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address)
- [GitHub email addresses and noreply addresses](https://docs.github.com/en/account-and-profile/concepts/email-addresses)

## 3. Create the project repository as private

Guide the user through GitHub's repository creation page:

1. Open [Create a new repository](https://github.com/new).
2. Choose a clear, project-appropriate repository name.
3. Add a short description if useful.
4. Set visibility to **Private**. This is the default for this workflow.
5. Initialize with a README if appropriate for the chosen setup.
6. Create the repository and confirm that GitHub displays it as **Private**.

Do not ask the user to publish source code, project plans, screenshots, issue text, or other material merely to make setup easier. Keep the project private while its contents, ownership, licensing, and release intentions are still being developed.

A private repository is accessible to its owner and people or applications the owner authorizes. It is not a substitute for account security, careful permission management, backups, or secret handling. Review collaborator access and grant only the minimum permissions needed.

If a connected GitHub tool can create repositories, the AI must still explain the intended name, owner, private visibility, and initial contents, then obtain the user's explicit approval before creating it. If no authorized repository-creation capability is available, guide the user through the GitHub interface; never claim to have created it.

## 4. Prepare the repository safely

After creation:

- Verify the repository URL and confirm that its visibility is private.
- Confirm that the intended owner is correct.
- Add only the agreed starter files and project documentation.
- Use a project-specific README, project brief, decision log, research log, risk notes, and milestone plan as appropriate.
- Keep secrets, passwords, tokens, private keys, personal data, and confidential third-party information out of the repository.
- Use placeholders and synthetic examples in documentation.
- Decide whether collaborators are needed; explain access levels before inviting anyone.
- Do not install tools, connect accounts, grant application permissions, or run commands with side effects without the user's informed approval.

## 5. Verify before the first commit or push

Before any project files are committed or pushed:

- Confirm the repository is private.
- Confirm email privacy is enabled in GitHub settings.
- Confirm Git or the selected Git client uses the user's GitHub-provided noreply address for commits.
- Confirm the command-line email-block setting is enabled where available.
- Review the files and commit contents for secrets, personal data, confidential information, and unintended publication.
- Explain what has been checked and what has not been verified.

Do not request that the user paste configuration output containing personal details into chat. Prefer asking the user to confirm the setting on their own device or provide a redacted screenshot.

Only after this gate is satisfied should the project move into implementation.

## 6. Continue with the normal development workflow

Once the repository is ready, establish the project-specific branch, review, testing, handover, and backup practices described in [the development workflow](DEVELOPMENT_WORKFLOW.md). Keep the workflow proportionate to the project's size and risk.

## AI behavior and user experience

- Detect the transition point proactively; the user should not have to know when GitHub setup is needed.
- Explain why this step comes before coding.
- Ask one simple question or give one small action at a time.
- Use plain language and explain unfamiliar terms.
- Never imply that a setting is enabled or a repository is private until verified.
- Keep the user in control of account creation, account connections, permissions, repository visibility, collaborator invitations, and publication.
- If the user chooses a different setup, explain the trade-offs and record the decision. Do not silently override the private-by-default safeguard.
