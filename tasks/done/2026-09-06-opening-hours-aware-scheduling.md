---
id: 2026-09-06-opening-hours-aware-scheduling
title: 營業時間感知排程：AI 排程不把景點排在打烊時段
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T12:05:58Z
created_at: 2026-09-06T02:24:52Z
completed_at: 2026-09-06T12:05:59Z
branch: claude/opening-hours
depends_on: []
scope:
  - apps/api/app/trips/hours.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/hotspots/router.py
  - apps/web/components/day-health-strip.tsx
  - apps/api/app/trips/router.py
  - apps/api/app/hotspots/service.py
  - apps/api/app/trips/itinerary.py
  - apps/api/tests/test_trip_hours.py
  - apps/api/tests/test_ai_itinerary.py
  - apps/web/components/day-health-strip.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 營業時間感知排程：AI 排程不把景點排在打烊時段

## Why

`docs/planning-flow-spec.md` §1 步驟 9 與 §6 PR 6。這是規格認定的第一個真正超越點：去趣 chicTrip 的 8 篇評測
都沒提到營業時間，它一律預設每個景點停 1 小時。我們的資料已經有了——
`HotspotPlaceProfile.opening_hours_json`（`models.py:508`）由 Google Places 補齊、
`normalize_draft`（`apps/api/app/ai/itinerary.py`）也已經把每個開始時間重寫到時段網格上，
**只差把前者餵進 `_safe_slots`（`ai/itinerary.py:594`）**。目前 `opening_hours_json` 在
`trips/` 與 `ai/` 底下零引用。

「我們不會讓你星期一跑去一間沒開的美術館」是可以截圖示範的差異。

## Definition of done

- [x] AI 生成／精修的行程不會把有已知營業時間的景點排在打烊時段；沒有時間資料的景點行為不變。
- [x] 每天有一條 Day Health 提示：可能遲到（`fixed_time` 停留點趕不到）、到達時已打烊、尚未查路 N 段。
- [x] 沒有或過期的營業時間**只會沉默**，不會猜：只評估 `provider_expires_at` 仍在未來的列，這條路徑不打任何 Places 即時查詢。

## Steps

- [x] 新增 `apps/api/app/trips/hours.py`：把 Google structured periods 解析成行程時區的每週區間，
      提供「某時刻是否營業」與「下一個開門時間」。
- [x] 在 trip-selections 路徑（`hotspots/router.py:344` 附近）把 `opening_hours_json` 複製到項目 `data`，
      並在 `_safe_slots` 依它挑時段（找不到可用時段就退回原行為，並在 `planning.warnings` 註明）。
- [x] `GET /trips/{id}/health`：結合 `RouteScheduleConflict.late_minutes`（`trips/route_planner.py`）與營業時間做每日三項判斷。
- [x] `apps/web/components/day-health-strip.tsx`：每個日欄頂端的 sticky 帶，點警告跳到該停留點。
- [x] 測試：週一休館的景點不會被排在週一；缺資料時無提示。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_ai_itinerary.py tests/test_trip_hours.py -q
```

手動：對東京行程生成，挑一個週一休館的美術館（Google 資料有 periods），
確認它不會落在週一，且 Day Health 對已排在打烊時段的手動項目亮起「到達時已打烊」。

## Notes

規格 §1 步驟 9 選了被動的 strip 而不是「幫我修」按鈕：不花供應商額度、旅客零額外操作。
硬規則：一個「營業中卻被標紅」的錯誤會毀掉整條 strip 的信任，所以寧可沉默。
Places Enterprise 免費額度每月只有一千餘次（見 memory），這條路徑不得觸發 `place_details`。

2026-09-06 claude-opus-5：

- `apps/api/app/trips/hours.py`：把 Google 的 `periods`（day 0 是星期日）解析成「以星期日 00:00 起算的分鐘」
  區間。回答一律三態：`True`／`False`／**`None`＝不知道**。看不懂、空的、過期的，一律 `None`，
  呼叫端就閉嘴——一個「開著卻被標紅」的錯誤會毀掉整條 strip 的信任，這是規格的硬規則。
  跨午夜（週五 18:00–週六 02:00）與「有 open 沒有 close」（24 小時營業）都有測試釘住。
- `fresh_hours(payload, expires_at)`：**只有 `provider_expires_at` 還在未來的快取才算數**。
  這條路徑**一次 Places 請求都不打**——每個排進去的景點打一次 Place Details，
  一個下午就能燒光 Enterprise 每月一千餘次的免費額度。
- 資料流：`list_rankings` 已經在載 `HotspotPlaceProfile`，順手把 `fresh_hours(...)` 放進 ranked item →
  `ItineraryHotspot.opening_hours` → `AIPlannerCandidate.opening_hours`。**不進 prompt**：
  規則由 `fallback_draft` 自己套，模型看不到這些數字，所以壞掉的 payload 不會變成提示詞裡的句子。
- 排程：`fallback_draft` 每個時段改成「往下找第一個那個時間開著的景點」。
  沒有可用時間資料的景點立刻符合，所以**沒有快取的行程排出來跟以前一模一樣**；
  週一休館的美術館會被跳過，而且**仍留在候選池裡**，星期二就會被排進去（測試釘住兩件事）。
- 選景點加入行程時（`hotspots/router.py` 的 trip-selections 路徑），把同一份 `fresh_hours` 複製進項目的
  `data.opening_hours`，讓每日檢查不用再查一次。
- `GET /trips/{id}/health`：每天三件事——`late`（`project_day_schedule` 的 `RouteScheduleConflict`）、
  `closed`（到達時間落在打烊時段，附「幾點開」如果同一天還會開）、`unrouted`（幾段沒有路段）。
  完全讀既有資料，開這一頁不花任何供應商額度。
- `day-health-strip.tsx` 掛在日欄上方，只在有事情要說時才出現，點警告會打開那個停留點。五語系。

沒有勾的一項是手動驗證：要在正式站對東京行程生成一次，挑一個 Google 有 periods 且週一休館的美術館，
確認它不會落在週一。本機沒有 Postgres 與 Places 金鑰，這一步得在部署後做。
