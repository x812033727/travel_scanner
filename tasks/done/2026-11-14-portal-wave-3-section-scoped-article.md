---
id: 2026-11-14-portal-wave-3-section-scoped-article
title: Portal Wave 3: section-scoped article recirculation, Osaka/Taipei stay decisions, and About draft sync
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-14T04:13:06Z
created_at: 2026-11-14T04:12:50Z
completed_at: 2026-11-14T04:28:49Z
branch: claude/portal-wave3-content-relevance
depends_on: []
scope:
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/app/(ads-public)/[locale]/life/[slug]/page.test.tsx
  - apps/web/lib/destination-decisions.json
  - apps/web/components/destination-guide.test.tsx
  - apps/web/app/[locale]/destinations/[destinationId]/page.test.tsx
  - docs/adsense-osaka-taipei-sources.md
  - apps/api/app/site_pages/drafts/en.json
  - apps/api/app/site_pages/drafts/ja.json
  - apps/api/app/site_pages/drafts/ko.json
  - apps/api/app/site_pages/drafts/zh-CN.json
  - apps/api/app/site_pages/drafts/zh-TW.json
  - apps/api/tests/test_site_pages_drafts.py
---

# Portal Wave 3: section-scoped article recirculation, Osaka/Taipei stay decisions, and About draft sync

## Why

Post-deploy inspection of Wave 2 (`PR #2097`) surfaced three content-value and topical-coherence gaps ahead of Google AdSense review:

1. **Cross-section trending recirculation on article pages**: `fetchRailTrending` in `apps/web/components/guides/article-page.tsx` queries `getTrendingGuides(locale, {}, 6)` without section or topic filters, causing AI/tech/finance `/life/*` articles (e.g. `/zh-TW/life/ai-tools-2026-overview`) to render five unrelated travel transport guides in the desktop/mobile `熱門閱讀` rail, and non-hub `life` articles without API-ranked `state.related` have no same-section fallback.
2. **Thin flagship destination hubs beyond Tokyo and Seoul**: `/destinations/osaka-kyoto` and `/destinations/taipei` still render bare catalog area name pills (`難波／心齋橋、梅田、京都站、四條河原町` and `台北車站、西門町、信義區、中山`) instead of sourced 5-locale stay decision cards before partner modules.
3. **Out-of-date default `about` drafts in `apps/api/app/site_pages/drafts/*.json`**: The shipped `about` draft JSON files still carry travel-only copy rather than the approved 5-locale multi-topic + AI-assistance + corrections copy in `docs/adsense-about-drafts.md`.

## Definition of done

- [x] Article right-rail / mobile trending (`railTrending`) is scoped to the article's `section` (preferring its primary `topic` first and topping up from `section`), excludes the current article, series-related lessons, and `RelatedGrid` items, and never mixes travel guides into `life` articles (or vice versa).
- [x] Non-hub `life` articles with no `state.related` entries fall back to same-topic / same-section `life` articles in `RelatedGrid` when available.
- [x] `apps/web/lib/destination-decisions.json` includes sourced 5-locale stay decision cards for `osaka-kyoto` and `taipei` using verified `https://` official tourism and rail primary sources documented in `docs/adsense-osaka-taipei-sources.md`, with no fares, journey minutes, or firsthand-stay claims.
- [x] `apps/api/app/site_pages/drafts/{en,ja,ko,zh-CN,zh-TW}.json` sync the `"about"` section with `docs/adsense-about-drafts.md` while keeping `effective_date: null`, preserving `requirements`, and maintaining identical block shapes across all 5 locales.

## Steps

- [x] Scope `fetchRailTrending` and add `relatedLife` fallback in `apps/web/components/guides/article-page.tsx`, plus unit tests in `apps/web/components/guides/article-page.test.tsx`.
- [x] Add `osaka-kyoto` and `taipei` 5-locale stay decisions to `apps/web/lib/destination-decisions.json`, document verified primary sources in `docs/adsense-osaka-taipei-sources.md`, and update `destination-guide.test.tsx` + `destinations/[destinationId]/page.test.tsx`.
- [x] Sync `"about"` across `apps/api/app/site_pages/drafts/{en,ja,ko,zh-CN,zh-TW}.json` and add AI-disclosure / corrections coverage in `apps/api/tests/test_site_pages_drafts.py`.
- [x] Run web, i18n, task, and API checks cleanly before marking the task `done`.

## How to verify

```bash
npm run check:tasks && npm run check:i18n && npm run lint:web && npm run typecheck:web
cd apps/web && npx vitest run components/guides/article-page.test.tsx components/destination-guide.test.tsx 'app/[locale]/destinations/[destinationId]/page.test.tsx'
cd apps/api && uv run ruff check app/site_pages tests/test_site_pages_drafts.py && uv run mypy app/site_pages tests/test_site_pages_drafts.py && uv run pytest tests/test_site_pages_drafts.py
```

## Notes

- All 18 unique official URLs across `osaka-kyoto` (`osaka-info.jp`, `nankai.co.jp`, `westjr.co.jp`, `kyoto.travel`) and `taipei` (`travel.taipei`, `tymetro.com.tw`) were fetched and verified HTTP 200 on 2026-11-14 UTC before authoring copy.
- `relatedLife` passes `{ section: "life", kind: "life" }` so `tools/e2e-runtime-api.mjs` (which filters `/api/v1/guides` by `kind`) and the real API both stay section-scoped, and gates on `!isHub && !state.series && !geminiSeries` so series lessons retain chapter-only navigation.
- Syncing `"about"` in `apps/api/app/site_pages/drafts/*.json` updates the default shipped drafts for fresh environments and `/admin/site-pages` resets; the production database still requires publishing `/about` once in `/admin/site-pages` if an older DB draft was already seeded.
