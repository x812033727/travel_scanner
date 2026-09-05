# Mokaair 資安檢查報告（第二輪，2026-09-04）

- 檢查基準：`main` 分支 commit `5c2d26e`（2026-09-04）
- 修正分支：`claude/security-audit-k9pk77`
- 前次審計：[`security-audit-2026-09.md`](security-audit-2026-09.md)（基準 `4c61b14`，2026-09-03）。兩個基準之間合入了約 31,000 行新程式碼（hotspots 候選管線、foods 分類、住宿區與路線、Gemini 整合、滑動 session、登出撤銷、BFF cookie 轉發），本輪的重點是這批未審計過的程式碼，以及前次「已修」項目的回歸驗證。
- 方法：唯讀原始碼審閱。自動化掃描規劃了 26 個面向，其中 **10 個完成完整掃描**（auth/session、OAuth、authz/IDOR、admin 權限、部署 agent、BFF proxy、SSRF、SQL injection、前端 XSS、CSP/標頭），其餘 16 個因執行資源中斷只做了重點抽查（見 §6）。掃描產出的 35 個原始發現**全部由人工回到現行原始碼逐行驗證**後才分類；修正以單元／整合測試、ruff、mypy strict、eslint、tsc、i18n 檢查驗證。沒有對正式環境做任何滲透或流量測試。

## 1. 整體評估

前次審計的絕大多數控制在 31,000 行新程式碼落地後仍然完整：`OFFICIAL_PROVIDER_HOSTS` 有跟上 Gemini／NAVITIME／Ekispert／ODsay 四個新供應商、`escape_like` 有套用到新的 foods 搜尋、BFF 的標頭白名單與 `X-Request-ID` 格式驗證正確、CSP nonce 不可能被客戶端指定（`proxy.ts` 用 `set()` 覆寫）、相依套件 `pip-audit` 與 `npm audit` 均為零已知漏洞。

需要修的問題集中在兩類：

1. **一個真正的 high 回歸**：#142／#145 引入滑動續期後，登出的 deny-list TTL 仍以「被出示那份 token」的 `exp` 計算，而同一條登入鏈裡較晚續期的兄弟 token 的 `exp` 更晚——deny 項目先過期，被複製走的 cookie 就能復活並自我續期到 30 天上限，而受害者之後的每次登出都拿到新的 `jti`，永遠撤不到它。
2. **前次修正沒有覆蓋到的旁路**：API-01 的保留管理員信箱擋了 `/auth/register` 卻沒擋 OAuth 首次建帳號；WEB-01 的請求體上限沒套到未登入的 OAuth callback；WEB-06 的 `safeExternalHref` 沒進到 search-experience／route-segment-card／新的美食卡片。

| 嚴重度 | 確認並修正 | 確認列為建議 | 經查證不成立 |
|---|---|---|---|
| High | 1 | 0 | 0 |
| Medium | 6 | 3 | 1 |
| Low | 6 | 4 | 4 |
| Info | 1 | 6 | 3 |

## 2. 已修正項目

