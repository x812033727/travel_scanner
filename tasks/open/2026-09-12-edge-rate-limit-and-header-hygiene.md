---
id: 2026-09-12-edge-rate-limit-and-header-hygiene
title: 邊緣層沒有限流，轉送標頭也沒有人剝
status: review
priority: P1
area: ops
owner: claude-opus-5
claimed_at: 2026-09-12T01:05:32Z
created_at: 2026-09-12T01:05:22Z
completed_at:
branch: claude/prevent-web-scraping-6xj3dg
depends_on: []
scope:
  - ops/nginx
  - .github/workflows/ci.yml
  - docker-compose.prod.yml
  - .env.example
  - apps/api/app/config.py
  - apps/api/app/infra.py
  - apps/api/app/travel_services/router.py
  - apps/api/tests/test_public_read_rate_limit.py
  - apps/api/tests/test_travel_services.py
  - apps/web/lib/client-address.ts
  - apps/web/lib/client-address.test.ts
  - apps/web/lib/public-server-fetch.ts
  - apps/web/lib/public-server-fetch.test.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/auth/oauth/_shared.ts
  - apps/web/app/[locale]/out/guides/[guideId]/route.ts
  - docs/anti-scraping.md
---

# 邊緣層沒有限流，轉送標頭也沒有人剝

## Why

`2026-09-11-public-read-rate-limit` 在 API 加了每來源的公開讀取上限，但它的正確性**完全建立在
一件目前沒人保證的事情上**：打到 API 的 `X-Travel-Client-IP` 真的是訪客的位址。

- 正式環境的 nginx（`nginx/1.28.3`）在 repo 外，沒有版本控管、沒有 `limit_req`、沒有連線數上限。
  這就是 `docs/security-audit-2026-09.md` 的 **INF-10**。
- 同一份審計「§6 無法從 repo 驗證的項目」第 3 點明確問到：要不要**把外部送進來的
  `X-Travel-Client-IP` 與 `X-Forwarded-For` 剝掉再自行設定**。沒剝掉的話，呼叫端可以自己挑
  要落在哪個限流桶（**API-11**）。
- 應用層限流只在拒絕時省下工作，請求本身還是吃掉一個 worker。讓大量請求變便宜的是邊緣層。

**另外查到一個現成的 bug**：`apps/api/app/travel_services/router.py` 的 131、625、731、860、893
行直接讀原始標頭，繞過 `forwarded_client_ip()`，於是繞過 `TRUST_PROXY_CLIENT_IP` 閘門。那五個
限流在**每一個環境**都相信任何人送來的位址，連 `TRUST_PROXY_CLIENT_IP=false` 也一樣；而且沒有
IP 格式驗證，任何字串都會變成 Redis key 的一部分，呼叫端可以無限量開出 `rate:` key。

## Definition of done

- [x] 偽造的 `X-Travel-Client-IP` 無法決定自己落在哪個限流桶。
- [x] 邊緣層有每來源的請求與連線上限，而且**沒有誤傷靜態資源**與搜尋引擎。
- [x] `travel_services` 那五處改走 `client_ip()`，回到 `TRUST_PROXY_CLIENT_IP` 閘門之內。
- [x] 參考設定有辦法不腐爛（CI 語法檢查），而且照著套用不會弄掉 www 的 301。

## Steps

- [x] 修 `travel_services/router.py` 五處直接讀取，改用 `client_ip(request)`。
- [x] `internal_proxy_token`：`config.py` 新設定、`infra.py` 比對（`hmac.compare_digest`）、
      compose 同時給 api 與 web、web 四個產生點經由 `lib/client-address.ts` 的共用 helper 帶上。
      **空字串＝維持現狀**，避免只設一邊造成全部訪客塌進同一個桶。
- [x] `ops/nginx/`：README、冪等 install.sh、`10-rate-limit.conf`、`proxy-headers.conf`、
      `mokaair.conf.example`、`ci-validate.conf`。
- [x] CI `containers` job 加一步 `nginx -t`。
- [x] 測試與文件。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
npm run test:web && npm run test:tools && npm run check:tasks && npm run build:web
docker run --rm -v "$PWD/ops/nginx:/etc/nginx/ops:ro" nginx:1.28-alpine \
  nginx -t -c /etc/nginx/ops/ci-validate.conf
