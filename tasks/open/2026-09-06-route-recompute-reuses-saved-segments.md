---
id: 2026-09-06-route-recompute-reuses-saved-segments
title: 整天重算只打真的缺的路段；編輯後不再自動整趟重算
status: review
priority: P1
area: api
owner: claude-fable-5.1
claimed_at: 2026-09-06T02:54:59Z
created_at: 2026-09-06T02:45:23Z
completed_at:
branch: claude/route-recompute-reuses-saved-segments
depends_on:
  - 2026-09-06-route-cache-time-key
scope:
  - apps/api/app/trips/route_tasks.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_trip_route_tasks.py
  - apps/api/tests/test_integration_postgres_redis.py
---

# 整天重算只打真的缺的路段；編輯後不再自動整趟重算

## Why

`compute_and_apply_routes`（`route_tasks.py:136-226`）對每一段相鄰 pair 都呼叫 `service.compute`，
已存在 DB 的路段只在 provider 失敗時當備援，從不重用。而 `PUT /itinerary` 的作廢邏輯其實很精準
——只刪碰到被改那一站的兩段（`router.py:2589-2601`）——然後卻排一個**整趟**的重算 job
（`router.py:2633`，不帶 day）。結果：AI 草稿行程改一站地點，5 天 × 5 站 = 20 段全部重打。
Ekispert 月額度 450 次撐不到 25 次編輯。

同一個迴圈也讓「改緩衝」變成整天重打，但緩衝根本不進 provider 請求。

產品決定（2026-09-06）：編輯之後**不自動**補查，缺的段先顯示距離估計，使用者按查路或點開那一段
才查，而且只查缺的段。行程第一次產生（AI 草稿、第一次查路）仍整天查一次。

## Definition of done

- [x] 整天重算時，已存在、mode 與 preference 都吻合、未過期、非 failed 的路段直接重用，不打
      provider；只有缺的段（被作廢的）才打。
- [x] 只改緩衝 → 0 次 provider，`ready_time` 跟著新緩衝重推。
- [x] 改當日預設交通方式 → 只有 mode 不同的非 override 段重打；`is_override` 的段沿用自己的
      mode 不重打。
- [x] `refresh=True` 仍全部重打、跳過 Redis。
- [x] `PUT /itinerary` 有作廢路段時不再 enqueue 整趟重算；`routing.status` 設為 `stale`，
      `total` 反映段數。第一次產生行程的 enqueue（`router.py:820、1695、3273、3463`）不變。
- [x] `apps/api` 的 ruff / mypy / pytest 通過；整合測試裡的 auto_compute 案例
      （`test_integration_postgres_redis.py:1007-1018`）依新行為調整。

## Steps

- [x] `route_tasks.py`：manual override 分支之後、`service.compute` 之前加「重用」分支。
- [x] `router.py:2617-2633`：拿掉 enqueue，改寫 `routing` 狀態為 `stale`。
- [x] `test_trip_route_tasks.py`：3 段已存刪 1 段 → provider 1 次；只改 buffer → 0 次；
      改 mode → 非 override 全打、override 不打；`refresh=True` → 全打。
- [x] `test_integration_postgres_redis.py`：更新「編輯後會排程」的斷言。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_trip_route_tasks.py tests/test_trip_route_planner.py
```

本機有 Postgres + Redis 時：`RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_integration_postgres_redis.py -k routing`。

線上：建一趟 3 站的日本 AI 草稿 → 記下 Redis `provider-usage:ekispert:<YYYY-MM>` →
改第 2 站地點 → 按查路 → 計數只 +2；再改緩衝 → 計數不變。

## Notes

- override 段用 `saved.preference` 自己比，不跟當天設定比：面板套用時帶的是 trip 層 preference，
  和日層可能不同，否則每次整天重算都會重打 override 段。
- 「重用」需要 `2026-09-06-route-cache-time-key` 的長 TTL，否則 15 分鐘後全部過期又會重打。
- 前端配合（不清整天、距離估計、refresh=false）在 `2026-09-06-route-editor-partial-invalidation`。
- `test_integration_postgres_redis.py` 沒有任何「編輯後會排程」的斷言（grep `queued` 為空），所以不用改；
  三處 `unexpected_enqueue` 都是建立流程，行為不變。
- 「重用」與「不 enqueue」放在同一張 api 任務，前端任務不再碰 `router.py`。
