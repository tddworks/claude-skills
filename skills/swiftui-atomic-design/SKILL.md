---
name: swiftui-atomic-design
description: |
  Guide for building SwiftUI components using Brad Frost's Atomic Design methodology — organizing views into Atoms, Molecules, Organisms, Templates, and Pages. Use this skill whenever building new SwiftUI UI components, refactoring existing views into reusable pieces, creating a design system, or organizing a component library. Also trigger when the user mentions "atomic design", "design system", "component hierarchy", "reusable components", "atoms and molecules", or wants to decompose a complex SwiftUI view into smaller, composable parts.
---

# SwiftUI Atomic Design

Atomic Design is Brad Frost's methodology for building UI systems from small, composable pieces. In SwiftUI, this maps naturally to the framework's compositional view architecture. The hierarchy flows from simple to complex:

**Atoms → Molecules → Organisms → Templates → Pages**

Each level composes the one below it. The discipline is knowing *where* a component belongs — that's what makes the system scalable.

## The Hierarchy

### Atoms — Single-responsibility UI primitives

An atom is the smallest meaningful UI element. It does one thing and has no awareness of its context. Atoms are the foundation everything else builds on.

**What qualifies as an atom:**
- Renders a single visual concept (a badge, an icon, a divider, a label)
- Takes only primitive/value-type inputs (String, Color, Bool, CGFloat, enums)
- Has zero business logic — purely presentational
- Never reads from Environment or stores

**SwiftUI patterns for atoms:**
- Small structs, typically 10–30 lines
- Use computed properties for style variants rather than complex switch statements in `body`
- Proportional sizing (e.g., `size * 0.5`) so atoms scale naturally

```swift
// Atom: Colored SF Symbol in a rounded square
struct IconBadge: View {
    let icon: String
    let color: Color
    var size: CGFloat = 28

    var body: some View {
        Image(systemName: icon)
            .font(.system(size: size * 0.5, weight: .medium))
            .foregroundStyle(color)
            .frame(width: size, height: size)
            .background(color.opacity(0.12))
            .clipShape(RoundedRectangle(cornerRadius: size * 0.21))
    }
}
```

```swift
// Atom: Capsule-shaped status indicator driven by an enum
struct StatePill: View {
    let text: String
    let color: Color

    var body: some View {
        Text(text)
            .font(.caption2.weight(.medium))
            .foregroundStyle(color)
            .padding(.horizontal, 8)
            .padding(.vertical, 3)
            .background(color.opacity(0.12))
            .clipShape(Capsule())
    }
}
```

**Common atoms:** badges, pills, dividers, icon wrappers, character counters, section headers (text-only), card backgrounds, simple labels.

### Molecules — Functional combinations of atoms

A molecule combines 2–3 atoms (or atom-level elements) into a unit that serves a single user purpose. The key test: *does this combination appear in multiple places?*

**What qualifies as a molecule:**
- Combines atoms into a meaningful group (icon + label + value)
- Serves one user-facing function (show info, trigger action, display status)
- May accept closures for actions, but doesn't manage state itself
- Can accept domain types if they simplify the API, but the view itself stays presentational

```swift
// Molecule: Label-value pair for detail screens
struct InfoRow: View {
    let label: String
    let value: String
    var valueColor: Color = .primary

    var body: some View {
        HStack {
            Text(label)
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Spacer()
            Text(value)
                .font(.subheadline)
                .foregroundStyle(valueColor)
        }
        .padding(16)
    }
}
```

```swift
// Molecule: Tappable card with icon, title, and subtitle
struct QuickActionCard: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(alignment: .leading, spacing: 12) {
                Image(systemName: icon)
                    .font(.system(size: 24))
                    .foregroundStyle(color)

                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.subheadline.weight(.semibold))
                    Text(subtitle)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(16)
            .background(Color(.secondarySystemGroupedBackground))
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
        .buttonStyle(.plain)
    }
}
```

**Common molecules:** info rows, action buttons with labels, search bars, form fields with validation, stat cards, option/toggle rows, tip views.

