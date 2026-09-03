# Mokaair 資安檢查報告（2026-09）

- 檢查基準：`main` 分支 commit `4c61b14`（2026-09-03）
- 修正分支：`claude/security-audit-hwyj2q`
- 範圍：`apps/api`（FastAPI、RQ workers）、`apps/web`（Next.js 16 BFF 與前端）、`apps/api/deployment_agent` 與 `ops/deployer`（主機部署 agent）、Docker／Compose、GitHub Actions、相依套件、Git 歷史與密鑰掃描
- 方法：唯讀的原始碼審閱，針對每個關鍵發現回到原始碼逐行確認；修正後以單元／整合測試、型別檢查、正式建置、瀏覽器載入檢查驗證。**沒有**對正式環境做任何滲透測試或流量測試，也沒有存取任何線上主機。

## 1. 整體評估

這個專案的安全基礎比同規模的專案紮實很多。密碼用 Argon2、JWT 有 `auth_version` 版本撤銷、OAuth 有 PKCE＋伺服器端一次性 state＋瀏覽器綁定＋完整 ID token 驗證、所有使用者資源都是 owner-scoped 查詢（沒有找到任何 IDOR）、分享 token 只存 SHA-256、部署 agent 用 body-bound HMAC＋一次性 nonce＋時間窗、生產設定在啟動時就拒絕不安全值、分析資料不存原始 IP、Git 歷史沒有任何密鑰、也沒有使用 python-jose／passlib 這類有 CVE 紀錄的套件。

需要處理的問題集中在三類：

1. **一個真正的權限漏洞**：`ADMIN_EMAILS` 裡尚未註冊的 Email 可以被任何人搶先註冊而直接成為管理員（含部署中心）。
2. **幾個可被濫用的信任邊界**：後台可把帶金鑰的供應商 base URL 指向任意主機、登出不撤銷 token、BFF 與 webhook 先把整個請求讀進記憶體再檢查大小、沒有 CSP。
3. **基礎設施衛生**：沒有 `.dockerignore`、`package.json` 用 `latest`、CI workflow 輸入可注入 shell、部署 agent 安裝腳本的權限錯誤。

| 嚴重度 | 數量 | 本次已修正 | 僅列為建議／註記 |
|---|---|---|---|
| High | 4 | 4（其中 1 項為文件化信任邊界） | 0 |
| Medium | 19 | 14 | 5 |
| Low | 21 | 10 | 11 |
| Info | 9 | 0 | 9 |

嚴重度定義：High＝可直接取得權限或外洩密鑰；Medium＝需要既有權限或特定條件才能利用，但影響範圍大；Low＝縱深防禦或影響有限；Info＝設計註記，不需要行動。

## 2. 發現清單

狀態欄：**已修**＝本分支已修正並附測試；**建議**＝需要產品或流程決策，只列入後續建議；**註記**＝不需行動的設計說明；**接受**＝評估後決定不改的風險。

### 2.1 FastAPI（`apps/api`）

