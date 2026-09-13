# Mokaair 資安複查（2026-09-13）

- 檢查基準：`main` commit `2bfd427`
- 分支：`claude/security-check-o5zaj1`
- 範圍：`apps/api`（FastAPI、RQ worker、`deployment_agent`）、`apps/web`（Next.js BFF 與前端）、
  `ops/`、Docker／Compose、GitHub Actions、相依套件、追蹤中的檔案內容
- 方法：唯讀原始碼審閱＋`npm audit`／`pip-audit`＋密鑰掃描。**沒有**滲透測試，也沒有存取任何線上主機。
- 前次基準：[`security-audit-2026-09.md`](security-audit-2026-09.md)（2026-09-03，commit `4c61b14`）

## 1. 結論

**沒有找到新的可利用漏洞。** 這次複查重跑了上一份稽核的攻擊面，並針對當時之後才長出來的功能
（社群私訊與影片、寵物友善、探索流、景點介紹、旅宿 clickout、AdSense、`database_admin`、
細分管理員角色）重看了一遍，沒有發現新的權限繞過、注入、IDOR 或密鑰外洩。

上一份稽核列為「已修」的項目抽查都還在原位；列為「建議」的項目裡，**風險最高的兩項已經做完**：

| 前次編號 | 項目 | 現況 |
| --- | --- | --- |
| 建議 #1 | `main` 的 branch protection | **已完成**。`.github/BRANCH_PROTECTION.md` 記錄 2026-09-06 設定：四個 CI job 為必要檢查、`strict` 開啟、對管理員生效。 |
| API-10／建議 #2 | 管理員升權需二次驗證 | **已完成**。`PATCH /admin/users/{id}/roles` 走 `require_admin_step_up(..., "users.roles")`；永久停權與抹除也各有自己的 step-up scope。 |
| WEB-11／建議 #5 | 後台頁面伺服器端門檻 | **已完成**。`app/[locale]/admin/layout.tsx` 在伺服器端 `loadAdminBootstrap()`，未登入 `redirect` 到登入頁，非管理員回 `forbidden`，再以 `canAccessAdminPath` 逐頁比對能力。 |

同時整套 RBAC 從「是不是管理員」升級成七個角色、十八種能力，`_admin_path_capability` 對沒有列出的
`/admin/*` 路徑一律落到 `roles.manage`（只有 owner 能過），是 fail-closed 的正確方向。

剩下的都是上一份稽核已經知道、當時決定延後的縱深防禦項目。這次把它們逐條回去確認現況，
並依照 `AGENTS.md` 的規矩立成六張任務卡（見 §4），不是留在對話紀錄裡。

## 2. 這次實際驗證過的項目

以下每一項都回到原始碼逐行確認，不是引用上一份稽核的結論。

**認證與工作階段**
- Argon2（`pwdlib`）雜湊；登入時帳號不存在也比對 `DUMMY_PASSWORD_HASH`，時間側通道一致。
- JWT 要求 `sub/ver/iss/aud/jti/iat/nbf/exp` 全部存在，`aud`／`iss` 都驗；`auth_version` 讓改密碼、
  重設密碼、刪帳號立刻讓所有既有 token 失效。
- 續期把原本的 `jti` 帶著走，所以一次登入只有一個撤銷把手；`revoke_access_token` 的 TTL 取
  `max(exp, session_started_at + 絕對上限)`，複製出去的 cookie 沒辦法自己續成一條登出摸不到的鏈。
- Redis 不通時 `ensure_token_not_revoked` 回 503（fail-closed），不是放行。
- 絕對上限在「出示 token」時就檢查，不是只在續期時檢查。

**帳號復原**
- 重設／驗證／刪除信的 token 是 `secrets.token_urlsafe(32)`，資料庫只存 SHA-256，30 分鐘到期、
  一次性、綁 `auth_version`。
- 連結用 fragment（`#token=`）帶 token，不會進伺服器日誌或 `Referer`。
- `forgot-password` 對存在、不存在、已停用的帳號回應完全一致；per-IP 10/hr 與 per-email 3/hr 雙重限流。

**授權**
- 掃過全部 108 個 `/admin/*` 變更端點，每一個都掛著 `AdminUser`、`require_capability(...)` 或
  等效的 dependency，沒有只靠 `CurrentUser` 的。
