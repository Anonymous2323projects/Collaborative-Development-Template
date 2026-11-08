# Privacy and Public Publication Standard

## Default assumption

Everything committed here is public and may be copied, indexed, archived, or retained by third parties. A later deletion does not guarantee that a copy or Git-history object disappears.

## Personal information and contributor choice

A contributor controls whether their own name or contact details appear publicly. Do not require contributors to publish personal contact details, and do not assume that every contributor wants them hidden. Respect each person's explicit choice for their own information.

Never publish another person's real name or personal contact details without that person's explicit authorization for that exact public use. This applies equally to friends, family, collaborators, repository owners, and other contributors. A contributor's choice about their own information does not grant permission to publish someone else's.

Git commit metadata may contain an author and committer email address. Each contributor should choose and configure the address they are comfortable making public, including a platform-provided privacy address where available. Do not alter another contributor's commit identity or rewrite their history without their explicit permission. For a contributor's own historical metadata, assess the scope, practical benefit, and impact on collaborators before considering history cleanup.
- home addresses, precise location data, personal identifiers, account IDs, private profile details, or private repository URLs;
- private conversations, chat transcripts, emails, support tickets, voice recordings, or screenshots containing personal information;
- passwords, API keys, access tokens, private keys, certificates, recovery codes, session cookies, or other credentials;
- confidential employer, client, friend, family, or third-party information;
- private source code, unpublished designs, internal documents, or data without clear authorization and rights to publish.

This prohibition applies to source files, documentation, examples, filenames, commit messages, issues, pull requests, releases, logs, screenshots, image metadata, archives, and generated artifacts.

## Safe examples

- Use fictional roles such as `developer-a`, `reviewer-b`, and `assistant`.
- Use reserved example domains such as `example.com` or `.invalid`; never invent an address that could belong to a real person.
- Use obvious placeholders such as `<TOKEN>`, `<OWNER>`, and `<PROJECT>`.
- Use synthetic data that cannot reasonably be linked to a real person.
- Keep examples generic and independent of any private project.

## Before transferring an insight from another project

1. Confirm the insight is general-purpose rather than project-specific.
2. Confirm the contributor has authority to share it and that licences permit reuse.
3. Rewrite it from first principles in neutral language.
4. Remove names, identifiers, paths, URLs, distinctive configurations, conversation wording, and unnecessary contextual details.
5. Review the result as if the people involved were strangers reading a public repository.
6. Do not publish if identification or authorization is uncertain.

## Pre-commit and release review

Use automated secret/PII detection as a safety net, not as a substitute for human review. Inspect the staged diff and all release artifacts. Check image/document metadata and generated files. Review commit messages and history.

## Incident response

For containment, credential rotation, evidence preservation, Git-history remediation, privacy assessment, communication, and recovery, follow the [Incident Response Playbook](INCIDENT_RESPONSE.md).

At minimum, if sensitive information is exposed:
1. Stop further publication and notify the maintainer privately.
2. Revoke and rotate exposed credentials immediately; deleting a secret from a file does not invalidate it.
3. Assess personal-data exposure, affected people, applicable notification duties, and any contractual or legal obligations.
4. Remove exposed content from the current tree and assess Git-history cleanup and downstream copies.
5. Record the incident without reproducing the sensitive information.

Do not promise that deleting a file fully erases public exposure.
