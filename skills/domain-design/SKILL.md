---
name: domain-design
description: Visualize business domains as standalone HTML + inline-SVG artifacts using an opinionated editorial design system. Ships six domain-modelling types — Aggregate, Context Map, Event Storm, Context Canvas, Ubiquitous Language glossary, and Domain Model — for exploring DDD designs with stakeholders, capturing decisions from event-storming sessions, or documenting a bounded context in a repo. Use this skill whenever the user wants to sketch, explore, or document a business domain — triggered by mentions of DDD, domain-driven design, bounded contexts, aggregates, event storming, ubiquitous language, context mapping, or any request to "visualize the domain", "draw the model", "map the contexts", "show the aggregate", or "help me think through the business". Shares a skinnable style guide with diagram-design so technical and domain diagrams produced for the same project look like siblings.
license: MIT
---

# Domain Design

Generate domain-modelling artifacts as self-contained HTML files with inline SVG and CSS. One opinionated editorial design system, a first-run style-guide gate, six diagram types purpose-built for Domain-Driven Design conversations, and a taste gate that keeps output honest.

**What this skill is for.** Helping a user think through and document their business domain: what the aggregates are, where the bounded contexts sit, which events move through the system, which terms live in the ubiquitous language. It is a thinking and communication tool — every output is meant to be read by a human stakeholder, not executed.

**What it is not.** Not an architecture or technical diagram skill — reach for `diagram-design` if the user wants sequence diagrams, layered architecture, ER, flowcharts, or any of the 13 technical types there. These two skills share a style guide so they render as siblings when used in the same project.

---

## 0. First-time setup — style guide gate

**Before generating your first domain artifact in a new project, verify the style guide has been customized.**

Open [`references/style-guide.md`](references/style-guide.md) and check the default tokens. If they're still the shipped defaults (paper `#faf7f2`, ink `#1c1917`, accent `#b5523a` rust), **pause and ask the user**:

> *"This is your first domain-design artifact in this project. The style guide is still at the default (neutral stone + rust). Do you want to customize it to match your brand first? Options: (a) run onboarding — I'll pull colors and fonts from your website, (b) paste your tokens manually, (c) proceed with the default for now."*

Then branch:
- **(a)** → follow [`references/onboarding.md`](references/onboarding.md) to fetch the site, extract palette + fonts, propose a diff, and write `style-guide.md`.
- **(b)** → accept the user's tokens and write them into `style-guide.md` under a new "Custom tokens" section.
- **(c)** → proceed; optionally remind the user they can run onboarding later.

If `diagram-design` has already been onboarded in this project, `style-guide.md` will already be branded — detect this and skip the gate. The two skills intentionally share the same skin.

---

## 1. Philosophy

**The domain is the thing. Everything else is scaffolding.**

A good domain artifact does three jobs at once: it forces you to name things, it surfaces what you don't yet understand, and it leaves a trace a non-technical stakeholder can read. Anything that doesn't serve one of those jobs is clutter.

Applied to this skill:

- **Use the user's words, not yours.** If the user says "subscription", don't rename it "plan". Ubiquitous language is load-bearing — respect it. If the term is ambiguous, stop and ask.
- **Names before shapes.** The hardest part of domain modelling is naming. Resist the urge to draw 20 boxes and call them `Order1`, `Order2`, `OrderItem`. If you can't name it, don't box it.
- **One concept, one box.** Two boxes that always move together are one aggregate. Two value objects that share every field are one value object.
- **Coral is editorial, not a flag.** 1–2 focal elements per diagram — the aggregate root, the critical event, the core domain. Using it on 5 boxes erases the signal.
- **Density 4/10.** If it's over 9 boxes, it's probably two diagrams. Overview + detail, not one big chart.

The diagram is done when nothing can be removed.

---

## 2. When to use

Use when a reader will learn more about the **business** from a visual than from prose.

