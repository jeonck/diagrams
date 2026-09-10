# Notification Hub (notify-hub-en)

> A **fictional project**, here to show the structure of this repository. It is not a
> real service.
>
> This is the English edition of [`notify-hub`](../notify-hub/README.md).

A shared internal platform that takes events from other services and sends them out as
push, email and SMS. [Online Store](../order-platform-en/README.md) is its first sending
service.

## Design complete

All fifteen representative kinds are drawn, and all three decisions are `Accepted`.
Running `node tools/build-index.mjs` reports nothing left to draw.

The [sequence diagram](diagrams/notify-sequence-en/diagram.html), which we picked as the
first thing to draw, is what narrowed the question in
[0003 Idempotency key](decisions/0003-idempotency-key.md) — the picture showed which
window the key covers (②) and which it does not, and the answer was to put the worker's
**conditional claim (⑤)** in that gap. When the decision settled, the
[sequence](diagrams/notify-sequence-en/diagram.html),
[activity](diagrams/notify-activity-en/diagram.html) and
[ERD](diagrams/notify-erd-en/diagram.html) all changed with it.

It is still **not exactly-once**. A window remains where the provider has the request but
the worker dies before recording the result, and on a channel whose provider has no
idempotency key a duplicate can go out. That is accepted, and the ADR says so.

## Scope

**In** — accepting notification requests, sending per channel (push, email, SMS), retry
and giving up, delivery history, per-user channel preferences

**Out** — a tool for writing notification copy, A/B testing, billing by volume, user
segments

## Design decisions

- **A queue sits between intake and sending** — so the sending service is not tied to
  the provider's speed.
  [ADR 0001](decisions/0001-queue-between-receive-and-send.md) ·
  [C4](diagrams/notify-c4-en/diagram.html)
- **Retry with exponential backoff five times, then DLQ** — transient errors recover on
  their own, and permanent failures do not hold a worker.
  [ADR 0002](decisions/0002-retry-with-backoff-then-dlq.md) ·
  [State transitions](diagrams/notify-state-en/diagram.html)
- **An idempotency key stops duplicate sends** — a unique constraint at intake, a
  conditional claim at the worker. No new store.
  [ADR 0003](decisions/0003-idempotency-key.md) ·
  [Send sequence](diagrams/notify-sequence-en/diagram.html) ·
  [Retry activity](diagrams/notify-activity-en/diagram.html)
