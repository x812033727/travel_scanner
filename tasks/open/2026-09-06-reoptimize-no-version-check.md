---
id: 2026-09-06-reoptimize-no-version-check
title: reoptimize 沒有版本檢查，日期守衛是 TOCTOU
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T04:13:16Z
created_at: 2026-09-06T00:55:36Z
completed_at:
branch: claude/trip-api-p2
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/tests/test_trip_reschedule.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/web/components/trip-editor.tsx
---

# reoptimize 沒有版本檢查，日期守衛是 TOCTOU

## Why

`POST /trips/{id}/reoptimize` **完全不接受 version 參數**，而 #155 為它新加的
`trip_search_dates_diverged` 守衛（`router.py:1369-1400`）是一個讀取時的檢查，
擋在一個要跑好幾秒的流程前面。

所以：檢查通過之後、寫入之前，另一個請求（例如 `PATCH /trips/{id}` 改日期）可以插進來，
而 reoptimize 仍然會用它一開始讀到的狀態寫入。這是典型的 TOCTOU。

同一個守衛還有第二個洞：`search_dates_diverged` 的第二個條件是
`trip_end is not None and return_date is not None and trip_end != return_date`。
`SearchCreate.return_date` 對單程／多城市搜尋是 None，所以那個條件永遠是 False。
單程搜尋建立的行程把結束日往前縮之後可以繞過守衛，接著 reoptimize 會把項目重新插在
原本的第 4、5 天 —— 現在已經超出 `trip.end_date` —— 之後每一次
`PUT /trips/{id}/itinerary` 都會撞到 `router.py:2000` 的範圍檢查，
永久回 422 `itinerary_date_out_of_range`。**行程再也不能編輯**，正是這個守衛要防的那個鎖死。

## Definition of done

- [x] reoptimize 像其他行程寫入一樣接受並比對 version，寫入時仍持有該版本。
- [x] 日期分歧的判斷不依賴搜尋自己的可選欄位，單程與多城市行程也擋得住。

## Steps

- [x] 讓 reoptimize 走與其他寫入相同的 compare-and-swap 模式。
- [x] 改成比對行程當下的 start_date/end_date 與已存方案首末日的實際日期，
      而不是比對 SearchRequest 的 departure_date/return_date；
      或在 return_date 為 None 時退回 `departure_date + (天數 - 1)`。
- [x] 加測試涵蓋單程搜尋建立的行程縮短結束日之後的路徑。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_reschedule.py tests/test_trip_schedule.py
```

## Notes

出處：補跑 #155 的六路審查。TOCTOU 由 `reschedule-concurrency` 審查者提出（blocker），
NULL return_date 的洞由 `reschedule-corruption` 審查者提出（medium）。兩者是同一個守衛的兩面，
所以合在一張任務。

同一個審查者還提到一個低嚴重度的相關問題：在新的 409 之後用同一個 Idempotency-Key 重試 reoptimize，
會得到 HTTP 200 加上未變動的行程，呈現得像一次完成的重新查價。這個路徑早於 #155，
修上面兩點的時候可以順手看一下。

2026-09-06 claude-fable-5-1：

- `POST /trips/{id}/reoptimize` 現在要 body `{version}`（缺就 422）。先便宜比一次版本
  （不符就釋放保留次數、409 `trip_version_conflict`，供應商一通都不打），供應商回來後再以
  `UPDATE ... WHERE version = :version RETURNING` 做 compare-and-swap，輸了就 rollback、釋放保留、409；
  贏了才刪列重建。前端 `reoptimizePrices()` 送 `currentTrip.version`。
- 日期守衛改成兩段：`search_query_for_trip()` 把搜尋平移到行程當下日期（不再比對 SearchRequest 的
  可選欄位），`ensure_plan_within_trip()` 在寫入前檢查方案每一天都落在 `trip.start_date..end_date` 內。
  單程／多城市原本繞得過的那個洞，現在是對結果檢查，跟搜尋有沒有 `return_date` 無關。
- 順手修了 Notes 提到的低嚴重度問題：保留次數只有在 CAS 成功後才寫 `resource_id`，所以用同一個
  Idempotency-Key 重試一次失敗的 reoptimize 會得到 409 `idempotency_result_unavailable`，
  不會再拿到 200 加原封不動的行程。
- 測試：`test_trip_reschedule.py` 四個單元案例；`test_integration_postgres_redis.py`
  一個整合案例（版本不符 409 且不打供應商、越界方案 409、失敗重試不重放、次數不扣、列 id 不變）。
