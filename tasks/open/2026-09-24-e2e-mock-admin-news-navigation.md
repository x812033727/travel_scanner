---
id: 2026-09-24-e2e-mock-admin-news-navigation
title: 離線 e2e 的假導覽表沒有 /admin/news，admin-operations.spec 從沒打開新聞後台
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-24T04:52:01Z
completed_at:
branch:
depends_on: []
scope:
  - tools/e2e-runtime-api.mjs
  - apps/web/e2e/admin-operations.spec.ts
  - apps/web/lib/admin-navigation-e2e-fixture.test.ts
---

# 離線 e2e 的假導覽表沒有 /admin/news，admin-operations.spec 從沒打開新聞後台

## Why

PR #694（2026-09-23 合併）新增 `/admin/news`，改了兩份導覽表：

- API 的 `NAVIGATION_REGISTRY`（`apps/api/app/admin/operations_service.py:61-64`）：排在 guides 後面，capability 是 `content.read`，badge 是 `news_review_pending`。
- 前端的 `fallbackAdminNavigation`（`apps/web/lib/admin-operations.ts:34`）。

e2e 這邊只有 full-stack spec 的兩份清單補上了 `/admin/news`（`apps/web/e2e/admin-operations-full-stack.spec.ts:4、:16`，可用 `git show 2142f228 -- apps/web/e2e/admin-operations-full-stack.spec.ts` 查看）。CI web job 用的離線那一套沒有跟上：

- `tools/e2e-runtime-api.mjs:83-107` 自己抄了一份導覽表，一共 21 列，沒有 news。`:131` 的 `pending` 也沒有 `news_review_pending`。把 mock 跑起來打 `/api/v1/admin/bootstrap`：owner 回 21 個 href、content 回 11 個、viewer 回 19 個，都沒有 `/admin/news`。
- `apps/web/e2e/admin-operations.spec.ts:4-26` 的 `ADMIN_PAGES`，和 `:31` 的 `ROLE_NAVIGATION.content`，都沒有 `/admin/news`。

這造成兩個結果：

1. CI web job 跑的是 `admin-operations.spec.ts`（`.github/workflows/ci.yml:121`），但它從沒打開過 `/admin/news`。會走到這頁的只有 full-stack-smoke（`ci.yml:322`，full-stack spec `:97-104` 的 owner 迴圈）。離線 spec 對每頁做的檢查，新聞後台一項都沒套到：沒有 pageerror、沒有第一方 4xx、沒有站外請求、沒有寫入、不溢出。
2. 在離線 mock 底下，連 owner 打開 `/zh-TW/admin/news` 都會看到「你沒有這個後台的權限」。原因是 layout 會拿 bootstrap 回來的導覽跑 `canAccessAdminPath`（`apps/web/app/[locale]/admin/layout.tsx:31`、`lib/admin-operations.ts:160-167`），mock 沒這一列就判成 forbidden。

手抄的導覽表這是第二次漂移。第一次是 2026-09-12 的 `/admin/guides`（`tasks/done/2026-09-12-guides-admin-entry-unreachable.md`），那次漏的是 API registry，結果正式站 forbidden。這次漏的是 e2e mock。所以這張票也要補一道自動檢查。

### 為什麼只補導覽清單不夠

mock 那一列和 `ADMIN_PAGES` 要一起改：只改一邊，`:244` 和 `:275` 的導覽 `toEqual` 就會紅。

但兩邊都改了、卻沒補 API fixture 時，CI **不會**紅，頁面卻是壞的：

- spec 的 `page.route("**/api/travel/**")` 遇到沒列的路徑會回 `pageResult()`（`:79-81`、`:220-221`），也就是 `{ items: [], total: 0, page: 1, limit: 20, pages: 1 }`。
- `apps/web/components/admin-news-workspace.tsx:101-104` 同時打四支 API。`:121-124` 的 `useMemo` 不管在哪個分頁、每次 render 都會跑 `candidates?.candidates.filter(...)`，拿到 pageResult 就丟 `TypeError: Cannot read properties of undefined (reading 'filter')`。
- 補了 candidates 的 fixture 之後，還有三處會依序壞掉：sources 分頁 `:240` 的 `sources.map`、settings 分頁 `:255` 的 `settings.gates[vertical]`，以及 stats 缺欄位時 `:195` 會印出 `Pipeline runs: undefined`。
- 這個 TypeError 會被 `apps/web/app/[locale]/admin/error.tsx` 接住。它換上自己的 h1「這個後台頁面載入失敗」，但 admin layout 的側欄照樣在。
- 錯誤被明確的 error boundary 接住時，Next 只做 `console.error`（`node_modules/next/dist/client/react-client-callbacks/error-boundary-callbacks.js` 的 `onCaughtError`），不會觸發 Playwright 的 `pageerror`。
- owner 迴圈只檢查三件事：有任何 h1（`:249`）、側欄在（`:251`）、`pageErrors` 是空的（`:259`）。三項都會過。換句話說，只照抄導覽清單，矩陣會綠著放過一個整頁出錯的新聞後台。

