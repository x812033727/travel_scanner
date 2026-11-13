---
id: 2026-11-13-reposition-mokaair-as-an-information-portal
title: Reposition Mokaair as an information portal with SEO, CJK search, trending rail, Atom feeds and upgraded daily news pipeline
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-13T02:13:21Z
created_at: 2026-11-13T02:13:01Z
completed_at: 2026-11-13T05:44:46Z
branch: claude/portal-seo-news-upgrade
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/page.test.tsx
  - apps/web/app/[locale]/guides
  - apps/web/app/[locale]/life
  - apps/web/app/[locale]/search/articles
  - apps/web/components/site-header.tsx
  - apps/web/components/site-footer.tsx
  - apps/web/components/content-blocks.tsx
  - apps/web/components/guide-code-block.tsx
  - apps/web/components/home-guides.tsx
  - apps/web/components/home-guides.test.tsx
  - apps/web/components/home-portal-tabs.tsx
  - apps/web/components/guides
  - apps/web/components/site-search
  - apps/web/e2e/guides-adsense.spec.ts
  - apps/web/lib/nav-links.ts
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/lib/guide-atom-feed.ts
  - apps/web/lib/guide-atom-feed.test.ts
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/en/navigation.json
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/messages/zh-TW/search.json
  - apps/api/app/guides/router.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/service.py
  - apps/api/app/guides/search.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_search.py
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_ai.py
  - apps/api/tests/test_news_sources_cli.py
---

# Reposition Mokaair as an information portal with SEO, CJK search, trending rail, Atom feeds and upgraded daily news pipeline

## Why

Mokaair (`mokaair.com`) has grown hundreds of AI, tech, lifestyle, finance and travel articles plus an automated news pipeline, yet its homepage (`/`), header navigation, structured data (`WebSite` `SearchAction`), article search, and news editorial prompts still behave like a trip-planning landing page with three small text-only guide lists. Readers looking for daily tech/AI/software news and practical comparison guides (benchmarked against `kocpc.com.tw` and `maplefeather.com`) cannot scan breaking news, filter categories on `/`, subscribe via RSS/Atom, see real reader-driven trending articles, or match mixed-script / natural-language CJK queries in `/search/articles`.

## Definition of done

- [x] Homepage (`/`) leads as an information-publishing and information-discovery portal: hero featured story + secondary visual picks, merged real-time daily news desk (`ai-news`, `tech-news`, `crypto`) with Atom feed links, interactive category filter tabs (`全部`, `即時快訊`, `AI 應用`, `科技與軟體`, `旅遊攻略`, `投資理財`), real reader-trending + editorial picks sidebar, series hubs, and compact quick-entry bar to travel comparison (`/search/new`), hotspots, foods and tools across all 5 locales.
- [x] Global navigation (`nav-links.ts`) prioritizes `AI 應用`, `生活科技` (including `科技新聞`), and `旅遊情報攻略`; `GuideCard` supports full-card stretched-link clickability, cleaner editorial typography, and optional `news_date` display; `/life` and news topic hubs expose valid UTF-8 Atom 1.0 feeds (`/[locale]/life/feed.xml` and `/[locale]/life/topics/[topic]/feed.xml`) with `<link rel="alternate" type="application/atom+xml">`.
- [x] SEO & structured data: `webSite()` emits `SearchAction` targeting `/{locale}/search/articles?q={search_term_string}`; `guideArticle()` emits `NewsArticle` when `newsDate` is present (`Article` for evergreen guides) and dated news articles display `news_date` cleanly alongside `updated` and reading time.
- [x] Backend trending & search (`apps/api/app/guides`): `GET /api/v1/guides/trending` ranks published articles by real non-bot `AnalyticsEvent` (`page_view`) traffic over a rolling window with honest `featured`/curated backfill (never fabricating view numbers); `/guides/search` splits mixed ASCII/CJK queries (`Gemini教學` -> `gemini`, `教學`), falls back gracefully on multi-character CJK phrases, and supports `sort=relevance|latest` plus topic/sort chips on `/search/articles` and quick topic shortcuts in `SiteSearchDialog`.
- [x] Daily news automation (`apps/api/app/news_automation`): `sources.json` broadens lead keywords and validated official evidence sources across AI tools, Apple/Google/Microsoft/browser/creative software updates; `ai.py` upgrades writer/editor/judge instructions for search-intent conclusion-first titles, 3-sentence first-screen triage (what changed, who gets it, free/paid/Taiwan availability), non-redundant `summary` / comparison `table` / `callout` / query-driven H2s / `faq` while keeping strict evidence-only verification.
- [x] Article reading architecture & synthetic artwork cleanup: suppress synthetic `/guides/news-assets/` (`Original editorial artwork`) placeholder boxes across article bodies, cards, homepage leads, search results, OpenGraph/Twitter and JSON-LD while keeping backend `lint_document` compatibility; upgrade article pages (`article-page.tsx`, `article.tsx`, `content-blocks.tsx`, `guide-code-block.tsx`, `related-grid.tsx`, `series-navigation.tsx`, `partner-link.tsx`, `travel-crosslinks.tsx`) to a 2-column desktop layout with elevated reading sheet, sticky desktop TOC rail, collapsible mobile TOC, accented H2s, constrained wide diagrams, and compact Sources card; polish remaining hubs and chrome (`/ai`, `/guides`, `/guides/[kind]`, `SeriesRow`, `DestinationGroups`, `ListingToolbar`, `SiteFooter`).

