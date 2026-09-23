# Mokaair 資安複查（2026-09-23）

- 檢查基準：`main` commit `ffa42476`（2026-09-23）
- 分支：`claude/security-audit-480b3e`
- 前次基準：[`security-review-2026-09-13.md`](security-review-2026-09-13.md)（commit `2bfd427`）。
  兩個基準之間合入 221 個 commit；程式碼面的變動集中在 `foods`、`hotspots`、`ai`、`trips`、
  `guides` 的搜尋與匯入、web 的 `codex-learning`／`guides` 元件／sitemaps／`llms.txt`、
  nginx 的爬蟲位址表、`ops/release/hold.py`，以及五個新的 workflow。
- 範圍：`apps/api`（FastAPI、RQ worker、`deployment_agent`）、`apps/web`（BFF 與前端）、
  `ops/`、Docker／Compose、GitHub Actions、相依套件、追蹤中的檔案與 git 歷史（201 個 ref），
  以及這次第一次能驗的 GitHub 倉庫設定（唯讀 API）。
- 方法：四個唯讀代理分區審閱（認證／授權、注入與資料處理、web／BFF、ops／CI／密鑰），每個
  代理先讀前三份稽核再看 delta。**代理回報的每一項都由我回到原始碼逐行重驗**（含用 Node 驗
  WHATWG 的解析、用 `gh api` 讀分支保護），只有重驗成立的才列入。沒有滲透測試，沒有存取
  正式主機。

## 1. 結論

**沒有 Critical、沒有 High。** 兩個 Medium 都不是「今天就能打」的：M1 要先能連到主機本身或
compose 的 bridge，M2 要第三方供應商的腳本先被入侵。前三輪修過的項目沒有一項回歸：登出
撤銷整條續期鏈、保留信箱的 OAuth 路徑、`OFFICIAL_PROVIDER_HOSTS` 三處綁定（新的 Jev 供應商
也在表上）、`escape_like`、Gemini grounding 的 `canonical_external_url`、`validate_editorial_url`
六個寫入點、BFF 的路徑段與標頭白名單、admin layout 的伺服器端門檻、Actions 釘 SHA、ruff `S`
規則，都還在原位。

09-13 立的六張票：五張 done，一張 blocked（正式 compose 網路分段，理由不變）。09-19 的
P1「Google 金鑰進 URL 被記進 log」修了六處，但**漏了第七處**（L2），而且那張票的回歸測試
是白名單式的，所以新漏的那一處不會被抓到。

一處要更正前次報告：09-13 §2 寫「`forwarded_client_ip` 要同時滿足信任旗標、token 相符、
合法 IP 三者」。實際上 token 比對只在 token **有設定**時才發生，空值時所有呼叫者都通過（M1）。

| 嚴重度 | 數量 | 立票 | 不立案 |
|---|---|---|---|
| Medium | 2 | 2 | 0 |
| Low | 13 | 13（併成 6 張） | 0 |
| Info | 6 | 1（併入 supply-chain） | 5 |

## 2. 這次實際驗證過的項目

每一項都回到現行原始碼確認，不是引用前幾份的結論。

**認證與工作階段** — JWT 要求 `sub/ver/iss/aud/jti/iat/nbf/exp` 全部存在，`auth_version`
與絕對上限在每次出示時檢查；續期沿用同一個 `jti`，`revoke_access_token` 的 TTL 取
`max(exp, 絕對上限)`（R2-01 仍成立）；Redis 不通時撤銷檢查回 503。Argon2、未知帳號也比對
dummy hash、`reject_weak_password` 套在註冊／改密碼／重設。OAuth：Redis `GETDEL` 一次性
flow、state 與瀏覽器綁定 `compare_digest`、Google／LINE 用 PKCE S256、id_token 以 JWKS 驗
`RS256`＋`aud`＋`iss`、同 Email 絕不自動合併、保留信箱在 register 與 OAuth 兩邊都擋。

**授權** — 以 AST 列出全部 431 條路由：每一條 `/admin/*` 都掛著 `AdminUser` 或
`require_capability(...)` 的別名；未列名的 `/admin/*` 路徑仍落到 `roles.manage`（fail-closed）。
角色變更、抹除、永久停權都走 `require_admin_step_up`（HS256、獨立 iss／aud、300 秒、綁
`sub`＋`ver`、cookie `SameSite=Strict`、path `/api/v1/admin`）。新增的 `trips/selections.py`
（景點／美食／店家「加入行程」共用）、`ingest_router`、`export_router`、`stay_router` 都經
`owned_trip`；社群的 `owned_post`、`conversation_for`、`media_url` 都是 owner／member scoped。
`/ai/parse-trip`、`/destinations/discover` 與規劃器現在同時按帳號與 IP 計量（`plan_within_budget`
fail-closed），是基準之後新增的。

