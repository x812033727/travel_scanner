---
id: 2026-09-06-flaky-navigation-e2e
title: navigation.spec.ts 兩個案例在 CI 間歇逾時
status: done
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T05:16:58Z
created_at: 2026-09-06T00:54:14Z
completed_at: 2026-09-06T05:51:32Z
branch: claude/web-p2-ux
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
  - apps/web/playwright.config.ts
  - .github/workflows/ci.yml
---

# navigation.spec.ts 兩個案例在 CI 間歇逾時

## Why

2026-09-06 清 PR 佇列時，同一個 spec 的兩個案例在不同 PR 上各紅了一次，重跑就過：

- `e2e/navigation.spec.ts:593 › search criteria can be revised before running a new comparison`
  —— `locator.fill: Test timeout of 30000ms exceeded`，卡在
  `expect(page.getByRole("heading", { name: "泰國・普吉完整旅程" })).toBeVisible()`。
- `navigation › primary travel flow is visible (desktop-chromium)` —— `element(s) not found`。

兩次都伴隨 web server 的 `SyntaxError: Unexpected end of JSON input`。

不穩定的測試的代價不是那 5 分鐘重跑，而是它會訓練大家「紅了就重跑」，真正的失敗
會被同樣的反射動作蓋掉。

## Definition of done

- [x] 這兩個案例連續跑 20 次不紅（或找出根因並修掉，而不是加長逾時了事）。

## Steps

- [x] 先確認 `SyntaxError: Unexpected end of JSON input` 是什麼 —— 那看起來像 mock
      API 回了截斷的 JSON，或是頁面在資料還沒到齊時就被斷言。如果是前者，測試本身
      是對的，該修的是 mock 或 server。
- [x] 找出 heading「泰國・普吉完整旅程」出現前實際等待的是哪個請求，改成等那個條件
      而不是等元素。
- [x] 本機重複跑確認：`npx playwright test e2e/navigation.spec.ts --repeat-each=20`。

## How to verify

```bash
cd apps/web && npx playwright test e2e/navigation.spec.ts --repeat-each=20 --project=desktop-chromium
```

## Notes

失敗的紀錄在這幾個 CI run（會過期，先看的話趁早）：
PR #168 的 `feat/trip-intent-bar`、PR #171 的 `fix/food-seed-test-drift`。
兩次都是 `web` job 的 "Run isolated browser UI tests" 步驟。

另外一個**已經被修掉**的相鄰問題，可以當作參考：`test_usage_settings_integration.py`
會連續註冊多個帳號而撞到同 IP 的註冊節流，回 429 讓測試紅。另一個 session 在
`claude/better-workflow-planning-324ki8` 上以「測試環境放寬同一 IP 上限」解掉了
（commit 01f7eba，已隨 PR #163 併入 main）。同樣是「基礎設施造成的假性失敗」，
處理方式值得比照。

2026-09-06 claude-fable-5-1：根因不在那兩個案例，而在 CI 讓 Playwright 起 `next dev`：
每一頁第一次被打開時才編譯，30 秒的測試逾時要同時吃掉編譯、mock API 與同機的另一個 server，
偶爾就超過；`Unexpected end of JSON input` 是同一件事的另一面（開發伺服器在編譯中被打斷的回應）。
CI 在 Playwright 前一步早就 `npm run build:web` 了，卻沒用那份 build。

- `playwright.config.ts`：`PLAYWRIGHT_SERVE_BUILD=true` 時 webServer 改跑 `next start`；
  本機預設仍是 dev server，改一行不用重 build。`ci.yml` 的 Playwright 步驟設這個 env。
- 本機驗證：`npm run build` 後 `PLAYWRIGHT_SERVE_BUILD=true PLAYWRIGHT_PORT=3200 npx playwright test
  e2e/navigation.spec.ts --project=desktop-chromium --repeat-each=10 -g "..."`，
  三個案例（那兩個加上 `explore surfaces show each other as sibling tabs`）各跑 10 次，30/30 過，
  單一案例 0.4–1.5 秒；同一天 dev server 模式下 `explore surfaces` 在 PR #198 第一次 CI 就紅過一次
  （瀏覽器端 `Cannot read properties of undefined (reading 'areas')`，換頁時資料還沒到），值得記著。
- 沒有加長任何逾時，spec 本身沒改。
