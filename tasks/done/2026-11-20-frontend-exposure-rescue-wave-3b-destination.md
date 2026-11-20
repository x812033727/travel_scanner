---
id: 2026-11-20-frontend-exposure-rescue-wave-3b-destination
title: Frontend exposure rescue wave 3B: destination hub depth/ItemList/Discover, dynamic hub/city OG cards, Organization.sameAs, and llms.txt feeds
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-20T15:53:50Z
created_at: 2026-11-20T15:53:41Z
completed_at: 2026-11-20T15:56:54Z
branch: agy/frontend-exposure-wave3b-hubs-og-eeat
depends_on: []
scope:
  - apps/web/app/llms.txt/route.test.ts
---

# Frontend exposure rescue wave 3B: destination hub depth/ItemList/Discover, dynamic hub/city OG cards, Organization.sameAs, and llms.txt feeds

## Why

1. **Destination city hubs were truncated and lacked Discover/OG cards**: All 33 destination pages (`/destinations/[destinationId]`) fetched only 3 guides, emitted no `ItemList` JSON-LD, lacked `DISCOVER_ROBOTS`, and fell back to the generic brand `/og.png`.
2. **Topic hubs lacked bespoke social preview cards**: Only `ai-news` and `tech-news` emitted custom `og:image` when their lead carried real photography; all other topic hubs (`claude-code`, `ai-terms`, `transport`, `itinerary`, `finance`, `software`, etc.) fell back to `/og.png`.
3. **Organization JSON-LD lacked `sameAs` entity linking**: Search and answer engines could not bind Mokaair's website to its official YouTube channel and social profiles via `Organization.sameAs`.
4. **`/llms.txt` omitted per-vertical news Atom feeds**: AI search agents reading `/llms.txt` were not pointed at `/en/life/feed.xml`, `/en/life/topics/ai-news/feed.xml`, or `/en/life/topics/tech-news/feed.xml`.

## Definition of done

- [x] Shared `renderEditorialOgCard` extracted into `apps/web/lib/editorial-og-card.tsx`, powering article, destination (`/og/[locale]/destinations/[destinationId]/card.png`), and topic (`/og/[locale]/topics/[section]/[topic]/card.png`) 1200x630 PNG cards.
- [x] Destination pages fetch up to 12 city guides, emit `ItemList` JSON-LD, declare `DISCOVER_ROBOTS`, and wire their dynamic destination OG/Twitter card.
- [x] Indexable topic hubs without real lead photography emit their dynamic topic OG/Twitter card (archive/noindex pages stay clean).
- [x] `Organization` JSON-LD supports verified HTTPS `NEXT_PUBLIC_SITE_SAME_AS` entity links.
- [x] `/llms.txt` lists the news desk and AI/tech topic Atom feeds.
- [x] All unit tests, lint, typecheck, i18n, and task checks pass.

## Steps

- [x] Extract `renderEditorialOgCard` and add destination & topic dynamic OG routes + node Vitest tests.
- [x] Upgrade `apps/web/app/[locale]/destinations/[destinationId]/page.tsx` + tests.
- [x] Wire topic dynamic OG fallback in `apps/web/components/guides/topic-hub-page.tsx` + tests.
- [x] Add `parseSameAs` + `Organization.sameAs` in `apps/web/lib/structured-data.ts` + tests.
- [x] Add news Atom feeds to `apps/web/app/llms.txt/route.ts` + tests.

## How to verify

```bash
cd apps/web && npx vitest run "app/og/[locale]/[kind]/[slug]/card.png/route.test.ts" "app/og/[locale]/destinations/[destinationId]/card.png/route.test.ts" "app/og/[locale]/topics/[section]/[topic]/card.png/route.test.ts" "app/[locale]/destinations/[destinationId]/page.test.tsx" components/guides/topic-hub-page.test.tsx lib/structured-data.test.ts app/llms.txt/route.test.ts "app/[locale]/robots-directives.test.ts"
npm run lint:web && npm run typecheck:web && npm run check:i18n && npm run check:tasks
```

## Notes

- Kept 100% file-disjoint from Wave 2 (PR #2188) and Wave 3A (PR #2189).
- `/foods` filtered URLs already canonicalize cleanly to `/${locale}/foods` via `layout.tsx` (`e2e/seo.spec.ts`), and `robots-directives.test.ts` intentionally keeps `/foods` as its no-noindex control route, so `/foods` was left untouched.
- To activate `Organization.sameAs` in production, set `NEXT_PUBLIC_SITE_SAME_AS=https://www.youtube.com/@...` in the web environment.
