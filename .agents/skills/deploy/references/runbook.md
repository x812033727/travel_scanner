# 部署 runbook

## 腳本做什麼

`/root/deploy-travel-scanner.sh`（root、mode 700、在 git work tree 之外）自 2026-09-03 起包了整個流程：`umask 022`、取 `/var/lock/travel-scanner-deploy.lock`、守門（暫停檔與規則 1，見 preflight.md）、`git fetch`、`git merge --ff-only origin/main`（記下舊 SHA）、只在 incoming commit 動到 migrations 時 `pg_dump -Fc`、`ensure_readable`（把 apps ops tools docs tasks 底下不可讀的檔案與目錄修回 644／755，`.env` 不動）、`docker compose -f docker-compose.prod.yml --profile hotspots up --build -d`、連續三次內部健康檢查、失敗就自動回滾（`git reset --hard` 舊 SHA 再重建，回滾也會再跑一次 `ensure_readable`）、log 寫到 `/root/deploy-logs/`。

`--profile hotspots` 很重要：`hotspot-collector` 在 compose 裡掛在這個 profile 底下，README 裡的示範指令沒帶它，照抄會默默少一個服務。腳本已經帶了。`news` 與 `video` 服務也各掛在自己的 profile（見 `docker-compose.prod.yml`），主機腳本 2026-09-24／25 起也帶 `--profile news` 與 `--profile video`；腳本不在 git 裡，有疑問就在主機上 `grep -- --profile /root/deploy-travel-scanner.sh`。

順序規則（`README.md` 與 `docs/article-architecture.md`）：migration → API → web；API 先或一起，永遠不要讓 web 單獨領先一個新增操作的 API 改動。一次性腳本一起重建所有容器所以自然符合；分階段驅動要自己守。

**為什麼每次都全部重建**：腳本沒有 `--force-recreate`，是 `up --build -d` 自己決定的。建置內容沒變時快取全中，映像的 `Created` 與 layer 都跟上次一樣，但映像 ID 是新的：主機是 Docker 29 加 containerd image store（`docker info` 的 `driver-type` 是 `io.containerd.snapshotter.v1`），映像 ID 是 OCI image index 的 digest（`docker image inspect -f '{{json .Descriptor}}'` 的 `mediaType` 是 `…image.index.v1+json`），每次建置都換，compose 看到 ID 變了就重建容器。2026-10-05 只改 skill 文件的 363489fe9，log 裡 postgres、redis 以外每個容器（含 `migrate`、video-ai-worker、video-worker）都是 `Recreate`，前後兩個 api 映像的 `Created` 都是 02:10:44.89Z（上一次真正建置的時間），ID 從 `67929f47…` 換成 `9e5d4be0…`。所以「只有文件，不會打斷工人」不成立：部署前看預檢的 `paid video work`（preflight.md）。

## 旗標

| 旗標 | 意思 |
| --- | --- |
| （無） | origin/main 比 live 新就部署，否則什麼都不做 |
| `--dry-run` | 只調查：會不會被拒、拒的理由、有沒有新 commit |
| `--force` | 重建目前的 commit（修完檔案權限、換了 `.env` 之後用） |
| `--no-rollback` | 失敗時不回滾，留現場給人看 |
| `--ignore-hold` | 無視暫停檔與規則 1，印 WARNING。只在站主決定之後用 |

## 用包裝腳本跑

```bash
MSYS_NO_PATHCONV=1 <SSH> "bash -s -- [--force] [--no-rollback] [--ignore-hold]" < .agents/skills/deploy/scripts/host-deploy.sh
```

包裝腳本先自己檢查：暫停檔存在而沒帶 `--ignore-hold` 就 `exit 9`；鎖被佔就 `exit 9`。然後用 nohup 起部署腳本、等它結束、把 buildkit 的 `#N` 行濾掉印最後 60 行、印 `DEPLOY_EXIT=<code>`。SSH 中途斷線時部署照樣跑完，log 在 `/root/deploy-logs/wrapper-<ts>.log`。

同一個目錄裡的 `auto-<ts>.log` 與 `auto-verify-<ts>.log` 是自動部署 timer（`ops/autodeploy/README.md`）跑同一支腳本與 `host-verify.sh` 留下的，`button-<ts>.log` 是 timer 替後台按鈕跑的，內容格式一樣；分辨一次部署是人跑的、時段內自動的還是按鈕的，看檔名前綴。`journalctl -u travel-scanner-autodeploy` 有每一輪的關卡決定。

一定用 Bash 工具的 `run_in_background`，等完成通知；輸出檔在結束前是空的（`tail` 會緩衝），空檔不代表卡住。

## 分類器擋下來的時候

auto 模式的分類器自 2026-09-18 起會擋部署呼叫，不管是 `-m 檔案` 還是 inline；換寫法重試會被標成 Auto-Mode Bypass，而且整個 session 都記得。正確順序：

1. 第一次就先把 session 切到 Manual（`set_session_permission_mode` → `default`，往低切不需要核准卡），送同一個指令，站主按允許。站主也能自己切：送出鈕旁的模式選單或 `Ctrl+Shift+M`（Manual＝default）。部署完請站主切回 Auto。
2. 或交給站主在自己的終端跑一行（Windows PowerShell 5.1 的形狀）：`& "<plink.exe 的路徑>" -batch -load <PuTTY session> -l root -i "<金鑰 .ppk>" /root/deploy-travel-scanner.sh`。金鑰路徑與 session 名稱只在站主自己的機器上。
3. 唯讀的調查（`-m` 送純讀檔的腳本）以前都過，但 2026-09-24 起連 plink 跑的唯讀預檢也曾被擋成 Production Reads：先問站主要不要部署，要就在預檢之前切 Manual。讀 `~/.claude/settings*.json` 找既有規則也曾被擋，不要花回合在被擋的路上。

