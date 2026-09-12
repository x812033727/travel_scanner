---
id: 2026-09-12-nginx-deploy-checks-false-pass
title: ops/nginx 的上機指引有三處會假通過
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-12T03:56:07Z
completed_at:
branch:
depends_on: []
scope:
  - ops/nginx
---

# ops/nginx 的上機指引有三處會假通過

## Why

2026-09-12 把 `ops/nginx/` 套到正式主機（`hostinger2`，nginx 1.28.3）時，照著
`ops/nginx/README.md` 的驗收步驟做，三項檢查全部「通過」——但沒有一項證明了它宣稱要證明的
事。三個都是**假通過**：會回報成功，所以沒有人會回頭查。

設定本身來自 `2026-09-12-edge-rate-limit-and-header-hygiene`（PR #411，開票時仍未合併），這張票只談那份設定的**上機指引**，不動設定內容本身。`depends_on` 留空是因為那張票的檔案還
在 PR 分支上，`check` 看不到它。

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
   驗證自己的前置條件。

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

- [ ] 照 README 做一次，任何一項檢查通過時，它宣稱證明的事情真的成立。
- [ ] 安裝器不會在主機上留下一個「編了也不會生效」的設定檔。
- [ ] 範例設定講清楚它是要被合併的，不是被複製的。

## Steps

- [ ] `install.sh`：`sites-enabled/` 裡已經有指向 `sites-available/` 的 mokaair 設定時，不要
      再種 `mokaair.conf`；改成印出實際啟用的檔名，並要求把範例合併進那一個。
- [ ] README 的偽造位址檢查加前置驗證：先確認 `PUBLIC_READ_RATE_LIMIT_MODE` 真的在 API 容器
      的環境裡，不在就明說這項還不能做，而不是讓 `EXISTS` 回 0 被當成通過。
- [ ] README 補一個不依賴應用層的證明（見 Notes 的隔離 nginx 做法），讓邊緣層先上時就有東西可驗。
- [ ] `10-rate-limit.conf` 或 README 處理 `error_log` 層級：光設 `limit_req_log_level warn`
      不夠，還要有一個 warn 層級的目的地。
- [ ] `mokaair.conf.example` 頂端說明它是合併來源，並列出主機會有而範例沒有的東西（ACME
      webroot、額外網域與其憑證、TLS 參數、`default_server`）。

## How to verify

在一台 `sites-enabled/` 已經有別的檔名的機器上跑 `install.sh`，它必須拒絕種出第二個檔案，並指名
真正該編的那一個。然後：

```bash
# 限流事件看得到（不是靠 error.log）
seq 1 80 | xargs -P 8 -I{} curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/zh-TW \
  | sort | uniq -c
grep -c 'limiting requests' /var/log/nginx/mokaair-limit.log   # 要等於上面 429 的數量
```

偽造位址那項：在 `PUBLIC_READ_RATE_LIMIT_MODE` 尚未進入 API 容器環境時執行，README 的指令必須
明確說「還不能驗」，而不是印出通過。

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