所以 fixture 一定要補，而且要有一個只有新聞工作區真的畫出來才會成立的斷言。

fixture 要加在 spec 的 `isolateAdmin`，不是加在 mock API。workspace 是 client component，打的是 `/api/travel/...`（`lib/api.ts:161`），這些請求在瀏覽器端就被 `page.route` 攔下來了，到不了 mock。mock 對未知路徑回的是 404（`tools/e2e-runtime-api.mjs:345-346`）。

2026-09-24 在 main `692dcf5a` 核對過 #694 之後的變化：

- #703（`827c74bd`）在 `SettingsView` 加了 `model_options` 和 `default_models`（`apps/api/app/news_automation/schemas.py:179-185`）。前端型別（`lib/admin-news.ts:34-46`）裡這兩個是 optional，但 fixture 照 API 的完整形狀給。
- `CandidatePage` 仍是 `{candidates, total, page, pages}`（`schemas.py:245-249`），`StatsView` 在 `:333-341`。
- 路由在 `router.py:40`（sources）、`:84`（settings）、`:97`（candidates）、`:163`（stats）。
- #708、#713 沒有動到 workspace、mock 或這兩支 spec。

## Definition of done

- [ ] 離線 mock 回給 owner、viewer、content 的 bootstrap 導覽都含 `/admin/news`，位置跟真的 registry 一樣（guides 之後、hotspots 之前）；`pending` 帶 `news_review_pending`。
- [ ] `admin-operations.spec.ts` 的 owner 矩陣會打開 `/zh-TW/admin/news`，而且：
  - 回 200，h1 是「AI 每小時自動新聞」；
  - 看得到資料載入後才會出現的「Pipeline runs: 0」；
  - 沒有「這個後台頁面載入失敗」標題；
  - 沒有 pageerror、第一方 4xx、站外請求、寫入，桌機寬度也不溢出。
- [ ] `/zh-TW/admin/news?tab=settings` 畫得出三張 gate 卡片（「AI · 啟用門檻」等），`?tab=sources` 畫得出「新增來源」，兩頁都沒有「這個後台頁面載入失敗」。
- [ ] 反向：暫時拿掉 candidates fixture，owner 矩陣會紅，不會綠著放過錯誤面板。
- [ ] 角色矩陣：content 和 viewer 看得到 `/admin/news`；support、operations、database_operator、deployer 看不到。
- [ ] 以後 `fallbackAdminNavigation` 多一列而 mock 沒跟上時，`npm run test:web` 會紅，而且訊息裡直接列出缺的 href。

## Steps

- [ ] `tools/e2e-runtime-api.mjs`：在 `:85` 的 guides 列後面加 `["news", "content", "/admin/news", "content.read", "news_review_pending"]`。`:131` 的 `pending` 補上 `news_review_pending: 0`。側欄只在數字大於 0 時才畫 badge（`components/admin-nav.tsx:121-123`），所以不會多出 badge，`readability.spec.ts` 量的東西也不會變。
- [ ] `apps/web/e2e/admin-operations.spec.ts`：在 `ADMIN_PAGES` 的 `"/admin/guides"` 後面插入 `"/admin/news"`，`ROLE_NAVIGATION.content` 在同樣位置插入。viewer 和 owner 是從 `ADMIN_PAGES` 推出來的，不用改。
- [ ] 在 `isolateAdmin` 的 GET 分支加四個 fixture，放在 `:212-215` 的 guides fixture 旁邊。形狀照 `apps/api/app/news_automation/schemas.py`：
  - `/admin/news/candidates`：回 `{ candidates: [], total: 0, page: 1, pages: 1 }`。route 用 `url.pathname` 比對，`?limit=100` 不影響。
  - `/admin/news/sources`：回 `[]`。
  - `/admin/news/settings`：回完整的 SettingsView。可以直接照抄 `apps/web/components/admin-news-workspace.test.tsx:32-52` 的 `settings`，裡面有 ai、tech、crypto 三個 `gates`，以及 `model_options`、`default_models`、`updated_at`。
  - `/admin/news/stats`：回 `{ pending_review: 0, failed: 0, published: 0, queue_by_status: {}, pipeline_runs: 0, pipeline_failures: 0, input_tokens: 0, output_tokens: 0 }`。
- [ ] 在 owner 迴圈裡替 `/admin/news` 加專屬斷言：
  1. heading「AI 每小時自動新聞」可見；
  2. 文字「Pipeline runs: 0」可見，只有 stats 載入而且 render 沒丟錯時才會出現；
  3. 然後斷言「這個後台頁面載入失敗」heading `toHaveCount(0)`。
- [ ] 迴圈結束後，另外打開 `/zh-TW/admin/news?tab=settings` 和 `?tab=sources`：
  - 先等「Pipeline runs: 0」出現；
  - 再斷言 settings 看得到「AI · 啟用門檻」或「儲存設定」，sources 看得到「新增來源」（字串見 `lib/admin-news-copy.ts:28-31`）；
  - 錯誤標題數量為 0。
  - 不要把帶 `?tab=` 的網址加進 `ADMIN_PAGES`，那份清單要跟導覽的 href 逐一相等。