| 編號 | 嚴重度 | 標題 | 位置 | 狀態 |
|---|---|---|---|---|
| API-01 | High | 註冊 `ADMIN_EMAILS`／`DEPLOY_ADMIN_EMAILS` 內的 Email 即成為管理員，沒有 Email 驗證 | `app/auth/service.py::is_admin_user`、`app/auth/router.py::register` | 已修 |
| API-02 | Medium | 登出不撤銷 access token（`jti` 有簽發但未使用） | `app/auth/router.py::logout` | 已修 |
| API-03 | Medium | 後台可設定的 FlightAware／Skyscanner／Duffel／Google Travel Impact／Travelpayouts base URL 未綁定官方主機，可把 API 金鑰送到攻擊者主機 | `app/admin/service.py::_validate_provider_values` | 已修 |
| API-04 | Medium | `apply_runtime_overrides` 讀取資料庫覆寫值時不重新驗證，直接寫入資料庫可繞過所有 URL 檢查 | `app/admin/service.py::apply_runtime_overrides` | 已修 |
| API-05 | Medium | 沒有全域請求大小上限；LINE webhook 先把整個 body 讀進記憶體才檢查 | `app/middleware.py`、`app/line/router.py` | 已修 |
| API-06 | Medium | 生產環境未驗證 `TRUST_PROXY_CLIENT_IP`（為 false 時所有 IP 限流塌成同一個 bucket）；`API_CORS_ORIGINS=*` 在非生產環境可與 credentials 併用 | `app/config.py`、`app/main.py` | 已修 |
| API-07 | Low | LIKE 萬用字元未逸出，公開的 `/hotspots/rankings?q=` 可用 `%_%_%` 觸發昂貴掃描 | `app/hotspots/service.py`、`hotspots/admin_router.py`、`foods/admin_router.py` | 已修 |
| API-08 | Low | 上游供應商錯誤原文（含內部 URL）回傳給用戶端 | `app/flights/router.py`、`app/search/router.py` | 已修 |
| API-09 | Low | `ACCESS_TOKEN_EXPIRE_MINUTES` 沒有上限 | `app/config.py` | 已修 |
| API-10 | Medium | 任一管理員都可把任何帳號升為管理員，不需重新輸入密碼；被劫持的管理員 session 可建立持久後門 | `app/admin/users.py::update_admin_user` | 建議 |
| API-11 | Low | `TRUST_PROXY_CLIENT_IP=true` 時，任何能連到 `api:8000` 的同網路容器都能偽造 `X-Travel-Client-IP` | `app/infra.py::client_ip`、`docker-compose.prod.yml` | 建議 |
| API-12 | Low | 密碼政策只有長度（10–128），`1234567890` 可通過 | `app/auth/schemas.py` | 建議 |
| API-13 | Low | LINE 登入的 `email_verified` 以「有 email」推定，Google／Apple 則讀取真正的 claim | `app/auth/oauth.py` | 註記 |
| API-14 | Low | 航班 clickout 的 303 轉址只驗 HTTPS，不像 affiliate 流程有 host allowlist | `app/search/router.py` | 建議 |
| API-15 | Low | `canonical_external_url` 擋 IP 字面值但不解析 DNS；後端不會抓取這些網址，影響僅限外連 | `app/hotspots/guides.py` | 註記 |
| API-16 | Low | 分析用的每日訪客 hash 以 `APP_SECRET_KEY` 當 HMAC key，輪替密鑰會同時中斷訪客統計連續性 | `app/analytics/service.py` | 建議 |
| API-17 | Low | 三處先撈出使用者全部 rows 再在 Python 過濾（flight offers、trips、alerts），大量資料時放大延遲 | `app/search/router.py`、`restaurants/user_router.py`、`alerts/router.py` | 建議 |
| API-18 | Info | `GET /providers/status` 未登入即可讀取供應商配置清單；`X-Response-Time-Ms` 是免費的時間側通道；RQ 以 pickle 序列化工作（Redis 已強制密碼）；`naver_maps_client_id` 同時被當作 secret 與公開值；API 端未送 HSTS（應由反向代理處理） | 各處 | 註記 |

### 2.2 部署 agent 與主機腳本（`apps/api/deployment_agent`、`ops/deployer`）

| 編號 | 嚴重度 | 標題 | 位置 | 狀態 |
|---|---|---|---|---|
| OPS-01 | High | `travel-deployer` 屬於 `docker` 群組，等同主機 root；systemd 強化只限制 agent 程序，不限制它能啟動的容器。這是設計取捨，但原本沒有寫在任何文件裡 | `travel-scanner-deployer.service`、`install.sh` | 已修（文件化） |
| OPS-02 | Medium | 負數或非數字 `Content-Length` 讓 agent `read(-1)` 讀到 EOF（驗證簽章之前）；連線沒有 timeout | `deployment_agent/server.py` | 已修 |
| OPS-03 | Low | 非 ASCII 簽章讓 `hmac.compare_digest` 拋出 `TypeError`，逃出 handler 的 try | `deployment_agent/security.py` | 已修 |
| OPS-04 | Medium | `/etc/travel-scanner` 建立為 `root:root 0750`，agent 使用者無法 traverse 讀取 `runtime.env`，部署會以「runtime environment file is missing」失敗 | `install.sh` | 已修 |
| OPS-05 | Medium | 安裝腳本從不設定 `runtime.env`（含所有正式密鑰）的權限；`deployer.env` 只在第一次安裝時設定 | `install.sh` | 已修 |
| OPS-06 | Medium | `/run/travel-scanner-deployer` 在 tmpfs 上，重開機後由 agent 以 `travel-deployer` 群組重建，API 容器（gid `travel-api`）失去 socket 存取 | `server.py`、systemd unit | 已修 |
| OPS-07 | Medium | systemd unit 缺少 `PrivateDevices`、`RestrictAddressFamilies`、`RestrictNamespaces`、`CapabilityBoundingSet` 等強化 | systemd unit | 已修（部分） |
| OPS-08 | Medium | CI gate 以 workflow 的顯示名稱 `CI` 比對，而名稱來自被部署的那個 commit；能推到 `main` 的人即等同主機 root。repo 內看不到 branch protection／required reviews 設定 | `deployment_agent/executor.py::_ci` | 建議 |
| OPS-09 | Low | mirror fetch 使用強制更新（`+refs`），`main` 可被 force-push 倒退 | `deployment_agent/executor.py` | 註記 |

