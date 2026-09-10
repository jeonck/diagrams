---
{
  "title": "Retry with exponential backoff five times, then DLQ",
  "status": "Accepted",
  "date": "2026-09-08",
  "phase": "design",
  "diagrams": ["notify-state-en", "notify-activity-en", "notify-bpmn-en"]
}
---

## Context

Most provider errors were transient — send it again a few seconds later and it works.
But mixed in were failures that never succeed no matter how often we try, like an
invalid token. Retrying those forever ties a worker to that one job.

## Decision

A failed send is retried with exponential backoff, with a cap on the number of attempts.

- The interval starts at 1 second and doubles. Five attempts at most.
- Past five, the message goes to the DLQ (dead-letter queue) and we give up on it.
- Giving up is recorded too. Nothing disappears quietly.

## Consequences

**What we gain** — transient errors recover without a person. A permanent failure does
not hold a worker. What piles up in the DLQ shows which failures are structural.

**What it costs** — five is a weakly founded number. All we have today is that observed
transient errors usually recover within three attempts, and we will revisit it in
operation. Backoff also means the last attempt lands more than 30 seconds in, and for
an urgent notification that delay may be the problem.

Who checks the DLQ, and when, is not decided yet.
