---
name: swiftui-atomic-design
description: |
  Guide for building SwiftUI components using Brad Frost's Atomic Design methodology — organizing views into Atoms, Molecules, Organisms, Templates, and Pages with Design Tokens for theming. Use this skill whenever building new SwiftUI UI components, refactoring existing views into reusable pieces, creating a design system, or organizing a component library. Also trigger when the user mentions "atomic design", "design system", "component hierarchy", "reusable components", "atoms and molecules", "design tokens", or wants to decompose a complex SwiftUI view into smaller, composable parts, or needs to implement theming/customization across a SwiftUI app.
---

# SwiftUI Atomic Design System

Atomic Design is Brad Frost's methodology for building UI systems from small, composable pieces. In SwiftUI, this maps naturally to the framework's declarative, compositional view architecture. The hierarchy flows from simple to complex:

**Design Tokens → Atoms → Molecules → Organisms → Templates → Pages**

Each level composes the one below it. Design Tokens provide the visual foundation that all levels reference. The discipline is knowing *where* a component belongs — that's what makes the system scalable, consistent, and maintainable.

## Design Tokens — The Visual Foundation

Design tokens are the centralized source of truth for all visual properties: colors, typography, spacing. They sit *beneath* atoms — every component references tokens rather than hardcoding values. This ensures consistency across the entire design system and makes sweeping visual changes (rebranding, dark mode, accessibility) a single-point update.

**Why tokens matter:**
- Change a brand color once, and it propagates everywhere
- Enable theming (light/dark, high contrast) without touching component code
- Create a shared vocabulary between design and development
- Prevent visual drift as the codebase grows

```swift
// Design Tokens: Centralized visual constants
struct DesignTokens {
    struct Colors {
        static let primary = Color("PrimaryColor")
        static let secondary = Color("SecondaryColor")
        static let background = Color("BackgroundColor")
        static let surface = Color(.secondarySystemGroupedBackground)
        static let textPrimary = Color.primary
        static let textSecondary = Color.secondary
    }

    struct Typography {
        static let largeTitle = Font.largeTitle.weight(.bold)
        static let title = Font.title2.weight(.semibold)
        static let headline = Font.headline.weight(.medium)
        static let body = Font.body
        static let caption = Font.caption
        static let captionBold = Font.caption2.weight(.medium)
    }

    struct Spacing {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 16
        static let lg: CGFloat = 24
        static let xl: CGFloat = 32
    }

    struct Radius {
        static let sm: CGFloat = 8
        static let md: CGFloat = 12
        static let lg: CGFloat = 16
    }
}
```

**Common token categories:** colors, typography (font families, sizes, weights), spacing (margins, padding), corner radii, shadows/elevations, animation durations, opacity values.

## Theming and Customization

Tokens become powerful when combined with SwiftUI's Environment system for runtime theming. Define theme variants and inject them through the environment so every component adapts automatically.

```swift
// Theme definition using tokens
struct AppTheme {
    let primaryColor: Color
    let secondaryColor: Color
    let backgroundColor: Color
    let textColor: Color

    static let light = AppTheme(
        primaryColor: .blue,
        secondaryColor: .gray,
        backgroundColor: .white,
        textColor: .black
    )

    static let dark = AppTheme(
        primaryColor: .cyan,
        secondaryColor: .gray,
        backgroundColor: .black,
        textColor: .white
    )
}

// Environment integration
struct AppThemeKey: EnvironmentKey {
    static let defaultValue: AppTheme = .light
}

extension EnvironmentValues {
    var appTheme: AppTheme {
        get { self[AppThemeKey.self] }
        set { self[AppThemeKey.self] = newValue }
    }
}

// Apply theme to a view hierarchy
struct ThemedModifier: ViewModifier {
    let theme: AppTheme
    func body(content: Content) -> some View {
        content.environment(\.appTheme, theme)
    }
}

extension View {
    func themed(_ theme: AppTheme) -> some View {
        modifier(ThemedModifier(theme: theme))
    }
}
```

Components read from `@Environment(\.appTheme)` instead of hardcoding colors, making the entire UI theme-switchable.

## The Hierarchy

### Atoms — Single-responsibility UI primitives

An atom is the smallest meaningful UI element. It does one thing and has no awareness of its context. Atoms reference Design Tokens for all visual properties — they never hardcode colors, fonts, or spacing.

