# Project Governance

## Purpose

This document explains how the Collaborative Development Template is maintained and how decisions are made. It is intentionally lightweight and suitable for a small, maintainer-led project.

## Roles

- **Maintainer:** The repository owner is responsible for project direction, releases, security response, moderation, and final repository decisions.
- **Contributors:** Anyone may propose improvements through issues or pull requests. Contribution does not imply decision-making authority or maintainer status.
- **Reviewers:** A reviewer may provide technical or editorial feedback. A review is advisory unless repository settings explicitly make it a merge requirement.

## Decision process

1. Prefer evidence, user impact, safety, legal solidity, usability, trust, and freedom—in that priority order.
2. Research relevant standards and existing solutions before adding new mechanisms or dependencies.
3. Keep changes focused, explain material trade-offs, and preserve backwards compatibility where practical.
4. Use pull requests for substantive changes so the rationale and validation remain visible. Apply [Change, Review, and Merge Assurance](MERGE_AND_CHANGE_ASSURANCE.md), including the five perspectives, PR-specific evidence, and live technical-gate verification.
5. The maintainer makes the final decision after considering feedback and the project's capacity. For a single-maintainer project, use a platform-enforced exact-head owner authorization rather than an impossible self-review requirement. Never treat an AI review or successful CI as owner authorization.
6. Record durable decisions in the relevant project documentation or changelog; do not duplicate the same decision across multiple files.

## Changes requiring particular care

Changes to privacy boundaries, security policy, licensing, contribution terms, default project instructions, or release/update behavior require explicit rationale and careful review. Do not weaken safeguards merely to improve convenience or a security score.

## Merge protection and exact-head authorization

The default branch should have an active ruleset that requires pull requests, relevant status checks, resolved review threads, and blocks deletion/force-push. Configure required check names against their trusted integration and require the branch to be up to date. Keep bypass actors empty unless a narrowly justified emergency path is documented and audited. Where no second human reviewer is available, a maintainer authorization should be bound to the exact PR head SHA; any new commit requires a new authorization. Verify the live ruleset rather than relying on this text.

## Releases and compatibility

The repository is a documentation and workflow template, not a packaged application. Releases are therefore optional milestones, not a prerequisite for using the template. When a release is published, it must identify the source commit, summarize user-visible changes, call out migration or compatibility implications, and link to the changelog. Do not imply that a release has been published when only a commit or tag exists.

## Conflict of interest and moderation

The maintainer should disclose material conflicts when practical and may decline contributions that cannot be safely or responsibly maintained. Community concerns are handled under [the Code of Conduct](CODE_OF_CONDUCT.md).

## Governance changes

This document may evolve through a focused pull request. Material changes to maintainer authority, contribution rights, or user expectations must be clearly described before adoption.
