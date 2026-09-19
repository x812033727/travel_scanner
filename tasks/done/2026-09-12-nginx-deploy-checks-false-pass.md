---
id: 2026-09-12-nginx-deploy-checks-false-pass
title: ops/nginx 的上機指引有三處會假通過
status: done
priority: P1
area: ops
owner: claude-opus-5
claimed_at: 2026-09-19T16:08:58Z
created_at: 2026-09-12T03:56:07Z
completed_at: 2026-09-19T16:55:20Z
branch: claude/nginx-crawler-ranges-repo
depends_on:
  - 2026-09-12-edge-rate-limit-and-header-hygiene
scope:
  - ops/nginx
---

# ops/nginx 的上機指引有三處會假通過

## Why

2026-09-12 把 `ops/nginx/` 套到正式主機（`hostinger2`，nginx 1.28.3）時，照著
`ops/nginx/README.md` 的驗收步驟做，三項檢查全部「通過」——但沒有一項證明了它宣稱要證明的
事。三個都是**假通過**：會回報成功，所以沒有人會回頭查。

設定本身來自 `2026-09-12-edge-rate-limit-and-header-hygiene`（PR #411，2026-09-12 03:47Z 合併），
這張票只談那份設定的**上機指引**，不動設定內容本身。

1. **`install.sh` 種的檔名不是主機啟用的那個。** 安裝器寫 `sites-available/mokaair.conf`，
   而這台主機啟用的是 `sites-enabled/mokaair.com -> sites-available/mokaair.com`。照 README
   的順序做：編 `mokaair.conf` 的 EDIT 標記 → `nginx -t` 過 → `systemctl reload nginx` 成功
   → **線上一個位元都沒變**。接著後面每一項驗收都會通過，正因為舊設定還在跑，站台當然正常。
   那個空殼檔已從主機刪掉，但下次跑 `install.sh` 會再種一次。

2. **偽造位址那一項，在應用層還沒上線時恆為通過。** README 說它是「唯一能證明每來源計數不能
   被繞過」的檢查，做法是問 Redis `rate:public-read-ip-minute:<sha256(ip)>` 在不在。但寫那個
   key 的 `PublicReadRateLimitMiddleware` 跟 nginx 設定在同一個 PR 裡，而邊緣層**本來就該先
   上**——app 層限流的正確性正是建立在標頭已經被剝掉之上。所以在正確的上機順序下，跑這項檢查
   時 middleware 必定還沒部署，`EXISTS` 必定回 0，包含「nginx 根本沒剝標頭」的情況。檢查沒有
   驗證自己的前置條件。#411 在邊緣層上線四分鐘後就合併進 main 了，但正式機當時仍在 #406，
   兩件事差得夠遠，剛好示範了這個時間差不是假想的。

3. **`grep 'limiting requests' /var/log/nginx/error.log` 在 Debian/Ubuntu 預設安裝下永遠回空。**
   `10-rate-limit.conf` 設了 `limit_req_log_level warn`，但 Ubuntu 的 `nginx.conf` 是
   `error_log /var/log/nginx/error.log;`——沒給層級，預設就是 `error`，比 `warn` 高，於是每一
   筆限流事件都被丟掉。實測：200 次請求打出 128 個 429，access.log 全都有，error.log 自始至終
   沒被寫過。這一項的用途正是抓 Googlebot 被誤傷，卻是三個裡面唯一會長期誤導人的。

另外 `mokaair.conf.example` **不是這台主機的 drop-in**：只有線上那份有 `mocair.io` /
`www.mocair.io` 的 301 與獨立憑證、`default_server`、inline 的 `ssl_protocols` /
`ssl_ciphers`，以及 certbot 在 port 80 的 ACME webroot。範例的 `/.well-known/` 是 proxy 到
Next，整份照抄會弄壞憑證更新。

## Definition of done

- [x] 照 README 做一次，任何一項檢查通過時，它宣稱證明的事情真的成立。（2026-09-19 在
      `hostinger2` 跑完四步，結果在下方；第 4 步另外抓到 README 自己的兩個誤導。）
- [x] 安裝器不會在主機上留下一個「編了也不會生效」的設定檔。（離線以假的 `/etc/nginx` 演練過
      11 種情境，見 2026-09-19 筆記；主機上的那一次在 How to verify 第 1 步。）
