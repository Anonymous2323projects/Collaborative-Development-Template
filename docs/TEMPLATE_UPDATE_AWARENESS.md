# Template Update Awareness and Adoption

## Purpose and scope

A repository created from a GitHub template is a snapshot. It does not automatically receive later changes to the source template. Projects therefore need a lightweight, user-controlled way to discover relevant upstream improvements without silently importing changes or losing local work.

This policy covers **awareness and adoption of changes to the Collaborative Development Template**. It complements, but does not replace, [the Update and Release Security Policy](../UPDATE_AND_RELEASE_SECURITY.md), which governs software update mechanisms and release artifacts.

## Core rule: notify, explain, offer — never silently apply

The assistant or project tooling may check whether a newer template version exists and may present an update proposal. It must not, merely because an update exists:

- push, pull, merge, cherry-pick, rebase, overwrite, or delete project files or branches;
- change the project's instructions, security controls, dependencies, settings, or data;
- install or execute downloaded code;
- imply that a template update is mandatory when it is only recommended.

The user decides whether and when to adopt an update. A clear, specific approval to apply a reviewed update authorizes only the described scope. Any material scope expansion, destructive action, permission change, or external side effect requires separate approval.

## Establish the installed baseline

When a project is created from this template, record its source and starting point using [the Template Update Record](../TEMPLATE_UPDATE_RECORD_TEMPLATE.md), or an equivalent existing project record.

Record at least:

- source repository URL;
- source release/tag, if one was used;
- exact source commit SHA used to create the project;
- date the template was applied;
- last upstream check date and checked commit/release;
- known local customizations or files that must not be overwritten.

Do not guess the starting commit after the fact. If it is unknown, mark it unknown and establish a new baseline only with the user's agreement. Keep this record in the downstream project, not in the template repository itself.

## When and how to check

Use a proportionate, Free-compatible baseline:

1. At project bootstrap, record the source baseline.
2. At the start of a substantial new work session, or at a meaningful maintenance/release checkpoint, check the source repository if current GitHub access is available.
3. If no check has been made for about 30 days and the user is actively working on the project, raise an upstream check at the next useful checkpoint. This is a review interval, not a promise of background monitoring.
4. Where available, users may independently enable GitHub repository notifications using **Watch → Custom → Releases**. This is optional and does not grant the assistant repository write access.
5. Scheduled or event-triggered monitoring may be used only when supported, configured, and explicitly authorized. It is never required for Free-plan compatibility.

Check the latest stable GitHub Release first. If the source repository does not publish stable releases, compare the recorded commit with the current default branch and clearly label the result as **unreleased upstream changes**, not as a stable release. Do not treat an arbitrary branch head, pull request, or unreviewed commit as a published release.

If GitHub cannot be reached, say that the update status is unknown. Do not report “up to date” based on stale data.

## What an update notice must contain

A useful notice should state:

- installed source release/commit and date, if known;
- latest stable release or checked default-branch commit, plus check date;
- whether the changes are released or still unreleased;
- a concise summary of relevant changes and affected files;
- classification: security-critical, security-recommended, compatibility/legal, functional, documentation-only, or not relevant;
- material compatibility, migration, privacy, licence, or operational risks;
- whether local customizations may conflict;
- a recommended action and why;
- clear choices: review the diff, apply the agreed changes, defer, or dismiss.

Do not overwhelm users with unrelated upstream changes. Explain why a change matters to this project and identify anything that needs human judgment.

## Safe adoption workflow

When the user asks to proceed:

1. Confirm the upstream source, release/commit, and exact proposed scope.
2. Fetch and inspect the relevant upstream diff and files; do not trust release descriptions alone.
3. Check provenance, commit/release authenticity where supported, licences, security implications, and any linked advisories.
4. Compare upstream changes with the downstream project's current files and local customizations.
5. Prepare a backup or recoverable Git checkpoint where appropriate.
6. Apply only the reviewed, relevant changes on a dedicated branch or equivalent isolated working copy.
7. Preserve project-specific decisions and customizations. Resolve conflicts deliberately; never replace a whole file merely because the upstream version is newer.
8. Run relevant tests, security checks, and documentation/link checks.
9. Present the diff, test evidence, unresolved risks, and rollback path.
10. Leave merge/push to the user's explicit authorization and the project's normal review process.

