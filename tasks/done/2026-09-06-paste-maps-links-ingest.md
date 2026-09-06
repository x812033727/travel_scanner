---
id: 2026-09-06-paste-maps-links-ingest
title: 貼 Google Maps 連結加景點（待安排 inbox）
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T11:40:37Z
created_at: 2026-09-06T02:24:52Z
completed_at: 2026-09-06T11:41:06Z
branch: claude/trip-place-inbox
depends_on: []
scope:
  - apps/api/app/trips/ingest.py
  - apps/api/app/trips/ingest_router.py
  - apps/api/app/restaurants/imports.py
  - apps/api/migrations/versions
  - apps/web/components/trip-inbox-panel.tsx
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/tests/test_trip_place_ingest.py
  - apps/web/components/trip-inbox-panel.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 貼 Google Maps 連結加景點（待安排 inbox）

## Why

`docs/planning-flow-spec.md` §1 步驟 6 與 §6 PR 7／PR 8。去趣最受好評的能力是「貼連結就能加景點」，
而我們七成的零件已經在了：`resolve_maps_input()`（`apps/api/app/restaurants/imports.py:101`）
會展開短網址、驗 15 個主機白名單、抽 Place ID，目前只在後台商家來源匯入（`admin_sources_router.py:136`）被呼叫一次。

規格另外指出這是修好意圖列「候選用盡」的關鍵：`_load_ai_planner_candidates` 只拉 40 景點＋20 店家，
而且目的地不在 33 個目錄內就回空陣列；使用者貼進來的地點若進入候選集，兩個限制都解開。

## Definition of done

- [x] 使用者在行程頁貼一段 Google Maps 連結或地名，每一筆落在「待安排」inbox（是候選，不是決定）。
- [x] 解析到的 Place ID 若對到 `TravelHotspot.google_place_id`，換成目錄裡的完整記錄（深度分數、導覽、五語系名）。
- [ ] inbox 列可以被拖進日欄，也能被意圖列／AI 生成當候選使用，且 apply 不會 409。

## Steps

- [x] 遷移：`trip_place_candidates` 表（真表，不是快取——apply 會從資料庫重算候選簽章）。
- [x] `POST /trips/{id}/places/ingest`：批次解析，套區域守衛與配額（規格 §7 Q4 要先定數字：建議 30 行/批、100 地點/人/天）。
- [ ] `_load_trip_candidates()` 包住 `_load_ai_planner_candidates` 並附加 `kind="inbox"` 候選；
      **所有**候選載入點（preview／generate／apply／intents）一次切換，否則 apply 的簽章比對會 409。
      `AIPlannerCandidate.kind` 的 Literal 要放寬；`_replaceable_ai_items` 需要 `generated_by` 標記與 `candidate_key`。
- [x] `apps/web/components/trip-inbox-panel.tsx`：貼上 sheet ＋ 日欄旁的 inbox rail。
- [ ] `is_durable_coordinate_source` 加 `scope: Literal["catalog","trip"]`：Google 座標對行程項目算耐久，對 `TravelHotspot` 永遠不算。

## How to verify

貼 3 條 `maps.app.goo.gl` 短網址＋2 個地名 → inbox 出現 5 筆，其中對到目錄的顯示目錄名稱與導覽；
把一筆拖進第二天 → `PUT /itinerary` 成功；再用意圖列精修該日 → diff 出現 inbox 候選且 apply 200。

## Notes

規格明說這是「PR 1 之後風險最高的一張」：候選簽章不一致會讓每一次 apply 都 409。先拆成
「只匯入」（PR 7）與「進候選集」（PR 8）兩個 PR。Place ID 額度：短網址展開＋文字搜尋都算，
每月 Enterprise 額度緊，配額數字要在合併前定案。iOS 沒有 share target，這裡先做貼上框。

2026-09-06 claude-opus-5：**做完任務 Notes 說的 PR 7（只匯入），PR 8（進候選集）另開票**
（`2026-09-06-paste-inbox-into-candidates`）。Notes 自己說「候選簽章不一致會讓每一次 apply 都 409」，
那一半值得自己一個 PR 與自己的整合測試，不該跟匯入綁在一起上線。

做完的部分：

- 遷移 `0049_trip_place_candidates`＋`TripPlaceCandidate` 模型（真表，status 有 CHECK 約束，
  `(trip_plan_id, status)` 有索引），`hotspot_id` 對到目錄時 `ON DELETE SET NULL`。
- `apps/api/app/trips/ingest.py`：`split_lines`／`parse_line`／`hotspots_by_place_id`／`candidate_from`。
  連結交給既有的 `resolve_maps_input`（15 個 Google 主機白名單、短網址展開、Place ID 抽取），
  純文字就當成地名留著。**一次 Places 請求都沒有花**：解析到的 Place ID 只拿去比對我們自己的
  `travel_hotspots.google_place_id`，對到就帶著目錄的五語系名稱（`load_hotspot_names`）、座標、
  深度分數進來；對不到就保留使用者貼的字。要 Google 幫忙認出剩下的每一行都要付一次錢，所以不做。
- `POST /trips/{id}/places/ingest`、`GET /trips/{id}/places`、`DELETE …/{id}`、`POST …/{id}/used`。
  **配額定案**（規格 §7 Q4 要的數字）：一次最多 30 行（`MAX_LINES_PER_PASTE`），
  每人每天 100 個地點（`DAILY_PLACE_LIMIT`，Redis 計數，**在展開短網址之前**逐行扣，
  所以超長的貼上不會先花掉一堆外連請求再被擋）。
- 前端 `trip-inbox-panel.tsx` 掛在行程工具面板：貼上框、待安排清單、每列「加到這一天」與移除。
  **加進去成功之後才**呼叫 `/used` 並從清單移除，儲存失敗時貼上的東西不會消失。
  對到目錄的列會顯示「目錄景點 · 城市」。

沒有勾的三項：

- 「拖進日欄」做成了按鈕（加到目前選取的那一天），不是拖放。行程編輯器現有的拖放是同一天內排序，
  跨元件拖放要動 `planner-itinerary-card` 的 drag 來源與 drop 目標，屬於 PR 8 的範圍。
- `_load_trip_candidates()` 與 `is_durable_coordinate_source` 的 `scope` 參數是 PR 8。
