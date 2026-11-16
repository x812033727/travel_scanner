---
id: 2026-11-16-admin-redeploy-button-via-timer
title: Admin redeploy button runs the host deploy script through the auto deploy timer
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-16T01:12:57Z
completed_at:
branch:
depends_on:
  - 2026-11-16-autodeploy-daily-window
scope:
  - apps/api/app/config.py
  - apps/api/app/deployments
  - apps/api/tests/test_deployment_center.py
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-deployments-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - ops/autodeploy
  - ops/deployer/README.md
---

# Admin redeploy button runs the host deploy script through the auto deploy timer

## Why

站主要在後台有一顆「重新部署」按鈕（2026-11-16）。後台其實已經有 `/admin/deployments`
（`apps/web/components/admin-deployments-panel.tsx`、`apps/api/app/deployments/`、`deployment_runs` 表），
但它背後的執行者是 `apps/api/deployment_agent`（`ops/deployer`），而那條路線至今不能用在正式站：

- 它用自己的 `/srv/travel-scanner/releases` 與 compose 專案 `travel-scanner`，只建 `api`、`web`，
  不帶 `hotspots`／`news`／`video` profile；正式站跑的是 `/root/travel_scanner` 全部 profile，
  啟用會變成兩套容器並存（`ops/deployer/README.md`）。
- 它讀不到暫停檔與分階段發布目錄，所以每次都會拒絕
  （`tasks/open/2026-10-07-deployment-agent-needs-read-access-to.md`）。

正式站唯一被驗證過的執行者是 `/root/deploy-travel-scanner.sh`，而 `ops/autodeploy` 的 root timer
已經會在所有 gate 通過後呼叫它、跑 `host-verify.sh`、失敗寫暫停檔。所以按鈕不另開一條特權通道：
**API 只在 `deployment_runs` 寫一筆「請求」，主機上的 timer 下一輪接單、照同一套 gate 跑同一支腳本、把進度寫回這筆紀錄。**
API 容器不需要 Docker socket、SSH 金鑰或任何主機權限。設計：`docs/ops/admin-redeploy-button-and-daily-autodeploy-plan.md`。

## Definition of done

- [ ] 設定 `DEPLOYMENT_EXECUTOR=host_timer|agent`（預設 `host_timer`；`agent` 保留現行代理路線）。
      `host_timer` 時不需要 `DEPLOY_AGENT_SOCKET`／`DEPLOY_AGENT_HMAC_KEY`，`deployments_configured` 也不再要求它們。
- [ ] 按鈕：**只有 owner 角色**能按（站主 2026-11-16；`host_timer` 下 deployer 角色看得到紀錄但按鈕停用、API 回 403），
      本機密碼重新驗證、`Idempotency-Key`、每小時 5 次限流。
      兩個選項：「部署最新的綠色 main」（預設）與「重建目前版本」（腳本 `--force`）；
      一個勾選「有付費影片工作時先等」（預設勾）。
- [ ] API 建立 `status=queued`、`metadata_json.executor="host_timer"` 的 run；`uq_deployment_one_active`
      保證同時只有一筆進行中，連點與兩個管理員同時按都只會有一筆。
- [ ] timer 每輪先查 `queued` 的 host_timer run，用 `UPDATE … SET status='preflight' WHERE id=… AND status='queued' RETURNING`
      認領；按鈕請求**跳過**靜默期、每日時段與每日次數上限，**不跳過**：自動部署暫停檔、部署暫停檔／規則 1／鎖
      （腳本自己的 exit 3）、`CI` 未綠（「重建目前版本」不查 CI）、勾選時的付費工作。被擋就把 run 標 `failed`，
      `failure_code` 用固定字串（`autodeploy_paused`、`deployment_hold_active`、`ci_not_green`、`paid_work_running`、
      `deploy_lock_held`），`failure_detail` 帶原因第一行。
- [ ] 進度寫回 `deployment_events`（preflight → building → verifying → succeeded/failed/rolled_back），
      `previous_sha`、`target_sha`、`ci_url`、log 檔名、`host-verify.sh` 的 `TOTAL` 行；面板照現有輪詢顯示。
      部署中 api 重啟約 8 秒 502，面板要把它當「部署中」而不是錯誤。
