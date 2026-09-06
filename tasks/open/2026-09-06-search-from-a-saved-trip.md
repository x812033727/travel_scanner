---
id: 2026-09-06-search-from-a-saved-trip
title: 從旅程出發查機票：條件由旅程推導，報價帶回錨點
status: review
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T20:39:30Z
created_at: 2026-09-06T20:38:58Z
completed_at:
branch: claude/better-workflow-planning-324ki8
depends_on: []
scope:
  - apps/api/app/i18n.py
  - apps/api/app/search/router.py
  - apps/api/app/search/schemas.py
  - apps/api/app/trips/flight_anchor.py
  - apps/api/app/trips/itinerary.py
  - apps/api/app/trips/router.py
  - apps/api/app/trips/search_criteria.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/api/tests/test_search_from_trip.py
  - apps/web/components/flight-anchor-card.test.tsx
  - apps/web/components/flight-anchor-card.tsx
  - apps/web/components/flight-offer-card.test.tsx
  - apps/web/components/flight-offer-card.tsx
  - apps/web/components/search-experience.test.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/e2e/full-stack.spec.ts
  - apps/web/lib/trip-types.ts
  - apps/web/messages/en/search.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/search.json
  - apps/web/messages/zh-TW/trips.json
  - docs/user-flow-plan.md
---
# 從旅程出發查機票：條件由旅程推導，報價帶回錨點

## Why

`docs/user-flow-plan.md` 的 PR D。`/search` 原本是一扇沒有入口的門：旅程頁沒有「查機票」，
`POST /searches` 也從不讀旅程，所以已經存了旅程的人要重新輸入一次條件，查完的報價又回不到
旅程。這張任務是那一段的實作，PR #249。

這張任務是在工作做完、PR 開出來之後才補登的：當初的來源是使用者直接交辦，不是看板。
補登的目的是讓看板看得到這些檔案正在被改，免得別人認領到同一批檔案。

## Definition of done

- [x] `POST /searches` 接受 `trip_id`，條件在建立搜尋當下從旅程推導；客戶端明確給的欄位優先。
- [x] `GET /trips/{id}/search-criteria` 在扣次前攤開條件與缺口，缺口各有自己的代碼。
- [x] `POST /trips/{id}/flight-anchors/{direction}/from-offer` 把報價寫回錨點，保留
      `offer_id` 與價格快照。
- [x] `PATCH /trips/{id}` 接受 `origin_airport`。
- [x] `/search?trip_id=…` 模式：只搜機票、缺出發地在頁內問並存回、機票卡可帶入去回程。
- [x] 旅程頁錨點卡有「查機票 · 消耗 N 次」。
- [x] 五語系文案、單元／整合／e2e 測試。

## Steps

- [x] 後端兩個新模組 `app/trips/search_criteria.py`、`app/trips/flight_anchor.py`。
- [x] 前端旅程模式與帶入按鈕。
- [x] rebase 到當時的 main（前進了 417 個檔案），三處跟著調整：合作平台區塊改用 #221 的、
      目的地目錄改用 #199 的 `localizeDestinations(tc)`、整合測試沿用 #219 的事件迴圈作法。
- [x] 對抗式審查（六個面向、每個發現三個獨立視角試著推翻）的 9 個發現逐一修掉。
- [ ] 合併。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_integration_postgres_redis.py   # 需要 Postgres/Redis
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npx playwright test e2e/full-stack.spec.ts                                       # 需要整套服務
```

## Notes

- **scope 和 `2026-09-06-readable-foundation` 有兩個檔案重疊**：
  `apps/web/components/flight-anchor-card.tsx` 與 `apps/web/components/trip-editor.tsx`。
  認領時被工具擋下來，因為那張任務正在進行中；這張是事後補登、程式碼早就推上去了，
  所以用 `--force` 記錄現況而不是假裝沒有重疊。給那張任務的人：本分支在這兩個檔案裡只加了
  三個東西——錨點卡的 `search?: { href, charge }` 屬性與那個 `<Link>`、旅程頁的
  `flightSearchCharge`、以及傳給錨點卡的 `search={{…}}`。都不碰樣式，先合誰都好處理。
- 審查發現裡值得記住的一個：`reoptimize` 原本只保護 `flight_selection_source == "manual"`
  的錨點，所以新的 `"offer"` 會被靜默覆蓋掉。現在用 `member_chose_flight()` 具名判斷，
  以後再多一種來源就改那一個地方。
- 兩件看到但不在這個範圍裡的事已另開任務：`2026-09-06-full-trip-search`（彈性日期區塊的
  價格標籤寫死）與 `2026-09-06-ask-origin-airport-at-trip-creation`（建立旅程時就問出發地）。
