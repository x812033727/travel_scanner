---
id: 2026-10-11-video-stage-receipt-site-identity
title: Preserve stage receipt identity across public and internal video worker transport
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:18:58Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-video-stage-receipt-site-identity.md
  - tools/video/automation/client.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/client.test.mjs
  - ops/video/worker.sh
---

## Why

相同receipt/publicCLI=https mokaair vs normalinternal=http web3000會identity拒絕；CF/SEC actualnativepublic[] internalthrows。main票缺；原receipt/sitehash不能無條件放寬。

## Done when

- [ ] 同logicalsite兩transport接受既有receipts但changedsite/source/request/result仍failclosed
- [ ] zero-newPOST完成/UNKNOWNkeys，migration不implicitarchive/重買

## Steps

- [ ] 持久化原P1票与actualreadonlyreprosource/hash
- [ ] fakepublic↔internalclock/transportcases後審stablelogicalsitebinding；不呼叫正式retry

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-09-video-stage-receipt-site-identity`。

原始保留分支／核對HEAD：
- `codex/stalled-videos-completion-20261008@b9940f18c1dfed8b493ceb9778df4c845728d4e2`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
