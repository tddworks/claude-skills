# Phase 5 — Infrastructure

**Your task:** implement the port port against the real external system (RPC client, HTTP API, DB, file system), and wire server-pushed events into the aggregate's push-fed writers.

## Inputs

- `<AggregatePort>` protocol from Phase 3
- The infrastructure layer (API client / DB adapter / event consumer — whatever the project uses)
- Wire format the external system speaks (JSON-RPC, REST, protobuf, etc.)

## Steps

### 1. Conform the existing infra client to the new port

Don't create a new class per port. The infra client is usually a single object that speaks the wire protocol. Extend it with a conformance:

```swift
extension <InfraClient>: <AggregatePort> {
    public func list() async throws -> [<Value>] {
        let response: <WireType> = try await request(method: "<verb>", params: [:])
        return response.items.map { $0.toDomain() }
    }

    public func <action>(id: <Value>.ID, <args>) async throws {
        try await request(method: "<verb>", params: [...])
    }
}
```

Keep mapping (wire → domain) in this file. The domain layer never sees wire types.

### 2. Define the wire types

Wire types are `Decodable` / `Encodable` mirrors of what the external system sends. Keep them flat, keep them in infra, map them to domain values at the seam.

```swift
struct <Value>Wire: Codable {
    let id: String
    let status: String
    // …

    func toDomain() -> <Value> {
        <Value>(
            id: .init(id),
            status: <Status>(wire: status),
            …
        )
    }
}
```

If the wire format is documented in a schema file (`docs/infra client-protocol.md`, OpenAPI, proto), update it here so future readers see the whole surface in one place.

### 3. Wire push events to aggregate writers

If the external system pushes state changes (websocket events, SSE, webhooks), route them to the aggregate's `apply` / `upsert` / `remove`:

```swift
final class <StreamInterpreter> {
    private weak var <feature>: <AggregateImpl>?

    func setFeature(_ agg: <AggregateImpl>?) { self.<feature> = agg }

    func handle(_ event: <WireEvent>) {
        switch event.kind {
        case "<feature>.snapshot":
            let items = event.items.map { $0.toDomain() }
            Task { @MainActor in <feature>?.apply(items: items) }

        case "<feature>.updated":
            let item = event.item.toDomain()
            Task { @MainActor in <feature>?.upsert(item) }

        case "<feature>.removed":
            Task { @MainActor in <feature>?.remove(id: .init(event.id)) }

        default: break
        }
    }
}
```

**Push vs. pull:**
- Pull (`refresh`) = the aggregate asks the port. Used for initial load / manual refresh.
- Push (`apply` / `upsert` / `remove`) = the interpreter feeds the aggregate from server events. Used for live sync.

Both co-exist. Push keeps the UI live; pull fills gaps (reconnect, cold start).

### 4. Wire it at the composition boundary

The place where you construct `<AggregateImpl>` is also where you give it its port and connect the stream:

```swift
// Connection / bootstrap code
let port = infraClient  // conforms to <AggregatePort>
let aggregate = <AggregateImpl>(port: port)
streamInterpreter.setFeature(aggregate)

let entity = <ParentImpl>(id: …, <feature>: aggregate)
entities.upsert(entity)
```

If the infra client / connection already has a `wireUp(...)` or `bind(...)` style method, add the new aggregate there. Don't scatter wiring across the codebase.

### 5. Test the infra conformance

Integration-style tests for the mapper + port:

```swift
@Suite
struct <InfraClient><AggregatePort>Tests {
    @Test func `list decodes wire response into domain values`() async throws {
        let client = <InfraClient>(transport: StubTransport(response: """
        {"items": [{"id": "a", "status": "pending"}]}
        """))
        let result = try await client.list()
        #expect(result.count == 1)
        #expect(result.first?.id.rawValue == "a")
    }
}
```

Assert on **domain values**, not on the raw JSON. The test's job is to prove the seam converts correctly.

### 6. Update the wire-format doc

If the project documents its wire protocol, add the new methods/events there. Keep the doc and the code in lockstep — stale wire docs are worse than none.

## Output

- `<InfraClient>: <AggregatePort>` conformance (or a dedicated adapter if the infra is layered differently)
- Wire types with `toDomain()` / `fromDomain()` mappers
- Stream interpreter routes relevant events to `apply` / `upsert` / `remove`
- Composition layer wires the port into `<AggregateImpl>` at bootstrap
- Infra tests green
- Wire-format doc updated

## Gate

- No wire types leak into the domain layer.
- No domain types leak into the wire layer.
- Push events mutate the aggregate via its writers — never reach into private state.
- Reconnect story works: after a disconnect, calling `refresh()` resyncs the aggregate (don't rely on push-only).
- Feature flag / demo mode still works — the aggregate can be constructed with no port and stays functional.

## Anti-patterns

- **New class `<Feature>Backend` / `<Feature>Service` wrapping the infra client.** You already have the infra client; conform it to the port instead. One object, one job.
- **Wire types in the domain.** If `<Value>` has `let rawJSON: [String: Any]`, the boundary is in the wrong place.
- **Push-only with no pull.** First reconnect with stale state exposes this. Always implement `refresh`.
- **Pull-only with no push.** The UI lags behind reality. If the external system has events, route them.
- **Fire-and-forget on errors.** Port errors should either update `lastError` on the aggregate or bubble up — never silently discard. Decide which at the aggregate surface (most reads: capture as state; most writes: bubble).
- **Skipping the mapper test.** The wire→domain mapping is where bugs hide. One test per non-trivial field transformation.
