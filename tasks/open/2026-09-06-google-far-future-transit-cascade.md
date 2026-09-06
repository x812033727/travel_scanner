---
id: 2026-09-06-google-far-future-transit-cascade
title: Google 遠期大眾運輸一段最多打 6 次，且是唯一沒有預算保留的路線 provider
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T02:45:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/routing.py
  - apps/api/tests/test_trip_routing.py
---

# Google 遠期大眾運輸一段最多打 6 次，且是唯一沒有預算保留的路線 provider

## Why

`GoogleRouteProvider.compute_options`（`routing.py:511-578`）為一段路準備最多 6 個請求 body
（`requested`、`without_preference`、`coordinates`、`near_term_schedule`、`near_term_daytime`、
`current_schedule`），空結果就打下一個。出發時間超過 14 天的大眾運輸，`requested` 幾乎必空
（Google 只公布近期班次），所以一段路常常是「2–4 次計費換 1 個結果」。

而且 Google 是唯一沒有 `reserve_*` 預算保留的路線 provider：`usage_meter.py:314` 有
`reserve_google_maps_request`，但 `_post` 只在 `finally` 裡 `record_google_maps_request`，
永遠不會擋。

影響範圍：Google 負責大眾運輸的地區（台灣等；日本走 Ekispert、韓國走 ODsay），以及所有地區的
步行／汽車。

## Definition of done

- [ ] 出發時間 > now + 14 天的大眾運輸，第一個送出的請求就是 `near_term_schedule`，
      其餘 fallback 順序不變。
- [ ] Google 路線請求在送出前先 `reserve_google_maps_request`，額度用完時回 `[]` 並記 log，
      跟 Ekispert／ODsay 一致。
- [ ] 現有 `test_scheduled_transit_*` / `test_far_future_transit_*` 測試依新順序調整，
      並新增「>14 天只打一次」的案例。

## Steps

- [ ] 讀 `supported_transit_time`（`routing.py:242`）與 `_next_matching_transit_time`
      確認 14 天門檻的來源。
- [ ] 調整 `attempts` 的組裝順序。
- [ ] 接 `reserve_google_maps_request`（看 `restaurants/google.py:162,214` 的用法）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trip_routing.py -k "google"
```

## Notes

- 從 2026-09-06 交通成本檢討分出來；主要漏額度的是整趟重算與快取 key，先修那兩張
  （`2026-09-06-route-cache-time-key`、`2026-09-06-route-recompute-reuses-saved-segments`）。
