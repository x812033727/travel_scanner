---
id: 2026-09-13-web-upstream-keepalive-502
title: nginx 重用 Next.js 剛關掉的閒置連線，POST 零星回 502
status: in-progress
priority: P1
area: ops
owner: claude-opus-5
claimed_at: 2026-09-13T11:57:48Z
created_at: 2026-09-13T11:57:42Z
completed_at:
branch: claude/strange-lumiere-df2349
depends_on: []
scope:
  - ops/nginx/upstream-keepalive.conf
  - ops/nginx/mokaair.conf.example
  - ops/nginx/ci-validate.conf
  - ops/nginx/install.sh
  - ops/nginx/README.md
  - docker-compose.prod.yml
---

# nginx 重用 Next.js 剛關掉的閒置連線，POST 零星回 502

## Why

2026-09-13 11:22:11 UTC，站主在後台發布隱私權政策韓文版：
`POST /api/travel/admin/site-pages/privacy/publish?locale=ko`。瀏覽器顯示「請求失敗（HTTP 502）」，
重按一次就成功。站主當天在 `hostinger2` 上收集到的證據：

- nginx error.log 有 `upstream prematurely closed connection while reading response header from
  upstream`，upstream 是 `http://127.0.0.1:8091`，也就是 web 容器。
- API 容器沒有第一個 POST 的紀錄，只記到重試那次的 200。
- web 容器沒有重啟：`RestartCount=0`、`OOMKilled=false`、`StartedAt=11:10:07Z`。那次啟動來自 12 分鐘前的部署
  （`/root/deploy-logs/deploy_20260913_110839.log`）。

原因是 nginx 和 Node 關閒置連線的先後順序反了：

- 線上的 `/etc/nginx/sites-enabled/mokaair.com`（樣板是 `ops/nginx/mokaair.conf.example`）只寫了
  `upstream mokaair_web { server 127.0.0.1:8091; keepalive 32; }`，沒有 `keepalive_timeout`。nginx 因此把閒置的上游連線留
  **60 秒**。`proxy-headers.conf` 設了 `proxy_http_version 1.1` 與 `Connection ""`，所以連線池確實在用。
- Next.js standalone 的 `server.js` 只在設了 `KEEP_ALIVE_TIMEOUT` 時才改 `server.keepAliveTimeout`。16.3.3 的位置是
  `next/dist/build/utils.js:1127` 產生的樣板，以及 `next/dist/server/lib/start-server.js:248`。`ops/`、兩份 compose、
  `apps/web/Dockerfile`、`.env.example` 都沒設這個變數，所以用的是 Node 預設的 **5 秒**。
- Node 閒置 5 秒就關掉連線。nginx 若剛好在同一刻從池子拿這條連線送出請求，讀回來的就是 EOF。GET 會被 nginx 換一條連線重試，
  使用者看不到。POST、PATCH、LOCK 屬於 non-idempotent，送出後 nginx 不會重送（`proxy_next_upstream` 預設不含
  `non_idempotent`），於是直接回 502。所以使用者只會在 POST 上看到錯誤，而且是零星的。

Next.js 16.3.3 自帶的文件寫的正是這個情況：`node_modules/next/dist/docs/01-app/03-api-reference/06-cli/next.md`
的「Configuring a timeout for downstream proxies」一節。它要求 Node 的 keep-alive 逾時比前面那層 proxy **長**。

## Definition of done

- [ ] 閒置的上游連線一定是 nginx 先關，Next.js 那端不再主動關。
- [ ] 兩個修正任何一個先上線，一般情況下就已經成立。compose 那半跟著部署上線，nginx 那半要另外上機。
- [ ] 正式機上看得到兩半都生效（見 How to verify 的 A 與 D）。
- [ ] 部署與重啟視窗以外，error.log 不再出現 upstream 為 `127.0.0.1:8091` 的
      `upstream prematurely closed connection` 或 `Connection reset by peer`。

## Steps

