---
id: 2026-09-14-sitemap-lists-pet-friendly-places
title: Sitemap lists the pet-friendly place pages, not just the directory
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-14T13:30:26Z
completed_at:
branch:
depends_on:
  - 2026-09-10-seo-open-content-pages
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
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

- [ ] `sitemap.xml` carries one entry per locale for every published pet-friendly place,
      with the same reciprocal hreflang set the static routes get.
- [ ] The list is still empty when the community switch is off or the API is unreachable,
      exactly as `/pet-friendly` itself already behaves.
- [ ] Enumerating the places cannot make `sitemap.xml` hang or fail: a capped number of
      pages, a timeout, and a partial read that still returns the static routes.
- [ ] No `lastModified` invented for a place. `verified_at` is a real date if one is
      wanted; "now" on every crawl is the signal the file's own comment warns against.

## Steps

- [ ] Add a paging loader to `lib/community/public.server.ts` beside `loadPetPlaces`,
      following `guideSitemapEntries()` in `lib/guides.server.ts` for the cap/partial shape
      (it already returns `{ entries, complete }` for exactly this reason).
- [ ] Append the entries in `sitemap.ts` after the static routes, as the guide articles are.
- [ ] Remove the "deliberately absent" note about the per-record routes as it is satisfied.

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
