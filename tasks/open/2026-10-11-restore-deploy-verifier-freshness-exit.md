---
id: 2026-10-11-restore-deploy-verifier-freshness-exit
title: 恢復部署驗證退出碼與重建時刻防護的共享追蹤
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:18:54Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-deploy-verifier-freshness-exit.md
---

## Why

歷史部署收據已完成，但唯一保留的防護票未進main；fresh main仍把video-worker StartedAt與HEAD commit時刻比較，且TOTAL有FAIL仍以最後echo成功結束。

## Done when

先確認沒有同義open票並引用原HEAD/收據；失敗時退出非零；同一已驗證部署/容器重建cutoff一致；保留非fatal的AI-drama disabled分類。

## Steps

只讀對帳原稿與當前main；正式實作前窄scope及claim；以假docker/git/date輸出重現FAIL退出0及HEAD早於重建的情況，再修正並驗證。

## Verification

離線shell fixture涵蓋PASS/FAIL退出碼、重建時刻、缺容器與AI-drama關閉；不重建正式容器來迎合驗證。

## Notes

原branch codex/news-publication-deploy-receipt HEAD 380e463ae785ac98b66eb4fc52dd13d9a6166549；#1201部署/13服務health收據是日期證據，不能當成目前主機健康。原claims不釋放。

建票時scope只含本對帳票；預定實作範圍（完成owner/同義票核對後擴scope或拆窄票）：
- `.agents/skills/deploy/scripts/host-verify.sh`
- `共享skill鏡像/連結及對應工具測試（先查目前結構）`

原始保留分支／核對HEAD：
- `codex/news-publication-deploy-receipt@380e463ae785ac98b66eb4fc52dd13d9a6166549`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。

本票scope只含這份對帳紀錄；需要實作時先查owner及重複票，再擴成精確可claim路徑或另開窄實作票。
