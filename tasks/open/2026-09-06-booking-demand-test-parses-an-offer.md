---
id: 2026-09-06-booking-demand-test-parses-an-offer
title: Booking Demand 連線測試停在城市 ID，從不解析旅館報價
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T15:15:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/providers/booking.py
  - apps/api/tests/test_booking_demand_probe.py
---

# Booking Demand 連線測試停在城市 ID，從不解析旅館報價

## Why

後台 Booking.com Demand API 的「測試連線」呼叫的是：

```python
if provider == "booking_demand":
    await BookingHotelProvider(redis, settings).probe()
    return f"Booking.com Demand API {settings.booking_demand_env} 驗證成功"
```
（`apps/api/app/admin/service.py`）

而 `probe()` 只做到解析城市 ID 就結束（`apps/api/app/providers/booking.py:438-447`）：

```python
async def probe(self) -> None:
    query = SearchCreate(origin="TPE", destination="NRT", ...)
    if await self._city_id(query) is None:
        raise ConnectionError("Booking Demand API 已回應，但無法對應東京城市資料")
```

它從不請求、也從不解析任何一筆旅館報價。所以只要城市查得到，測試就顯示「驗證成功」，即使
`/accommodations/search` 的權限沒開、回應格式變了、或報價解析失敗——那些才是使用者真正會遇到的路徑。

這和 `2026-09-06-admin-planner-test-real-candidates`（已完成）是同一個形狀：健康檢查量的東西
不是使用者會遇到的東西。那張任務把 AI 規劃測試從「送空候選」改成載入真實候選之後，才第一次
真的走過會壞的那一步。

`booking_demand` 另外還被 `_production_test_required` 列管（`admin/service.py:910`），
production 環境**必須**通過這個測試才會標示為可用，所以測試測得不夠深的代價更高。

## Definition of done

- [ ] 測試會實際取得並解析至少一筆旅館報價，解析失敗時測試失敗。
- [ ] 成功訊息帶出可辨識的證據（例如取得幾筆報價），讓操作者看得出它真的走完了。
- [ ] sandbox 與 production 兩種環境都適用，不需要為測試特別放寬驗證。

## Steps

- [ ] 擴充 `BookingHotelProvider.probe()`：在 `_city_id` 之後實際跑一次最小的住宿查詢並解析回應，
      沿用正式查詢路徑的解析函式，不要另寫一份寬鬆的解析。
- [ ] 日期選未來且短天數，把查詢量壓到最低；Demand API 有額度。
- [ ] 訊息加上報價筆數，比照 `admin/service.py` 裡 MET Norway 測試回報預報天數的寫法。
- [ ] 新增 `apps/api/tests/test_booking_demand_probe.py`，用 `httpx.MockTransport` 覆蓋
      「城市查得到但報價解析失敗」這個情境，斷言測試會失敗。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_booking_demand_probe.py -q
```

在 `/admin/settings` 對 Booking.com Demand API 按測試連線，訊息應包含取得的報價筆數。

## Notes

優先度 P3，因為 Booking Demand 目前未啟用（`booking_demand` 需要 Affiliate ID 與 Bearer Token，
生產環境尚未設定），所以現在沒有人被這個問題影響。等要啟用它時再做，做的時機比做的難度重要。

來源與 `2026-09-06-configured-readiness-beyond-key-presence` 相同：2026-09-06 那輪缺陷類別搜尋的
副產物，事實成立但不屬於當時搜尋的類別。該輪把這一項標為 speculative，我在 origin/main 上逐行
確認過 `probe()` 的內容，確實只到城市 ID 為止。
