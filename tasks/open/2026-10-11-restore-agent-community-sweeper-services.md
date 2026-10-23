---
id: 2026-10-11-restore-agent-community-sweeper-services
title: 恢復部署代理遺漏community-sweeper的共享票
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:18:56Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-agent-community-sweeper-services.md
---

## Why

Stay22功能及clickout已merged #379；獨有local open票沒有共享。fresh main APPLICATION_SERVICES明示應涵蓋compose全部long-running service，但tuple仍不含community-sweeper；forward/rollback沿用該tuple。

## Done when

核對當前compose必需service集合並以同義票查重；代理forward/rollback包含community-sweeper，one-shot migrate仍保持另外執行；若代理停用，也需記錄仍存在的原始程式缺口。

## Steps

只讀比compose和agent集合；確認owner/scope後補tuple與契約測試，或採可靠manifest-derived集合；不在這輪啟用部署代理或正式部署。

## Verification

fake CommandRunner測試forward/rollback必需services及migration不誤重跑；主機agent enabled/disabled若要報現況需另外read-only證據。

## Notes

原branch codex/stay22-hotel-clickout HEAD d5e137b2cf56786758ea9a1753c8c69ee9621187；Stay22功能done保持，不因漏掉代理服務重開整個Stay22任務。

建票時scope只含本對帳票；預定實作範圍（完成owner/同義票核對後擴scope或拆窄票）：
- `apps/api/deployment_agent/executor.py`
- `apps/api/tests/test_deployment_agent_contract.py`

原始保留分支／核對HEAD：
- `codex/stay22-hotel-clickout@d5e137b2cf56786758ea9a1753c8c69ee9621187`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。

本票scope只含這份對帳紀錄；需要實作時先查owner及重複票，再擴成精確可claim路徑或另開窄實作票。
