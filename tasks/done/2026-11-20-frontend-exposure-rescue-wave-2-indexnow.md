---
id: 2026-11-20-frontend-exposure-rescue-wave-2-indexnow
title: Frontend exposure rescue wave 2: IndexNow instant indexing, homepage SearchAction/ItemList, Atom media thumbnails, and LCP hero fetchPriority
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-20T15:17:34Z
created_at: 2026-11-20T15:17:15Z
completed_at: 2026-11-20T15:36:59Z
branch: agy/frontend-exposure-wave2
depends_on: []
scope:
  - apps/api/app/config.py
  - apps/api/app/guides/indexnow.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/cli.py
  - apps/api/tests/test_indexnow.py
  - apps/web/app/indexnow-key.txt/route.ts
  - apps/web/app/indexnow-key.txt/route.test.ts
  - docker-compose.prod.yml
  - ops/nginx/mokaair.conf.example
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/page.seo.test.tsx
  - apps/web/app/feed.xml/route.ts
  - apps/web/app/feed.xml/route.test.ts
  - apps/web/lib/guide-atom-feed.ts
  - apps/web/lib/guide-atom-feed.test.ts
  - apps/web/components/home-portal-tabs.tsx
  - apps/web/components/guides/card.tsx
  - apps/web/components/guides/card.test.tsx
---

# Frontend exposure rescue wave 2: IndexNow instant indexing, homepage SearchAction/ItemList, Atom media thumbnails, and LCP hero fetchPriority

## Why

After Wave 1 (PR #2187) fixed SSR navigation, dynamic OG cards, sitemap freshness, VideoObject JSON-LD, destination SEO titles, and social share buttons, four additional organic-discovery bottlenecks remained:

1. **No IndexNow push notification**: New and updated guides/news waited for passive Bing/Yandex/Seznam/Naver crawls instead of being pushed on publish/unpublish or via a backfill CLI.
2. **Homepage structured data gaps**: `apps/web/app/[locale]/page.tsx` gated `WebSite.potentialAction` (`SearchAction`) on `hotspotsEnabled` even though `/search/articles` is always public, and omitted an `ItemList` graph for the homepage news headlines.
3. **Plain-text Atom feeds**: `/feed.xml` and `/[locale]/life/**/feed.xml` emitted no `<media:thumbnail>` tags, costing visual CTR in feed aggregators and discovery surfaces.
4. **Unprioritized LCP hero images**: The homepage lead hero (`HomePortalTabs`) and featured hub cards (`GuideCard`) loaded eagerly without `fetchPriority="high"`.

## Definition of done

- [x] `INDEXNOW_KEY` + host-pinned `INDEXNOW_ENDPOINT` (`api.indexnow.org`) added to API settings, with automatic best-effort IndexNow push on guide publish/unpublish and `python -m app.cli indexnow-submit` for dry-run/backfill.
- [x] Web `/indexnow-key.txt` route serves `INDEXNOW_KEY` as `text/plain` (404 when unset/invalid), wired in `docker-compose.prod.yml` and allowed in `ops/nginx/mokaair.conf.example`.
- [x] Homepage emits `SearchAction` unconditionally and includes an `ItemList` graph for rendered news articles.
- [x] `/feed.xml` and `buildGuideAtomFeed` declare `xmlns:media` and emit `<media:thumbnail>` for articles with real editorial heroes (skipping synthetic `/guides/news-assets/` placeholders).
- [x] Homepage lead hero and featured `GuideCard` set `fetchPriority="high"`.
- [x] API ruff/mypy/pytest and web lint/i18n/typecheck/vitest pass cleanly.

## Steps

- [x] Add host-pinned IndexNow settings, client module (`apps/api/app/guides/indexnow.py`), publish/unpublish hooks, CLI command, and pytest coverage.
- [x] Add `/indexnow-key.txt` Next.js route + unit tests, `docker-compose.prod.yml` env pass-through, and nginx crawl-control rule.
- [x] Fix homepage `SearchAction` and add news `ItemList` JSON-LD + update `page.seo.test.tsx`.
- [x] Add Media RSS `<media:thumbnail>` to `/feed.xml` and `guide-atom-feed.ts` + update feed tests.
- [x] Add `fetchPriority="high"` to `HomePortalTabs` lead hero and featured `GuideCard` + update `card.test.tsx`.

## How to verify

```bash
cd apps/api && uv run ruff check app/config.py app/guides/indexnow.py app/guides/admin_service.py app/cli.py tests/test_indexnow.py && uv run mypy app/config.py app/guides/indexnow.py app/guides/admin_service.py app/cli.py && uv run pytest tests/test_indexnow.py tests/test_guides.py
cd apps/web && npx vitest run app/indexnow-key.txt/route.test.ts "app/[locale]/page.seo.test.tsx" app/feed.xml/route.test.ts lib/guide-atom-feed.test.ts components/guides/card.test.tsx components/home-guides.test.tsx
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run check:tasks
```

## Notes

- Claimed with `--force` over two stale Nov 12–13 MiniMax video-worker claims (`apps/api/app/config.py`) that had no active edits on `main`.
- Deliberately kept 100% file-disjoint from Wave 1 (PR #2187) so both PRs merge without conflict.
- To activate IndexNow on production after deploy: set `INDEXNOW_KEY=<32-hex-chars>` in production `.env`, restart `api` + `web`, verify `https://mokaair.com/indexnow-key.txt`, and run `python -m app.cli indexnow-submit --since-hours 168 --apply`.
