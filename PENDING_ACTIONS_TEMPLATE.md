# Pending Actions and Human Follow-up

Use this file as the durable register of actions that require a human, a decision, external access, or later verification. It complements `PROJECT_MEMORY.md`; it is not a chat transcript, general task backlog, or substitute for issue tracking.

For projects using the Collaborative Development Template, initialize this file from this template when there are meaningful human-dependent actions. Keep it concise. If the project already has a suitable canonical issue tracker or action register, use that instead and record its location in `PROJECT_MEMORY.md`.

## Operating rules for ChatGPT

1. At the start of each ChatGPT work session, before substantial handovers, and whenever work approaches a recorded dependency, read this register and check whether entries are still current.
2. When user testing, a human decision, account access, physical action, or other user-dependent step is needed, explain exactly why and what it unlocks. Offer to walk through it one step at a time or defer it.
3. If deferred, record the action here immediately. Do not rely on chat history or model memory as the only record. If the user chooses to do it now, guide one step at a time and update the entry when completed.
4. Classify the impact:
   - **Critical blocker:** safety, privacy, security, legal, data-loss, or irreversible-risk validation. Stop the affected operation until resolved.
   - **Blocking:** dependent work cannot be completed reliably without this action. Pause only that dependent work; continue independent work.
   - **Non-blocking:** useful validation or feedback that does not prevent safe progress. Continue autonomously and remind proportionately.
5. Do not make the user repeat actions or re-test unchanged behavior. Check existing evidence first. Reopen a completed action only when relevant code, configuration, environment, or requirements have changed.
6. Remind without nagging. Surface critical blockers immediately, blocking actions when the dependent work is next, and non-blocking actions at a meaningful checkpoint or the agreed reminder interval. Respect a user's request to postpone or stop reminders.
7. Never claim that a reminder will arrive later unless a scheduled reminder or monitoring task was actually created and confirmed. ChatGPT scheduled tasks are optional delivery mechanisms, not the source of truth. Check their availability and limitations; project files may not be accessible to tasks created inside a ChatGPT Project.
8. Do not create scheduled tasks, notifications, external tickets, or messages without the user's authorization. A user agreeing to defer an action authorizes recording it, not necessarily creating an external notification.
9. When an action is completed, record the outcome and evidence, then mark it completed. If it is cancelled or no longer relevant, record why and close it. Review stale entries instead of silently deleting useful history.
10. Keep user effort minimal. Ask only for the smallest action or decision that genuinely blocks progress. Do not turn every optional check into a gate.

## Status and priority vocabulary

- Priority: `critical`, `blocking`, `non-blocking`
- Status: `open`, `deferred`, `in-progress`, `blocked`, `completed`, `cancelled`, `superseded`
- Reminder cadence: `immediate`, `next relevant session`, `milestone`, `weekly`, `monthly`, or a user-agreed schedule.

## Open actions

| ID | Action / exact user step | Why it matters / what it unlocks | Priority | Status | Owner | Due / revisit | Last surfaced | Evidence / outcome |
|---|---|---|---|---|---|---|---|---|
| PA-001 | <CLEAR ACTION> | <DEPENDENCY OR BENEFIT> | <PRIORITY> | <STATUS> | <USER / AI / OTHER> | <DATE OR TRIGGER> | <DATE> | <LINK OR NONE> |

## Reminder preferences

- Preferred cadence: <USER-AGREED CADENCE OR "ASK WHEN FIRST DEFERRING">
- Step-by-step guidance: <OFFER WHEN ACTION IS SUITABLE>
- Quiet periods / do-not-remind constraints: <NONE OR USER-DEFINED>
- External scheduled reminders: <NOT REQUESTED / AUTHORIZED / ACTIVE WITH VERIFIED DETAILS>

## Closed actions

Move completed, cancelled, or superseded items here when a short audit trail is useful. Keep only enough history to explain the outcome and avoid reopening settled work.

| ID | Outcome | Closed date | Evidence / reason |
|---|---|---|---|
| <ID> | <OUTCOME> | <DATE> | <LINK OR REASON> |

---

## Session review checklist

- [ ] Read current project memory, handover, and this action register.
- [ ] Verify open actions against the live project state; close stale or already-completed items.
- [ ] Identify which work is genuinely blocked and which work can continue independently.
- [ ] Surface only the most relevant reminder(s), with a step-by-step or defer option when appropriate.
- [ ] Update statuses, evidence, and next reminder trigger after user interaction or verification.
- [ ] Reconcile the register before handing work to another session or assistant.