**注入與資料處理** — 沒有任何字串拼接的 SQL；`text()` 只有常數字串或綁定參數；migration 的
f-string 只插模組常數。SSRF 防護以 `catalog_review/evidence.py` 為範本：語法閘門後解析 DNS、
拒絕非公網位址、把連線釘在檢查過的 IP 上但保留 SNI／Host、不跟隨轉址、每一跳重驗（最多 6 跳）；
`restaurants/imports.py` 的 Google 短網址展開同樣逐跳驗證。唯一的 `subprocess` 在
`pack_ingest.py`（argv 清單、無 shell、只有 CLI 會到）；`check_svg` 在渲染前擋掉 `script`、
`foreignObject`、`image`、`use`。沒有 `eval`／`exec`／`pickle`／`yaml.load`。上傳圖片先進
quarantine、限 10 MB／25 MP／單幀、重新 raster 成 WebP。AI 結構化輸出一律
`extract_json_document` → pydantic `model_validate_json`；規劃器的 `candidate_key` 對伺服器端
建的候選表解析，未知鍵丟棄；連結只來自 grounding metadata。15 個 RQ enqueue 點都是固定的
函式路徑與 UUID／enum 參數。密鑰 Fernet 存放、只回遮罩、`audit_safety` 會刮掉 bearer／JWT／
URL 帳密／`key=`。

**web／BFF** — 路徑段拒絕 `.`／`..`／分隔符與 NUL；只轉發白名單標頭；Host 不轉發；請求與回應
都逐位元組計數；變更方法要求同源 `Origin`（`Origin: null` 會被 `new URL("null")` 拒絕，已驗）；
clickout 表單不再帶 `noreferrer`。`dangerouslySetInnerHTML` 仍是三處（兩個帶 nonce 的
bootstrap 常數、JSON-LD 逸出 `<`）；新的 block 類型（summary、faq、code、table、callout、
rich_paragraph）全部以 React 文字渲染；圖片限自家 `/guides/<slug>/<name>.(webp|jpg|png|svg)`；
連結走 `contentBlockLink`／`httpsLink`／`safeExternalHref`。feed 逸出、`llms.txt` 是
`text/plain`、sitemaps 只讀公開端點且不帶 cookie。伺服器端沒有任何抓取使用者提供的 URL。
分享 token 256-bit、只存 SHA-256、公開欄位白名單不含作者身分。

**信任邊界與基礎設施** — nginx 對外先清 `X-Travel-Client-IP`、覆寫 `X-Forwarded-For`，11 個
`proxy_pass` 都含同一個 include；HSTS 只在 server 層一個 `add_header`（location 裡沒有，所以
不會被繼承吃掉）；`client_max_body_size 6m`；FastAPI 的 8090 不對外、正式環境 `docs_url` 關閉。
限流覆蓋每一個 `/api/*`（含登入、註冊、後台、AI）與每一個頁面；爬蟲位址表只認已公布的
Googlebot／Bingbot 網段，命中者仍有上限（30 r/s），不是豁免；產生器驗 CIDR 語法並拒絕空輸出。
部署 agent 走 Unix socket、HMAC 涵蓋 timestamp／nonce／method／path／body 摘要、`shell=False`、
路徑白名單；`hold.py` 用 `O_CREAT|O_EXCL`、只清自己的 release、拒絕控制字元。正式 compose：
Postgres／Redis 不對外、密碼必填、api／web 只綁 loopback、非 root、`cap_drop: ALL`、
`no-new-privileges`；兩個 `.dockerignore` 都排除 `.env*`，`deployment_agent` 不進 image。
CI：全部 `permissions: contents: read`（`issues: write` 只在 red-main）、沒有 `pull_request_target`、
沒有把 `github.event.*` 插進 `run:`、帶密鑰的 workflow 只能 `workflow_dispatch`、七個 action
全部釘 SHA（`tools/workflow-pins.test.mjs` 強制、Dependabot 更新）、09-14 之後沒有新加的
未釘 action、`npm ci`＋`uv sync --frozen`。密鑰：工作樹與全歷史掃 AWS／OpenAI／Anthropic／
Google／GitHub／Slack 樣式、PEM／PPK、帶帳密的 DB URL——除 L7 之外只有 CI／dev 的佔位值。

