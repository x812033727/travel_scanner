---
id: 2026-11-13-portal-wave-2-google-news-sitemap
title: Portal wave 2: Google News sitemap, Discover metadata, article scroll-spy/share/trending rail, category depth and CJK intent search
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-13T08:11:01Z
created_at: 2026-11-13T08:09:35Z
completed_at: 2026-11-13T08:49:51Z
branch: claude/portal-wave2-discovery-seo
depends_on: []
scope:
  - apps/api/app/guides/search.py
  - apps/api/tests/test_guides_search.py
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_ai.py
  - apps/web/app/sitemap-news.xml
  - apps/web/app/feed.xml
  - apps/web/app/llms.txt
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/search/articles
  - apps/web/components/home-guides.tsx
  - apps/web/components/home-guides.test.tsx
  - apps/web/components/home-portal-tabs.tsx
  - apps/web/components/guides
  - apps/web/components/site-search
  - apps/web/lib/seo.ts
  - apps/web/lib/news-sitemap.ts
  - apps/web/lib/news-sitemap.test.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-TW/navigation.json
  - tools/e2e-runtime-api.mjs
---

# Portal wave 2: Google News sitemap, Discover metadata, article scroll-spy/share/trending rail, category depth and CJK intent search

## Why

Wave 1 (`#2094`) repositioned Mokaair as an information-publishing and discovery portal. After deploying Wave 1 to `mokaair.com`, five concrete gaps remain against top-tier Chinese tech/lifestyle media (`kocpc.com.tw`, `maplefeather.com`):

1. **Google News & Discover technical signals**: There is no dedicated 48-hour Google News Sitemap (`/sitemap-news.xml`), published article pages and the home page do not emit explicit `googleBot` `max-image-preview:large` / `max-snippet:-1` directives for Google Discover, `/feed.xml` omits Atom `<author>` and `<category>` metadata, and `/llms.txt` does not advertise `/feed.xml` or `/sitemap-news.xml`.
2. **Article reading UX & recirculation**: Most organic search visitors land directly on an article page, yet desktop TOC links have no active scroll-spy highlight or reading progress indicator, articles lack zero-script 1-click Copy Link / LINE / Web Share actions, and desktop right rails have no **Trending** recirculation (short `< 3` heading news stories have no right rail at all).
3. **Portal category depth & newsroom scannability**: Homepage category tabs (`AI`, `Travel`, `Money`) only fetch 4 compact cards in a single column, and `NewsList` on `/life` (merged across 3 verticals) and news topic hubs omits topic badges and optional summary lines.
4. **Search recall & zero-dead-end discovery**: Multi-term CJK search queries containing generic intent modifiers (`日本 eSIM 推薦`, `Gemini CLI 教學`) or colloquial Taiwan synonyms (`日幣`, `韓幣`, `網卡`) return 0 hits when the article title uses different phrasing (`怎麼選`, `日圓`, `韓元`), and `SiteSearchDialog` / `/search/articles` do not surface live trending articles before typing or on zero-hit searches.
5. **Daily news rollout clarity**: Automated news writer/editor prompts benefit from explicit rollout-stage clarity (live vs preview vs plan/region-limited as stated by the evidence) in the opening triage and comparison table.

## Definition of done

- [x] `/sitemap-news.xml` serves valid Google News Sitemap XML for dated news published in the last 48 hours across all 5 locales (`zh-tw`, `zh-cn`, `en`, `ja`, `ko` language codes) and answers `503` with `Retry-After: 600` on upstream failure, without altering `/sitemap.xml` children or `robots.ts` `sitemap`.
- [x] Published articles (`guideArticleMetadata`) and `/` (`app/[locale]/page.tsx`) emit `googleBot` `max-image-preview: "large"`, `max-snippet: -1`, `max-video-preview: -1` while hub pages keep `<meta name="robots">` count 0 when indexable (`e2e/seo.spec.ts` invariant).
- [x] `/feed.xml` emits `<author><name>Mokaair</name></author>` and `<category>` tags, and `/llms.txt` lists `/feed.xml` and `/sitemap-news.xml`.
- [x] Published article pages render a zero-external-script share bar (Copy Canonical Link, LINE share link, progressive Web Share), progressive scroll-spy TOC with reading progress and back-to-top, and a desktop right-rail Trending recirculation card (even for `< 3` heading news articles when trending items exist).
- [x] Homepage category tabs expand up to 8 articles (lead card featured + matching series hubs) while keeping `"all"` overview compact at 4 per column; `NewsList` supports `showTopic` on `/life` and `showDescription` on news topic hubs.
- [x] Backend `/guides/search` falls back cleanly on zero hits by stripping CJK/English intent modifiers (`推薦`, `教學`, `攻略`, `比較`, etc.) when core entity terms remain and expanding Taiwan/CJK colloquial synonyms (`日幣`/`日圓`, `韓幣`/`韓元`, `台幣`/`新台幣`, `網卡`/`esim`, `筆電`/`筆記型電腦`), and `SiteSearchDialog` + `/search/articles` surface trending articles and `news_date`.

## Steps

- [x] Upgrade `apps/api/app/guides/search.py` and `apps/api/app/news_automation/ai.py` with tests in `test_guides_search.py` and `test_news_ai.py`.
- [x] Add `apps/web/lib/news-sitemap.ts` (+ unit tests), `apps/web/app/sitemap-news.xml/route.ts`, Discover `googleBot` metadata on `/` and published articles, and `/feed.xml` + `/llms.txt` improvements.
- [x] Add 5-locale UI strings in `common.json` and `navigation.json`, implement `ArticleShareBar`, `ArticleTocRail`, and desktop right-rail Trending recirculation in `article-page.tsx` and `article.tsx`.
- [x] Upgrade `home-guides.tsx`, `home-portal-tabs.tsx`, `news-list.tsx`, `life/page.tsx`, `topic-hub-page.tsx`, `site-search-dialog.tsx`, `search/articles/page.tsx`, `search-results.tsx`, and `tools/e2e-runtime-api.mjs`.
- [x] Run `check:tasks`, `check:i18n`, `lint:web`, `typecheck:web`, `vitest`, `test:tools`, and API `ruff`/`mypy`/`pytest`.

## How to verify

```bash
npm run check:tasks && npm run check:i18n && npm run lint:web && npm run typecheck:web
cd apps/web && npx vitest run --maxWorkers=2
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_guides.py tests/test_guides_search.py tests/test_news_ai.py -q
```

## Notes

- Claimed with `--force` because the three overlapping tickets (`2026-10-19-worker-video-languages-five` at 579 h, `2026-10-29-daily-brief-on-the-host-worker` at 358 h, and `2026-10-29-news-automation-drafts-notable-new-ai` at 365 h) are all >14 days stale (>24 h threshold) with no active worktree or competing portal PR (`who-is-on-it.mjs` verified).
