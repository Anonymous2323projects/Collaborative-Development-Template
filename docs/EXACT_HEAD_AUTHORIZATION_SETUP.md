# Exact-Head Authorization App Setup

This guide configures the optional dedicated GitHub App used by the trusted default-branch authorization workflow. It is designed for a public repository using GitHub Free or a private repository whose plan supports GitHub Actions environments and environment secrets. Read it alongside the [Change, Review, and Merge Assurance standard](../MERGE_AND_CHANGE_ASSURANCE.md), which defines the review and authorization requirements.

**Do not create an App, generate a private key, or change a ruleset until the repository owner has approved that setup.** This document describes the procedure; it does not authorize the action.

## 1. Confirm the repository and plan

- Confirm the exact repository owner, repository name, default branch, and visibility.
- This design relies on a GitHub Actions environment, an environment secret, and a deployment-branch restriction.
- GitHub provides environments, environment secrets, and deployment-branch restrictions for public repositories on current plans. Private/internal repositories require GitHub Pro, Team, or Enterprise for these features. GitHub rulesets are likewise available on GitHub Free for public repositories, but private repositories require Pro, Team, or Enterprise. Therefore, a private repository on GitHub Free cannot rely on this environment-secret design or ruleset enforcement. Its manual owner-approval fallback is procedural only: it cannot technically prevent direct pushes or merges and is not equivalent to an enforced gate. Record that reduced assurance explicitly; do not claim technical enforcement. Do not make a repository public or upgrade a plan without the owner's informed choice.
- Replace `main` below with the repository's actual default branch if it differs.

## 2. Create a dedicated GitHub App

From the account that owns the repository:

