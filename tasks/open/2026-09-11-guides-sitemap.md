---
id: 2026-09-11-guides-sitemap
title: Guide articles and section pages in the sitemap
status: in-progress
priority: P1
area: web
owner: claude-opus-5-guides-sitemap
claimed_at: 2026-09-11T16:00:26Z
created_at: 2026-09-11T15:43:20Z
completed_at:
branch: claude/distracted-lumiere-260705
depends_on: []
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/e2e/seo.spec.ts
  - tools/e2e-runtime-api.mjs
  - docs/seo.md
---

# Guide articles and section pages in the sitemap

## Why

旅遊情報與攻略專區（`/guides`）隨 PR #398 上線，但當時 `apps/web/app/sitemap.ts` 被
`2026-09-10-seo-robots-sitemap` 與 `2026-09-11-pr388-seo-review` 鎖住，所以沒有列進 sitemap，
搜尋引擎只能靠內部連結慢慢發現這些文章。

API 端已經準備好：`GET /api/v1/guides/sitemap` 回傳 `{"entries": [{kind, slug, locale, published_at}]}`，
每篇已發布、未過期文章的每個已發布語系一筆，新到舊，上限 1,000 筆。它和列表頁、文章頁共用
`apps/api/app/guides/publication.py` 的發布判斷，所以不會列出網站不提供的網址。這張票是網頁端的一半。

## Definition of done

- [x] `/guides`、`/guides/intel`、`/guides/howto` 以五個語系出現在 sitemap，不掛功能開關。
- [x] 每篇文章的每個已發布語系各一筆，未發布的語系沒有；`alternates.languages` 只列該文章已發布的
      語系，英文已發布時才有 `x-default`，與文章頁 `<head>` 宣告的集合相同。
- [x] 文章條目帶 `lastmod`（取自 API 的 `published_at`），靜態路由仍然沒有，兩者分開測試。
- [x] 攻略 API 連線失敗或回 HTTP 500 時，sitemap 與只有靜態路由時完全相同，不會變空也不會 500。
- [x] 文章條目有上限，`docs/seo.md` 的數量估算與實際一致。
- [x] `npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web && npm run build:web`
      在本機通過。
- [ ] PR 的 `api`、`web`、`containers`、`full-stack-smoke` 全綠（推送時 CI 還沒跑完，由分支保護在合併時把關）。

## Steps

- [x] `lib/guides.server.ts`：`guideSitemapEntries()`。`no-store`、`AbortSignal.timeout(3000)`、任何失敗回 `[]`，
      逐筆驗證 kind／slug／locale／日期，截在 `GUIDE_SITEMAP_LIMIT`。
