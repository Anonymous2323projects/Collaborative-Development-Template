# Repository Settings Checklist

> Maintainer-only operational checklist. This file is not part of the downstream starter pack.

This repository is a public GitHub Template Repository. File changes alone cannot configure GitHub repository settings; verify each item in the live repository settings and record the date/evidence in the maintainer handover.

## Verified baseline

Last checked against GitHub repository metadata on 2026-11-08:

- [x] Repository is public.
- [x] Default branch is `main`.
- [x] GitHub Template Repository is enabled.
- [x] Issues and pull requests are enabled.
- [ ] Repository description is set — API currently reports no description.
- [ ] Relevant repository topics are set — API currently reports no topics.
- [ ] Main branch protection is enabled — branch API reported `protected: false`; no repository rulesets were returned. Recheck in Settings because API permissions and endpoint visibility can affect verification.
- [ ] A GitHub Release has been published — no releases were returned. This is optional until a deliberate stable milestone is ready.

## Recommended repository metadata

Suggested description:

> A ChatGPT-first, privacy-first template for structured collaborative software development, with durable project memory and GitHub-based workflows.

Suggested topics (choose the closest supported labels):

- `chatgpt`
- `ai-assisted-development`
- `software-development`
- `project-template`
- `open-source`
- `privacy`
- `developer-tools`

Keep the description factual. Do not claim certification, guaranteed security, or universal compatibility.

## Main branch protection

GitHub documents protected branches and rulesets as available for public repositories on GitHub Free. Configure protection for `main` in **Settings → Branches** (or **Settings → Rules → Rulesets**, depending on the interface):

1. Require changes to enter through a pull request.
2. Require the repository's actual CI status checks to pass. Select the exact check names shown by GitHub after a successful workflow run; do not guess them.
3. Require conversation resolution if review conversations are used.
4. Block force pushes and branch deletion.
5. Do not require an approving review while there is only one maintainer who cannot provide an independent review. Add at least one approval when there are multiple active maintainers/reviewers and the project can enforce it without blocking all changes.
6. Keep an intentional administrator recovery/bypass path to avoid locking out the sole maintainer; document any bypass.

Do not treat branch protection as a substitute for review or the repository's explicit authorization rules. Recheck after workflow job names change because required status checks are name-sensitive.

Official references: [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) and [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

## Security and Actions settings

- Confirm Actions are enabled for the repository.
- Set the default `GITHUB_TOKEN` permission to read-only where possible.
- Keep each workflow's explicit permissions minimal.
- Require full-length SHA pinning for Actions if the repository's Actions policy offers that control.
- Keep Dependabot enabled for GitHub Actions; review updates rather than merging them blindly.
- Keep Gitleaks workflow results visible and investigate failures. A CI scan is not equivalent to GitHub Secret Protection, push protection, or a complete secret audit.
- Enable secret scanning and push protection where the plan and repository ownership type support them. Public repositories receive GitHub secret scanning for free; private-repository availability depends on plan and ownership.
- Confirm private vulnerability reporting is enabled only if the maintainer is ready to receive and triage reports.

References: [Actions workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [secure use](https://docs.github.com/en/actions/reference/security/secure-use), and [secret-scanning availability](https://docs.github.com/en/code-security/concepts/secret-security/about-alerts).

## Releases

Do not create a release merely to populate the Releases page. When a stable, useful template milestone is ready:

1. Review the changelog and all public files.
2. Choose a version and create an annotated tag from the exact reviewed commit.
3. Publish GitHub release notes using `.github/release.yml` as the category template.
4. State compatibility implications and any manual migration steps.
5. Link the release and source commit in the maintainer handover.

The repository is a documentation/workflow template, so signed binary artifacts and SBOM generation are not automatically proportionate requirements. Reassess if distributable software or release artifacts are introduced.