| 編號 | 嚴重度 | 標題 | 位置 |
|---|---|---|---|
| R2-01 | High | 登出 deny-list 的 TTL 只涵蓋被出示的那份 token，較晚續期的兄弟 token 能在 deny 項目過期後復活並續期到 30 天上限（API-02 修正在滑動續期下的回歸） | `app/auth/service.py::revoke_access_token` |
| R2-02 | Medium | 保留管理員信箱（`ADMIN_EMAILS`／`DEPLOY_ADMIN_EMAILS`）仍可經 OAuth 首次登入建立帳號（API-01 修正不完整；LINE 的 `email_verified` 又是「有 email 即推定」，見前次 API-13） | `app/auth/oauth.py` 新帳號分支 |
| R2-03 | Medium | 未登入的 OAuth callback `POST` 用 `request.formData()` 無上限讀入整個 body（WEB-01 修正未覆蓋此路由） | `apps/web/app/api/auth/oauth/_shared.ts` |
| R2-04 | Medium | 任一資料庫旗標管理員可「停權」`ADMIN_EMAILS`／`DEPLOY_ADMIN_EMAILS` 指定的管理員（停權會 bump `auth_version` 立刻踢下線），效果等同被擋下的「降權」 | `app/admin/users.py::update_admin_user` |
| R2-05 | Medium | Gemini 回應裡的 grounding URI 未經驗證就先發出 GET（一跳、不跟隨轉址），被污染的搜尋結果可指向 `http://127.0.0.1` 或雲端 metadata 位址（盲 SSRF） | `app/hotspots/guides.py` |
| R2-06 | Medium | agent 部署啟動清單漏掉 `hotspot-collector` 與 `analytics-scheduler`：經 agent 部署的主機從未執行分析資料保留期清除（隱私承諾失效）；回滾用無服務清單的 `up -d` 會把舊版 `migrate` 對著較新 schema 重跑，注定失敗 | `deployment_agent/executor.py` |
| R2-07 | Medium | BFF 改轉發 Cookie 後，分析事件的 `is_authenticated` 只認 `Authorization` 標頭，網頁使用者全部被記成未登入（資料正確性） | `app/analytics/service.py` |
| R2-08 | Low | `PUT /trips/{id}/itinerary` 可把普通項目「升級」成 `system_role` 卡片：躲過不可變規則、觸發唯一約束 500、且變成永遠刪不掉 | `app/trips/router.py` |
| R2-09 | Low | `safeExternalHref`（WEB-06）未套用到 search-experience 的供應商連結、route-segment-card 的 `maps_url`、美食卡片的地圖與來源連結 | `apps/web/components/*` |
| R2-10 | Low | 美食 `source_urls` 寫入端無任何 URL 驗證，卻在公開頁面渲染成連結；已套用與餐廳編輯來源相同的公開 HTTPS 驗證 | `app/foods/admin_router.py` |
| R2-11 | Low | `install.sh` 用 `install -d -m 0750 /srv/travel-scanner/releases` 只會把 mode 套在葉子目錄，`/srv/travel-scanner` 本身是 0755 世界可 traverse | `ops/deployer/install.sh` |
| R2-12 | Low | `ExecStartPost=chgrp` 與 agent 建立 socket 是競態（OPS-06 修正的 socket 群組在輸掉時不生效、unit 直接 failed）；改為最多等 10 秒的等待迴圈 | `ops/deployer/travel-scanner-deployer.service` |
| R2-13 | Low | 管理後台關閉 `google_maps_javascript_enabled` 安全閘門後，`/runtime/public-config` 仍照發瀏覽器 Maps key | `app/admin/service.py::public_runtime_config` |
| R2-14 | Info | 保留信箱經 OAuth 被拒時，登入頁只顯示泛用錯誤；補上 `admin_email_reserved` 的五語系訊息與錯誤碼白名單 | `apps/web/app/api/auth/oauth/_shared.ts`、`messages/*/auth.json` |

### R2-01 登出撤銷涵蓋整條續期鏈（High）

`create_access_token` 在續期時刻意沿用同一個 `jti`（#145：「整條鏈只有一個撤銷把手」），但 `revoke_access_token` 的 TTL 是 `presented.exp - now`。攻擊路徑：偷到 cookie 的人各自續期，鏈上就有多份同 `jti`、不同 `exp` 的 token；受害者登出時出示的是自己那份（`exp` 較早），deny 項目在攻擊者那份到期前就先消失，之後攻擊者的 token 通過 `ensure_token_not_revoked`，並立即再續期。受害者後續每次登出都是新登入（新 `jti`），永遠撤不到舊鏈，唯一終點是 30 天絕對上限或改密碼。

修正：TTL 改為 `max(presented.exp, session_started_at + session_absolute_max_days) - now`——絕對上限之後任何同鏈 token 都會被 `session_past_absolute_cap` 拒絕，所以 deny 項目撐到那一刻就涵蓋了所有兄弟。原本斷言 `ttl <= 3600` 的測試等於把缺陷寫成規格，已改寫；新增測試證明：撤銷較早的那份後，deny TTL 大於較晚兄弟的剩餘壽命並涵蓋到絕對上限，且新舊兩份都立即失效。

### R2-02 OAuth 首次建帳號套用保留信箱檢查（Medium）

`/auth/register` 對保留信箱回 403（API-01 修正），但 `exchange_oauth` 的新帳號分支只檢查「email 已驗證」「Email 未被註冊」「註冊開放」。只要在任一 IdP 控制該信箱（LINE 甚至只推定驗證），就能繞過 CLI-only 的管理員建立路徑。修正：同一條 403 `admin_email_reserved` 規則套用到 OAuth 分支，並補 BFF 端錯誤碼白名單與五語系訊息（R2-14）。

### R2-03 OAuth callback 請求體上限（Medium）

Apple 的 form_post callback 是未登入路由，原本 `request.formData()` 會先把任意大小的 body 讀進記憶體。改用 WEB-01 的 `limitedRequestBody`（上限 16 KiB，先檢查宣告長度、再逐 chunk 計數）後以 `URLSearchParams` 解析——OAuth form_post 依規格就是 `application/x-www-form-urlencoded`。超限回轉址錯誤，不再讀取。

### R2-04～R2-13

各修正的細節見對應 commit 訊息與測試：