### 2.3 Next.js（`apps/web`）

| 編號 | 嚴重度 | 標題 | 位置 | 狀態 |
|---|---|---|---|---|
| WEB-01 | Medium | BFF proxy 與 LINE webhook 先 `arrayBuffer()` 讀完整個 body 才比大小；`Content-Length` 可省略或造假，chunked 上傳可耗盡記憶體 | `app/api/travel/[...path]/route.ts`、`app/api/line/webhook/route.ts` | 已修 |
| WEB-02 | Medium | 沒有 Content-Security-Policy | `next.config.ts`、`proxy.ts` | 已修 |
| WEB-03 | Medium | `out/*` 轉址路由把整包 Cookie 轉發給 API、取最左（可偽造）的 `X-Forwarded-For` 當客戶端 IP、`new URL()` 沒包 try 會變成 500 | `app/[locale]/out/guides/[guideId]/route.ts`、`out/hotspots/[hotspotId]/source/route.ts` | 已修 |
| WEB-04 | Low | `out/guides` 是 GET 卻觸發會消耗會員配額（120／小時）的上游 POST，跨站連結可代替已登入會員消耗配額 | `out/guides/[guideId]/route.ts` | 接受（見 §4） |
| WEB-05 | High | `apps/web/package.json` 有 15 個相依用 `"latest"`；任何 `npm install` 都會無聲升到剛發布的大版本（供應鏈風險） | `apps/web/package.json` | 已修 |
| WEB-06 | Low | 約 15 處 `href`／`action`／`location.assign` 直接使用供應商、AI 或後台輸入的 URL。React 19 已在 render 時阻擋 `javascript:`，但 `location.assign` 不受保護 | `components/*` | 已修 |
| WEB-07 | Low | GA4 measurement ID（後台可設定）未驗證格式就插入 `<Script src>` | `components/analytics-provider.tsx` | 已修 |
| WEB-08 | Low | Dockerfile 的 `NEXT_PUBLIC_SITE_URL` 預設 `http://localhost:3000`，漏傳 build arg 會把 localhost 烙進正式版當允許的 Origin | `apps/web/Dockerfile` | 已修 |
| WEB-09 | Low | proxy 的 15 秒 timeout 只涵蓋 headers，不涵蓋回應主體讀取 | `route.ts` | 已修 |
| WEB-10 | Low | OAuth flow cookie 是未簽章的 base64 JSON（API 端仍以 Redis 驗證 state／binding，影響有限） | `app/api/auth/oauth/_shared.ts` | 建議 |
| WEB-11 | Low | 後台頁面只有 client 端門檻，未登入者可看到完整後台版面與功能清單（資料仍受 API 403 保護） | `app/[locale]/admin/layout.tsx` | 建議 |
| WEB-12 | Low | HSTS 沒有 `includeSubDomains`／`preload` | `next.config.ts` | 建議 |
| WEB-13 | Info | `travel_access` 可加 `__Host-` 前綴；`secure` 旗標在三處以兩種方式計算；LINE webhook replay 保護為 event id＋7 天，沒有時間戳 | 各處 | 註記 |
| WEB-14 | Info | 13 處 `target="_blank"` 沒有 `rel`（現代瀏覽器已預設 `noopener`） | `components/*` | 註記 |