## 3. 發現清單

| 編號 | 嚴重度 | 標題 | 位置 | 任務 |
|---|---|---|---|---|
| M1 | Medium | `INTERNAL_PROXY_TOKEN` 在正式環境不是必填；空值時 `_from_our_proxy` 對所有呼叫者回 `True`，compose 預設 `${INTERNAL_PROXY_TOKEN:-}`，啟動驗證只要求 `TRUST_PROXY_CLIENT_IP` | `app/infra.py`、`app/config.py::validate_api_serving_security`、`docker-compose.prod.yml` | [`internal-proxy-token-required-in-production`](../tasks/open/2026-09-23-internal-proxy-token-required-in-production.md) |
| M2 | Medium | 聯盟腳本（Travelpayouts drive）與 GTM 掛在 `[locale]` 根 layout，`/admin`、`/account`、`/my`、`/trips` 都在其下；`connect-src` 仍 Report-Only、`'strict-dynamic'` 信任其後續載入。供應商腳本被入侵即可在站主的後台文件裡同源呼叫 admin API 並外送 | `apps/web/app/[locale]/layout.tsx`、`components/travelpayouts-drive.tsx`、`components/analytics-provider.tsx` | [`third-party-scripts-on-privileged-routes`](../tasks/open/2026-09-23-third-party-scripts-on-privileged-routes.md) |
| L1 | Low | `support` 角色（`users.manage`）可不經 step-up 對資料庫指定的 `owner`／`deployer`／`database_operator` 做最長 90 天的限時停權（自己、環境指定帳號、最後一位 owner 除外）；`sessions/revoke` 與解除停權完全沒有 self／環境指定守門 | `app/admin/user_router.py`、`app/admin/users.py` | [`admin-owner-suspension-guards`](../tasks/open/2026-09-23-admin-owner-suspension-guards.md) |
| L2 | Low | Google Weather 仍把 Maps key 放在 `?key=`；09-19 的回歸測試只列三個模組所以抓不到；api／worker 沒把 `httpx`／`httpcore` 壓到 WARNING（只有 collector 有）。Ekispert／ODsay 依供應商設計只能走查詢字串，共享同一個潛在曝露 | `app/weather/google.py`、`tests/test_api_keys_not_in_urls.py` | [`google-weather-key-in-url`](../tasks/open/2026-09-23-google-weather-key-in-url.md) |
| L3 | Low | BFF `safeRedirectLocation` 放行 `/\host`，瀏覽器解析成 `https://host/`（已用 Node 驗）。API 所有轉址都是絕對 HTTPS（航班驗 scheme＋host、聯盟用 `allowed_hosts`、Places 驗 Google URI），所以今天到不了這行，屬縱深 | `apps/web/app/api/travel/[...path]/proxy-security.ts` | [`bff-admin-shell-hardening`](../tasks/open/2026-09-23-bff-admin-shell-hardening.md) |
| L4 | Low | `proxy.ts` matcher 跳過任何含「.」的路徑；今天沒有動態段允許「.」，所以只有 `[...rest]` 的 404 文件沒有 nonce 與強制的 `script-src`，但那個文件仍掛著整棵 provider 樹與第三方腳本 | `apps/web/proxy.ts` | 同上 |
| L5 | Low | admin 的逐頁能力檢查在 layout；Next.js 的 soft navigation 不重跑 layout，受限角色點連結進到能力外的頁會拿到殼（資料仍受 API `require_capability` 保護） | `apps/web/app/[locale]/admin/layout.tsx` | 同上 |
| L6 | Low | `/sitemap.xml`、`^~ /sitemaps/`、`/llms.txt`、整個 `/.well-known/` 前綴不計 `limit_req`，而 sitemap 路由是 `force-dynamic`、`max-age=0`；剩下的上限只有 `limit_conn 20` | `ops/nginx/mokaair.conf.example` | [`nginx-sitemap-budget-and-tls-policy`](../tasks/open/2026-09-23-nginx-sitemap-budget-and-tls-policy.md) |
| L7 | Low | 公開倉庫裡有逐字的主機指令紀錄：PuTTY 儲存的工作階段名稱、root 登入、本機 plink 路徑、隧道埠、一個一次性 Postgres 容器的密碼（容器當天已刪，沒有東西是活的）；四份批次 README、nginx README 與數個 done 票重複了工作階段名稱 | `docs/ai-terms-series/postgresql-validation.json`（#489）等 | [`scrub-host-details-from-docs`](../tasks/open/2026-09-23-scrub-host-details-from-docs.md) |
| L8 | Low | 130 個追蹤檔案含本機使用者路徑（docs 下的 evidence JSON／log）；`.agents/skills` 與 `.claude/skills` 乾淨（有測試強制），docs 沒有 | `docs/**` | 同上 |
| L9 | Low | `.gitignore` 沒有 `*.pem`、`*.ppk`、`*.key`、`*.p12`、`id_rsa*`、`id_ed25519*`（歷史上從未提交過） | `.gitignore` | 同上 |
| L10 | Low | 基底映像用可變 tag（`python:3.13-slim`、`node:22-alpine`、`postgres:17-alpine`、`redis:7.4-alpine`、`nginx:1.28-alpine`）；`pip install uv` 沒釘版本；`axllent/mailpit:latest` | Dockerfiles、compose、workflows | [`supply-chain-pins-and-announcers`](../tasks/open/2026-09-23-supply-chain-pins-and-announcers.md) |
| L11 | Low | `ci-red-main.yml` 的 `workflow_run` `branches: [main]` 濾的是**觸發 run 的 head branch**，fork PR 的分支叫 `main` 且 CI 紅就會開「CI is red on main」issue（欄位都是 GitHub 產生的，沒有注入，只是誤報） | `.github/workflows/ci-red-main.yml` | 同上 |
| L12 | Low | `ssl_protocols`／`ssl_ciphers`／`server_tokens` 只在主機的 `nginx.conf`，repo 證明不了 TLS 1.0／1.1 已關、版本標頭已藏（README 的煙霧測試還預期有 `Server:`） | `ops/nginx/mokaair.conf.example` | [`nginx-sitemap-budget-and-tls-policy`](../tasks/open/2026-09-23-nginx-sitemap-budget-and-tls-policy.md) |
| L13 | Low | `travel_locale` 在 BFF 登入路徑設定時沒帶 `secure`（OAuth callback 有）；偏好 cookie、HSTS 蓋得住 | `apps/web/app/api/travel/[...path]/route.ts` | [`bff-admin-shell-hardening`](../tasks/open/2026-09-23-bff-admin-shell-hardening.md) |
| I1 | Info | `GET /hotspots/sources` 未登入可讀各 collector 是否啟用（與 API-18 `/providers/status` 同類，只有布林） | `app/hotspots/router.py` | 不立案 |
| I2 | Info | `masked_secret` 對 `settings.read`（`viewer` 角色）也回末四碼 | `app/admin/service.py` | 不立案 |
| I3 | Info | `POST /auth/oauth/{provider}/exchange` 沒限流（`start` 有）；`flow_id` 256-bit 且 `GETDEL` 一次性，所以只是一次請求一次 Redis 操作 | `app/auth/router.py` | 不立案 |
| I4 | Info | 每日的 `npm-audit.yml`／`pip-audit.yml` 失敗時沒有人被通知，只有最後一個 committer 會收 email | workflows | 併入 supply-chain |
| I5 | Info | GitHub 設定：**Dependabot alerts 關閉**（version updates 照跑，但 advisory 不會通知）；沒有 required reviews（單一站主，`enforce_admins` 開著） | 倉庫設定 | 站主，見 §5 |
| I6 | Info | 前次未立案的四項現況不變：`/providers/status` 未登入可讀、OAuth flow cookie 未簽章、航班 clickout 沒有 host allowlist、API image 單階段 | — | 不立案，理由同 09-13 |