**What qualifies as an atom:**
- Renders a single visual concept (a badge, an icon, a divider, a label, a button)
- Takes only primitive/value-type inputs (String, Color, Bool, CGFloat, enums)
- Has zero business logic — purely presentational
- Never reads from Environment or stores (except theme tokens)
- References Design Tokens for all visual values

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
// Atom: Capsule-shaped status indicator
struct StatePill: View {
    let text: String
    let color: Color

    var body: some View {
        Text(text)
            .font(DesignTokens.Typography.captionBold)
            .foregroundStyle(color)
            .padding(.horizontal, DesignTokens.Spacing.sm)
            .padding(.vertical, 3)
            .background(color.opacity(0.12))
            .clipShape(Capsule())
    }
}
```

```swift
// Atom: Reusable primary button
struct PrimaryButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(DesignTokens.Typography.headline)
                .foregroundColor(.white)
                .padding(.horizontal, DesignTokens.Spacing.lg)
                .padding(.vertical, DesignTokens.Spacing.md)
                .background(DesignTokens.Colors.primary)
                .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.sm))
        }
    }
}
```

```swift
// Atom: Styled text with token-based typography
struct TitleText: View {
    let text: String

    var body: some View {
        Text(text)
            .font(DesignTokens.Typography.title)
            .foregroundStyle(DesignTokens.Colors.textPrimary)
    }
}
```

**Common atoms:** badges, pills, dividers, icon wrappers, character counters, section headers (text-only), card backgrounds, simple labels, primary/secondary buttons, text field wrappers.

### Molecules — Functional combinations of atoms

A molecule combines 2–3 atoms (or atom-level elements) into a unit that serves a single user purpose. Molecules are the backbone of the design system — they create the reusable patterns that appear throughout the app. The key test: *does this combination appear in multiple places?*

**What qualifies as a molecule:**
- Combines atoms into a meaningful group (icon + label + value)
- Serves one user-facing function (show info, trigger action, display status)
- May accept closures for actions, but doesn't manage state itself
- Can accept `@Binding` for two-way data flow (e.g., text fields)
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
                .font(DesignTokens.Typography.body)
                .foregroundStyle(DesignTokens.Colors.textSecondary)
            Spacer()
            Text(value)
                .font(DesignTokens.Typography.body)
                .foregroundStyle(valueColor)
        }
        .padding(DesignTokens.Spacing.md)
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
            VStack(alignment: .leading, spacing: DesignTokens.Spacing.sm) {
                Image(systemName: icon)
                    .font(.system(size: 24))
                    .foregroundStyle(color)

                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(DesignTokens.Typography.headline)
                        .foregroundStyle(DesignTokens.Colors.textPrimary)
                    Text(subtitle)
                        .font(DesignTokens.Typography.caption)
                        .foregroundStyle(DesignTokens.Colors.textSecondary)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(DesignTokens.Spacing.md)
            .background(DesignTokens.Colors.surface)
            .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.md))
        }
        .buttonStyle(.plain)
    }
}
```

```swift
// Molecule: Search form combining label, text field, and button atoms
struct SearchBar: View {
    @Binding var query: String
    var placeholder: String = "Search..."
    var onSearch: () -> Void

    var body: some View {
        HStack(spacing: DesignTokens.Spacing.sm) {
            Image(systemName: "magnifyingglass")
                .foregroundStyle(DesignTokens.Colors.textSecondary)

            TextField(placeholder, text: $query)
                .font(DesignTokens.Typography.body)

            if !query.isEmpty {
                Button { query = "" } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(DesignTokens.Colors.textSecondary)
                }
            }
        }
        .padding(DesignTokens.Spacing.sm)
        .background(DesignTokens.Colors.surface)
        .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.sm))
        .onSubmit(onSearch)
    }
}
```

**Common molecules:** info rows, action buttons with labels, search bars, form fields with validation, stat cards, option/toggle rows, tip views, labeled input fields.

### Organisms — Complex, self-contained UI sections

An organism is a distinct section of the interface that could stand alone. It composes multiple molecules (and atoms) into a cohesive unit. Organisms form the significant parts of your UI — login forms, navigation bars, metric dashboards. This is where you introduce `@ViewBuilder` content slots and section-level structure.