### 2.4 基礎設施與 CI

| 編號 | 嚴重度 | 標題 | 位置 | 狀態 |
|---|---|---|---|---|
| INF-01 | High | 沒有任何 `.dockerignore`；API image 用 `COPY . .`，開發機上的 `apps/api/.env`、`.venv`、tests、主機專用的 `deployment_agent` 都會進 image layer | `apps/api/Dockerfile` | 已修 |
| INF-02 | Medium | `.gitignore` 沒有涵蓋 `.env.local`／`.env.production`、`ops/deployer/deployer.env`、`*.sqlite3`、`coverage/` | `.gitignore` | 已修 |
| INF-03 | Medium | `workflow_dispatch` 的自由文字輸入直接插進 `run:` shell，其中一個 job 持有 Amadeus／Google 密鑰 | `airline-crawler-validation.yml`、`live-provider-validation.yml` | 已修 |
| INF-04 | Medium | `ci.yml` 沒有 `permissions:` 區塊，`GITHUB_TOKEN` 依 repo 預設（舊 repo 為讀寫） | `.github/workflows/ci.yml` | 已修 |
| INF-05 | Medium | 開發用 compose 把 `travel:travel` 的 Postgres 與無密碼 Redis 綁在 `0.0.0.0` | `docker-compose.yml` | 已修 |
| INF-06 | Medium | 正式 compose 沒有 `read_only`／`tmpfs`、沒有網路分段（web 可直連 postgres）、api／web 沒有 healthcheck | `docker-compose.prod.yml` | 建議 |
| INF-07 | Medium | API image 單階段，`pip`、`uv`、原始碼都留在正式 image | `apps/api/Dockerfile` | 建議 |
| INF-08 | Low | 第三方 action `astral-sh/setup-uv@v6` 以可變 tag 釘住 | 所有 workflow | 建議 |
| INF-09 | Low | migration `0033` 的 downgrade 把社群帳號的 `password_hash` 設成空字串（無法通過驗證，但只能靠重設密碼復原） | `migrations/versions/0033_social_login_identities.py` | 建議 |
| INF-10 | Info | repo 內沒有 TLS 終端／反向代理設定；`apps/web/AGENTS.md` 是被追蹤的 AI agent 指令檔 | — | 註記 |

## 3. 已修正項目說明

### API-01 保留管理員 Email 不可自助註冊（High）

`is_admin_user` 以 `ADMIN_EMAILS` 判定管理員，而 `POST /auth/register` 對任何 Email 直接建立帳號、沒有 Email 驗證流程。只要知道或猜到 allowlist 裡尚未註冊的地址，搶先註冊就是管理員；`can_deploy_user` 只再檢查「自己的」密碼，所以部署中心也一併淪陷。OAuth 首次建立帳號的路徑不受影響，因為它要求 provider 已驗證的 Email。

修正：`register` 對 `ADMIN_EMAILS ∪ DEPLOY_ADMIN_EMAILS` 內的地址回 403 `admin_email_reserved`（五語系訊息）。新增 `python -m app.cli create-admin --email ...` 作為不經公開表單建立管理員的路徑（密碼由 `getpass` 或 `--password-stdin` 提供，沿用 `RegisterRequest` 的驗證與 `set-admin` 的稽核紀錄）。README 的 Administration 段落已改寫。

測試：`tests/test_auth_hardening.py`（保留地址註冊 → 403、無 cookie、session 未被寫入；大小寫不敏感；其他語系訊息）。

### API-02 登出撤銷 token（Medium）

登出原本只刪 cookie，被竊取的 token 在到期前（預設 60 分鐘）持續有效。修正：`AccessTokenClaims` 帶出 `jti` 與 `exp`，登出時把 `jti` 寫入 Redis deny-list（TTL 等於剩餘壽命），`current_user`／`optional_current_user` 在資料庫檢查之後查 deny-list。Redis 失效時回 503 `session_check_unavailable`（fail-closed，與限流器一致）。登出永遠回 204 並清 cookie，無效 token 不會寫入任何東西。