- [x] `docker-compose.prod.yml` 的 web 加上 `KEEP_ALIVE_TIMEOUT: "65000"`，比 nginx 預設的 60 秒長。
- [x] 新增 `ops/nginx/upstream-keepalive.conf`，內容是 `keepalive 32;` 和 `keepalive_timeout 4s;`。4 秒比 Node 預設的 5 秒短。
- [x] `mokaair.conf.example` 的 upstream 改成 include 這個 snippet。`ci-validate.conf` 的 upstream 也 include，
      讓 CI 的 `nginx -t` 真的在 upstream context 裡驗到這兩行。
- [x] `install.sh` 安裝這個 snippet。沒有任何已啟用的設定 include 它時，印出提醒。
- [x] `README.md`：表格補一列，補上升級說明與驗證步驟。
- [x] 本機實測 Next 16.3.3 standalone 真的會讀 `KEEP_ALIVE_TIMEOUT`。
- [x] 查 API 那一跳有沒有同樣的問題。
- [ ] **需要站主同意**：部署（compose 那半）。
- [ ] **需要站主同意**：主機 nginx。staging 和 reload 分成兩次呼叫。
- [ ] 上機後照 How to verify 驗證，把結果寫回這裡。

## How to verify

### Repo 端

```bash
npm run check:tasks && npm run test:tools
bash -n ops/nginx/install.sh
# 下面兩行由 CI 的 containers job 執行（本機沒有 docker）
docker run --rm -v "$PWD/ops/nginx:/etc/nginx/ops:ro" nginx:1.28-alpine nginx -t -c /etc/nginx/ops/ci-validate.conf
docker compose -f docker-compose.prod.yml config --quiet
```

### 正式機（**沒有站主同意不要做**）

主機是 `hostinger2`：nginx 1.28.3、4 個 worker，`127.0.0.1:8090` 和 `8091` 由 docker-proxy 監聽。
依 A → B → C → D 的順序做。**B 和 C 必須是兩次各自獨立的指令呼叫。**以前把上傳、寫 `/etc/nginx` 和
`systemctl reload nginx` 放在同一次呼叫裡被擋過，拆開後就能執行。

**A. 部署（compose 那半）。**執行 `/root/deploy-travel-scanner.sh`，然後：

```bash
curl -sI http://127.0.0.1:8091/ | grep -i '^keep-alive:'     # 應該是 timeout=65；修正前是 timeout=5
```

**B. nginx staging（一次呼叫）。**做完 A 之後，`/root/travel_scanner/ops/nginx` 已經是新版，不用另外上傳。
如果想在合併前先上 nginx，就用 `pscp` 把這個分支的 `ops/nginx/` 傳到 `/root/nginx-staging-<ts>/`，
再把下面的 `cd` 改到那個目錄。

```bash
set -euo pipefail
ts=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p /root/nginx-backups/$ts && cp -a /etc/nginx /root/nginx-backups/$ts/etc-nginx
cd /root/travel_scanner/ops/nginx
test -f upstream-keepalive.conf
# install.sh 也會重寫另外兩個檔案。線上版本必須和 repo 完全相同；cmp 失敗就先停下來比對差異。
cmp 10-rate-limit.conf /etc/nginx/conf.d/mokaair-rate-limit.conf
cmp proxy-headers.conf /etc/nginx/snippets/mokaair-proxy-headers.conf
seeded=0; [ -e /etc/nginx/sites-available/mokaair.conf ] || seeded=1
bash install.sh     # 這時還沒有 include，所以會印出提醒，是預期行為
# 這台主機啟用的是 mokaair.com。install.sh 會補種一份沒有啟用的 mokaair.conf 空殼
# （見 2026-09-12-nginx-deploy-checks-false-pass 第 1 點），這次補種的就刪掉。
if [ "$seeded" = 1 ]; then rm /etc/nginx/sites-available/mokaair.conf; fi
site=/etc/nginx/sites-available/mokaair.com
test "$(grep -c '^[[:space:]]*keepalive 32;' "$site")" = 1
sed -i 's|^\([[:space:]]*\)keepalive 32;$|\1include /etc/nginx/snippets/mokaair-upstream-keepalive.conf;|' "$site"
grep -n -A3 'upstream mokaair_web' "$site"
nginx -t
echo "backup: /root/nginx-backups/$ts/etc-nginx"
```

