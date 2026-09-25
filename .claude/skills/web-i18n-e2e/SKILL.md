---
name: web-i18n-e2e
description: apps/web 的多語系文案與本機 Playwright e2e：在五個語系、25 個 namespace 的 messages 加鍵或加 namespace，npm run check:i18n 擋什麼（鍵與 ICU 參數要跟 en 一致、重複鍵、可編輯 namespace 白名單、新增的中文要進目錄）與每種紅法的修法，後台文案覆寫怎麼疊在目錄上；playwright.config.ts 的桌機與手機兩個 project、PLAYWRIGHT_SERVE_BUILD、tools/e2e-runtime-api.mjs 假 API、跑單一 spec、後台 spec 怎麼登入，以及從結案 flake 票學到的寫法。不管整條 CI 分診、Windows 環境與 Dependabot（dev-and-ci）、後台頁登記（backend-conventions）、文章翻譯（article-localization、content-pipeline）。要加或改介面文字、check:i18n 紅了、寫或跑 e2e、測試時紅時綠時，先讀這個 skill。Add UI copy across the five locales, fix check:i18n failures, and write and run Playwright specs locally without flakes.
metadata:
  short-description: 介面文案多語系與本機 Playwright e2e
---

# 介面文案與 e2e（web-i18n-e2e）

> 本文提到的 `references/…`、`scripts/…` 都在 `.agents/skills/web-i18n-e2e/` 底下；`.claude/skills/web-i18n-e2e/` 只放這份 SKILL.md 的逐字複本。

這個 skill 只放流程、指令與去哪裡讀。規則的來源是程式本身：`tools/check-i18n.mjs`、`tools/json-duplicate-keys.mjs`、`apps/web/playwright.config.ts`、`tools/e2e-runtime-api.mjs`，後台文案覆寫的規格在 `docs/ui-text-overrides.md`。指令都從 repo 根目錄或 `apps/web` 跑，照每段寫的。

## 不變的規矩

1. **`en` 是基準**。每個語系的每個 namespace，攤平後的鍵集合與每個鍵的 `{參數}` 集合都要跟 `en` 一樣。參數名不翻譯；plural 分支用 `#` 開頭。
2. **新的顯示文字一律進目錄**。在 `apps/web/{app,components,lib}` 的 `.ts/.tsx` 裡寫中文（連註解）會被 check:i18n 擋；本機只有 `git add` 之後才會檢查這一項。
3. **加 namespace 有七處要改**，其中 `apps/web/i18n/request.ts` 與 `apps/web/vitest.setup.tsx` 漏了沒有任何檢查會抓（`references/i18n.md`）。
4. **改鍵名或改參數會讓站主在後台的覆寫變孤兒**。PR 說明要寫出來。
5. **e2e 伺服器端的資料來自假 API，瀏覽器端的來自 `page.route`**，兩邊不互通；伺服器端新增一支 API 呼叫就要在 `tools/e2e-runtime-api.mjs` 補回應。
6. **新 spec 要加進 workflow 的清單**，CI 是逐一列出 spec 檔的。
7. **flake 要找成因**：不放寬斷言、不加長逾時、不 skip、不加 retry（`references/flake-lessons.md`）。

## 主幹 A：改介面文字

| # | 做什麼 | 關卡 |
| --- | --- | --- |
| 1 | 找到文字屬於哪個 namespace（`grep -rn "既有的某句" apps/web/messages/zh-TW`）；功能若已用 `apps/web/lib/<feature>-messages/` 就跟著它 | 知道要改哪五個檔 |
| 2 | 五個語系同位置加鍵：先 `en`，再 `zh-TW`，再 `ja`、`ko`、`zh-CN` | 參數名與集合一致 |
| 3 | 元件用 `useTranslations`／`getTranslations` 取；元件測試斷言 zh-TW 的句子 | 元件裡沒有新的中文字面字串 |
| 4 | `git add` 後跑 `npm run check:i18n` | 印出 `Validated 5 locales across 25 namespaces.` |
| 5 | 紅了照 `references/check-i18n.md` 的表修；缺哪些鍵用 `i18n-diff.mjs` 列 | 全綠 |
| 6 | `npm run lint:web && npm run typecheck:web && npm run test:web` | 全綠 |

