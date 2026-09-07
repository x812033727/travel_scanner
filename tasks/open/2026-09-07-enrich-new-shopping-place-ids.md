---
id: 2026-09-07-enrich-new-shopping-place-ids
title: 30 筆新購物店家還沒 place enrichment，所以加不進行程
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-07T01:03:39Z
completed_at:
branch:
depends_on: []
scope:
  - ops/notes/hotspot-place-enrichment.md
---

# 30 筆新購物店家還沒 place enrichment，所以加不進行程

## Why

2026-09-07 上線後稽核發現。30 筆專門購物店家種子全部是 `map_match_status='unverified'`、
沒有任何一筆有 `hotspot_place_profiles`。**沒有任何自動流程會撿到它們**：

- `due_refresh_targets`（places.py）是 INNER JOIN `hotspot_place_profiles` 且要求
  `match_status in ('approved','auto_approved')`——完全沒有 profile 的列看不到。
- `refresh_due_map_place_ids`（service.py）要求 `google_place_id IS NOT NULL` 且
  `map_match_status='verified'`——同樣看不到。
- 線上 collector 每次都印 `place_enrichment: {'skipped': True, 'reason': 'nothing_due'}`。

唯一碰得到「沒有 profile」那些列的查詢是 `enrichment_targets`（outerjoin + `profile.id is null`），
而它只有一個呼叫端：後台的 `POST /admin/hotspots/place-enrichment/runs`。

實務後果：這 30 家店會出現在排行榜與主題篩選裡，但

- 按「加入行程」→ 404「找不到可加入行程的景點」（`router.py` 的 trip-selections 閘門）
- `/hotspots/recommendations` 的 `planner_ready` 把它們濾掉
- AI 規劃器的 `_planner_eligible` 把它們濾掉
- 卡片上沒有地圖連結

**最痛的一點：三筆 `outlet` 全部是新的**（東薈城、臨空城、多摩南大澤），所以行程表單選了
「Outlet」這個店型偏好，候選會是**零筆**。`electronics` 8 筆裡 7 筆新、`drugstore` 4 筆裡 2 筆新。

## Definition of done

- [ ] 30 筆都有 place profile，且該 verified 的已 verified。
- [ ] 選「Outlet」的行程能排進至少一家 Outlet。

## Steps

- [ ] 後台或 API：`POST /api/v1/admin/hotspots/place-enrichment/runs`，帶 `Idempotency-Key`，
      body `{"mode":"missing_or_expired","scope":"hotspots","hotspot_ids":[...],"confirm_usage":true}`。
- [ ] 跑完到 place-profiles 審核佇列把 pending 的比對清掉——`enrich_hotspot_place` 只有在候選
      自動核准時才自己把 `map_match_status` 設成 verified，其餘都等人。
- [ ] 韓國那 5 筆（icn-* ×4、pus-gukje-market）另外需要 NAVER 網址才過得了 `has_exact_map_identity`
      的 KR 規則——擋在 `2026-09-06-naver-maps-key` 後面，先跳過。

## How to verify

```sql
select h.slug, h.map_match_status, (h.google_place_id is not null)
from travel_hotspots h where h.slug like 'nrt-%' or h.slug like 'kix-%' ...;
```

行程表單選「購物」+「Outlet」，確認候選裡有 Outlet。

## Notes

- **這不是這批種子特有的問題**：全站 approved 景點有 126 筆是 unverified，30 筆只是加入了既有的
  待補清單。但 outlet 因為三筆全新，是唯一一個「整個店型都沒得選」的。
- **會花 Google Places 額度**：一列大約 2 次呼叫，30 列約 60 次。2026-09 這個月
  `hotspot_place_enrichment_runs` 已經累計 estimated 1,898 次呼叫 / 1,190 個目標，
  免費額度是 1,000/月（見 [[travel-scanner-hotspot-place-ids]]），所以**動手前要先確認費用**。
- 只有後台那條路徑碰得到這些列，所以這是營運動作，不是程式問題。
