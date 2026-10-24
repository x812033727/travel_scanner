---
id: 2026-10-11-restore-agent-community-sweeper-services
title: 恢復部署代理遺漏community-sweeper的共享票
status: done
priority: P2
area: meta
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:23:32Z
created_at: 2026-10-11T14:18:56Z
completed_at: 2026-10-24T13:23:50Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-agent-community-sweeper-services.md
  - apps/api/deployment_agent/executor.py
  - apps/api/tests/test_deployment_agent_contract.py
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

### 2026-10-24 implementation claim

Owner requested completing still-needed open tasks. Current main still defines
`community-sweeper` as an unprofiled long-running Compose service, while the
deployment agent's explicit `APPLICATION_SERVICES` omits it in both forward
activation and rollback. The current open-PR inventory has no change to the two
implementation paths above, and no active task claims those paths. Expanded this
task's scope to those exact files after claiming it. This is a code-only repair;
it does not enable the deployment agent or perform a production deployment.

The independent contract reads the repository's production Compose service
definitions, selects unprofiled long-running services, then exercises the real
deployment executor through new-release activation and a health-failed rollback
with a fake Compose transport. Before the repair it failed only because
`community-sweeper` was missing (1 failed, 7 deselected, exit 1). The repair adds
that service to the shared forward/rollback tuple; the contract also requires
`migrate` to run exactly once before activation and to stay absent from both
`up` calls, with `--no-deps` retained on rollback.

Validation after repair: `tests/test_deployment_agent_contract.py` plus
`tests/test_deployment_center.py` **35 passed, exit 0** on Windows CPython 3.13.15
(137.51 seconds). Focused mypy passed for both changed source/test files;
focused Ruff passed, and `git diff --check` passed. This proves
the code contract through a fake transport; no claim about the live deployment
agent's enablement or production container state is made.


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- Read exact task tasks/open/2026-10-11-restore-agent-community-sweeper-services.md; 0 unchecked checklist rows; no same-id tasks/done file at origin/main 63d49d575a76302b9a82ca611b55bb6a7f6418f6.
- Current origin/main apps/api/deployment_agent/executor.py APPLICATION_SERVICES includes postgres, redis, api, worker, alert-worker, alert-scheduler, hotspot-collector, analytics-scheduler, web; community-sweeper absent.
- 2026-10-24 execution: One service added to shared forward/rollback allowlist after independent real-compose contract red proof;35 pytest,mypy,Ruff passed. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
