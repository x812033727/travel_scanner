---
id: 2026-09-14-foods-establishment-graph
title: AIO: /foods states its merchants and their verification as FoodEstablishment
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:27:28Z
created_at: 2026-09-14T13:48:24Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
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

- [x] `/{locale}/foods` emits one `FoodEstablishment` per merchant actually rendered, with
      `name`, `address`, and `citation` from the sources the card lists.
- [x] Nothing is claimed for a merchant whose card is in its unavailable or moderated state.
- [x] No `aggregateRating` and no `Review` (see Notes).

## Steps

- [x] Read `lib/foods.ts` for the exact merchant shape and which fields the card guarantees.
- [x] Add `foodEstablishment(locale, input)` beside `guideArticle` in `lib/structured-data.ts`,
      same conventions: pure, spread-conditional optionals, `localeUrl` for internal URLs.
- [x] Call it from `app/[locale]/foods/page.tsx` over the merchants the page seeded server-side,
      never over a list fetched after hydration.
- [x] Tests in `lib/structured-data.test.ts`, in the existing per-builder `describe` style.

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

### 2026-09-19 done in repo (claude-fable-5-1)

Branch `claude/travel-scanner-pr-552-rpq36m`. Files: `apps/web/lib/structured-data.ts`,
`apps/web/lib/structured-data.test.ts`, `apps/web/app/[locale]/foods/page.tsx`.

**What `/{locale}/foods` emits now.** Next to the existing `BreadcrumbList`, in the same
`StructuredData` array, one `FoodEstablishment` per merchant of the server-seeded first page
(`initial.merchants.items` -- the array `FoodBrowser` renders on the server, so the graph and the
cards cannot disagree):

- `@id`: `{localeUrl}/foods#merchant-<id>`, the card's own DOM anchor and the fragment the share
  button hands out (`useSharedAnchor` scrolls to it).
- `name`, and `alternateName` = `local_name` when it differs (the line under the heading).
- `address`: `PostalAddress` with `streetAddress` = the one address line the catalog stores (when
  present) and `addressLocality` = `destination_name`, the city the card names beside the pin.
- `award`: the translated label of the first source distinction in the card's badge set
  (`foods.distinctions.*`), when any.
- `citation`: one `CreativeWork` per source the card lists, `name` = title, `url` only when
  `safeExternalHref` accepts it -- the card's own test; otherwise the card prints the title as text
  and the graph carries the name alone.

Builders: `foodEstablishment(locale, card, awards)` (one node, typed on the card fields it reads)
and `foodEstablishments(locale, seed, awards)` (the page's entry: the seed as `unknown`, the
browser's own `Array.isArray(items)` test, one node per item). The page resolves the six badge
labels with `getTranslations({ namespace: "foods" })` and passes them in, so the builder stays free
of translation lookups, as the file header asks.

**Unavailable / moderated.** The public `/foods/merchants` list applies
`publishable_merchant_filters()` (approved, active, verified map identity, durable coordinates, a
current source) in SQL and re-checks each row (`apps/api/app/foods/publication.py`), so a withheld
merchant never reaches `items`; the web `FoodMerchant` shape carries no state field at all. The
one withheld state the page itself sees is a seed that failed to load (API timeout gives `null`):
the server then renders no card and the browser fetches after hydration, and the graph returns
nothing rather than run ahead of it. Tested with `null`, `undefined`, a non-list, a string and an
empty list.

**Deliberately left out, and why:**

- `aggregateRating` / `review`: nothing on the site collects a rating (Notes above). The test pins
  the node's exact key set and checks the serialised node for `aggregateRating`, `"review"`,
  `Review` and `Rating`.
- The "Sources checked on {date}" line (`verified_at`): the only schema.org home for "we checked
  this on" is `lastReviewed`, a WebPage property. A merchant has no page of its own, and a
  per-merchant date on `/foods`'s WebPage would claim one review date for a page showing twenty --
  the same reasoning `guideArticle` records for `dateAccessed`.
- `url` / `sameAs` from `official_website_url`: the card draws that link only after
  `reviewedExternalHref` (https only, no credentials, ports, bare or local hosts), which is private
  to `components/merchant-external-links.tsx` and outside this scope. Emitting the raw field could
  name a website the card refused to draw. Follow-up, if wanted: export that check and add `url`.
- `addressCountry` (`country_code`), `geo`, `servesCuisine` (the category chips mix cuisines with
  venue types -- a cafe is not a cuisine), `openingHours`, `telephone`, `priceRange`, `hasMenu`:
  the card renders none of them as such.
- No `ItemList`: merchants have no page of their own and `itemList` lists only entries with URLs
  (file header rule). This ticket's "BreadcrumbList + ItemList today" overstated the page; it
  emitted the `BreadcrumbList` alone, and still does, now with the establishments beside it.

**Verified:** `npx vitest run lib/structured-data.test.ts "app/[locale]/foods"` (31 passed),
`npm run lint:web`, `npm run typecheck:web` clean. Not done here: pasting a built `/en/foods` into
validator.schema.org needs the API up; the e2e runtime fixture serves no public merchant list, so
`e2e/seo.spec.ts` sees a null seed on `/foods` and only the `BreadcrumbList`, as before.
`docs/seo.md`'s graph table has no FoodEstablishment row yet -- outside this scope, one line to add
when this merges.
