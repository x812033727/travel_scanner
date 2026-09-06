---
id: 2026-09-06-opening-hours-aware-scheduling
title: 營業時間感知排程：AI 排程不把景點排在打烊時段
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T02:24:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/hours.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/hotspots/router.py
  - apps/web/components/day-health-strip.tsx
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

- [ ] AI 生成／精修的行程不會把有已知營業時間的景點排在打烊時段；沒有時間資料的景點行為不變。
- [ ] 每天有一條 Day Health 提示：可能遲到（`fixed_time` 停留點趕不到）、到達時已打烊、尚未查路 N 段。
- [ ] 沒有或過期的營業時間**只會沉默**，不會猜：只評估 `provider_expires_at` 仍在未來的列，這條路徑不打任何 Places 即時查詢。

## Steps

- [ ] 新增 `apps/api/app/trips/hours.py`：把 Google structured periods 解析成行程時區的每週區間，
      提供「某時刻是否營業」與「下一個開門時間」。
- [ ] 在 trip-selections 路徑（`hotspots/router.py:344` 附近）把 `opening_hours_json` 複製到項目 `data`，
      並在 `_safe_slots` 依它挑時段（找不到可用時段就退回原行為，並在 `planning.warnings` 註明）。
- [ ] `GET /trips/{id}/health`：結合 `RouteScheduleConflict.late_minutes`（`trips/route_planner.py`）與營業時間做每日三項判斷。
- [ ] `apps/web/components/day-health-strip.tsx`：每個日欄頂端的 sticky 帶，點警告跳到該停留點。
- [ ] 測試：週一休館的景點不會被排在週一；缺資料時無提示。

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