- [x] 範例設定講清楚它是要被合併的，不是被複製的。

## Steps

- [x] `install.sh`：`sites-enabled/` 裡已經有指向 `sites-available/` 的 mokaair 設定時，不要
      再種 `mokaair.conf`；改成印出實際啟用的檔名，並要求把範例合併進那一個。
- [x] README 的偽造位址檢查加前置驗證：先確認 `PUBLIC_READ_RATE_LIMIT_MODE` 真的在 API 容器
      的環境裡，不在就明說這項還不能做，而不是讓 `EXISTS` 回 0 被當成通過。
- [x] README 補一個不依賴應用層的證明（見 Notes 的隔離 nginx 做法），讓邊緣層先上時就有東西可驗。
- [x] `10-rate-limit.conf` 或 README 處理 `error_log` 層級：光設 `limit_req_log_level warn`
      不夠，還要有一個 warn 層級的目的地。（目的地放在 site 檔的 server 區塊——範例與 README——
      不放 `10-rate-limit.conf`；理由在 2026-09-19 筆記。）
- [x] `mokaair.conf.example` 頂端說明它是合併來源，並列出主機會有而範例沒有的東西（ACME
      webroot、額外網域與其憑證、TLS 參數、`default_server`）。

## How to verify

全部在 `hostinger2` 上以 root 執行，照這個順序；每一步的完整指令都在 `ops/nginx/README.md`，
這裡只寫要看到什麼。

**1. 安裝器不再種空殼。** 這台主機啟用的是 `sites-enabled/mokaair.com -> sites-available/mokaair.com`，
而且 2026-09-12 已把上次種出的 `mokaair.conf` 刪掉，所以開跑前就不該有那個檔：

```bash
cd /root/travel_scanner && git pull                     # 拿到這個 PR
test ! -e /etc/nginx/sites-available/mokaair.conf && echo "clean before"
bash ops/nginx/install.sh | tee /root/install-1.txt
bash ops/nginx/install.sh | tee /root/install-2.txt
test ! -e /etc/nginx/sites-available/mokaair.conf && echo "still clean"   # 沒有種出第二個檔案
cmp /root/install-1.txt /root/install-2.txt && echo "idempotent"
```

輸出必須有 `The mokaair site is already enabled on this host as:` 接著
`/etc/nginx/sites-enabled/mokaair.com -> /etc/nginx/sites-available/mokaair.com`、
`Not seeding /etc/nginx/sites-available/mokaair.conf`，而 `Next, in this order:` 第 1 步是
merge 進 `/etc/nginx/sites-available/mokaair.com`，不是 `ln -s`。主機的 upstream 已經是 include
snippet（2026-09-13 那張票），所以不該再印 keep-alive 的提醒。

**2. 不依賴應用層的證明。** README「1. The forged address is discarded at the edge」整段照跑
（`/root/nginxtest/test.conf`、`echo.py`、curl、最後那個 `if`）。要看到 `PASS`；接著
`nginx -T` 的兩個計數（`include …mokaair-proxy-headers.conf;` 的行數與 `proxy_pass` 的行數）
要相等。結束要記得 `-s quit` 那個隔離的 nginx 並 kill 回聲伺服器。

**3. 偽造位址 end-to-end。** README「2. The forged address opens no counter」：先跑 `printenv`
那一行。印出 `observe` 或 `enforce` 才往下；印出 `NOT YET…` 或 `off` 就停，並在這張票記下
「這項尚未驗、原因是 middleware 還沒上／mode 是 off」——那正是這張票要的行為，不算失敗。往下時
要看到 `mine (<你的位址>): 1   forged: 0`；`mine: 0` 代表這次請求根本沒被計數，旁邊的 `forged: 0`
不能當通過。

**4. 限流事件看得到（不是靠 error.log）。** 主機的 `sites-available/mokaair.com` 在 2026-09-12
已有那兩行 `error_log`，先確認還在，再跑 README 的 before/after 區塊：

```bash
nginx -T 2>/dev/null | grep -c 'mokaair-limit.log'        # >= 1
# README「The limits apply to pages but not to assets」的 before/after 區塊，網域換成 mokaair.com
```