## Steps

- [x] Add `GET /api/v1/guides/trending` and upgrade `apps/api/app/guides/search.py` (mixed ASCII/CJK splitting, CJK bigram fallback when strict AND finds zero, `sort=relevance|latest`) with unit/integration tests.
- [x] Upgrade `apps/api/app/news_automation/ai.py` and `sources.json` and verify source/AI tests.
- [x] Add 5-locale copy in `apps/web/messages/{en,zh-TW,zh-CN,ja,ko}` (`metadata`, `navigation`, `search`, `common`), update `structured-data.ts`, `guides.ts`, `guides.server.ts`, and add `guide-atom-feed.ts` + feed routes.
- [x] Upgrade `HomeGuides` / `HomePortalTabs`, `page.tsx`, `nav-links.ts`, `GuideCard`, `NewsList`, `/life`, `topic-hub-page.tsx`, `article.tsx` / `article-page.tsx`, `/search/articles`, and `SiteSearchDialog`.
- [x] Remove synthetic `/guides/news-assets/` placeholder artwork across all reader/social surfaces, upgrade article page to a 2-column desktop architecture with elevated reading sheet and sticky TOC rail, and polish `/ai`, `/guides`, `GuideCodeBlock`, and `SiteFooter`.
- [x] Run web, i18n, tools, tasks, and API checks and update tests.

## How to verify

```bash
npm run check:tasks && npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web && npm run test:tools
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_guides.py tests/test_guides_search.py tests/test_news_ai.py tests/test_news_sources_cli.py -q
```

## Notes

- Reuses existing first-party `AnalyticsEvent` (`event_name = 'page_view'`, `is_bot = False`, `normalized_path`) so real reader popularity works immediately in production without a database schema migration, falling back cleanly to `featured` / curated articles on cold start without inventing view counts (`docs/seo.md`).
- Deduplicates article slugs across `blocks`, `news`, `software`, `trending`, and `series` in `loadHomeGuides(locale)` so no article link appears twice on `/`, while preserving all Playwright geometry and SSR contracts (`section[aria-labelledby="home-guides-title"] > p`, `/search/new` CTA in initial viewport, `home-guides-*` compact card columns).
- `/[locale]/life/feed.xml` and `/[locale]/life/topics/[topic]/feed.xml` answer HTTP 503 with `Retry-After: 600` when the upstream API is unavailable so feed readers do not replace cached entries with an empty feed during deploys.
- Frontend visual layout polish across reader surfaces (`SiteHeader`, `SiteFooter`, `globals.css`, `HomeGuides`, `HomePortalTabs`, `page.tsx`, `GuideCard`, `NewsList`, `HubHero`, `TopicTiles`, `AiHubRails`, `SeriesRow`, `DestinationGroups`, `ListingToolbar`, `SearchResultCard`, `GuideArticle`, `article-page.tsx`, `ContentBlocks`, `GuideCodeBlock`, `/life`, `/guides`, `/guides/[kind]`, `/search/articles`, `topic-hub-page.tsx`): full-bleed sticky masthead, multi-layered `--surface` over `--paper` elevation across light/dark and all 3 palettes (`mocha`, `lagoon`, `forest`), 2-column desktop article layout with elevated reading sheet and sticky right-rail TOC, and frontend suppression (`visibleGuideHero`, `isSyntheticNewsBlock`) of generic `/guides/news-assets/` (`Original editorial artwork`) placeholders across both historical DB articles and newly generated news items without breaking backend `lint_document` / localization validators.
