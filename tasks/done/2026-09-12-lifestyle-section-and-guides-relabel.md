---
id: 2026-09-12-lifestyle-section-and-guides-relabel
title: 生活分享專區與旅遊情報攻略改名
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T14:18:00Z
created_at: 2026-09-12T14:17:59Z
completed_at: 2026-09-12T15:32:46Z
branch: claude/travel-info-lifestyle-sharing-cf720f
depends_on: []
scope:
  - apps/api/app/guides
  - apps/api/migrations/versions/0074_lifestyle_guides.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_migration.py
  - apps/api/tests/test_migration_dead_branches.py
  - apps/api/tests/test_travel_services.py
  - apps/api/tests/test_affiliate_brand_channels.py
  - apps/api/tests/test_admin_operations.py
  - apps/web/app/[locale]/guides
  - apps/web/app/[locale]/life
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/app/robots.test.ts
  - apps/web/components/guides
  - apps/web/components/guides-navigation.test.tsx
  - apps/web/components/site-navigation.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/components/community/explore.tsx
  - apps/web/components/community/explore.test.tsx
  - apps/web/components/community/home.tsx
  - apps/web/components/community/home.test.tsx
  - apps/web/components/community/travel-tools.test.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-list.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/admin.test.tsx
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/lib/guide-affiliate.ts
  - apps/web/lib/guide-affiliate.test.ts
  - apps/web/lib/nav-links.ts
  - apps/web/lib/hotel-booking-placement.ts
  - apps/web/lib/admin-operations.test.ts
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/e2e/seo.spec.ts
  - apps/web/e2e/discovery.spec.ts
  - tools/e2e-runtime-api.mjs
  - docs/travel-guides.md
  - docs/travel-services.md
  - docs/affiliate-configuration.md
  - docs/seo.md
---

# 生活分享專區與旅遊情報攻略改名

## Why

站主要把導覽的「情報攻略」改成「旅遊情報攻略」，並另開一個與旅遊無關的「生活分享」專區
（AI 資訊與教學、工具、其他），用更多可索引內容換曝光，再把讀者導向已有分潤按鈕的頁面。
規劃時另外查到兩個要一起處理的既有問題：

- `/admin/guides` 在正式站根本進不去：API 的 `NAVIGATION_REGISTRY` 沒有 guides 項目，
  `visibleAdminNavigation` 只有 server 清單為空時才用 web fallback，`canAccessAdminPath` 直接 forbidden。
- 五個 `navigation.json` 的 scope 被 `2026-09-06-legal-content-from-owner`（review）持有；
  該票的 navigation.json 步驟已在 `fc274a1d` 合併，已做窄幅釋放（見該票 Notes）。

設計主軸：不建第二套文章系統。`guide_articles.kind` 多一個值 `life`，沿用同一套
model／revision／audit／publication／後台編輯器；「專區」只在 URL（`/life`）、導覽、主題詞彙
（`guide_topics.section`）、文末區塊四處分岔。完整計畫與決策理由在 PR 說明。

## Definition of done

- [x] 五個語系的導覽與 footer 都顯示「旅遊情報攻略」與「生活分享」兩個入口，三種導覽模式與手機 discovery 分支各出現一次。
- [x] `/life`、`/life/{slug}` 可讀、可索引、進 sitemap；`/guides/life/{slug}` 是 404。
- [x] 後台 `/admin/guides` 從側欄進得去；能建立 `life` 文章，主題只列七個 life 主題；已發布的文章不能跨專區改 kind。
- [x] life 文章文末永遠有「最新旅遊情報攻略」＋「熱門目的地」內部連結；填了目的地且後台勾了「生活分享」置入面才出現合作方按鈕，clickout 記錄 `placement='life'`。
- [x] Migration 0073 在 SQLite 兩腿與 PostgreSQL 都通過；既有旅遊主題 `section='travel'`。

## Steps

