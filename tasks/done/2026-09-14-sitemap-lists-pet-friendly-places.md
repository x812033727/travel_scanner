---
id: 2026-09-14-sitemap-lists-pet-friendly-places
title: Sitemap lists the pet-friendly place pages, not just the directory
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:27:46Z
created_at: 2026-09-14T13:30:26Z
completed_at: 2026-09-22T10:45:06Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on:
  - 2026-09-10-seo-open-content-pages
scope:
  - apps/web/app/sitemaps/sitemap.ts
  - apps/web/app/sitemaps/sitemap.test.ts
  - apps/web/lib/community/public.server.ts
  - apps/web/lib/community/public.server.test.ts
---

# Sitemap lists the pet-friendly place pages, not just the directory

## Why

`2026-09-10-seo-open-content-pages` made `/{locale}/pet-friendly/{id}` server-render its
record and return `index: true`, and added `/{locale}/pet-friendly` to `SITEMAP_ROUTES`
behind the community switch. The directory is listed; the place pages it links to are not.

That is the right first step and not the end of it. The directory pages one cursor at a
time, so a crawler reaching place 200 has to follow "load more" — a button, not a link.
The place pages are the content with the verified rules on them, so they are what should
rank for "does this café take dogs", and a sitemap entry is how a new one gets seen in
days rather than whenever a crawl happens to walk the directory.

`/community/posts/{id}` and `/community/profiles/{handle}` have the same gap, but no
public enumeration endpoint to build a list from — `/community/posts` is the member feed.
Those stay out until there is one; this task is only about the places.

## Definition of done

- [x] `sitemap.xml` carries one entry per locale for every published pet-friendly place,
      with the same reciprocal hreflang set the static routes get.
- [x] The list is still empty when the community switch is off or the API is unreachable,
      exactly as `/pet-friendly` itself already behaves.
- [x] Enumerating the places cannot make `sitemap.xml` hang or fail: a capped number of
      pages, a timeout, and a partial read that still returns the static routes.
- [x] No `lastModified` invented for a place. `verified_at` is a real date if one is
      wanted; "now" on every crawl is the signal the file's own comment warns against.

## Steps

- [x] Add a paging loader to `lib/community/public.server.ts` beside `loadPetPlaces`,
      following `guideSitemapEntries()` in `lib/guides.server.ts` for the cap/partial shape
      (it already returns `{ entries, complete }` for exactly this reason).
- [x] Append the entries in `sitemap.ts` after the static routes, as the guide articles are.
- [x] Remove the "deliberately absent" note about the per-record routes as it is satisfied.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run build:web
```

Then with the API reachable, `curl -s localhost:3000/sitemap.xml | grep -c pet-friendly`
against the number of published places, and confirm it drops to zero with the community
switch off.

## Notes

- `getPetPlaces` in `lib/community/public.server.ts` already reads the first page with the
  right headers, cache policy and switch gate. The paging loader wants the same treatment
  and a cap, not a second copy of it.
- The directory's own endpoint is `GET /api/v1/pet-friendly/places`, which answers
  `{ items, next_cursor }`. `include_uncertain` defaults to false, which is the set that
  should be listed: a place whose rules are not currently verified is what the page itself
  labels "needs confirmation".

### 2026-09-19 done in repo (claude-fable-5-1)

- **Scope corrected first.** `app/sitemap.ts` no longer exists: `2026-09-14-sitemap-split-before-1000-rows`
  moved the children to `app/sitemaps/sitemap.ts` (the index is the hand-written `app/sitemap.xml/route.ts`).
  The two scope lines now name the moved file and its test; no active task holds `app/sitemaps`.
- **Where the rows live: the `static` child, after the routes.** The section children are cut by guide
  section × locale and the index lists them from `GET /guides/sitemap/summary`; what decides whether a
  place page exists is the community switch, which the static child already reads. A child of their
  own would need the index to learn that switch (`app/sitemap.xml/route.ts` and its test, outside this
  ticket) and nothing needs it yet: at the cap the places add at most 1,000 × 5 = 5,000 rows to
  `static`, a tenth of Google's per-file limit. The day the count needs it, that is the follow-up.
- **The enumerator**: `petPlaceSitemapEntries()` in `lib/community/public.server.ts`, returning
  `{ entries: [{ id, verified_at? }], complete }` like `guideSitemapEntries()`. `publicJson` was split
  into the switch gate (`communityOpen`) and the bare read (`publicRead`), so the pager shares the
  same headers, `no-store` and timeout as the page reads instead of a second copy; the four loaders
  are unchanged in behaviour. It pages `GET /api/v1/pet-friendly/places?limit=50&include_uncertain=false`
  through `next_cursor`. `include_uncertain` is the API's default, sent anyway so the listed set --
  places whose rules are currently verified -- cannot move under a default change.
- **Caps and timeouts, and why:**
  - page size **50**: the API's maximum (`limit` is `le=50` in `pets.py`);
  - **20 pages** = 1,000 places. A cap on the read, not the directory: past it the read says
    `complete: false` and the first thousand still list. Raise it, or give the places their own
    child, when the count approaches it;
  - **3 s per page**: the module's existing `TIMEOUT_MS`, reused;
  - **10 s for the whole enumeration** (`PET_PLACE_SITEMAP_BUDGET_MS`). Twenty pages that each just
    made a 3 s timeout would hold `sitemap.xml` for a minute, which is the hang the DoD forbids. The
    read stops between pages once the budget is spent, and the last page's timeout shrinks to what is
    left, so the worst case is about 10 s -- well inside nginx's `proxy_read_timeout 300s`, and far
    above what 20 warm pages need (each is one bounded 501-row scan on the API side).
- **Never throws.** Switch off or unreadable: `{ entries: [], complete: true }` with no API call --
  nothing is public, which is the truth, not a failure. A failed, malformed, non-2xx or timed-out page,
  the page cap and the budget: what was read so far with `complete: false`. `sitemap.ts` also drops the
  rows when the community state it read itself is closed, so a read that raced the switch can never
  disagree with `/pet-friendly`.
- **`lastModified` only from a parseable `verified_at`**; a place without one gets no field at all, never
  "now". Ids are kept only when made of RFC 3986 unreserved characters (UUIDs are), because Next writes
  `<loc>` and each alternate `href` unescaped and calls `toISOString()` on the date -- a bad id would cost
  the whole file and an Invalid Date a 500 for the child, so each costs one row or one field instead.
  Entries carry all five locales + x-default (the page renders every locale from the one record and
  the layout's hreflang says the same), `changeFrequency: "monthly"`, `priority: 0.5`, deduplicated by id.
- **Validation:** `npx vitest run app/sitemaps/sitemap.test.ts lib/community/public.server.test.ts` --
  148 passed (12 new); `npm run test:web` -- 289 files / 3,164 tests passed; `npm run lint:web` and
  `npm run typecheck:web` clean. Not run here: `npm run build:web` and the `curl | grep -c pet-friendly`
  check in "How to verify", which need a reachable API; those remain for the host.
- **Noticed, not done (outside scope):** `docs/seo.md` still says "Nothing outside the guides emits
  `lastmod`"; the place pages now do, from `verified_at`. Filed as a docs follow-up. The browser suite's
  static-child row count in `e2e/seo.spec.ts` is unaffected because the fixture API does not open the
  community; if it ever does, that count gains the fixture's places.
