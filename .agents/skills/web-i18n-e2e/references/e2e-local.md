# 在本機跑 Playwright e2e

## `apps/web/playwright.config.ts` 做了什麼

- `testDir: "./e2e"`，所以指令都在 `apps/web` 底下跑，spec 路徑寫 `e2e/<name>.spec.ts`。
- 兩個 project：`desktop-chromium`（Desktop Chrome）與 `mobile-chromium`（Pixel 7）。不加 `--project` 就兩個都跑，CI 也是兩個都跑。
- 沒有設 `retries`，所以 `trace: "on-first-retry"` 平常不會留 trace。要 trace 就加 `--trace=retain-on-failure`（`food-map-reservations.yml` 就是這樣跑）。
- `webServer` 起兩個行程：
  1. 假 API：`node ../../tools/e2e-runtime-api.mjs`，聽 `127.0.0.1:8000`，等 `/api/v1/runtime/site-visibility` 回應才開始。它的 `reuseExistingServer` 永遠是 true。
  2. Next：預設 `npm run dev -- --port <port>`；`PLAYWRIGHT_SERVE_BUILD=true` 時改 `npm run start -- --port <port>`（`next start --keepAliveTimeout 65000`，要先 build）。`API_INTERNAL_URL` 預設指到 `http://127.0.0.1:8000`，也就是假 API。

| 環境變數 | 作用 |
| --- | --- |
| `PLAYWRIGHT_PORT` | Next 的 port，預設 3000 |
| `PLAYWRIGHT_BASE_URL` | 測試打的網址，預設 `http://127.0.0.1:<port>` |
| `PLAYWRIGHT_SERVE_BUILD=true` | 跑 build 好的版本（CI 的做法）而不是 dev server |
| `PLAYWRIGHT_REUSE_EXISTING=true` | **不起假 API**，Next 也沿用已經在跑的那個。只給 full-stack spec 對真的 API 用 |
| `API_INTERNAL_URL` | Next 伺服器端要打的 API |
| `E2E_API_PORT` | 只有單獨起假 API 時有用；config 等的網址寫死 8000，改了 Playwright 會等不到 |

## 跑法

```bash
cd apps/web
npx playwright install chromium                       # 第一次，或瀏覽器版本對不上時
npx playwright test e2e/navigation.spec.ts --project=desktop-chromium
npx playwright test e2e/navigation.spec.ts -g "search criteria can be revised"
npx playwright test e2e/site-pages.spec.ts --trace=retain-on-failure
npx playwright show-trace test-results/<資料夾>/trace.zip
npx playwright test --list e2e/admin-operations.spec.ts   # 只列出案例，不跑
```

從 repo 根目錄：`npm run test:e2e --workspace @travel-scanner/web -- e2e/navigation.spec.ts`。

CI 的跑法（build 後服務 build，冷編譯不會吃掉 30 秒逾時）：

```bash
npm run build:web
cd apps/web && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/admin-operations.spec.ts
```

PowerShell 設環境變數的寫法是 `$env:PLAYWRIGHT_SERVE_BUILD = "true"; npx playwright test ...`。Windows 開發環境的其他細節在 skill `dev-and-ci`。

跑之前：

- **確定 8000 port 上沒有別的東西**。本機 API 開著的話，Playwright 會直接拿它當假 API（`reuseExistingServer: true`），跑出來的結果不算數。
- dev server 模式第一次開每一頁都要編譯；本機第一輪逾時，先用 `PLAYWRIGHT_SERVE_BUILD=true` 重跑再下結論。
- 懷疑 flake 時用 `--repeat-each=20 --project=desktop-chromium -g "<案例>"` 重複跑，不要只重跑一次。
- dev server 模式會把 `apps/web/next-env.d.ts` 的 import 改成 `./.next/dev/types/...`。跑完 `git checkout -- apps/web/next-env.d.ts`，不要把它 commit 進去（它也會讓之後的 rebase 卡住）。
- 沒有自己 `node_modules` 的 git worktree（靠上層目錄解析套件），`--list` 可以跑，但 dev server 起不來（`.next/dev/.../build-manifest.json` ENOENT、等 webServer 逾時）。要真的跑 e2e，在那個 worktree 裡 `npm ci`。

## 哪些 spec 在 CI 跑

CI 是**逐一列出** spec 檔，新 spec 沒加進清單就永遠不會在 CI 跑。

| workflow（job） | spec |
| --- | --- |
| `.github/workflows/ci.yml`（`web`，用假 API） | navigation、readability、signed-out、travel-services、stay22-allez、stay22-script、guides-adsense、stay22-maps、merchant-styles、admin-domains、admin-operations、site-experience、site-pages、discovery-card-details、planner-premium、korea-dual-maps、seo |
| `ci.yml`（`full-stack-smoke`，真的 API＋Postgres＋Redis） | full-stack、community（`COMMUNITY_E2E=1`）、admin-domains-full-stack（`ADMIN_DOMAIN_E2E=1`）、admin-operations-full-stack（`ADMIN_OPERATIONS_E2E=1`），都 `PLAYWRIGHT_REUSE_EXISTING=true` |
| `.github/workflows/planner-premium.yml` | planner-route-tones、planner-calm、planner-premium、trip-stay-areas、stay22-maps |
| `.github/workflows/travel-discovery.yml` | discovery、frontend-flow、discovery-card-details、discovery-full-stack、frontend-flow-full-stack |
| `.github/workflows/food-map-reservations.yml` | food-map-reservations、food-reservation-platforms、merchant-styles 的其中一條 |

