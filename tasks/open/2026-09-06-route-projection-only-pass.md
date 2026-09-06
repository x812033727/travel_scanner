---
id: 2026-09-06-route-projection-only-pass
title: 編輯後不打 provider 也要把 DB 的行程時間重新推算
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T03:35:08Z
completed_at:
branch:
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

- [ ] 存檔有作廢路段時，後端做一次「只推算、不打 provider」：留下來的段沿用
      duration，缺的段用 `estimate_leg_minutes`，把每站 start/end 與 conflicts 寫回 DB。
- [ ] 這一步 0 次 provider 呼叫，且不會把估計值存成 `trip_route_segments`
      （否則 `_reusable_segment` 會把它當真值重用）。
- [ ] 分享頁在編輯後、查路前顯示的時間與編輯器一致。

## Steps

- [ ] `route_planner.project_day_schedule` 接受缺段的估計 duration（或另寫一個
      projection-only 版本），不要動它現有的 segment 語意。
- [ ] `update_itinerary` 在作廢之後呼叫它（同步或排一個不打 provider 的 job）。
- [ ] 測試：有一段缺、一段留 → 下游 start_time 被重推、沒有任何 segment 被新增。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trip_route_planner.py
```

## Notes

- 前端的估計公式在 `apps/web/lib/trip-types.ts` 的 `estimateLegMinutes`，後端在
  `apps/api/app/trips/routing.py` 的 `estimate_leg_minutes`，兩邊數字一樣。
- 這是 P2：編輯器畫面已經正確，只有分享頁與離線快取會落後到使用者按查路。
