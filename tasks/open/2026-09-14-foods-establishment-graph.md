---
id: 2026-09-14-foods-establishment-graph
title: AIO: /foods states its merchants and their verification as FoodEstablishment
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-14T13:48:24Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/app/[locale]/foods/page.tsx
---

# AIO: /foods states its merchants and their verification as FoodEstablishment

## Why

`/foods` is the site's second-richest honest structured-data opportunity and emits only
`BreadcrumbList` + `ItemList` today. The merchant card really renders the name, the address, the
award where there is one, every source title, and the date each was verified — so a
`FoodEstablishment` graph would describe exactly what a reader sees, which is the rule
`lib/structured-data.ts` states in its header.

For an answer engine, a restaurant is the clearest kind of entity there is: a name, a place, and
a dated verification. The `guideArticle` work established the pattern — `citation` from the
sources a page already shows — and `/foods` has the same asset unpublished.

## Definition of done

- [ ] `/{locale}/foods` emits one `FoodEstablishment` per merchant actually rendered, with
      `name`, `address`, and `citation` from the sources the card lists.
- [ ] Nothing is claimed for a merchant whose card is in its unavailable or moderated state.
- [ ] No `aggregateRating` and no `Review` (see Notes).

## Steps

- [ ] Read `lib/foods.ts` for the exact merchant shape and which fields the card guarantees.
- [ ] Add `foodEstablishment(locale, input)` beside `guideArticle` in `lib/structured-data.ts`,
      same conventions: pure, spread-conditional optionals, `localeUrl` for internal URLs.
- [ ] Call it from `app/[locale]/foods/page.tsx` over the merchants the page seeded server-side,
      never over a list fetched after hydration.
- [ ] Tests in `lib/structured-data.test.ts`, in the existing per-builder `describe` style.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
```

Then paste a built `/en/foods` page's JSON-LD into validator.schema.org.

## Notes

**No rating markup.** Nothing on this site collects one; the interest score is Mokaair's own
signal, not a user rating, and `docs/seo.md` commits in writing to adding no Product/Offer
markup. `aggregateRating` over an internal score would be invented review markup.

Only mark up merchants the server actually rendered. The food directory has moderated and
unavailable states, and a graph that names a merchant whose card is withheld describes something
the page does not show.
