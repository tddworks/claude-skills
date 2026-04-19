# Phase 1 — Discovery

**Your task:** before drafting any architecture or writing any code, find out what already exists in the codebase and what the user actually means.

## Inputs

- The user's ask (one sentence to one paragraph)
- The project root

## Steps

### 1. Find the architecture docs

```
<project>/docs/architecture/     — canonical domain map
<project>/docs/features/         — per-feature design docs
<project>/design-concept/        — interactive HTML mockups (if any)
<project>/CLAUDE.md              — top-level conventions & feature index
```

If the project has an **aggregate audit / inventory** (`aggregates.md` or similar), read it first — it's the current snapshot of the domain shape.

If the project has a per-feature design doc for this feature, **read it end-to-end** before touching code. The doc is the contract.

### 2. Reconcile docs with current code

Docs drift. Before treating any doc as truth, verify:

- Grep the type names in the doc against the codebase — do they still exist?
- Have they been renamed?
- Does the shape match what the audit says today?

If the doc is stale:
- For small drift: update it inline as you go, note in your discovery summary.
- For large drift: stop and fix the doc first. Don't implement against a broken map.

### 3. Capture the user's mental model

Re-read the user's ask. Write down their **exact words** for:
- The thing being added (noun)
- The actions it allows (verbs)
- The states it can be in
- Who uses it

**These are your naming candidates.** Don't translate their words into jargon. If the user said "<their-word>", the type is `<TheirWord>` (or `<TheirWord>s` if it's a collection) — not `<TheirWord>Manager`, `<TheirWord>Service`, `<TheirWord>Handler`.

Sanity test: read your candidate names aloud. Does it sound like a person describing their work, or like a library API? If it's the latter, rename.

### 4. Check for existing homes

Before declaring a new aggregate, check whether the feature fits into something that already exists:

| If the feature is... | Check if it fits as... |
|---|---|
| A collection the user owns | A sub-aggregate on an existing parent entity |
| A new field on an existing concept | An extra property on an existing value type |
| A new derived query | A computed property on an existing aggregate |
| A new push from an external system | An `apply` / `upsert` / `remove` method on an existing aggregate |

Most features slot into one of those four. Only invent a new aggregate when none of them fit.

### 5. Scope the design-doc question

Decide: does this feature already have a design doc?

- **Yes, accurate** → proceed to Phase 3 (Domain TDD) directly; the design is the contract.
- **Yes, stale** → fix the doc, then proceed. Or go back to Phase 2 if the shape changed materially.
- **No** → go to Phase 2 (Domain design) to produce one.

## Output

A short (< 300 words) discovery note with these sections:

```markdown
## Discovery — <feature name>

**What exists:**
- <doc paths that mention this feature, or "none">
- <relevant aggregates / types in the code>
- <design-concept screens, if any>

**Drift (current code vs docs):**
- <bullets or "none — docs match code">

**User's vocabulary:**
- noun(s): …
- action(s): …
- state(s): …

**Shape hypothesis:**
- This feels like a <new sub-aggregate on X | new field on Y | computed on Z | push-fed writer on W>.
- Candidate names: …

**Next phase:**
- <Phase 2 (new design needed)> | <Phase 3 (design doc already accurate)>
```

## Gate

- You can name the feature in the user's own words.
- You know whether a design doc exists and whether it matches the code.
- You have a hypothesis about which of the four domain shapes this feature fits.

Only proceed once all three are true. If you're guessing at any of them, keep digging — read more of the existing code or ask the user one clarifying question.

## Anti-patterns

- **Loading the whole codebase into context.** Read only the 2–3 files that are load-bearing for this feature.
- **Inventing a design doc the user didn't ask for.** Phase 2 handles that — here you just find out if one exists.
- **Renaming the user's words.** "approvals" ≠ "ApprovalManager". Keep their exact noun.
- **Grep-and-skim.** If a type is relevant, open the file and read its public surface.
