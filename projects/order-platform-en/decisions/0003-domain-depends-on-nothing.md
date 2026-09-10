---
{
  "title": "The domain depends on nothing",
  "status": "Accepted",
  "date": "2026-09-04",
  "phase": "design",
  "diagrams": ["package-deps-en", "order-class-en"]
}
---

## Context

Testing the order calculation rules meant standing up the database and the payment
gateway, because the domain classes referenced JPA annotations and an HTTP client
directly.

A test that checked one rule took seconds, so nobody wrote many tests for the rules.

## Decision

Dependencies point one way only — inward, toward the domain.

- `domain` imports no other package. That includes frameworks.
- When the domain needs the outside world, it defines a **port** (an interface) inside
  the domain, and `infrastructure` implements it.
- `web` knows `application`, and `application` knows `domain`. Never the reverse.

## Consequences

**What we gain** — testing a domain rule needs neither Spring nor a database. Swapping
persistence or an external API leaves the domain untouched.

**What it costs** — one more layer of indirection, ports and adapters. Adding one store
means writing an interface and an implementation together, which reads to a newcomer as
"why am I writing this twice".

In the `Package dependencies` diagram, the fact that no arrow leaves `domain` **is**
this decision.
