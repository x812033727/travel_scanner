---
id: 2026-09-06-planner-shop-themes
title: 購物行程：規劃器聽得懂店家類型，也知道什麼當季
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T18:20:46Z
created_at: 2026-09-06T18:20:09Z
completed_at: 2026-09-06T18:21:27Z
branch: claude/planner-shop-themes
depends_on: []
scope:
  - apps/api/app/search/schemas.py
  - apps/api/app/ai/parser.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/hotspots/service.py
  - apps/api/app/trips/router.py
  - apps/api/app/trips/itinerary.py
  - apps/api/tests/test_planner_candidates.py
  - apps/web/lib/destinations.ts
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/messages/en/newTrip.json
  - apps/web/messages/ja/newTrip.json
  - apps/web/messages/ko/newTrip.json
  - apps/web/messages/zh-TW/newTrip.json
  - apps/web/messages/zh-CN/newTrip.json
---

# 購物行程：規劃器聽得懂店家類型，也知道什麼當季

## Why

主題（#245）讓目錄知道哪些景點是賞櫻、哪些購物景點賣藥妝，但 AI 規劃器完全看不到這一層。說「想買藥妝」的旅客拿到的還是那幾條熱門商店街；四月去京都的行程，櫻花名所排不排得進去純看它在熱門排行的名次。

使用者要的「購物行程」就是這個：選了購物興趣＋店家類型，行程裡就排進對應的店。

## Definition of done

- [x] 旅客可以在新行程表單選店家類型；只有選了「購物」才出現。
- [x] 指定的店家類型會排在該城市的一般商店街與地標之前。
- [x] 旅程月份落在某個季節主題內時，當季景點會被拉進候選池，**但有上限**——四月的京都不該變成連續十棵櫻花樹。
- [x] 延伸城市的花期不會重塑主行程。
- [x] 「想買藥妝」這種自然語言也能解析出店家類型。

## Steps

- [x] `SearchPreferences.shop_themes`：清洗、去重、非空時補上 `shopping` 興趣。
- [x] `service.py`：`months_in_span`、`in_season`、`item_theme_slugs`、`season_slugs_for`、`PLANNER_SEASONAL_SHARE`、`SHOP_DEFAULT_DURATION_MINUTES`，以及 `load_planner_hotspots` 的收集順序與配額。
- [x] `ItineraryHotspot.in_season`、`AIPlannerCandidate.themes/in_season`。
- [x] `SYSTEM_PROMPT` 說明兩個欄位；供應商掛掉時的 catalog fallback 排序也照顧。
- [x] `trips/router.py` 把偏好與**整趟旅程**的月份傳下去。
- [x] `ai/parser.py`：`SHOP_THEME_KEYWORDS`。
- [x] 前端店型 chips 子列＋五語文案。
- [x] 測試：API 7 個新案例、前端 2 個。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest      # 1112 passed
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

新行程表單：選「購物」→ 出現店型子列 → 選「藥妝」「電器」→ 送出的 `preferences.shop_themes` 應為 `["drugstore","electronics"]`，`interests` 含 `shopping`。

## Notes

- **季節取自整趟旅程，不是被重排的那一段**：四月行程中間重排某一天，那天仍然是四月。所以 `_load_trip_candidates` 傳的是 `trip.start_date/end_date`，不是 `start_date/end_date`。
- **當季有配額（1/8）**：超過的當季景點得純靠名次競爭。沒有這條的話，四月的京都會被櫻花洗版。
- **延伸城市不算當季**：`in_season()` 只認主目的地。鎌倉的花期不是重排東京行程的理由。
- 指定店型時會自動補 `shopping` 興趣（表單、解析器、`SearchPreferences` 三處都補），所以配額邏輯不會因為興趣沒勾而失效。
- 店家沒有種子時長時給 75 分鐘（地標是 120）。
- `_ordered_hotspots` 的兩個排序鍵都改了（初始排序與最近鄰）；`_ordered_excursions` 沒改——那是挑一日遊的，沒有店可言。
- 解析器只收通用名詞（藥妝、電器、百貨…）。品牌名是地點名稱，不是偏好。
