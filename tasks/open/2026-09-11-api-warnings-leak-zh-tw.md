---
id: 2026-09-11-api-warnings-leak-zh-tw
title: 後端回傳的繁中警告句被原樣顯示在所有語系
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-11T03:20:36Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/routing.py
  - apps/api/app/trips/router.py
  - apps/api/app/search/orchestrator.py
  - apps/api/app/search/tasks.py
---

# 後端回傳的繁中警告句被原樣顯示在所有語系

## Why

API 本身有一份完整的五語系錯誤 catalog（`apps/api/app/i18n.py`，所有 code 都有翻譯），但 `warnings[]` 陣列是半套的：有些地方 append **代碼**，有些地方直接 append **繁體中文整句**。

做對的（代碼）：`trips/stay_router.py:505` `"children_ages_missing"`、`trips/stay_areas.py:263` `"consider_second_stay"`——前端在 `stay-area-flow.tsx:315,355` 用 `filter(KNOWN_WARNINGS.has)` 後查表翻譯。

漏出去的（繁中整句）：

- `trips/routing.py:586`「步行路線為測試版，請依現場道路與安全狀況調整。」`:773`「偏好條件沒有結果，已改用一般大眾運輸路線。」`:793`「精準地點識別無法建立路線，已用相同地點的座標重試。」
- `trips/router.py:3152,3154,3159` 三則天氣區間警告。
- `search/orchestrator.py:214,242,363,365` 碳排資料／FlightAware／彈性日期定價警告。
- `search/tasks.py:30,42`「搜尋處理發生系統錯誤，已自動退回保留次數。」

渲染點分別是 `route-segment-card.tsx:88`、`trip-weather-panel.tsx:200`、`search-experience.tsx:1423-1430`——全部原樣印出。

諷刺的是 `search-experience.tsx:1123-1126` 有一段長註解，記錄的正是他們為供應商徽章修掉的同一類 bug。

## Definition of done

- [ ] 上列所有 `warnings` 改為 append 代碼。
- [ ] 五語系前端 catalog 有對應翻譯。
- [ ] 未知代碼被安全忽略，不會把原始字串印給使用者。

## Steps

- [ ] 為每則警告定一個代碼，沿用 `"children_ages_missing"` 那種 snake_case 命名。
- [ ] 後端四個檔改為 append 代碼；有參數的警告改回傳 `{code, params}`。
- [ ] 前端三個渲染點改為查表，並照 `stay-area-flow.tsx:315` 的作法先 `filter` 掉不認得的代碼。
- [ ] 五語系 catalog 補齊。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests -k "routing or search" -q
cd apps/web && npm run check:i18n && npm run test:web -- route-segment trip-weather
```

## Notes

- `apps/api/app/places/router.py:513-516` 的 `assumptions` 與 `:541` 的 `next_step` 是同一類問題，但那個檔被 `2026-09-11-wizard-crash-when-all-criteria-any` 佔住 scope，刻意沒納入。兩張任務誰先做完，把剩下那個記到對方 Notes 裡。
- `apps/api/app/usage/service.py:256` 的 402 detail 也是寫死繁中，由 `2026-09-11-usage-exhausted-dead-end` 處理。