- `owned_trip()`、`visible_profile()`、社群 `member()` 都是 owner-scoped 查詢，沒有找到 IDOR。
- 分享連結 token 只存 SHA-256、可撤銷，fork 出來的副本不帶原作者的 `notes` 與價格快照。

**輸入與輸出**
- 沒有任何字串拼接的 SQL；全部走 SQLAlchemy 參數化。
- `dangerouslySetInnerHTML` 只有三處：JSON-LD（`<` 逸出成 `<`）與兩個帶 nonce 的 bootstrap script。
- 站台內容與景點介紹是結構化 block union，不是儲存 HTML；連結走共用的 `contentBlockLink` 白名單
  （只收 `https:`／`http:`／格式正確的 `mailto:`，拒絕帶帳密的 URL），圖片只收自家 `/guides/...` 路徑。
- 上傳圖片先進 quarantine、重新 raster 成 WebP（剝掉 EXIF／XMP／ICC）、擋 decompression bomb 與多幀，
  presign 的 `content-length-range` 上界綁在 schema 的 10 MB。

**信任邊界**
- nginx `proxy_set_header X-Travel-Client-IP ""` 先清掉外部偽造值，`X-Forwarded-For $remote_addr` 是覆寫而非附加。
- BFF 一律新建 `Headers` 物件，只放白名單 header；取 `x-forwarded-for` 最右側那筆。
- API 端 `forwarded_client_ip` 要同時滿足 `TRUST_PROXY_CLIENT_IP`、`X-Travel-Proxy-Token` 相符、
  值是合法 IP，三者缺一就回 `None`。
- BFF 路徑段拒絕 `.`／`..`／分隔符並逐段 `encodeURIComponent`；變更方法要求同源 `Origin`（缺少即拒絕）；
  上游轉址只允許 HTTPS 或同源 HTTP。
- 部署 agent 走 unix socket，HMAC 涵蓋 timestamp／nonce／method／path／body 摘要，±60 秒時間窗，
  nonce 一次性；部署本身另外要求管理員重新輸入密碼＋確認字串＋CI 綠燈＋SHA 相符。
- LINE webhook 以 `hmac.compare_digest` 驗簽。

**基礎設施**
- `npm audit`（root 與 `apps/web`）與 `uv run pip-audit`：**0 個已知漏洞**。
- 全樹掃 AWS key／OpenAI key／GitHub PAT／PEM 私鑰樣式：**0 筆**。
- 正式 compose 只綁 loopback（`127.0.0.1:8090`、`127.0.0.1:8091`），non-root、`cap_drop: ALL`、
  `no-new-privileges: true`。
- 生產啟動時 `validate_deployment_security()` 會擋掉：預設或過短的 `APP_SECRET_KEY`、
  與它相同的 `SETTINGS_ENCRYPTION_KEY`、`COOKIE_SECURE=false`、非 HTTPS origin、預設資料庫密碼、
  無密碼 Redis、指向非官方主機的供應商 base URL。
- workflow 沒有 `pull_request_target`，也沒有把 `github.event.*` 的自由文字插進 `run:`。

## 3. 仍然開著的項目

全部來自上一份稽核的建議清單，這次確認都還在，沒有一項是新的。

