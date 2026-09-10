---
{
  "title": "Move the session to Redis",
  "status": "Accepted",
  "date": "2026-09-06",
  "phase": "operations",
  "supersedes": "0002-session-in-app-memory",
  "diagrams": ["deployment-topology-en"]
}
---

## Context

Going to three app servers broke the premise of
[0002](0002-session-in-app-memory.md). Sticky sessions carried us for a while, but two
problems stayed. Every deploy logged out whoever was pinned to that server, and when
autoscaling removed a server its sessions went with it.

Sticky sessions did not spread load evenly either. The one server that happened to hold
the long-lived users stayed busy.

## Decision

The session lives in Redis, and app servers hold no state.

- Sticky sessions are turned off on the load balancer.
- Any app server handles any request identically.

## Consequences

**What we gain** — deploys and autoscaling no longer touch logins. Load spreads evenly.
Adding an app server becomes a change of one number.

**What it costs** — one more thing to operate, and if Redis dies everyone is logged out.
Every session lookup adds a network round trip.

Leaving Redis as a single point of failure is something we accept at this size. We will
revisit replication when a mass logout costs more than it does today.
