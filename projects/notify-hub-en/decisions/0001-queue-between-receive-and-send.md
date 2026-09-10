---
{
  "title": "Put a queue between intake and sending",
  "status": "Accepted",
  "date": "2026-09-07",
  "phase": "design",
  "diagrams": ["notify-c4-en", "notify-deployment-en", "notify-packages-en"]
}
---

## Context

The first proposal was for the intake API to take the request, send it to the provider
right there, and return the result. That was simple, but two things bothered us.

When the push provider slows down, that latency is passed straight back to the sending
service. Order processing getting slower because of a notification was not something we
could accept. And if the provider goes down for a moment, the notifications in that
window simply disappear.

## Decision

A queue sits between intake and sending.

- The intake API puts the request on the queue and returns `202 Accepted` immediately.
  It does not wait for the send to finish.
- A send worker takes it off the queue and calls the provider.
- The intake API and the send workers scale separately.

## Consequences

**What we gain** — the sending service no longer depends on how fast the provider is.
If the provider dies, notifications wait in the queue and go out later. When traffic
spikes, we add workers.

**What it costs** — the sending service cannot learn from the response whether the send
succeeded; if it needs to know, it has to query the history. There is one more thing to
operate, and when the queue backs up notifications arrive late — a new state that is
neither success nor failure, just **late**.

Queue depth is something we watch. Noticing a backlog too late means users get a
notification long after the moment it was about.
