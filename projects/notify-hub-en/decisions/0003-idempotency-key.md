---
{
  "title": "Stop duplicate sends with an idempotency key",
  "status": "Accepted",
  "date": "2026-09-09",
  "phase": "design",
  "diagrams": ["notify-sequence-en", "notify-components-en", "notify-erd-en", "notify-activity-en"]
}
---

## Context

Choosing a queue ([0001](0001-queue-between-receive-and-send.md)) made duplicates
possible. Most queues guarantee at-least-once delivery, so the same message can be
processed twice.

The same is true on the sending side. When a request times out, the service sends the
same notification again — and the earlier request may in fact have been accepted.

A user getting the same notification twice counts as a failure.

## Decision

**We defend at two points: intake and worker.** Either one alone is not enough.

### At intake — the idempotency key

The sending service attaches an `Idempotency-Key` header to every request, and the
intake API uses that key to filter duplicates. For a key it has seen, it does not queue
anything; it returns the state of the request it already accepted.

The key is enforced **by a unique constraint on the `notification` table, with no
separate store.** The intake path writes a notification row anyway. Putting the key on
that row turns "check, then insert" into a single insert, so when two requests arrive at
once only one succeeds. Something like Redis would be faster, but it opens a window
between the check and the insert, and leaves two stores that can disagree.

Retention is **90 days, the same as the delivery history**. After that, the same key is
treated as a new request. A sending service retries within seconds, not after 90 days,
and matching the history means both are deleted together.

### At the worker — a conditional state transition

The idempotency key cannot stop the queue from handing over the same message twice. That
message is already accepted, and the key check happened back at intake.

Before sending, the worker **claims the row with a conditional update**:

- `UPDATE notification SET status='Sending' WHERE id=? AND status='Queued'`
- One row updated means go ahead. Zero means another worker already took it, so this one
  moves on quietly.

On top of that, the same idempotency key is passed to the provider.

## Consequences

**What we gain** — both intake and sending are defended, and there is no new component
to operate. The duplicate check is atomic with the insert or update, so there is no race
between checking and acting.

**What it costs** — one more database round trip on the intake path, and a key index
that grows with the number of notifications.

And **this is not exactly-once.** If the provider accepted the request but the worker
dies before we record the result, the retry sends the same notification again. Channels
whose provider supports idempotency keys (push, email) filter it there, but **a channel
that does not can emit a duplicate in that window.** We accept it — the window is narrow,
and closing it needs something close to two-phase commit.

Which guarantee each channel has is written down in the operations notes, and when a
duplicate is reported, that window is the first place we look.