`429s:` 與 `logged:` 兩個數字要相等（安靜時段跑；同時有別人被限流會多幾筆）。

四步都過，才把 Definition of done 第一項打勾並 `done`。

## Notes

**已經上線的部分（2026-09-12）。** 邊緣層已套用在 `hostinger2`：`conf.d/mokaair-rate-limit.conf`、
`snippets/mokaair-proxy-headers.conf`，以及合併進 `sites-available/mokaair.com`（不是
`mokaair.conf`）。那台主機前面沒有 CDN，realip 區塊維持註解。`/etc/nginx` 的備份在
`/root/nginx-backups/20260912T034351Z/etc-nginx`。site 設定裡另外加了兩行，因為第 3 點：

```nginx
error_log /var/log/nginx/error.log error;
error_log /var/log/nginx/mokaair-limit.log warn;
```

實測數字：`/zh-TW` 200 次 → 72×200 + 128×429；`/_next/static/…` 200 次 → 200×200（靜態資源
沒被誤傷）；`www` → apex 的 301 在 `/api/auth/oauth/google/start` 上路徑保留。

**不依賴應用層也能證明標頭有被剝掉的做法。** 另起一個獨立的 nginx 行程，讀**同一份已安裝的**
snippet，後面接一個回聲伺服器，完全不碰線上設定：

```bash
nginx -c /root/nginxtest/test.conf -p /root/nginxtest   # 一個 location，include 已安裝的 snippet，
                                                        # proxy_pass 到 127.0.0.1:9081 的回聲伺服器
curl -s -H 'X-Travel-Client-IP: 198.51.100.1' -H 'X-Forwarded-For: 198.51.100.1' \
     -H 'X-Real-IP: 198.51.100.1' http://127.0.0.1:9080/
```

2026-09-12 的結果：上游收到的是 `X-Forwarded-For: 127.0.0.1`、`X-Real-IP: 127.0.0.1`，而
`X-Travel-Client-IP` **整個不存在**——偽造值被丟掉，不是被附加。這正是 README 那項檢查想證明
的事，而且邊緣層單獨上線時就能做。

### 2026-09-19 done in repo (claude-fable-5-1)

只動了 `ops/nginx/` 四個檔案和這張票；限流數值、zone、snippet 內容一個都沒改。

**`install.sh`——先看主機啟用了什麼，再決定要不要種。** 安裝三個自有檔案之後，掃
`sites-enabled/*`（symlink 用 `readlink -f` 跟到底、告訴操作者該編的是 `sites-available/` 裡
那一個；一般檔案也算）與 `conf.d/*.conf`（nginx.org 套件的佈局，`sites-available/` 根本沒被
include），跳過我們自己裝的 `mokaair-rate-limit.conf`。「像 mokaair 站台」的判準是去掉註解後
有 `upstream mokaair_web`、`proxy_pass http://mokaair_web`、`mokaair-proxy-headers.conf`、
`limit_req zone=mokaair_`（`limit_req_zone` 宣告不會命中）或 `server_name … mokaair` 任一個。
有啟用的檔案而它不是 `sites-available/mokaair.conf` 時：不種、印出
`already enabled on this host as: <symlink> -> <target>`、要求把範例 merge 進那一個，「Next」
的第 1 步改成 merge（不再有 `ln -s`）；若 `mokaair.conf` 同時存在，明講它是沒被啟用的殘留
（`rm` 它）或「兩個都啟用是錯的」。沒有任何啟用檔像這個站台時維持原行為：沒檔就種、有檔就
`Kept existing`，多一行提醒它還沒被 link 進 `sites-enabled/`。沒有新依賴（`readlink`、`grep`、
`install` 本來就在用）。這裡沒有 nginx 也沒有 docker，但沙盒是 root，所以用一個用完即刪的假
`/etc/nginx` 跑過 11 種情境：新主機、種了沒 link、種了有 link、`hostinger2` 那種相對 symlink
到 `mokaair.com` 加一個 `default` 站台、加殘留的 `mokaair.conf`、`mokaair.conf` 也被 link、
直接放在 `sites-enabled/` 的一般檔案、懸空 symlink 加目錄、只在註解裡提到 marker、站台在
`conf.d/`、`conf.d/` 只有我們自己的檔案——每一種都落在預期的分支，`mokaair.com` 情境連跑兩次
輸出與檔案樹逐位元相同，`bash -n` 通過。

