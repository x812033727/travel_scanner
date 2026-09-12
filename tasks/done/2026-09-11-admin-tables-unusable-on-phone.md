---
id: 2026-09-11-admin-tables-unusable-on-phone
title: 後台九張表格在手機無法閱讀
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T18:02:50Z
created_at: 2026-09-11T03:21:00Z
completed_at: 2026-09-11T18:25:01Z
branch: claude/mokaair-website-access-k7xiku
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
  - apps/web/components/admin-responsive-tables.test.ts
  - apps/web/e2e/admin-operations.spec.ts
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

- [x] 九張表格在 360px 寬都能讀，每個值旁邊都有欄名。
- [x] 不需要橫向捲動就能看完一列。

## Steps

- [x] 五張補 `data-label`：照抄 `AdminDataTable` 的使用者做法（`admin-audit-panel.tsx:103`、`admin-users-panel.tsx:833-906`、`admin-database-panel.tsx:109-110`），欄名直接取自 `thead` 的文字。
- [x] 四張改用 `AdminDataTable`，或至少加上 `admin-responsive-table` class 並補 `data-label`。
- [x] 優先做 `admin-hotspots-panel`（1,769 筆熱點待審，是最常用的）與 `admin-deployments-panel`（部署狀態常在手機上看）。
- [x] 加一個 e2e 斷言：Pixel 7 尺寸下後台頁面無橫向溢位（`e2e/navigation.spec.ts:64` 已有同類斷言可照抄）。

## How to verify

```bash
cd apps/web && npm run test:web -- admin
cd apps/web && npx playwright test --project="Pixel 7"
```

手動：手機開 `/zh-TW/admin/hotspots`、`/zh-TW/admin/deployments`，每列應該看得出哪個數字是哪一欄。

## Notes

- `playwright.config.ts:32-33` 已經對 Desktop Chrome 與 Pixel 7 兩個裝置跑所有 spec，加斷言不需要新的設定。
- 圖表那一塊處理得很好，不要動：`globals.css:67-96` 給 `.analytics-dashboard` 加了 `overflow-x: hidden; contain: inline-size`，並讓隱藏的 `table.sr-only` 不會撐寬版面，每張圖也都有 `sr-only` 的表格等價物（`admin-analytics-panel.tsx:40,82,88`）。

## claim 用了 --force，理由寫在這裡（claude-opus-5, 2026-09-11）

三張任務的 scope 擋著，三張都查過：工作已經合併進 main，遠端分支都已不存在（`git ls-remote --heads origin <branch>` 全部沒有回傳），只是任務檔沒標 `done`。

| 擋著的任務 | claim 時間 | 已合併的證據 |
| --- | --- | --- |
| `2026-09-09-configurable-catalog-review-run-call-limit` | 09-09 15:54（逾 50 小時） | `app/catalog_review/budget.py` 的 `run_call_limit` 已在 main |
| `2026-09-10-complete-hotspot-review-identity-and-rationale` | 09-10 05:34（逾 36 小時） | `1aefd59 fix(admin): 完整景點審核身分與理由編輯 (#385)` |
| `2026-09-11-food-reservation-platforms` | 09-11 06:29（約 11.5 小時，未達 24 小時門檻） | `19a9429 feat(foods): 獨立儲存訂位平台與多平台支援 (#392)`，正是最後一次動到 `admin-food-merchants-panel.tsx` 的 commit |

第三張還沒到 24 小時，但沒有進行中的工作需要被保護：分支已刪、改動已在 main。而這次的改動只是往 `<td>` 加 `data-label` 屬性，不動任何邏輯。

沒有去改它們的任務檔。

## 完成紀錄（claude-opus-5, 2026-09-11）

十一張表格（任務列了九張，做的時候發現 `admin-settings-panel` 有兩張，`admin-food-taxonomy-panel` 也是兩張）現在在手機上都是卡片式，每個值旁邊都有欄名。

- **五張補 `data-label`**：hotspots(9)、foods(6)、food-merchants(8)、food-taxonomy 兩張(7+6)。欄名直接取自同一張表 `thead` 的運算式，所以翻譯不會分岔。
- **四張補上 `admin-responsive-table` 再補 `data-label`**：merchant-coordinate-queue(4)、hotspot-places(6)、deployments(6)、settings 兩張(4+3)。class 一加上去，`min-width: 0 !important` 就把 `min-w-[820px]`～`[1100px]` 全部中和掉了。

### 兩個做的時候才發現的

1. **`admin-settings-panel` 的兩張表每列以 `<th>` 開頭**（月份是列標題），所以第一版的欄名整排往左偏一格：`used` 被標成「月份」。寫了一支驗證腳本逐列比對「欄名序列 vs `thead`」才抓到，修好後十一張全部對齊。
2. **`admin-merchant-coordinate-queue` 的欄名是寫死的繁中**（「選取」「店家」「Google 找到」「訊號」），整個面板都沒有 i18n。沒有順手翻譯（超出這張的範圍），但把四個字串抽成一個 `COLUMNS` 常數，讓 `<th>` 和 `data-label` 共用——否則等於把同樣的漢字再寫一次，`check:i18n` 的漢字增量守門會擋下來。這個面板的 i18n 另外建檔。

### 驗證

**`admin-responsive-tables.test.ts`（新檔）**：直接讀原始碼，掃出所有掛著 `admin-responsive-table` 的表，斷言每個非 `colSpan` 的 `<td>` 都有 `data-label`。不用 render 是因為這些面板要 session、API stub 和篩選狀態才走得到表格，而要守的規則本來就是 markup 的靜態性質。另外有一條「至少要找到 8 個檔案」的守門，避免掃描器壞掉之後靜悄悄地通過。拿掉一個 `data-label` 確認會紅。

**`e2e/admin-operations.spec.ts` 加一條 Pixel 7 案例**，走 hotspots／foods／deployments／settings 四頁。這條測試我改了三次才有用：

| 版本 | 為什麼不算數 |
| --- | --- |
| 量 `document.scrollWidth - clientWidth` | 外層的 `overflow-x-auto` 會把 980px 的表格藏起來，量不到——這正是這些表格當初能出貨的原因 |
| 改量每張 `<table>` 的寬度，但導頁後立刻量 | 四頁都還停在「載入工作區…」，`table` 數量是 0，等於什麼都沒量到 |
| 等 `networkidle` | 這些工作區在網路靜下來之後才畫出表格，還是 0 |

最後的版本：等 `table` 出現（有上限、等不到也不失敗，因為 deployments 與 settings 在 fixture 下沒有資料列），並加一條 `tablesReached > 0` 的守門確保整輪真的量到東西。把 hotspots 的 `admin-responsive-table` 拿掉之後：

```
Error: /admin/hotspots has a table wider than a Pixel 7
```

復原後通過。整套 `npm run test:web` 229 files / 2324 tests 全過。
