---
id: 2026-09-07-add-a-meal-to-a-day
title: 行程裡新增一餐：四個 trip-selections 端點接受 mode: replace_meal|append
status: review
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:10:01Z
created_at: 2026-09-07T00:45:41Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/foods/router.py
  - apps/api/app/foods/schemas.py
  - apps/api/app/foods/selection.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/i18n.py
  - apps/api/app/restaurants/user_router.py
  - apps/api/app/trips/selections.py
  - apps/api/tests/test_trip_selections.py
  - apps/web/components/frontend-plan-action.test.tsx
  - apps/web/components/travel-card-actions.test.tsx
  - apps/web/components/travel-card-actions.tsx
  - apps/web/lib/frontend-navigation.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-TW/common.json
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

- [x] 四個端點都接受 `mode`：`append`（現況，維持預設）與 `replace_meal`。
- [x] `replace_meal` 需要指出是哪一餐（`lunch` 或 `dinner`），把該日對應 `system_role` 的
      系統卡填成這個地點，保留 `system_role` 與它的時間，而不是新增一列。
- [x] 那一餐已經有內容時的行為有明確答案（覆蓋或 409），而且四個端點一致。
- [x] 前端 `travel-card-actions` 在選日期時可以選「當作午餐／晚餐」。
- [x] 五語系文案與測試。

## Steps

- [x] 四個端點共用一個 helper，不要各寫一份。
- [x] 前端選單。

## How to verify

```bash
cd apps/api && uv run pytest tests/ -k "trip_selection or hotspot_selection or add_a_meal or meal" -q
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
cd apps/web && npx vitest run components/travel-card-actions.test.tsx components/frontend-plan-action.test.tsx
npm run check:i18n && npm run typecheck:web && npm run lint:web
```

## Notes

- 相關程式碼：`apps/api/app/hotspots/router.py:321`（四個裡面最完整的一個，其他三個是同一個
  形狀）。`system_role in {"lunch", "dinner"}` 的判斷在 `apps/api/app/trips/router.py:3292`
  附近已經有，填餐的規則要和那裡一致。

### 2026-09-19 done in repo (claude-fable-5-1)

- 票開出來時的前提已經過時：只有 `/hotspots` 還是 `max(position)+1` 接在最後；
  `/restaurants` 與兩個 `/foods` 端點早已改成必填 `meal_role`、直接寫進餐食卡，而且沒有
  append 可選。這次把四個端點都接到同一個 helper，行為才真的一致。
- Helper 在 `apps/api/app/trips/selections.py`：`TripSelectionRequest`（四個 request model 的
  基底：`mode`、`meal`、`overwrite`，以及舊欄位 `meal_role`）、`SelectionPlace`（各 router 描述
  自己那種地點的資料結構）與 `place_trip_selection()`（找旅程、檢查日期、append 或填餐卡、
  analytics、`persist_system_schedule_change`）。`apps/api/app/foods/selection.py` 只剩
  merchant → `SelectionPlace` 的轉接；`MerchantTripSelectionRequest` 搬到 `foods/router.py`
  和 `FoodTripSelectionRequest` 放一起。
- 合約：`mode` 預設 `append`（hotspot 的 body 完全不變）；`replace_meal` 必須帶 `meal`
  （`lunch`｜`dinner`），少了就 422；`meal` 沒有搭 `replace_meal` 也 422（不然又會默默接成活動，
  正是這張票要關掉的 bug）。舊客戶端只送 `meal_role` 仍等同 `replace_meal` + 該餐，所以
  `hotspot-restaurants-panel` 與 `test_trip_localization_integration` 不用改就繼續成立；
  `meal_role` 與 `mode: append` 或不同的 `meal` 同時出現 → 422。
- 填餐卡的規則和 `trips/router.py` `update_itinerary` 對 lunch/dinner 系統卡的規則一致：只換
  「地點」欄位（title、location_name、names_json、座標與來源、provider_place_id、location_source、
  is_estimated、data），保留 `system_role`、position、start/end time、duration、fixed_time、locked
  與 notes，不新增列；`data` 以 `SELECTION_DATA_KEYS`（`replan.MEAL_LOCATION_DATA_KEYS` 加上四個
  來源各自寫的 id／連結鍵）清掉上一個地點的識別，再寫 `meal_selection_source: "user"`、
  `needs_place_confirmation: False`。
- 已佔用的決定：**409 `meal_slot_occupied`，除非 request 帶 `overwrite: true`**，四個端點相同。
  「已佔用」= `data.meal_selection_source == "user"`（旅客自己選過的餐），和 `replan` 只保留
  user 餐、`reschedule._protected_kind` 只把 user 餐算 `chosen_meal` 同一條線；placeholder
  （`unset`）與 AI 建議（`ai`）直接填入，不問。五語系文案在 `app/i18n.py`
  `_TRIP_SELECTION_ERRORS`。
- Web：`travel-card-actions.tsx` 兩個對話框（新的 `TravelPlanAction` 與 legacy sheet）都改成
  「加入方式」選單：接在這天最後／當作午餐／當作晚餐（hotspot 預設 append，料理與店家維持
  預設午餐）；送 `mode: "replace_meal", meal` 而不是 `meal_role`；append 的 body 不變。收到
  `meal_slot_occupied` 時顯示可讀訊息並多一顆「換成這個」按鈕，第二次才帶 `overwrite: true`，
  和版本衝突的 409（鎖住、要重新載入）分開處理。文案：`lib/frontend-navigation.ts`
  `frontendCopy` 與五份 `messages/*/common.json` 的 `cardActions.placement*`、`mealOccupied`、
  `overwrite`；舊的 `cardActions.meal/lunch/dinner` 沒有人用了，但依「只插入不刪改」的規則留著，
  下次有人動 common.json 再一起清。
- 範圍外的後續：`hotspot-restaurants-panel` 只送 `meal_role`，遇到 409 會顯示 API 的本地化
  detail 但沒有覆蓋按鈕 → 開了 `2026-09-19-hotspot-restaurants-panel-offers-the-overwrite`。
- 驗證（全綠）：
  - `cd apps/api && uv run pytest tests/ -k "trip_selection or hotspot_selection or add_a_meal or meal" -q`
    （含新的 `tests/test_trip_selections.py`：四個端點 × append／replace_meal lunch／dinner、
    缺 `meal` 422、舊 `meal_role`、已佔用 409 與 overwrite、AI 建議直接覆蓋、日期與版本錯誤、404、
    五語系文案）
  - `cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests`
  - `cd apps/web && npx vitest run components/travel-card-actions.test.tsx components/frontend-plan-action.test.tsx`
    與整套 `npm run test:web`（290 檔／3197 測試）
  - `npm run check:i18n && npm run typecheck:web && npm run lint:web`
