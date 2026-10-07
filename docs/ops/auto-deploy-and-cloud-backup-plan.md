# 自動部署與雲端備份：規劃（2026-10-07）

兩個功能，六張票，全部在 `tasks/open/2026-10-07-*`。這一頁只放現況、設計決定與站主要拍板的事；
做法細節、驗收與指令在各票裡。部署本身的規矩不重抄，見 `ops/release/README.md` 與 skill `deploy`。

## 一、現況（從 repo 讀出來的，主機上的實際狀態要再核對）

### 部署

| 路徑 | 狀態 | 誰觸發 |
| --- | --- | --- |
| 一次性腳本 `/root/deploy-travel-scanner.sh` | 平常用這條；有暫停檔與規則 1 的守門、flock、有 migration 才 `pg_dump`、三次健康檢查、失敗自動回滾 | **人**：站主或代理用 SSH 跑 `host-deploy.sh` |
| 分階段發布驅動（`docs/*/release_host.py`） | 內容批次用；自己管暫停檔 | 人 |
| 後台部署中心 `apps/api/deployment_agent` + `ops/deployer` | 預設關；不認暫停檔；用自己的 `/srv/travel-scanner/releases` 與 `-p travel-scanner` 專案名，只建 `api`、`web` 兩個映像、不帶 `hotspots`／`news`／`video` profile。直接啟用會跟路徑 A 的容器並存成兩套 | 後台按鈕（需 deployer 角色＋密碼） |

結論：**main 合併之後沒有任何東西會自己部署**。每次都要有人開 SSH，而且 auto 模式的分類器會擋部署呼叫（skill `deploy` 規則 3），常常要站主切 Manual 或自己跑一行。

### 備份

| 東西 | 現在 |
| --- | --- |
| PostgreSQL（文章、店家、景點、社群、影片工作、後台設定，**全部內容**） | 只在 incoming commit 動到 migrations 時 `pg_dump -Fc` 到 `/root/travel_scanner_predeploy_<ts>.dump`；後台部署中心的七份驗證備份只在它被用到時才產生，而它是關的。**沒有排程備份，沒有異地副本** |
| Redis（`redis_data`） | 無 |
| 不在 git 裡的設定與密鑰：`/root/travel_scanner/.env`、`/etc/travel-scanner/*.env`、`/etc/mokaair-uploader/`、`/etc/nginx/sites-enabled/mokaair.com`、`/etc/letsencrypt`、**`/root/deploy-travel-scanner.sh` 本身**、各 systemd unit | 無；nginx 只有改動前的 `/root/nginx-backups/` |
| AI 帳號登入狀態 `/var/lib/mokaair-ai-accounts/*`（Claude／Codex／agy 的 OAuth token） | 無（可重新登入，但五個帳號乘三個工具很花時間） |
| 影片資料卷：`video_media`（付費生成的圖、片段、音樂，14 天）、`video_work`（1080p 成品）、`video_reviews`、`video_docs`、`video_home` | 無；付費素材一掉就要重買 |
| 分階段發布目錄 `/root/mokaair-*`、`/root/deploy-logs/` | 無（小，但是發布紀錄） |

結論：主機磁碟一壞，站台內容只剩最近一次有 migration 的那份 dump，而且它跟主機在同一顆碟上。

## 二、設計決定

### 自動部署：主機端輪詢器，不是 GitHub Actions 推

- **主機上一支 systemd timer（每 5 分鐘）跑 `ops/autodeploy/autodeploy.py tick`**，發現 `origin/main` 比 live 新、
  該 SHA 的 `CI` workflow 是 `success`，就呼叫現有的 `/root/deploy-travel-scanner.sh`。
- 為什麼不用 GitHub Actions 透過 SSH 推：要把主機 root 金鑰放進 GitHub secrets、要開 inbound SSH 給 runner 的 IP，
  而這台主機曾因連線次數把客戶端鎖在外面。拉（pull）的做法跟部署中心代理一樣只需要一把唯讀的 `Actions: Read` token。
- 為什麼不直接啟用後台部署中心：它是另一套 release 佈局，而且不認暫停檔（上表）。它留著當手動按鈕；認暫停檔另開 P3 票。
- **執行者仍然是 `/root/deploy-travel-scanner.sh`**：暫停檔、規則 1、flock、回滾、log 全部沿用，輪詢器只決定「現在要不要跑它」。
  所以分階段發布期間它自動退讓（腳本 `exit 3`），不用再加一把鎖。
- 輪詢器自己的守門：合併後靜默期（預設 20 分鐘沒有新 commit 才部署，把連續合併併成一次重建）、
  CI 還在跑就等、有 `running` 的付費影片工作就等（跟預檢同兩句 select）、可設定不部署的時段。
- **失敗就自己停**：部署腳本非零結束（它已經回滾）時寫 `/root/travel-scanner-autodeploy.paused`（第一行人看的理由，第二行 JSON），
  之後每一輪只印原因不動手，直到人刪掉。成功後跑 `host-verify.sh`，PASS／FAIL 一起記進狀態檔。
- 程式碼進 repo（`ops/autodeploy/`，有 unittest，要能在 Windows 跑，跟 `ops/release/hold.py` 一樣），
  用 `install.sh` 複製到 `/opt/travel-scanner-autodeploy/`，升級是人工動作（跟 `ops/deployer` 一致）。