### Organisms — Complex, self-contained UI sections

An organism is a distinct section of the interface that could stand alone. It composes multiple molecules (and atoms) into a cohesive unit. Organisms are where you introduce `@ViewBuilder` content slots and section-level structure.

**What qualifies as an organism:**
- Represents a visually distinct region (a section, a card group, a toolbar)
- Composes multiple molecules into a layout
- May use `@ViewBuilder` for content injection
- May read from `@Environment` for contextual data
- Can manage local UI state (`@State` for expand/collapse, selection, etc.)

```swift
// Organism: Collapsible content section with header
struct ContentSection<Content: View>: View {
    let title: String
    let subtitle: String?
    let icon: String
    let iconColor: Color
    @ViewBuilder let content: Content

    @State private var isExpanded = true

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header (molecule-level composition)
            Button { withAnimation { isExpanded.toggle() } } label: {
                HStack(spacing: 10) {
                    IconBadge(icon: icon, color: iconColor)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(title).font(.headline)
                        if let subtitle {
                            Text(subtitle).font(.caption).foregroundStyle(.secondary)
                        }
                    }
                    Spacer()
                    Image(systemName: "chevron.right")
                        .rotationEffect(.degrees(isExpanded ? 90 : 0))
                        .foregroundStyle(.secondary)
                }
            }
            .buttonStyle(.plain)
            .padding(16)

            if isExpanded {
                content.padding(.horizontal, 16).padding(.bottom, 16)
            }
        }
        .background(Color(.secondarySystemGroupedBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
```

**Common organisms:** content sections, form groups, navigation bars, card lists, detail panels, metric dashboards, grouped settings.

### Templates — Page-level layout scaffolding

A template defines the spatial arrangement of organisms on a screen. It's the skeleton — it knows *where* things go but not *what specific data* fills them. Templates use generics and `@ViewBuilder` heavily.

**What qualifies as a template:**
- Defines the overall page structure (ScrollView, navigation, toolbars)
- Arranges organism-level slots
- Handles page-level concerns: loading states, empty states, error states
- Does NOT contain specific data — that's the Page's job

```swift
// Template: Standard detail page layout
struct DetailPageTemplate<
    Header: View,
    Content: View,
    Actions: View
>: View {
    @ViewBuilder let header: Header
    @ViewBuilder let content: Content
    @ViewBuilder let actions: Actions
    let isLoading: Bool

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                header
                if isLoading {
                    ProgressView().frame(maxWidth: .infinity, minHeight: 200)
                } else {
                    content
                }
            }
            .padding()
        }
        .safeAreaInset(edge: .bottom) {
            actions
                .padding(.horizontal)
                .padding(.bottom, 8)
        }
    }
}
```

### Pages — Templates filled with real data

A page is a specific instance of a template, wired to real data and business logic. This is where `@Observable` objects, `@Environment`, and navigation live.

```swift
// Page: App detail screen using the DetailPageTemplate
struct AppDetailPage: View {
    let app: AppEntity
    @Environment(\.appRepository) private var repository
    @State private var isLoading = true
    @State private var metrics: AppMetrics?

    var body: some View {
        DetailPageTemplate(
            header: { AppHeaderOrganism(app: app) },
            content: {
                if let metrics {
                    MetricsDashboardOrganism(metrics: metrics)
                    RecentReviewsOrganism(appId: app.id)
                }
            },
            actions: {
                QuickActionCard(title: "View in App Store", subtitle: "Open external link",
                    icon: "arrow.up.forward.app", color: .blue) { /* open URL */ }
            },
            isLoading: isLoading
        )
        .task { metrics = try? await repository.fetchMetrics(for: app.id); isLoading = false }
    }
}
```

## Directory Structure

Organize components by atomic level within each module:

```
Sources/
├── Components/
│   ├── Atoms/           # IconBadge, StatePill, SectionHeader, ListDivider
│   ├── Molecules/       # InfoRow, QuickActionCard, ActionRow, OptionRow
│   └── Organisms/       # ContentSection, MetricsDashboard, ReviewsList
├── Templates/           # DetailPageTemplate, ListPageTemplate
└── Pages/               # AppDetailPage, SettingsPage
```