測試：登出後同一 token 以 header 或 cookie 呈現都 401；Redis 故障 → 503；無 token 登出仍清 cookie。

### API-03／API-04 供應商 base URL 綁定官方主機（Medium）

`app/config.py` 新增 `OFFICIAL_PROVIDER_HOSTS` 與 `official_provider_url_ok()`，後台寫入驗證（`_validate_provider_values`）、生產環境啟動驗證（有對應金鑰時）與資料庫覆寫讀取（`apply_runtime_overrides`）共用同一份表：OpenAI、Anthropic、MiniMax、FlightAware（`aeroapi.flightaware.com`）、Skyscanner（`partners.api.skyscanner.net`）、Duffel（`api.duffel.com`）、Google Travel Impact（`travelimpactmodel.googleapis.com`）、Travelpayouts、LINE。讀取時若資料庫值不在官方主機，忽略該欄位並記錄警告，回到環境變數值。

未綁定：NAVITIME（`navitime_api_base_url`，官方 gateway 主機隨合約而異）、KKday／Klook／Agoda（`*_api_base_url` 目前沒有任何 client 使用）。這四個仍只驗 HTTPS；若日後啟用，請在同一張表加入官方主機。

### API-05 請求大小上限（Medium）

新增純 ASGI 的 `RequestBodyLimitMiddleware`：`Content-Length` 超過上限回 413（負數或非數字回 400），沒有宣告長度的 chunked body 在串流時計數、超限即中止。上限由 `API_MAX_REQUEST_BYTES` 設定（預設 5 MiB，與 BFF 的 `API_PROXY_MAX_BODY_BYTES` 一致）。LINE webhook 另外在讀取 body 前先比對 `Content-Length`。

### API-06 API 進程啟動檢查（Medium）

新增 `Settings.validate_api_serving_security()`，只在 `app/main.py`（HTTP API 進程）呼叫，不影響 workers 與 CLI：`API_CORS_ORIGINS` 含 `*` 在任何環境都拒絕（因為 `allow_credentials=True`）；生產環境 `TRUST_PROXY_CLIENT_IP` 必須為 true（正式 compose 已如此設定）。`ACCESS_TOKEN_EXPIRE_MINUTES` 限制在 5–1440。

### API-07／API-08 LIKE 逸出與錯誤訊息（Low）

`app/db.py::escape_like` 取代原本只在 `admin/users.py` 內的逸出邏輯，套用到四個 `ilike` 查詢。`flights/router.py` 與 `search/router.py` 三處把 `str(exc)` 改為固定訊息，原文改記錄到 log。

### OPS-02～OPS-07 部署 agent 與主機腳本（Medium／Low）

- `server.py`：`Content-Length` 解析失敗或負數回 400、超過 64 KiB 回 413，都在 HMAC 驗證之前且不再讀取；handler 設定 15 秒 socket timeout。
- `security.py`：簽章必須符合 `[0-9a-f]{64}` 才進入 `compare_digest`。
- `install.sh`：先建立帳號再建目錄；`/etc/travel-scanner` 改為 `root:travel-deployer 0750`；`runtime.env`／`deployer.env` 每次執行都重設為 `0640 root:travel-deployer`；`/run/travel-scanner-deployer` 重設為 `travel-deployer:travel-api 0750`；移除永遠為真的 guard。
- systemd unit：`ExecStartPre=+/bin/sh -c 'install -d ... && chown travel-deployer:travel-api ... && chmod 0750 ...'` 在每次啟動（含重開機後）重建 socket 目錄；新增 `PrivateDevices`、`ProtectClock`、`ProtectHostname`、`RestrictNamespaces`、`RestrictRealtime`、`RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6`、`SystemCallArchitectures=native`、`CapabilityBoundingSet=`。刻意沒有加 `SystemCallFilter`／`ProtectProc`，因為無法在此環境驗證 docker CLI 相容性。
- `ops/deployer/README.md` 新增「Trust boundary」段落，明載 docker 群組等同 root、檔案權限、token 需為 fine-grained 唯讀 Actions 權限、變更後必須重跑 `preflight`。