- [x] `app/sitemap.ts`：三條靜態路由；與可見度讀取並行；文章條目一律排在靜態條目之後。
- [x] `app/sitemap.test.ts`：`describe("guide articles")`；「沒有 lastmod」的斷言縮到靜態路由並說明原因。
- [x] `lib/guides.server.test.ts`：loader 的請求紀律與契約檢查。
- [x] `tools/e2e-runtime-api.mjs` 加合成的攻略 sitemap 資料；`e2e/seo.spec.ts` 更新網址數並檢查實際輸出的 XML。
- [x] `docs/seo.md`：新的數量、lastmod 的分流、站務文件仍在 sitemap 之外。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web && npm run build:web
npm run test:tools && npm run check:tasks
# 本機沒有 Docker／Postgres：用 production build 對 e2e 的 mock API 驗證網頁端
node tools/e2e-runtime-api.mjs &
API_INTERNAL_URL=http://127.0.0.1:8000 npm run start --workspace @travel-scanner/web -- --port 3000 &
curl -s localhost:3000/sitemap.xml | grep guides
cd apps/web && PLAYWRIGHT_REUSE_EXISTING=true PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/seo.spec.ts
```

「只列已發布、未過期的文章」這一半由 API 的整合測試負責（`apps/api/tests/test_guides.py` 的撤下、過期、
封存三種情況都斷言 `/guides/sitemap` 變空），在 CI 的 `api` job 以 PostgreSQL 執行。

## Notes

- **範圍鎖的處理。** 認領時工具指出四個 review 中的任務占著這張票的範圍：
  `2026-09-10-seo-robots-sitemap`、`2026-09-10-seo-audit-followups`、`2026-09-11-pr388-seo-review`
  （都隨 PR #388 合併，2026-09-11T01:27:36Z）與 `2026-09-11-travel-guides-web`（PR #398）。
  原本經使用者同意在本 PR 代為結案，但另一個 session 的 PR #400 同時在收同一批（連同另外 18 張，
  證據更完整）。為了不讓兩個 PR 在 `tasks/done/` 上衝突，改由 #400 結案，本 PR 撤回。
  #400 合併前，本分支的 `check:tasks` 會有這四張與本任務範圍重疊的警告，不影響 CI。
- **與 `2026-09-11-guides-sitemap-and-entry-points` 重疊。** 那張由 PR #400 開立，把 sitemap、頁尾連結、
  目的地頁連結與 discovery 的「攻略」改名綁在一起；其中 sitemap 就是本任務。#400 合併後，更新本分支時
  把那張的 sitemap 項目勾掉並從 scope 拿掉 `app/sitemap.ts`、`app/sitemap.test.ts`，只留另外三項。
- **刻意的例外：文章條目帶 `lastmod`。** 靜態路由不帶的理由是「sitemap 不知道內容何時變動」，
  這對城市指南成立，對文章不成立：API 回傳的是真實的發布日。`sitemap.test.ts` 原本「完全沒有
  lastmod」的斷言縮到靜態路由，並且在有文章的情況下執行，讓這個分流是測出來的，而不是假設的。
- **`published_at` 是首次發布日。** `admin_service.py:208-210` 重新發布時保留原值
  （`test_guides.py:289-290` 也這樣斷言），所以修訂過的文章 `lastmod` 不會前進。
  後續另開 `2026-09-11-guide-lastmod-republication`。
- **`docs/seo.md` 的「Managed document URLs remain outside the sitemap」講的是頁尾四份站務文件**
  （`/about`、`/privacy`、`/terms`、`/contact`），不是攻略。這次之後它仍然成立，所以改寫成兩種情況
  分開講，而不是刪掉。
- **slug 在網頁端也驗格式。** Next 的 sitemap 序列化不跳脫 `<loc>` 與 hreflang 的 `href`
  （`next/dist/build/webpack/loaders/metadata/resolve-route-data.js`），一筆含 `&` 或 `<` 的 slug
  會讓整份 XML 失效、所有網址一起被拒。API 寫入時已強制 `^[a-z0-9]+(?:-[a-z0-9]+)*$`，網頁端照同一個
  規則丟掉不合的列。
- **`e2e/seo.spec.ts` 寫死 365 筆。** 三條新路由之後是 380，加上 mock 裡三筆合成文章是 383。

## 驗證紀錄

2026-09-12，本機（Windows）：

- `npm run lint:web`、`check:i18n`（5 語系、25 個 namespace）、`typecheck:web`、`test:tools`（27）、
  `check:tasks` 通過。`npm run test:web` 全套 225 個檔案、2,239 個測試通過；其中
  `app/sitemap.test.ts` 與 `lib/guides.server.test.ts` 共 113 個。
- `npm run build:web` 通過，`/sitemap.xml` 仍是 `ƒ`（動態）。
- 本機沒有 Docker 與 Postgres，所以用 production build 接 `tools/e2e-runtime-api.mjs` 驗證網頁端。
  `curl -s localhost:3000/sitemap.xml` 可被 XML 解析器正常解析：383 筆 `<url>`、3 筆 `<lastmod>`，
  文章條目是第 381–383 筆（全部在靜態條目之後），15 筆攻略區頁面沒有 `lastmod`、各帶 6 條 alternates。

  ```
  /zh-TW/guides/intel/synthetic-fare-notice    lastmod 2026-09-08T09:30:00.000Z  hreflang ja, zh-TW
  /ja/guides/intel/synthetic-fare-notice       lastmod 2026-09-07T01:00:00.000Z  hreflang ja, zh-TW
  /en/guides/howto/synthetic-airport-transfer  lastmod 2026-09-01T00:00:00.000Z  hreflang en, x-default
  ```

- 同一組伺服器上 `e2e/seo.spec.ts` 桌面與 Pixel 7 共 32 個測試通過。