- **R2-04**：環境指定管理員的保護從「不可降權」擴大為「不可降權也不可停權」，並涵蓋 `DEPLOY_ADMIN_EMAILS`；要移除請先改主機環境設定（與既有 409 `admin_environment_override` 一致）。
- **R2-05**：grounding URI 先過 `canonical_external_url`（HTTPS、無帳密、擋 IP 字面值與 localhost）再發出解析請求；轉址目的地本來就有驗證。新增測試證明 `http://127.0.0.1`、metadata IP、帶帳密 URL 完全不會被抓取。
- **R2-06**：新增 `APPLICATION_SERVICES` 常數涵蓋 compose 裡全部長駐服務；前向啟動與回滾共用同一清單，回滾另加 `--no-deps` 讓舊版 `migrate` 不會被 `depends_on` 拉起來。**注意**：`--no-deps` 的行為只做了程式碼層驗證與單元測試，請比照前次 install.sh 的做法先在 staging 主機演練一次回滾。
- **R2-08**：新的守門條件：`system_role` 只能出現在「本來就是 system 的列」上，新列與升級一律 422；整合測試（CI 的 Postgres 環境）覆蓋升級路徑。
- **R2-09／R2-10**：連結經 `safeExternalHref`（僅 http/https）渲染；`source_urls` 寫入時重用 `validate_editorial_url`（公開 HTTPS、無自訂連接埠、擋內網與供應商自有網域）。既有種子資料全數通過此驗證。
- **R2-11／R2-12**：主機腳本與 systemd unit 只做了語法檢查（`bash -n`、位於無 systemd 環境），部署前請在 staging 跑一次 `install.sh` 與服務重啟。
- **R2-13**：安全閘門關閉時 `google_maps_browser_key` 回 `null`。瀏覽器 key 本來就設計為公開並應在雲端主控台做 referrer 限制，此為縱深防禦。

## 3. 確認屬實、列為建議的項目

| 編號 | 嚴重度 | 說明 | 建議 |
|---|---|---|---|
| R2-15 | Medium | 帳號限流在密碼驗證**之前**計數：任何人拿別人的 Email 連打錯誤密碼即可把該帳號鎖在登入外（帳號鎖定 DoS 與防撞庫的既有取捨） | 改以（Email＋IP）複合 key 或在多次失敗後才升級為帳號級限流；`app/auth/router.py` |
| R2-16 | Medium | SSE 搜尋串流最長 7.5 分鐘，單一帳號可同時開的串流數沒有上限 | 以 Redis 記每帳號進行中的串流數並設上限；`app/search/router.py` |
| R2-17 | Medium | 前次 API-10 仍然成立：管理員互升／互改不需要重新輸入密碼（本輪 R2-04 只堵掉環境指定帳號的停權面） | 依前次建議為 `PUT /admin/users/{id}` 加 `current_password` |
| R2-18 | Low | `POST /auth/register` 對保留信箱回專屬 403，等於可枚舉 `ADMIN_EMAILS` 內容（回應差異是 API-01 修正刻意的 UX 取捨） | 若在意，統一回 409 `email_exists`；同時 R2-02 的 OAuth 路徑也用同一錯誤碼，行為一致 |
| R2-19 | Low | 部署 agent 的工作若在 worker 執行緒死亡時停在 ACTIVE，會永久擋住之後所有部署（SQLite 沒有超時回收） | 啟動時把超過時限的 ACTIVE 工作標記為 failed；`deployment_agent/store.py` |
| R2-20 | Low | web 端登出在上游 503（Redis 故障、撤銷失敗）時仍清瀏覽器 cookie，畫面看起來已登出但 token 未撤銷 | 讓 header-session 在 logout 非 2xx 時提示「未完全登出」 |
| R2-21 | Info | 滑動續期把被竊 cookie 的價值從 1 小時放大到最長 30 天，且沒有「登出所有裝置」 | 提供 bump `auth_version` 的「登出所有裝置」按鈕（改密碼已有同效果） |
| R2-22 | Info | 管理員調整會員額度時，ledger reference 內含操作管理員的 UUID，會回傳給該會員 | reference 改用不含 actor id 的格式 |
| R2-23 | Info | 使用量 ledger 的管理面與 R2-15～R2-16 屬同類：昂貴上游（AI、路線、供應商搜尋）主要靠登入後的配額防護，未登入面只有 IP 限流 | 維持現狀即可，部署時確認 `TRUST_PROXY_CLIENT_IP` 文件化的邊界（前次 API-11） |
| R2-24 | Info | `fx_rate_base_url` 只能由環境變數設定（不在後台可改欄位內），不在 `OFFICIAL_PROVIDER_HOSTS` 表內；無金鑰、風險僅限操作者自誤 | 若日後開放後台編輯，先加進允許表 |
| R2-25 | Info | 後台可設定的 AI model 名稱會插進請求路徑（host 已鎖官方），惡意值最多能改打同主機其他端點 | 可加 `^[A-Za-z0-9._:-]{1,128}$` 格式驗證作縱深 |
| R2-26 | Info | 前次 WEB-02 的嚴格 CSP 仍是 Report-Only（規劃如此）；`next.config.ts` 的強制政策不含 `script-src` | 依前次 §7 的時程轉為強制 |

