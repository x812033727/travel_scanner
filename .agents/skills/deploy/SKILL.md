---
name: deploy
description: 把 travel_scanner 部署到唯一的正式主機 mokaair.com：先做主機預檢（暫停檔、未啟用的分階段發布、鎖、磁碟），在背景跑一次性的部署腳本，驗證健康與 migration，處理回滾與清理，並照顧 auto 模式分類器與 SSH 的限制。要重新部署、部署某個已合併的 PR、看部署為什麼被拒絕（exit 3、暫停檔）、判斷一個分階段發布是活的還是被遺棄的、清掉暫停檔、做部署後稽核、查主機磁碟或容器狀態時，先讀這個 skill。Deploy travel_scanner to the single production host. Covers the host preflight (hold file, stranded staged releases, locks, disk), running the one-shot deploy script in the background, health and migration checks, rollback and cleanup, and the permission-classifier and SSH constraints. Use it for any redeploy, a refused deploy, judging or clearing a hold, and post-deploy checks. Not for content imports (that is content-pipeline) and not for writing nginx config.
metadata:
  short-description: 正式站部署：預檢、部署、驗證、回滾
---

# 正式站部署（deploy）

只有一台正式主機。這個 skill 只放指令、關卡、去哪裡讀；分階段發布與暫停檔的規則全文在 `ops/release/README.md`，別在這裡重抄。`<SSH>` 是你自己開到主機 root shell 的指令前綴（每個人的連線方式、金鑰放在自己的筆記，不進 repo）；從 Git Bash 送絕對 POSIX 路徑時前面加 `MSYS_NO_PATHCONV=1`。

## 主機長什麼樣

| 東西 | 在哪裡 |
| --- | --- |
| repo 與 compose | `/root/travel_scanner`，`docker-compose.prod.yml`；web 在 127.0.0.1:8091、api 在 127.0.0.1:8090，nginx 站台 `/etc/nginx/sites-enabled/mokaair.com` |
| 一次性部署腳本 | `/root/deploy-travel-scanner.sh`（root、mode 700、不在 git 裡）；log 在 `/root/deploy-logs/` |
| 暫停檔與鎖 | `/root/travel-scanner-deploy.hold`、`/var/lock/travel-scanner-deploy.lock` |
| 分階段發布的目錄 | `/root/mokaair-*`（`state.json` 或 `host-state/`、`publication-*.json`、各階段 log） |
| 備份 | 腳本只在 incoming commit 動到 migrations 時做 `pg_dump`，放 `/root/travel_scanner_predeploy_<ts>.dump`；nginx 備份在 `/root/nginx-backups/` |
| 三條部署路徑 | 一次性腳本（平常用這條）；Codex 的分階段驅動（prepare → CI → activate → 內容階段）；`ops/deployer/` 的後台部署中心（預設關，**還不認暫停檔**） |
| 兩種「hold」 | 主機的暫停檔擋的是**部署**（`hold.py`、`--ignore-hold`、exit 3）；repo 裡的 `apps/api/app/guides/publish_holds.json` 擋的是**發布**特定 slug（沒有旗標可繞，要刪條目）。別混用 |

## 不變的規矩

1. **先預檢再部署。** 暫停檔存在、或有 `state.json` 在 24 小時內 `built_at` 但沒有 `activated_at`／`failed_at`，腳本會 `exit 3` 拒絕。看到拒絕先讀 `.agents/skills/deploy/references/preflight.md` 判斷是活的發布還是被遺棄的，證據攤開給站主選；`--ignore-hold` 只在站主選了之後用。
2. **部署一律在背景跑**（Bash 的 `run_in_background`），前景呼叫會撞工具逾時、把 SSH 連線連同部署一起切斷。用 `scripts/host-deploy.sh`：它用 nohup 起腳本、印 `DEPLOY_EXIT`。
3. **auto 模式的分類器會擋部署呼叫**，而且換個寫法重試會被當成繞過。第一次就先把 session 切到 Manual（`set_session_permission_mode` → `default`）再送，或把一行指令交給站主自己跑。被擋就停，不要重試。
4. **SSH 呼叫要批次**：一次連線跑一個腳本，不要十次連線各跑一行；四十幾次連線曾把客戶端 IP 鎖在 SSH 外。站台 200 但 SSH 逾時，先分清是鎖還是 sshd 死了（`.agents/skills/deploy/references/pitfalls.md`）。
5. **同一個呼叫裡不要 grep 部署腳本的名字**：plink 把整個腳本當一行命令送過去，`ps` 會比對到自己。要知道有沒有部署在跑，用 flock 試鎖。
6. **動別人的東西先問**：清暫停檔、把死掉的發布標成 `failed_at`、改部署腳本、改 nginx，都要站主在對話裡明確同意；正式站的 `UPDATE`、灌腳本進容器，分類器一律擋，別繞。
7. **不碰 `.env`**（mode 600 必須維持）；主機上的 nginx 設定比 repo 的範例新，`ops/nginx/install.sh` 只覆寫四個專案檔、不 reload、不改站台檔。
8. 內容包跟著程式部署上去，但**沒匯入就不會上線**：匯入是內容那條線的事，走 skill `content-pipeline`。