### 三個值得多說一句的

**M1** 的攻擊面在主機內：nginx 對外已經先清掉 `X-Travel-Client-IP`，所以要利用它得先站在主機
或 compose bridge 上。它是不是 live 取決於正式主機的 env 有沒有設 token，這次沒有連主機所以
不知道。修法是在 `validate_api_serving_security` 把它變成正式環境必填——那會讓沒設 token 的
主機**啟動失敗**，所以票上寫明要先確認主機 env 再合。09-12 的票刻意把空值留成「維持原行為」，
理由是只設一邊會把全部訪客塌成一個 bucket；現在看，一個大聲的啟動拒絕比一個看不見的信任便宜。

**M2** 不是新程式碼引進的，是 09-13 之後 CSP 只強制了 `script-src` 半邊、而第三方腳本從來
沒被擋在後台之外，兩件事合起來的結果。`(ads-public)` 對 AdSense 做了獨立的 root 與匿名文件，
同一個想法沒有套到聯盟腳本與 GTM。把它們從特權路由拿掉之後，`connect-src` 才有條件轉強制。

**L7／L8** 是因為倉庫公開才升到 Low。工作階段名稱與 root 登入只有偵察價值（主機要金鑰），
一次性容器的密碼已經跟容器一起消失，不需要輪替任何東西；要做的是刮乾淨並加一個測試，讓
下一份 evidence JSON 進不來。歷史不重寫。