| Situation | Use |
|---|---|
| "Help me think through the X domain" | [Event Storm](references/type-event-storm.md) to discover, [Domain Model](references/type-domain-model.md) to structure |
| "What aggregates do we have here?" | [Aggregate](references/type-aggregate.md) per root + [Domain Model](references/type-domain-model.md) overview |
| "How do teams/systems relate?" | [Context Map](references/type-context-map.md) |
| "Summarize this bounded context" | [Context Canvas](references/type-context-canvas.md) |
| "I keep confusing these terms" | [Ubiquitous Language glossary](references/type-language.md) |
| "Document the rules for this aggregate" | [Aggregate](references/type-aggregate.md) with invariants band |

**Don't use for:**

- Technical architecture, sequence, ER, state machines, flowcharts → [`diagram-design`](../diagram-design/SKILL.md).
- UI wireframes → `ios-ux-prototype` / `app-design-concept`.
- Runtime flow of code (not business flow) → `diagram-design` sequence/architecture.
- "Just a list of terms with no structure" → write a markdown table; a diagram adds no value.

**First question to answer before drawing anything:** *Would the reader learn more from this visual than from a short prose paragraph, a markdown table, or a bullet list?* If no — don't draw.

---

## 3. Diagram types

### Selection guide

| If you're showing…                                                        | Use                     | Reference |
|---------------------------------------------------------------------------|-------------------------|-----------|
| One aggregate's structure (root + entities + value objects + invariants)  | **Aggregate**           | [type-aggregate.md](references/type-aggregate.md) |
| Multiple bounded contexts + how they integrate (ACL, OHS, shared kernel…) | **Context Map**         | [type-context-map.md](references/type-context-map.md) |
| Discovery: events, commands, policies, read models along a timeline       | **Event Storm**         | [type-event-storm.md](references/type-event-storm.md) |
| A single bounded context at a glance (purpose, language, boundaries)      | **Context Canvas**      | [type-context-canvas.md](references/type-context-canvas.md) |
| A glossary of domain terms with definitions + aliases                     | **Ubiquitous Language** | [type-language.md](references/type-language.md) |
| Several aggregates inside one context + how they relate                   | **Domain Model**        | [type-domain-model.md](references/type-domain-model.md) |

Rules of thumb:

- If a markdown table communicates the same thing, use the table.
- If two types overlap (domain model + aggregate), produce both: overview first, then one or two aggregate blow-ups.
- If the user is mid-event-storming, produce an Event Storm first; convert to Aggregate / Domain Model only after stickies stabilize.
- Don't hybridize grammars — an Event Storm with Context Map boundaries is confusing. Pick a dominant axis.

**Always load the relevant `references/type-*.md` before drawing** — it contains layout conventions, DDD semantics, anti-patterns, and example files.

---

## 4. Universal anti-patterns

These mark low-quality domain artifacts:

| Anti-pattern                                                    | Why it fails                                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `Order`, `OrderService`, `OrderManager`, `OrderRepository`      | Technical names in the domain. Use the business noun and its role (aggregate/VO/entity). |
| Boxes labelled `Entity1`, `Entity2`                             | Means the domain isn't named yet — stop and get names.                                    |
| Every box the same color and weight                             | Erases hierarchy; reader can't find the root.                                             |
| Coral on every "important" thing                                | Coral is 1–2 editorial accents per diagram, not a signaling system.                       |
| Arrows between contexts with no integration pattern labelled    | Context Map arrows always carry a pattern (ACL, CS, SK, OHS/PL…). Without labels they're decoration. |
| Aggregate drawn with tightly-coupled children from other roots  | Collapse, or draw the other aggregate separately — aggregates can't share entities.       |
| Event Storm with no time axis / random left-right order         | Events have a temporal order. Establish it or the board is noise.                         |
| Dark mode + purple/cyan glow                                    | "Looks technical" without decisions. Use the editorial skin.                              |
| JetBrains Mono everywhere                                       | Mono is for technical content (types, IDs). Business nouns go in Geist sans.              |
| Ubiquitous language entry that's a definition of the code type  | The glossary exists for business meaning, not type signatures.                            |