**What qualifies as an organism:**
- Represents a visually distinct region (a section, a card group, a toolbar, a form)
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
            Button { withAnimation { isExpanded.toggle() } } label: {
                HStack(spacing: 10) {
                    IconBadge(icon: icon, color: iconColor)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(title).font(DesignTokens.Typography.headline)
                        if let subtitle {
                            Text(subtitle).font(DesignTokens.Typography.caption)
                                .foregroundStyle(DesignTokens.Colors.textSecondary)
                        }
                    }
                    Spacer()
                    Image(systemName: "chevron.right")
                        .rotationEffect(.degrees(isExpanded ? 90 : 0))
                        .foregroundStyle(DesignTokens.Colors.textSecondary)
                }
            }
            .buttonStyle(.plain)
            .padding(DesignTokens.Spacing.md)

            if isExpanded {
                content
                    .padding(.horizontal, DesignTokens.Spacing.md)
                    .padding(.bottom, DesignTokens.Spacing.md)
            }
        }
        .background(DesignTokens.Colors.surface)
        .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.md))
    }
}
```

```swift
// Organism: Login form composing labeled input molecules
struct LoginForm: View {
    @State private var username = ""
    @State private var password = ""
    var onLogin: (String, String) -> Void

    var body: some View {
        VStack(spacing: DesignTokens.Spacing.lg) {
            LabeledInputField(label: "Username", text: $username)
            LabeledInputField(label: "Password", text: $password, isSecure: true)
            PrimaryButton(title: "Login") {
                onLogin(username, password)
            }
        }
        .padding(DesignTokens.Spacing.lg)
        .background(DesignTokens.Colors.surface)
        .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.md))
    }
}
```

**Common organisms:** content sections, form groups, navigation bars, card lists, detail panels, metric dashboards, grouped settings, login forms.

### Templates — Page-level layout scaffolding

A template defines the spatial arrangement of organisms on a screen. It's the skeleton — it knows *where* things go but not *what specific data* fills them. Templates use generics and `@ViewBuilder` heavily. They handle page-level concerns like loading states, empty states, and error states.

**What qualifies as a template:**
- Defines the overall page structure (ScrollView, navigation, toolbars)
- Arranges organism-level slots using generic view parameters
- Handles page-level concerns: loading states, empty states, error states
- Does NOT contain specific data — that's the Page's job

```swift
// Template: Standard detail page layout with header, content, and actions
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
            VStack(spacing: DesignTokens.Spacing.md) {
                header
                if isLoading {
                    ProgressView()
                        .frame(maxWidth: .infinity, minHeight: 200)
                } else {
                    content
                }
            }
            .padding(DesignTokens.Spacing.md)
        }
        .background(DesignTokens.Colors.background)
        .safeAreaInset(edge: .bottom) {
            actions
                .padding(.horizontal, DesignTokens.Spacing.md)
                .padding(.bottom, DesignTokens.Spacing.sm)
        }
    }
}
```

```swift
// Template: Main layout with navigation bar and content area
struct MainLayout<Content: View>: View {
    let title: String
    @ViewBuilder let content: Content

    var body: some View {
        VStack(spacing: 0) {
            // Navigation bar (organism)
            HStack {
                Image(systemName: "arrow.left")
                Spacer()
                Text(title).font(DesignTokens.Typography.headline)
                Spacer()
                Image(systemName: "gear")
            }
            .padding(DesignTokens.Spacing.md)
            .background(DesignTokens.Colors.primary)

            content
                .padding(DesignTokens.Spacing.md)
            Spacer()
        }
        .background(DesignTokens.Colors.background)
    }
}
```

### Pages — Templates filled with real data

A page is a specific instance of a template, wired to real data and business logic. This is where `@Observable` objects, `@Environment`, and navigation live. Pages are what users actually interact with — they assemble templates, inject data, and handle user actions.

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
                QuickActionCard(
                    title: "View in App Store",
                    subtitle: "Open external link",
                    icon: "arrow.up.forward.app",
                    color: .blue
                ) { /* open URL */ }
            },
            isLoading: isLoading
        )
        .task {
            metrics = try? await repository.fetchMetrics(for: app.id)
            isLoading = false
        }
    }
}
```

```swift
// Page: Login page using MainLayout template
struct LoginPage: View {
    var body: some View {
        MainLayout(title: "Welcome") {
            LoginForm { username, password in
                // Handle authentication
            }
        }
    }
}
```

## Directory Structure

Organize components by atomic level within each module:

```
Sources/
├── DesignTokens/        # Colors, Typography, Spacing, Radius
├── Components/
│   ├── Atoms/           # IconBadge, StatePill, PrimaryButton, TitleText
│   ├── Molecules/       # InfoRow, QuickActionCard, SearchBar, ActionRow
│   └── Organisms/       # ContentSection, LoginForm, MetricsDashboard
├── Templates/           # DetailPageTemplate, MainLayout, ListPageTemplate
└── Pages/               # AppDetailPage, LoginPage, SettingsPage
```

For a shared design system module used across targets:

```
DesignSystemModule/
├── Sources/
│   ├── Tokens/          # DesignTokens, AppTheme
│   ├── Atoms/
│   ├── Molecules/
│   ├── Organisms/
│   └── Modifiers/       # ViewModifiers that cut across levels
```

## Decision Guide: Where Does This Component Go?

Ask these questions in order:

1. **Is it a visual constant (color, font, spacing)?** → Design Token
2. **Does it render a single visual element with no children?** → Atom
3. **Does it combine 2–3 simple elements for one purpose?** → Molecule
4. **Does it represent a distinct UI section with internal structure?** → Organism
5. **Does it define page layout without specific data?** → Template
6. **Does it wire a template to real data and business logic?** → Page

**Gray areas:**
- A section header with just icon + title = **Atom** (single concept: "label this section")
- A section header with icon + title + subtitle + action button = **Molecule** (multiple atoms combined)
- A collapsible section with header + content slot = **Organism** (manages state, contains others)
- A labeled text field = **Molecule** (combines label atom + text field atom)
- A login form with multiple fields + button = **Organism** (composes multiple molecules, manages `@State`)

## SwiftUI-Specific Patterns

### ViewModifiers as cross-cutting atoms

When a visual treatment applies across levels (card styling, glass effects), extract it as a `ViewModifier` rather than duplicating styling. This keeps atoms clean and ensures visual consistency:

```swift
struct CardBackgroundModifier: ViewModifier {
    var cornerRadius: CGFloat = DesignTokens.Radius.md

    func body(content: Content) -> some View {
        content
            .padding(DesignTokens.Spacing.md)
            .background(DesignTokens.Colors.surface)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
    }
}

extension View {
    func cardBackground(cornerRadius: CGFloat = DesignTokens.Radius.md) -> some View {
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
        VStack(alignment: .leading, spacing: DesignTokens.Spacing.sm) {
            Text(title).font(DesignTokens.Typography.headline)
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
        VStack(spacing: DesignTokens.Spacing.md) {
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
        case .primary: DesignTokens.Colors.primary
        case .secondary: DesignTokens.Colors.secondary
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
    HStack(spacing: DesignTokens.Spacing.sm) {
        IconBadge(icon: "star.fill", color: .yellow, size: 24)
        IconBadge(icon: "star.fill", color: .yellow, size: 32)
        IconBadge(icon: "star.fill", color: .yellow, size: 44)
    }
    .padding()
}
```

## Best Practices

### Consistency and Scalability
- **Use Design Tokens everywhere**: Never hardcode colors, fonts, or spacing in components — always reference tokens
- **Component Library**: Build and maintain a library of reusable components at each atomic level
- **Naming Conventions**: Follow consistent naming that reflects the atomic level (e.g., `PrimaryButton` atom, `SearchBar` molecule, `LoginForm` organism)
- **Modular Design**: Break components into the smallest reusable modules
- **Documentation**: Include `#Preview` blocks and header comments describing atomic level and purpose
- **Regular Reviews**: Periodically audit components to ensure they're at the correct atomic level

### Theme Integration
- Components should read theme values from `@Environment` or Design Tokens, never hardcode brand colors
- Support light/dark mode through token-based theming
- Test all components against every theme variant in previews

## Anti-Patterns

- **Fat atoms**: If an atom has more than ~30 lines of body, it's probably a molecule
- **Molecules with @State**: Local UI state belongs in organisms, not molecules. Molecules receive and display, they don't manage
- **Organisms that know about navigation**: Navigation is a page concern. Organisms signal intent via closures, pages handle routing
- **Templates with hardcoded data**: If you see real strings or API calls in a template, the data should move up to the page
- **Skipping levels**: Don't jump from atoms to pages. The intermediate levels exist to manage complexity — skipping them creates monolithic views that are hard to reuse and test
- **Hardcoded visual values**: Using `Color.blue` or `.font(.system(size: 16))` directly in components instead of referencing Design Tokens defeats the purpose of the system
- **Token-less theming**: Building theme support without Design Tokens leads to scattered, inconsistent overrides

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