- [ ] 評估要不要把「錯誤標題為 0」的斷言放進整個 owner 迴圈，讓每一頁都檢查。先在本機跑一次：如果其他頁面在 fixture 底下也掉進錯誤面板，這張票只保留 `/admin/news` 的斷言，那些頁面另開一張票列出來，不要順手擴大 scope。
- [ ] 新增 `apps/web/lib/admin-navigation-e2e-fixture.test.ts`，做法照 `apps/web/lib/usage-catalog-e2e-fixture.test.ts`：
  - 讀 `tools/e2e-runtime-api.mjs` 的原始碼，抽出 `adminNavigation` 每一列的 href；
  - 跟 `fallbackAdminNavigation`（`lib/admin-operations.ts:31`）的 href 做集合比對，不比順序，因為兩邊本來就不是同一個順序；
  - 失敗訊息要列出缺了哪些 href。

## How to verify

```bash
node --check tools/e2e-runtime-api.mjs
npm run test:web -- admin-navigation-e2e-fixture
npm run build:web
cd apps/web && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/admin-operations.spec.ts e2e/admin-domains.spec.ts e2e/readability.spec.ts
```

- 跑 Playwright 之前，先確定 127.0.0.1:8000 上沒有別的服務。`playwright.config.ts` 啟動 mock 時用了 `reuseExistingServer: true`，本機 API 如果開著，Playwright 會拿它來代替 mock，跑出來的結果就不算數。
- 不要加 `--project`。CI 兩個 project 都會跑，`admin-domains` 和 `readability` 的手機版也用同一份 mock 畫側欄。
- 預期 `bootstrap registry drives every owner page without first-party failures` 和 `role bootstrap filters navigation and direct URLs fail closed` 都通過，`admin-domains` 和 `readability` 也維持綠燈。

反向驗證，改完後各做一次再還原：

- 刪掉 mock 的 news 列：drift guard 要紅並列出 `/admin/news`，owner 矩陣也要紅。
- 刪掉 candidates fixture：owner 矩陣要紅在 `/admin/news` 的專屬斷言上。如果只做了「有 h1、沒 pageerror」的舊寫法，這裡會綠著通過。

直接看 mock 回什麼（用 18765 port，不跟 8000 衝突）：

```bash
E2E_API_PORT=18765 node tools/e2e-runtime-api.mjs & pid=$!
curl -s --retry 10 --retry-connrefused --retry-delay 1 -H "Authorization: Bearer e2e-content" \
  http://127.0.0.1:18765/api/v1/admin/bootstrap | grep -o '"/admin/news"'
kill $pid
```

改之前這段什麼都印不出來，改完要印出 `"/admin/news"`。

## Notes

- 來源：2026-09-23 修 PR #694 的 full-stack-smoke 時發現。當時只改了 full-stack spec 的兩份清單，mock 和離線 spec 都沒跟上。2026-09-24 在 main `692dcf5a` 重驗，問題還在，mock 也實際跑過。
- 先例：`tasks/done/2026-09-12-guides-admin-entry-unreachable.md` 是 `/admin/guides` 的同一組修法。drift guard 的先例是 `apps/web/lib/usage-catalog-e2e-fixture.test.ts`。
- 既有盲點，不只新聞頁有：owner 迴圈的「有 h1」「側欄在」「沒有 pageerror」三項，任何頁面掉進 `app/[locale]/admin/error.tsx` 都照樣會過。full-stack spec 因為另外收了 `consoleErrors`（`admin-operations-full-stack.spec.ts:107`）才看得到這種錯。處理方式見 Steps 倒數第二項。
- `tasks/open/2026-09-24-keep-every-news-review-item-reachable` 會改 workspace 的 candidates 請求，改成多個 status 加分頁。route 只比對 pathname，所以這裡的 fixture 照樣能用；但如果那張票改了回傳形狀（例如加 facets），這裡的 fixture 要一起改。兩張票的 scope 不重疊。
- `tasks/open/2026-09-09-site-experience-settings` 還沒人認領，但它的 scope 也列了 `tools/e2e-runtime-api.mjs` 和 `apps/web/e2e/admin-operations.spec.ts`。如果它先被認領，這張票的 claim 會被拒絕。那張票看起來已經由 #380（`30a8e06a`）合併，只是一直沒結案，總整理時可以順便確認。
- 不在這張票的範圍：API registry（Python）和前端 fallback（TS）之間的一致性。`apps/api/tests/test_admin_operations.py:36-38` 已經釘住 news 列和它的 badge。如果想一次防住三份清單，drift guard 可以用同樣的方法讀 `apps/api/app/admin/operations_service.py` 裡的 `href="..."`，只動新的測試檔，不用擴大 scope。