```

主機上的驗收見 `ops/nginx/README.md`。**真正的驗收條件是那個 Redis key 檢查**：送一個偽造的
`X-Travel-Client-IP`，然後確認它沒有開出對應的 `rate:` key。那是唯一能證明「每來源計數不能被
繞過」的東西。

## 本次驗證

- API：ruff、mypy、`pytest` 3269 passed / 203 skipped。
- Web：lint、check:i18n、typecheck、`vitest` 2305 passed、test:tools、build。
- nginx 設定：**這個環境沒有 nginx 也沒有 docker daemon，跑不了 `nginx -t`**，所以改用
  crossplane 的 strict 解析（會驗指令名稱與所在 context）：`ci-validate.conf` 連同兩份
  snippet 三個檔案全數 `status: ok`；`mokaair.conf.example` 包成 http 區塊後也是 `ok`。
  唯一的 error 是 crossplane 不認得 `http2 on;`——它的指令表早於 nginx 1.25.1，而正式環境
  是 1.28.3，所以那是假警報，已在設定裡註明舊版要改用 `listen 443 ssl http2;`。
  **權威的檢查是 CI 那一步的真 `nginx -t`。**
- `install.sh` 過 `bash -n`，未在真實主機執行過。
- `docker compose -f docker-compose.prod.yml config` 通過，並確認 `api` 與 `web` 兩個服務
  都拿到 `INTERNAL_PROXY_TOKEN`。
- 那五處限流的回歸測試**確認會失敗**：把其中一處改回讀原始標頭，
  `test_public_rate_limits_never_read_the_forwarded_address_directly` 立刻紅。

## Notes

- **scope 與 `2026-09-11-public-read-rate-limit` 重疊，是用 `--force` 認領的。** 那張是同一個
  owner（claude-opus-5）、同一條 branch（`claude/prevent-web-scraping-6xj3dg`）的前一階段，
  不是別人的工作。board 上會同時看到兩張活著的 task 指向同一批檔案，原因就是這個。
- **前面沒有 CDN。** `tasks/done/2026-09-06-social-login-launch-prep.md:75` 記錄實際 curl 到的
  Server 標頭是 `nginx/1.28.3`；若有 Cloudflare 會是 `Server: cloudflare`。
  `ANALYTICS_COUNTRY_HEADER` 在 `.env.example` 與正式 compose 都是空的。所以 `$remote_addr`
  就是訪客，realip 模組不必要而且開了會出錯——但那段要留成註解，之後真加了 CDN 有跡可循。
- **L3 分不出 web 容器和旁邊另一個容器。** 兩份 compose 都沒有宣告 `networks:`，全部落在預設
  bridge 上拿動態 IP，重啟就變；而「整個 compose 子網」正好就是威脅集合本身。所以 CIDR 允許
  清單是裝飾，共享金鑰才是唯一真的移動了邊界的作法。
- **不要把金鑰設成生產環境必填**（`validate_api_serving_security()`）。還沒設這個變數的主機
  會在下次部署直接起不來。要變必填是另一張 task，等線上確認兩邊都生效之後再說。
- **不要改兩份 security audit。** 它們是有基準 commit 的歷史快照（`4c61b14` / `5c2d26e`），
  第二輪是用「回歸驗證」章節記錄前一輪項目的現況，從來不回頭編輯前一份。INF-10 與 API-11
  維持原樣，處置寫在這裡與 `docs/anti-scraping.md`。
- nginx 的兩個繼承陷阱：`proxy_set_header` 與 `add_header` 只有在當前層級**一個都沒定義**時
  才從上層繼承。任何 location 自己寫了一行，server 層級那幾行就全部消失——所以走 `include`。
- 照著套用最容易弄壞的三件事：www → apex 的 301（沒有它 OAuth 會永遠 `oauth_state_invalid`，
  見 `docs/social-login.md:40-61`）、`/api/line/webhook`（LINE 會突發重送）、
  `/.well-known/apple-developer-domain-association.txt`（由 Next 從 `public/` 供應）。
