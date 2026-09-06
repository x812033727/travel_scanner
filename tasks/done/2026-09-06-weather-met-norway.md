---
id: 2026-09-06-weather-met-norway
title: 旅程天氣改由 MET Norway 供應，Google Weather 退為備援
status: done
priority: P2
area: api
owner: claude-fable-5.1
claimed_at: 2026-09-06T06:30:56Z
created_at: 2026-09-06T06:28:54Z
completed_at: 2026-09-06T07:07:25Z
branch: claude/weather-met-norway
depends_on: []
scope:
  - apps/api/app/weather
  - apps/api/app/config.py
  - apps/api/app/trips/router.py
  - apps/api/app/admin/service.py
  - apps/api/tests/test_met_norway_weather.py
  - apps/api/tests/test_trip_weather.py
  - apps/web/components/trip-weather-panel.tsx
  - apps/web/components/trip-weather-panel.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - .env.example
---

# 旅程天氣改由 MET Norway 供應，Google Weather 退為備援

## Why

旅程天氣現在每次查詢打兩次 Google Weather（目前天氣 + 10 日預報），走 Google Maps Platform 計費。
owner 2026-09-06 從 public-apis 清單挑了 MET Norway：挪威氣象局的全球預報，CC BY 4.0，
**允許商業使用**，只要求 User-Agent 能識別應用、座標不超過四位小數、同一地點不要每分鐘重打。
Open-Meteo 雖然也免費，但免費方案只限非商業用途，mokaair 有分潤與付費點數，所以不選它。

## Definition of done

- [x] 旅程天氣預設由 MET Norway 供應；`weather_provider=google` 可以把 Google 排回第一順位。
- [x] 任一 provider 失敗就換下一個，全部失敗才回第一個的錯誤；Google 沒設金鑰時不再擋住整個功能。
- [x] MET 的 `symbol_code` 對到面板既有的 icon 規則（RAIN／SNOW／SLEET／THUNDER／CLEAR），
      五語系描述由請求 locale 決定。
- [x] 每日彙整用旅程時區切日：氣溫取瞬時值與六小時區間的極值、濕度與風速取最大、UV 只算白天、
      降雨量以小時值優先、六小時值只補沒被算到的時段，不重複累加。
- [x] MET 沒有降雨機率，面板改顯示降雨量（mm）；有機率的來源維持百分比。
- [x] 後台多一個「MET Norway 天氣」供應商，連線測試會真的查一次東京。
- [x] `apps/api` ruff／mypy／pytest 與 `apps/web` lint／typecheck／i18n／vitest 通過。

## Steps

- [x] `weather/met_norway.py`：Locationforecast 2.0 `complete` 解析、快取、錯誤對應、符號對照。
- [x] `weather/service.py`：`TripWeatherService` 決定順序與備援。
- [x] `config.py`：`weather_provider`、`met_norway_base_url`、`met_norway_user_agent`。
- [x] `trips/router.py`：改走 facade，帶入請求 locale 與旅程時區；警告文案不再寫死 Google。
- [x] `admin/service.py`：供應商定義、狀態與連線測試。
- [x] 前端面板：eyebrow 改顯示 `attribution`、降雨欄位支援 mm；`outOfRange` 五語系去掉 Google 字樣。
- [x] 測試：`test_met_norway_weather.py`、`test_weather_service.py`、`test_trip_weather.py`、面板測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_met_norway_weather.py tests/test_weather_service.py tests/test_trip_weather.py tests/test_google_weather.py
npm run lint:web && CI=1 npm run check:i18n && npm run typecheck:web && cd apps/web && npx vitest run components/trip-weather-panel.test.tsx
```

線上：開任一旅程頁，天氣區塊的 eyebrow 應顯示 MET NORWAY，來源列寫「資料來源：MET Norway」；
後台 `/admin/settings` 的「MET Norway 天氣」按連線測試會回「取得 N 天預報」。

## Notes

- 後台面板的分類對應（`providerCategoryOf`）與欄位標籤沒改：`admin-settings-panel.tsx`
  正被 `2026-09-06-multi-locale-guide-backfill` 佔用。目前 MET Norway 會落在「其他」分類、
  欄位用原始鍵名顯示，那張收掉後再補 `met_norway: "maps"` 與 `weather_provider`／
  `met_norway_user_agent` 的標籤（標籤要走 `admin.json` 目錄，`check:i18n` 會擋硬編碼中文）。
- MET 的 `Expires` 大約每小時更新，我們的 `weather_cache_ttl_seconds=900` 已符合它的節流要求。
- 日出日落沒接：MET 要另打 Sunrise API，每日一次，先留空。
- 生產 `.env` 沒有 `WEATHER_PROVIDER`，程式預設就是 met_norway；部署後不用改設定。
