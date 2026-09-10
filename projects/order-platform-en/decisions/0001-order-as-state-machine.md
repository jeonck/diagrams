---
{
  "title": "Treat an order as a state machine",
  "status": "Accepted",
  "date": "2026-09-02",
  "phase": "analysis",
  "diagrams": ["order-state-en", "order-class-en"]
}
---

## Context

An order moves between placed, paid, preparing, shipping and cancelled. The first
implementation kept a `status` string field and branched on it wherever it mattered:
`if (order.status == "paid")`.

Once those branches passed ten, two things surfaced. Nowhere in the code did it say
which state may follow which. And a bug where a shipping order fell back to awaiting
payment went through review without anyone catching it.

## Decision

Order states and transitions are an explicit state machine.

- The allowed transitions are declared in one place, and every transition goes through
  that table.
- Each transition is named after the **event** that causes it: `payment approved`,
  `dispatched`, `cancelled by customer`.
- A transition that is not allowed raises. It is never ignored quietly.

## Consequences

**What we gain** — the possible states and transitions fit on one picture. Adding a
state makes any transition you forgot show up at compile time or in a test. An invalid
transition never reaches the data.

**What it costs** — code that changes state takes one more hop. Adding a state means
editing the transition table and its callers together, which is more work than changing
a single field used to be.

The `Order state transitions` diagram is that table, drawn. If the diagram and the
table disagree, the table is right.
