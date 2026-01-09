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
2. Structure: page header → journey rows → phone frames with content
3. Add flow arrows between screens and annotations for callouts

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
      <div class="dynamic-island"></div>
      <div class="screen-layout">
        <div class="status-bar">
          <span class="status-bar-left">9:41</span>
          <span class="status-bar-right">📶 📡 🔋</span>
        </div>
        <!-- Screen content here -->
      </div>
    </div>
  </div>
</div>
```

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
    <div class="action-icon blue">📱</div>
    <h3>Feature</h3>
    <p>Description</p>
  </div>
</div>
```

### List Group
```html
<div class="list-group">
  <div class="list-row">
    <div class="list-icon yellow">⭐</div>
    <span>Setting</span>
    <span class="chevron">›</span>
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
- `references/ios-components.md` - Full component documentation with all variants
