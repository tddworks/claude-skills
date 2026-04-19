# Phase 7 — Docs

**Your task:** capture the *why* before memory decays. Update the feature doc, the aggregate audit, and any visual artifacts.

## Inputs

- Green feature from Phases 3–6 (domain, infra, views all working)
- The project's docs directory (`docs/`, `Documentation/`, etc.)

## Steps

### 1. Write the feature doc

One markdown file per feature: `<project>/docs/features/<feature>.md`. Sections, in this order:

```markdown
# <Feature>

## What it is
One paragraph: what this feature lets the user do, in their own words.

## User mental model
- **Nouns**: <the types, in the user's own words>
- **Verbs**: <what they do, in the user's own words>
- **States**: <the statuses that matter to the user>

## Domain shape
Aggregate: `<Aggregate>` (protocol) + `<AggregateImpl>` (impl)
Value: `<Value>`
Port: `<AggregatePort>`

```
<ASCII architecture diagram from Phase 2, updated to match final impl>
```

## Wire protocol
| Method / event | Direction | Purpose |
|---|---|---|
| `<verb>` | client → server | <what it does> |
| `<feature>.updated` | server → client | <when it fires> |

## MVP scope
Short list of what ships. Explicitly list what's *out*.

## File map
- `<domain module>/<Feature>/<Value>` — value type
- `<domain module>/<Feature>/<Aggregate>` — protocol + `<AggregateImpl>` impl
- `<domain module>/<Feature>/<AggregatePort>` — infra port
- `Modules/Infrastructure/Sources/<…>` — port conformance + wire mapping
- `<app module>/<Feature>/` — UI bound to the root facade

## Data flow
Short walkthrough: user taps X → view calls `root.<feature>.approve(...)` → aggregate calls port → server responds → push event → interpreter calls `upsert` → view rerenders. 5–8 lines max.

## Testing
- Unit tests: tests for `<Value>` + `<AggregateImpl>` in the domain test target
- Integration: tests for `<AggregatePort>` conformance in the infra test target
- Manual QA: <any scenarios that aren't automated>

## Open questions / follow-ups
Anything deferred. Don't leave ghost TODOs in code; list them here instead.
```

Keep it under 300 lines. If it's longer, the feature is doing too much.

### 2. Update the aggregate audit

Most projects maintain an inventory — `docs/architecture/aggregates.md` or similar. Add a row for the new aggregate:

```markdown
| Aggregate | Owner | Port | Notes |
|---|---|---|---|
| `<Aggregate>` | `<Parent>` or `<Root>` | `<AggregatePort>` | <anything notable — e.g. "push-fed + pullable", "optimistic toggle with revert"> |
```

If the feature deleted or renamed something, update the row rather than leaving ghosts.

### 3. Update the top-level CLAUDE.md / README feature index

If the project has a feature index (a table in `CLAUDE.md` or `README.md` listing features and their docs), add the new feature's row:

```markdown
| <Feature> | `docs/features/<feature>.md` | <entry point — e.g. "tap X → <Feature>View"> |
```

This is how the *next* agent finds your work.

### 4. Visual artifacts (optional but recommended)

If the project uses HTML/SVG domain diagrams (see `domain-design` skill), regenerate the affected ones:

- **Domain model** — add the new value + aggregate.
- **Context canvas** — add any new external system the port talks to.
- **Event storm** — add new commands and events the feature introduces.

Skip this if the project doesn't use visual artifacts. Don't invent the practice just for this feature.

### 5. Cross-link

Inside the new feature doc, link back to:

- The aggregate audit (for cross-reference).
- Related feature docs (if this feature touches or depends on them).
- Design mockups (if the project has `design-concept/` or similar).

And from those artifacts, link in to the new feature doc. Docs that don't link to each other get lost.

### 6. Commit the docs with the code

Docs live in the same commit as the feature, not a follow-up PR. "Docs later" is how docs drift.

## Output

- `<project>/docs/features/<feature>.md` (new or updated)
- Aggregate audit updated with the new entry
- CLAUDE.md / README feature index updated
- Visual artifacts regenerated (if project uses them)
- Cross-links in place

## Gate

- A new engineer reading `docs/features/<feature>.md` can understand what the feature does, where its code lives, and how it flows, without reading the source.
- Aggregate audit matches the code — no drift.
- No orphan rows in the audit (deleted aggregates are removed, not just marked).

## Anti-patterns

- **Restating the code.** Docs that say "the `approve` method calls `port.approve`" are useless. Docs capture *why*, *when*, and *the mental model*.
- **Docs-after-PR.** By next week you've forgotten the nuance. Write the doc before you hit "submit".
- **Novel-length feature docs.** If it's >300 lines, split it or cut it. Agents and humans skim.
- **Untracked decision notes in Slack or commit bodies.** If a design choice matters enough to remember, it matters enough to land in the doc.
- **Auto-generated docstrings as "the docs".** They describe method signatures, not behavior. The feature doc exists precisely because signatures aren't enough.
- **Diagrams that don't match code.** Stale is worse than missing. If the audit or diagram would need to lie to stay unchanged, update it.
