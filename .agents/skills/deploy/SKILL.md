---
name: deploy
description: 把 travel_scanner 部署到唯一的正式主機 mokaair.com：先做主機預檢（暫停檔、未啟用的分階段發布、鎖、磁碟），在背景跑一次性的部署腳本，驗證健康與 migration，處理回滾與清理，並照顧 auto 模式分類器與 SSH 的限制。要重新部署、部署某個已合併的 PR、看部署為什麼被拒絕（exit 3、暫停檔）、判斷一個分階段發布是活的還是被遺棄的、清掉暫停檔、做部署後稽核、查主機磁碟或容器狀態時，先讀這個 skill。Deploy travel_scanner to the production host with preflight, background deploy, health checks, rollback and hold handling.
metadata:
  short-description: 正式站部署：預檢、部署、驗證、回滾
---

# 正式站部署（deploy）

只有一台正式主機。這個 skill 只放指令、關卡、去哪裡讀；分階段發布與暫停檔的規則全文在 `ops/release/README.md`，別在這裡重抄。`<SSH>` 是你自己開到主機 root shell 的指令前綴（每個人的連線方式、金鑰放在自己的筆記，不進 repo）；從 Git Bash 送絕對 POSIX 路徑時前面加 `MSYS_NO_PATHCONV=1`。session 本身就在正式主機上時（`/root/deploy-travel-scanner.sh` 存在），沒有 SSH 這一跳：`<SSH>` 留空、`MSYS_NO_PATHCONV=1` 不用，`<SSH> -m <腳本>` 與 `<SSH> "bash -s -- …" < <腳本>` 都改成 `bash <腳本> …`，部署照樣用 `run_in_background`。

## 主機長什麼樣

| 東西 | 在哪裡 |
| --- | --- |
| repo 與 compose | `/root/travel_scanner`，`docker-compose.prod.yml`；web 在 127.0.0.1:8091、api 在 127.0.0.1:8090，nginx 站台 `/etc/nginx/sites-enabled/mokaair.com` |
| 一次性部署腳本 | `/root/deploy-travel-scanner.sh`（root、mode 700、不在 git 裡）；log 在 `/root/deploy-logs/` |
| 暫停檔與鎖 | `/root/travel-scanner-deploy.hold`、`/var/lock/travel-scanner-deploy.lock` |
| 分階段發布的目錄 | `/root/mokaair-*`（`state.json` 或 `host-state/`、`publication-*.json`、各階段 log） |
| 備份 | 腳本只在 incoming commit 動到 migrations 時做 `pg_dump`，放 `/root/travel_scanner_predeploy_<ts>.dump`；nginx 備份在 `/root/nginx-backups/` |
| 四條部署路徑 | 一次性腳本（平常用這條）；**自動部署 timer**（`ops/autodeploy/`，每 5 分鐘一輪，main 綠了就跑同一支一次性腳本）；Codex 的分階段驅動（prepare → CI → activate → 內容階段）；`ops/deployer/` 的後台部署中心（預設關，**還不認暫停檔**） |
| 自動部署的檔案 | 狀態 `/var/lib/travel-scanner-autodeploy/state.json`（最後一輪的決定、最後一次自動部署的 SHA 與驗證結果）；暫停檔 `/root/travel-scanner-autodeploy.paused`（自動部署失敗、腳本已回滾，兩行格式同部署暫停檔）；log `/root/deploy-logs/auto-<ts>.log` 與 `auto-verify-<ts>.log`；設定 `/etc/travel-scanner/autodeploy.env`（`AUTODEPLOY_ENABLED=false` 是乾跑）；`journalctl -u travel-scanner-autodeploy` |
| 三種「hold」 | 主機的暫停檔擋的是**部署**（`hold.py`、`--ignore-hold`、exit 3）；repo 裡的 `apps/api/app/guides/publish_holds.json` 擋的是**發布**特定 slug（沒有旗標可繞，要刪條目）；自動部署的 `.paused` 只擋 **timer 自己**，手動部署不受它影響。別混用 |

## 不變的規矩