## 跟自動部署 timer 共存

timer 開著時，合併的 commit 在下一個部署時段（`AUTODEPLOY_DEPLOY_WINDOWS`，站主定案台灣 04:30–06:00，一天最多一次）自動部署並驗證；時段外的 tick 記 `wait: schedule`，當天已部署過記 `wait: daily_limit`。多數「部署某個已合併的 PR」不必手動做：看 `state.json` 的 `last_deploy.sha`，或等預檢的 `last auto deploy` 出現那個 SHA。等不到時段時，先請站主在 `/admin/deployments` 按「部署最新版本」（只有 owner 能按；timer 約 5 分鐘內接手，跳過時段與每日上限，其餘關卡照走），這比開 SSH 少一次被分類器擋的機會。要手動部署時：

0. 後台按鈕的請求在跑時，`deployment_runs` 有一筆 `preflight`／`building`／`verifying` 的 run，timer 也持有部署鎖；等它結束。

1. 預檢的 `tick=active` 代表一輪正在部署，等它結束（它持有部署鎖，`host-deploy.sh` 本來就會拒絕）。
2. `--force` 重建目前 commit、`--ignore-hold` 這類 timer 不會做的事才需要手動；手動跑完 timer 的下一輪看到 live 等於 origin/main 就什麼都不做。
3. 分階段發布：驅動的暫停檔（`hold.py acquire`）同樣擋 timer（它跑 `--dry-run` 看到 exit 3 就等），不用另外關 timer；但 `clear` 之後下一輪 timer 就會部署當時的 main，發布目錄的基準就對不上了，所以 `clear` 要在最後一個階段成功之後，不要提早。

### 後台按鈕被拒絕時怎麼讀

按鈕請求的 run 標成 `failed` 時，`failure_code` 是固定字串（全表在 `ops/autodeploy/README.md` "The admin button"）。最常見的幾個：

| failure_code | 意思 | 怎麼辦 |
| --- | --- | --- |
| `deployment_autodeploy_paused` | 自動部署暫停檔存在 | 照 `preflight.md` 的「自動部署的暫停檔」讀 log、修好、刪檔；站主規定不能強制部署 |
| `deployment_hold_active` | 部署暫停檔或規則 1（分階段發布） | 照 `preflight.md` 判斷那個發布是活的還是被遺棄的 |
| `deployment_ci_not_green` | main 的 CI 還沒綠或紅了 | 等 CI，或先修紅燈 |
| `deployment_paid_work_running` | 有付費影片工作在跑 | 等它結束，或站主取消勾選「先等」再按 |
| `deployment_dry_run` | timer 還在乾跑（`AUTODEPLOY_ENABLED=false`） | 正常；detail 寫著會部署哪個 SHA |
| `deployment_executor_unavailable` | 10 分鐘沒人接單 | timer 沒裝、停了或主機有事：`systemctl status travel-scanner-autodeploy.timer` |
| `deploy_script_exit_<n>` | 腳本失敗，已回滾並寫暫停檔 | 讀 `button-<ts>.log`，同自動部署失敗 |

## 回滾

- 部署失敗：腳本自己回滾到舊 SHA 並重建；看 log 尾端與 `DEPLOY_EXIT`。
- 部署成功但功能壞：在 main 上 revert 再部署一次，不要手改主機的 work tree（腳本的 preflight 拒絕髒的 work tree，`git status --porcelain` 必須是空的）。
- 資料庫：腳本只在有 migration 時備份；分階段驅動在 activate 時做 `pg_dump`。回復用 `pg_restore` 到容器內的 postgres，要站主同意。
- nginx：`/root/nginx-backups/<ts>/etc-nginx` 整份 `cp -a` 回去，`nginx -t && systemctl reload nginx`（reload 與寫檔分成兩個呼叫，分類器對綁在一起的那種會擋）。

## 部署後接著做的事

- 內容包跟程式一起上去了，但沒匯入就不會上線：照 `.agents/skills/content-pipeline/references/publish-runbook.md`。
- 主機 nginx 的四個專案檔如果這次 PR 有改：`sudo bash ops/nginx/install.sh` → `nginx -t` → 另一個呼叫 `systemctl reload nginx`；站台檔 `sites-enabled/mokaair.com` 要手動 merge，`install.sh` 不動它。
- `ops/release/` 的測試 CI 不跑：改到 `hold.py` 時本機 `python -m unittest discover -s ops/release -v`。

## 磁碟

映像與建置快取在 `/var/lib/containerd`（containerd image store），不在 `/var/lib/docker`。每次部署與每個分階段發布都留下 `travel-scanner-{api,web}:<sha40>` 標籤，`docker image prune` 動不了有標籤的映像。2026-09-21 實測：刪 180 個舊標籤只回收 11 GB，`docker builder prune -af` 回收 121.6 GB，站台全程不受影響，之後冷建置 4 分 23 秒、快取回到 3 GB。安全的映像刪法：用 `docker ps -aq | xargs docker inspect -f '{{.Image}}'` 保護所有容器（含停止的）用到的映像 ID 與 `:local`，其餘分批 20 個刪，失敗的那批逐一重試找出壞的。清 `/root/mokaair-*` 舊目錄時只挑 `-type d`，40 個鬆散檔案裡有驅動的鎖與腳本；先把清單寫進 `/root/deploy-logs/purge-<date>.log` 再刪。
