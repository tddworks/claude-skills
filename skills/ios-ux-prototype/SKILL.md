---
name: ios-ux-prototype
description: |
  Create interactive iOS/mobile app UX flow prototypes as HTML documents with realistic phone mockups.
  Use when: (1) Visualizing user journeys and navigation flows, (2) Creating mobile app wireframes,
  (3) Documenting screen-to-screen navigation patterns, (4) Presenting iOS UI designs with annotations,
  (5) Prototyping app architecture before implementation. Generates self-contained HTML files with
  iOS-native styling, phone frames, flow arrows, and callout annotations.
---

# iOS UX Prototype

Create interactive HTML prototypes showing mobile app user journeys with realistic iPhone mockups.

## Quick Start

1. Copy CSS from `assets/ios-design-system.css` into a new HTML file
2. Paste the sprite from `assets/sf-symbols.svg` once near the top of `<body>`
3. Structure: page header → journey rows → phone frames with content
4. Add flow arrows between screens and annotations for callouts

## iOS 26 Design (default)

Target the current iOS 26 design language — **Liquid Glass** surfaces and
**SF Symbols**. Apply these by default unless the user asks for an older look:

- **Liquid Glass floating tab bar** — use `.tab-bar` (now a translucent,
  blurred capsule detached from the screen edges; the active tab gets its own
  glass "lens" pill). Give scrolling screens `padding-bottom: 104px` on
  `.scroll-content` so rows clear the floating bar.
- **Liquid Glass nav/toolbar buttons** — use `.nav-glass-btn` (circular) or
  `.nav-glass-btn.text` (pill) for trailing actions, instead of plain text.
- **SF Symbols over emoji** — never use emoji for UI affordances, list icons,
  tab icons, or actions. Reference glyphs from the sprite:
  `<svg class="sf"><use href="#sf-house"/></svg>`. Glyphs inherit `currentColor`.
  - Country flags are the *only* allowed emoji (SF Symbols has no flag glyphs).
  - Need a glyph that isn't in the sprite? Add a new `<symbol>` (24×24 viewBox)
    following the existing pattern.
- Glassy segmented controls and translucent system alerts come for free in the CSS.

```html
<!-- iOS 26 large-title nav with a Liquid Glass action button -->
<div class="nav-large with-action">
  <h1>Proxies</h1>
  <span class="nav-glass-btn"><svg class="sf"><use href="#sf-plus"/></svg></span>
</div>

<!-- Liquid Glass floating tab bar with SF Symbols -->
<div class="tab-bar">
  <div class="tab-item active">
    <svg class="tab-ic"><use href="#sf-house"/></svg>
    <span class="tab-label">Home</span>
  </div>
  <div class="tab-item">
    <svg class="tab-ic"><use href="#sf-gear"/></svg>
    <span class="tab-label">Settings</span>
  </div>
</div>
```

Common sprite glyphs: `sf-house`, `sf-globe`, `sf-antenna`, `sf-gear`,
`sf-person`, `sf-magnifier`, `sf-bell`, `sf-star`, `sf-chevron`,
`sf-chevron-down`, `sf-back`, `sf-arrow-up/down`, `sf-refresh`, `sf-plus`,
`sf-check`, `sf-xmark`, `sf-ellipsis`, `sf-share`, `sf-trash`, `sf-heart`,
`sf-paintbrush`, `sf-doc`, `sf-clipboard`, `sf-folder`, `sf-photo`, `sf-qrcode`,
`sf-link`, `sf-list`, `sf-lock`, `sf-shield`, `sf-bolt`, `sf-power`, `sf-info`,
`sf-clock`, `sf-chart`, `sf-wifi`, `sf-nosign`, `sf-compass`.

## Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[App] User Journey</title>
  <style>/* Copy from assets/ios-design-system.css */</style>
</head>
<body>
  <div class="page">
    <header class="page-header">
      <h1>Journey Title</h1>
      <p>Description of the navigation flow</p>
    </header>
    <div class="journey-row">
      <!-- Journey steps with phone mockups -->
    </div>
  </div>
