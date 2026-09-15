---
id: 2026-09-14-sitemap-split-before-1000-rows
title: sitemap 拆成 sitemap index：已經 1,395 列，上限 1,000 已破
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-14T23:07:00Z
completed_at:
branch:
depends_on:
  - 2026-09-14-claude-code-tutorial-center
  - 2026-09-14-pack-ingest-urlopen-scheme
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guides.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
  - docs/seo.md
  - docs/travel-guides.md
---

# sitemap 拆成 sitemap index：已經 1,395 列，上限 1,000 已破

## Why

`guides-pack lint` 現在算到 986 個 (article, locale) 列（#513 之後，含 #515 財經系列的 40 篇與 #516 批次 08 的 20 篇），早就過了 `SITEMAP_WARN_ROWS = 800`
（`apps/api/app/guides/pack_ingest.py`）的警戒線；兩個專區共用一個 1,000 列的 sitemap（`SITEMAP_LIMIT`
在 `apps/api/app/guides/service.py`、`SITEMAP_GUIDE_ENTRY_LIMIT` 在 `apps/web/lib/guides.server.ts`），新的先進、
舊的被擠出，被擠出的文章仍可索引但不再被 sitemap 宣告、也沒有 `lastmod`。生活分享 AI 系列批次 09–11 還有 60 篇、批次 12 有 11 篇、
財經系列（`docs/life-finance-series.md`）還有 80 篇要進來：986 列再加任何一批 20 篇就超過 1,000，全部進來會到 1,137。

`GET /guides/sitemap`（`apps/api/app/guides/router.py`）沒有分頁參數，所以不能只在 web 端拆；`docs/seo.md`
寫的「No sitemap index is needed」與 `docs/travel-guides.md` 的「Still open」都要一起改。


## 2026-09-15 複測：966 列，headroom 只剩 34

財經系列批次 03 開工前實測 `origin/main` 上的內容包：**778 個包、966 個 (article, locale) 列**
（zh-TW 758、en／ja／ko／zh-CN 各 52）。比這張票寫的 926 又多了 40 列，因為這中間又合併了幾批。

- 距離 `SITEMAP_LIMIT = 1000` 只剩 **34 列**。
- 財經批次 03（20 篇，只有 zh-TW）落地後是 **986**，剩 14 列。
- 財經批次 04–06 還有 **60 篇**，AI 系列批次 08–12 還有 **91 篇**——兩邊加起來 151 篇，
  **不管哪一邊先動都會爆掉**。

站主已知悉並決定先寫批次 03。**批次 04 開工前這張票必須先解決。**

### 2026-09-15 批次 03 落地並併入當天 main：**1,395 列，上限已經破了**

先講分支自己的數字：財經批次 03 的二十篇落地後，`pack_cli lint` 回報 **986 列**，
與上面的推算一致，headroom 14。

**但把當天的 `origin/main` 併進來之後是 1,395 列。**
內容包 963 個（850 個單語系、93 個**五語系**、20 個四語系；kind 分佈 life 838、howto 106、intel 19）。
對照上面複測時的 778 個包、32 個五語系——**推過 1,000 的不是財經系列，是五語系包從 32 變成 93**，
一個五語系包就是五列。

所以這張票的性質變了：**不再是「還剩幾列」，而是已經有大約 395 個已發布的
(article, locale) 進不了 sitemap**（`service.py` 的查詢是 `.limit(SITEMAP_LIMIT)`，
`order_by(published_at.desc())`，所以被砍掉的是**最舊的那些**）。
搜尋引擎抓不到那幾百頁，而且不會有任何錯誤訊息。

**這張票的優先順序應該往上調，不只是「批次 04 開工前要做」。**

這張票目前認領不了：`depends_on` 的 `2026-09-14-claude-code-tutorial-center` 與
`2026-09-14-pack-ingest-urlopen-scheme` 都還是 `status: review`，而且兩張都佔著
`apps/api/app/guides/pack_ingest.py` 的 scope。要動這張票得先讓那兩張合併或認領過期。

## Definition of done

- [ ] `/sitemap.xml` 變成 sitemap index，靜態路由一個子 sitemap、文章依專區或依語系分成多個子 sitemap，每個子檔不超過 1,000 列，沒有文章被擠掉。
- [ ] API 提供可分頁或依專區／語系篩選的 sitemap 讀法，web 端逐頁讀完；API 失敗時退回靜態子 sitemap，不出空檔。
- [ ] `robots.ts` 指向 sitemap index；`e2e/seo.spec.ts` 與 `apps/web/app/sitemap.test.ts` 更新；`pack_ingest.py` 的 `SITEMAP_WARN_ROWS` 警語改成對子 sitemap 的上限說話。
- [ ] `docs/seo.md`、`docs/travel-guides.md` 改寫預算段落。

## Steps

- [ ] 決定切法（建議依專區：`guides`、`life`，再依語系）並寫進 `docs/seo.md`。
- [ ] API：`SitemapEntry` 讀法加 `section`／`locale`／`cursor` 參數，保留舊呼叫相容。
- [ ] Web：`sitemap.ts` 用 Next 的 `generateSitemaps` 或自訂 index route 產出多檔。
- [ ] 測試與文件。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
cd apps/api && uv run pytest tests/test_guides.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
```

部署後抓 `/sitemap.xml` 與每個子 sitemap，確認總列數等於已發布的 (article, locale) 數。

## Notes

- 2026-09-15 提到 P1：#515 財經系列一次加了 40 列、#516 批次 08 再加 20 列，986 已經離上限 14 列，任何一批 20 篇落地就會開始把最舊的文章擠出 sitemap。

- `guides.server.ts` 與 `pack_ingest.py` 目前被 review 中的 `2026-09-14-claude-code-tutorial-center`、`2026-09-14-pack-ingest-urlopen-scheme` 持有，所以先 depends_on 那兩張。
- `2026-09-14-guide-listing-curated-order` 也會改 `service.py`；先合併的那張，後面那張要 rebase。
- 來源：`docs/travel-guides.md`「Both sections share one 1,000-row sitemap budget」；Google 單一 sitemap 上限 50,000 列，這裡的 1,000 是自訂預算。
