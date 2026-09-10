---
{
  "title": "Keep the session in app-server memory",
  "status": "Superseded",
  "date": "2026-09-03",
  "phase": "operations",
  "supersededBy": "0005-session-in-redis",
  "diagrams": []
}
---

## Context

We had to decide where the login session lives. At the time there was a single app
server, and running one more datastore looked like work without a reason.

## Decision

The session lives in the app-server process memory.

## Consequences

**What we gain** — one less thing to operate, and no network round trip to read a session.

**What it costs** — restarting an app server logs everyone out. Adding servers requires
sticky sessions on the load balancer.

## Why this was superseded

Going to three app servers broke the premise. See
[0005 Move the session to Redis](0005-session-in-redis.md).
