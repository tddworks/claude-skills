---
name: feature-lifecycle
description: Full-lifecycle guide for implementing a feature end-to-end in a London-school DDD Swift/iOS codebase (or any layered Domain/Infrastructure/App project that uses protocol + concrete impl aggregates, narrow infrastructure ports, and Chicago-school state-based TDD). Use this skill whenever the user asks to **build**, **implement**, **add**, **ship**, or **develop** a feature — including vague asks like "let's add X", "build me Y", "implement Z", or "wire up the W flow". Strongly prefer this skill over jumping straight to code whenever a new domain concept is in play. Each lifecycle phase has its own focused sub-guide so the agent loads only the instructions for the current task, not a 600-line monolith.
license: MIT
---

# Feature Lifecycle

One skill, eight focused phases. Each phase tells the agent exactly what to do for that step — inputs, steps, outputs, and a gate to know it's done.

```
1. Discovery        → what already exists, what the user means
2. Domain design    → ASCII architecture + naming + user approval
3. Domain TDD       → value tests + aggregate tests + protocol + impl class (Red → Green)
4. Composition      → plug the aggregate onto parent + facade forwarders
5. Infrastructure   → port conformance + push routing + wire format
6. Views            → SwiftUI bind to the facade; no ViewModel layer
7. Docs             → feature doc + aggregate audit + visual artifacts
8. Verify           → pre-commit checklist + tests + build
```

**The phases are sequential. Don't skip ahead.** If a phase's gate isn't met, go back.

---

## Which sub-guide to load

Load only the reference for the phase you're in. Don't read the full set up front.

| Phase | Load | Output when you're done |
|---|---|---|
| 1. Discovery | [`references/01-discovery.md`](references/01-discovery.md) | A short "discovery note" listing existing docs, drift, user's words |
| 2. Domain design | [`references/02-domain-design.md`](references/02-domain-design.md) | Approved ASCII architecture + component table + file map |
| 3. Domain TDD | [`references/03-domain-tdd.md`](references/03-domain-tdd.md) | Protocol + `<NounImpl>` + port + tests all green |
| 4. Composition | [`references/04-composition.md`](references/04-composition.md) | Aggregate plugged into parent entity + facade forwarders on the composition root |
| 5. Infrastructure | [`references/05-infrastructure.md`](references/05-infrastructure.md) | Port conformance + push routing wired; infra layer green |
| 6. Views | [`references/06-views.md`](references/06-views.md) | Views binding to the facade; UI builds |
| 7. Docs | [`references/07-docs.md`](references/07-docs.md) | Feature doc + audit update + visual artifacts |
| 8. Verify | [`references/08-verify.md`](references/08-verify.md) | Checklist green, tests green, release build green |

---

## The core pattern (the thing every phase serves)

```swift
// 1. Domain noun — protocol
@MainActor @Mockable
public protocol <Aggregate>: Observable {
    var items: [<Value>] { get }
    // ... rich computed queries + business-intent commands + apply/upsert/remove
}

// 2. Concrete implementation class
@Observable @MainActor
public final class <AggregateImpl>: <Aggregate> {
    public init(port: (any <AggregatePort>)? = nil) { … }
}

// 3. Narrow internal port (infra seam)
@Mockable
public protocol <AggregatePort>: Sendable {
    // async throws methods the infra client / DB / API implements
}
```

Every phase assumes this shape. Deviations (protocol-less classes, legacy `xxxBackend` glue, role protocols named as collections) are smells — see [`references/02-domain-design.md`](references/02-domain-design.md) for the naming playbook.

---

## When in doubt

- **Names feel clunky?** Read them out loud. If a non-engineer wouldn't say it, rename.
- **Tests hard to write?** The aggregate is coupled to too much. Pull dependencies behind a narrow port.
- **Composition root keeps growing methods?** Push them down to the owning aggregate. The root is a facade, not a coordinator.
- **Views casting `as? <concrete impl>`?** Protocol surface too minimal. Grow it.
- **User pushes back on a name?** Pushback is signal. Re-derive from first principles — don't patch with another loaded word.

---

## The anti-patterns (from most-costly, in order)

1. **Jumping to code without Phase 1–2.** You'll build the wrong shape and have to undo it.
2. **Domain as setters only — no rich behavior.** Logic ends up scattered across views and infra.
3. **`XxxBackend`, `XxxRegistry`, `XxxManager`, `XxxService`.** Infrastructure words in the domain.
4. **Coordinator methods on the composition root.** Cross-aggregate orchestration lives on the aggregate that owns the triggering state, or propagates via `@Observable` reactions.
5. **Views touching `@Observable` indirection** (e.g. `root.something?.child?.more`). Expose a facade on the root; never leak composition detail to views.
6. **Interaction-based tests** (`verify(mock).method.called(...)`). This skill uses Chicago-school state/return-value tests only.
7. **Ship-first, doc-after.** The feature doc (Phase 7) captures *why*; write it before memory decays.

Load the next sub-guide when you're ready for the phase. One at a time.
