---
name: prod-host-ops
description: 正式站在部署以外的日常操作。涵蓋 nginx 邊緣層（限流、偽造的轉送位址、爬蟲網段、access_log、會通過卻什麼都沒證明的檢查、ss -tan 與 -tn）、零星的 POST 502、在主機上診斷 AI 行程規劃與新聞 worker、用後台或主機 CLI（sources_cli、settings_cli）改正式站設定與逐張驗證 AI 卡片、用瀏覽器驅動後台 React 表單、法律頁雜湊核對、用真實點擊驗分潤 clickout、主機 AI 帳號代理的用法。要查 429 或 502、改限流或 nginx log、查某個 AI 功能為何失敗、開關新聞自動化、改後台設定並證明生效、發布法律頁、驗合作按鈕時，先讀這個 skill。部署本身走 deploy，看板走 task-board，文章與目錄匯入走 content-pipeline 或 catalog-import，本機開發與 CI 走 dev-and-ci。Operate the production site between deploys, covering the nginx edge, sporadic 502s, AI and news diagnosis, settings changes through the admin or host CLIs, and admin, legal-page and clickout verification.
metadata:
  short-description: 正式站營運：邊緣層、AI 與新聞診斷、後台設定與驗證
---

# 正式站營運（prod-host-ops）

> 本文提到的 `references/…`、`scripts/…` 都在 `.agents/skills/prod-host-ops/` 底下；`.claude/skills/prod-host-ops/` 只放這份 SKILL.md 的逐字複本。

部署之外、碰正式站的事都在這裡：看、改、證明。**連線、SSH 批次、auto 模式分類器會擋什麼，全部照 skill `deploy`**（`.agents/skills/deploy/SKILL.md` 的「不變的規矩」與 `.agents/skills/deploy/references/pitfalls.md`），這裡不重抄。`<SSH>` 同 deploy：你自己開到主機 root shell 的前綴。主機上 repo 在 `/root/travel_scanner`，compose 指令都在那個目錄以 `docker compose -f docker-compose.prod.yml` 執行。

## 不變的規矩

1. **一個檢查要能失敗才算數。** 這台主機上有一串檢查「通過但什麼都沒證明」（清單在 `.agents/skills/prod-host-ops/references/nginx-edge.md`）；寫下結論前先問：如果壞了，這個指令的輸出會不一樣嗎？
2. **設定的真相在資料庫，不在容器環境。** AI 金鑰、模型、Base URL、功能開關都在後台 `provider_configs` 列，`load_runtime_settings(session)` 才是有效值；在容器裡 `printenv` 會看到「沒有金鑰」而其實有。
3. **改正式站設定先問站主**，用有選項的提問；nginx reload、改 `.env`、正式站的寫入都是。後台裡的「發布」「確認發布」這類不可逆按鈕，先把要按的東西寫清楚，讓站主決定由誰按。
4. **不印出秘密。** 金鑰只報「有／沒有」；`--actor-email` 從容器的 `ADMIN_EMAILS` 取，經 shell 變數傳、不印出來。
5. **自己的檢查迴圈要慢**：頁面限流是每個位址 5 r/s（burst 20），腳本一律循序、每次 ≥ 1 秒；自己拿到 429 先懷疑自己的節奏。
6. **用戶端的東西要在真的瀏覽器裡驗。** curl 帶手寫的 `Origin` 只證明伺服器規則；`form_input` 只改 DOM 不改 React state。
7. **影片指令用 `exec`，不用 `run`。** 在主機上手動跑 `tools/video/cli.mjs` 一律 `docker compose -f docker-compose.prod.yml exec -T video-worker …`；`docker compose run` 另開的容器跟工人同一個 hostname 卻看不到工人的程序，會把工人拿著的專案鎖 `LEASE` 誤判成死的而接手（`docs/videos/AUTOMATION.md`）。

## 主幹

