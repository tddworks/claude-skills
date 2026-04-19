# Phase 3 — Domain TDD

**Your task:** write the domain layer protocol + `<NounImpl>` + port, driven by tests. Chicago school — state-based assertions only.

## Inputs

- Approved design from Phase 2 (names, types, file map)

## Steps

### 1. Write value-type tests first (Red)

The value type is the simplest thing. Test computed properties, derived state, semantic booleans.

```swift
@Suite
struct <Value>Tests {
    @Test func `<state variant> routes to <bucket>`() {
        let value = <Value>(status: .<variant>(...))
        #expect(value.bucket == .<expected>)
        #expect(value.needsAttention == <expected>)
    }
    // one test per variant
}
```

Run tests — they should fail because `<Value>` doesn't exist yet.

### 2. Implement value type (Green)

Minimal struct that makes the tests pass:

```swift
public struct <Value>: Sendable, Equatable, Identifiable {
    public let id: <IDType>
    public var <field>: <Type>
    // …
    public init(...) { … }
}

extension <Value> {
    public var <computedQuery>: Bool { /* derived from state */ }
    public var <bucket>: <BucketEnum> {
        switch status {
        case .a: return .x
        case .b: return .y
        }
    }
}
```

Run tests — green.

### 3. Write aggregate tests (Red)

Aggregate state changes via `apply`, `upsert`, `remove`. Commands via `await`-able methods. Port stubbed (return data, don't verify calls).

```swift
@Suite(.serialized)
@MainActor
struct <AggregateImpl>Tests {
    // MARK: push-fed writes

    @Test func `apply replaces items wholesale`() {
        let agg = <AggregateImpl>()
        agg.apply(items: [stub(id: "a"), stub(id: "b")])
        #expect(agg.items.count == 2)

        agg.apply(items: [stub(id: "c")])
        #expect(agg.items.count == 1)
    }

    @Test func `upsert replaces by id`() {
        let agg = <AggregateImpl>()
        agg.upsert(stub(id: "a", <state>: .x))
        agg.upsert(stub(id: "a", <state>: .y))
        #expect(agg.items.count == 1)
        #expect(agg.items.first?.<state> == .y)
    }

    @Test func `remove deletes by id`() { … }
    @Test func `remove is a no-op when id is missing`() { … }

    // MARK: computed queries

    @Test func `<count>Count reflects matching items only`() {
        let agg = <AggregateImpl>()
        agg.apply(items: [stub(…), stub(…), stub(…)])
        #expect(agg.<count>Count == <expected>)
    }

    // MARK: commands via stubbed port

    @Test func `refresh populates items from port`() async {
        let port = Mock<AggregatePort>()
        given(port).list().willReturn([stub(id: "a"), stub(id: "b")])

        let agg = <AggregateImpl>(port: port)
        await agg.refresh()

        #expect(agg.items.count == 2)
        #expect(agg.lastError == nil)
    }

    @Test func `refresh captures port error`() async {
        let port = Mock<AggregatePort>()
        given(port).list().willThrow(StubError.boom)

        let agg = <AggregateImpl>(port: port)
        await agg.refresh()

        #expect(agg.lastError != nil)
    }

    @Test func `refresh is a no-op when port is nil`() async {
        let agg = <AggregateImpl>(port: nil)
        await agg.refresh()
        #expect(agg.items.isEmpty)
    }

    // MARK: - helpers
    private enum StubError: Error { case boom }
    private func stub(id: String = "x", …) -> <Value> { … }
}
```

### 4. Implement the port protocol + `<AggregateImpl>` (Green)

```swift
// Infra port
@Mockable
public protocol <AggregatePort>: Sendable {
    func list() async throws -> [<Value>]
    func <action>(id: <Value>.ID, <args>) async throws
}

// Aggregate protocol
@MainActor @Mockable
public protocol <Aggregate>: Observable {
    var items: [<Value>] { get }
    var lastError: Error? { get }
    // computed queries
    var <query>: [<Value>] { get }
    var <count>Count: Int { get }
    // commands
    func refresh() async
    func <action>(_ item: <Value>, <args>) async throws
    // push-fed writers
    func apply(items: [<Value>])
    func upsert(_ item: <Value>)
    func remove(id: <Value>.ID)
}

// Concrete impl
@Observable @MainActor
public final class <AggregateImpl>: <Aggregate> {
    public private(set) var items: [<Value>] = []
    public private(set) var lastError: Error?

    @ObservationIgnored
    private let port: (any <AggregatePort>)?

    public init(port: (any <AggregatePort>)? = nil) {
        self.port = port
    }

    // Computed queries — derive from items only
    public var <query>: [<Value>] { items.filter(\.<predicate>) }
    public var <count>Count: Int { <query>.count }

    // Push-fed writers — the aggregate is the single writer of its state
    public func apply(items: [<Value>]) {
        self.items = items
    }

    public func upsert(_ item: <Value>) {
        if let idx = items.firstIndex(where: { $0.id == item.id }) {
            items[idx] = item
        } else {
            items.append(item)
        }
    }

    public func remove(id: <Value>.ID) {
        items.removeAll { $0.id == id }
    }

    // Commands — delegate to port, capture errors as state
    public func refresh() async {
        guard let port else { return }
        do {
            let latest = try await port.list()
            items = latest
            lastError = nil
        } catch {
            lastError = error
        }
    }
}
```

### 5. Refactor

With tests green, look for:

- **Behaviour on helper services** that should be on the value or aggregate — move it.
- **Raw Bool properties** that deserve a semantic name — add a computed `is<X>` / `has<Y>` / `needs<Z>`.
- **Duplicate computation** between callers — pull into a computed query.
- **Tests that assert on mock call counts** — delete; add a state assertion instead.

### 6. Regenerate project (if the project uses a manifest-generated workspace) and run tests

```
<manifest regeneration command>   # only needed if the project auto-generates its IDE workspace
<test command>                    # run domain-layer tests; scope to the new feature if possible
```

Confirm every test passes before moving on.

## Output

- `<domain module>/<Feature>/<Value>` — value type
- `<domain module>/<Feature>/<Aggregate>` — protocol + `<AggregateImpl>` impl
- `<domain module>/<Feature>/<AggregatePort>` — infra port
- `<domain tests>/<Feature>/` — tests for `<Value>` + `<AggregateImpl>` (exact file names match the project's testing convention)
- Tests green

## Gate

- Value tests cover every state variant's computed derivations.
- Aggregate tests cover `apply`/`upsert`/`remove`, each computed query, `refresh` success/failure/nil-port.
- Zero `verify(mock).x.called(...)` — all assertions are on state or return values.
- Tests run in under a second (domain tests should be fast and pure).

## Anti-patterns

- **Mock-then-verify tests.** `verify(mockPort).approve.called(.once)` is London school — this skill rejects it. Test observable state only.
- **Rich value, thin aggregate.** Keep behaviour on the value when it's intrinsic to the data (bucket routing, semantic booleans). Aggregate methods should do things the value alone can't (mutate collection, talk to the port).
- **Testing framework bleed.** Don't test `@Observable` itself. Don't test Swift's `filter`. Test YOUR logic.
- **Port mocked in value-type tests.** Values have no dependencies. If a value test needs a mock, the value isn't a value.
- **Time-based tests.** If you're testing "time ago" / dates, take a reference date as a parameter instead of calling `Date()` inside the value.
