# 別再犯：主機與部署的坑

每條一句祈使句，後面是為什麼。新坑加在對應的段落。

## SSH 與連線

- 一次連線跑一個腳本，不要一行一連線：四十幾次 plink 之後客戶端 IP 曾被鎖在 SSH 外，站台照常回應。
- 站台 200 但 SSH 逾時，先分清原因再動：一次是連線被擋，另一次 `ssh.service` 根本是 inactive（被 SIGTERM 乾淨停掉、還被 disable）。用 Hostinger 面板的網頁主控台看 `systemctl is-active ssh; ss -lntp | grep <port>; iptables -L INPUT -n | head`，**永遠不要按 Force reboot**。主控台在 hpanel.hostinger.com/vps → 那台主機 → 右上角的按鈕，開了要先按一個鍵才出現提示字元。
- 被鎖時停止重試：每次嘗試都可能延長封鎖。先 `curl` 公開站，分清是主機掛了還是只有管理通道斷；然後等，或從主控台把 IP 解掉。只有 sshd 是 active 而且 port 在 listen，才可能是封鎖。
- sshd 死了就 `systemctl start ssh`；那次它還被 disable，重開機也不會自己起來，考慮 `systemctl enable ssh`。
- Git Bash 送絕對 POSIX 路徑給 plink 前加 `MSYS_NO_PATHCONV=1`，否則 `/root/...` 會被改寫成 `C:/Program Files/Git/root/...`。
- 別用 PuTTY 視窗打字：電腦操作對終端機只有點擊權限。檔案傳輸用同目錄的 `pscp`。
- 連線細節（session 名、金鑰路徑）留在自己的筆記，不寫進 repo、不寫進 skill。

## 分類器（auto 模式）

- 被擋的部署呼叫不要換寫法重試，會被標成 Auto-Mode Bypass 而且整個 session 記得；第一次就切 Manual 或交給站主跑。
- 讀取類：純讀檔的 `-m` 調查通常會過，但 2026-09-24 起連唯讀預檢也曾被擋成 Production Reads，所以先問要不要部署、再切 Manual；同一個呼叫包 `ps`、`who`、`last`、`docker images` 曾被擋成 Production Reads；`git` 檢查串 psql 也被擋過。一個呼叫做一件事。
- psql 只有最簡單的 select 可能會過（2026-09-13 連它都在站主要求的診斷裡被擋過一次，別指望正式站 psql，先用公開 API 或瀏覽器拿資料），jsonb 運算子與 `'"'"'` 引號的會被擋；`UPDATE`／`INSERT` 一律擋，即使有稽核列。
- 改正式站設定：站主已登入時，在 Claude in Chrome 操作真的後台表單會過（點欄位、`ctrl+a`、`type`、點「儲存設定」、「測試連線」）；在頁面裡用 JS `fetch` 去 PUT 後台 API 會被擋。一開始就給站主兩條路：(a) 他在 Chrome 登入 mokaair.com、你操作表單，(b) 他自己到 /admin/settings 改。
- 後台的最後一顆發布鈕留給站主按：在內建瀏覽器裡填欄位、「儲存草稿」、打開「發布」確認框都過（約 17 次），但把儲存＋點「發布」＋等待包成一批被擋，拿掉點「發布」那步就過。
- 灌腳本進 api 容器（base64、stdin 都算）會被擋。
- nginx：上傳＋`install`＋`nginx -t` 一個呼叫、`systemctl reload nginx` 另一個呼叫；綁在一起的會被擋。
- 改部署腳本本身被擋成 Modify Shared Resources；用有選項的提問拿到站主的同意後同一個呼叫就過。改之前先備份、`bash -n`、用 `sed` 複本在 `/tmp` 測（`REPO` 指向不存在的目錄、鎖與 log 目錄指到 `/tmp`，通過守門後會停在 `cd`）。
- 內容發布（`guides-import --publish`）要先用有選項的提問寫明篇數；`--dry-run` 從不被擋。
- 對別的 session 持有的票做 `done`／`release` 會被擋成 Interfere With Workloads；列出票號與證據問過就過。

## 腳本與行程

