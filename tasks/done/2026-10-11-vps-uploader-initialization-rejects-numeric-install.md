---
id: 2026-10-11-vps-uploader-initialization-rejects-numeric-install
title: VPS uploader initialization rejects numeric install owner on production host
status: done
priority: P2
area: docs
owner: codex-open-tasks-uploader-doc
claimed_at: 2026-10-24T16:14:34Z
created_at: 2026-10-11T14:18:58Z
completed_at: 2026-10-24T16:21:39Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tasks/open/2026-10-11-vps-uploader-initialization-rejects-numeric-install.md
  - docs/videos/VPS-UPLOADER.md
---

## Why

setup實際install -o10001拒绝host不存在的numeric account；frozenmain runbook仍有install -d -m0700 -o10001 -g10001以及copy -o10001。兩處無修。原setup code無產品diff，這個欠缺票僅舊ref。

## Done when

- [x] containerUID不存在host passwd時first-install仍可跑
- [x] private目錄、UID1000/10001讀權與已存在文件拒絕不變

## Steps

- [x] 將原票持久化共享main
- [x] 用普通install建立再以chown +10001:+10001（service +1000:+1000）明確給numeric UID，保持mode
- [x] Linux臨時非secretfixture驗stat；勿重跑或rotate已存在正式credentials

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-01-vps-uploader-initialization-rejects-numeric-install`。

原始保留分支／核對HEAD：
- `codex/vps-uploader-setup-20261001@4bc6154d549eff183d5ad70b4f40b81ab691d018`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。


### 2026-10-24 coordinator acceptance

Current host isolated nonsecret fixture confirmed uutils coreutils0.8.0 with UID/GID1000 and10001 absent from NSS. Original init and isolated numeric copy step each actualexit1(invalid user10001), correcting the assumption that GNU behavior applies to this host. Candidate first-install actualexit0: five ownership/mode stats, two expected UID reads and four cross/unrelated UID denials passed; three existing-file guards and full repeated setup refused with exit1 and preserved bytes. UID read checks model separate bind-mounted files via root-selected cwd/hardlinks; live Docker mounts were not changed or tested. All owned temporary fixtures removed and absence verified. External patch LF git-apply check actual0; failed WSL probe/initial CRLF patch check retained. Independent reviewer codex-root-independent-uploader-doc-review-20261025 reconstructed exactly three command substitutions, preserving all other document bytes, guards,modes,paths and entropy generation. Source44a8d04243720b33eff7fa63e2a478beececb35e6cefb6f65b150f934880b918 -> installedf71402f13aaf6723fdbc05a576d26750a5d850f854eb7c6f1c64d00080112913 readback matched. No real credentials,accounts,uploader settings or containers changed. Local runbook fix; merge remains separate.