**README——三項檢查各自帶前置條件，不能再無條件通過。**
- 偽造位址拆成兩節。「1.」是不依賴應用層的證明：完整的 `/root/nginxtest/test.conf`（自己的
  `pid`，不然會蓋掉正式 nginx 的 `/run/nginx.pid`；自己的 log 與 temp path；一個 location
  include **已安裝的** snippet，`proxy_pass` 到 127.0.0.1:9081）、`echo.py` 回聲伺服器（把收到的
  request header 逐行回在 body）、那條 curl、9-12 當天的預期輸出、以及一個 `PASS`/`FAIL` 的
  `if`（偽造值不得出現在任何地方、`X-Travel-Client-IP` 不得存在、兩個位址標頭都得是
  `127.0.0.1`），另加 `nginx -T` 裡 include 數要等於 `proxy_pass` 數。這個 `if` 在這裡測過：直接
  打回聲伺服器（沒有 nginx）是 `FAIL`、預期輸出是 `PASS`、`$proxy_add_x_forwarded_for` 式的附加
  是 `FAIL`、空值標頭存在也是 `FAIL`。「2.」才是 Redis：先
  `docker compose -f docker-compose.prod.yml exec -T api sh -c 'printenv PUBLIC_READ_RATE_LIMIT_MODE'`，
  沒有就印 `NOT YET: … cannot be done until …` 並停；有值再送一個帶偽造標頭的請求，同時查
  **自己位址的 key 必須是 1**（從 access.log 用 `?edge=<stamp>` 找回 nginx 看到的位址）與偽造位址
  的 key 必須是 0——`mine: 0` 時旁邊的 `forged: 0` 明說不算數。redis-cli 改成在容器裡用
  `REDISCLI_AUTH="$REDIS_PASSWORD"`（跟 compose 的 healthcheck 一樣），不再假設主機 shell 有
  `$REDIS_PASSWORD`。
- 限流日誌那節寫明 `limit_req_log_level warn` 只是層級不是目的地、Ubuntu 預設 `error_log` 沒給層級
  就是 `error`、9-12 的 128 個 429 一筆都沒進 error.log；那兩行 `error_log` 列為必要步驟（並解釋為
  什麼要兩行：server 層級的 `error_log` 是取代不是疊加，只加第二行會讓真正的錯誤不再進 error.log），
  然後 grep `mokaair-limit.log` 的 before/after 差值要等於 429 數。
- Install 一節改寫成安裝器的兩種情況與 merge 的做法；Trust boundary 第一點原本寫「從沒在真主機跑
  過」，9-12 之後已不成立，改成記錄那次套用並指回這張票。

**第 3 步的取捨：目的地放 site 檔的 server 區塊（範例已加那兩行，README 列為必要），不放
`10-rate-limit.conf`。** 三個理由：(1) `conf.d/` 是 http context，在那裡寫 `error_log` 會取代主機
主設定的預設值、對這台機器上**每一個** server 生效，別的站台的 warn 也會流進 `mokaair-limit.log`；
(2) `10-rate-limit.conf` 會被 `ci-validate.conf` 與 `tools/test-guide-image-rate-limit.py` 在主機
以外載入，那些環境沒有可寫的 `/var/log/nginx`，絕對路徑會讓 `nginx -t` 變紅；(3) `hostinger2`
的 `sites-available/mokaair.com` 9-12 就是這樣加的，範例照抄主機，merge 的 diff 最小。
`10-rate-limit.conf` 只多了一段註解指向目的地（`git diff` 只有 `#` 開頭的行），CI 的 `nginx -t`
讀到的指令完全沒變。

**`mokaair.conf.example`。** 檔頭改成「MERGE SOURCE, not a drop-in」：新主機由 `install.sh` 種、
既有主機 merge 進自己的檔案、絕不整份覆蓋，並列出主機有而範例沒有的四樣（port 80 的 ACME webroot
——範例的 `/.well-known/` 是 proxy 到 Next、port 80 是全部 301，蓋過去會弄壞下一次續期；
`mocair.io` / `www.mocair.io` 各自的憑證與 301；inline `ssl_protocols` / `ssl_ciphers`；
`default_server`），以及該從範例拿走的東西。主 server 區塊加了那兩行 `error_log` 與說明。