Type-specific anti-patterns live in each `references/type-*.md`.

---

## 5. Design system

**Skinnable.** All colors, typography, and tokens live in [`references/style-guide.md`](references/style-guide.md) as semantic roles (`paper`, `ink`, `muted`, `accent`, `link`, …). This file is shared with `diagram-design` — a project's technical and domain diagrams render as siblings.

When specs below or in type references mention "ink" / "accent" / "muted", look up the current hex in `style-guide.md`.

### Semantic roles at a glance

| Role                | Purpose |
|---------------------|---------|
| `paper`, `paper-2`  | Page background and container background |
| `ink`               | Primary text / stroke |
| `muted`, `soft`     | Secondary text, default arrows, sublabels |
| `rule`, `rule-solid`| Hairline borders |
| `accent`, `accent-tint` | 1–2 focal elements per diagram |
| `link`              | External relationships, outbound events |

**Focal rule:** `accent` goes on 1–2 elements max — the aggregate root, the focal event, the core bounded context. Everything else is `ink` / `muted` / `soft`.

### Domain-role → treatment

Domain-design extends the node vocabulary with DDD-specific roles. These compose with the base style.

| Role                    | Fill                    | Stroke                 | Notes |
|-------------------------|-------------------------|------------------------|-------|
| **Aggregate root**      | `accent-tint`           | `accent`               | Focal. Only one per Aggregate diagram. |
| **Entity**              | white                   | `ink`                  | Has identity. |
| **Value object**        | `ink @ 0.05`            | `muted`                | No identity, replaced whole. |
| **Domain event**        | `#fff4cc` (orange-tint) | `#b5523a` thin         | Noun in past tense. |
| **Command**             | `#cfe0ff` (link-tint)   | `#2563eb` thin         | Verb in imperative. |
| **Actor / Persona**     | white, rounded pill     | `soft`                 | User or external system initiating a command. |
| **Policy / Reaction**   | `#e9d5ff` (lavender)    | `muted`                | "Whenever X, do Y." |
| **Read model**          | `paper-2`               | `muted`                | Query-side projection. |
| **External system**     | `ink @ 0.03`            | `ink @ 0.30`           | Outside the current context. |
| **Context boundary**    | dashed `6,4`            | `accent @ 0.50`        | Wraps a bounded context. |
| **Hotspot / Question**  | `#ffd6d6` (pink)        | `#b5523a` dashed `4,3` | Unknown / to-explore marker. |

Using these roles consistently across an Event Storm, a Domain Model, and an Aggregate diagram makes them instantly cross-readable.

### Typography (summary — full spec in style-guide.md)

- **Title** — Instrument Serif, 1.75rem, 400 — H1 only
- **Node name** — Geist (sans), 12px, 600 — human-readable nouns (aggregate names, entity names)
- **Ubiquitous term** — Geist (sans), 13px, 600, `accent` — glossary entry headwords
- **Sublabel** — Geist Mono, 9px — IDs, types, version numbers
- **Eyebrow / tag** — Geist Mono, 7–8px, uppercase, tracked — role tags (`AGG ROOT`, `EVENT`, `VO`)
- **Arrow label** — Geist Mono, 8px — integration pattern, cardinality
- **Editorial aside** — Instrument Serif *italic*, 14px — callouts only

Mono is for technical content (types, IDs, version tags). Business nouns go in Geist sans. Page title in Instrument Serif.

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## 6. SVG primitives

Reuses the same primitive vocabulary as `diagram-design`. Rather than duplicate, treat the rules below as authoritative and refer to `diagram-design/SKILL.md` §6 for extended examples if the skill is installed.

