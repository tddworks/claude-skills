# iOS Components Reference

Complete documentation for all iOS UX prototype components.

## Table of Contents

1. [Phone Frame Variants](#phone-frame-variants)
2. [Navigation Patterns](#navigation-patterns)
3. [List Components](#list-components)
4. [Form Components](#form-components)
5. [Grid Components](#grid-components)
6. [Tab Components](#tab-components)
7. [Status Indicators](#status-indicators)
8. [Annotations](#annotations)
9. [Layout Helpers](#layout-helpers)

---

## Phone Frame Variants

### iPhone 14 Pro (Default)
```html
<div class="phone-frame">
  <div class="phone-screen">
    <div class="dynamic-island"></div>
    <div class="screen-layout">
      <!-- content -->
    </div>
  </div>
</div>
```

### Custom Size (override CSS variables)
```css
:root {
  --phone-width: 390px;  /* iPhone 14 Pro Max */
  --phone-height: 844px;
}
```

---

## Navigation Patterns

### Large Title (Root screens)
```html
<div class="nav-large">
  <h1>Screen Title</h1>
</div>
```

### Inline with Back (Pushed screens)
```html
<div class="nav-inline">
  <div class="nav-inline-left">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
      <path d="M15 18l-6-6 6-6"/>
    </svg>
    <span>Back</span>
  </div>
  <span class="nav-inline-title">Title</span>
  <span class="nav-inline-right">Done</span>
</div>
```

### Inline with Badge
```html
<div class="nav-inline">
  <div class="nav-inline-left"><!-- back --></div>
  <span class="nav-inline-title">App Info</span>
  <span class="language-tag">English</span>
</div>
```

---

## List Components

### App List Row
```html
<div class="app-list">
  <!-- Normal row -->
  <div class="app-row">
    <div class="app-icon blue">A</div>
    <div class="app-details">
      <div class="app-name">App Name</div>
      <div class="app-meta">v1.0.0 · iOS</div>
    </div>
    <span class="app-badge ready">Ready</span>
    <span class="chevron">›</span>
  </div>

  <!-- Selected row -->
  <div class="app-row selected">
    <!-- same content -->
  </div>
</div>
```

**App Icon Colors**: `.blue`, `.purple`, `.orange`, `.green`, `.cyan`, `.pink`

**Badge Types**:
- `.app-badge.review` - Orange (In Review)
- `.app-badge.ready` - Green (Ready for Sale)
- `.app-badge.draft` - Purple (Draft)
- `.app-badge.rejected` - Red (Rejected)

### Settings List
```html
<div class="list-group">
  <div class="list-row">
    <div class="list-icon yellow">⭐</div>
    <span>Reviews</span>
    <span class="chevron">›</span>
  </div>
  <div class="list-row">
    <div class="list-icon green">✓</div>
    <span>Verified</span>
    <span class="value">Yes</span>
    <span class="chevron">›</span>
  </div>
</div>
```

**Icon Colors**: `.blue`, `.purple`, `.orange`, `.green`, `.yellow`, `.red`, `.gray`

---

## Form Components

### Read-only Form
```html
<div class="form-card">
  <div class="form-row">
    <div class="form-row-icon">📦</div>
    <span class="form-row-label">Bundle ID</span>
    <span class="form-row-value">com.app.name</span>
  </div>
</div>
```

### Editable Form
```html
<div class="form-card">
  <div class="form-input">
    <label>App Name</label>
    <input type="text" value="My App">
  </div>
  <div class="form-input" style="border-top: 0.5px solid var(--separator);">
    <label>Subtitle</label>
    <input type="text" placeholder="Optional subtitle">
  </div>
</div>
```

### Form Section with Header
```html
<div class="form-section">
  <div class="form-header">
    <span>📱</span>
    <span>App Identity</span>
  </div>
  <div class="form-card">
    <!-- form rows -->
  </div>
</div>
```

---

## Grid Components

### Action Card Grid
```html
<div class="action-grid">
  <div class="action-card">
    <div class="action-icon blue">📱</div>
    <h3>App Info</h3>
    <p>Metadata & Settings</p>
  </div>
  <div class="action-card highlighted">
    <div class="action-icon purple">🖼️</div>
    <h3>Screenshots</h3>
    <p>App Store Media</p>
  </div>
</div>
```

**Icon backgrounds**: `.blue`, `.purple`, `.orange`, `.cyan`, `.green`, `.yellow`, `.red`

### Screenshots Grid
```html
<div class="screenshots-grid">
  <div class="screenshot-slot filled"></div>
  <div class="screenshot-slot">
    <span class="plus">+</span>
    <span class="label">Add</span>
  </div>
</div>
<div class="screenshot-count">3 of 10 screenshots</div>
```

---

## Tab Components

### Segmented Control (3-5 items)
Use when you have a fixed number of equal options.
```html
<div class="segmented-control">
  <div class="segment active">Essentials</div>
  <div class="segment">Story</div>
  <div class="segment">Version</div>
</div>
```

### Scrollable Tabs (many items)
Use when options may overflow or vary in count.
```html
<div class="scrollable-tabs">
  <div class="scroll-tab active">iPhone 6.7"</div>
  <div class="scroll-tab">iPhone 6.5"</div>
  <div class="scroll-tab">iPad Pro 12.9"</div>
  <div class="scroll-tab">iPad Pro 11"</div>
  <div class="scroll-tab">Mac</div>
</div>
```

### Bottom Tab Bar
Use sparingly - only for top-level app navigation.
```html
<div class="tab-bar">
  <div class="tab-item active">
    <span class="tab-icon">🏠</span>
    <span class="tab-label">Home</span>
  </div>
  <div class="tab-item">
    <span class="tab-icon">📱</span>
    <span class="tab-label">Apps</span>
  </div>
</div>
```

---

## Status Indicators

### Version/Status Pills
```html
<div class="status-row">
  <span class="version-pill">v2.1.0</span>
  <span class="status-pill">In Review</span>
</div>
```

### Language Tag
```html
<span class="language-tag">English</span>
```

### Highlight Box (Tips/Info)
```html
<div class="highlight-box">
  <h4>💡 Tip</h4>
  <p>The first 3 screenshots are most important.</p>
</div>
```

---

## Annotations

Position annotations relative to the phone frame using absolute positioning.

### Arrow Directions
```html
<!-- Arrow points right (annotation on left side of target) -->
<div class="annotation right" style="top: 200px; left: -150px;">
  Tap here →
</div>

<!-- Arrow points left (annotation on right side) -->
<div class="annotation left" style="top: 200px; right: -150px;">
  ← Select this
</div>

<!-- Arrow points down (annotation above target) -->
<div class="annotation bottom" style="bottom: -50px; left: 50%; transform: translateX(-50%);">
  Key feature!
</div>

<!-- Arrow points up (annotation below target) -->
<div class="annotation top" style="top: -50px; left: 50%; transform: translateX(-50%);">
  Notice this
</div>
```

---

## Layout Helpers

### Page Header
```html
<header class="page-header">
  <h1>User Journey Title</h1>
  <p>Description of the flow being documented</p>
</header>
```

### Journey Row
```html
<div class="journey-row">
  <div class="journey-step"><!-- phone --></div>
  <div class="flow-arrow"><!-- svg --></div>
  <div class="journey-step"><!-- phone --></div>
</div>
```

### Section Divider
```html
<div class="section-divider">
  <div class="section-divider-line"></div>
  <span class="section-divider-text">Alternative Flow</span>
  <div class="section-divider-line"></div>
</div>
```

### Insight Box (Summary)
```html
<div class="insight-box">
  <h3>Key Design Pattern</h3>
  <div class="insight-grid">
    <div class="insight-item">
      <div class="icon">📋</div>
      <h4>App Info</h4>
      <p>Segmented Control at top</p>
    </div>
  </div>
</div>
```

---

## Complete Example Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>App User Journey</title>
  <style>
    /* Paste contents of ios-design-system.css here */
  </style>
</head>
<body>
  <div class="page">
    <header class="page-header">
      <h1>App Name User Journey</h1>
      <p>Navigate from list to detail to action</p>
    </header>

    <div class="journey-row">
      <!-- Step 1 -->
      <div class="journey-step">
        <div class="step-header">
          <div class="step-number">1</div>
          <span class="step-title">App List</span>
        </div>
        <div class="phone-frame">
          <div class="phone-screen">
            <div class="dynamic-island"></div>
            <div class="screen-layout">
              <div class="status-bar">
                <span class="status-bar-left">9:41</span>
                <span class="status-bar-right">📶 📡 🔋</span>
              </div>
              <div class="nav-large"><h1>My Apps</h1></div>
              <div class="scroll-content">
                <div class="app-list">
                  <div class="app-row selected">
                    <div class="app-icon blue">A</div>
                    <div class="app-details">
                      <div class="app-name">MyApp</div>
                      <div class="app-meta">v1.0 · iOS</div>
                    </div>
                    <span class="app-badge ready">Ready</span>
                    <span class="chevron">›</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flow-arrow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </div>

      <!-- Step 2 -->
      <div class="journey-step">
        <div class="step-header">
          <div class="step-number">2</div>
          <span class="step-title">Dashboard</span>
        </div>
        <div class="phone-frame">
          <!-- ... -->
        </div>
      </div>
    </div>
  </div>
</body>
</html>
```
