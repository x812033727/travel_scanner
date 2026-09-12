---
id: 2026-09-12-guides-admin-entry-unreachable
title: 情報攻略的後台入口沒登記在 API 導覽表，正式站打開 /admin/guides 是 forbidden
status: done
priority: P1
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-12T13:25:11Z
created_at: 2026-09-12T13:25:10Z
completed_at: 2026-09-12T14:01:51Z
branch: claude/article-publish-hide-settings-a87b8d
depends_on: []
scope:
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_admin_operations.py
  - tools/e2e-runtime-api.mjs
  - apps/web/e2e/admin-operations.spec.ts
  - apps/web/e2e/admin-operations-full-stack.spec.ts
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/components/admin-shell.tsx
---

# 情報攻略的後台入口沒登記在 API 導覽表，正式站打開 /admin/guides 是 forbidden

## Why

PR #398 把 `/admin/guides` 加進前端的 `fallbackAdminNavigation`（`apps/web/lib/admin-operations.ts:33`），
卻沒加進 API 的 `NAVIGATION_REGISTRY`（`apps/api/app/admin/operations_service.py:49`）。
`visibleAdminNavigation` 只要 API 回了導覽就不看 fallback，`app/[locale]/admin/layout.tsx:31` 再用
`canAccessAdminPath` 檢查，所以正式站的 `/admin/guides` 直接顯示「你沒有這個後台的權限」，側欄也沒有入口。
`admin-nav.tsx` 的文案表與 icon 表同樣沒有 `guides`。正式站因此有 19 個主題、0 篇文章。

## Definition of done

- [x] owner 與 content 角色的 bootstrap 導覽含 `/admin/guides`，側欄「內容」群組顯示「情報與攻略」並有 icon。
- [x] `test_admin_operations` 斷言 registry 含 `/admin/guides`；兩個 admin-operations e2e 的導覽常數與 fixture 同步。
- [x] 側欄標籤不在 TS 裡新增中文：缺席的鍵改查 `admin.navigation` 訊息目錄（五語系本來就有 `navigation.guides`）。

## Steps

- [x] `NAVIGATION_REGISTRY` 加 `guides`（content 群組第一項，無 badge）。
- [x] `admin-nav.tsx` / `admin-shell.tsx` 的 `label()` 退回 `admin.navigation.<key>`；icon 用 lucide `Newspaper`。
- [x] `tools/e2e-runtime-api.mjs`、`admin-operations.spec.ts`（`ADMIN_PAGES`、`ROLE_NAVIGATION.content`、
      `/admin/guides` 與 topics 的 fixture）、`admin-operations-full-stack.spec.ts` 同步。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_operations.py -q
npm run test:web -- admin-nav
cd apps/web && npx playwright test e2e/admin-operations.spec.ts --project=desktop-chromium
```

## Notes

- `guides_pending` 這個 badge 算的是 `HotspotGuide`（站外文章），不是 `guide_articles`，所以這個入口不掛 badge。
- 與 `2026-09-12-guides-visibility-and-admin-list` 同一分支、同一個 PR。