| # | 情況 | 做什麼 | 讀 |
| --- | --- | --- | --- |
| 1 | 429、爬蟲被擋、「Google 抓不到 ads.txt」 | 先確認 log 有記到（access_log 覆蓋問題），按來源位址而非 UA 分組，對照公布的網段 | `.agents/skills/prod-host-ops/references/nginx-edge.md` |
| 2 | POST 零星 502 | 分清部署重建（容器 StartedAt 對得上部署 log）與 keep-alive 競態；用 `ss -tan` 看誰先關 | `.agents/skills/prod-host-ops/references/nginx-edge.md` 的「502」 |
| 3 | AI 行程規劃／介紹搜尋失敗或變慢 | 讀 api log 的 `ai planner provider … failed`，看有效設定，再按卡片的「測試連線」 | `.agents/skills/prod-host-ops/references/ai-settings.md` |
| 4 | 新聞沒產出、候選卡住 | `settings_cli` 看開關與金鑰、看 `news-worker` 在不在、看清單在哪個狀態 | `.agents/skills/prod-host-ops/references/news-ops.md` |
| 5 | 改後台設定 | 後台表單（或主機 CLI），改完逐張驗證 | `.agents/skills/prod-host-ops/references/ai-settings.md`、`.agents/skills/prod-host-ops/references/admin-browser.md` |
| 6 | 法律頁改版 | 後台逐語系編輯 → 雜湊核對 → 逐語系發布 → 20 個網址回歸 | `.agents/skills/prod-host-ops/references/admin-browser.md` |
| 7 | 合作按鈕、分潤 clickout | 真實瀏覽器點擊，看請求的 `Origin` 與 303 | `.agents/skills/prod-host-ops/references/admin-browser.md` |
| 8 | 主機上的 Claude／Codex／agy 帳號 | 用哪個帳號、額度怎麼讀、登入壞了怎麼補 | `.agents/skills/prod-host-ops/references/ai-accounts.md` |
| 9 | 昨晚的備份有沒有成功、timer 還在不在跑 | `bash /opt/travel-scanner-backup/status.sh`；看到 `BACKUP STALE`／`BACKUP FAILED` 照下面「備份」節處理 | 本檔「備份」節、`ops/backup/README.md` |

## 常用指令

```bash
# 容器與服務（news-scheduler、news-worker 在 compose profile news）
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml ps --format '{{.Name}} {{.Status}}'"
# 部署重建還是當機：StartedAt 對照 /root/deploy-logs/deploy_*.log 的時間
<SSH> "docker inspect -f '{{.State.StartedAt}}' travel_scanner-web-1; ls -t /root/deploy-logs | head -3"
# 邊緣層的三個 log（error.log 與 access.log 看不到主站的限流與正常請求）
<SSH> "tail -n 20 /var/log/nginx/mokaair-limit.log; tail -n 20 /var/log/nginx/mokaair-limited.log; tail -n 5 /var/log/nginx/mokaair-crawl.log"
# 新聞自動化：只看，不改
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.settings_cli"
# AI 行程規劃失敗的原因（狀態碼與回應摘錄）
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml logs --since 2h api | grep 'ai planner provider'"
# 公開站慢慢量
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' https://mokaair.com/zh-TW
# 昨晚的備份：timer 狀態、最後一次成功與幾小時前、失敗原因；失敗或超過 36 小時 exit 1
<SSH> "bash /opt/travel-scanner-backup/status.sh"
```

每一條都是一次連線；要跑好幾條就寫成一個腳本用 `bash -s` 一次送（deploy 的規矩 4）。

## 備份

每晚 04:17（台灣時間）`travel-scanner-backup.timer` 跑 `/opt/travel-scanner-backup/backup.py run`：驗證過的 `pg_dump`、部署前的 predeploy dump、用 age 加密的設定包，寫到 `/var/backups/travel-scanner/nightly/<ts>/`，結果記在 `/var/lib/travel-scanner-backup/last.json`。規則全文在 `ops/backup/README.md`，這裡只放怎麼看、壞了怎麼辦。

`status.sh` 印四種東西：`timer: enabled=… active=… run=…`、`last success: <時間> (<n> h ago) …`、`last failure: …`、`last skipped: …`，最後一行可能是 `BACKUP STALE`（最後成功超過 36 小時）或 `BACKUP FAILED`（最後一次失敗比最後成功新）。部署預檢（skill `deploy` 的 `host-preflight.sh`）也印同一段。

