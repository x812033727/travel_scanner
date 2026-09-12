---
id: 2026-09-11-api-warnings-leak-zh-tw
title: 後端回傳的繁中警告句被原樣顯示在所有語系
status: done
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T16:30:48Z
created_at: 2026-09-11T03:20:36Z
completed_at: 2026-09-11T17:18:15Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/api/app/trips/routing.py
  - apps/api/app/trips/router.py
  - apps/api/app/search/orchestrator.py
  - apps/api/app/search/tasks.py
  - apps/api/tests/test_trip_weather.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/web/components/route-segment-card.tsx
  - apps/web/components/trip-weather-panel.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/components/route-segment-card.test.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/components/trip-weather-panel.test.tsx
  - apps/web/lib/warnings.ts
  - apps/web/lib/warnings.test.ts
  - apps/api/app/trips/route_planner.py
  - apps/api/tests/test_trip_routing.py
  - apps/api/tests/test_trip_route_planner.py
  - apps/api/tests/test_korea_transit_google_fallback.py
  - apps/api/tests/test_naver_maps.py
  - apps/api/tests/test_google_weather.py
  - apps/api/app/weather/google.py
  - apps/api/app/weather/met_norway.py
  - apps/api/app/trips/route_tasks.py
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
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

- [x] 上列所有 `warnings` 改為 append 代碼。
- [x] 五語系前端 catalog 有對應翻譯。
- [x] 未知代碼被安全忽略，不會把原始字串印給使用者。

## Steps

- [x] 為每則警告定一個代碼，沿用 `"children_ages_missing"` 那種 snake_case 命名。
- [x] 後端四個檔改為 append 代碼；有參數的警告改回傳 `{code, params}`。
- [x] 前端三個渲染點改為查表，並照 `stay-area-flow.tsx:315` 的作法先 `filter` 掉不認得的代碼。
- [x] 五語系 catalog 補齊。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests -k "routing or search" -q
cd apps/web && npm run check:i18n && npm run test:web -- route-segment trip-weather
```

## Notes

- `apps/api/app/places/router.py:513-516` 的 `assumptions` 與 `:541` 的 `next_step` 是同一類問題，但那個檔被 `2026-09-11-wizard-crash-when-all-criteria-any` 佔住 scope，刻意沒納入。兩張任務誰先做完，把剩下那個記到對方 Notes 裡。
- `apps/api/app/usage/service.py:256` 的 402 detail 也是寫死繁中，由 `2026-09-11-usage-exhausted-dead-end` 處理。

## 瀏覽器實測補充（2026-09-11 第二輪）

用真實瀏覽器對 `en` / `ja` / `ko` 共 12 條路由，搜尋第一輪點名的 27 個寫死繁中字串，**零命中**。

**這不代表本任務的問題不存在，而是那些程式路徑在唯讀環境下走不到**：刪除確認框需要帳號裡有行程（測試帳號 0 筆）、機票與飯店卡需要完成一次搜尋（環境只轉讀取，不送寫入）、行程時間軸需要行程裡有項目。

所以本任務的狀態是**未驗證**，不是**已推翻**。接手的人請自己建一筆有內容的行程再確認，不要因為「掃描沒掃到」就把它關掉。

順帶澄清一個第二輪用過的無效指標：曾以「頁面漢字佔比」推估洩漏程度，但**日文本來就使用漢字**（實測 `ja` 頁面漢字 28–37%，同時有大量假名，是真正的日文），該指標對日文無效，不可採信。英文頁實測漢字僅 0.2–5.2%，且經逐一檢查後確認全部來自語言切換器的語言名稱（繁體中文／简体中文／日本語），屬正確做法。

## claim 用了 --force，理由寫在這裡（claude-opus-5, 2026-09-11）

`apps/api/app/trips/routing.py` 與 `router.py` 在 `2026-09-10-seoul-day2-transport-ux`（codex-seoul-day2-release）的 scope 裡。理由與 `2026-09-11-trips-list-hardcoded-zh-tw` 那張相同：claim 已逾 34 小時（協定上算 stale，board 也標了 stale），而它的工作已經合併進 main（`5f34f77`）。

## 完成紀錄（claude-opus-5, 2026-09-11）

任務列的四個檔都改成代碼了，另外把三件事一起做掉——都是同一個渲染點會吃到的，不做的話這張任務的 DoD 其實不成立：

- `trips/route_planner.py:130` 的 `f"固定預約可能遲到 {late_minutes} 分鐘"`。
- `trips/routing.py` 另外四處（`:339` `:340` 的班次範圍預覽、NAVER 路況、平均等待時間）與 `trips/route_tasks.py:213`。
- `weather/google.py` 四則與 `weather/met_norway.py` 一則。**這一項是修正我自己的一個錯誤判斷**：我原本以為 `weather.warnings` 是 Google 已經在地化過的氣象警示，所以打算原樣放行；讀了 `weather/google.py:286-300` 才發現那四句是我們自己 append 的繁中。

### 帶參數的那一則沒有改成 `{code, params}`

`固定預約可能遲到 {n} 分鐘` 的分鐘數**本來就已經結構化地傳出去了**——`RouteScheduleConflict.late_minutes`，而 `route-mode-panel.tsx:556` 早就用 `t("conflictLate", { minutes })` 把它翻成五語系顯示。那句警告只是把同一個數字再用繁中講一次。

所以這裡發代碼 `fixed_booking_late`，文案不帶數字（「這段移動可能讓下一個固定預約遲到，請確認下一站的時間。」），確切分鐘數留給既有的 `conflictLate`。這樣不必動 schema、不必動 `warnings_json` 的既有資料，也沒有真的遺失資訊。剩下真正需要 `{code, params}` 的警告列在 `2026-09-11-remaining-api-warning-literals`。

### 「未知代碼安全忽略」不能寫成單純的 filter

第一版我在三個渲染點都寫了 `filter(KNOWN.has)`。跑測試才發現這會把 `trip-weather-panel.test.tsx:124` 的供應商警示（`山區天氣變化較快…`）一起丟掉——`weather.warnings` 是我們自己的代碼**和**供應商自由文字混在一起的。

改成 `apps/web/lib/warnings.ts` 的 `translateWarnings()`，用形狀判斷：

- 像代碼（`^[a-z][a-z0-9_]*$`）而且查得到 → 翻譯。
- 像代碼但查不到 → 不顯示（代碼名字對讀者毫無用處，這是 DoD 的第三條）。
- 不像代碼 → 原樣顯示（供應商文字，或還沒遷移的舊警告）。

第三條順便讓這件事可以漸進遷移：還沒改的後端警告和已經存進 `warnings_json` 的舊資料都照常顯示，不會突然消失。

### 驗證

- `lib/warnings.test.ts` 四個案例分別釘住上面三條規則與空陣列；其中「供應商文字要留著」那條就是第一版會紅的那條。
- `route-segment-card.test.tsx` 加一條：已知代碼翻出來，`a_code_from_a_newer_server` 什麼都不顯示。
- 後端把 `DISCLOSURES[locale]` 之外的斷言一路改成代碼；`uv run pytest` 3257 passed，`ruff`、`mypy` 乾淨。
- `npm run test:web` 228 files / 2304 tests 全過。

### 掃出來但沒做的

整個 `apps/api/app` 還有二十餘處寫死的繁中警告，落在別的渲染點，而且多數帶參數。清單與優先順序建在 `2026-09-11-remaining-api-warning-literals`（P1）。
