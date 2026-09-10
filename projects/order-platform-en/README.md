# Online Store (order-platform-en)

> A **fictional project**, here to show the diagram notation and the structure of this
> repository. It is not a real service, and the names and numbers are invented to make
> the explanation work.
>
> This is the English edition of [`order-platform`](../order-platform/README.md). Same
> product, same decisions, written for English readers.

A commerce backend: a customer orders a product and pays, the system draws down
inventory and hands the parcel to shipping.

## Scope

**In** — product search, cart, order creation, payment approval, inventory drawdown,
handing off to shipping, cancellation and refund

**Out** — settlement, promotions and coupons, customer support, recommendations,
multi-region and multi-currency

Payment and email are not built here; they are external systems
(see [C4 context & container](diagrams/c4-container-en/diagram.html)).

## Design decisions

Each one is kept as an ADR under [`decisions/`](decisions).

- **An order is a state machine.** Instead of a status field branched on everywhere, the
  transitions and the events that cause them are explicit.
  [ADR 0001](decisions/0001-order-as-state-machine.md) · [Order state transitions](diagrams/order-state-en/diagram.html)
- **The domain depends on nothing.** Persistence and external APIs implement ports that
  the domain defines.
  [ADR 0003](decisions/0003-domain-depends-on-nothing.md) · [Package dependencies](diagrams/package-deps-en/diagram.html)
- **Reads are split from writes.** Writes go to the primary, reads to a replica.
  [ADR 0004](decisions/0004-split-read-and-write.md) · [Web service deployment](diagrams/deployment-topology-en/diagram.html)
- **A person only presses approve.** Apart from one approval before the production
  deploy, the pipeline is fully automatic.
  [ADR 0006](decisions/0006-manual-approval-before-production.md) · [CI/CD pipeline](diagrams/cicd-pipeline-en/diagram.html)

## One order, seen from several angles

Every diagram in this project draws the same order domain, so understanding one makes
the next easier to read — the same `Order` appears

- in the [ERD](diagrams/order-erd-en/diagram.html) as tables and foreign keys,
- in the [class diagram](diagrams/order-class-en/diagram.html) as responsibilities and composition,
- in the [state transitions](diagrams/order-state-en/diagram.html) as states and events,
- in the [BPMN](diagrams/fulfillment-bpmn-en/diagram.html) as work crossing departments.

The full list is in the [repository README](../../README.md#다이어그램-목록).
