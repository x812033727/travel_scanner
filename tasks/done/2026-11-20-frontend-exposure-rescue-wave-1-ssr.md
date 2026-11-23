---
id: 2026-11-20-frontend-exposure-rescue-wave-1-ssr
title: Frontend exposure rescue wave 1: SSR header nav, dynamic article OG cards, sitemaps/robots/VideoObject, destination SEO titles, and social share links
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-20T14:45:44Z
created_at: 2026-11-20T14:45:28Z
completed_at: 2026-11-20T15:10:11Z
branch: agy/frontend-exposure-wave1
depends_on: []
scope:
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/sitemap.py
  - apps/api/tests/test_guides.py
  - apps/web/components/discovery-status-provider.tsx
  - apps/web/app/[locale]/layout.tsx
  - apps/web/app/[locale]/layout.test.tsx
  - apps/web/components/site-navigation.tsx
  - apps/web/components/site-navigation.test.tsx
  - apps/web/lib/article-og.ts
  - apps/web/app/og/[locale]/[kind]/[slug]/card.png/route.tsx
  - apps/web/app/og/[locale]/[kind]/[slug]/card.png/route.test.ts
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/app/sitemap.xml/route.ts
  - apps/web/app/sitemap.xml/route.test.ts
  - apps/web/app/sitemaps/sitemap.ts
  - apps/web/app/sitemaps/sitemap.test.ts
  - apps/web/app/llms.txt/route.ts
  - apps/web/app/llms.txt/route.test.ts
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/app/[locale]/videos/page.tsx
  - apps/web/app/[locale]/videos/page.test.tsx
  - apps/web/lib/destinations-copy.json
  - apps/web/app/[locale]/destinations/[destinationId]/page.tsx
  - apps/web/app/[locale]/destinations/[destinationId]/page.test.tsx
  - apps/web/components/guides/article-share-bar.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/e2e/seo.spec.ts
---

# Frontend exposure rescue wave 1: SSR header nav, dynamic article OG cards, sitemaps/robots/VideoObject, destination SEO titles, and social share links

## Why

Several technical gaps were suppressing Mokaair's search, Google Discover, Google News, video, and social exposure:
1. `SiteNavigation` gated all 26 primary header nav links behind `!discovery.loading`, which was always `true` during SSR because `LocaleLayout` did not provide `getDiscoveryStatus()`, leaving `<header><nav>` as an empty skeleton in server HTML.
2. Articles without bespoke editorial photography (including automated news stories whose synthetic artwork is suppressed) fell back to the static site-wide `/og.png` and omitted `image` from `Article`/`NewsArticle` JSON-LD, hurting Google Discover eligibility and social CTR.
3. `/robots.txt` did not declare `/sitemap-news.xml`, `/sitemap.xml` index children omitted `<lastmod>`, and `/videos` was absent from `SITEMAP_ROUTES`, `/llms.txt`, and `VideoObject` JSON-LD.
4. All 165 city destination guide pages (`33 destinations x 5 locales`) used a bare `{city} | Mokaair` `<title>` without travel-intent keywords.
5. `ArticleShareBar` lacked zero-script share links for Threads, Facebook, and X.

## Definition of done

- [x] `LocaleLayout` provides server-resolved discovery state via `DiscoveryStatusProvider` so `SiteNavigation` renders primary editorial and directory links directly in SSR HTML without hydration mismatch.
- [x] Articles without bespoke photography resolve `og:image`, `twitter:image`, and `Article`/`NewsArticle` JSON-LD `image` to a dynamic `1200x630` PNG card at `/og/[locale]/[kind]/[slug]/card.png` (outside `/api/` and `proxy.ts`, with static `/og.png` fallback if CJK font loading fails).
- [x] `/robots.txt` advertises both `/sitemap.xml` and `/sitemap-news.xml`, `/sitemap.xml` emits real per-child `<lastmod>` from `GET /guides/sitemap/summary`, `/videos` is listed per published locale in `static` sitemap and `/llms.txt`, and `/videos` plus article embedded videos emit `VideoObject` JSON-LD.
- [x] Destination guide pages render localized intent-rich SEO `<title>` templates across all 5 locales.
- [x] `ArticleShareBar` includes zero-script Threads, Facebook, and X share anchors across all 5 locales.

## Steps

- [x] Add `latest_modified_at` to API `/guides/sitemap/summary` and emit `<lastmod>` on section children in `/sitemap.xml`.
- [x] Add `DiscoveryStatusProvider`, seed it in `LocaleLayout`, and resolve it in `SiteNavigation` for SSR links.
- [x] Add `lib/article-og.ts`, `/og/[locale]/[kind]/[slug]/card.png/route.tsx`, and wire into `article-page.tsx`.
- [x] Add `/sitemap-news.xml` to `robots.ts`, `/videos` to `SITEMAP_ROUTES` and `/llms.txt`, and `videoObject` structured data to `/videos` and `article-page.tsx`.
- [x] Upgrade destination `<title>` across all 5 locales in `destinations-copy.json` and `destinations/[destinationId]/page.tsx`.
- [x] Add Threads, Facebook, and X share links to `ArticleShareBar` and 5-locale `common.json`.

## How to verify

Run:
- `cd apps/api && uv run ruff check app/guides/schemas.py app/guides/sitemap.py tests/test_guides.py && uv run mypy app/guides/schemas.py app/guides/sitemap.py && uv run pytest tests/test_guides.py -k sitemap && uv run pytest tests/test_guides_sitemap_pagination.py`
- `npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web`

## Notes

- Claimed with `--force` over two stale October video-worker claims (`2026-10-19-worker-video-languages-five`, `2026-10-29-daily-brief-on-the-host-worker`) whose broad `apps/web/messages/` scope was for admin keys; this task only adds three public share keys to `common.json`.
- `/og/[locale]/[kind]/[slug]/card.png` is intentionally outside `/api/` (so `robots.ts` allows crawlers) and ends in `.png` (so `proxy.ts` skips locale rewriting).
- Note on open PR #2103 (`claude/portal-wave4-seo-web-ux`, stuck failing `web-e2e` since 2026-11-14): this branch incorporates `sitemap-news.xml` in `robots.ts` and `VideoObject` on `/videos` cleanly on top of current `origin/main`.
