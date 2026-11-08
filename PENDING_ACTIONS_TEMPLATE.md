# Pending Actions

Use this register only when a project has meaningful actions that require a person, a decision, external access, or later verification. If the project already has a suitable issue tracker or action list, use that and record its location in `PROJECT_MEMORY.md`. **Do not create an empty register.**

This file records actions; it does not send notifications.

## How ChatGPT should use it

1. Explain why an action is needed and what it unlocks. Offer to guide the user through it now or defer it.
2. If it remains outstanding after the current interaction, record it here. If the user completes it now, record the result and evidence.
3. Mark safety, privacy, security, legal, data-loss, and irreversible-risk checks as **critical**. Pause the affected operation until resolved.
4. Mark work that genuinely depends on the action as **blocking**. Continue unrelated work.
5. Mark useful but non-essential checks as **non-blocking**. Raise them at a relevant checkpoint; do not nag.
6. Reuse completed evidence while the relevant code, settings, environment, and requirements remain unchanged.
7. Do not create external tickets, messages, scheduled tasks, or notifications without authorization. This register does not create reminders.
8. Close completed, cancelled, or superseded actions with a short outcome. Do not silently erase useful history.

## Open actions

| ID | Exact action | Why it matters | Priority | Status | Owner | Next review trigger | Evidence / outcome |
|---|---|---|---|---|---|---|---|
| <ID> | <CLEAR STEP> | <WHAT IT UNLOCKS> | <critical / blocking / non-blocking> | <open / deferred / in progress / blocked> | <USER / AI / OTHER> | <DATE OR EVENT> | <LINK / NONE> |

## Closed actions

Keep a short record only when the outcome may matter later.

| ID | Outcome | Closed date | Evidence / reason |
|---|---|---|---|
| <ID> | <RESULT> | <DATE> | <LINK / REASON> |

## Review

At a new session or handover, check open actions against the live project, close stale items, identify what is actually blocked, and update evidence. Ask only for the smallest human action that genuinely matters.
