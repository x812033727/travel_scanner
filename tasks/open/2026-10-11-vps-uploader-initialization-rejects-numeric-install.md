---
id: 2026-10-11-vps-uploader-initialization-rejects-numeric-install
title: VPS uploader initialization rejects numeric install owner on production host
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T14:18:58Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-vps-uploader-initialization-rejects-numeric-install.md
  - docs/videos/VPS-UPLOADER.md
---

## Why

setup實際install -o10001拒绝host不存在的numeric account；frozenmain runbook仍有install -d -m0700 -o10001 -g10001以及copy -o10001。兩處無修。原setup code無產品diff，這個欠缺票僅舊ref。

## Done when

- [ ] containerUID不存在host passwd時first-install仍可跑
- [ ] private目錄、UID1000/10001讀權與已存在文件拒絕不變

## Steps

- [ ] 將原票持久化共享main
- [ ] 用普通install建立再以chown +10001:+10001（service +1000:+1000）明確給numeric UID，保持mode
- [ ] Linux臨時非secretfixture驗stat；勿重跑或rotate已存在正式credentials

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-01-vps-uploader-initialization-rejects-numeric-install`。

原始保留分支／核對HEAD：
- `codex/vps-uploader-setup-20261001@4bc6154d549eff183d5ad70b4f40b81ab691d018`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
