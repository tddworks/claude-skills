# Phase 6 — Views

**Your task:** build the UI layer. Views bind to the composition-root facade directly. No ViewModel layer, no business logic, no composition-detail leakage.

## Inputs

- Composition root with a facade for the feature (from Phase 4)
- Design mockups / screens for the feature (if any)

## Steps

### 1. Bind to the facade

Views take the root as input (or read it from the environment) and call its forwarders. They never reach into the aggregate graph.

```swift
struct <Feature>View: View {
    let root: <Root>

    var body: some View {
        List {
            Section("Needs attention") {
                ForEach(root.<feature>NeedsAttention) { item in
                    <Feature>Row(item: item, onApprove: {
                        Task { try? await root.<feature>.approve(id: item.id) }
                    })
                }
            }
            Section("Recent") {
                ForEach(root.<feature>Recent) { item in
                    <Feature>Row(item: item)
                }
            }
        }
        .task { await root.refresh<Feature>() }
    }
}
```

Two allowed shapes:
- **Forwarder-per-query** (`root.<feature>Items`, `root.<feature>NeedsAttention`) — good when the view needs a few slices.
- **Expose the aggregate** (`root.<feature>: any <Aggregate>`) — good when the view wants to bind to many parts of the aggregate at once. Still goes through the facade; the aggregate is resolved there.

### 2. Keep views dumb

Views express **what** to show, not **how** to fetch it. The aggregate owns the how.

**Bad:**
```swift
// logic creeping into the view
if root.session?.id != nil && !root.session!.isRunning && user.canApprove {
    Button("Approve") { /* ad-hoc orchestration */ }
}
```

**Good:**
```swift
// the domain already answers this
if item.needsAttention {
    Button("Approve") {
        Task { try? await root.<feature>.approve(id: item.id) }
    }
}
```

If a view is reaching for more than one field to compute a boolean, the aggregate/value is missing a computed query. Push it down.

### 3. No ViewModel layer

This pattern intentionally skips ViewModels. The aggregate **is** the view model — it's `@Observable`, it holds state, it has computed queries, it responds to commands.

A "ViewModel" in a typical MV* pattern does three things:
- Holds state → the aggregate does this.
- Exposes derived queries → the aggregate's computed properties do this.
- Translates UI events to domain commands → the view does this inline, since commands are one-line calls.

If you feel a ViewModel coming on, ask: "what's the new type going to hold?" If the answer is transient UI state (sheet shown, selected tab, input text), put it in the view with `@State`. If it's domain state, it belongs on the aggregate.

### 4. Handle async work with `.task` / `Task`

- **`.task` on the view** — for initial loads tied to the view's lifecycle. Cancels on disappear.
- **`Task { … }` in a button** — for explicit user commands. Don't await in the action directly.

```swift
Button("Refresh") {
    Task { await root.refresh<Feature>() }
}
.task {
    await root.refresh<Feature>()
}
```

### 5. Error + empty + loading states

Three states every feature view needs:

```swift
if let error = root.<feature>LastError {
    ErrorRow(error: error) { Task { await root.refresh<Feature>() } }
} else if root.<feature>Items.isEmpty {
    ContentUnavailableView("No <things> yet", systemImage: "<icon>")
} else {
    <List or grid>
}
```

Surface these from the aggregate: `var lastError: Error?`, `var items: [T]`. The view maps state → UI, nothing more.

### 6. Don't test views in this skill

Chicago-school state tests on the aggregate already cover logic. SwiftUI snapshot / preview testing is out of scope for this lifecycle — rely on previews + manual QA + real-device testing.

What you SHOULD test at the view layer:
- Previews render. Open Xcode previews for every new view; a preview that won't compile is a broken view.

### 7. Previews with live mocks

Create at least one preview per view, using a `<AggregateImpl>` wired with stub data:

```swift
#Preview("<Feature> — populated") {
    let agg = <AggregateImpl>()
    agg.apply(items: [.stub(id: "a"), .stub(id: "b", status: .<variant>)])
    let root = <Root>(/* wire agg into root */)
    return <Feature>View(root: root)
}

#Preview("<Feature> — empty") {
    <Feature>View(root: <Root>())
}
```

Previews are the cheapest way to iterate on layout. They also double as living documentation of the feature's states.

## Output

- SwiftUI view(s) binding to `root.<feature>…` via facade
- Zero references to `root.<entities>.active?.<feature>` in view code
- No ViewModel types
- Previews for populated / empty / error states
- UI builds cleanly on iOS (or whatever the target platform is)

## Gate

- Grep confirms no view touches `active?.<feature>`.
- Views don't do `as? <AggregateImpl>` (protocol is rich enough).
- Commands in views are one-liners wrapped in `Task {}`.
- Previews compile and render something sensible.

## Anti-patterns

- **`@StateObject var viewModel = FeatureViewModel(...)`.** This pattern has no ViewModels. If you're tempted, the aggregate is missing a query or a command.
- **Business logic in `computed` view vars.** `var filtered: [Item] { items.filter(...) }` belongs on the aggregate as a computed query, not on the view.
- **Optional-chaining graphs in views.** `root.devices.active?.sessions?.items.filter(...)` is a bug magnet and hides missing forwarders. Add the forwarder.
- **View holding its own state that mirrors the aggregate.** `@State var items = [...]` that re-reads from the aggregate is always a race. Bind directly.
- **Views calling the port.** Views never see the port. If a view needs a refresh, the aggregate exposes it.
- **Skipping previews.** Without a preview, you don't know the view compiles in isolation — and layout bugs sneak in.
