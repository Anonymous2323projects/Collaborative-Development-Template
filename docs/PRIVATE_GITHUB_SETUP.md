# Private GitHub Project Setup Guide

Use this guide when a project is ready to work with a remote GitHub repository. It is not a reason to delay discovery, design, or safe local development.

The public Collaborative Development Template is only the starter. Starting with a **Private** GitHub project is the recommendation, not a compulsory step before exploration. For an entirely private project, one private repository normally suffices. If the code/product repository will be **public**, keep non-public memory, decisions, handovers and communication in a separate **restricted private record location**. An existing private GitHub repository, protected local files or a suitably secured other-hosted workspace may qualify; a second GitHub repository is one practical option, not a requirement. Verify privacy, recovery and handover before publication.

GitHub privacy does not change ChatGPT Project sharing. Check the ChatGPT Project separately and use **Only those invited** unless wider access is intentional. Members of a shared Project can see its chats, files, and instructions. Project-only memory does not hide that material from members.

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

**Choose the setup before publishing:**
- **Private project:** use one suitable private project repository. No extra coordination repository is needed just because the template is used.
- **Public product/code:** store only publishable material in the public repository. Before the first public push, establish a separate protected private record location for memory, decisions, handovers and internal work. This can be an existing private repository, secure local storage or another trusted restricted host; an extra GitHub repository is optional. Moving files later does not erase public Git history.
- **No remote repository needed yet:** continue idea exploration or safe local work. Offer GitHub when it provides a real benefit.

For a project intended to become public, guide the user through these steps at the appropriate time:
1. Check for an existing public product repository and a suitable restricted private record location, whether a private repository, protected local workspace or another secure host. Verify visibility, access, ownership, connected apps where relevant, and reliable backup/handover; do not duplicate suitable storage.
2. If no suitable private record location exists, explain the options and obtain the owner's choice. A **Private** GitHub coordination repository is a simple option, but protected local or appropriately restricted other-hosted storage also works when the project can be handed over securely. Do not create accounts/repositories or connect access without explicit approval.
3. Propose or verify a separate public product repository. Review its initial files, metadata, commit identity, history, issues and PRs for non-public material **before** the first public push or visibility change.
4. Record privately which repository holds publishable code and where the private project record lives. Keep ChatGPT Project sharing settings separately restricted; ensure Project Instructions point to the correct record location and explain a manual status/handover method when connectors are unavailable.
5. Complete the [privacy review](../PRIVACY_AND_PUBLICATION.md) and [release-readiness assessment](../PROJECT_RISK_AND_RELEASE_READINESS.md) before public release; obtain the user's explicit publication authorization.

Do not create either repository, alter visibility, link access or publish without informed user authorization.

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
