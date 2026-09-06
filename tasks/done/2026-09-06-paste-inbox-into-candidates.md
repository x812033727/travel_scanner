---
id: 2026-09-06-paste-inbox-into-candidates
title: 待安排地點進入 AI 候選集（PR 8）
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T13:02:00Z
created_at: 2026-09-06T11:40:40Z
completed_at: 2026-09-06T13:02:02Z
branch: claude/inbox-candidates
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/intents.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/trips/ingest.py
  - apps/web/components/trip-inbox-panel.tsx
  - apps/web/components/trip-editor.tsx
  - apps/api/app/locations/coordinates.py
  - apps/api/tests/test_trip_place_ingest.py
  - apps/api/tests/test_coordinate_scope.py
  - apps/api/tests/test_integration_postgres_redis.py
---

# 待安排地點進入 AI 候選集（PR 8）

## Why

`2026-09-06-paste-maps-links-ingest` 已經把貼上的地點存進 `trip_place_candidates`（PR 7，2026-09-06 落地）。
還缺的是規格 §6 PR 8：讓那些地點變成 AI 與意圖列的**候選**，這樣「候選用盡」與「目的地不在 33 個目錄內」
兩個限制都會鬆開。

原任務的 Notes 說得很清楚：這是「PR 1 之後風險最高的一張」，因為候選簽章不一致會讓每一次 apply 都 409。

## Definition of done

- [x] `_load_trip_candidates()` 包住 `_load_ai_planner_candidates`，把 inbox 列以 `kind="inbox"` 附加進去。
- [x] **所有**候選載入點（preview／generate／apply／intents）一次切換，apply 的簽章比對不會 409。
- [x] `AIPlannerCandidate.kind` 的 Literal 放寬；`_replaceable_ai_items` 有 `generated_by` 標記與 `candidate_key`。
- [x] `is_durable_coordinate_source` 加 `scope: Literal["catalog","trip"]`：
      Google 座標對行程項目算耐久，對 `TravelHotspot` 永遠不算。
- [x] 整合測試：貼 3 個地點 → 意圖列精修該日 → diff 出現 inbox 候選 → apply 200（不是 409）。
- [ ] 待安排清單可以拖進日欄（PR 7 只做了「加到這一天」按鈕）。

## Steps

- [x] 先寫「apply 不 409」的整合測試，再改候選載入。
- [x] `trip_place_candidates.status` 在被 AI 採用時也要變 `used`，否則同一個地點會一直出現在候選裡。
- [ ] 拖放：`trip-inbox-panel.tsx` 的列設 `draggable`，日欄的 `<li>` 接 `onDrop`。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trip_intents.py tests/test_ai_itinerary.py -q
```

貼 3 條 `maps.app.goo.gl` 短網址 → inbox 出現 3 筆 → 用意圖列精修該日 → diff 出現 inbox 候選且 apply 200。

## Notes

PR 7 的成果：`app/trips/ingest.py`（解析與比對，不花 Places 額度）、`app/trips/ingest_router.py`
（配額 30 行/次、100 地點/人/天）、`TripPlaceCandidate` 模型與 `0049_trip_place_candidates`、
前端 `trip-inbox-panel.tsx`。候選列已經帶著目錄的五語系名稱與座標，所以 PR 8 不需要再查一次資料。

2026-09-06 claude-opus-5：

- `_load_trip_candidates(session, trip, ...)` 包住 `_load_ai_planner_candidates`，把待安排列以
  `kind="inbox"`、key `inbox:<id>` 附加在後面。**三個 trip 範圍的載入點一次全換**
  （`/itinerary/preview`、deprecated 的 `/itinerary/generate`、`/itinerary/apply`）；
  建立行程那一個沒換，因為那時候還沒有 trip、也就沒有待安排清單。
- 順序是固定的（`created_at`, `id`），preview 與 apply 因此建出同一份清單，
  `_candidate_signatures` 的比對才有意義——那正是這張票警告的 409 風暴來源。
  整合測試 `test_a_pasted_place_can_be_offered_by_the_planner_and_applied_without_a_conflict`
  貼一個地點 → preview → apply，**斷言不是 409**。
- `AIPlannerCandidate.kind` 放寬成 `hotspot | merchant | inbox`；`_ordered_hotspots`
  與模型草稿的活動時段驗證都改成 `kind in {"hotspot", "inbox"}`；意圖列的「還有沒有別的選擇」
  也把待安排列算進去（`intents.py` 的 `hotspots`）。日歸與跨城那兩個判斷維持只看 `hotspot`：
  待安排列沒有 `depth_kind`，本來就不會是那種行程。
- `generated_by` 與 `candidate_key` 早就寫在項目的 `data` 裡（`ai/itinerary.py`），
  `_replaceable_ai_items` 不需要再補。apply 寫完之後 `_retire_used_inbox_rows` 把被採用的列改成
  `used`，否則同一個地點會一直出現在候選裡。
- **關鍵的一步：貼進來的地點現在多半自己就有座標。** `coordinates_from_maps_url()` 從 Google Maps
  網址讀 `!3d/!4d`（圖釘）或 `@lat,lng`（地圖中心），一毛錢都不用花。原本只有對到目錄的列有座標，
  等於候選集還是被 33 個城市的目錄綁著；現在只要連結帶著圖釘，沒對到目錄的地點也能被規劃。
  沒有座標的列仍留在清單裡等使用者自己放——要幫它們定位就得對每一行打一次 Place Details，
  那是這張票刻意不做的事。
- `is_durable_coordinate_source(..., scope="catalog" | "trip")`：`trip` 多接受
  `google_places` 與 `user_paste`。目錄一個錯的圖釘是發給所有人看、而且會活得比加它的人久；
  行程裡一個錯的圖釘只花掉那位旅客一趟路。預設仍是 `catalog`，既有兩個呼叫端行為不變。

沒有勾的一項：**待安排清單還是「加到這一天」按鈕，不是拖放**。清單目前住在工具面板的
`PlannerOverlay`（modal）裡，而 modal 蓋在日欄上面——從蓋住畫面的東西拖到它底下的清單並不成立。
要做拖放得先把它從 modal 改成日欄旁的 rail，那是版面改動，值得自己一張票。
