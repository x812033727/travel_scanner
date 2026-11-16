# 後台「重新部署」按鈕與每日自動部署：規劃（2026-11-16）

站主的兩個需求：

1. 後台有一顆「重新部署」按鈕。
2. 每天定時檢查 `main` 有沒有新的 commit，有就重新部署。

兩張票：`tasks/open/2026-11-16-autodeploy-daily-window.md`（先做）與
`tasks/open/2026-11-16-admin-redeploy-button-via-timer.md`（依賴前者）。這一頁放現況、設計決定與要站主拍板的事；
驗收與步驟在票裡。部署本身的規矩見 `ops/release/README.md` 與 skill `deploy`，這裡不重抄。

## 一、現況：兩個需求在 repo 裡都有半成品

| 東西 | 在哪裡 | 狀態 |
| --- | --- | --- |
| 自動部署輪詢器 | `ops/autodeploy/`（systemd timer 每 5 分鐘一輪，八道 gate，呼叫 `/root/deploy-travel-scanner.sh`，成功跑 `host-verify.sh`，失敗寫暫停檔） | 程式與測試已合併；**主機上還沒安裝**（2026-10-16 唯讀檢查），安裝、乾跑一週、開啟在 `2026-10-07-autodeploy-rollout-and-skill-docs` |
| 後台部署中心 | `/admin/deployments`、`apps/api/app/deployments/`、`deployment_runs`／`deployment_events` 表、`apps/api/deployment_agent` + `ops/deployer` | 預設關（`DEPLOYMENTS_ENABLED=false`）；**不能直接開**：代理用自己的 `/srv/travel-scanner/releases` 與 compose 專案名、只建 `api`／`web`、不帶 `hotspots`／`news`／`video` profile，啟用會跟正式站那套容器並存成兩套；而且它讀不到暫停檔與分階段發布目錄，每次都會拒絕（`2026-10-07-deployment-agent-needs-read-access-to`） |

所以兩個需求的缺口都不大：

- 每日：輪詢器只會「main 綠了 25 分鐘內就部署」，沒有「一天一次、固定時段」。
- 按鈕：介面、權限、紀錄表都有了，缺的是一個**能在正式站用**的執行者。

## 二、設計決定

### 只有一個執行者：`/root/deploy-travel-scanner.sh`，只有一個呼叫者：autodeploy timer

```
後台按鈕 ──(API 寫一筆 queued 的 deployment_runs)──┐
                                                   ▼
每日時段 ──────────────────────────────▶ autodeploy timer（root，每 5 分鐘）
                                                   │  gate：暫停檔、hold／規則 1／鎖、CI 綠、付費工作…
                                                   ▼
                                     /root/deploy-travel-scanner.sh  →  host-verify.sh
                                                   │
                                   進度與結果寫回 deployment_runs／deployment_events（按鈕請求）
                                   與 state.json（全部）
```

- **按鈕不開新的特權通道。** API 容器不拿 Docker socket、SSH 金鑰或主機權限，只在資料庫寫一筆請求；
  root timer 每輪先查有沒有請求，用 `UPDATE … WHERE status='queued' RETURNING` 認領，跑跟自動部署同一套 gate、同一支腳本。
  timer 已經用 `docker compose exec postgres psql` 查付費影片工作，postgres 也不在部署的重建範圍內，寫回不會斷。
- **為什麼不修好部署中心代理再用它**：它是第二套 release 佈局，要讓它接管正式站得先把兩套容器對齊、再給它讀 `/root` 的權限，
  工程量與風險都比「讓已經在設計裡的 timer 多接一種單」大得多。代理路線保留成 `DEPLOYMENT_EXECUTOR=agent`，不刪。
- **為什麼不用 GitHub Actions 透過 SSH 推**：理由同 `docs/ops/auto-deploy-and-cloud-backup-plan.md` 第二節
  （root 金鑰進 GitHub secrets、要開 inbound SSH、這台主機曾因連線次數把客戶端鎖在外面）。
- 腳本的暫停檔、規則 1、flock、回滾、log 全部沿用，所以分階段發布期間按鈕與每日部署都會自動退讓（腳本 `exit 3`）。

### 每日自動部署：部署時段，而不是一天只跑一次 timer

- 新設定 `AUTODEPLOY_DEPLOY_WINDOWS`（台北時間，例如 `04:30-06:00`）：自動部署只在窗內**開始**；
  `AUTODEPLOY_MAX_AUTO_DEPLOYS_PER_DAY=1`：當天成功過就不再部署。
- timer 仍然每 5 分鐘一輪，不改成 `OnCalendar` 每天一次：
  只跑一次的話，剛好遇到 CI 還在跑或付費影片工作在跑，就整天不部署；按鈕也需要輪詢來接單。
- 窗結束時當天有新 commit 卻沒部署成，發一次通知寫明卡在哪道 gate（既有 `AUTODEPLOY_NOTIFY_URL`）。
- 靜默期（預設 20 分鐘）照舊：窗開始前剛合併的 commit 會等它滿 20 分鐘再部署。

### 按鈕跟每日部署的差別

| | 每日自動部署 | 後台按鈕 |
| --- | --- | --- |
| 誰觸發 | 時段到了且 main 有新的綠色 commit | 只有 owner 角色，重新輸入密碼 |
| 靜默期、時段、每日上限 | 遵守 | 跳過 |
| 自動部署暫停檔（上次失敗） | 停 | 停（先讀 log 再刪，skill `deploy` 規則 10） |
| 部署暫停檔、規則 1、鎖 | 停 | 停 |
| CI 必須綠 | 是 | 是（「重建目前版本」除外，它不換 commit） |
| 付費影片工作在跑 | 等 | 預設等，可取消勾選 |
| 延遲 | 窗內第一輪 | 最多一個 timer 間隔（5 分鐘） |

## 三、順序

1. `2026-11-16-autodeploy-daily-window`：只改 `ops/autodeploy`，小、可單獨合併。
2. `2026-11-16-admin-redeploy-button-via-timer`：API、面板、五語系文案、timer 接單。
   `apps/api/app/config.py` 目前在別的進行中票的 scope 裡（影片語音那兩張），認領前先確認它們結束。
3. 主機：`2026-10-07-autodeploy-rollout-and-skill-docs` 的安裝、token、`AUTODEPLOY_ENABLED=false` 乾跑
   （同時驗證時段與按鈕的 `would_deploy`），再開啟。站主要在場，部署呼叫會被 auto 模式分類器擋（skill `deploy` 規則 3）。

## 四、要站主拍板的事

1. ~~每日部署的時段與一天最多幾次~~：站主 2026-11-16 定案，台灣時間 04:30–06:00、一天一次。
2. ~~通知管道~~：站主 2026-11-16 定案，先只看後台（`AUTODEPLOY_NOTIFY_URL` 留空；timer 的最後決定、自動部署暫停檔與「時段結束沒部署成」顯示在 `/admin/deployments`）。
3. ~~按鈕可以用的人~~：站主 2026-11-16 定案，只給 owner。
4. ~~暫停檔時能不能強制部署~~：站主 2026-11-16 定案，不能；擋下並顯示原因。
5. 按鈕的延遲：5 分鐘可以接受，還是把 timer 改成每分鐘（只在有請求或在時段內才 `git fetch`）。
6. 一把 fine-grained PAT，只給這個 repo `Actions: Read`，放 `/etc/travel-scanner/autodeploy.env`（同既有計畫第三節第 5 點）。