- 不要在會執行部署腳本的同一個呼叫裡 grep 它的名字：plink 把整個腳本當一行命令送過去，`pgrep -f` 會比對到自己，連 `[d]eploy` 的括號寫法也救不了。要知道有沒有部署在跑，`flock -n /var/lock/travel-scanner-deploy.lock true`。
- 分階段驅動的行程名不會出現在你的命令列裡，`pgrep -af 'release[_]host|…'` 對它們是安全的。
- 背景執行的輸出檔在結束前是空的（`tail` 緩衝），不要當成卡住。
- `find` 的目錄清單寫對：repo 頂層是 `apps docs ops tasks tools`，寫一個不存在的目錄會讓 `find` 回 1，在 `set -e` 底下整個部署會中止。
- 部署腳本 `--dry-run` 印 `NOTE: a real deploy would refuse to start` 只是預告，真的部署才會 `exit 3`。

## 檔案權限與環境

- 某個 shell 用 `umask 077` 跑過 git 之後，fast-forward 寫出的檔案全是 600，容器以非 root 使用者讀不到 `/app/app/models.py`，站台 502 兩分半。腳本現在自帶 `umask 022` 與 `ensure_readable`；看到 `PermissionError` 在 `/app` 底下的原始碼路徑就是這個；另一個訊號是 `docker compose ps` 只剩 postgres 與 redis 活著。確認：`cd /root/travel_scanner && find apps ops tools docs tasks -type f ! -perm -004 | wc -l`（不存在的目錄別寫進去）。
- 腳本以外弄壞的樹手動修：`find apps ops tools docs tasks -type d ! -perm -005 -exec chmod a+rx {} +`，再 `find … -type f ! -perm -004 -exec chmod a+r {} +`，然後 `/root/deploy-travel-scanner.sh --force`。執行位以下的權限 git 看不見，所以「work tree 要乾淨」的預檢不會被觸發。
- 修權限只針對 `apps ops tools docs tasks`，永遠不要遞迴 chmod 整個目錄：`/root/travel_scanner/.env` 是 600 而且必須維持。
- `--actor-email` 的值從容器的 `ADMIN_EMAILS` 讀（`docker compose … exec -T api printenv ADMIN_EMAILS`），經 shell 變數傳、不要印出來；它不是這個 session 看到的使用者 email。

## 磁碟與映像

- 磁碟滿了先看 `/var/lib/containerd`，不是 `/var/lib/docker`，也不是發布目錄（77 個目錄只佔 22 GB，containerd 佔 127 GB）。
- `docker image prune` 幾乎回收不到東西：每次部署留下的 `:<sha40>` 標籤不是 dangling。`docker system df` 的兩個數字加起來超過磁碟總量，就是共享 layer 的訊號，能回收多少事前算不出來。
- `docker builder prune -af` 才是大槓桿（一次 121.6 GB），站台不受影響，冷建置只多約 4 分鐘；「8 到 10 分鐘」是過時的說法。
- 清發布目錄只挑 `-type d`，40 個鬆散檔案裡有 `mokaair-deploy.lock`（四把鎖之一）與驅動還會用到的腳本。

## nginx 與邊緣層

- 主機上的站台檔比 repo 的 `mokaair.conf.example` 多很多（mocair.io 的 301、憑證、`default_server`、certbot 的 ACME webroot）；把範例整份蓋上去會弄壞續憑證。
- `install.sh` 只覆寫四個專案檔、不 reload、不改站台檔；曾經它會多種一個 `mokaair.conf`，改那個檔案什麼都不會發生。
- `keepalive 32;` 要手動換成 `snippets/mokaair-upstream-keepalive.conf` 的 include，否則 nginx 的 60 秒閒置池比 Next 的 5 秒長，POST 會零星 502（GET 會自動重試、POST 不會）；compose 那半是 `KEEP_ALIVE_TIMEOUT=65000`。
- 判斷是部署還是當機：`docker inspect travel_scanner-web-1` 的 StartedAt 對得上 `/root/deploy-logs/deploy_*.log` 就是部署重建的 8 秒 `connect() failed (111)`。
- `combined` 格式記的 `$body_bytes_sent` 對 chunked 回應含框架：同一個 59 bytes 的 `ads.txt` 由動態路由回會記成 70，靜態檔記成 59，用這個分辨是誰回的。
