---
id: 2026-10-11-retain-existing-guide-packs-in-imported
title: Retain existing guide packs in imported language runtime snapshots
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:18:57Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-retain-existing-guide-packs-in-imported.md
  - docs/videos/imported-long-languages/package-runtime.mjs
  - docs/videos/imported-long-languages/prepare.test.mjs
---

## Why

12個已付費translation/review後runtime漏已存在content pack，private複製原字節修好；branch/sharedmain票缺。

## Done when

- [ ] selectedsourceguide既有pack+hash入snapshot
- [ ] missing/stalepreflight先拒絕，不import別的packs/secrets

## Steps

- [ ] 原ticket/pack2952f35f SHA持久化；與#1359/runner繼任scope協調
- [ ] 不dispatchfixture載入runtime

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-08-retain-existing-guide-packs-in-imported`。

原始保留分支／核對HEAD：
- `codex/stalled-videos-completion-20261008@b9940f18c1dfed8b493ceb9778df4c845728d4e2`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