**C. reload（另一次呼叫）。**

```bash
systemctl reload nginx && systemctl is-active nginx
```

**D. 驗證（再另一次呼叫）。**`nginx -T` 讀的是磁碟上的檔案，所以還要實際看一條連線是被哪一端關掉的：

```bash
nginx -T 2>/dev/null | grep -E 'mokaair-upstream-keepalive|keepalive_timeout 4s'
curl -s -o /dev/null --resolve mokaair.com:443:127.0.0.1 https://mokaair.com/zh-TW
ss -tn state established '( dport = :8091 )'     # 記下 nginx 這端的 local port
sleep 8
ss -tan '( dport = :8091 )'     # 同一個 port 出現在 TIME-WAIT：nginx 先關的。一定要加 -a
ss -tan '( sport = :8091 )' | grep -v LISTEN     # 修正前 TIME-WAIT 出現在這裡（docker-proxy 那端）
```

**長期看 log。**只有部署或重啟的那一分鐘（同一分鐘也會有 `Connection refused`）才應該看到這兩種錯誤：

```bash
zcat -f /var/log/nginx/error.log* | grep 'upstream: "http://127.0.0.1:8091' \
  | grep -E 'prematurely closed|reset by peer' | cut -c1-19 | sort | uniq -c
```

**回滾。**執行 `cp -a /root/nginx-backups/<ts>/etc-nginx/. /etc/nginx/ && nginx -t`，
再用另一次呼叫執行 `systemctl reload nginx`。多出來的 `snippets/mokaair-upstream-keepalive.conf`
沒有被 include，留著無害。compose 那半跟著部署腳本的回滾一起還原。

## Notes

### 正式機上查到的事（2026-09-13，唯讀）

- **修正前，閒置連線確實是 web 那端先關。**從主機打一次 `/zh-TW` 後，nginx 手上有 `127.0.0.1:58596` 和 `:58600`
  兩條到 8091 的連線。8 秒後，nginx 那端兩條都不見了；docker-proxy 那端（`127.0.0.1:8091` → `58596`、`58600`）則在
  TIME-WAIT，代表主動關閉的是 web 那一側。
- **`ss -tn` 預設不列 TIME-WAIT。**同一時刻 `ss -tn` 數到 0 列，`ss -tan` 數到 4 列。README 和上面 D 的檢查
  一定要加 `-a`，否則修好之後也會被誤讀成兩半都沒生效。這是第一次在主機上試跑時抓到的。
- **從 08-31 到現在，部署與重啟視窗以外只有這一次。**8091 上的 `prematurely closed` 和 `reset by peer` 共 60 筆，
  除了 11:22:11 那筆 POST，其餘都落在同一分鐘有 `Connection refused` 的時段，或 `deploy_20260906_131448` 之內。
  09-09 01:16 和 09-11 04:04 沒有部署紀錄，但同一分鐘也有 refused，是手動重啟。這是罕見的競態，不是每天發生；
  靠 log 驗收要看幾週，不是幾小時。
- **web 容器在 11:21:00–11:23:30 之間一行 log 都沒有。**沒有例外，也沒有崩潰，符合「請求根本沒進到 Node 的 HTTP parser」。
- 線上 nginx 只有 `mokaair_web` 一個 upstream，所有 `proxy_pass` 都指向它。nginx **沒有**直接代理 API（8090），
  和樣板的規定一致。
- web 映像是 `NODE_VERSION=22.23.2`。8090 和 8091 由 docker-proxy 監聽（`daemon.json` 沒有 `userland-proxy`，
  所以是預設開啟）。Node 關閉連線後，要經過 docker-proxy 才會變成送給 nginx 的 FIN 或 RST，所以同一種競態在 log 裡
  兩種訊息都可能出現。

