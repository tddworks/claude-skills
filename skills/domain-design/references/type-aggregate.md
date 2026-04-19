# Aggregate

**Best for:** one aggregate root and the entities, value objects, invariants, commands, and events that live inside its consistency boundary.

An Aggregate diagram is the single most useful domain artifact per square inch. It forces naming (one root, named children), surfaces rules (the invariants band), and bounds scope (everything outside is drawn faint or external).

## DDD vocabulary reminder

- **Aggregate root** — the entity that is the single entry point to the cluster. External code holds references to the root, never to inner entities.
- **Entity** — has identity (an ID). Inside the aggregate, an entity is owned by the root.
- **Value object** — no identity. Replaced whole, never mutated in place. Defined by its fields.
- **Invariant** — a rule that must always be true for the aggregate (across all its members) inside a transaction.
- **Command** — a request to change state, named in imperative (`PlaceOrder`, `CancelSubscription`).
- **Domain event** — a fact that happened, named in past tense (`OrderPlaced`, `SubscriptionCancelled`).

## Layout conventions

**Top band — header**

- Eyebrow: `AGGREGATE · <context name>` (Geist Mono, uppercase, tracked).
- H1 title: the aggregate root name (Instrument Serif).

**Middle — the aggregate itself**

- **One aggregate root box, centered, coral fill (`accent-tint`) and coral stroke (`accent`).** This is the only focal element — never give a child the coral treatment.
- **Entities** to one side (usually left): white fill, ink stroke, role tag `ENTITY`.
- **Value objects** to the other side: `ink @ 0.05` fill, muted stroke, role tag `VO`.
- Each child shows 2–5 key fields in Geist Mono sublabel — not the full list. Skip the type signatures unless the types encode a domain rule (e.g. `Money`, `EmailAddress`).
- Use plain lines (no arrow heads) between root and children — containment, not direction. Optionally annotate the line with cardinality (`1`, `0..*`, `1..*`).

**Bottom band — behaviour**

Three horizontal strips, each labelled with a small eyebrow:

1. **Commands** — blue-tinted boxes (`CMD`), verbs in imperative. These are the *allowed intentions* a client may express against the aggregate.
2. **Events** — yellow-tinted boxes (`EVENT`), nouns in past tense. These are the facts the aggregate *emits* after it processes a command.
3. **Invariants** — plain text list, one per line, Geist sans italic, prefixed with `·`. Short English sentences, never code.

Optional top-right **Actor / Persona** pill — who initiates commands against this aggregate (`Customer`, `BillingSystem`, `OpsAdmin`).

## Example layout

```
┌─ AGGREGATE · BILLING ─────────────────────────────────────────┐
│                                                                │
│                       Subscription                             │
│                    ┌───────────────┐                           │
│          1         │ [AGG ROOT]    │         1..*              │
│    Entity ─────────│  Subscription │───────── VO               │
│                    │  id, plan,    │                           │
│                    │  status       │                           │
│                    └───────────────┘                           │
│    ┌────────┐                                 ┌────────┐       │
│    │ENTITY  │                                 │  VO    │       │
│    │Invoice │                                 │ Money  │       │
│    │ id,    │                                 │ amount,│       │
│    │ total  │                                 │ iso    │       │
│    └────────┘                                 └────────┘       │
│                                                                │
│  Commands:   [StartTrial]  [UpgradePlan]  [Cancel]             │
│  Events:     [TrialStarted] [PlanUpgraded] [SubscriptionEnded] │
│  Invariants:                                                   │
│     · A subscription can have at most one active trial.        │
│     · The plan level can only change during a renewal window.  │
│     · Cancellation is irreversible within the current period.  │
└────────────────────────────────────────────────────────────────┘
```

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Two aggregate roots in the same diagram | Put them in a Domain Model; Aggregate = one root. |
| Tight-coupled children that come from *another* aggregate | External aggregates are referenced by ID (Value Object), not embedded. Draw those as muted ID-reference VOs. |
| Generic field lists (`createdAt`, `updatedAt`, `deletedAt`) | These add noise. Only show fields that carry domain meaning. |
| "Invariants" that describe validation rules on a single field | Invariants span the aggregate. "Email must be valid" isn't an invariant; "Customer cannot have two active subscriptions" is. |
| Commands named as past-tense or CRUD (`UpdateSubscription`) | Commands are intentions in the ubiquitous language — `ChangePlan`, not `UpdateSubscription`. |
| Events that double up ("OrderPlacedAndPaid") | One event per fact. Compound events hide missing workflow steps. |

## Complexity budget

- 1 root + up to 6 children (entities + VOs combined).
- Up to 6 invariants.
- Up to 5 commands and 5 events each.

If you can't fit, you likely have two aggregates. Split.

## Examples

- `assets/example-aggregate.html` — minimal light
- `assets/example-aggregate-dark.html` — minimal dark
- `assets/example-aggregate-full.html` — full editorial with summary cards
