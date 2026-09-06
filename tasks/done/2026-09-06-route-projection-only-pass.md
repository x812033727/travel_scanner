---
id: 2026-09-06-route-projection-only-pass
title: 編輯後不打 provider 也要把 DB 的行程時間重新推算
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T10:50:17Z
created_at: 2026-09-06T03:35:08Z
completed_at: 2026-09-06T10:50:21Z
branch: claude/trip-api-extras
depends_on:
  - 2026-09-06-route-recompute-reuses-saved-segments
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/route_planner.py
  - apps/api/tests/test_trip_route_planner.py
---

# 編輯後不打 provider 也要把 DB 的行程時間重新推算

## Why

`2026-09-06-route-recompute-reuses-saved-segments` 之後，`PUT /itinerary` 不再排背景重算。
編輯器本身會用 `projectChainedStarts` 把時間接好，但 **DB 裡的 `trip_plan_items.start_time /
end_time` 要等使用者按查路才會重推**。看得到差異的地方：唯讀分享頁、PWA 離線快取、
`routing.conflicts`（可能遲到）。AI 草稿行程以前是存檔後幾秒自動修好；手動行程一直都是這樣。

## Definition of done

- [x] 存檔有作廢路段時，後端做一次「只推算、不打 provider」：留下來的段沿用
      duration，缺的段用 `estimate_leg_minutes`，把每站 start/end 與 conflicts 寫回 DB。
- [x] 這一步 0 次 provider 呼叫，且不會把估計值存成 `trip_route_segments`
      （否則 `_reusable_segment` 會把它當真值重用）。
- [x] 分享頁在編輯後、查路前顯示的時間與編輯器一致。

## Steps

- [x] `route_planner.project_day_schedule` 接受缺段的估計 duration（或另寫一個
      projection-only 版本），不要動它現有的 segment 語意。
- [x] `update_itinerary` 在作廢之後呼叫它（同步或排一個不打 provider 的 job）。
- [x] 測試：有一段缺、一段留 → 下游 start_time 被重推、沒有任何 segment 被新增。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trip_route_planner.py
```

## Notes

- 前端的估計公式在 `apps/web/lib/trip-types.ts` 的 `estimateLegMinutes`，後端在
  `apps/api/app/trips/routing.py` 的 `estimate_leg_minutes`，兩邊數字一樣。
- 這是 P2：編輯器畫面已經正確，只有分享頁與離線快取會落後到使用者按查路。

2026-09-06 claude-opus-5：

- `route_planner.py` 新增 `estimated_segment()` 與 `project_day_with_estimates()`。後者把「還活著的段」
  加上「每個缺口一段估算」餵給既有的 `project_day_schedule`，所以現有的 segment 語意一個字都沒改。
  估算段標成 `provider="estimate"`、`status="estimated"`、`schedule_mode="estimate"`，
  分鐘數用 `estimate_leg_minutes`（與前端 `estimateLegMinutes` 同一組數字）。
- `router.py` 新增 `reproject_saved_times()`，在 `update_itinerary` 作廢路段之後、最後一次 commit 之前跑：
  只走被動到的那幾天，把非固定時間的列 `start_time/end_time` 寫回 DB，並把 conflicts 放進
  `trip.data["routing"]["conflicts"]`。**0 次 provider 呼叫**，而且完全沒有呼叫 `persist_projected_segments`，
  所以估算值不會進 `trip_route_segments`，`_reusable_segment` 不可能把它當真值重用。
- 兩端缺座標的段不估、直接跳過（測試釘住），因為距離估算需要兩端經緯度。
- 測試：`test_trip_route_planner.py` 兩支新案例——一段留一段缺時的時間鏈與估算值，
  以及缺座標時不亂猜。
