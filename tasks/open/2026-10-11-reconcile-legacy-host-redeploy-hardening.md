---
id: 2026-10-11-reconcile-legacy-host-redeploy-hardening
title: 對帳並恢復舊主機redeploy備份與rollback安全缺口
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:18:55Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-legacy-host-redeploy-hardening.md
---

## Why

Sep14一次部署收据已完成，局部未共享票指出舊host腳本可能帶dirty source、跳過無migration backup、mutable tags令rollback重建同壞版。當前repo不存在原scope manual-deploy.sh，不能把歷史主機狀態直接當現況。

## Done when

讀取實際安裝入口/version及main對應driver後，對每一舊缺口列已替代或具體仍需修正；真正缺口保留窄implementation票及測試契約，完成收據封存不混入未發布文章。

## Steps

只讀對帳clean pinned green input、baseline、每次部署fresh verified backup及舊image digestrollback；引用現在程式證據；若未修，另窄claim實作及disposable failure測試。

## Verification

以假docker/git/pgdump/pgrestore實證backup-before-change、reject dirty/unverified input、rollback使用舊image；歷史pg_restore --list不是full restore drill。

## Notes

原branch codex/redeploy-20260914 HEAD 434fc41292b7530f006d6ff29f93c4655aa5deea；a4ee0f507部署及backup hash是日期收據，不是這輪正式站驗收。原claims保持。

建票時scope只含本對帳票；預定實作範圍（完成owner/同義票核對後擴scope或拆窄票）：
- `ops/deployer/README.md`
- `主機實際manual redeploy入口（先read-only定位；目前repo無manual-deploy.sh）`

原始保留分支／核對HEAD：
- `codex/redeploy-20260914@434fc41292b7530f006d6ff29f93c4655aa5deea`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。

本票scope只含這份對帳紀錄；需要實作時先查owner及重複票，再擴成精確可claim路徑或另開窄實作票。
