---
id: 2026-09-06-full-trip-search
title: 彈性日期區塊的價格標籤寫死 full_trip_search
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:14:46Z
created_at: 2026-09-06T20:32:08Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/web/components/flight-date-options.tsx
  - apps/web/components/flight-date-options.test.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/components/search-experience.test.tsx
  - apps/web/components/trip-editor.tsx
---

# 彈性日期區塊的價格標籤寫死 full_trip_search

## Why

`flight-date-options.tsx` 的「重新搜尋」按鈕用 `useOperationCharge("full_trip_search")`
取價格標籤，但實際扣哪一種次數是伺服器從送出的 payload 推導的
（`app/usage/service.py::search_operation`）。兩者只要不一致，畫面就會報一個價、
伺服器保留另一個價；管理者把不同操作調成不同次數之後，使用者會看到說一次卻扣兩次，
或是被告知還夠用卻拿到 402。

`apps/web/lib/usage-catalog.ts` 已經有 `searchUsageOperation()`，它是伺服器那支函式的
逐行對應，寫來就是給前端算同一個答案用的；這個元件（還有其他寫死操作名稱的地方）沒有用它。

PR #249 已經把 `search-experience.tsx` 的旅程模式改成用 `searchUsageOperation` 推導，
並且在旅程模式不再顯示這個區塊（換一週的結果帶不回旅程錨點）。剩下非旅程模式的這一個。

## Definition of done

- [x] 彈性日期區塊顯示的價格，和按下去之後伺服器真正保留的次數是同一個數字。
- [x] 站內沒有第二處把搜尋操作名稱寫死在畫面上。

## Steps

- [x] 由呼叫端把操作名稱（或算好的 charge）傳進 `FlightDateOptions`，來源是
      `searchUsageOptions`／`searchUsageOperation`，不要在元件裡再猜一次。
- [x] `grep -rn 'useOperationCharge("' apps/web` 看還有沒有其他寫死的搜尋操作。
- [x] 補一個測試：彈性日期的重新搜尋在 modules 只有 flight 時標的是
      `flexible_flight_search`，不是 `full_trip_search`。

## How to verify

```bash
npm run test:web -- components/flight-date-options.test.tsx
npm run typecheck:web && npm run lint:web
```

在後台把 `full_trip_search` 與 `flexible_flight_search` 調成不同次數，然後在
`/search` 跑一次彈性日期搜尋，確認按鈕上的數字和 `/usage` 實際保留的數字一致。

## Notes

- 這是 main 上既有的問題，不是 PR #249 造成的；#249 只是讓它更容易被看到，因為旅程模式
  預設就停在「機票」分頁。
- 對抗式審查在 PR #249 上發現這一點，三個獨立視角都確認標籤與伺服器推導可能不一致；
  預設設定（所有操作都是 1 次）看不出來，要管理者調過價才會顯現。

### 2026-09-19 done in repo (claude-fable-5-1)

改了什麼：

- `flight-date-options.tsx` 多一個必填的 `operation: UsageOperation` prop，元件只拿它去
  `useOperationCharge`，不再自己寫 `full_trip_search`。傳操作名稱而不是算好的 charge，
  是因為文案（消耗 N 次／免費／暫時無法確認）本來就由元件自己組，呼叫端只需要決定
  「伺服器會把這個 payload 算成哪一種操作」。
- `search-experience.tsx`：原本非旅程模式那一支也是寫死 `"full_trip_search"`（跨行，
  `grep 'useOperationCharge("'` 抓不到）。現在有一個 `searchOperation(flexDays)`，用
  `begin()` 真正送出的值（`trip_type`、modules、`optimization_mode`、`flexible_dates`）
  丟進 `searchUsageOperation`；開始搜尋按鈕用 `searchOperation(parsed.flex_days)`，
  彈性日期區塊用 `searchOperation(0)`（套用估價會把 `flex_days` 釘成 0 再跑
  `begin()`）。四個模組抽成 `FULL_TRIP_MODULES`，`begin()` 與定價共用同一個陣列。
  旅程模式的結果和改前完全相同（未釘選 → `travel_search`；釘選且有 flex →
  `flexible_flight_search`）。
- `trip-editor.tsx`：「查機票 · 消耗 N 次」原本寫死 `travel_search`，改成
  `searchUsageOperation({ modules: ["flight"] })`——那個連結開的是 `/search?trip_id=`，
  送的就是旅程加 flight 一個模組，和搜尋頁與伺服器同一條推導。
- grep 結果（每一處都看過）：`airline-fare-lab` `public_airline_fare_search`、
  `back-to-back-fare-search` `back_to_back_fare_search`、`live-back-to-back-search`
  `live_back_to_back_fare_search`、`flight-status-search` 與 `trip-editor`
  `flight_status_lookup`、`itinerary-diff` 與 `trip-editor` 的 `ai_itinerary_*`、
  `itinerary_optimization`、`price_reoptimization`——這些都是端點固定的操作，伺服器不從
  payload 推導，維持原樣。會被 `search_operation` 推導的只有上面兩處，都已改掉。
- 測試：`flight-date-options.test.tsx` 新增「modules 只有 flight 的彈性日期重新搜尋標
  `flexible_flight_search`（目錄定 2 次）而不是 `full_trip_search`（3 次）」；
  `search-experience.test.tsx` 新增一個不變量測試：按下套用之後，把第二次
  `POST /searches` 的 body 丟進 `searchUsageOperation`，按鈕上引用的數字必須等於那個操作
  在目錄裡的價格。今天非旅程 payload 一定算成 `full_trip_search`，所以畫面上的數字沒變，
  變的是它從此跟著 payload 走。
- scope 加了 `search-experience.tsx`、`search-experience.test.tsx`、`trip-editor.tsx`：
  改之前確認過 board 上沒有 in-progress／review 的票持有這三個路徑（列出 trip-editor.tsx
  的幾張都還是 open，不持有 scope）。

驗證（本機）：

```
npx vitest run components/flight-date-options.test.tsx components/search-experience.test.tsx components/trip-editor.test.tsx
 Test Files  3 passed (3)
      Tests  100 passed (100)
npm run typecheck:web   -> tsc --noEmit（exit 0）
npm run lint:web        -> eslint . --max-warnings=0（exit 0）
```

留給 owner 的手動檢查：在後台把 `full_trip_search` 與 `flexible_flight_search` 調成不同
次數，到 `/search` 跑一次彈性日期搜尋、選一個估價日期，確認「套用並重新搜尋整趟 · 消耗 N 次」
的 N 和 `/usage` 實際保留的數字一致；再開一個旅程頁看「查機票 · 消耗 N 次」等於
`travel_search` 的價格。