1. **先預檢再部署。** 暫停檔存在、或有 `state.json` 在 24 小時內 `built_at` 但沒有 `activated_at`／`failed_at`，腳本會 `exit 3` 拒絕。看到拒絕先讀 `.agents/skills/deploy/references/preflight.md` 判斷是活的發布還是被遺棄的，證據攤開給站主選；`--ignore-hold` 只在站主選了之後用。
2. **部署一律在背景跑**（Bash 的 `run_in_background`），前景呼叫會撞工具逾時、把 SSH 連線連同部署一起切斷。用 `.agents/skills/deploy/scripts/host-deploy.sh`：它用 nohup 起腳本、印 `DEPLOY_EXIT`。
3. **auto 模式的分類器會擋部署呼叫**，而且換個寫法重試會被當成繞過。第一次就先把 session 切到 Manual（`set_session_permission_mode` → `default`）再送，或把一行指令交給站主自己跑。被擋就停，不要重試。
4. **SSH 呼叫要批次**：一次連線跑一個腳本，不要十次連線各跑一行；四十幾次連線曾把客戶端 IP 鎖在 SSH 外。站台 200 但 SSH 逾時，先分清是鎖還是 sshd 死了（`.agents/skills/deploy/references/pitfalls.md`）。
5. **同一個呼叫裡不要 grep 部署腳本的名字**：plink 把整個腳本當一行命令送過去，`ps` 會比對到自己。要知道有沒有部署在跑，用 flock 試鎖。
6. **動別人的東西先問**：清暫停檔、把死掉的發布標成 `failed_at`、改部署腳本、改 nginx，都要站主在對話裡明確同意；正式站的 `UPDATE`、灌腳本進容器，分類器一律擋，別繞。
7. **不碰 `.env`**（mode 600 必須維持）；主機上的 nginx 設定比 repo 的範例新，`ops/nginx/install.sh` 只覆寫四個專案檔、不 reload、不改站台檔。
8. 內容包跟著程式部署上去，但**沒匯入就不會上線**：匯入是內容那條線的事，走 skill `content-pipeline`。
9. **手動部署前先看 timer。** `systemctl is-active travel-scanner-autodeploy.service` 是 `active` 代表一輪正在部署（它也持有部署鎖，`host-deploy.sh` 會拒絕）；等它結束再跑，或先看 `state.json` 是不是已經把要部署的 SHA 部好了。timer 開著時 main 合併後最多 25 分鐘（靜默期 20 加輪詢 5）就會自己上線，多數時候不必手動部署。
10. **自動部署的暫停檔不要直接刪。** `/root/travel-scanner-autodeploy.paused` 第一行寫著哪個 SHA、哪支 log、退出碼；先讀那支 log 判斷失敗原因，在 main 上修正，確認之後才刪檔（刪了下一輪就會再部署同一個或更新的 SHA）。暫停檔與分階段發布的部署暫停檔（規矩 1）是兩回事：後者擋所有部署，前者只擋 timer。

## 主幹

| # | 階段 | 做什麼 | 關卡 |
| --- | --- | --- | --- |
| 1 | 預檢 | `host-preflight.sh`（唯讀）：暫停檔、被規則 1 標記的目錄、24 小時內動過的發布目錄、鎖、live HEAD 對 origin/main、磁碟、自動部署 timer 的狀態與暫停檔、還沒結算的付費影片工作 | 沒有暫停檔、沒有 FLAGGED、鎖是空的、timer 沒有在部署中（`tick=inactive`）、沒有 `AUTO DEPLOY PAUSED`、沒有 `PAID WORK IN FLIGHT`；否則進 preflight.md 的判斷 |
| 2 | 決定 | 先看要不要部署：預檢加 `--dry-run`，別的 session 常部署，main 可能早就 live，那就不必問。要的話：站主要部署什麼（哪個 PR／SHA）、要不要 `--force`、要不要 `--ignore-hold` | 用有選項的提問，不接受一句「好」 |
| 3 | 部署 | `host-deploy.sh`（背景），或站主自己跑一行 | `DEPLOY_EXIT=0`、腳本自己的 3/3 健康檢查過 |
| 4 | 驗證 | 一支唯讀腳本、一次 SSH 跑完：`.agents/skills/deploy/scripts/host-verify.sh`（live SHA、部署 log、容器與映像、alembic、health、首頁、公開站），再加這次 diff 專屬的檢查（抓一個新程式才有的字串或行為），寫法見 `post-deploy.md` | 每行 `PASS`、`TOTAL fail=0` 才算部署完成 |
| 5 | 收尾 | 把 SHA、耗時、有無 migration 寫進票或交接；內容匯入交給內容線；大功能上線後做 `post-deploy.md` 的三個問題 | 票或記憶有紀錄 |

## 指令