2026-09-25 沒有任何 workflow 在跑的：admin-analytics、admin-hotspot-ai-search、claude-code-series、csp、deployments、flight-status、gemini-series、hotspot-guides、hotspot-review-editor。改到它們涵蓋的頁面時要自己在本機跑。新增 spec 時把它加進對的 workflow（`ci.yml` 的 `web` job 是四個必要檢查之一），那是 CI 檔的改動，要在票的 scope 裡。

full-stack spec 開頭有 `test.skip(process.env.X !== "1", ...)`，本機沒起完整堆疊時會顯示 skipped，不是通過。

## 資料從哪裡來：兩層 mock

| 請求 | 誰發 | 怎麼 mock |
| --- | --- | --- |
| 伺服器端 render（layout、`generateMetadata`、server component、admin bootstrap） | Next 伺服器直接打 `API_INTERNAL_URL` | `tools/e2e-runtime-api.mjs`。`page.route` **攔不到** |
| 瀏覽器端的 `/api/travel/**`（同源 BFF） | 瀏覽器 | spec 裡的 `page.route("**/api/travel/**", ...)`。沒攔到的會經 BFF 打到假 API，未知路徑回 404 |
| service worker 發的 fetch | worker | `page.route`／`context.route`／`setOffline` 都攔不到（`tasks/done/2026-09-11-offline-today-e2e.md`） |

`tools/e2e-runtime-api.mjs` 的規矩：

- 未知路徑回 404，而 `admin-operations.spec.ts` 會數第一方 4xx、`korea-dual-maps.spec.ts` 會數 console error。伺服器端 render 新增了一支 API 呼叫，就要在這裡補一個回應，否則別的 spec 會紅。
- 它手抄了好幾份正式資料的形狀（用量操作清單、後台導覽表、角色 capability）。**正式那一份多一列、這裡沒跟上，就是漂移**：`apps/web/lib/usage-catalog-e2e-fixture.test.ts` 是防漂移測試的範本；後台導覽表還沒有這種測試，缺 `/admin/news` 的事見票 `2026-09-24-e2e-mock-admin-news-navigation`。
- 只放明顯是假的資料（`example.test` 信箱、`Synthetic ...` 標題），不放正式站的真實內容或個資。
- 不需要啟動整個 Playwright 就能看它回什麼：`E2E_API_PORT=18765 node tools/e2e-runtime-api.mjs`，再 `curl -H "Authorization: Bearer e2e-content" http://127.0.0.1:18765/api/v1/admin/bootstrap`。

## 登入與後台 spec

登入狀態是**伺服器端**看 cookie 決定的：locale layout 沒看到 `travel_access` cookie 就畫登出的 header，mock `/auth/me` 沒用。

- 一般登入：`apps/web/e2e/session.ts` 的 `pretendSignedIn(page)`，加上 `travel_access=e2e-session`（domain `127.0.0.1`）。
- 後台：`apps/web/lib/admin-bootstrap.server.ts` 把 cookie 值當 `Bearer` 打 `/api/v1/admin/bootstrap`。假 API 的 `adminBootstrap`：`e2e-session` 是 owner，`e2e-<role>` 是那個角色（`viewer`、`support`、`content`、`operations`、`database_operator`、`deployer`），其他值回 401。導覽與 capability 由它決定，後台 layout 用 `canAccessAdminPath` 擋直接輸入網址，mock 導覽裡沒有的頁面會顯示沒有權限。
- 角色矩陣的寫法看 `apps/web/e2e/admin-operations.spec.ts` 的 `isolateAdmin(page, role)`：設 cookie、`page.route` 攔 `/api/travel/**`、記錄所有寫入、收集站外請求與第一方 4xx。
- full-stack 後台 spec 是真的在 `/zh-TW/login` 填帳密；帳號由 CI 用 `app.cli create-admin` 建。本機沒有那個堆疊就別跑它們。

後台頁掉進 `app/[locale]/admin/error.tsx` 時，Next 只 `console.error`、不觸發 `pageerror`，側欄與 h1 都還在。只斷言「有 h1、側欄在、沒有 pageerror」的矩陣會綠著放過整頁出錯；新頁面要加一個只有資料真的畫出來才成立的斷言，並斷言錯誤標題數量為 0。

新增後台頁的登記（API 的 `NAVIGATION_REGISTRY`、前端 fallback、權限）不在這個 skill，見 skill `backend-conventions`；這裡只負責 e2e 的假導覽表與 spec 清單跟上。
