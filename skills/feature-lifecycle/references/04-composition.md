# Phase 4 — Composition

**Your task:** plug the new aggregate onto the parent entity (if any) and expose it through the composition-root facade. Views must never drill into composition detail.

## Inputs

- Green domain layer from Phase 3 (protocol + `<AggregateImpl>` + port)
- The existing composition root (`Workspace` / `App` / `Root` — whatever this project calls it)
- The parent entity the aggregate hangs off (if it's a sub-aggregate)

## Steps

### 1. Decide where the aggregate lives

| Case | Owner |
|---|---|
| Per-user / per-device / per-tenant content | Sub-aggregate on the owning entity (e.g. `Device`, `User`) |
| App-wide singleton (catalog, registry, settings) | Directly on the composition root |
| Transient session-scoped thing | Sub-aggregate on the session entity |

Prefer the narrowest owner that fits. If the aggregate's lifecycle is tied to some entity, it belongs on that entity.

### 2. Add the aggregate to the parent

If the aggregate hangs off an entity (say `Device`), extend both the protocol and the live impl:

```swift
@MainActor @Mockable
public protocol <Parent>: Observable {
    // existing members…
    var <feature>: any <Aggregate> { get }
}

@Observable @MainActor
public final class <ParentImpl>: <Parent> {
    // existing fields…
    public let <feature>: any <Aggregate>

    public init(…, <feature>: any <Aggregate> = <AggregateImpl>()) {
        …
        self.<feature> = <feature>
    }
}
```

The parent holds the aggregate as `any <Aggregate>` — NOT `<AggregateImpl>`. Tests swap in mocks via the init param.

### 3. Expose a facade on the composition root

The composition root is the single thing views talk to. It should hide "which entity owns this" from callers.

```swift
@Observable @MainActor
public final class <Root> {
    public let <entities>: any <Entities>       // e.g. devices: any Devices

    @ObservationIgnored
    private let _fallback<Aggregate>: any <Aggregate> = <AggregateImpl>()

    private var _<feature>: any <Aggregate> {
        <entities>.active?.<feature> ?? _fallback<Aggregate>
    }

    // Facade surface — thin forwarders, one per query/command the UI needs
    public var <feature>Items: [<Value>] { _<feature>.items }
    public var <feature>NeedsAttention: [<Value>] { _<feature>.needsAttention }
    public func refresh<Feature>() async { await _<feature>.refresh() }
}
```

**Rules:**
- Fallback is always a working `<AggregateImpl>()` with no port — empty, no crashes, no optional chaining in views.
- `@ObservationIgnored` on the fallback so it doesn't pollute the root's change graph.
- Forwarders are *verbs the UI uses*, not the full aggregate surface.
- If the UI wants to bind directly to the aggregate (e.g. `ForEach(sessions.items)`), expose it as `public var <feature>: any <Aggregate> { _<feature> }`.

### 4. Write composition tests (optional, thin)

You already tested the aggregate in Phase 3. The composition layer just needs to prove that:

- The facade returns the active entity's aggregate, not the fallback, when there is one.
- The facade returns the fallback when no entity is active.

```swift
@Test func `facade returns active entity's aggregate`() {
    let parent = <ParentImpl>(id: "a")
    parent.<feature>.apply(items: [stub(id: "x")])
    let entities = <EntitiesImpl>()
    entities.upsert(parent)
    entities.activate(id: "a")

    let root = <Root>(<entities>: entities)
    #expect(root.<feature>Items.count == 1)
}

@Test func `facade returns empty when no entity is active`() {
    let root = <Root>()
    #expect(root.<feature>Items.isEmpty)
}
```

Keep this test file short. The aggregate's own tests do the heavy lifting.

### 5. Remove leaky accesses

Grep for any code that touches the aggregate via `<root>.<entities>.active?.<feature>`. That pattern leaks composition detail into views and other layers. Replace each call site with the facade forwarder.

```
# smell
root.devices.active?.sessions.items

# fix — either new forwarder or expose the aggregate
root.sessionItems
root.sessions.items
```

If a view needs something the facade doesn't expose, **add the forwarder** — don't bypass the facade.

## Output

- `<Parent>` protocol + `<ParentImpl>` extended with `<feature>: any <Aggregate>`
- `<Root>` composition root gains a fallback + forwarders
- Zero callers drilling through `active?.<feature>`
- Composition tests green

## Gate

- Views and other non-domain callers touch the feature only through the root facade.
- No `as? <AggregateImpl>` casts anywhere — callers see `any <Aggregate>`.
- Fallback works: calling `root.<feature>Items` with no active entity returns `[]`, not a crash.
- `<ParentImpl>` init signature has the aggregate as an injectable parameter (for tests).

## Anti-patterns

- **Exposing `devices.active?` in views.** Views end up doing `workspace.devices.active?.sessions?.items ?? []`. Every `?` is a missed facade forwarder.
- **Fallback with a port.** The fallback exists so there's always a valid aggregate, even offline. It must not talk to a real port — keep it pure in-memory.
- **Parent exposes `<AggregateImpl>` concretely.** Breaks tests, couples consumers to the impl. The parent's protocol holds `any <Aggregate>`.
- **Coordinator methods on the root.** `Root.approveSession(id:)` calling into the aggregate is a smell — the UI should call `root.sessions.approve(id:)` directly (via the forwarded aggregate) or the aggregate should react to a state change somewhere else.
- **Root growing a method per command.** If you're adding `root.<doThing1>`, `root.<doThing2>`, `root.<doThing3>` as thin passthroughs to the same aggregate, just expose `root.<feature>: any <Aggregate>` and let callers use it.
