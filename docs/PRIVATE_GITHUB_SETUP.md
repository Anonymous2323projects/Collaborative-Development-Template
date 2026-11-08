# Private GitHub Project Setup Guide

Use this guide when a project is ready to work with a remote GitHub repository. It is not a reason to delay discovery, design, or safe local development.

## 1. Check the starting point

Ask one question at a time:

1. Does the user already have a GitHub account?
2. Is there already a suitable repository for this project?
3. Is the user able to access it?

If an appropriate repository exists, inspect its settings before suggesting changes. Do not create a duplicate or change visibility without explicit approval.

If the user needs an account, guide them to [GitHub sign-up](https://github.com/signup). Never ask for passwords, authentication codes, recovery codes, or other secrets in chat.

## 2. Choose the commit identity knowingly

A Git commit can contain the author's name and email address. Explain this before the first remote push, then let each contributor choose how their own identity appears.

- **Public email:** the contributor may use an email address they are comfortable making visible in commit history.
- **GitHub `noreply` email:** the contributor can use the address GitHub provides in [email settings](https://github.com/settings/emails). This helps keep their personal email out of future commits.
- **Other informed choice:** respect the contributor's decision where GitHub supports it.

If the contributor chooses `noreply`, help them configure the exact address shown in their own GitHub settings for command-line Git or their chosen editor. Do not guess or construct an address, and do not ask them to paste it into chat. GitHub's **Keep my email addresses private** setting controls web-based commits; command-line Git must also be configured with the chosen address. The optional **Block command line pushes that expose my email** setting can provide an additional safeguard, but it does not configure Git.

Before the first push, check the author details attached to the saved change (name and email) and compare them with the contributor's choice. The contributor can confirm the result without sharing the full address in chat.

**Important limits:**
- A `noreply` address is not anonymity. A username, author name, code, or other public activity may still identify someone.
- Changing settings does not remove an email address from commits already pushed.
- Do not rewrite existing history or change another contributor's commit identity without explaining the consequences and obtaining explicit permission.
- Never impose either disclosure or concealment. Each contributor controls their own identity details.

Official guidance: [Set your commit email](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address), [Email addresses on GitHub](https://docs.github.com/en/account-and-profile/concepts/email-addresses).

## 3. Create or choose the repository

For a new GitHub project repository, **Private** is the default recommendation. Public visibility requires the user's informed, explicit choice after explaining what becomes visible.

1. Open [Create a new repository](https://github.com/new).
2. Choose a clear name and add a description if useful.
3. Select **Private** unless the user has explicitly chosen public visibility.
4. Initialize with a README only if appropriate for the chosen setup.
5. Create the repository and verify its owner, URL, and visibility.

A private repository is accessible to its owner and people or applications they authorize. It is not a secret store or a substitute for account security, backups, and careful access management. Grant only the permissions collaborators need.

Do not make a repository public just to obtain a GitHub feature. Plan availability changes; check the current [protected branch documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [secret scanning documentation](https://docs.github.com/en/code-security/concepts/secret-security/about-alerts), and [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) before relying on a specific plan limit. The template's own Gitleaks workflow is an additional check, not a guarantee or a substitute for GitHub Secret Protection.

If a connected tool can create a repository, explain the intended owner, name, visibility, and initial contents first, then obtain explicit approval. Never claim creation unless verified.

## 4. Prepare and verify before the first push

- Confirm the correct repository and intended visibility.
- Confirm the contributor's chosen commit identity is configured.
- Check the author details attached to the saved change (name and email) against that choice.
- Review files and commit contents for secrets, personal data, confidential information, and unintended publication.
- Check collaborator access and explain any external permissions being requested.
- Explain what was verified and what remains unknown.

Do not ask the user to paste personal email addresses or unredacted configuration output into chat. A redacted screenshot or local confirmation is usually enough.

Local work can continue before these remote-publication checks are complete, provided it is safe and no remote push occurs.

## 5. Continue with the project workflow

Once the repository is ready, follow [the development workflow](DEVELOPMENT_WORKFLOW.md). On plans where branch protection is unavailable, review and merge approval remain manual working agreements. Keep the process proportionate to the project's size and risk.

## How ChatGPT should guide the user

- Explain the reason for each check in plain language.
- Give one manageable step at a time.
- Reuse verified settings; do not make the user repeat setup without a reason.
- Preserve the user's choice of repository, visibility, and own commit identity.
- Ask before account connections, permission changes, invitations, repository creation, or publication.
- Never claim that a setting or repository state is verified until it has actually been checked.