## 主幹 B：寫或跑 e2e

| # | 做什麼 | 關卡 |
| --- | --- | --- |
| 1 | 確定 127.0.0.1:8000 上沒有本機 API 在跑 | 否則 Playwright 會拿它當假 API |
| 2 | 找最像的既有 spec 當範本；登入用 `pretendSignedIn`，後台角色用 `admin-operations.spec.ts` 的 `isolateAdmin` 寫法 | 知道資料從哪一層來 |
| 3 | 瀏覽器端請求用 `page.route("**/api/travel/**")` 攔；伺服器端要的資料補進 `tools/e2e-runtime-api.mjs` | 沒有第一方 404、沒有 console error |
| 4 | 用 `waitForResponse`、web-first 斷言等條件；加一個「資料真的畫出來才成立」的斷言 | 沒有 `waitForTimeout` |
| 5 | 本機跑兩個 project，再用 `--repeat-each` 壓一下 | 連續綠 |
| 6 | 反向驗證：拿掉關鍵 fixture 或修正，測試要紅 | 紅在預期的斷言上 |
| 7 | 把 spec 加進對的 workflow 清單（在票的 scope 裡） | CI 真的會跑它 |

## 指令

```bash
# i18n
npm run check:i18n
node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs            # 列出每個缺的／多的鍵與參數差異
node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs trips foods
node --test tools/json-duplicate-keys.test.mjs                   # 重複鍵掃描器自己的測試

# 元件測試
cd apps/web && npx vitest run components/route-mode-panel.test.tsx
npm run test:web -- usage-catalog-e2e-fixture

# e2e（在 apps/web）
npx playwright install chromium
npx playwright test e2e/navigation.spec.ts --project=desktop-chromium -g "search criteria"
npx playwright test e2e/site-pages.spec.ts --trace=retain-on-failure
npx playwright test e2e/navigation.spec.ts --repeat-each=20 --project=desktop-chromium
# CI 的方式：先 build 再服務 build
npm run build:web
cd apps/web && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/admin-operations.spec.ts
# 單獨起假 API 看它回什麼
E2E_API_PORT=18765 node tools/e2e-runtime-api.mjs
```

## 規則在哪裡（不重抄）

| 問題 | 讀 |
| --- | --- |
| 目錄結構、加鍵與加 namespace 的七處、`lib/*-messages` 這種第二種目錄、覆寫怎麼疊上去 | `.agents/skills/web-i18n-e2e/references/i18n.md` |
| check:i18n 的六項檢查、每個錯誤訊息的原因與修法、漢字檢查何時才跑 | `.agents/skills/web-i18n-e2e/references/check-i18n.md` |
| playwright.config 的 project 與環境變數、跑法、哪些 spec 在哪個 workflow、兩層 mock、登入與後台角色 | `.agents/skills/web-i18n-e2e/references/e2e-local.md` |
| Playwright 與 Vitest 的 flake 教訓（等哪個回應、disposed body、冷編譯、keep-alive、passive effect 空檔、探針） | `.agents/skills/web-i18n-e2e/references/flake-lessons.md` |
| 後台文案覆寫的 API、驗證、快取、編輯器 | `docs/ui-text-overrides.md` |
| passive effect 空檔的完整調查 | `tasks/done/2026-09-11-modal-escape-flake-under-load.md` |
| 整條 CI 的紅燈分診、Windows 開發環境、Dependabot | skill `dev-and-ci` |
| 新後台頁的登記（registry、權限、導覽） | skill `backend-conventions` |
| 開票、認領、PR 與合併 | skill `task-board` |

## 這個 skill 的檔案

- `references/i18n.md`、`references/check-i18n.md`、`references/e2e-local.md`、`references/flake-lessons.md`：見上表。
- `scripts/i18n-diff.mjs`：唯讀，列出每個語系相對 `en` 缺的鍵、多的鍵、參數不同的鍵；不需要 npm 套件。
- `.claude/skills/web-i18n-e2e/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