**這裡驗過的 / 驗不了的。** `bash -n ops/nginx/install.sh` 通過；README 的 13 個 bash 區塊各自
`bash -n` 通過；`key()` 算出的 key 與原 README 的一行式相同。這個環境沒有 `nginx`、沒有 docker
daemon、也沒有 crossplane，所以 `nginx -t -c ci-validate.conf` 與
`tools/test-guide-image-rate-limit.py`（要給它一個 nginx 執行檔路徑）都沒跑——但
`ci-validate.conf` include 的三個檔案裡只有 `10-rate-limit.conf` 動過、而且只動註解；範例檔 CI 不
載入，新加的 `error_log` 是 server context 合法指令；checker 對範例唯一的斷言
`limit_req zone=mokaair_content_pages burst=20 nodelay;` 原封不動。CI 的 `containers` job 會跑
真的 `nginx -t`。

**還需要主機的部分。** 上面 How to verify 四步要在 `hostinger2` 跑一次：安裝器現在可以放心重跑
（不會再種 `mokaair.conf`）；隔離 nginx 的證明本來 9-12 就做過、這次是照 README 新寫的版本再跑
一次確認文件正確；Redis 那項看 `printenv` 印什麼決定是「過」還是「尚未驗」；日誌那項要 before/after
相等。四步過了再打 DoD 第一項、`done`。

---

## 2026-09-19 takeover (claude-opus-5)

Taken over from `claude-fable-5-1` with `--force` at the site owner's explicit request, because
the two halves turned out to be ordered and could not be done by two owners:
`2026-09-19-edge-rate-limit-refuses-search-crawlers` put a verified-crawler allowlist on the
host, and **How to verify step 1 runs `install.sh`, which overwrites
`conf.d/mokaair-rate-limit.conf` from the repo** (`install.sh:27`). Until the repo carried that
config, step 1 would have replaced the live file with one that does not declare
`mokaair_crawlers`, and the site config's `limit_req zone=mokaair_crawlers` would have made
`nginx -t` fail. Loud rather than silent, but it blocks this ticket either way.

The repo has now caught up with the host. Added under this ticket's scope:

- `05-crawler-ranges.conf` — 617 published Google/Bing prefixes, generated by
  `tools/nginx-crawler-ranges.mjs`; `install.sh` puts it at `conf.d/05-mokaair-crawler-ranges.conf`
- `10-rate-limit.conf` — chained key maps so a verified crawler leaves `mokaair_content_pages`
  and lands in a new `mokaair_crawlers` zone at 30r/s, plus `log_format mokaair_limited` and
  the `$mokaair_is_limited` map
- `mokaair.conf.example` — four crawl-control locations exempt from the page budget
  (`/robots.txt`, `/sitemap.xml`, `/llms.txt`, `^~ /sitemaps/`), the crawler `limit_req`, and
  the 429-only `access_log`
- `ci-validate.conf` — **必要**, not cosmetic: it includes `10-rate-limit.conf`, whose maps now
  read `$mokaair_verified_crawler`, and an undefined variable is a config error in nginx

Both CI container checks were reproduced on `hostinger2` with the exact commands from
`.github/workflows/ci.yml:150-157`, against this branch's files in a temp dir, touching nothing
live:

```
nginx -t -c /etc/nginx/ops/ci-validate.conf        -> syntax is ok / test is successful
test-guide-image-rate-limit.py /usr/sbin/nginx     -> PASS: 120 image requests allowed;
                                                      page budget preserved; 7 non-image routes limited
```

With a control: deleting the `05-crawler-ranges.conf` include makes it fail with
`[emerg] unknown "mokaair_verified_crawler" variable`, which is the failure this include exists
to prevent.

**Definition of done item 1 still needs steps 2-4 on the host, and step 1 after this merges.**
Step 1 cannot run before the merge for the reason at the top of this section.

### Host verification run, 2026-09-19