## 4. GitHub 倉庫設定（這次第一次能從外部驗）

| 項目 | 現況 |
|---|---|
| `main` 分支保護 | 四個必要檢查（`api`、`web`、`containers`、`full-stack-smoke`）、`strict`、`enforce_admins`、禁 force push 與刪除。與 `.github/BRANCH_PROTECTION.md` 一致 |
| Actions | `GITHUB_TOKEN` 預設唯讀；fork PR 首次貢獻者需核准；沒有 rulesets |
| Secret scanning | 開啟，push protection 開啟，0 筆警示 |
| Dependabot | `dependabot.yml` 的 version updates 在跑（沒有積壓的 PR）；**alerts 關閉**；沒有 code scanning |
| 可見性 | 公開 |

## 5. 站主要做的事、以及無法從 repo 驗證的項目

1. **開 Dependabot alerts**（Settings → Code security）。公開倉庫免費，開了之後 advisory 會直接
   通知，不必等每日 audit job 紅掉才有人看（I4、I5）。
2. **確認正式主機 env 的 `INTERNAL_PROXY_TOKEN`** 在 `api` 與 `web` 兩邊都有值。M1 的票在
   這個確認之前不能合，否則部署會在啟動驗證被擋下。
3. 09-19 那張票的 **YouTube key 輪替**仍待站主（票停在 review）。
4. HSTS `includeSubDomains` 的決定（09-14 留下，需要知道 DNS 的人）。
5. 沿用前幾輪、這次一樣沒有存取權的項目：主機 `nginx.conf` 的 TLS 設定、Google Maps 與
   NAVER 瀏覽器金鑰的 referrer 限制、部署 agent 的 PAT 實際範圍、`/etc/travel-scanner/*.env`
   的實際權限、`/root/deploy-travel-scanner.sh`（不在 git 裡）是否把 `.env` 印進部署 log。

## 6. 本次執行的檢查

| 項目 | 指令 | 結果 |
|---|---|---|
| Node 相依稽核 | `npm audit --audit-level=low` | 0 vulnerabilities |
| Python 相依稽核 | `cd apps/api && uv run pip-audit --local --skip-editable` | No known vulnerabilities found |
| 09-19 的回歸測試 | `uv run pytest tests/test_api_keys_not_in_urls.py` | 4 passed（但見 L2：白名單漏了一個模組） |
| ruff（含 `S` 規則） | `uv run ruff check .` | All checks passed |
| 密鑰掃描 | 工作樹＋全歷史（201 個 ref）比對常見金鑰樣式、PEM／PPK、帶帳密 URL | 除 L7 外 0 筆 |
| GitHub 設定 | `gh api .../branches/main/protection`、`.../actions/permissions/workflow`、`.../secret-scanning/alerts` | 見 §4 |
| 任務檔驗證 | `npm run check:tasks` | 通過（新增 8 張） |

這次沒有修改任何應用程式或設定檔，所以沒有跑 lint／型別／測試；八張票各自寫了該跑的指令。

## 7. 建議的處理順序

1. **M1 `INTERNAL_PROXY_TOKEN` 必填**（P1 api）。改動最小，但要先做 §5 第 2 項。
2. **L2 Google Weather 金鑰走 header**（P2 api）。便宜，而且把回歸測試從白名單改成掃描
   之後，這一類就不會再漏。
3. **L1 owner 停權守門**（P2 api）。
4. **M2 第三方腳本離開特權路由**（P2 web），做完才輪到 `connect-src` 轉強制。
5. **L7–L9 刮乾淨＋加測試**（P2 docs）。倉庫是公開的。
6. 三張 P3（BFF 縱深、nginx 邊緣、供應鏈釘選）順序隨意；供應鏈那張裡 `docker-compose.prod.yml`
   的 tag 要等 09-13 的 compose 票解除封鎖。
