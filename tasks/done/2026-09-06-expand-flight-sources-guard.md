---
id: 2026-09-06-expand-flight-sources-guard
title: 航班來源擴充讀舊資料沒有防護：型別不符的 search id 會直接 500
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T15:01:54Z
created_at: 2026-09-06T14:04:54Z
completed_at: 2026-09-06T15:15:21Z
branch: claude/flight-sources-guard
depends_on: []
scope:
  - apps/api/app/search/router.py
  - apps/api/tests/test_search_flight_sources.py
---

# 航班來源擴充讀舊資料沒有防護：型別不符的 search id 會直接 500

## Why

`POST /searches/{search_id}/flight-sources/expand` 用兩個沒有防護的 `model_validate` 讀回既有資料：

```python
query = SearchCreate.model_validate(search.request_json)
existing = [
    ensure_itinerary_key(FlightOffer.model_validate(item))
    for item in search.result_json.get("modules", {}).get("flight", [])
]
```
（`apps/api/app/search/router.py:262-268`）

同一個檔案在六十行之上做同一件事時是有防護的，這是最強的證據——那個 try/except 不是隨手寫的：

```python
try:
    original_query = SearchCreate.model_validate(search.request_json)
except ValueError:
    original_query = None
```
（`apps/api/app/search/router.py:198-201`）

**可觸發的路徑不是 schema 漂移，而是型別不符的列。** 有兩個端點會寫 `SearchRequest.request_json`，
而且寫的是不同的 schema：

- `apps/api/app/search/router.py` 寫 `SearchCreate.model_dump(mode="json")`。
- `apps/api/app/providers/flight_router.py:54-57` 寫 `LiveBackToBackSearch.model_dump(mode="json")`，
  `operation="live_back_to_back_fare_search"`。

`LiveBackToBackSearch` 沒有 `modules`、沒有 `destination`、沒有 `departure_date`，而 `SearchCreate`
的 `modules` 是 `Field(min_length=1)` 且沒有預設值，`validate_route` 還要求 origin/destination/
departure_date。所以這種列**永遠不可能**通過 `SearchCreate`，一定拋 `ValidationError`。

`_owned_search()`（`apps/api/app/search/router.py:230-236`）只比對 `id` 與 `user_id`，沒有比對
`operation`，所以沒有任何東西擋住這種列進到上面那行。`apps/api/app/main.py:69-70` 只註冊了
`AppError` 與 `RequestValidationError`，pydantic 的 `ValidationError` 兩者皆非，於是逃逸成 500。

**觸發難度**：`LiveBackToBackResponse` 不回傳 `search_id`，也沒有端點列出使用者的 search id，
前端唯一的呼叫點（`apps/web/components/search-experience.tsx`）帶的是 `POST /searches` 回來的 id。
所以最壞情況是呼叫者拿自己的列打自己，屬於罕見路徑，不是 P0——但它是 500 而不是 409/422，
而且同一列在冪等重播分支（`:246-253`）會成功回傳，同一份資料一條路正常一條路炸掉。

這張任務來自修完 `2026-09-06-tokyo-planner-duration-500` 之後，用 40 個代理對整個
repo 搜同一類缺陷（stored data → 有界 pydantic Field → 未處理的 ValidationError → 500）的結果。
掃出 18 個候選，17 個經對抗式查證後判定事實正確但不屬於這個類別，只有這一項存活。

## Definition of done

- [x] 用型別不符的 `search_id` 呼叫 flight-sources/expand，得到 4xx 與可讀訊息，而不是 500。
- [x] 用 `result_json` 中含有無法解析的航班報價的列呼叫，同樣不會 500。
- [x] 回歸測試涵蓋這兩種情況。

## Steps

- [x] 在 `_owned_search()` 或 `expand_flight_sources` 內判斷 `operation`，非航班搜尋的列以
      `AppError(404/409)` 拒絕；沿用 `:198-201` 既有的 try/except 形式包住兩個 `model_validate`。
- [x] 同檔案 `:197`、`:358`、`:409` 有同樣的裸 `FlightOffer.model_validate` 形式，一併檢視。
- [x] 新增 `apps/api/tests/test_search_flight_sources.py`：植入一列
      `operation="live_back_to_back_fare_search"` 的 `SearchRequest`，斷言回 4xx 而不是 500。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_search_flight_sources.py -q
```

## Notes


**同一輪搜尋中事實成立、但刻意不在此處理的設計問題**（若要做請各自另開任務，不要併進這張）：

- `normalize_draft` 把模型回傳的項目全部丟棄並改用內建目錄補齊時，`PlanningMetadata` 仍記
  `provider="minimax"`，而退費閘門只在 `provider == "catalog"` 時觸發
  （`apps/api/app/trips/router.py` 的 apply 路徑）。查證認為程式碼追蹤正確，但「實際會發生」
  這個前提沒有證據，需要先在生產環境觀察到才值得動。
- `_configured()` 只憑金鑰存在與否判斷就緒狀態，所以後台卡片可能顯示綠燈而功能其實不通。
- `ai_planner` 的後台連線測試送 `candidates=[]`，結構上看不到候選建構這條路徑。改成送一筆真實
  候選，就能在測試階段擋下 `tokyo-planner-duration-500` 那一類缺陷。

**已查證為不成立、不要重開的**：`AIPlannerCandidate.name`／`local_name` 的 160 字上限相對於
資料庫 255 字並無實際越界資料；四筆剛好落在邊界上的 Kanto 種子值目前合法；`extra="forbid"`
造成的 `ValidationError` 在 `apps/api/app/ai/itinerary.py` 的 provider 迴圈裡有被明確接住，
會回 HTTP 200 加 `status="fallback"` 並正確退費，不是未處理的例外。

### 做完之後（2026-09-06，claude-opus-5）

三個讀取點各包成一個具名 helper：`_stored_query`（`request_json` → `SearchCreate`）、
`_stored_offers`（`result_json.modules.flight` → `FlightOffer`）、`_stored_offer`（`FlightOfferRecord.data`）。
三個都回 409 加各自的 code（`search_not_expandable`／`search_offers_unreadable`／`offer_unreadable`），
不再讓 pydantic 的 `ValidationError` 逃到 500。

`expand_flight_sources` 的驗證提前到 `_owned_search` 之後、Redis 與供應商準備之前——
型別不符的列在做任何事之前就被擋下來，也不會白跑 provider 名冊。

兩個決定：

- **沒有加 operation 白名單。** 判斷「這列是不是可擴充的搜尋」的真正條件是 `request_json` 的形狀，
  不是 operation 字串；`search_operation()` 目前會回五種值，未來多一種就要記得改白名單，
  但形狀檢查不用。訊息也一樣清楚。
- **`:197` 的 `SearchCreate.model_validate` 維持原本的 `except ValueError → None`。** 那裡的語意不同：
  拿不到原始查詢時 refresh 仍然可以進行，不該變成 409。

測試分兩層：`tests/test_search_flight_sources.py` 直接測三個 helper（不需要資料庫，
包含一條釘住前提的案例——`LiveBackToBackSearch` 的 dump 永遠過不了 `SearchCreate`），
`test_integration_postgres_redis.py` 加一條端點層的案例，真的插一列
`operation="live_back_to_back_fare_search"` 再打 expand，斷言 409 而不是 500。
