---
id: 2026-09-06-hotspot-themes-web
title: 熱門景點頁的主題篩選與季節徽章
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T15:12:19Z
created_at: 2026-09-06T15:12:18Z
completed_at: 2026-09-06T16:49:46Z
branch: claude/hotspot-themes-web
depends_on: []
scope:
  - apps/web/lib/hotspot-themes.ts
  - apps/web/lib/hotspot-themes.test.ts
  - apps/web/components/hotspot-theme-chips.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/hotspot-explorer.test.tsx
  - apps/web/messages/en/hotspots.json
  - apps/web/messages/ja/hotspots.json
  - apps/web/messages/ko/hotspots.json
  - apps/web/messages/zh-TW/hotspots.json
  - apps/web/messages/zh-CN/hotspots.json
---

# 熱門景點頁的主題篩選與季節徽章

## Why

API 端（`2026-09-06-hotspot-themes-api`）為景點加了第二層分類：季節主題（賞櫻、賞楓、滑雪、花火、燈飾、賞雪，各帶適用月份）與購物店家類型（藥妝、電器、百貨、Outlet…）。熱門景點頁還看不到它們——讀者無法問「四月的東京有什麼櫻花景點」，也看不出手上這個景點什麼時候值得去。

## Definition of done

- [x] 篩選表單下方有主題 chip 列，分「季節限定」「購物類型」兩排，單選；點下去立刻重新查詢並把 `theme=` 寫進網址。
- [x] 當月適用的季節主題標示「當季」。
- [x] 沒有任何景點的主題不顯示，除非它正是目前選取的那個。
- [x] 景點卡片顯示主題徽章，季節主題附月份區間（`3月–4月`／`Mar–Apr`，跨年的 `11月–1月` 合併成一段）。
- [x] 主題篩不到東西時，空狀態換一句話告訴讀者可以換主題或清條件。
- [x] API 還沒送 `themes` 時（舊 payload、e2e stub）整列不出現，頁面照舊。

## Steps

- [x] `lib/hotspot-themes.ts`：型別、`normalizeMonths`、`monthRuns`（12→1 併段）、`monthRangeLabel`（用 `Intl.DateTimeFormat`，不進語言檔）、`isInSeason`。
- [x] `components/hotspot-theme-chips.tsx`：`HotspotThemeChips`（分組單選）與 `HotspotThemeBadges`（卡片徽章）。
- [x] `hotspot-explorer.tsx`：型別、`theme` state、URL 同步與初始讀取、清除條件、手機篩選計數、chip 列、卡片徽章、空狀態。順手把重複的 `categoryCodes` 換成 `HOTSPOT_CATEGORY_CODES`。
- [x] 五個 `messages/*/hotspots.json` 各加 6 個鍵。
- [x] 測試：`lib/hotspot-themes.test.ts`（月份格式化，含跨年與五語）、`hotspot-explorer.test.tsx` 三個新案例。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
git add -A && CI=1 node tools/check-i18n.mjs
cd apps/web && npx vitest run lib/hotspot-themes.test.ts components/hotspot-explorer.test.tsx
```

瀏覽器：`/zh-TW/hotspots` 應出現兩排主題 chip，當月季節帶「當季」標記，點「賞櫻」後網址出現 `theme=sakura`、卡片徽章顯示「賞櫻 · 3月–4月」；切到 `/en/hotspots` 標籤與月份都變英文（標籤來自 API，月份來自 `Intl`）。

## Notes

- 主題名稱由 API 依 `X-Travel-Locale` 回傳（和 `area.name` 一樣），**不進語言檔**；只有「全部主題」「主題篩選」「季節限定」「購物類型」「當季」「景點主題」「主題空狀態」這幾句是本地字串。
- 月份用 `Intl.DateTimeFormat(locale, {month:"short", timeZone:"UTC"})` 產生，所以之後新增主題不必動語言檔。實測輸出：zh-TW／zh-CN／ja `3月–4月`、ko `3월–4월`、en `Mar–Apr`。
- chip 點擊會把 `theme` 以參數傳進 `load()`／`syncUrl()`，不等 React state 提交；否則第一次點擊會送出舊值。
- `themes` 在 `RankedHotspot` 與 `FacetsResponse` 都是選填：既有測試 fixture 與 `e2e/hotspot-guides.spec.ts` 的 stub 都沒有這個欄位，仍需照常運作。
- 測試檔新增了 `afterEach` 清網址：原本第一個案例會把 `?destination_id=tokyo&area=akihabara` 留給下一個案例，新的「分享連結」案例會被它污染。
- 沒有寫成 `depends_on: 2026-09-06-hotspot-themes-api`：那張任務還在另一個分支上，寫了會讓這條分支的 `check:tasks` 紅掉。實際順序是 API 先上；但因為 `themes` 是選填，這個 PR 先合也只是主題列不出現而已。
