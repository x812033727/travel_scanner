---
id: 2026-11-16-admin-overview-autodeploy-warning
title: Admin overview warns when auto deploy is paused or a deploy window was missed
status: done
priority: P2
area: api
owner: claude-opus-5-5-autodeploy
claimed_at: 2026-11-16T02:38:40Z
created_at: 2026-11-16T01:58:54Z
completed_at: 2026-11-16T05:23:40Z
branch: claude/fervent-wright-70jrlh
depends_on:
  - 2026-11-16-admin-redeploy-button-via-timer
scope:
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_admin_operations.py
---

# Admin overview warns when auto deploy is paused or a deploy window was missed

## Why

站主 2026-11-16 決定通知先只看後台（`AUTODEPLOY_NOTIFY_URL` 留空）。`/admin/deployments` 已經顯示主機排程器的狀態
（`deployment_host_status`，見 `2026-11-16-admin-redeploy-button-via-timer`），但站主平常進的是後台總覽；
自動部署失敗暫停、或部署時段結束沒部署成，要在總覽的待辦卡上看得到，不然沒人會去部署頁看。

## Definition of done

- [x] `DEPLOYMENT_EXECUTOR=host_timer` 時，後台總覽（`apps/api/app/admin/operations_service.py`）在下列情況出現警示卡，連到 `/admin/deployments`：
      自動部署暫停檔存在（`paused_reason`）、排程器超過 15 分鐘沒回報、`last_missed_window` 是最近 24 小時內。
- [x] `apps/api/tests/test_admin_operations.py` 覆蓋三種情況與都沒有的情況。

## Steps

- [x] 讀 `app.deployments.host.read_host_status`，照總覽既有的卡片格式加一張。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_operations.py
```

## Notes

- 卡片文字若要進前端目錄，scope 要加對應的 messages 檔。
- 2026-11-16 claude-opus-5-5-autodeploy（PR x812033727/travel_scanner#2124）：總覽「系統健康」區已經有一張連到
  `/admin/deployments` 的「部署」卡（`_system_status` 的 `deployment`），所以沒有新增卡片或前端文案，而是讓它在
  `host_timer` 下讀心跳表：沒回報過／超過 15 分鐘沒回報 → `unavailable`；暫停檔 → `degraded`「自動部署已暫停：…」；
  24 小時內錯過部署時段 → `degraded`「部署時段 … 結束沒部署（sha 卡在 gate）」；其餘 `healthy`（進行中幾個、目前版本、乾跑模式）。
  順手修掉上一張票留下的問題：`host_timer` 下這張卡原本會去問部署代理，顯示「部署 Agent 無法連線」。
  實作在 `host_deployment_component`；測試 7 個參數化情況加一個「不問代理」的整合測試，`test_admin_operations.py` 29 passed。