**注意**：`install.sh` 與 unit 檔只做了語法檢查（`bash -n`、`systemd-analyze verify`），沒有在真實主機執行。部署前請先在 staging 主機跑一次 `install.sh` 與 `preflight`。

### WEB-01／WEB-09 串流限量的請求主體（Medium）

`lib/request-body.ts::limitedRequestBody` 先檢查宣告長度，再逐 chunk 計數、超限即 `cancel()`。BFF proxy 與 LINE webhook 都改用它；proxy 的 timeout 也延伸涵蓋非 SSE 回應主體的讀取（逾時回 504 `upstream_timeout`）。

### WEB-02 Content-Security-Policy（Medium）

- **強制**（`next.config.ts`，所有路徑）：`frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self' https:`。`https:` 是必要的，因為 clickout 表單 POST 到本站後會 303 到合作夥伴，Chrome 會用 `form-action` 檢查轉址目標。
- **Report-Only**（`proxy.ts` 中介層，HTML 路由）：以每個請求產生的 nonce 建立嚴格政策（`lib/csp.ts::buildStrictContentSecurityPolicy`），涵蓋 GA4、NAVER Maps、Google Maps Embed iframe、任意 HTTPS 圖片。中介層把政策同時寫進 request header，Next.js 會據此替自己的 inline script 加上 nonce；layout 讀取 `x-nonce` 給 theme bootstrap script。
- 驗證：以正式建置啟動伺服器，用 Chromium 載入 `/zh-TW`、`/zh-TW/hotspots`、`/zh-TW/search`、`/zh-TW/login`、`/en/pricing`、`/zh-TW/trips`：每頁全部 script 都帶 nonce（14～16／14～16）、theme script 的 nonce 與 header 一致、`securitypolicyviolation` 事件為 0。
- 轉為強制的步驟見 §7。

### WEB-03 `out/*` 轉址路由（Medium）

改為只從 `travel_access` cookie 取出 token 送 `Authorization: Bearer`（不再轉發整包 Cookie）、改用與主 proxy 相同的 `forwardedClientAddress()`（取最右的 XFF）、`new URL()` 包進 try 後回 502。測試新增 http:／帶帳密／`javascript:`／畸形 URL 都回 502，畸形 id 在呼叫 API 前就 404。

### WEB-05 相依版本釘選（High）

`"latest"` 全部改為目前 lock 檔版本的 caret 範圍（`next ^16.3.3`、`react ^19.2.8` …），並用 `npm install --package-lock-only` 同步 lock 內的 spec；lock 內沒有任何 `version` 變動，`npm ci` 通過。

### WEB-06～WEB-08 前端縱深防禦（Low）

`lib/navigation.ts::safeExternalHref` 只放行 `http:`／`https:`（NAVER app 連結另外允許 `nmap:`），套用到 hotel／flight offer、餐廳、景點、導航、後台候選文章與來源連結，以及 LINE 綁定的 `location.assign`。GA4 ID 必須符合 `^G-[A-Z0-9]{4,20}$`。Dockerfile 的 `NEXT_PUBLIC_SITE_URL` 不再有預設值，缺少即 build 失敗。

### INF-01～INF-05 基礎設施（High／Medium）

新增 root 與 `apps/api` 的 `.dockerignore`；`.gitignore` 補上 `.env.*`（保留 `.env.example`）、`*.env`、`*.sqlite3*`、`coverage/`、`playwright/.auth/`；`ci.yml` 加 `permissions: contents: read`；三個 `workflow_dispatch` 步驟改為經 `env:` 傳入再以 `"$ROUTE_ORIGIN"` 引用；開發用 compose 的 5432／6379／8000 改綁 `127.0.0.1`。

## 4. 評估後接受的風險

- **WEB-04** `out/guides` 的 GET 觸發會消耗配額的上游 POST。曾考慮以 `Sec-Fetch-Site: cross-site` 拒絕，但這會讓已登入會員從外部分享連結（LINE、部落格）點進來時一律 403，破壞合法流量；上游已有每位會員 120／小時的限流，實際影響是統計污染與配額消耗，屬 Low。若要處理，建議改成「先顯示本站確認頁，再由同站點擊觸發 POST」。

