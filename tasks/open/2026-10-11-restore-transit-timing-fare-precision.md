---
id: 2026-10-11-restore-transit-timing-fare-precision
title: 補回交通步行秒數與未知票價精度待辦
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T14:18:53Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-transit-timing-fare-precision.md
  - apps/api/app/trips/routing.py
  - apps/api/tests/test_trip_routing.py
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/components/route-segment-card.tsx
  - apps/web/components/route-segment-card.test.tsx
  - apps/web/lib/trip-types.ts
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
---

## Why

原precision/fare票僅在codex/seoul-day2-transport-ux@abdd425422a522f1e80d538025d571054b7c8864，main不存在。原#387 release完成，但2026-10-11 main仍per-step最低1分鐘合計與_money({})=0/nullcurrency，導致walking超過total及裸0票價。

## Done when

- [ ] 以source seconds合計／排序後round，subminute五語表達誠實。
- [ ] missing/invalid money=unavailable，verified zero＋可靠currency可區分。
- [ ] deterministic backend/UI fixtures與preview/apply回歸通過。

## Steps

保留seconds、相容舊persisted JSON；修排名与UIsummary；驗money shape與currency，不能只clamp walking總數。

## Verification

24×20秒=8分鐘、缺fare／空object／缺currency／zeroKRW／一般KRW fixtures；pytest、Ruff/mypy、component tests、types/i18n、desktop/mobile synthetic browser。

## Notes

原raw Google fare未保留，空object是支持機制而非當日response證明。原trip未apply，保留v8/33item/0route記錄；不查新付費provider、不啟用Maps/改key/改正式trip。

原始保留分支／核對HEAD：
- `codex/seoul-day2-transport-ux@abdd425422a522f1e80d538025d571054b7c8864`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
