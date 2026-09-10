---
{
  "title": "One human approval, right before production",
  "status": "Accepted",
  "date": "2026-09-08",
  "phase": "operations",
  "diagrams": ["cicd-pipeline-en"],
  "basis": ["value-stream-en"]
}
---

## Context

Deploying entirely by hand pushed us into batching several changes into one release,
and when something broke it was hard to tell which change caused it.

The opposite proposal — automate the whole way through — was on the table too. But this
service touches payments and inventory, and shipping to production with nobody looking
was more than the team was ready to accept.

## Decision

The pipeline runs automatically, with a human approval at **exactly one point**: right
before the production deploy.

- Build, test, image, staging deploy and integration tests all run without approval.
- The approval answers one question — "do we ship this change now?" It is not a second
  code review.
- Everything after the approval is automatic again. No one touches the rolling deploy
  or the health checks.

## Consequences

**What we gain** — we can ship one change at a time, which makes the cause of a problem
much easier to narrow down. A person steps in only at the risky moment.

**What it costs** — the approval becomes the bottleneck in lead time. As the
`Order feature value stream` shows, waiting already accounts for most of lead time, and
waiting for an approval is one more piece of it. When the approver is away, deploys stop.

Removing the approval is a conversation for after we have evidence that our deploy
failure rate is low enough.
