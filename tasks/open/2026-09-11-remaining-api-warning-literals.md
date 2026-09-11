---
id: 2026-09-11-remaining-api-warning-literals
title: 後端仍有二十餘處警告字串是寫死的繁中
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-11T17:16:49Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/reschedule.py
  - apps/api/app/trips/share_router.py
  - apps/api/app/trips/schedule.py
  - apps/api/app/search/orchestrator.py
  - apps/api/app/crawlers/back_to_back.py
  - apps/api/app/providers/live_back_to_back.py
---

# 後端仍有二十餘處警告字串是寫死的繁中

## Why

`2026-09-11-api-warnings-leak-zh-tw` 把它列出的四個檔（`trips/routing.py`、`trips/router.py` 的天氣、`search/orchestrator.py`、`search/tasks.py`）改成代碼了，另外順手處理了同一個渲染點會吃到的 `trips/route_planner.py`、`trips/route_tasks.py`、`weather/google.py`、`weather/met_norway.py`。

做的時候掃了整個 `apps/api/app`，發現這個問題比那張任務描述的大得多。以下還是寫死的繁中，各自落在別的渲染點：

| 位置 | 內容 |
| --- | --- |
| `trips/router.py:2398,3310,3474,4272,4486,4642,5335` | 「背景路線服務暫時無法使用…」「行程已變更…」「地點已更新…」 |
| `trips/router.py:3532,3562,3748` | `warning=` 參數：「主要飯店已更新…」「每日時間已更新…」「餐食狀態已更新…」 |
| `trips/router.py:5141,5498` | 手動移動時間說明；`5498` 帶日期參數 |
| `trips/reschedule.py:496` | 「旅程日期已變更，移動時間需要重新計算。」 |
| `trips/share_router.py:150` | 「這是從分享連結存下的行程…」 |
| `trips/stay_router.py:86` `trips/schedule.py:101` | `LODGING_WARNING`、`USER_LODGING_KEPT_WARNING` |
| `trips/route_tasks.py:256,258` | 帶數量參數的兩則 |
| `search/orchestrator.py:440` | 帶 `{module}` 與 `{provider_name}` 兩個參數 |
| `crawlers/back_to_back.py:810,812` `providers/live_back_to_back.py:274` | 帶幣別／角色參數 |
| `hotspots/router.py:422` `restaurants/user_router.py:231` `foods/selection.py:111` | 「…已更新，請重新計算這一天的路線。」 |

其中不少帶參數，所以這張要先決定帶參數警告的表示法——原任務的 Steps 寫的是 `{code, params}`，但那會動到 schema 與 `warnings_json` 的既有資料。

## Definition of done

- [ ] 上表所有位置都不再 append 繁中整句。
- [ ] 帶參數的警告有一個明確、有型別的表示法，且舊資料（已存進 `warnings_json` 的整句）不會炸掉。
- [ ] 每個渲染點都用 `apps/web/lib/warnings.ts` 的 `translateWarnings`。

## Steps

- [ ] 先決定帶參數的表示法。`translateWarnings` 目前的規則是：像代碼的（`^[a-z][a-z0-9_]*$`）查表、查不到就不顯示；不像代碼的原樣顯示。所以舊資料會原樣顯示，不會消失——這給了漸進遷移的空間。
- [ ] 一個檔一個檔改，每改一個就把對應的前端斷言換成代碼。
- [ ] 五語系 catalog 補齊。

## How to verify

```bash
cd apps/api && uv run pytest -q
cd apps/web && npm run check:i18n && npm run test:web
```

## Notes

- 已完成的部分可以照抄：`apps/web/lib/warnings.ts`、`messages/*/trips.json` 的 `route.warning` 與 `weather.warning`、`messages/*/search.json` 的 `results.warning`。
- `search/orchestrator.py:440` 特別值得優先處理：它落在搜尋結果頁的警告區，是使用者最常看到的那一個。