For a documentation-only template update, a focused patch or pull request is normally preferable to copying the entire upstream repository. A downstream project may intentionally diverge from the template; do not erase that independence.

## Emergency update notice — the “break-glass” path

An emergency notice is a **high-priority warning and decision path**, not a remote-control channel.

Use it only when credible evidence indicates an actively exploited vulnerability, a compromised release/source channel, a severe legal or safety issue, or another imminent material risk. The notice must identify:

- the evidence and source, affected versions/commits, and confidence level;
- the actual impact and exposure, without overstating unverified claims;
- the narrowest safe immediate mitigation;
- whether a verified fix exists and how its authenticity was checked;
- what happens if the user defers, including any justified service/support consequences;
- the recovery or rollback route and any known rollback risks.

The assistant should surface a credible emergency promptly at the next interaction in which it can communicate. It must not claim continuous monitoring or guarantee that a user will be notified while offline.

**No emergency notice authorizes an automatic push, merge, overwrite, install, or data migration.** The user must explicitly authorize the proposed action. If the affected project's own documented incident plan permits an operator to disable a vulnerable feature or isolate a service, follow that plan and its authorization model; do not invent such authority from this template. Never install an unverified replacement. If no trustworthy fix exists, recommend the narrowest safe containment and explain the uncertainty.

The existing [Update and Release Security Policy](../UPDATE_AND_RELEASE_SECURITY.md) governs any actual software updater, emergency version block, signed artifact, or installation process. A GitHub template update notice is not itself a secure software updater.

## Legal and regulatory applicability

This template provides an engineering and governance baseline, not a guarantee of legal compliance or legal advice. Before distributing a product, determine which rules apply to its product category, role in the supply chain, users, territory, contract, and deployment model.

Examples that may be relevant in the EU include:

- **Cyber Resilience Act (Regulation (EU) 2024/2847):** obligations depend on whether the offering is a product with digital elements and on the responsible economic operator and applicable provisions. The main obligations apply from 11 December 2027; vulnerability/incident reporting obligations began applying on 11 September 2026. Among other things, the Regulation addresses vulnerability handling, support periods, and the availability of security updates. Do not assume every repository template or every project automatically falls within its scope.
- **Digital Content Directive (Directive (EU) 2019/770):** for covered consumer contracts for digital content or digital services, traders must inform consumers of and supply updates, including security updates, needed to maintain conformity for the relevant period. A consumer's failure to install an update affects liability only under the Directive's stated conditions; this is not a general permission for silent forced installation.

Check the current consolidated legislation and national implementation, contractual terms, exceptions, and authoritative guidance for the actual product. Obtain qualified legal advice where the consequences or scope warrant it. Never market this template as “legally watertight” or claim that following it guarantees compliance.

Primary sources:
- EU Cyber Resilience Act: https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32024R2847
- EU Digital Content Directive: https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32019L0770
- The Update Framework: https://theupdateframework.io/

## Acceptance criteria

- [ ] A downstream project can identify the exact template baseline or explicitly record it as unknown.
- [ ] An assistant checks upstream status at appropriate project checkpoints when access is available, without requiring paid automation.
- [ ] Stable releases are distinguished from unreleased default-branch changes.
- [ ] An update notice explains relevance, impact, risks, and choices.
- [ ] No update is silently pushed, merged, installed, or applied.
- [ ] Local customizations and project-specific decisions are preserved.
- [ ] Adoption uses a reviewable branch/patch and appropriate validation.
- [ ] Emergency notices are evidence-based, proportionate, and separate from automatic installation.
- [ ] If access or monitoring is unavailable, the limitation is disclosed and no false “up to date” claim is made.
