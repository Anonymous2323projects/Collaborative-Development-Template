# Exact-Head Authorization App Setup

This guide configures the optional dedicated GitHub App used by the trusted default-branch authorization workflow. It is designed for a public repository using GitHub Free or a private repository whose plan supports GitHub Actions environments and environment secrets. Read it alongside the [Change, Review, and Merge Assurance standard](../MERGE_AND_CHANGE_ASSURANCE.md), which defines the review and authorization requirements.

**Do not create an App, generate a private key, or change a ruleset until the repository owner has approved that setup.** This document describes the procedure; it does not authorize the action.

## 1. Confirm the repository and plan

- Confirm the exact repository owner, repository name, default branch, and visibility.
- This design relies on a GitHub Actions environment, an environment secret, and a deployment-branch restriction.
- GitHub provides environments, environment secrets, and deployment-branch restrictions for public repositories on current plans. Private/internal repositories require GitHub Pro, Team, or Enterprise for these features. If the repository is private on GitHub Free, do not claim this environment-secret design is available; use the documented manual owner-approval fallback unless a separately reviewed secret-management design is adopted.
- Replace `main` below with the repository's actual default branch if it differs.

## 2. Create a dedicated GitHub App

From the account that owns the repository:

1. Open **Settings → Developer settings → GitHub Apps → New GitHub App**.
2. Give it a clear name such as `<repository>-merge-authorization`.
3. Set the homepage to the repository URL.
4. Select **Only on this account** for app visibility. This workflow does not need to be installable by other accounts.
5. Disable webhooks; this App does not receive webhook events.
6. Under **Repository permissions**, grant only:
   - **Commit statuses: Read and write**
   - **Metadata: Read-only** (GitHub's required baseline permission)
7. Leave all other permissions at **No access**. Do not grant Contents, Pull requests, Checks, Actions, Administration, or organization permissions for this design.
8. Create the App and record its **Client ID**. The Client ID is used as a workflow variable; it is not the private key.

The App must not be installed across all repositories. Its installation is restricted to the one repository in step 3.

## 3. Install the App on one repository only

1. Open the new App's **Install App** page.
2. Choose the account that owns the target repository.
3. Select **Only select repositories**.
4. Select only this repository and install.
5. Recheck the installation page and confirm the selected repository list contains no unrelated repositories.

## 4. Create and protect the authorization environment

In the target repository:

1. Open **Settings → Environments** and create an environment named exactly `merge-authorizer`.
2. Under deployment branches and tags, allow only the exact default branch (normally `main`). Do not select all branches or all protected branches.
3. Disable **Allow administrators to bypass configured protection rules**.
4. Add the following environment variable:
   - `MERGE_AUTH_APP_CLIENT_ID`: the App's Client ID.
5. Add the following environment secret:
   - `MERGE_AUTH_APP_PRIVATE_KEY`: the complete PEM private-key contents generated for this App.
6. Optionally set `MERGE_AUTHORIZER_LOGINS` to a comma-separated allowlist of exact GitHub login names. If it is set, include the repository owner. If it is absent in a user-owned repository, the trusted authorizer defaults to the repository owner.

**Secret handling:**

- Never put the private key in a repository-level secret, source file, issue, pull request, artifact, log, or chat message.
- Do not upload the PEM file to ChatGPT or Codex.
- Keep the downloaded PEM in a secure temporary location only long enough to add the environment secret; do not leave it in Downloads, the repository, or a synced project folder.
- GitHub App private keys do not expire automatically. They must be manually rotated or revoked. Treat this as a long-lived credential and keep its access limited.
- The workflow mints an installation token scoped to this repository with only `statuses:write`. The token is revoked by the action after the job and expires after one hour even if not revoked.

The Actions environment is a practical least-privilege control, not a hardware-backed key vault. A dedicated key vault with signing-only access can provide stronger protection, but requires a separately reviewed integration. Do not overstate the protection provided by an Actions environment secret.

## 5. Verify the workflow before enabling the ruleset gate

Confirm the default-branch workflow:

- triggers only on `issue_comment`;
- checks the authorized owner before creating the App token;
- checks out policy code from the default branch, not the PR head;
- does not execute PR code or workflows;
- uses `GITHUB_TOKEN` only with read permissions;
- references the App credentials only in the trusted authorization workflow;
- scopes the installation token to this repository and `permission-statuses: write`;
- sets `skip-token-revoke: false`;
- pins the token action to a reviewed full commit SHA.

The expected status context is **Explicit maintainer merge authorization**. Do not infer that the App is working merely because the workflow job ran.

## 6. Publish a test status before selecting the expected source

GitHub's ruleset UI requires the App to be installed, have the required status permission, and have recently submitted a check run associated with a pre-existing required status check. Therefore:

1. Use a disposable, non-production test PR with a known exact head SHA and a valid assurance record.
2. From the authorized owner account, post the exact authorization command for that test PR and full 40-character head SHA.
3. Confirm that the status **Explicit maintainer merge authorization** is published by the dedicated App on that exact SHA.
4. Open the ruleset editor and verify that the App is offered as the expected source for that exact status context.

**Stop if the App or context is not selectable.** The current workflow publishes a commit status. GitHub's documentation also refers to a recently submitted check run when describing expected-source selection. Do not guess that a commit status satisfies this UI prerequisite. Do not add `checks:write` or broaden App permissions as a workaround. Research and review a minimal Checks API alternative first; it may require a different status implementation and new adversarial tests.

Do not use a real production PR as the first setup test if a disposable test PR can be used.

## 7. Configure the live ruleset

Only after step 6 succeeds:

- Require **Explicit maintainer merge authorization** with the dedicated App selected as the expected source.
- Require the relevant CI checks for repository hygiene/workflow policy, secret scanning, CodeQL, and any stack-specific build/tests. Verify each exact check name and source.
- Require branches to be up to date with the base branch (strict checks).
- Require pull requests and resolved review threads.
- Block deletion and non-fast-forward updates.
- Keep bypass actors empty.
- For a single-maintainer repository, do not require an impossible second-person approval. The exact-head owner status is the separate owner authorization; it does not replace substantive review.

A passing status from an earlier head does not authorize a changed head. A base-branch update must also be handled by the strict up-to-date rule. Statuses do not expire automatically.

## 8. Adversarial acceptance tests

Before describing the gate as technically enforced, use separate test PRs to verify:

- an unauthorized comment cannot mint the App token or publish success;
- an authorized comment with a stale or incorrect SHA fails closed;
- a changed head requires fresh authorization;
- an unresolved review thread blocks authorization;
- ordinary authorization is rejected when protected policy files change;
- the policy-change route requires the additional protected-policy evidence and explicit owner decision;
- a PR-controlled workflow on a pull-request ref cannot access the environment secret;
- the App status is accepted only from the expected App identity;
- a revoke command changes the current status to failure;
- if status publication/revocation is unavailable, an older success may remain; the owner must verify revocation or invalidate the old head before treating it as revoked;
- the token is revoked after the workflow job.

If any test fails or cannot be performed, record the limitation and retain a manual owner gate. Do not claim technical enforcement.

## 9. Recovery and rotation

If the App key may be exposed:

1. Stop using the affected authorization workflow and prevent further merges.
2. Generate a replacement private key and update the environment secret through GitHub Settings.
3. Delete/revoke the compromised key in the App's key-pair settings.
4. Re-run the exact-head and adversarial acceptance tests.
5. Verify the live ruleset still requires the correct App and status context.
6. Record the incident and recovery evidence without reproducing the key.

If the App or environment is misconfigured, do not broaden permissions or enable administrator bypass to get past the failure. Pause the automated gate and use the documented manual owner-approval fallback until the issue is corrected and verified.

## Governing assurance standard

Follow the canonical [Change, Review, and Merge Assurance Standard](../MERGE_AND_CHANGE_ASSURANCE.md) for the complete review, authorization, and evidence requirements. This setup guide is subordinate to that standard.

## Official references

- [Create a GitHub App](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/creating-a-github-app)
- [Install your own GitHub App](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app)
- [Create GitHub App Token action](https://github.com/marketplace/actions/create-github-app-token)
- [Manage GitHub App private keys](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps)
- [GitHub Actions environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [Ruleset status-check requirements and expected source](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [REST API for commit statuses](https://docs.github.com/en/rest/commits/statuses)
- [REST API for check runs](https://docs.github.com/en/rest/checks/runs)
