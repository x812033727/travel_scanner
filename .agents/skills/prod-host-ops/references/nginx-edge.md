# nginx 邊緣層：看、改、證明

安裝步驟與每個驗證的完整腳本在 `ops/nginx/README.md`；這裡是在正式主機上操作時要知道的事，以及那份清單上會騙人的地方。

## 主機上長什麼樣

| 東西 | 在哪裡 |
| --- | --- |
| 站台檔 | `/etc/nginx/sites-available/mokaair.com`（`sites-enabled/` 連過去）。**改這個檔**；不要另外放一個 `mokaair.conf`，nginx 不會讀它 |
| 專案擁有的四個檔 | `conf.d/mokaair-rate-limit.conf`、`conf.d/05-mokaair-crawler-ranges.conf`、`snippets/mokaair-proxy-headers.conf`、`snippets/mokaair-upstream-keepalive.conf`，由 `ops/nginx/install.sh` 覆寫（冪等、不 reload、不碰站台檔） |
| 站台檔獨有的東西 | `mocair.io`／`www` 的 301 與各自的憑證、`default_server`、內嵌的 `ssl_protocols`／`ssl_ciphers`、port 80 上 certbot 的 ACME webroot。`ops/nginx/mokaair.conf.example` 是合併來源，**不能整份蓋過去**（`/.well-known/` 會被導到 Next，續憑證就壞了） |
| 前面有沒有 CDN | 沒有：`curl -sI https://mokaair.com` 回 `Server: nginx`、沒有 `cf-ray`／`via`／`x-served-by`，所以 `real_ip` 區塊保持註解。哪天有了 CDN，`$remote_addr` 會變成 CDN 的出口位址，所有限流都失去意義 |

改站台檔前先備份整個 `/etc/nginx`（`cp -a /etc/nginx /root/nginx-backups/<時間>/`），回滾是 `cp -a <備份>/. /etc/nginx/` 再 `nginx -t && systemctl reload nginx`。上傳＋`install`＋`nginx -t` 一次呼叫，`systemctl reload nginx` 另一次呼叫（分類器會擋綁在一起的，見 skill `deploy`）。reload 要站主同意。

## 限流區與豁免

`ops/nginx/10-rate-limit.conf` 定義、站台檔使用：

| 區 | 速率 | 用在 |
| --- | --- | --- |
| `mokaair_content_pages` | 每位址 5 r/s，`burst=20 nodelay` | `location /`（頁面）。已驗證的爬蟲在這區的 key 是空的，不計 |
| `mokaair_crawlers` | 每位址 30 r/s，`burst=60` | 同一個 `location /`，只有 `$mokaair_verified_crawler` 為 1 的位址有 key |
| `mokaair_api` | 10 r/s，`burst=20` | `location /api/` |
| `mokaair_conns` | 每位址 20 條連線（`limit_conn`，server 層） | 全部，**包括已驗證的爬蟲** |

不限流：`/_next/static/`、`/brand/`、`/api/line/webhook`、`/.well-known/`，以及五個爬取控制路徑 `/robots.txt`、`/ads.txt`、`/sitemap.xml`、`/llms.txt`、`^~ /sitemaps/`。`limit_req` 與 `limit_conn` 都回 429。文章圖片 `/guides/<slug>/<file>.(webp|jpg|png|svg)` 在頁面區的 key 也是空的。

爬蟲網段由 `tools/nginx-crawler-ranges.mjs` 從 googlebot.json、special-crawlers.json（Search Console 的即時測試從這裡來）與 bingbot.json 產生：`node tools/nginx-crawler-ranges.mjs > ops/nginx/05-crawler-ranges.conf`，commit 差異，再用 `install.sh` 裝上主機。沒有執行期抓取，網段會過期，所以隔一陣子重跑。**豁免永遠依位址，不依 User-Agent**。`/ads.txt` 不靠網段：它有自己的 `location`，因為一個 429 在 AdSense 眼裡就是「這個網站沒有 ads.txt」。

## 四個 log，各記什麼

