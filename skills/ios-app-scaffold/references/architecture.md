# iOS Layered Architecture Reference

## Layer Overview

```
┌─────────────────────────────────────┐
│            App Layer                │  SwiftUI Views, App Entry
│         Sources/App/                │  Depends on: Domain, Infrastructure
├─────────────────────────────────────┤
│       Infrastructure Layer          │  Persistence, Networking
│     Sources/Infrastructure/         │  Depends on: Domain
├─────────────────────────────────────┤
│          Domain Layer               │  Business Logic, Models, Protocols
│        Sources/Domain/              │  No dependencies
└─────────────────────────────────────┘
```

## Domain Layer

Pure business logic with no external dependencies.

### Structure
```
Sources/Domain/
├── Models/       # Data structures (Codable, Sendable)
├── Protocols/    # Repository interfaces (@Mockable)
└── Utils/        # Domain utilities (Logger, helpers)
```

### Key Patterns

**Models**: Rich domain models with behavior
```swift
public struct Subscription: Identifiable, Codable, Hashable, Sendable {
    public let id: UUID
    public var name: String
    public var price: Decimal

    public var monthlyEquivalent: Decimal {
        // Business logic lives in the model
    }
}
```

**Protocols**: Use `@Mockable` for testability
```swift
@Mockable
public protocol SubscriptionRepository: Sendable {
    func fetchAll() async throws -> [Subscription]
    func save(_ item: Subscription) async throws
}
```

## Infrastructure Layer

Implements domain protocols with concrete persistence.

### Structure
```
Sources/Infrastructure/
├── Local/        # SwiftData repositories
└── Network/      # API clients (if needed)
```

### SwiftData Pattern
```swift
public final class LocalRepository: SomeRepository, @unchecked Sendable {
    private let modelContainer: ModelContainer
    private let modelContext: ModelContext

    public init() throws {
        let schema = Schema([EntityModel.self])
        let config = ModelConfiguration(schema: schema)
        self.modelContainer = try ModelContainer(for: schema, configurations: [config])
        self.modelContext = ModelContext(modelContainer)
    }
}
```

## App Layer

SwiftUI views consuming domain models directly.

### Structure
```
Sources/App/
├── Views/           # SwiftUI views by feature
├── Resources/       # Assets, localization
├── Application/     # App constants, loggers
├── Extensions/      # View helpers
├── Info.plist
├── *.entitlements
└── *App.swift       # App entry point
```

### Key Patterns

**Views consume Domain directly** (no ViewModel layer)
```swift
struct ContentView: View {
    @Binding var subscriptions: [Subscription]
    let repository: SubscriptionRepository
}
```

**Dependency injection via init**
```swift
@main
struct MyApp: App {
    private let repository: SomeRepository

    init() {
        self.repository = try! LocalRepository()
    }
}
```

## Testing

### Domain Tests
- Test model behavior and computed properties
- Use Swift Testing framework (`@Test`)
```swift
@Test func model_computesCorrectly() {
    let model = MyModel(value: 10)
    #expect(model.computed == 20)
}
```

### Infrastructure Tests
- Test repository implementations
- Use in-memory SwiftData for isolation

## Tuist Configuration

### Project.swift Key Settings
- `SWIFT_VERSION`: "6.0"
- `IPHONEOS_DEPLOYMENT_TARGET`: "18.0"
- `SWIFT_STRICT_CONCURRENCY`: "complete"
- `ENABLE_DEBUG_DYLIB`: "YES" (for SwiftUI previews)
- `ENABLE_PREVIEWS`: "YES"

### Dependencies
- **Mockable**: Protocol mocking via Swift macros
- Add more via `packages` array in Project.swift