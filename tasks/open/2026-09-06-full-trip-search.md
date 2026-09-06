---
id: 2026-09-06-full-trip-search
title: 彈性日期區塊的價格標籤寫死 full_trip_search
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T20:32:08Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/flight-date-options.tsx
  - apps/web/components/flight-date-options.test.tsx
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

- [ ] 彈性日期區塊顯示的價格，和按下去之後伺服器真正保留的次數是同一個數字。
- [ ] 站內沒有第二處把搜尋操作名稱寫死在畫面上。

## Steps

- [ ] 由呼叫端把操作名稱（或算好的 charge）傳進 `FlightDateOptions`，來源是
      `searchUsageOptions`／`searchUsageOperation`，不要在元件裡再猜一次。
- [ ] `grep -rn 'useOperationCharge("' apps/web` 看還有沒有其他寫死的搜尋操作。
- [ ] 補一個測試：彈性日期的重新搜尋在 modules 只有 flight 時標的是
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