- [x] API：kind／section、主題種子、`section` 篩選、跨區主題 422、已發布換區 409、migration 0073、placement `life`、後台側欄登錄。
- [x] Web：`/life` 兩頁、共用文章頁模組、crosslinks、合作方規則集中到 `guide-affiliate.ts`、導覽四處、後台編輯器、sitemap、e2e fixture。
- [x] 文案五語系、docs 四份、任務板。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app
uv run pytest tests/test_guides.py tests/test_guides_migration.py tests/test_travel_services.py tests/test_admin_operations.py tests/test_schema.py tests/test_error_localization.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web && npm run test:tools && npm run check:tasks
```

手動：三種導覽模式、後台建 life 文章並發布、`/zh-TW/life` 無 noindex 而 `?topic=ai` 有、
填 tokyo 且勾了置入面才有合作方面板。部署後查 `GET /api/v1/runtime/ui-text?locale=zh-TW`
是否有 `navigation.guides` 覆寫蓋住新標籤。

## Notes

- 主題管理介面另開 `2026-09-12-guide-topic-admin-crud`；內文 link 區塊缺 `rel=sponsored` 另開
  `2026-09-12-content-link-block-sponsored`。
- `robots-directives.test.ts` 的 `PUBLIC` 不能加 `/life`（它用 regex 掃整檔，篩選檢視的 noindex 會讓它失敗）。
- 「預設關」只擋 destination-offer 的列表與 clickout；飯店／服務 clickout 對任何 placement 都接受（guide／city 也一樣）。

## What shipped

- **One system, three kinds.** `guide_articles.kind` gained `life`; the revision history,
  per-locale publication, audit trail and editor are the same ones `/guides` uses. The
  sections diverge only at the URL, the nav entry, the topic vocabulary and what ends an
  article.
- **`guide_topics.section`** scopes the vocabulary. `_resolve_topics` refuses a topic from
  the other section on create *and* update (422 `guide_topic_section_mismatch`), and
  `update_article` refuses a cross-section kind change once any locale is published (409
  `guide_kind_locked`) — without that second rule a published article's URL could move
  silently, because `topics` defaults to empty and the mismatch check would never fire.
- **`/life` and `/life/{slug}`**, with `/guides/life/...` a 404 so an article has one URL.
  `guideHref`/`guideListHref` are the only URL builders; `guideArticleMetadata` and
  `renderGuideArticle` hold the article screen once for both sections.
- **End of a lifestyle article:** commission-free travel crosslinks always (three newest
  travel articles plus at most six destination links, its own `<section>` with a rule above
  it), then the destination partner panel only when the editor named a destination —
  `placement="life"`, every module, off by default.
- **The unreachable back office** was found here and fixed by PR #437, which landed while
  this branch was being written: `/admin/guides` had no `NAVIGATION_REGISTRY` entry, so the
  sidebar never offered it and `canAccessAdminPath` refused anyone who typed the URL. That
  is why the section had nineteen topics and zero articles. This branch kept #437's version
  and dropped its own.
- **Migration 0073** widens the kind CHECK through `batch_alter_table`, adds
  `guide_topics.section` with a `server_default`, then seeds. Its downgrade never raises:
  it keeps the wider CHECK while `kind='life'` rows exist rather than destroying them.

## Numbers

- API: ruff and mypy clean; 3398 passed. The one failure, `test_warning_codes`, is the
  known Windows path-separator bug in that test's own allowlist
  (`2026-09-12-test-warning-codes-allowlist-misses-its`) in files this change never touched.
- Web: lint, `check:i18n`, `check:tasks`, `test:tools` and typecheck clean; 2509 passed.
  `shared-trip-view.test.tsx` cannot load because `qrcode` is missing from this worktree's
  `node_modules`; the file is untouched and CI installs it.

## Left undone on purpose

- The bottom tab bar gains nothing (four unit tests and two e2e specs pin its counts, and
  `/guides` set that precedent).
- No `site_features` flag: adding a seventh key flips the whole site to `unavailable` until
  the API emits it, and `/guides` carries none either.
- `SitemapEntry` and `sitemap_entries` untouched, so
  `2026-09-11-guide-lastmod-republication` rebases cleanly. Both sections share the one
  1,000-row budget; revisit past ~800.
- No new affiliate partner or module for non-travel products: the registry is eight travel
  platforms and `AffiliateModule` is five travel modules behind a DB CHECK.
- The phone header now carries a sixth 44px control in discovery mode. It needs eyeballing
  at 375px; if it wraps to two rows, drop the icon and rely on the footer.

## The rebase onto #437 and #436

Two overlapping PRs landed mid-flight, so this is worth recording rather than rediscovering.
Nineteen files conflicted and none of the resolutions were mechanical:

- **#437** (`情報攻略文章可隱藏／恢復上架`) rewrote the same admin surface: the panel became a
  list (`admin-guides-list.tsx`) plus an editor addressed by `?article=&lang=`, `is_active`
  left `ArticleUpdate` for dedicated hide/unhide endpoints, `list_articles` became a
  facet-keyed filter dict returning `total`/`pages`/`facets`, and it made the same
  `NAVIGATION_REGISTRY` fix. Their shapes won everywhere they overlapped. The section rules
  were re-applied onto them: the section became its own facet dimension (so a kind count
  browsed inside a section stays inside it), the empty `section`×`kind` intersection returns
  an empty *paginated* response rather than an unfiltered one, and the section filter moved
  from the panel to their list, where the pagination it protects actually lives.
- **#436** added `share` to `BookingPlacement`, so `life` goes after it; both docs tables
  and the `contentPlacementTokens` set (their shape, better than the filter chain) carry
  four content surfaces now.
- **#432** also took migration `0073`, so this one is `0074_lifestyle_guides` and revises
  `0073_catalog_run_enrich_mode`. `test_schema.py` catches the double head, but only through
  an unrelated-looking failure in `test_admin_operations.py`.
- `KINDS` was deleted from `schemas.py` here as unused; #437's facet code uses it, so it is
  back — which is also why `life` appears in the kind facet at zero and three of their
  assertions needed the extra entry.