## 5. 做得好、請勿「修壞」的部分

- Argon2 密碼雜湊（`pwdlib`）、不存在帳號也做等量 hash 驗證（避免帳號列舉時間差）、登入成功清除帳號限流計數。
- `auth_version` 讓改密碼、停用帳號、解除社群綁定都能立刻讓所有既有 token 失效。
- OAuth：state／nonce／PKCE 都是 32–64 bytes 隨機值、Redis `GETDEL` 一次性、瀏覽器綁定以 SHA-256 存放並 `compare_digest`、ID token 以 JWKS `kid`＋RS256＋aud／iss／exp 驗證、Email 相同絕不自動合併、link 意圖綁定 user id＋`auth_version`。
- 分享 token 256 bits、只存 SHA-256、可撤銷；公開回應使用明確欄位白名單。
- 所有 trips／alerts／saved items／flight lookups／affiliate context 都是 owner-scoped 查詢，沒有找到 IDOR。
- 航空公司爬蟲的 SSRF 防護（固定主機白名單、手動處理轉址且要求同主機、robots.txt、大小上限）與 Google Maps 短網址展開的逐跳主機驗證。
- 部署 agent：HMAC 涵蓋 method／path／body 摘要、±60 秒時間窗、nonce 在簽章通過後才寫入、命令面固定且 `shell=False`、備份先於 migration、三次健康檢查、回滾不降級資料庫、密鑰經 `sanitize()`。
- 後台密鑰只回傳遮罩、Fernet 加密存放、連線測試訊息會把已知密鑰值刮掉、未知欄位一律拒絕。
- 生產設定啟動驗證：32 字元以上且互不相同的 `APP_SECRET_KEY`／`SETTINGS_ENCRYPTION_KEY`、HTTPS origin、非預設資料庫密碼、Redis 密碼、官方 AI／LINE 主機。
- 分析資料：不存原始 IP、每日輪替的 keyed hash、遵守 DNT／GPC、路徑去識別化、只存 referrer 類別、保留期限由排程強制。
- BFF：以全新 `Headers` 物件建構上游請求（Cookie／Authorization／XFF 結構上不可能穿透）、cookie→Bearer 轉換、`Set-Cookie` 不回傳、mutating 方法要求同源 `Origin`（缺少即拒絕）、路徑段拒絕 `..`／分隔符、轉址只允許 HTTPS 或同源、`safeNextPath` 防開放式轉址、OAuth 錯誤碼白名單。
- 容器：非 root、`cap_drop: ALL`、`no-new-privileges`、正式環境只綁 loopback、Redis 需密碼、必要密鑰缺少即拒絕啟動。
- CI 每次 push 都跑 `pip-audit` 與 `npm audit --audit-level=high`；帶密鑰的 workflow 全部只能 `workflow_dispatch`，fork PR 碰不到密鑰；`::add-mask::` 用法正確。
- 相依套件全部是目前版本，沒有 python-jose、passlib、bcrypt、pyyaml；兩個 lock 檔都有完整 hash 並以 frozen 安裝。

## 6. 無法從 repo 驗證的項目

以下項目需要在 GitHub 設定頁或正式主機上確認，本次沒有存取權限：

1. `main` 的 branch protection／required reviews／rulesets（OPS-08 的嚴重度完全取決於此；repo 內沒有 `CODEOWNERS` 與 `dependabot.yml`）。
2. repo 的 `GITHUB_TOKEN` 預設權限（Settings → Actions → Workflow permissions）。
3. 反向代理／TLS 終端設定（不在 repo 內）：是否送 HSTS、是否剝除來自外部的 `X-Travel-Client-IP` 與 `X-Forwarded-For` 再自行設定、LINE webhook 如何到達 FastAPI（BFF 的 `/api/travel/line/webhook` 因為 Origin 檢查與 header 白名單無法通過驗證，LINE 必須另有路徑）。
4. Google Maps 瀏覽器金鑰與 NAVER 瀏覽器 client id 是否已在雲端主控台限制 API 與 referrer。
5. 部署 agent 的 GitHub PAT 實際範圍。
6. `/etc/travel-scanner/*.env` 在正式主機上的實際權限、`DEPLOYMENTS_ENABLED` 目前是否為 true。
7. `install.sh` 與 systemd unit 的修改只做了語法與靜態檢查，沒有在主機上執行。