```bash
# 1 唯讀預檢（讀檔案，加兩句影片工作表的 select；加 --full 才看行程與容器，分類器擋的是後者）
MSYS_NO_PATHCONV=1 <SSH> -m .agents/skills/deploy/scripts/host-preflight.sh
MSYS_NO_PATHCONV=1 <SSH> "bash -s -- --full" < .agents/skills/deploy/scripts/host-preflight.sh
# 腳本自己的調查模式：只印會不會拒絕、原因是什麼，什麼都不做
MSYS_NO_PATHCONV=1 <SSH> "/root/deploy-travel-scanner.sh --dry-run"
# 3 部署（背景執行；旗標原樣傳給部署腳本）
MSYS_NO_PATHCONV=1 <SSH> "bash -s --" < .agents/skills/deploy/scripts/host-deploy.sh
MSYS_NO_PATHCONV=1 <SSH> "bash -s -- --force" < .agents/skills/deploy/scripts/host-deploy.sh
# 4 驗證：填入剛部署的 squash SHA，一支腳本一次 SSH 跑完（plink -m 不傳參數，所以用 sed 填）
TMP=$(mktemp -d)   # repo 外任何暫存目錄都行（Claude Code 用 session 的 scratchpad 也可以）
sed 's/^EXPECTED_SHA=""$/EXPECTED_SHA="<squash sha>"/' .agents/skills/deploy/scripts/host-verify.sh > "$TMP/verify.sh"
MSYS_NO_PATHCONV=1 <SSH> -m "$TMP/verify.sh" | grep -E '^(PASS|FAIL|TOTAL|SHA |WARN)'
# 只想看單項時的手動版
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

每次部署都重建所有從 repo 建置的容器（postgres、redis 以外全部，2026-10-05 是十二個應用容器加 `migrate`），只有文件的 commit 也一樣：建置內容沒變時快取全中、映像不會重做，但映像 ID 每次建置都會換新（主機用 containerd image store），compose 就把容器全部重建，原因見 `runbook.md`。所以 video-ai-worker 與 video-worker 每次都會重啟，進行中的付費影片工作會被打斷，部署前看預檢的「paid video work」。video-worker 被砍時拿著的專案鎖 `LEASE` 會留在影片的工作目錄；工人的 hostname 固定是 `video-worker`，新工人確認舊程序已結束後會接手，不用手動刪（`docs/videos/AUTOMATION.md`）。中間約 8 秒 502；hotspot-collector 重啟的第一輪會重算當天排行、也會跑 guide backfill（吃 YouTube 與 Brave 額度），所以同一天多次部署要集中。

## 規則在哪裡（不重抄）

| 問題 | 讀 |
| --- | --- |
| 兩條路徑、四把鎖、暫停檔的格式與 `hold.py acquire/verify/clear/show`、放棄一個發布的順序、不碰正式環境的驗證法 | `ops/release/README.md` |
| 自動部署 timer 的八道關卡、安裝與上線順序、狀態檔與暫停檔、怎麼停 | `ops/autodeploy/README.md`、程式在 `ops/autodeploy/autodeploy.py` |
| 後台部署中心（第三條路徑）的安裝、限制、狀態與 log | `ops/deployer/README.md`、程式在 `apps/api/deployment_agent/` |
| nginx 的四個專案檔、驗證步驟、access_log 與 error_log 的坑 | `ops/nginx/README.md` |
| CI 的四個必要檢查與怎麼可靠地讀 | `.github/BRANCH_PROTECTION.md` |
| 部署後的內容匯入 | `.agents/skills/content-pipeline/references/publish-runbook.md` |
| 這台主機踩過的坑 | `.agents/skills/deploy/references/pitfalls.md` |

## 這個 skill 的檔案

- `.agents/skills/deploy/references/preflight.md`：怎麼判斷暫停檔背後的發布是活的還是被遺棄的、清理的三種做法與各自要站主同意的地方。
- `.agents/skills/deploy/references/runbook.md`：腳本做了什麼、旗標、包裝腳本、讀 log、交給站主跑的一行指令長什麼樣、回滾。
- `.agents/skills/deploy/references/post-deploy.md`：驗證清單、`host-verify.sh` 怎麼用與怎麼加這次專屬的檢查、大功能上線後的三個稽核問題、邊緣層的假陽性檢查。
- `.agents/skills/deploy/references/pitfalls.md`：SSH、分類器、磁碟、腳本、nginx 的坑。
- `.agents/skills/deploy/scripts/host-preflight.sh`、`.agents/skills/deploy/scripts/host-deploy.sh`、`.agents/skills/deploy/scripts/host-verify.sh`：在主機上跑的 bash，不含任何憑證；`host-verify.sh` 只要填頂端的 `EXPECTED_SHA`（該 Up 的服務與 alembic head 都在主機上推出來），怎麼加這次專屬的檢查，見 `post-deploy.md`。
- `.claude/skills/deploy/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
