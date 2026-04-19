# Phase 8 — Verify

**Your task:** run the full checklist before calling the feature done. No green builds → no merge.

## Inputs

- Everything from Phases 3–7 committed
- The project's test + build commands

## Steps

### 1. Run the full test suite

Not just the tests you wrote. The feature may have touched shared code.

```
<test command for the project — e.g. `make test`, `swift test`, `npm test`>
```

If anything fails:
- Your change caused it → fix it (don't skip the test).
- Pre-existing failure unrelated to your change → note it in the commit / PR, don't silently suppress.

### 2. Run the release build

Tests passing ≠ app builds. Run the release / archive build for every target platform:

```
<release build command — e.g. `xcodebuild … build`, `npm run build`>
```

The release config catches things debug misses: stricter warnings, dead-code stripping, optimizer-only bugs.

### 3. Regenerate the project (if applicable)

If the project auto-generates its IDE workspace from a manifest, regenerate it so schemes + file lists stay in sync:

```
<manifest regeneration command>
```

Commit the regenerated files if they changed.

### 4. Manual smoke test

Fire up the app, exercise the feature end-to-end:

- Happy path — the thing the user asked for works.
- Empty state — no data, no active entity, fresh install.
- Error state — disconnect the external system, see the UI degrade gracefully.
- Reconnect — reconnecting repopulates state.

Automated tests don't catch "the button isn't tappable because another view is on top of it". The smoke test does.

### 5. Pre-commit checklist

Walk this list. Don't skip items just because they "usually pass".

**Domain**
- [ ] Value type has `Sendable + Equatable + Identifiable`.
- [ ] Value-level computed queries (bucket/category/semantic booleans) live on the value, not in helpers.
- [ ] Aggregate is `@MainActor @Mockable protocol <Noun>: Observable`.
- [ ] Concrete impl is `@Observable @MainActor final class <NounImpl>: <Noun>`.
- [ ] Aggregate has `apply(items:)` / `upsert(_:)` / `remove(id:)` (push-fed writers).
- [ ] Port is `@Mockable protocol <NounPort>: Sendable`, kept internal to the concrete impl.

**Composition**
- [ ] Aggregate is plugged onto its owning entity (not the composition root, unless it's genuinely app-wide).
- [ ] Composition root exposes the feature through a facade forwarder — no `active?.<feature>` in views.
- [ ] Fallback aggregate exists so views never see `nil`.

**Tests**
- [ ] Zero `verify(mock).method.called(...)` assertions — Chicago-school only.
- [ ] Value tests cover each state variant's derived queries.
- [ ] Aggregate tests cover apply/upsert/remove + each computed query + refresh success/failure/nil-port.
- [ ] Tests run in under a second per target (domain tests should be fast).

**Wire**
- [ ] Port conformance lives in infra, maps wire↔domain at the seam.
- [ ] Server push events route through `apply` / `upsert` / `remove`.
- [ ] Reconnect flow calls `refresh()` so state resyncs.

**Docs**
- [ ] `docs/features/<feature>.md` exists and matches the code.
- [ ] Aggregate audit updated.
- [ ] CLAUDE.md / README feature index updated.

**Build**
- [ ] All tests green.
- [ ] Release build green.
- [ ] No warnings introduced (or the new ones are documented).

### 6. Write a tight commit / PR description

Use conventional commits: `feat(<scope>): <summary>`. The body answers three things:

1. **What** the feature does (one sentence).
2. **Why** (the user need / problem it solves).
3. **How** (one paragraph on the domain shape — "adds `<Aggregate>` protocol + `<AggregateImpl>` impl on `<Parent>`, wires `<AggregatePort>` conformance on the infra client, exposes through `<root>.<feature>` facade").

Link to the feature doc. Don't restate the diff.

### 7. Decide what's left

If Phase 8's checklist uncovered something (stale fallback, missing error state, a view still drilling through `active?`), fix it **now**. Don't defer to "a follow-up PR" unless it's genuinely out of scope.

Genuine follow-ups go on the feature doc's "Open questions / follow-ups" section, not in TODOs in code.

## Output

- All tests green
- Release build green
- Checklist complete
- Commit / PR description written
- Feature doc + audit + index committed in the same change

## Gate

- The feature works in the real app, not just in tests.
- An agent reading the feature doc + your commit message can understand the change without reading the diff.
- No "fix later" notes in the code.

## Anti-patterns

- **"Tests pass locally".** If they don't pass in CI, they don't pass. Run the same command CI runs.
- **Skipping the release build.** Optimizer-specific bugs find you at ship time, when it's most expensive.
- **Merging with a known failing smoke test.** The one edge case you rationalized is the one the user hits first.
- **Follow-up-PR rot.** "I'll fix the fallback / rename the type / delete the dead path in a follow-up" almost always becomes never. If it's worth doing, do it in the same change.
- **Commit messages that describe the diff, not the feature.** `feat(<scope>): add <Aggregate> protocol, <AggregateImpl> class, <AggregatePort> port` is a diff summary. `feat(<scope>): <what the user can now do, in plain words>` is a feature summary. Prefer the latter.
- **Leaving the audit stale.** An audit that lies is worse than no audit. If you touched a row, update it.
