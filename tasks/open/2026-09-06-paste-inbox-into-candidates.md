---
id: 2026-09-06-paste-inbox-into-candidates
title: 待安排地點進入 AI 候選集（PR 8）
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T11:40:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/intents.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/trips/ingest.py
  - apps/web/components/trip-inbox-panel.tsx
  - apps/web/components/trip-editor.tsx
---

# 待安排地點進入 AI 候選集（PR 8）

## Why

`2026-09-06-paste-maps-links-ingest` 已經把貼上的地點存進 `trip_place_candidates`（PR 7，2026-09-06 落地）。
還缺的是規格 §6 PR 8：讓那些地點變成 AI 與意圖列的**候選**，這樣「候選用盡」與「目的地不在 33 個目錄內」
兩個限制都會鬆開。

原任務的 Notes 說得很清楚：這是「PR 1 之後風險最高的一張」，因為候選簽章不一致會讓每一次 apply 都 409。

## Definition of done

- [ ] `_load_trip_candidates()` 包住 `_load_ai_planner_candidates`，把 inbox 列以 `kind="inbox"` 附加進去。
- [ ] **所有**候選載入點（preview／generate／apply／intents）一次切換，apply 的簽章比對不會 409。
- [ ] `AIPlannerCandidate.kind` 的 Literal 放寬；`_replaceable_ai_items` 有 `generated_by` 標記與 `candidate_key`。
- [ ] `is_durable_coordinate_source` 加 `scope: Literal["catalog","trip"]`：
      Google 座標對行程項目算耐久，對 `TravelHotspot` 永遠不算。
- [ ] 整合測試：貼 3 個地點 → 意圖列精修該日 → diff 出現 inbox 候選 → apply 200（不是 409）。
- [ ] 待安排清單可以拖進日欄（PR 7 只做了「加到這一天」按鈕）。

## Steps

- [ ] 先寫「apply 不 409」的整合測試，再改候選載入。
- [ ] `trip_place_candidates.status` 在被 AI 採用時也要變 `used`，否則同一個地點會一直出現在候選裡。
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