| log | 記什麼 | 用途 |
| --- | --- | --- |
| `/var/log/nginx/mokaair-limit.log` | 每一次限流事件（`limiting requests` 或 `limiting connections`），有區名、位址、請求，**沒有 UA** | 誰被擋、被哪個區擋 |
| `/var/log/nginx/mokaair-limited.log` | 所有 429，格式 `mokaair_limited`，**有 UA** | 抓冒名爬蟲 |
| `/var/log/nginx/mokaair-crawl.log` | 五個爬取控制路徑的所有請求（`combined`） | 「Google 有沒有來、拿到什麼」 |
| `/var/log/nginx/access.log` | **只有** `www`、`mocair.io`、port 80 那幾個 server block | 主站的正常請求不在這裡 |

主站的正常 200 請求**哪裡都沒有記**：server 層的 `access_log` 會取代繼承來的那一條，所以加了只記 429 的條件式 log 之後，主站就只剩被拒的與爬取控制的請求。任何看起來像「某爬蟲從某天起就沒來過」的結論，先確認那段時間 log 有沒有在記。要記別的東西，在同一層**再加一條** `access_log`（同層兩條都生效），不要只放一條。`error_log` 同理：站台檔 server block 裡要有 `error.log error;` 與 `mokaair-limit.log warn;` 兩條，只放第二條會讓真正的錯誤不再進 `error.log`。

`combined` 記的 `$body_bytes_sent` 對 chunked 回應含框架：同一份 59 bytes 的 `ads.txt`，動態路由回的記成 70，靜態檔記成 59，可以從 log 分辨是誰回的。

## 會通過、但什麼都沒證明的檢查

| 看起來像 | 實際上 | 改用 |
| --- | --- | --- |
| `grep 'limiting requests' /var/log/nginx/error.log` 空的 → 沒人被擋 | `nginx.conf` 的 `error_log` 沒寫等級＝`error`，`warn` 等級的限流事件全被丟掉 | 讀 `mokaair-limit.log`，並先確認 `nginx -T \| grep -c mokaair-limit.log` ≥ 1 |
| 429 的數量 ≠ `grep -c 'limiting requests'` → 有問題 | `limit_conn` 也回 429，但記成 `limiting connections by zone "mokaair_conns"` | 兩個字串都數 |
| `seq 1 80 \| xargs -P 8 curl …/zh-TW` 全 200 → 限流壞了 | 8 個併發打 1.5 秒的頁面約 5.3 r/s，正好是區的速率，`burst=20` 永遠吸收得掉 | `(for i in $(seq 1 40); do curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/zh-TW & done; wait) \| sort \| uniq -c`，應該看到約 20 個 429 |
| `zgrep -i googlebot … \| awk '$9==429'` 有 20 筆 → Googlebot 被擋 | UA 是任何人都能填的：當時 13 筆是自己的稽核機器帶 `-A Googlebot`，7 筆是冒名的憑證掃描器；真的 Googlebot／Bingbot 是零 | 按 `$1`（來源位址）分組，對照公布的網段再下結論；`mokaair-limited.log` 有 UA 可交叉看 |
| 偽造位址的 Redis 檢查 `forged: 0` → 通過 | api 容器沒有 `PUBLIC_READ_RATE_LIMIT_MODE`（或是 `off`）時，根本沒有東西在寫 `rate:public-read-ip-minute:*`，永遠是 0 | 先 `docker compose -f docker-compose.prod.yml exec -T api sh -c 'printenv PUBLIC_READ_RATE_LIMIT_MODE'`；沒有值就寫「這項沒做」，用 README 檢查 1 的隔離 nginx 證明表頭衛生 |
| `ss -tn` 看不到那條連線 → 已經關了／誰也沒關 | `ss -tn` 預設不列 TIME-WAIT | 用 `ss -tan`（見下面 502 那段） |
| `nginx -T` 裡有新設定 → 已生效 | `nginx -T` 讀的是磁碟上的檔，不是 worker 載入的 | reload 之後用行為證明（限流的 40 並行、keep-alive 的 TIME-WAIT） |
| 改了 `sites-available/mokaair.conf`、`nginx -t` 過、reload 成功 | 那個檔沒被 enable，nginx 一個字都沒讀 | 改 `mokaair.com`，並用行為驗證 |

`ops/nginx/README.md` 檢查 2 的範例寫 `cd /srv/travel-scanner/current`，這台主機是 `/root/travel_scanner`。