### Background

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="0.9" fill="rgba(28,25,23,0.10)"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="PAPER"/>
<rect width="100%" height="100%" fill="url(#dots)" opacity="0.55"/>
```

### Arrow markers — define all three, always

```svg
<marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="MUTED"/>
</marker>
<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="ACCENT"/>
</marker>
<marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="LINK"/>
</marker>
```

### Node box — role-aware

```svg
<!-- Paper mask prevents arrows bleeding through transparent fills -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="PAPER"/>
<!-- Role-specific fill + stroke from §5 table -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="STROKE" stroke-width="1"/>
<!-- Role tag (rx=2, rectangle — NOT a pill) -->
<rect x="X+8" y="Y+6" width="36" height="12" rx="2" fill="transparent" stroke="STROKE@0.40" stroke-width="0.8"/>
<text x="X+26" y="Y+15" fill="STROKE@0.8" font-size="7" font-family="'Geist Mono', monospace"
      text-anchor="middle" letter-spacing="0.08em">AGG ROOT</text>
<!-- Business noun — Geist sans -->
<text x="CX" y="CY+2" fill="INK" font-size="12" font-weight="600"
      font-family="'Geist', sans-serif" text-anchor="middle">Subscription</text>
<!-- Technical sublabel — Geist Mono -->
<text x="CX" y="CY+18" fill="MUTED" font-size="9"
      font-family="'Geist Mono', monospace" text-anchor="middle">id, plan, status</text>
```

### Arrow labels — always mask

Every arrow label gets an opaque paper rect behind it. Without one it bleeds through the line.

```svg
<rect x="MID_X-26" y="ARROW_Y-12" width="52" height="12" rx="2" fill="PAPER"/>
<text x="MID_X" y="ARROW_Y-3" fill="MUTED" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.06em">ACL · customer</text>
```

Rules: ≤16 chars, all-caps for pattern tags (`ACL`, `OHS/PL`, `SK`), sentence-case for role descriptors (`customer`, `supplier`). Never `writing-mode` vertical.

### Context boundary

Wraps all nodes belonging to a bounded context in a dashed accent rect with a top-left eyebrow tag.

```svg
<rect x="BX" y="BY" width="BW" height="BH" rx="12" fill="transparent"
      stroke="ACCENT@0.50" stroke-width="1" stroke-dasharray="6,4"/>
<rect x="BX+12" y="BY-8" width="96" height="16" rx="2" fill="PAPER"/>
<text x="BX+60" y="BY+3" fill="ACCENT" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.14em">
  BILLING
