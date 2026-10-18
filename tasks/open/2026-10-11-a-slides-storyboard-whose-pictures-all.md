---
id: 2026-10-11-a-slides-storyboard-whose-pictures-all
title: Decide automatic storyboard approval for a passing picture with a nonblocking judge note
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T14:18:59Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-a-slides-storyboard-whose-pictures-all.md
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
  - docs/videos/ILLUSTRATED.md
---

## Why

main storyboard_check_passed still拒绝普通shot verdict.problems非空；#1341 accepted-best例外只對accepted:true，不處理已passed高分但nonblocking note的77/77情況。原owner policy票main缺。

## Done when

- [ ] 由產品owner確定passed+nonblocking-note是否自動接受；若仍manual則label/docs如實寫
- [ ] 完整expected_shots/file hashes coverage不弱化
- [ ] rule/test/docs同一decision

## Steps

- [ ] 持久化原policy票，附56/77note資料與#1203原因
- [ ] 先decision再窄改規則或label/docs，不替owner批准影片

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-04-a-slides-storyboard-whose-pictures-all`。

原始保留分支／核對HEAD：
- `claude/ai-terminology-video-series-c1754d@92e3ae6ba64b75243b6127da2c09d4b96470f0c5`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
