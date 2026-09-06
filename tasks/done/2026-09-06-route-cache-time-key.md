---
id: 2026-09-06-route-cache-time-key
title: 路線快取 key 依 provider 的時間粒度；DB 路段過期與 Redis TTL 分開
status: done
priority: P1
area: api
owner: claude-fable-5.1
claimed_at: 2026-09-06T02:45:39Z
created_at: 2026-09-06T02:45:21Z
completed_at: 2026-09-06T05:05:03Z
branch: claude/route-cache-time-key
depends_on: []
scope:
  - apps/api/app/trips/routing.py
  - apps/api/app/trips/route_tasks.py
  - apps/api/app/trips/router.py
  - apps/api/app/config.py
  - apps/api/tests/test_trip_routing.py
  - apps/api/tests/test_trip_route_tasks.py
  - .env.example
---

# 路線快取 key 依 provider 的時間粒度；DB 路段過期與 Redis TTL 分開

## Why

`RouteService.compute_options` 的 Redis 快取 key 把出發時間以 ISO 分鐘級塞進去
（`routing.py:2211`），但實際送給 provider 的時間粒度遠比這粗：

- Ekispert `plain`（現在的預設）只送 `date`，不送 `time`（`routing.py:1580-1582`）；
- ODsay 完全不看時間（`routing.py:1891`）；
- Google 步行不送 `departureTime`（`routing.py:491`）；
- Google 汽車送的是 `max(departure, now)` 加 `TRAFFIC_AWARE`，幾週後的日期只是預測值。

整天路線是串連推算的（上一段抵達 = 下一段出發），所以上游改一站，下游每一段的出發時間都
變幾分鐘 → 全部 cache miss → 每段都再打一次 provider。Ekispert 每月只有 450 次。

另外 `trip_route_segments.expires_at` 沿用同一個 `route_cache_ttl_seconds=900`
（`route_tasks.py:215`、`router.py:4044`），存進 DB 的路段 15 分鐘就被 `segment_from_record`
標成 stale（`route_planner.py:150-155`）。Redis 的 provider 結果快取和「使用者已套用的路段」
是兩件事，不該共用一個 15 分鐘。

## Definition of done

- [x] 同一段路、同一種交通方式，在 provider 看不出差別的時間範圍內（Ekispert plain 同一天、
      ODsay 任何時間、Google 步行任何時間、Google 汽車同 15 分鐘、其餘大眾運輸同 10 分鐘）
      只打一次 provider。
- [x] 不同 mode、不同 preference、不同 provider 組合仍各自快取。
- [x] miss 時送給 provider 的參數不變（仍是真實出發時間）。
- [x] 存進 DB 的路段改用獨立的 `route_segment_ttl_seconds`（預設 30 天），不再 15 分鐘就 stale；
      手動路段仍永不過期。
- [x] `route_cache_ttl_seconds` 預設拉到 86_400。
- [x] `apps/api` 的 ruff / mypy / pytest 通過。

## Steps

- [x] `routing.py`：新增 `RouteService._cache_time_key(providers, departure_time, travel_mode)`，
      `compute_options` 的 `"t"` 改用它。
- [x] `config.py`：新增 `route_segment_ttl_seconds`；`route_cache_ttl_seconds` 預設 86_400。
      `.env.example` 補一行。
- [x] `route_tasks.py:215, :283` 與 `router.py:4044` 改用 `route_segment_ttl_seconds`。
- [x] `test_trip_routing.py` 補桶化測試；`test_trip_route_tasks.py` 確認 `expires_at` 不再是 15 分鐘。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_trip_routing.py tests/test_trip_route_tasks.py tests/test_trip_route_planner.py tests/test_admin_provider_settings.py
```

部署後到 `/admin/settings` 的 Google Maps 區確認 `route_cache_ttl_seconds` 沒有被 DB 覆寫成 900
（DB 值蓋過 env 預設）。

## Notes

- 命中時的 `departure_time`/`arrival_time` 不需要精確：`project_day_schedule`
  （`route_planner.py:88-90`）會用 `duration_minutes` 從上一站結束時間重新推算，
  所以桶化不會讓時間表錯位。
- 這張只改 key 與 TTL，不改「整天重算每段都打 provider」的行為；那是
  `2026-09-06-route-recompute-reuses-saved-segments`。
- 改 key 後舊的 `routes:options:*` 條目會自然過期，不用清。
- 結論的前提：「一次把三種交通方式都讀回來」不會省——每家 provider 都是一段路 × 一種交通方式
  計一次，Google Routes 一個請求只能指定一個 `travelMode`；預覽面板已經是點哪種才查哪種。