## 4. 經查證不成立的項目（避免日後重複回報）

| 主張 | 為何不成立 |
|---|---|
| 「客戶端可自帶 `X-Request-ID` 進行 log injection」 | BFF 以 `^[A-Za-z0-9._:-]{1,128}$` 驗證後才轉發（`route.ts`），無 CRLF／控制字元空間；trace id 本可由客戶端起頭 |
| 「CSP nonce 取自客戶端可控的請求標頭」 | `proxy.ts` 對 `x-nonce` 與 `content-security-policy-report-only` 都是 `headers.set()`——覆寫、不是透傳 |
| 「BFF 把可偽造的 `X-Forwarded-For` 直接變成受信任的客戶端 IP」 | 取的是**最右**一段（`.at(-1)`，即最近一跳 proxy 所附加者），配合 README 已文件化的「edge proxy 必須剝除入站轉發標頭」邊界；與前次 API-11 相同屬部署前提，非程式缺陷 |
| 「公開分頁／ILIKE 搜尋可造成無上限掃描」 | hotspots／foods 的 `limit` 均有 `le=50`／`le=30` 上限、`q` 上限 100 字並經 `escape_like(escape="\\")`、cursor 上限 100 字；成本受表大小約束 |
| 「thumbnail URL 插進 CSS background-image 可注入」 | 該值經 `JSON.stringify` 包裹（引號與反斜線都被跳脫），無法逸出 `url("…")` 字串語境；任意 https 圖片本就在 CSP `img-src https:` 允許範圍 |
| 「`/srv` 權限」的世界可讀部分 | 僅 `/srv/travel-scanner` 目錄 0755 可 traverse 屬實（已修 R2-11）；其下 `releases/` 本來就是 0750，備份目錄亦然 |
| 「回滾後分析排程器被 `--remove-orphans` 移除」 | `--remove-orphans` 只移除 compose 檔**未定義**的服務；實際問題是從未被啟動（已修 R2-06） |

## 5. 回歸驗證結果（前次「已修」項目）

在現行 HEAD 逐項確認仍然成立：API-03／API-04（`OFFICIAL_PROVIDER_HOSTS` 並已涵蓋 Gemini、NAVITIME、Ekispert、ODsay）、API-05（`RequestBodyLimitMiddleware`）、API-06、API-07（新的 foods 搜尋亦用 `escape_like`）、WEB-01（BFF proxy 與 LINE webhook）、WEB-03、WEB-05（無 `latest`，lock 檔一致）、WEB-07、WEB-08、INF-01～INF-05。**發現回歸或旁路者**：API-01（OAuth 路徑，R2-02）、API-02（TTL 語義，R2-01）、WEB-01（OAuth callback 路由，R2-03）、WEB-06（新元件未套用，R2-09）、OPS-06（chgrp 競態，R2-12）。

## 6. 本輪未完整覆蓋的面向

自動化掃描中斷，以下面向只做了重點抽查，建議下一輪補齊：LINE webhook 簽章與 replay 細節、密鑰與設定加密全面複查、限流／DoS 全面盤點（R2-15／R2-16 是抽查所得）、使用量 ledger 併發競態、AI prompt injection 全面盤點（R2-05 是抽查所得）、回應欄位白名單全面盤點、分享／公開端點、hotspots 候選管線與 foods 深查、migrations 0034–0036、CI workflow 深查、git 歷史密鑰掃描、web 轉址／快取。已完成的抽查：`pip-audit` 與 `npm audit` 零已知漏洞；種子與工具檔無硬編碼密鑰跡象（未掃全歷史）。

## 7. 本次驗證

| 項目 | 指令 | 結果 |
|---|---|---|
| API lint／型別 | `uv run ruff check .`、`uv run mypy app` | 通過（170 檔，strict） |
| API 測試 | `uv run pytest` | 634 passed、28 skipped（新增 9 個測試；整合測試由 CI 的 Postgres／Redis 執行，含 R2-08 的新案例） |
| Web lint／型別／i18n | `npm run lint:web`、`npm run typecheck:web`、`npm run check:i18n` | 通過（5 語系 21 namespaces） |
| Web 單元測試 | `npm run test:web` | 通過（含 OAuth callback 上限的新測試） |
| 相依稽核 | `uv run pip-audit --local --skip-editable`、`npm audit --audit-level=low` | 均為 0 已知漏洞 |
| 主機腳本 | `bash -n ops/deployer/install.sh` | 通過（未於主機執行，見 R2-06／R2-11／R2-12 注意事項） |
