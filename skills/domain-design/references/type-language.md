# Ubiquitous Language Glossary

**Best for:** documenting the vocabulary of a bounded context. Each term has a definition, optional aliases, and a note on what it is *not*.

Ubiquitous language is the DDD pillar that's easiest to skip and most expensive to skip. When a team drifts into technical jargon (`User`, `Record`, `Item`, `Entity`), bugs and miscommunication follow. A glossary pins the shared words.

## Layout conventions

The glossary is a column of **term cards**, one per entry. Each card:

- **Headword** — the term in Geist sans, 14px, 600, `accent`. This is the load-bearing element.
- **Part of speech** — small eyebrow tag: `NOUN`, `VERB`, `EVENT`, `ROLE`. Helps readers tell "Subscribe" (verb, command) apart from "Subscription" (noun, aggregate).
- **Definition** — one or two sentences, Geist sans, 12px, `ink`. Plain language. No code, no types.
- **Aliases** — optional. Small muted line with `also called:` prefix in Geist Mono 9px.
- **Not** — optional. Small line with `not:` prefix, lists common false-cousin terms with short disambiguation.
- **Source** — optional. Where the term came from (a specific stakeholder, a contract, a regulation).

Layout:

- Single column is usually best — easier to scan alphabetically.
- Two columns if 8+ terms; group alphabetically or by sub-domain.
- Horizontal hairline between cards, not heavy borders.

## Grouping

Optional: group by **sub-domain or role** with sticky sub-headers:

```
─── COMMERCE ────────────────────────────────────────
  Cart · Checkout · Order · Payment

─── FULFILMENT ──────────────────────────────────────
  Shipment · Carrier · Tracking
```

Sub-headers are Geist Mono 8px, uppercase, tracked, `muted`.

## Cross-references

A term can reference another:

- Use a small `→` before the referenced term in italics: `→ *Subscription*`.
- Don't hyperlink — the glossary should be readable printed.

## Example entry

```
SUBSCRIPTION                                        [NOUN · AGGREGATE]
A customer's ongoing entitlement to a plan. Created when the customer
completes checkout and ends on explicit cancellation or non-renewal.
  also called: account (legacy), plan (marketing)
  not: Invoice — the billing artefact for a single period. See → *Invoice*.
  source: Billing handbook §2.1
```

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Definitions that are code signatures (`{ id: UUID, plan: string }`) | The glossary is for meaning, not types. Move types to the code. |
| Marketing-speak ("Our powerful subscription platform…") | Glossary entries are definitional, not promotional. |
| Circular definitions ("A Subscription is when a user subscribes") | Pick a non-derived anchor: a fact, an event, a rule. |
| Same term listed twice with different meanings | That's a smell — either a missed bounded-context split, or consolidate. |
| No "not:" disambiguations on ambiguous terms | If `Customer` means two different things across contexts, say so. |
| 40+ terms on one page | Split by sub-domain or produce per-context glossaries. |

## Complexity budget

- ≤ 12 terms per card set (one Glossary artifact).
- If you have more, split by sub-domain or by bounded context — each sub-domain gets its own glossary.
- Definitions are ≤ 2 sentences.

## Examples

- `assets/example-language.html` — minimal light
- `assets/example-language-dark.html` — minimal dark
- `assets/example-language-full.html` — full editorial with sub-domain sub-headers
