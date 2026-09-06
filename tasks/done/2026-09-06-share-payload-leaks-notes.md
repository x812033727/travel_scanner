---
id: 2026-09-06-share-payload-leaks-notes
title: 分享連結會外洩項目備註與整包 data
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:42:57Z
created_at: 2026-09-06T00:53:04Z
completed_at: 2026-09-06T02:55:51Z
branch: claude/trip-api-p1
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/api/tests/test_trip_share_payload.py
  - apps/web/components/shared-trip-view.tsx
  - apps/web/lib/trip-types.ts
---

# 分享連結會外洩項目備註與整包 data

## Why

`GET /shared-trips/{token}` 的白名單（`app/trips/router.py`，`public_router.get` 裡的
`for key in (...)`）包含 `"items"` 與 `"data"`：

- `"items"` 走 `serialize_item()`，那個函式輸出 `"notes": item.notes` 和 `"data": item.data`。
  **每個項目的個人備註都會送給任何持有分享連結的人。**
- `"data"` 是行程的整包 blob，裡面有 `preferences`（含 `budget_twd`）、`total_cost`
  （逐項價格拆解）、`planning`（AI 供應商與警告）、`primary_lodging` 等。

分享連結的定位是「唯讀行程給朋友看」。2026-09-06 新加的行程備註（`trip_plans.notes`）
與成本帳目（`trip_expenses`）都刻意沒有進白名單，而且有整合測試釘住；但**項目層備註與
`data` 是在那之前就在漏的**，當時只有記下來沒修。

## Definition of done

- [x] 分享 payload 不含任何一筆 `items[].notes`。
- [x] 分享 payload 不含 `data`，或只含明確挑過、確定可公開的子集。
- [x] 有整合測試斷言上述兩點（比照 `test_trip_and_day_notes_persist_and_stay_out_of_the_share`
      的寫法）。
- [x] 擁有者自己開 `GET /trips/{id}` 仍看得到備註與 `data`（不要為了修分享而弄壞編輯器）。

## Steps

- [x] 讓分享路徑用一個獨立的 item 序列化，而不是共用 `serialize_item()`：
      只輸出畫面需要的欄位（title、時間、位置、地圖連結、duration…），不含 `notes`／`data`。
- [x] 決定 `data` 怎麼辦。`shared-trip-view.tsx` 與 `itinerary-timeline.tsx` 實際上用到
      `data` 的哪些鍵要先查清楚再刪，別直接拿掉導致分享頁壞掉。
- [x] 在 `test_integration_postgres_redis.py` 加斷言。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/ -q -k share
RUN_INTEGRATION_TESTS=1 ./.venv/Scripts/python.exe -m pytest tests/test_integration_postgres_redis.py -q -k share
```

手動：建立行程 → 在某個項目寫備註 → 產生分享連結 → 用無痕視窗開，
`GET /api/v1/shared-trips/<token>` 的回應裡不應該出現那段備註。

## Notes

**2026-09-06 完成。** 分享端點改成兩層白名單：行程層 `PUBLIC_TRIP_KEYS`（id、name、destination_name、
start_date、end_date、timezone、route_segments、updated_at；`data`、`total_price`、`currency`、`mode`、`version`、
`destination_place_id`、`route_preference` 全部拿掉——分享頁一個都沒讀），項目層 `public_item()` 只留
`PUBLIC_ITEM_KEYS`（時間軸畫得到的欄位）加上 `data` 的兩個鍵：`timeline_section` 與 `flight_info`
（後者再過一層 `PUBLIC_FLIGHT_INFO_KEYS`，只留班次時刻，不留 `price_snapshot`／訂位代號）。
`serialize_item()` 本身沒動：`router.py` 約 2429 行用它 round-trip 成 `ItineraryItemRequest`，改它會壞掉編輯器的儲存路徑。

分享頁實際讀的鍵（查過 `shared-trip-view.tsx`、`itinerary-timeline.tsx`、`flight-anchor-card.tsx`、`lib/trip-types.ts`）：
行程層 `name/destination_name/items/route_segments/timezone/updated_at`；項目層另需 `data.timeline_section`
（`isLogisticsItem`）與 `data.flight_info`（航班卡）。`priceSnapshot()` 缺資料時本來就回 null，所以航班卡少了報價不會壞。
前端加了 `SharedTrip` 型別（`Pick<Trip, …>`）讓分享頁不再假裝拿到整個 `Trip`。

測試：`tests/test_trip_share_payload.py`（無 DB，釘白名單與航班子集）；`test_share_link_carries_no_item_notes_and_no_trip_data`
（整合，用 `_signed_in_headers()`，PUT 一筆帶備註與 `price_snapshot` 的項目後開分享連結，斷言鍵集合、無備註、`data` 只剩區段）。

**白名單本身是加法式的（安全設計）** —— `app/trips/router.py` 約 4741 行附近的
`for key in ("id", "name", "mode", "total_price", "currency", "data", "version", …,
"items", "route_segments", "updated_at")`。所以只要把 `"data"` 拿掉、
並讓 `"items"` 走另一個序列化函式就好，不需要改動擁有者路徑。

**`serialize_item()` 在 `app/trips/router.py:609`**，輸出裡 `"data": item.data`（約 643 行）
與 `"notes": item.notes`（約 648 行）就是外洩點。它有 `locale`／`localized` 參數，
分享路徑要複用它的多語言標題邏輯的話，考慮加一個 `public=True` 參數而不是整個複製一份。

**整合測試會跑在 CI**（`ci.yml` 有 `RUN_INTEGRATION_TESTS: "1"`）。注意該檔案已經對同一個 IP
發出約 26 次 `POST /auth/register`，上限是 30/小時；**新測試請用 `_signed_in_headers()`
helper（2026-09-06 加的）直接建 user 列 + 簽 token**，不要再多打一次註冊，
否則會把別的測試推爆成 429。