1. Open **Settings → Developer settings → GitHub Apps → New GitHub App**.
2. Give it a clear name such as `<repository>-merge-authorization`.
3. Set the homepage to the repository URL.
4. Select **Only on this account** for app visibility. This workflow does not need to be installable by other accounts.
5. Disable webhooks; this App does not receive webhook events.
6. Under **Repository permissions**, grant:
   - **Commit statuses: Read and write** (used by the current implementation)
   - **Metadata: Read-only** (GitHub's required baseline permission)
   - **Checks: Read and write** only if the owner separately approves the Check Runs candidate after disposable acceptance; the current implementation does not request this permission.
7. Leave all other permissions at **No access**. Do not grant Contents, Pull requests, Actions, Administration, or organization permissions. Do not add Checks permission merely to make the UI option appear; first complete the lifecycle and revocation acceptance tests below.
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

The workflow first runs an unprivileged preflight job that has **no environment attached**. Only a preflight result confirming an authorized maintainer allows the separate `authorize` job to request the protected `merge-authorizer` environment. Therefore the optional non-secret maintainer allowlist must be available to the preflight without environment access:

1. Open **Settings → Secrets and variables → Actions → Variables** (repository-level variables, not environment variables).
2. Optionally create `MERGE_AUTHORIZER_LOGINS` as a comma-separated allowlist of exact GitHub login names. If set, include the repository owner.
3. If it is absent in a user-owned repository, the trusted preflight defaults to the repository owner. For organization-owned repositories, configure an explicit allowlist.

Do not move the App Client ID or private key out of the protected environment. The allowlist contains non-secret login names; it must not contain credentials.

**Secret handling:**

- Never put the private key in a repository-level secret, source file, issue, pull request, artifact, log, or chat message.
- Do not upload the PEM file to ChatGPT or Codex.
- Keep the downloaded PEM in a secure temporary location only long enough to add the environment secret; do not leave it in Downloads, the repository, or a synced project folder.
- GitHub App private keys do not expire automatically. They must be manually rotated or revoked. Treat this as a long-lived credential and keep its access limited.
- The current workflow mints an installation token scoped to this repository with only the explicitly requested write permission `statuses:write`; GitHub's Metadata read-only baseline remains. The proposed Check Runs design additionally requires `checks:write`, but that permission is not currently granted or implemented. The token is revoked by the action after the job and expires after one hour even if not revoked.

The Actions environment is a practical least-privilege control, not a hardware-backed key vault. A dedicated key vault with signing-only access can provide stronger protection, but requires a separately reviewed integration. Do not overstate the protection provided by an Actions environment secret.

## 5. Verify the workflow before enabling the ruleset gate

Confirm the default-branch workflow:

- triggers only on `issue_comment`;
- runs maintainer preflight in a separate job with no protected environment attached;
- gates the environment-protected authorization job on the successful authorized preflight output;
- reads the optional non-secret maintainer allowlist from a repository-level Actions variable, not from the protected environment;
- checks out policy code from the default branch, not the PR head;
- does not execute PR code or workflows;
- uses `GITHUB_TOKEN` only with read permissions;
- references the App credentials only in the trusted authorization workflow;
- scopes the installation token to this repository and `permission-statuses: write`; it may request `permission-checks: write` only after the separate Check Runs design is approved and implemented;
- sets `skip-token-revoke: false`;
- pins the token action to a reviewed full commit SHA.

The expected status context is **Explicit maintainer merge authorization**. Do not infer that the App is working merely because the workflow job ran.

## 6. Publish a test status before selecting the expected source

GitHub's ruleset UI requires the App to be installed, have the required status permission, and have recently submitted a check run associated with a pre-existing required status check.

**First determine which commit SHA the pull request's ruleset evaluates.** Use the pull request's checks box and read-only API evidence:
- If GitHub says **Showing checks for the merge commit**, the required status must be published on the current test-merge commit SHA.
- If the test-merge commit has no status/check and GitHub shows checks for the latest head commit, publish on the exact PR head SHA.
- Confirm the result by checking the check runs and commit statuses for both the current head SHA and the PR's current `merge_commit_sha`. Re-evaluate after either the base or head changes; a previous SHA's success does not carry forward.

The `issue_comment` event runs from the default branch, but workflow-job checks created by an `issue_comment` workflow are not eligible to satisfy a required PR check. The restriction applies to workflow-job checks, not to a status or Check Run published directly by an external GitHub App through the REST API. The dedicated App publication must target the SHA identified above.

Therefore:

1. Use a disposable, non-production test PR with a known exact head SHA, base SHA, status-target SHA and a valid assurance record.
2. From the authorized owner account, post the exact authorization command for that test PR and full 40-character head SHA.
3. Confirm that the status **Explicit maintainer merge authorization** is published by the dedicated App on the exact status-target SHA (head or test-merge commit, as established above).
4. Open the ruleset editor and verify that the App is offered as the expected source for that exact status context.

**Stop if the App or context is not selectable.** The current workflow publishes a Commit Status. GitHub's expected-source documentation also requires the App to have recently submitted a Check Run associated with a pre-existing required status check. Creating Check Runs through the REST API requires the GitHub App permission `checks:write` ([Checks API permission requirements](https://docs.github.com/en/rest/checks/runs)). The current App intentionally requests only `statuses:write`, so it cannot create that prerequisite. Also, if a Check Run and Commit Status share the same required name, GitHub requires **both** to pass ([required-status troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)); do not assume a one-time successful Check Run can safely seed the picker while production continues updating a same-named Commit Status.

A candidate design is to publish a **new Check Run for each accepted authorization or revocation command**, on the exact SHA GitHub evaluates for the PR, with one stable required name and a unique external ID. Start the new run as `in_progress`; complete it as `success` only after all evidence and final PR/head/base/command freshness checks pass, otherwise complete it as `failure`. Do not attempt to reopen or mutate a completed Check Run. A later command must create a new run with the same required name. This relies on GitHub selecting the current same-name run within the Check Suite; duplicate-name selection and suite-conclusion aggregation are not a formal guarantee in the REST documentation and must be proven in a disposable repository. GitHub documents a 1,000 same-name run limit per Check Suite. Test that a new in-progress run supersedes a prior success, that failure can be replaced by a later success, and that the required status is evaluated as expected.

The protected-environment approval delay is a separate residual: a revoke command may wait for environment approval before the App can create its new run, leaving a previous success visible on the same head during that delay. Do not remove environment protection or expose the App key to untrusted workflows as a shortcut. Address this with a separately reviewed trusted preflight/webhook design, or explicitly retain the manual owner gate until the risk is accepted. This Check Runs design is a candidate only; it requires disposable-repository acceptance and separate explicit owner approval for `checks:write` and any live ruleset change. No permission or live ruleset change is authorized by this guide.

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
- a Check Run is accepted only from the expected App identity;
- every accepted authorization/revocation command creates a new Check Run on the exact current status-target SHA;
- a revoke command creates a new same-name Check Run whose conclusion is failure;
- a later authorization creates a new same-name Check Run whose success correctly supersedes the prior failure;
- duplicate-name Check Run selection and Check Suite conclusion aggregation behave as expected, including the 1,000-run limit;
- if Check Run creation is delayed by protected-environment approval, an older success may remain visible until the new run exists; verify that the design blocks merges during this interval or retain a manual owner gate;
- if Check Run publication/revocation is unavailable, an older success may remain; the owner must verify revocation or invalidate the old head before treating it as revoked;
- the token is revoked after the workflow job.

If any test fails or cannot be performed, record the limitation and retain a manual owner gate. Do not claim technical enforcement.

### Authorization command ordering and queue behavior

The authorization job uses one concurrency group per pull request with `queue: max` and `cancel-in-progress: false`. This prevents a later-starting workflow from canceling an authorization or revocation that is already running. GitHub permits up to 100 pending jobs in this group. Queue order is based on when jobs start waiting, not the timestamp of the issue comment, so the script independently enumerates authorized maintainer commands and accepts only the latest one before publishing a result.

A stale queued command must not authorize anything. If a command workflow is canceled, fails, or is not observed to complete, treat the command as unprocessed. In particular, do not assume a revocation succeeded merely because its comment exists: wait for the corresponding workflow to complete and verify the exact-head status is `failure`. If the queue is saturated or the status remains pending/ambiguous, do not merge; wait for the queue to clear and repeat the exact command if needed. This is a fail-closed operational requirement, not an atomic transaction guarantee.

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
- [Ruleset availability by GitHub plan](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules)
- [REST API for commit statuses](https://docs.github.com/en/rest/commits/statuses)
- [REST API for check runs](https://docs.github.com/en/rest/checks/runs)