- [ ] 超過 10 分鐘沒被認領（timer 沒裝、停了、主機掛了）的 queued run，overview 顯示「主機排程器沒有回應」，
      並讓下一筆請求可以取消它（標 `failed`／`executor_unavailable`）。
- [ ] 後台面板在 `host_timer` 下顯示 timer 的狀態，這是站主目前**唯一的通知管道**（2026-11-16：先只看後台，
      `AUTODEPLOY_NOTIFY_URL` 留空）：最後一輪時間與決定（action、gate、reason、SHA）、最後一次自動部署與 verify 結果、
      今天的自動部署次數、`last_missed_window`（時段結束沒部署成）、自動部署暫停檔的第一行。
      timer 每輪把這些 upsert 成一列心跳（新的一張小表，要 migration，照 skill `backend-conventions`）；
      後台總覽（`apps/api/app/admin/operations_service.py` 的待辦卡）在暫停檔存在或錯過時段時顯示警示——
      該檔不在本票 scope，實作時擴 scope 或另開小票。
- [ ] 測試：API（建立、冪等、一筆進行中、權限、`host_timer` 不需代理設定）、`ops/autodeploy` 單元測試（認領、各種拒絕、
      成功寫回、失敗寫回、跳過靜默期與時段）、面板 vitest；五語系文案、`npm run check:i18n`。

## Steps

- [ ] API：`app/deployments/service.py` 依 `DEPLOYMENT_EXECUTOR` 分流；`host_timer` 的 `create_deployment` 不呼叫代理，
      `_reconcile` 改讀資料庫裡 timer 寫回的狀態。`target_sha` 是 NOT NULL：建立時先填 API 看到的 `origin/main`
      （可用既有唯讀 GitHub token），timer 認領時以實際 fetch 到的綠色 SHA 覆寫並記事件；或放寬成 nullable
      （要 migration，照 skill `backend-conventions`）。
- [ ] `ops/autodeploy/autodeploy.py`：新 gate 0「有沒有按鈕請求」，`_psql` 讀寫（它已經用
      `docker compose exec postgres psql` 查 `video_stage_jobs`）；postgres 不在部署重建範圍內，部署中寫回不會斷。
      SQL 只用固定語句與 UUID／SHA 正規式檢查過的值，不接受任何來自資料庫的指令或路徑。
- [ ] 面板與文案；隱藏 `host_timer` 用不到的代理專屬欄位（備份名稱等）。
- [ ] `ops/deployer/README.md`：寫明 `host_timer` 是預設、代理路線是未啟用的替代方案。skill `deploy` 的主機表
      （第四條路徑改成「後台按鈕 → timer → 一次性腳本」）不在本票 scope，交給
      `2026-10-07-autodeploy-rollout-and-skill-docs` 或另開小票。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_deployment_center.py
python -m unittest discover -s ops/autodeploy -v
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

主機上（timer 已裝、`AUTODEPLOY_ENABLED=false`）：按下按鈕，下一輪 journal 出現 `request <id>: would_deploy`，
run 標成 `failed`／`dry_run`；開啟後再按一次，看完整一輪 succeeded 與 `host-verify.sh` PASS。

## Notes

- 依賴 `2026-11-16-autodeploy-daily-window`：兩張都改 `ops/autodeploy/autodeploy.py`，先做小的那張避免衝突。
- 主機上真正可用要等 `2026-10-07-autodeploy-rollout-and-skill-docs` 的安裝與開啟。
- 按鈕的延遲最多一個 timer 間隔（5 分鐘）；若站主覺得太慢，可把 timer 改成每分鐘，但 `git fetch` 只在有請求或在部署時段內才做。
- 站主 2026-11-16 定案：按鈕只給 owner；自動部署暫停檔存在時**不能**強制部署（顯示原因，先讀 log 再刪暫停檔，skill `deploy` 規則 10）；
  通知先只看後台。還沒定：按鈕延遲 5 分鐘能否接受（計畫文件第四節第 5 點）。