表頭衛生（偽造的 `X-Travel-Client-IP`／`X-Forwarded-For`／`X-Real-IP` 被丟掉而不是被附加）用 README 檢查 1：另起一個只讀已安裝 snippet 的 nginx（自己的 pid 檔與 port 9080）加一個 echo server，完全不碰正在跑的 nginx。再用 `nginx -T` 數 `include …mokaair-proxy-headers.conf;` 與 `proxy_pass` 的行數，兩者要相等。

## 自己的驗證被限流

部署後的驗證迴圈也會撞 5 r/s：0.3 秒間隔抓 40 頁加圖片（約 120 個 GET）會拿到零星 429，1.5 秒間隔全部 200。循序、每次 ≥ 1 秒；站主的瀏覽器與你共用同一個出口位址時預算更少。後台側欄的 RSC prefetch 被 429 與功能無關。

## POST 零星 502（upstream keep-alive）

症狀：`error.log` 有 `upstream prematurely closed connection while reading response header`（或 `reset by peer`），只發生在 POST，web 容器沒有重啟。

原因：nginx 對 `upstream mokaair_web` 的閒置連線池若比 Next standalone 的閒置逾時長，nginx 會把請求送進一條 Next 已經關掉的連線。GET 會被 nginx 默默重試，POST（非冪等）不會，瀏覽器就拿到 502。兩半修法，各自由不同的路徑上線：

| 半邊 | 設定 | 怎麼上線 | 怎麼驗 |
| --- | --- | --- | --- |
| Next | `docker-compose.prod.yml` 的 `KEEP_ALIVE_TIMEOUT: "65000"` | 部署 | `curl -sI http://127.0.0.1:8091/ \| grep -i '^keep-alive:'` → `timeout=65`（`timeout=5` 表示還是 Node 預設） |
| nginx | `ops/nginx/upstream-keepalive.conf`（`keepalive 32; keepalive_timeout 4s;`） | `install.sh` 裝 snippet，**再手動**把站台檔 upstream 裡的 `keepalive 32;` 換成 `include /etc/nginx/snippets/mokaair-upstream-keepalive.conf;`，reload | 下面的 TIME-WAIT 測法 |

誰先關連線，誰就持有 TIME-WAIT：

```bash
curl -s -o /dev/null https://mokaair.com/zh-TW
ss -tn state established '( dport = :8091 )'   # 記下 nginx 這端的本地 port
sleep 8
ss -tan '( dport = :8091 )'                    # 一定要 -a
```

同一個本地 port 在 `TIME-WAIT` ＝ nginx 先關（修好了）；還在 `ESTAB` ＝ nginx 的閒置時間超過 8 秒（nginx 半邊沒生效）；整條不見 ＝ Next 先關，正是競態。docker-proxy 在 127.0.0.1:8090／8091 上聽，所以 Node 的關閉到 nginx 可能是 FIN 也可能是 RST。BFF → uvicorn 那一跳已經是安全方向（undici 約 4 秒先關、uvicorn 5 秒）。

分辨部署與競態：`docker inspect -f '{{.State.StartedAt}}' travel_scanner-web-1` 對得上 `/root/deploy-logs/deploy_*.log` 的時間，那一分鐘的 `connect() failed (111) … Connection refused` 就是部署重建（每次約 8 秒 502），不是當機。只看 log 判斷競態有沒有修好要好幾週，因為它本來就少見；用上面的 TIME-WAIT 測法。

## 其他驗證

- **canonical 網域的 301**：`curl -sSI https://www.mokaair.com/api/auth/oauth/google/start | grep -iE '^HTTP|^location'` 要 301 到 apex 的同一路徑。測 OAuth 路徑而不是 `/`，因為登入流程的 cookie 綁 host。
- **限流只對頁面、不對靜態檔**：README「The limits apply to pages but not to assets」的兩個 200 次迴圈（這是故意打爆，只在要證明限流時用）。
- **ads.txt**：`curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/ads.txt` 要 200，然後 `grep ' /ads.txt ' /var/log/nginx/mokaair-crawl.log | grep -i google` 看 Google 實際拿到什麼。AdSense 後台列的是哪個網域先確認：`mocair.io/ads.txt` 是跨網域 301，和 apex 是兩個問題。