For a shared design system module used across targets:

```
DesignSystemModule/
├── Sources/
│   ├── Atoms/
│   ├── Molecules/
│   ├── Organisms/
│   └── Modifiers/       # ViewModifiers that cut across levels
```

## Decision Guide: Where Does This Component Go?

Ask these questions in order:

1. **Does it render a single visual element with no children?** → Atom
2. **Does it combine 2–3 simple elements for one purpose?** → Molecule
3. **Does it represent a distinct UI section with internal structure?** → Organism
4. **Does it define page layout without specific data?** → Template
5. **Does it wire a template to real data and business logic?** → Page

**Gray areas:**
- A section header with just icon + title = **Atom** (single concept: "label this section")
- A section header with icon + title + subtitle + action button = **Molecule** (multiple atoms combined)
- A collapsible section with header + content slot = **Organism** (manages state, contains others)

## SwiftUI-Specific Patterns

### ViewModifiers as cross-cutting atoms

When a visual treatment applies across levels (card styling, glass effects), extract it as a `ViewModifier` rather than duplicating styling:

```swift
struct CardBackgroundModifier: ViewModifier {
    var cornerRadius: CGFloat = 12

    func body(content: Content) -> some View {
        content
            .padding(16)
            .background(Color(.secondarySystemGroupedBackground))
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
    }
}

extension View {
    func cardBackground(cornerRadius: CGFloat = 12) -> some View {
        modifier(CardBackgroundModifier(cornerRadius: cornerRadius))
    }
}
```

### @ViewBuilder for content injection

Organisms and templates should accept content through `@ViewBuilder` closures rather than concrete child types. This keeps higher-level components flexible without creating tight coupling:

```swift
struct SectionContainer<Content: View>: View {
    let title: String
    @ViewBuilder let content: () -> Content

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title).font(.headline)
            content()
        }
    }
}
```

### Generics for type-safe composition

Use generics when a component needs to render different view types in specific slots:

```swift
struct HeaderDetailLayout<Header: View, Detail: View>: View {
    @ViewBuilder let header: () -> Header
    @ViewBuilder let detail: () -> Detail

    var body: some View {
        VStack(spacing: 16) {
            header()
            detail()
        }
    }
}
```

### Style enums for atom variants

When an atom supports multiple visual treatments, use an enum rather than multiple boolean flags:

```swift
struct ActionBadge: View {
    enum Style { case primary, secondary, destructive }

    let label: String
    let style: Style

    private var color: Color {
        switch style {
        case .primary: .blue
        case .secondary: .secondary
        case .destructive: .red
        }
    }
    // ...
}
```

### Previews at every level

Every component should have a `#Preview` block. Atoms preview in isolation, molecules with sample data, organisms with mock content:

```swift
#Preview("IconBadge Sizes") {
    HStack(spacing: 12) {
        IconBadge(icon: "star.fill", color: .yellow, size: 24)
        IconBadge(icon: "star.fill", color: .yellow, size: 32)
        IconBadge(icon: "star.fill", color: .yellow, size: 44)
    }
    .padding()
}
```

## Anti-Patterns

- **Fat atoms**: If an atom has more than ~30 lines of body, it's probably a molecule
- **Molecules with @State**: Local UI state belongs in organisms, not molecules. Molecules receive and display, they don't manage
- **Organisms that know about navigation**: Navigation is a page concern. Organisms signal intent via closures, pages handle routing
- **Templates with hardcoded data**: If you see real strings or API calls in a template, the data should move up to the page
- **Skipping levels**: Don't jump from atoms to pages. The intermediate levels exist to manage complexity — skipping them creates monolithic views that are hard to reuse and test

## File Header Convention

Mark each file's atomic level in the header comment for quick identification:

```swift
//
//  IconBadge.swift
//  ModuleName
//
//  Atom: Colored SF Symbol in a rounded square
//
```

This makes it easy to verify a file is in the right directory and understand its role at a glance.