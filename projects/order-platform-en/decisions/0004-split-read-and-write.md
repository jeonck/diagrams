---
{
  "title": "Split reads from writes",
  "status": "Accepted",
  "date": "2026-09-05",
  "phase": "operations",
  "diagrams": ["deployment-topology-en", "network-topology-en"]
}
---

## Context

Order listings and product lookups make up most of our queries, and they were competing
for the same database instance as order creation. At peak selling hours, read latency
dragged payment processing down with it.

## Decision

The database is split into one primary and read replicas, and the application picks the
destination.

- Every write goes to the primary.
- Reads go to a replica.
- Except **reading back something you just wrote**, which goes to the primary.

## Consequences

**What we gain** — read load no longer gets in the way of the write path. When reads
grow, we add replicas.

**What it costs** — replication lag is a new failure mode. The bug where an order is
missing from the list right after you place it is hard to reproduce and shows up only
where someone missed the exception above. Deciding which reads fall under that
exception is a judgement call a person has to make.

In the `Web service deployment` diagram, the app server drawing separate arrows to the
primary and to the replica **is** this decision.
