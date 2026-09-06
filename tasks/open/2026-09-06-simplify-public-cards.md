---
id: 2026-09-06-simplify-public-cards
title: 公開頁精簡：景點卡動作分層、首頁膠囊溢出、排行榜第一屏
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T16:34:13Z
created_at: 2026-09-06T13:02:09Z
completed_at:
branch: claude/ux-simplify-public-2
depends_on: []
scope:
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/hotspot-explorer.test.tsx
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/hotspots/page.tsx
  - apps/web/lib/hotspots.server.ts
  - apps/web/messages/en/hotspots.json
  - apps/web/messages/ja/hotspots.json
  - apps/web/messages/ko/hotspots.json
  - apps/web/messages/zh-CN/hotspots.json
  - apps/web/messages/zh-TW/hotspots.json
---

# 公開頁精簡：景點卡動作分層、首頁膠囊溢出、排行榜第一屏

## Why

2026-09-06 的全站稽核裡，公開頁還有三件「看得見但不夠簡單」的事，都不是改個顏色
就能解決，要動版面，所以跟可讀性那批分開：

1. **一張景點卡有六個可以按的東西**：景點詳情、附近用餐、收藏、加入行程、分享、
   查看來源。沒登入的時候前兩個都是鎖頭，副標都是「登入後…」——同一件事講兩次，
   佔掉卡片一半高度。手機一屏看不完一張卡。
2. **首頁的信任膠囊在手機上被切掉**：「每筆資料標明來源／自動安排每日動線／即時與
   估算費用分開」是一條橫向捲動的膠囊列，390px 下第三顆只露出一半，也沒有任何
   可以繼續捲的提示。
3. **排行榜第一屏是空的**：`/hotspots` 的排行是進頁後才用瀏覽器去打
   `/hotspots/rankings`，量到 2–4 秒之間畫面上只有「正在整理最新排行…」與
   「已載入 0／0 個結果」。資料本身在伺服器端拿得到（`facets` 與 `rankings` 都是
   公開 GET），第一頁可以直接 server render。

## Definition of done

- [ ] 未登入時，一張景點卡上的鎖頭入口只有一個，講清楚登入之後會拿到什麼。
- [ ] 收藏／加入行程／分享維持一排，不再與兩顆大按鈕搶注意力。
- [ ] 首頁膠囊列在 320px 與 390px 下不會出現半顆被切掉的膠囊。
- [ ] `/hotspots` 第一屏直接帶著前 30 筆排行進來，不再出現「0／0」。

## Steps

- [ ] `hotspot-explorer.tsx`：未登入時把「景點詳情」與「附近用餐」合併成一顆
      入口，登入後維持兩顆。
- [ ] `search-workbench.tsx`：信任膠囊改成手機換行（或明確的捲動提示）。
- [ ] `app/[locale]/hotspots/page.tsx`：server 端先取第一頁排行與 facets，傳給
      `HotspotExplorer` 當初始值，之後的篩選仍走客戶端。

## How to verify

`/hotspots` 用 Playwright 停用 JavaScript 或看 `domcontentloaded` 當下的 HTML，
應該已經有 30 張卡；`travel-card-actions` 的三顆按鈕與合併後的入口在 320px 下
仍然是 44px 以上。

## Notes

- 排行 API 已經是公開 GET（`/api/travel/hotspots/rankings?limit=30`），server
  render 不需要新的認證路徑；注意 BFF 會把語系放在 `X-Travel-Locale` 標頭。
- 「熱門分數 / 30 天瀏覽 / 相較前期」這三個數字是刻意留著的產品定位（排行榜），
  這張任務不動它們。
