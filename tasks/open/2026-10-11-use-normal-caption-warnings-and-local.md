---
id: 2026-10-11-use-normal-caption-warnings-and-local
title: Use normal caption warnings and local bindings in imported language submission
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:18:58Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-use-normal-caption-warnings-and-local.md
  - docs/videos/imported-long-languages/runner.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
---

## Why

129Japanesecue ordinarypass+3readingwarnings卻被private分類為missing，native submitSnapshot local/remoteproject混用；privateworkaround尚未shared regression。

## Done when

- [ ] ordinaryreadingwarnings不變missing，invalidcaption仍拒絕
- [ ] renewal用sourceboundlocalproject，ownerremoteauthority分開

## Steps

- [ ] 持久化原票，對現在runner函式核對回歸範圍
- [ ] 用zero-model caption/localprojectfixtures測試，不動UNKNOWN

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-08-use-normal-caption-warnings-and-local`。

原始保留分支／核對HEAD：
- `codex/stalled-videos-completion-20261008@b9940f18c1dfed8b493ceb9778df4c845728d4e2`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
