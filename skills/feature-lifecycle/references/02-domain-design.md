# Phase 2 — Domain design

**Your task:** produce an approved architecture before writing any code.

## Inputs

- Discovery note from Phase 1 (user's vocabulary, existing shape, hypothesis)
- The user, to approve the proposed design

## Steps

### 1. Pick the domain shape

Every feature is one of:

| Shape | When to pick |
|---|---|
| **New sub-aggregate on an existing parent entity** | Feature is a collection or stateful concept owned by the parent (e.g. per-device setting, per-user preference set) |
| **New field / variant on an existing value type** | Extends a concept non-breakingly (e.g. add `origin: .a | .b` to `Project`) |
| **New computed property on an existing aggregate** | Pure view derivation, no new state |
| **New push-fed writer on an existing aggregate** | External system (server, API, event stream) pushes data the aggregate absorbs via `apply` / `upsert` / `remove` |
| **New top-level aggregate** | Genuinely new domain concept not on the existing map |

Default to the smallest shape that fits. New top-level aggregates are the last resort.

### 2. Name it using the user's words

Apply this naming playbook. For each candidate name, check these rules in order:

| Rule | Example fix |
|---|---|
| No `XxxBackend` / `XxxRegistry` / `XxxStore` / `XxxManager` / `XxxService` / `XxxHelper` | `<Thing>Registry` → `<Things>`; `<Thing>Store` → `<Things>` |
| No `XxxController` outside MVC | `<Thing>Controller` → plural noun of what it controls |
| `XxxRepository` only for pure CRUD (`find`, `save`, `delete`) | If it has domain verbs (`approve`, `refresh`, `subscribe`), rename to the plural noun |
| `IXxx` prefix — never | `I<Things>` → `<Things>` |
| Plural noun = collection aggregate; singular noun = entity or value | `<Thing>` (value) + `<Things>` (aggregate) |
| London-school pattern: protocol = noun, class = `<NounImpl>`, port = `<NounPort>` | `<Things>` protocol + `<ThingsImpl>` class + `<Thing>Port` port |

### 3. Draft the ASCII architecture

```
┌─── App (views) ─────────────────────────────────────────────────────┐
│   <new view(s)>                                                     │
└────────────────────────────▲────────────────────────────────────────┘
                             │ binds to facade
                             │
┌────────────────────────────┴────────────────────────────────────────┐
│  Domain                                                              │
│                                                                      │
│  <composition root — usually unchanged>                              │
│  └── forwards <feature>: any <Aggregate>                             │
│                                                                      │
│  <parent entity> (if sub-aggregate on an entity)                     │
│  └── <feature>: any <Aggregate>                                      │
│                                                                      │
│  <Aggregate>       @MainActor @Mockable protocol (Observable)        │
│  ├── items:        [<Value>]                                         │
│  ├── <queries>                                                       │
│  ├── <commands>                                                      │
│  └── apply / upsert / remove                                         │
│                                                                      │
│  <AggregateImpl>   @Observable @MainActor production impl            │
│  └── init(port: <AggregatePort>?)                              │
│                                                                      │
│  <Value>           value type (Sendable, Equatable, Identifiable)    │
│  └── <fields> + computed queries                                     │
│                                                                      │
│  <AggregatePort>  narrow @Mockable port                           │
│  └── <async throws methods>                                          │
└────────────────────────────▲────────────────────────────────────────┘
                             │ implemented by
┌────────────────────────────┴────────────────────────────────────────┐
│  Infrastructure                                                      │
│  └── <infra client / API / DB> conforms to <AggregatePort>        │
└──────────────────────────────────────────────────────────────────────┘
```

### 4. Component table

| Component | Kind | Purpose | Key methods |
|---|---|---|---|
| `<Value>` | Value type | Data snapshot | computed props |
| `<Aggregate>` | Protocol (aggregate) | Domain surface | queries, commands, apply/upsert/remove |
| `<AggregateImpl>` | Class (@Observable) | Production impl | holds state, delegates to port |
| `<AggregatePort>` | Protocol (infra port) | RPC/DB seam | async throws methods |

### 5. File map (exact paths)

```
<domain module>/Sources/<Feature>/
├── <Value>.<ext>
├── <Aggregate>.<ext>            ← protocol + concrete impl in one file is fine
└── <AggregatePort>.<ext>     ← (only if infra calls are needed)

<domain module>/Tests/<Feature>/
├── <Value>Tests.<ext>
└── <AggregateImpl>Tests.<ext>
```

The exact directory layout and file extension depend on the project (module layout, language). What matters is the grouping: value + aggregate + port co-located, tests mirroring the layout.

### 6. Get user approval

Present the ASCII + component table + file map **before writing code**. Ask explicitly: *"approve / modify?"*

Expect pushback on names. When it comes, **don't defend — rethink from first principles**. Re-derive the shape from the user's vocabulary, not from the code you've been sketching.

## Output

Approved proposal with three artifacts:

1. ASCII architecture diagram
2. Component table
3. File map

Commit the proposal to `<project>/docs/features/<feature>.md` (draft) if the project uses per-feature docs. The doc is the contract — further implementation follows it.

## Gate

- User has said "proceed" (or equivalent) on the proposal.
- Every name in the proposal passes the naming playbook.
- The shape is the smallest that fits (no new top-level aggregate if a sub-aggregate works).

## Anti-patterns

- **Writing code before approval.** You'll throw it away.
- **Rebranding infrastructure words.** `FooBackend` → `FooService` is not a fix; it's the same smell.
- **Designing for hypothetical requirements.** If the user didn't ask for it, don't model it.
- **Avoiding the pushback.** When the user says "that name feels off," they're usually right about the shape, not just the word. Re-derive.
- **Skipping the diagram.** The diagram is the cheapest place to discover that the shape is wrong.