- 上線順序：裝好但 `AUTODEPLOY_ENABLED=false` → 看一週 `--dry-run` 的 log 判斷它每次的決定都對 → 開啟。

### 備份：先有每晚驗證過的本機備份，再用 rclone 送 Google 雲端硬碟

- **第一層（票 4）**：每晚一次 systemd timer 跑 `ops/backup/backup.py`：`pg_dump -Fc` → `pg_restore --list` 驗證 → SHA-256 →
  `manifest.json`（主機、時間、live SHA、alembic revision、每個檔案的大小與雜湊）。本機留 7 天在 `/var/backups/travel-scanner/nightly/`。
  設定與密鑰打包成一個 tar，**不落地明文**：在暫存目錄建好、送出、刪掉。
- **第二層（票 5）**：`rclone` 一個 `drive` remote 再包一層 **`crypt` remote**，所有東西離開主機前都在本機加密
  （檔名與內容），Google 看到的只是密文。這樣密鑰、AI 帳號 token、資料庫內容可以用同一條規則送上去。
  Drive 上留 30 份每日＋12 份每月；`rclone` 用 `--drive-chunk-size` 與重試處理大檔。
- 認證方式：站主自己的 Google 帳號走 OAuth（`rclone authorize "drive"` 在站主電腦上做一次，把 token 貼到主機），
  scope 用 `drive.file`（只看得到 rclone 自己建的檔案），並建自己的 OAuth client ID（rclone 共用的那個會被限流）。
  不用 service account：service account 上傳到「我的雲端硬碟」的檔案沒有配額可用，只有 Workspace 的共用雲端硬碟才行。
- **還原演練是功能的一部分**（票 5 的 runbook）：從 Drive 拉回、解密、`pg_restore` 到一個拋棄式 postgres 容器、數幾張表。
  沒做過還原的備份不算備份。
- **監看（票 6）**：`/var/lib/travel-scanner-backup/last.json` 記最後一次成功；預檢與 `prod-host-ops` 看得到「最後備份幾小時前」，
  超過 36 小時算異常。
- 部署前的 dump：票 4 的腳本可以被部署腳本或輪詢器呼叫，讓「每次部署前都有一份驗證過的 dump」而不只是有 migration 時。
  這要改主機腳本，需要站主同意，列在票 4 的 Notes，不在定義完成裡。

## 三、站主要拍板的事

自動部署：

1. 輪詢間隔（建議 5 分鐘）與靜默期（建議 20 分鐘）。
2. 要不要有「不部署」的時段（例如台灣時間 09:00–12:00 流量高峰？或完全不設）。hotspot-collector 每次重啟都會重算當天排行並吃 YouTube／Brave 額度，所以一天多次合併時靜默期比時段更重要。
3. 有付費影片工作在跑時：等（建議）或照樣部署。等超過多久要通知？
4. 失敗與成功的通知管道：email（站台已有 `COMMUNITY_SMTP_*`）、Telegram／Discord webhook，或只看 log。
5. 一把 fine-grained PAT，只給這個 repo `Actions: Read`（跟部署中心代理同規格），放 `/etc/travel-scanner/autodeploy.env`。
6. 部署腳本要不要改成「每次部署前都 dump」（第二節最後一點）。

備份：

7. 用哪個 Google 帳號、配額多少（個人 15 GB 放不下影片成品；Workspace 或 Google One 的容量先確認）。
8. 影片資料卷要送哪些：建議 `video_media`（付費素材）與 `video_work/<slug>/upload/final.mp4`（成品）送，`video_work` 其餘、`video_home`、`video_reviews` 不送。票 4 第一步會先在主機量大小再決定。
9. 加密密語放哪裡：主機 `/etc/travel-scanner/backup.env`（0600）**加上**站主的密碼管理器。少了第二份，主機一掉備份就打不開。
10. AI 帳號 token 要不要送（加密後）。
11. 保留策略（建議 Drive 30 每日＋12 每月，本機 7 天）與還原演練頻率（建議每季）。

## 四、票與順序

| 票 | 做什麼 | 優先 | 依賴 |
| --- | --- | --- | --- |
| `2026-10-07-autodeploy-host-poller` | `ops/autodeploy/`：輪詢器、systemd timer、installer、測試 | P1 | — |
| `2026-10-07-autodeploy-rollout-and-skill-docs` | 預檢顯示輪詢器狀態、skill 與 `ops/release/README.md` 更新、乾跑一週後開啟 | P1 | poller |
| `2026-10-07-deployer-agent-honors-deploy-hold` | 後台部署中心認暫停檔 | P3 | — |
| `2026-10-07-backup-nightly-verified-dumps` | `ops/backup/`：每晚驗證過的 dump、設定包、manifest、本機保留、測試 | P1 | — |
| `2026-10-07-backup-google-drive-offsite` | rclone crypt → Google 雲端硬碟、Drive 保留、還原 runbook 與第一次演練 | P1 | nightly |
| `2026-10-07-backup-age-in-host-ops-checks` | 最後備份時間進預檢與 `prod-host-ops`，過期即警示 | P2 | nightly |

兩條線互不依賴，可以兩個 session 平行做；票的 `scope` 已經分開。