### 本機實測（Next 16.3.3 standalone、Node 24.13）

直接啟動 `.next/standalone` 的 `server.js`，用 raw socket 送一個請求，量伺服器多久後關閉閒置連線：

- 沒設 `KEEP_ALIVE_TIMEOUT`：回應帶 `Keep-Alive: timeout=5`，**6007 ms** 後關閉。Node 24 的
  `keepAliveTimeoutBuffer` 會多加 1 秒；Node 22.23.2 有沒有這 1 秒沒驗證，不影響結論。
- `KEEP_ALIVE_TIMEOUT=65000`：回應帶 `Keep-Alive: timeout=65`。閒置 **62 秒**後在同一條連線送第二個請求，照樣回 200
  （`headersTimeout` 的 60 秒不會作用在閒置連線上）。之後 **66004 ms** 關閉。

### API 那一跳（BFF → uvicorn）

結構一樣，但先後順序是對的，不用改：

- 客戶端是 Node 內建的 `fetch`（undici），`apps/web` 沒有自訂 dispatcher。實測 undici 7.18.2 閒置 **4018 ms**
  後由客戶端先關。
- 伺服器是 uvicorn 0.52.4（見 `uv.lock`），`timeout_keep_alive` 預設 **5 秒**。uvicorn 不送 `Keep-Alive`
  標頭，所以 undici 不會把自己的 4 秒拉長。
- `app/api/travel/[...path]/route.ts` 對非 SSE 的回應會整包讀完才回傳，不會出現「伺服器早就寫完、客戶端還沒讀完」的時間差。
- 如果真的是這一跳出事，BFF 會自己回一個 `502 upstream_unavailable` 的 JSON，nginx error.log 不會有紀錄。
  11:22 那次 nginx 有紀錄，所以不是這一跳。

### 決定

- **兩半都做。**compose 那半跟著一般部署上線，nginx 那半要站主另外上機，所以不論哪一半先上，都應該單獨有效。
  但 nginx 的 4 秒單獨上線時仍有漏洞：Node 在最後一個 byte 交給 kernel 時就開始計時，而未緩衝的 `/api/` 回應遇上慢客戶端時，
  nginx 可能晚好幾秒才讀完。Node 的 65 秒補上這個洞。
- **拆成 snippet，而不是直接改樣板裡的 upstream。**`install.sh` 從不動 site 設定檔，CI 的 `nginx -t` 也不讀
  `mokaair.conf.example`。直接改樣板的話，上機跑 `install.sh` 什麼都不會發生，CI 也驗不到那一行。放進 snippet 後，
  CI 會在真正的 upstream context 裡驗它，之後的調整也跟著 `install.sh` 上機。代價是既有主機要一次性把 `keepalive 32;`
  換成 include，`install.sh` 會提醒。
- **不要用 `proxy_next_upstream ... non_idempotent` 來修。**那會讓 nginx 重送應用程式可能已經處理過的 POST，
  造成重複發布或重複建立。
- **`install.sh` 的提醒用 `grep -R`（會跟著 symlink 走）。**`sites-enabled/` 裡放的是 symlink，用 `-r` 會漏看。
  已在 WSL 裡用假的 `/etc/nginx` 跑過四種情境：新主機、舊的 site 檔、改好之後、被註解掉的 include。也確認過把 `-R`
  改成 `-r` 時，測試會失敗。

### 不在這張票：部署本身造成的 502

每次部署，compose 都會重建所有容器。站主觀察到 11:10:06–11:10:14 約 8 秒的 502；error.log 在 11:09:53–11:10:08
之間有 12 筆 POST 和 15 筆 GET 被重設或提早關閉，11:10 那一分鐘另有 10 筆 `Connection refused`。AdSense 的爬蟲
（Mediapartners-Google）也碰到了這幾秒的 502。要消除它，需要 web 容器滾動更新，或在 nginx 端等待後重試，是另一件事。
