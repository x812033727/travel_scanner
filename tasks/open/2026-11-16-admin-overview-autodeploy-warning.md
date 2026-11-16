---
id: 2026-11-16-admin-overview-autodeploy-warning
title: Admin overview warns when auto deploy is paused or a deploy window was missed
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-11-16T01:58:54Z
completed_at:
branch:
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

- [ ] `DEPLOYMENT_EXECUTOR=host_timer` 時，後台總覽（`apps/api/app/admin/operations_service.py`）在下列情況出現警示卡，連到 `/admin/deployments`：
      自動部署暫停檔存在（`paused_reason`）、排程器超過 15 分鐘沒回報、`last_missed_window` 是最近 24 小時內。
- [ ] `apps/api/tests/test_admin_operations.py` 覆蓋三種情況與都沒有的情況。

## Steps

- [ ] 讀 `app.deployments.host.read_host_status`，照總覽既有的卡片格式加一張。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_operations.py
```

## Notes

- 卡片文字若要進前端目錄，scope 要加對應的 messages 檔。