## 主幹

| # | 階段 | 做什麼 | 關卡 |
| --- | --- | --- | --- |
| 1 | 預檢 | `host-preflight.sh`（唯讀）：暫停檔、被規則 1 標記的目錄、24 小時內動過的發布目錄、鎖、live HEAD 對 origin/main、磁碟 | 沒有暫停檔、沒有 FLAGGED、鎖是空的；否則進 preflight.md 的判斷 |
| 2 | 決定 | 站主要部署什麼（哪個 PR／SHA）、要不要 `--force`、要不要 `--ignore-hold` | 用有選項的提問，不接受一句「好」 |
| 3 | 部署 | `host-deploy.sh`（背景），或站主自己跑一行 | `DEPLOY_EXIT=0`、腳本自己的 3/3 健康檢查過 |
| 4 | 驗證 | `alembic current`、內部 `/health` 與 `/ready`、首頁 200 且 < 1 s、容器映像是 `:local`、抓一個 diff 加進的字串證明新程式在跑 | 全部成立才算部署完成 |
| 5 | 收尾 | 把 SHA、耗時、有無 migration 寫進票或交接；內容匯入交給內容線；大功能上線後做 `post-deploy.md` 的三個問題 | 票或記憶有紀錄 |

## 指令

```bash
# 1 唯讀預檢（只讀檔案；加 --full 才看行程與容器，分類器擋的是後者）
MSYS_NO_PATHCONV=1 <SSH> -m .agents/skills/deploy/scripts/host-preflight.sh
MSYS_NO_PATHCONV=1 <SSH> "bash -s -- --full" < .agents/skills/deploy/scripts/host-preflight.sh
# 腳本自己的調查模式：只印會不會拒絕、原因是什麼，什麼都不做
MSYS_NO_PATHCONV=1 <SSH> "/root/deploy-travel-scanner.sh --dry-run"
# 3 部署（背景執行；旗標原樣傳給部署腳本）
MSYS_NO_PATHCONV=1 <SSH> "bash -s --" < .agents/skills/deploy/scripts/host-deploy.sh
MSYS_NO_PATHCONV=1 <SSH> "bash -s -- --force" < .agents/skills/deploy/scripts/host-deploy.sh
# 4 驗證
MSYS_NO_PATHCONV=1 <SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api alembic current && curl -s -o /dev/null -w '%{http_code}\n' 127.0.0.1:8090/health && docker compose -f docker-compose.prod.yml ps --format '{{.Name}} {{.Image}} {{.Status}}'"
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' https://mokaair.com/zh-TW
```

部署腳本的旗標：不帶參數＝origin/main 比 live 新就部署；`--dry-run` 只調查；`--force` 重建目前的 commit；`--no-rollback` 失敗時不回滾、留現場；`--ignore-hold` 無視暫停檔與規則 1（會印 WARNING）。

## 要多久

| 情況 | 實測 |
| --- | --- |
| 只有文件的 commit，快取全中 | 30 到 40 秒 |
| web 或 api 重建 | 2 到 5 分鐘 |
| 清掉建置快取後的冷建置 | 約 4.5 分鐘 |
| 571 個內容包＋web＋api 一起 | 約 8 分鐘 |

每次建置都會產生新的映像 ID，compose 一律重建七個應用容器，中間約 8 秒 502；hotspot-collector 重啟的第一輪會重算當天排行、也會跑 guide backfill（吃 YouTube 與 Brave 額度），所以同一天多次部署要集中。

## 規則在哪裡（不重抄）

| 問題 | 讀 |
| --- | --- |
| 兩條路徑、四把鎖、暫停檔的格式與 `hold.py acquire/verify/clear/show`、放棄一個發布的順序、不碰正式環境的驗證法 | `ops/release/README.md` |
| 後台部署中心（第三條路徑）的安裝、限制、狀態與 log | `ops/deployer/README.md`、程式在 `apps/api/deployment_agent/` |
| nginx 的四個專案檔、驗證步驟、access_log 與 error_log 的坑 | `ops/nginx/README.md` |
| CI 的四個必要檢查與怎麼可靠地讀 | `.github/BRANCH_PROTECTION.md` |
| 部署後的內容匯入 | `.agents/skills/content-pipeline/references/publish-runbook.md` |
| 這台主機踩過的坑 | `.agents/skills/deploy/references/pitfalls.md` |

## 這個 skill 的檔案

- `references/preflight.md`：怎麼判斷暫停檔背後的發布是活的還是被遺棄的、清理的三種做法與各自要站主同意的地方。
- `references/runbook.md`：腳本做了什麼、旗標、包裝腳本、讀 log、交給站主跑的一行指令長什麼樣、回滾。
- `references/post-deploy.md`：驗證清單、大功能上線後的三個稽核問題、邊緣層的假陽性檢查。
- `references/pitfalls.md`：SSH、分類器、磁碟、腳本、nginx 的坑。
- `scripts/host-preflight.sh`、`scripts/host-deploy.sh`：在主機上跑的 bash，不含任何憑證。
- `.claude/skills/deploy/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