</body>
</html>
```

## Core Components

### Journey Step
```html
<div class="journey-step">
  <div class="step-header">
    <div class="step-number">1</div>
    <span class="step-title">SCREEN NAME</span>
  </div>
  <div class="phone-frame">
    <div class="phone-screen">
      <div class="screen-layout">
        <div class="status-bar">
          <span class="status-bar-left">9:41</span>
          <div class="status-bar-right">
            <!-- Signal bars -->
            <svg width="17" height="11" viewBox="0 0 17 11" fill="currentColor"><path d="M1 4.5C1 3.67 1.67 3 2.5 3h1C4.33 3 5 3.67 5 4.5v4C5 9.33 4.33 10 3.5 10h-1C1.67 10 1 9.33 1 8.5v-4zM6 3.5C6 2.67 6.67 2 7.5 2h1C9.33 2 10 2.67 10 3.5v5c0 .83-.67 1.5-1.5 1.5h-1C6.67 9 6 8.33 6 7.5v-5zM11 2.5c0-.83.67-1.5 1.5-1.5h1c.83 0 1.5.67 1.5 1.5v6c0 .83-.67 1.5-1.5 1.5h-1c-.83 0-1.5-.67-1.5-1.5v-6z"/></svg>
            <!-- WiFi -->
            <svg width="15" height="11" viewBox="0 0 15 11" fill="currentColor"><path d="M7.5 2.5a6.5 6.5 0 0 1 4.6 1.9.75.75 0 1 0 1.06-1.06A8 8 0 0 0 7.5 1a8 8 0 0 0-5.66 2.34.75.75 0 0 0 1.06 1.06A6.5 6.5 0 0 1 7.5 2.5zM7.5 5.5a4 4 0 0 1 2.83 1.17.75.75 0 1 0 1.06-1.06A5.5 5.5 0 0 0 7.5 4a5.5 5.5 0 0 0-3.89 1.61.75.75 0 0 0 1.06 1.06A4 4 0 0 1 7.5 5.5zM9.25 8.75a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0z"/></svg>
            <!-- Battery -->
            <svg width="25" height="12" viewBox="0 0 25 12" fill="currentColor"><rect x="0.5" y="0.5" width="21" height="11" rx="2.5" stroke="currentColor" fill="none"/><rect x="22" y="4" width="2" height="4" rx="1"/><rect x="2" y="2" width="17" height="7" rx="1"/></svg>
          </div>
        </div>
        <!-- Screen content here -->
      </div>
      <div class="home-indicator"></div>
    </div>
  </div>
</div>
```

**Note:** The phone frame uses a notch-style bezel by default. To use Dynamic Island style instead, add the `dynamic-island-style` class to `.phone-frame` and include a `<div class="dynamic-island"></div>` element.

### Flow Arrow
```html
<div class="flow-arrow">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M5 12h14M12 5l7 7-7 7"/>
  </svg>
</div>
```

### Annotation Callout
```html
<div class="annotation right" style="top: 200px; left: -150px;">Tap here →</div>
<!-- Positions: right, left, top, bottom (arrow direction) -->
```

## Navigation Patterns

### Large Title Nav
```html
<div class="nav-large"><h1>My Apps</h1></div>
```

### Inline Nav with Back
```html
<div class="nav-inline">
  <div class="nav-inline-left">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
      <path d="M15 18l-6-6 6-6"/>
    </svg>
    <span>Back</span>
  </div>
  <span class="nav-inline-title">Title</span>
  <span class="nav-inline-right">Edit</span>
</div>
```

### Segmented Control (3-5 options)
```html
<div class="segmented-control">
  <div class="segment active">Tab 1</div>
  <div class="segment">Tab 2</div>
  <div class="segment">Tab 3</div>
</div>
```

### Scrollable Tabs (many options)
```html
<div class="scrollable-tabs">
  <div class="scroll-tab active">iPhone 6.7"</div>
  <div class="scroll-tab">iPhone 6.5"</div>
  <div class="scroll-tab">iPad Pro</div>
</div>
```

## Content Components

### App List Row
```html
<div class="app-row selected">
  <div class="app-icon blue">A</div>
  <div class="app-details">
    <div class="app-name">App Name</div>
    <div class="app-meta">v1.0.0 · iOS</div>
  </div>
  <span class="app-badge review">In Review</span>
  <span class="chevron">›</span>
</div>
```

### Action Card Grid
```html
<div class="action-grid">
  <div class="action-card highlighted">
    <!-- tinted square: set the glyph color to match the tint -->
    <div class="action-icon blue" style="color:var(--blue)">
      <svg class="sf"><use href="#sf-bolt"/></svg>
    </div>
    <h3>Feature</h3>
    <p>Description</p>
  </div>
</div>
```

### List Group
```html
<div class="list-group">
  <div class="list-row">
    <!-- solid color square: glyph renders white via .list-icon -->
    <div class="list-icon yellow"><svg><use href="#sf-star"/></svg></div>
    <span>Setting</span>
    <span class="chevron"><svg><use href="#sf-chevron"/></svg></span>
  </div>
</div>
```

### Form Card
```html
<div class="form-card">
  <div class="form-row">
    <div class="form-row-icon">📦</div>
    <span class="form-row-label">Label</span>
    <span class="form-row-value">value</span>
  </div>
  <div class="form-input">
    <label>Field Name</label>
    <input type="text" value="Content">
  </div>
</div>
```

## Color Classes

**Icons**: `.blue`, `.purple`, `.orange`, `.cyan`, `.green`, `.yellow`, `.red`, `.gray`

**Badges**: `.app-badge.review` (orange), `.app-badge.ready` (green), `.app-badge.draft` (purple)

**Highlight**: `.action-card.highlighted` (blue border glow)

## Section Divider (Alternate Flows)

```html
<div class="section-divider">
  <div class="section-divider-line"></div>
  <span class="section-divider-text">Alternative Flow</span>
  <div class="section-divider-line"></div>
</div>
```

## Resources

- `assets/ios-design-system.css` - Complete CSS design system (copy into HTML)
- `assets/sf-symbols.svg` - SF Symbol sprite sheet (paste once into `<body>`)
- `references/ios-components.md` - Full component documentation with all variants
