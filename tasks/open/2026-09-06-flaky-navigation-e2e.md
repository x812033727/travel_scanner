---
id: 2026-09-06-flaky-navigation-e2e
title: navigation.spec.ts 兩個案例在 CI 間歇逾時
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:54:14Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
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

- [ ] 這兩個案例連續跑 20 次不紅（或找出根因並修掉，而不是加長逾時了事）。

## Steps

- [ ] 先確認 `SyntaxError: Unexpected end of JSON input` 是什麼 —— 那看起來像 mock
      API 回了截斷的 JSON，或是頁面在資料還沒到齊時就被斷言。如果是前者，測試本身
      是對的，該修的是 mock 或 server。
- [ ] 找出 heading「泰國・普吉完整旅程」出現前實際等待的是哪個請求，改成等那個條件
      而不是等元素。
- [ ] 本機重複跑確認：`npx playwright test e2e/navigation.spec.ts --repeat-each=20`。

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
