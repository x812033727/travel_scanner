---
id: 2026-09-06-intent-route-segment-cascade
title: 意圖精修刪除列時連帶清掉使用者輸入的交通時間
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:09:38Z
created_at: 2026-09-06T00:55:20Z
completed_at: 2026-09-06T03:25:12Z
branch: claude/intent-bar-fixes
depends_on:
  - 2026-09-06-intent-diff-mismatch
scope:
  - apps/api/app/trips/replan.py
---

# 意圖精修刪除列時連帶清掉使用者輸入的交通時間

## Why

這是 `2026-09-06-intent-diff-mismatch` 修完之後**還會剩下**的一層，值得單獨記錄，
因為它示範了那個 bug 真正的形狀。

第一版問題是「diff 說某列沒變，但 apply 會覆寫它的欄位」。修法是把使用者的欄位值帶到重建後的列上。
複查發現這樣還不夠：

**那一列仍然被 DELETE 再 INSERT，而 `trip_route_segments.from_item_id` / `to_item_id` 是
`ON DELETE CASCADE`。** 所以使用者手動輸入的交通時間（以及掛在該路線段上的其他資料）
會跟著被刪掉 —— 而 diff 說這一列「維持不變」。

修法只把問題往下沉了一層：帶欄位值不等於保住列的身分。

## Definition of done

- [x] 一次精修之後，diff 標為「維持不變」的列保有原本的 id，因此它的 `trip_route_segments` 還在。
- [x] 使用者手動覆寫過的交通時間在精修後仍然存在。
- [x] 有測試會在「被標為不變的列遭到刪除」時失敗。

## Steps

- [x] 確認範圍：除了 `trip_route_segments`，還有哪些東西以 `trip_plan_items.id` 為外鍵，
      會跟著 cascade 一起消失。
- [x] 讓真正沒有變動的列保留原 id，而不是刪除重建。
- [x] 如果有某些情況真的無法保住身分，那 diff 就不能說它「維持不變」，
      必須明說「已計算的交通時間會遺失」。保住身分是比較好的答案，先試那個。
- [x] 加回歸測試。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_intents.py
```

手動：在某一天的兩個景點之間手動覆寫交通時間，對同一天做一次不會動到那兩個景點的精修，
套用後確認那個交通時間還在。

## Notes

**2026-09-06 完成。** 以 `trip_plan_items.id` 為外鍵的只有 `trip_route_segments.from_item_id`／`to_item_id`
（兩者 `ON DELETE CASCADE`，`models.py` 約 1384 行）。`replan.reuse_rows()` 對 diff 標為不變的列（同日同時段、
沒有任何使用者可見欄位會被覆寫）原地更新——只換規劃器自己的 reason 與目錄中繼資料——保留原 id，
`_replan_records` 不再為這些列建新列；apply 端 `apply_trip_itinerary_preview` 只刪除真的被換掉的列。
回歸測試 `test_an_unchanged_stop_keeps_its_row_so_its_route_segments_survive` 斷言兩個未變的停留點
`reuse_rows` 回傳的是原物件、原 id，且 `_replan_records` 為空；`apply_and_check` 也對每個 reused pair 檢查快照不變。
沒有「保不住身分」的情況需要另外揭露：會動到的列一律進 moved／changed／removed，不會被算成不變。

出處：對 `wip/intent-bar-blocker-fixes` 的 round 1 修法所做的三路複查，
`no-loss` 這個審查者提出，嚴重度 high。原文（節錄）：

> A stop the sheet counts as unchanged is still DELETEd and re-INSERTed, and
> trip_route_segments.from_item_id/to_item_id are ON DELETE CASCADE — so a traveller's
> manually entered travel time and its note are destroyed by a refine the diff called unchanged.

複查同時提醒：修這個的時候要往外多看一層，還有沒有別的東西是以列 id 為鍵、會被 cascade 帶走的。

這張任務刻意與 `2026-09-06-intent-diff-mismatch` 分開，但兩者相依：
先把 diff 與 apply 對齊，再處理身分保留。scope 也刻意只寫 `replan.py`，
避免和上一張任務的 `intents.py` 重疊而互相擋住。