| 看到 | 先看 | 常見原因與做法 |
| --- | --- | --- |
| `timer: not installed` 或 `enabled=disabled` | `ls /opt/travel-scanner-backup`、`systemctl list-timers travel-scanner-backup.timer` | 還沒裝或被關掉：`ops/backup/README.md` 的安裝順序；啟用要站主同意 |
| `last success: never` | `journalctl -u travel-scanner-backup` | 從沒成功過：先手動 `backup.py run --dry-run` 再 `run`，看它停在哪一步 |
| `BACKUP STALE` 而 `last failure` 是空的 | `journalctl -u travel-scanner-backup --since -2d`、`last skipped` | timer 沒開（`active=inactive`）、主機當時關機（`Persistent=true` 會補跑，看 `next run`）、連續被部署鎖擋（`last skipped` 的時間都在凌晨：分階段發布佔鎖，等它結束就會補） |
| `BACKUP FAILED: database: …` | 失敗原因那行、`docker compose ps postgres` | `pg_dump` 或 `pg_restore --list` 失敗：postgres 不健康、磁碟滿（`df -h /var/backups`）。不要手動刪 `nightly/` 底下的目錄來騰空間，先確認保留數 |
| `BACKUP FAILED: config: …` | `age` 在不在（`command -v age`）、`backup.env` 的 `BACKUP_AGE_RECIPIENT` | 沒裝 age 或公鑰格式錯；公鑰只能是 `age1…`，私鑰永遠不在主機上 |
| `BACKUP FAILED: git` / `alembic` / `postgres` | `git -C /root/travel_scanner status`、`alembic_version` 表 | 主機 checkout 壞了或資料庫起不來，通常同時會有別的症狀；先處理站台 |
| `run=active` 很久 | `journalctl -u travel-scanner-backup -f` | 一次備份正在跑（大庫幾分鐘）；超過一小時再懷疑卡住，`TimeoutStartSec=2h` 會收掉 |

一份備份算不算備份，要看還原：單份 dump 的還原在 `ops/backup/README.md`，整台主機的演練 runbook 由異地備份那張票（`tasks/open/2026-10-07-backup-google-drive-offsite.md`）寫。修備份、改保留數、刪舊目錄都是改正式站，照規矩 3 先問站主。

## 參考檔

| 檔案 | 內容 |
| --- | --- |
| `.agents/skills/prod-host-ops/references/nginx-edge.md` | 主機上的 nginx 長相、限流區與豁免、四個 log、假通過的清單與正確的驗法、爬蟲網段的更新、keep-alive 502 的兩半與 `ss -tan`、CDN 檢查 |
| `.agents/skills/prod-host-ops/references/ai-settings.md` | AI 服務的卡片與欄位、優先順序、Claude 訂閱連線、逐張驗證、在主機上診斷行程規劃、MiniMax 的坑 |
| `.agents/skills/prod-host-ops/references/news-ops.md` | 新聞自動化的服務、`sources_cli`／`settings_cli`、清單與狀態、worker 被部署中斷之後、診斷順序 |
| `.agents/skills/prod-host-ops/references/admin-browser.md` | 用瀏覽器驅動後台 React 表單、原生 dialog 與勾選框、法律頁的雜湊核對與發布、用真實點擊驗 clickout |
| `.agents/skills/prod-host-ops/references/ai-accounts.md` | `/admin/ai-accounts` 與主機代理：帳號槽、SSH 上怎麼選帳號、額度來源、登入失敗的補救、檢查指令 |

## 規則全文在哪（不重抄）

| 問題 | 讀 |
| --- | --- |
| nginx 的安裝、每個驗證步驟的完整腳本 | `ops/nginx/README.md` |
| 新聞自動化的每個階段、清單、門檻 | `docs/news-automation.md` |
| AI 帳號代理的安裝、信任邊界、復原 | `ops/ai-accounts/README.md` |
| 公開讀取的應用層限流 | `docs/anti-scraping.md` |
| 部署、暫停檔、SSH 與分類器 | skill `deploy` |
| 每晚備份的每一步、安裝、單份 dump 的還原 | `ops/backup/README.md` |

`.claude/skills/prod-host-ops/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