## 7. 後續建議（依優先順序）

1. **確認 branch protection**：`main` 要求 PR review 與 CI 通過；因為能推到 `main` 的人等同主機 root（OPS-01、OPS-08）。
2. **管理員升權加二次驗證**（API-10）：`PUT /admin/users/{id}` 變更 `is_admin` 時要求 `current_password`（部署中心已有相同模式），前端 `admin-users-panel` 加密碼欄位（五語系）。
3. **CSP 轉為強制**：在正式環境觀察一到兩週瀏覽器 console 沒有 `Content-Security-Policy-Report-Only` 違規後，把 `proxy.ts` 的 response header 從 `Content-Security-Policy-Report-Only` 改為 `Content-Security-Policy`（request header 維持不變），並考慮加入 `report-to` 端點收集違規。若地圖或 GA 出現違規，把對應網域加入 `lib/csp.ts`。
4. **正式 compose 強化**（INF-06、API-11）：`read_only: true`＋`tmpfs: [/tmp]`、`frontend`／`backend` 兩個網路（`web` 不接 `backend`）、api／web `healthcheck`；需在 staging 驗證 uvicorn 與 Next standalone 在唯讀根目錄下的行為。
5. **後台頁面伺服器端門檻**（WEB-11）：`admin/layout.tsx` 以 cookie 呼叫 `/auth/me`，非管理員直接 `redirect`；需同步調整以 `page.route` mock API 的 e2e。
6. **API image 多階段建置**（INF-07）、**action 釘 SHA**（INF-08）、加入 Dependabot 或 Renovate。
7. **HSTS** 加 `includeSubDomains`（確認所有子網域皆走 HTTPS 後再加 `preload`）（WEB-12）。
8. **密碼政策**（API-12）：加入常見密碼清單或 zxcvbn 類強度檢查。
9. **分析 hash key 分離**（API-16）：用 HKDF 從 `SETTINGS_ENCRYPTION_KEY` 派生專用 key，讓 `APP_SECRET_KEY` 可以獨立輪替。
10. **OAuth flow cookie 簽章**（WEB-10）、**flight clickout host allowlist**（API-14）、**`0033` downgrade 改用不可驗證的 sentinel**（INF-09）、`/providers/status` 改為需登入（API-18）。
11. **ruff 加入 `S`（flake8-bandit）規則**，可自動抓到 LIKE 逸出與 body 限制這類問題。

## 8. 本次驗證

| 項目 | 指令 | 結果 |
|---|---|---|
| API lint／型別 | `uv run ruff check .`、`uv run mypy app` | 通過（152 檔） |
| API 測試 | `uv run pytest` | 419 passed、26 skipped（整合測試需 Postgres／Redis，CI 會跑） |
| Web lint／型別／i18n | `npm run lint:web`、`npm run typecheck:web`、`npm run check:i18n` | 通過 |
| Web 單元測試 | `npm run test:web` | 74 檔 225 tests 通過 |
| 工具測試 | `npm run test:tools` | 3 passed |
| 正式建置 | `npm run build:web` | 通過；所有 `[locale]` 路由維持 dynamic，Proxy（middleware）正常 |
| 瀏覽器 e2e | `npx playwright test e2e/navigation.spec.ts` | 59／60 通過；唯一失敗是沙箱內較舊的 Chromium 把日期格式化成「11月11日 週三」（多一個空白），與本次變更無關 |
| CSP 檢查 | 自訂 Playwright 腳本載入 6 個頁面 | 每頁 script 全數帶 nonce、theme script nonce 相符、0 個 report-only 違規 |
| 相依稽核 | `npm ci`、`npm audit --audit-level=high`、`uv run pip-audit --local --skip-editable` | 通過（見 commit 訊息） |
| Compose／YAML | `docker compose config`、`docker compose -f docker-compose.prod.yml config --quiet`、PyYAML 解析所有 workflow | 通過 |
| 主機腳本 | `bash -n ops/deployer/install.sh`、`systemd-analyze verify` | 通過（未於主機執行） |