| 前次編號 | 項目 | 現況 | 任務 |
| --- | --- | --- | --- |
| WEB-02／建議 #3 | 嚴格 CSP 仍是 `Report-Only`；實際強制的只有 baseline 四個指令，`script-src` 沒有被強制 | 未處理 | [`2026-09-13-csp-report-only-never-enforced`](../tasks/open/2026-09-13-csp-report-only-never-enforced.md) |
| WEB-12 | HSTS 沒有 `includeSubDomains` | 未處理 | 併入上一張 |
| INF-08／建議 #6 | Actions 以可變 tag 釘住；沒有 Dependabot／Renovate | 未處理 | [`2026-09-13-pin-actions-and-dependency-updates`](../tasks/open/2026-09-13-pin-actions-and-dependency-updates.md) |
| INF-06／API-11／建議 #4 | 正式 compose 沒有網路分段、沒有 `read_only`、`api` 與 `web` 沒有 healthcheck | 未處理 | [`2026-09-13-prod-compose-network-segmentation`](../tasks/open/2026-09-13-prod-compose-network-segmentation.md) |
| API-16／建議 #9 | 分析用 hash 借用 `APP_SECRET_KEY`，輪替簽章金鑰會同時打斷訪客統計 | 未處理 | [`2026-09-13-analytics-hash-key-separation`](../tasks/open/2026-09-13-analytics-hash-key-separation.md) |
| API-12／建議 #8 | 密碼政策只有長度 10–128 | 未處理 | [`2026-09-13-password-policy-length-only`](../tasks/open/2026-09-13-password-policy-length-only.md) |
| 建議 #11 | ruff 沒有啟用 `S`（flake8-bandit） | 未處理 | [`2026-09-13-ruff-flake8-bandit`](../tasks/open/2026-09-13-ruff-flake8-bandit.md) |
| INF-07／建議 #6 | API image 仍是單階段，`pip`／`uv`／原始碼都留在正式 image | 未處理 | 未立案（影響有限，見下） |
| API-18／建議 #10 | `GET /providers/status` 未登入即可讀取供應商配置清單 | 未處理 | 未立案 |
| WEB-10／建議 #10 | OAuth flow cookie 仍是未簽章的 base64 JSON | 未處理 | 未立案 |
| API-14／建議 #10 | 航班 clickout 的 303 只驗 `https` 與非空 host，沒有 host allowlist | 未處理 | 未立案 |
| WEB-04 | `GET /{locale}/out/guides/{id}` 會觸發消耗會員配額的上游 POST | 前次已「接受」 | 不立案 |

後四項沒有立案，是因為上一份稽核已經把它們評為 Low／Info 且理由仍然成立：`/providers/status`
只回傳「哪些供應商有設定」的布林值不含金鑰；OAuth flow cookie 的 state 與瀏覽器綁定仍在 Redis
端驗證，cookie 本身被竄改不會通過；航班 clickout 的目標來自供應商回應而非使用者輸入。
要立案隨時可以，但排在上面六張之後。

## 4. 建議的處理順序

1. **CSP 轉強制**（P1）。這是目前唯一一個「其他都做好了、只差最後一步」的項目：nonce 管線已經
   鋪好，嚴格政策已經在每個訪客的瀏覽器裡被評估，只是結論被丟掉。需要先在正式環境蒐集一輪
   violation 證據，不能直接翻旗標。
2. **Actions 釘 SHA＋Dependabot**（P2）。CI runner 在通往正式環境的路徑上（部署要求 CI 綠燈）。
3. **正式 compose 網路分段**（P2）。目前 `INTERNAL_PROXY_TOKEN` 一個人扛著「同一座 bridge 上誰都
   連得到 API」這件事。
4. **分析 hash 金鑰分離**（P2）。讓 `APP_SECRET_KEY` 可以在需要時單獨輪替，不必連帶弄髒統計。
5. **密碼政策**與 **ruff `S`**（P3）。兩張都便宜，而且 ruff 那張是永久性的，之後每個 commit 都受益。

## 5. 無法從 repo 驗證的項目

沿用上一份稽核的清單，這次一樣沒有存取權：正式主機上 `/etc/travel-scanner/*.env` 的實際權限、
反向代理是否真的送出 HSTS、Google Maps 與 NAVER 瀏覽器金鑰是否已在雲端主控台限制 referrer、
部署 agent 的 GitHub PAT 實際範圍、`DEPLOYMENTS_ENABLED` 目前的值。另外這次新增一項：
**嚴格 CSP 在正式環境的 violation 實況**，那是 §4 第 1 項能不能動的前提。

## 6. 本次執行的檢查

| 項目 | 指令 | 結果 |
| --- | --- | --- |
| Node 相依稽核 | `npm audit --omit=dev`、`cd apps/web && npm audit` | 0 vulnerabilities |
| Python 相依稽核 | `cd apps/api && uv run pip-audit` | No known vulnerabilities found |
| 密鑰掃描 | AWS／OpenAI／GitHub PAT／PEM 樣式全樹比對 | 0 筆 |
| 任務檔驗證 | `npm run check:tasks` | Validated 380 task file(s) |

這次沒有修改任何應用程式或設定檔，所以沒有跑 lint／型別／測試；六張任務卡各自寫了該跑的指令。