**Step 2 (forged address discarded at the edge): PASS.** The isolated nginx on 127.0.0.1:9080
reading the installed snippet showed the upstream receiving `X-Forwarded-For: 127.0.0.1` and
`X-Real-IP: 127.0.0.1`, with `198.51.100.1` nowhere and no `X-Travel-Client-IP` at all --
replaced, not appended. The companion count came out **include=10, proxy_pass=10**, equal, so
every proxying location in the loaded config carries the snippet; that also covers the four
crawl-control locations added in this PR.

**Step 3 (forged address opens no counter): NOT APPLICABLE, which the ticket says is the
correct outcome.** `printenv PUBLIC_READ_RATE_LIMIT_MODE` in the api container returns nothing
-- `PublicReadRateLimitMiddleware` is not configured on this host -- so the Redis `EXISTS`
check cannot distinguish "the header was discarded" from "nothing counted this request at all".
Recorded rather than run, exactly as the ticket asks.

**Step 4 (limiting events are visible): PASS, but the README's recipe needs two corrections.**
`mokaair-limit.log` appears 3 times in the loaded config. 40 truly-concurrent requests gave
20 x 200 and 20 x 429, and the log grew by 19.

Two things in the README's own block mislead, which is this ticket's subject:

1. **`seq 1 80 | xargs -P 8` can legitimately produce zero 429s.** Run exactly as written it
   returned **80 x 200**. Eight requests in flight against a ~1.5 s server-rendered page is
   about 5.3 r/s, which is the zone's rate, so the burst absorbs the overshoot indefinitely.
   The natural reading -- "nothing is being limited" -- is wrong, and it is the same trap as
   the other three. Use a burst that clearly exceeds the rate: `for i in $(seq 1 40); do ... &
   done; wait` gave 20 x 429 on the same host minutes later.
2. **`429s` and `grep -c 'limiting requests'` are not the same population.** `limit_conn`
   also answers 429 (`limit_conn_status 429`) but logs `limiting connections by zone
   "mokaair_conns"`. At 40 concurrent both fire, so the two numbers differ by however many
   connection refusals there were -- 20 vs 19 here. Compare against both phrases, or the
   check reports a mismatch that is not one.

**The question the ticket exists to answer.** Cross-referencing every client address in the new
`mokaair-limited.log` against `conf.d/05-mokaair-crawler-ranges.conf`: **no allowlisted address
has ever been refused.** For contrast, 44 refused requests carry a Googlebot or Bingbot
User-Agent, and every one of them comes from `111.251.215.82` -- the machine running this
audit. That is the whole argument for keying the exemption on published address ranges rather
than on the User-Agent, restated as data.

**Still open: step 1.** `install.sh` idempotency has to run after this PR merges and the host
pulls, for the ordering reason at the top of this section. Definition of done item 1 stays
unticked until then.

### Step 1, after #568 merged (2026-09-19)

`git pull` to `9af3511f`, then `install.sh` twice. Backup at
`/root/nginx-backup-step1-2026-09-19-165419`.

- **clean before / still clean** -- `sites-available/mokaair.conf` absent before and after, so
  the installer no longer seeds a file this host would never read. That was the first false
  pass in this ticket.
- **idempotent** -- the two runs printed identical output, and it names the real enabled file
  (`sites-enabled/mokaair.com -> sites-available/mokaair.com`) with merge instructions rather
  than `ln -s`.
- **`nginx -t` successful**, site answers 200 on `/zh-TW`, `/sitemap.xml` and `/feed.xml`.

One file did change, and it is worth saying why rather than waving it through:
`conf.d/mokaair-rate-limit.conf` went `5010e6e9` -> `7c911aee`. The diff is the eight-line
comment restored in #568 explaining why the `warn` destination lives in the site file and not
here -- the very thing the third false pass was about, which I had dropped while porting and
put back. `diff` over non-comment lines is empty: the directives are byte-identical. Reloaded
so the loaded config matches disk.

After the reload: `limit_req zone=mokaair_crawlers` x1, `$mokaair_verified_crawler` x3, the
four crawl-control locations x4. 40 concurrent requests to `/robots.txt` -> 40 x 200; the same
to `/zh-TW` -> 20 x 200 and 20 x 429. Crawl-control files exempt, ordinary pages still limited.

All four steps done; closing.
