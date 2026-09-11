---
id: 2026-09-11-admin-tables-unusable-on-phone
title: 後台九張表格在手機無法閱讀
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-foods-panel.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/admin-food-taxonomy-panel.tsx
  - apps/web/components/admin-merchant-coordinate-queue.tsx
  - apps/web/components/admin-hotspot-places-panel.tsx
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-settings-panel.tsx
---

# 後台九張表格在手機無法閱讀

## Why

站主每天用手機看後台。有九張表格在手機上不可用，分成兩種病因。

**五張套了卡片化樣式卻沒給欄名。** `globals.css:1011-1031` 的 `.admin-responsive-table` 在 `<768px` 把每個 `<td>` 變成兩欄 grid，左欄的內容來自 `td::before { content: attr(data-label) }`，同時 `:996` 把 `thead` 整個隱藏。這五張表套了 class 但 `<td>` 上**一個 `data-label` 都沒有**，於是每一列變成一疊右對齊的數值，左邊留著約 93px 的空白，完全沒有欄名可以對照：

| 檔案 | `<td>` 數 | 有 `data-label` 的 |
| --- | --- | --- |
| `admin-hotspots-panel.tsx:945` | 9 | 0 |
| `admin-foods-panel.tsx:343` | 6 | 0 |
| `admin-food-merchants-panel.tsx:929` | 8 | 0 |
| `admin-food-taxonomy-panel.tsx:285` | 部分 | 0 |
| `admin-food-taxonomy-panel.tsx:598` | 部分 | 0 |

**四張根本沒套卡片化。** 有 `overflow-x-auto` 包著所以不會撐破版面，但在 360px 螢幕上等於要橫向捲過三倍寬，而且沒有 sticky header——捲到第三欄就失去對照：

- `admin-merchant-coordinate-queue.tsx:193` — `min-w-[960px]`
- `admin-hotspot-places-panel.tsx:135` — `min-w-[980px]`
- `admin-deployments-panel.tsx:146` — `min-w-[820px]`，6 欄
- `admin-settings-panel.tsx:489` — `min-w-[42rem]`（672px）

## Definition of done

- [ ] 九張表格在 360px 寬都能讀，每個值旁邊都有欄名。
- [ ] 不需要橫向捲動就能看完一列。

## Steps

- [ ] 五張補 `data-label`：照抄 `AdminDataTable` 的使用者做法（`admin-audit-panel.tsx:103`、`admin-users-panel.tsx:833-906`、`admin-database-panel.tsx:109-110`），欄名直接取自 `thead` 的文字。
- [ ] 四張改用 `AdminDataTable`，或至少加上 `admin-responsive-table` class 並補 `data-label`。
- [ ] 優先做 `admin-hotspots-panel`（1,769 筆熱點待審，是最常用的）與 `admin-deployments-panel`（部署狀態常在手機上看）。
- [ ] 加一個 e2e 斷言：Pixel 7 尺寸下後台頁面無橫向溢位（`e2e/navigation.spec.ts:64` 已有同類斷言可照抄）。

## How to verify

```bash
cd apps/web && npm run test:web -- admin
cd apps/web && npx playwright test --project="Pixel 7"
```

手動：手機開 `/zh-TW/admin/hotspots`、`/zh-TW/admin/deployments`，每列應該看得出哪個數字是哪一欄。

## Notes

- `playwright.config.ts:32-33` 已經對 Desktop Chrome 與 Pixel 7 兩個裝置跑所有 spec，加斷言不需要新的設定。
- 圖表那一塊處理得很好，不要動：`globals.css:67-96` 給 `.analytics-dashboard` 加了 `overflow-x: hidden; contain: inline-size`，並讓隱藏的 `table.sr-only` 不會撐寬版面，每張圖也都有 `sr-only` 的表格等價物（`admin-analytics-panel.tsx:40,82,88`）。
