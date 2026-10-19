---
id: 2026-10-11-make-durable-polling-deadline-regression-deterministic
title: Make durable polling deadline regression deterministic
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:18:57Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-make-durable-polling-deadline-regression-deterministic.md
  - tools/video/automation/client.test.mjs
---

## Why

實際Windows concurrentdeadline224ms只lookup1次而預期2，main沒有該票；目前仍有wallclock控制，不應延長timeout假修。

## Done when

- [ ] answered/unanswered/refused/losttransport受controlledclock測試
- [ ] production polling/paid receipt語意不改

## Steps

- [ ] 先核對 main已加長25秒的測試是否已充分消除原負載flake；若只是重複歷史問題則不用新改。
- [ ] 持久化原票，用既有注入clock/sleep deterministicfixture
- [ ] focusedWindows/Linux client tests

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-08-make-durable-polling-deadline-regression-deterministic`。
- frozen main test的成功lookup case已用durablePollMs/durablePollIntervalMs=25000並註明先前40ms window；不宣稱現在仍紅。先按該修訂重新判斷必要性，再決定controlled clock是否值得獨立P3。

原始保留分支／核對HEAD：
- `codex/stalled-videos-completion-20261008@b9940f18c1dfed8b493ceb9778df4c845728d4e2`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
