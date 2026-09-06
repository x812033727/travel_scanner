---
id: 2026-09-06-route-optimizer-estimates
title: 最佳化用距離估計排順序、系統卡變更只作廢碰到的路段、步行汽車不看偏好
status: done
priority: P1
area: api
owner: claude-fable-5.1
claimed_at: 2026-09-06T03:35:09Z
created_at: 2026-09-06T03:35:06Z
completed_at: 2026-09-06T05:05:12Z
branch: claude/route-optimizer-estimates
depends_on:
  - 2026-09-06-route-recompute-reuses-saved-segments
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/routing.py
  - apps/api/app/trips/route_tasks.py
  - apps/api/app/trips/schedule.py
  - apps/api/app/trips/stay_router.py
  - apps/api/tests/test_trip_routing.py
  - apps/api/tests/test_trip_optimization_preview.py
  - apps/api/tests/test_trip_route_tasks.py
  - apps/api/tests/test_trip_schedule.py
  - apps/api/tests/test_trip_stay_router.py
---

# 最佳化用距離估計排順序、系統卡變更只作廢碰到的路段、步行汽車不看偏好

## Why

再確認三個路線 PR 之後的流程，還有三條路徑會不必要地打 provider：

1. **最佳化的 N×N 矩陣**：`plan_itinerary_optimization` 對每一對可移動地點都呼叫
   `compute_many`，而且 `travel_mode` 沒傳、預設 transit → 日本每一對都是一次 Ekispert。
   6 站 = 30 次、12 站 = 132 次，一次點擊就吃掉月額度的 7% 到 30%。
2. **系統卡變更整趟清空**：`persist_system_schedule_change` 把整趟（或整天）的
   `trip_route_segments` 全部刪掉再排整趟重算。換主要飯店只動每天頭尾兩段、
   改每日出發時間根本沒動到任何一段的端點、跳過午餐只動它前後兩段，卻全部重打。
3. **步行／汽車也比 preference**：`_reusable_segment` 對非 transit 的段也比 preference，
   但 Google 步行／汽車請求根本不帶 preference，白白重打。

順手抓到一個原本就壞的地方：最佳化把新順序交給 `compute_routes_for_rows` 後，
`active_route_rows` 又依 `position` 排回原順序，所以預覽拿到的路段一直是**舊順序**的，
apply 時 `by_pair` 對不到新順序的 pair，時間也沒被重推。

## Definition of done

- [x] 最佳化的成對矩陣改用直線距離估計（與前端 `estimateLegMinutes` 同一組數字），
      只有提議出來的那條鏈才真的查路，且用當天預設交通方式與緩衝。
- [x] 提議的鏈依新順序查路（`compute_routes_for_rows(..., ordered=True)`）。
- [x] 換飯店只作廢碰到飯店卡的段；改每日時間不作廢任何段；跳過／恢復餐食只作廢
      碰到那張卡的段。剩下的段交給 worker 重用。
- [x] 步行／汽車的段不因 preference 不同而重打。
- [x] `apps/api` 的 ruff / mypy / pytest 通過。

## Steps

- [x] `routing.py`：`estimate_leg_minutes(origin, destination, travel_mode)`。
- [x] `router.py`：最佳化改吃估計矩陣、依當天設定查鏈；`_adjacent_pairs` 提到模組層，
      新增 `stale_route_pairs`；`persist_system_schedule_change` 多收 `changed_item_ids`。
- [x] `schedule.py`：`sync_primary_lodging` 回傳有變動的飯店卡 id；`stay_router.py` 與
      `router.py` 的三個呼叫點傳入。
- [x] `route_tasks.py`：`_reusable_segment` 只在 transit 比 preference。
- [x] 測試：`test_trip_optimization_preview.py` 改用座標、斷言只查兩段且依新順序；
      `test_trip_route_tasks.py` 補 `stale_route_pairs` 與步行不比 preference；
      `test_trip_routing.py` 補估計值；`test_trip_schedule.py`／`test_trip_stay_router.py`
      斷言回傳的 id。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_trip_optimization_preview.py tests/test_trip_route_tasks.py tests/test_trip_routing.py tests/test_trip_schedule.py tests/test_trip_stay_router.py
```

線上：一趟 6 站的日本行程按「最佳化」→ Redis `provider-usage:ekispert:<YYYY-MM>` 只 +5
（鏈的五段），不是 +30；換主要飯店後按查路 → 每天只 +2。

## Notes

- 最佳化預覽的「預計節省 X 分」現在是估計值對估計值（前後都用同一套直線估計），
  提議順序的每段路線仍是 provider 真值；套用後按查路會用 Redis 快取，不再多花額度。
- 改每日出發時間後大眾運輸班次理論上會不同，但依產品決定先沿用舊路段的時間當估計，
  要精確就按「重新查詢可用路線」或當天查路（會 refresh）。
- `persist_system_schedule_change` 沒傳 `changed_item_ids` 時維持整趟清空，
  給還沒改的呼叫端用；目前四個呼叫端都已傳。
