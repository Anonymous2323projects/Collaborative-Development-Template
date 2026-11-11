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
5. The maintainer makes the final decision after considering feedback and the project's capacity. For a single-maintainer project, require a separate explicit exact-head owner decision without inventing a second human reviewer. Unless a separate technical gate is verified live, this remains a manual procedural step. Never treat an AI review or successful CI as owner authorization.
6. Record durable decisions in the relevant project documentation or changelog; do not duplicate the same decision across multiple files.

## Changes requiring particular care

Changes to privacy boundaries, security policy, licensing, contribution terms, default project instructions, or release/update behavior require explicit rationale and careful review. Do not weaken safeguards merely to improve convenience or a security score.

## Merge protection and exact-head authorization

Where supported, protect the default branch with pull requests, relevant checks, review-thread resolution, and deletion/force-push restrictions. Verify required check origins, strict up-to-date settings, and bypass actors live; do not infer enforcement from a policy document. Where a second human reviewer is unavailable, record the owner's explicit decision for the exact PR head SHA and recheck the head and base immediately before merging. This template does not provide a technically enforced owner-authorization gate.

## Releases and compatibility

The repository is a documentation and workflow template, not a packaged application. Releases are therefore optional milestones, not a prerequisite for using the template. When a release is published, it must identify the source commit, summarize user-visible changes, call out migration or compatibility implications, and link to the changelog. Do not imply that a release has been published when only a commit or tag exists.

## Conflict of interest and moderation

The maintainer should disclose material conflicts when practical and may decline contributions that cannot be safely or responsibly maintained. Community concerns are handled under [the Code of Conduct](CODE_OF_CONDUCT.md).

## Governance changes

This document may evolve through a focused pull request. Material changes to maintainer authority, contribution rights, or user expectations must be clearly described before adoption.