</text>
```

### Legend

Horizontal strip at the bottom, **never** floating inside the diagram. Expand `viewBox` height by ~60px.

---

## 7. Layout & complexity

### 4px grid

All values — font sizes, padding, node dimensions, gaps, x/y coords — divisible by 4. Non-negotiable.

| Category              | Allowed values                                    |
|-----------------------|---------------------------------------------------|
| Font sizes            | 8, 12, 16, 20, 24, 28, 32, 40                     |
| Node width / height   | 80, 96, 112, 120, 128, 140, 144, 160, 180, 200, 240 |
| x / y coordinates     | multiples of 4                                    |
| Gap between nodes     | 20, 24, 32, 40, 48                                |
| Padding inside boxes  | 8, 12, 16                                         |
| Border radius         | 4, 6, 8                                           |

Exempt: stroke widths, opacities, the 22×22 dot pattern.

### Complexity budget (per diagram)

| Type              | Max items                                                                 |
|-------------------|---------------------------------------------------------------------------|
| Aggregate         | 1 root + up to 6 child entities/VOs + up to 6 invariants + up to 5 events |
| Context Map       | 6 contexts, 10 integration arrows                                         |
| Event Storm       | 12 events, 8 commands, 6 policies, 4 read models                          |
| Context Canvas    | One context — no sub-limits, but canvas-card format caps the area         |
| Ubiquitous Language | 12 terms per glossary card                                              |
| Domain Model      | 6 aggregates, 10 relationships                                            |
| Coral (any type)  | ≤2 focal elements                                                         |

If you exceed, split: overview + detail, or per-context breakdown. Pushing past the budget almost always hides a missing bounded-context boundary.

### Page layout

1. **Header** — eyebrow (Geist Mono), title (Instrument Serif), optional subtitle (Geist muted).
2. **Diagram container** — `paper-2` background, 1px `rule` border, 8px radius, `overflow-x: auto`.
3. **Optional summary cards** — 2–3 columns, varied widths (`1.1fr 1fr 0.9fr`).
4. **Footer** — colophon in Geist Mono, muted, hairline top border.

---

## 8. Pre-output checklist (taste gate)

Run before producing any artifact.

**Domain fit:**
- [ ] Right type for what I'm showing? (§3 selection guide)
- [ ] Would a markdown table / prose do the same job? If yes — don't draw.
- [ ] Loaded the matching `references/type-*.md`?

**Naming:**
- [ ] Every noun is a business noun, not a technical class (`Order`, not `OrderService`)?
- [ ] No `Entity1` / `Placeholder` / unnamed boxes?
- [ ] Does the user's wording appear verbatim where it should (ubiquitous language)?
- [ ] Domain events are past-tense nouns (`OrderPlaced`, not `place order`)?
- [ ] Commands are imperative (`PlaceOrder`, not `ordered`)?

**Structure:**
- [ ] Aggregate root is the focal element (coral), children are not?
- [ ] Bounded-context boundaries drawn when >1 context is on the canvas?
- [ ] Context Map arrows each labelled with an integration pattern (ACL / OHS-PL / SK / CS / Conformist / Partnership)?
- [ ] Event Storm has a time axis (left-to-right)?

**Signal:**
- [ ] Coral on ≤2 elements?
- [ ] Legend covers every role used — and nothing extra?
- [ ] Within the type's complexity budget (§7)?

**Technical:**
- [ ] Arrows drawn before boxes (z-order)?
- [ ] Every arrow label has an opaque paper rect behind it?
- [ ] Legend is a horizontal bottom strip, not floating?
- [ ] Every coord, size, gap divisible by 4?

**Typography:**
- [ ] Business nouns in Geist sans, not Geist Mono?
- [ ] Technical details (IDs, types, version tags) in Geist Mono?
- [ ] Page title in Instrument Serif?
- [ ] No JetBrains Mono anywhere?

---

## 9. Output

Always produce a single self-contained `.html` file:

- Embedded CSS (no external except Google Fonts).
- Inline SVG (no external images).
- No JavaScript required.
- Renders in any modern browser with no build step.

Filename pattern: `<business-noun>-<type>.html` — e.g. `subscription-aggregate.html`, `billing-context-map.html`, `order-fulfilment-event-storm.html`.

Variants follow the same tiering as `diagram-design`:

| Variant            | When to use                                                          |
|--------------------|----------------------------------------------------------------------|
| **Minimal light**  | Default. Screenshot-ready. Diagram + title. Warm paper background.   |
| **Minimal dark**   | Dark-mode readers, slide decks, high-contrast social posts.           |
| **Full editorial** | Long-form docs where the diagram is the hero. Summary cards, subtitle. |

Start from the type-specific reference file; it will point at the relevant variant template to copy from.

---

## References

Type references (load only the one you need):

- [`references/type-aggregate.md`](references/type-aggregate.md)
- [`references/type-context-map.md`](references/type-context-map.md)
- [`references/type-event-storm.md`](references/type-event-storm.md)
- [`references/type-context-canvas.md`](references/type-context-canvas.md)
- [`references/type-language.md`](references/type-language.md)
- [`references/type-domain-model.md`](references/type-domain-model.md)

Shared infrastructure:

- [`references/style-guide.md`](references/style-guide.md) — tokens, shared with diagram-design
- [`references/onboarding.md`](references/onboarding.md) — pull brand from a website URL
- [`references/primitive-annotation.md`](references/primitive-annotation.md) — editorial callouts
