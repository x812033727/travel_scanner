---
id: 2026-09-08-food-platform-links
title: 七國美食卡精準導航與訂位平台
status: done
priority: P1
area: api
owner: codex
claimed_at: 2026-09-08T01:27:11Z
created_at: 2026-09-08T00:42:42Z
completed_at: 2026-09-08T01:34:53Z
branch: codex/food-platform-links
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/app/foods
  - apps/api/migrations/versions/0062_food_merchant_platform_links.py
  - apps/api/tests/test_food_platform_links.py
  - apps/api/tests/test_food_integration.py
  - apps/api/tests/test_schema.py
  - apps/web/components/food-dish-card.tsx
  - apps/web/components/food-dish-card.test.tsx
  - apps/web/components/food-merchant-card.tsx
  - apps/web/components/food-merchant-card.test.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/admin-food-merchants-panel.test.tsx
  - apps/web/lib/foods.ts
  - apps/web/lib/foods.test.ts
  - apps/web/messages
  - docs/food-platform-links.md
---

# 七國美食卡精準導航與訂位平台

## Why

旅客需要把精準導航與查看／訂位分開：前者沿用已驗證 Google Place ID 或韓國 Naver 地點，後者只在人工確認到特定分店頁時顯示各國平台按鈕。

## Definition of done

- [x] 七國店家都具有對應平台的查核結果，未驗證連結不公開。
- [x] 美食與店家小卡分開顯示精準導航及品牌化查看／訂位入口。
- [x] 後台可逐筆驗證、標記查無／模糊／停用並篩選查核狀態。
- [x] API、Web、migration 與 production build 驗證完成，PR #349 已建立。

## Steps

- [x] 建立 migration、模型、平台規則與 173 筆實際啟動資料的保守查核結果。
- [x] 串接公開 API、前台雙入口與五語系文案。
- [x] 串接管理 API、篩選與逐筆編輯介面。
- [x] 完成本機測試與品質檢查並建立 PR #349；CI 接續驗證。

## How to verify

- `pytest apps/api/tests/test_food_platform_links.py`
- `ruff check apps/api/app apps/api/tests`
- `mypy apps/api/app`
- `npm run lint:web && npm run typecheck:web`
- `npm run test:web -- --runInBand`
- `npm run build:web`

## Notes

- 訂位平台連結不是永久座標或店家來源證據。
- 韓國仍僅以 Naver 作導航；Catchtable Global 是獨立查看／訂位入口。
- 初始查核採保守發布：只有能確認特定分店頁者標記 verified；種子證據不足者保存 ambiguous，不假稱平台上不存在，並避免搜尋頁或錯誤分店公開。
- 主線實際 `MERCHANT_SEEDS` 為 173 筆；全部都有且僅有一筆對應國家平台的初始查核結果。
- 本機驗證：ruff、mypy（257 files）、API 其餘全套（1666 passed / 109 skipped）、Web 全套（133 files / 786 tests）、i18n、tools、typecheck、lint、production build 均通過。
- Windows 完整 API 收集會因既有 Unix-only `socketserver.UnixStreamServer` 失敗；排除該單一平台測試後其餘全套通過，Linux CI 負責補驗。
- Docker CLI 在本機不存在，PostgreSQL migration、容器與 full-stack smoke 由 CI 補驗。
