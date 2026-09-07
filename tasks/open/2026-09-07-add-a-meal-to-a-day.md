---
id: 2026-09-07-add-a-meal-to-a-day
title: 行程裡新增一餐：四個 trip-selections 端點接受 mode: replace_meal|append
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-07T00:45:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/router.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/restaurants/user_router.py
  - apps/web/components/travel-card-actions.tsx
---

# 行程裡新增一餐：四個 trip-selections 端點接受 mode: replace_meal|append

## Why

`docs/user-flow-plan.md` 的 PR F 原本包含這一項，實作時抽出來獨立處理，因為它動的是另外
四個 router，和提醒／航班動態那一包沒有共用的檔案。

四個「加入行程」端點——`POST /hotspots/{id}/trip-selections`、
`POST /restaurants/{place_id}/trip-selections`、`POST /foods/{id}/trip-selections`、
`POST /foods/merchants/{id}/trip-selections`——都是同一個做法：算出那一天最大的 `position`，
然後 `+1` 接在最後面。所以選了一家午餐餐廳，行程上會多出一個排在晚上的活動，而那天原本
空著的「午餐」系統卡還是空的。使用者要自己再把它拖上去，或是接受一天有兩個午餐。

## Definition of done

- [ ] 四個端點都接受 `mode`：`append`（現況，維持預設）與 `replace_meal`。
- [ ] `replace_meal` 需要指出是哪一餐（`lunch` 或 `dinner`），把該日對應 `system_role` 的
      系統卡填成這個地點，保留 `system_role` 與它的時間，而不是新增一列。
- [ ] 那一餐已經有內容時的行為有明確答案（覆蓋或 409），而且四個端點一致。
- [ ] 前端 `travel-card-actions` 在選日期時可以選「當作午餐／晚餐」。
- [ ] 五語系文案與測試。

## Steps

- [ ] 四個端點共用一個 helper，不要各寫一份。
- [ ] 前端選單。

## How to verify

```bash
cd apps/api && uv run pytest tests/ -k "trip_selection or hotspot_selection"
npm run test:web
```

## Notes

- 相關程式碼：`apps/api/app/hotspots/router.py:321`（四個裡面最完整的一個，其他三個是同一個
  形狀）。`system_role in {"lunch", "dinner"}` 的判斷在 `apps/api/app/trips/router.py:3292`
  附近已經有，填餐的規則要和那裡一致。
