---
id: 2026-11-20-frontend-exposure-rescue-wave-3a-dedicated
title: Frontend exposure rescue wave 3A: dedicated /videos/[slug] watch pages, GET /videos/{slug} API, and /sitemap-videos.xml
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-20T15:45:33Z
created_at: 2026-11-20T15:45:17Z
completed_at: 2026-11-20T15:49:18Z
branch: agy/frontend-exposure-wave3a-video-watch
depends_on: []
scope:
  - apps/web/messages/zh-TW/common.json
---

# Frontend exposure rescue wave 3A: dedicated /videos/[slug] watch pages, GET /videos/{slug} API, and /sitemap-videos.xml

## Why

All published Mokaair YouTube videos previously lived on a single `/[locale]/videos` gallery page. Google Video Search and Google Discover strongly prefer dedicated watch pages (one canonical URL per video with its own `<title>`, `VideoObject` structured data, high-priority hero thumbnail, companion editorial content, and a Google Video Sitemap).

## Definition of done

- [x] `GET /api/v1/videos/{slug}` returns a published video plus up to 6 same-category-first related published videos, and 404s for unknown, scheduled-future, private, unuploaded, or dropped videos.
- [x] Dedicated `/[locale]/videos/[slug]` watch page renders with `DISCOVER_ROBOTS`, `video.other` OpenGraph metadata, `VideoObject` + `BreadcrumbList` + related `ItemList` JSON-LD, privacy-preserving `youtube-nocookie` player with `fetchPriority="high"` thumbnail, companion article handover card, and related video cards.
- [x] `VideoCard` links every video title to its `/videos/[slug]` watch page.
- [x] `/sitemap-videos.xml` serves a Google Video Sitemap (`sitemap-video/1.1`) for all published watch pages (returning `503` with `Retry-After` on API outage) and is advertised in `robots.ts`.
- [x] All 5 locale `common.json` message files include watch-page copy and pass `check:i18n`.

## Steps

- [x] Add `GET /api/v1/videos/{slug}` (`PublicVideoDetail`) in `apps/api/app/video_reviews/public_api.py` and tests in `apps/api/tests/test_public_videos.py`.
- [x] Add `videoHref`, `getVideo`, and `getAllPublishedVideos` in `apps/web/lib/videos.ts` & `videos.server.ts`.
- [x] Add `/sitemap-videos.xml` (`apps/web/lib/video-sitemap.ts`, `apps/web/app/sitemap-videos.xml/route.ts` + tests) and advertise in `apps/web/app/robots.ts`.
- [x] Link `VideoCard` headings to `/videos/[slug]`, add `VideoWatchPlayer`, add `/[locale]/videos/[slug]` page + tests, and localize the 3 new labels across all 5 locales.

## How to verify

```bash
cd apps/api && uv run ruff check app/video_reviews/public_api.py tests/test_public_videos.py && uv run mypy app/video_reviews/public_api.py tests/test_public_videos.py && uv run pytest tests/test_public_videos.py -v
cd apps/web && npx vitest run app/sitemap-videos.xml/route.test.ts app/robots.test.ts "app/[locale]/videos/page.test.tsx" "app/[locale]/videos/[slug]/page.test.tsx"
npm run lint:web && npm run typecheck:web && npm run check:i18n && npm run check:tasks
```

## Notes

- Claimed with `--force` over two stale October video-worker claims (`2026-10-19-worker-video-languages-five`, `2026-10-29-daily-brief-on-the-host-worker`).
- Kept 100% file-disjoint from Wave 2 (PR #2188), branching cleanly off `origin/main` (which includes Wave 1 PR #2187).
