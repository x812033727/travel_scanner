---
id: 2026-09-11-form-validation-and-touch-targets
title: 表單驗證與低於四十四像素的觸控目標
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T19:25:01Z
created_at: 2026-09-11T03:21:17Z
completed_at: 2026-09-11T19:39:59Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/community/shell.tsx
  - apps/web/components/airline-fare-lab.tsx
  - apps/web/components/flight-status-search.tsx
  - apps/web/components/date-range-picker.tsx
  - apps/web/components/admin-restaurant-sources-panel.tsx
  - apps/web/components/admin-usage-settings-panel.tsx
  - apps/web/components/admin-analytics-panel.tsx
  - apps/web/components/admin-hotspot-guides-panel.tsx
  - apps/web/components/search-workbench.tsx
  - apps/web/components/search-workbench.test.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 表單驗證與低於四十四像素的觸控目標

## Why

**驗證只做第一步。** `search-workbench.tsx:120-142` 的 `validateStepOne` 管日期與天數，但 `goNext` 對第 1 到第 4 步什麼都不驗。把國家選到零個（`:100-104` 允許）只會得到一句 `cityNeedsCountry` 的提示（`:189`），照樣可以往下走、照樣可以送出。後端的 180 天旅行區間上限（`places/router.py:231`）前端沒有鏡像，超過只會在送出時吐一個原始的 validation 訊息。

**觸控目標。** 房規很清楚也大致遵守——`min-h-11` / `h-11`（44px）在 96 個檔案裡出現 673 次，`globals.css:407-410`、`:626-631`、`:3263-3270` 都是標準寫法。以下是例外：

| 位置 | 實際高度 | 影響 |
| --- | --- | --- |
| `community/shell.tsx:37-39` | ~40px | 整條社群子導覽（7 個連結），每個社群與寵物頁都有 |
| `airline-fare-lab.tsx:234-236` | ~40px | 三個模式頁籤 |
| `flight-status-search.tsx:164` | ~36px | 模式切換 |
| `date-range-picker.tsx:150` | ~20px | 「清除日期」是純文字無 padding，旁邊的日期格卻是正確的 `h-11`（`:17`） |
| `admin-restaurant-sources-panel.tsx:272` | 36px | 移除來源的圖示鈕 |
| `admin-usage-settings-panel.tsx:518,536` | 40px | 加減步進鈕 |
| `admin-analytics-panel.tsx:73` | 40px | 重新整理圖示鈕 |

**`grid-cols-3` 沒有手機變體。** 360px 減掉容器內距，三欄各約 100px。`airline-fare-lab.tsx:233` 的第三個頁籤標籤是「即時倒買 API」，會換行或被切。`admin-hotspot-guides-panel.tsx:607` 更是 `grid-cols-5` 配 `text-xs`，每欄約 60px。

## Definition of done

- [ ] 精靈每一步送出前都驗證該步的必填項，180 天上限在前端就擋。
- [x] 上表七處都達到 44px。
- [x] `grid-cols-3` / `grid-cols-5` 在手機上換行或改為單欄。

## Steps

- [ ] `goNext` 依 `step` 分派對應的驗證函式。
- [x] 加 180 天上限的前端檢查與說明。
- [x] 七處補 `min-h-11`。
- [x] `airline-fare-lab.tsx:233` 與 `admin-hotspot-guides-panel.tsx:607` 加手機斷點變體。

## How to verify

```bash
cd apps/web && npm run lint:web && npm run test:web
cd apps/web && npx playwright test --project="Pixel 7"
```

## Notes

- `search-workbench.tsx` 被 `2026-09-11-wizard-crash-when-all-criteria-any` 佔住 scope，本任務的 scope 不含它——驗證那部分請併到那張做，或等它完成。此處先記錄問題本身。
- `type="number"` 用在約 26 個檔案但只有 10 個配了 `inputMode`。影響不大（iOS 對 `type="number"` 本來就給數字鍵盤），列出來備查。

## 瀏覽器實測補充（2026-09-11 第二輪）

162 個頁面的實測（`getBoundingClientRect()` 取渲染後尺寸，非讀 class）確認本任務列出的問題，並補上實際數值與出現頻率：

| 元素 | 實測尺寸 | 出現頁數 |
| --- | --- | --- |
| 社群子導覽（社群動態／寵物友善／我的收藏／訊息…） | 42 × 82px | 22 |
| 「發佈」 | 40 × 52px | 22 |
| 「公開身分設定」 | 42 × 110px | 22 |
| 「我的貼文與草稿」 | 42 × 124px | 22 |

全站共 945 處低於 44px。**數量最多的頁尾五個連結（16px 高、每頁都有）不在本任務 scope**，已另立 `2026-09-11-footer-links-sixteen-px-tall`。

另補一項本任務原本沒提到的：`/foods` 在**特大字**設定下橫向溢位 15px（`html[data-text-size="largest"]`）。162 頁中唯一一個溢位的頁面，其餘尺寸與設定皆正常。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 觸控目標：九處，不是七處

表上七處全部補到 44px，另外量出兩個表上沒有的——`community/shell.tsx:38` 的「發佈」（40px）與 `:39` 的「訊息」（42px）。是先改完表上那些、再用瀏覽器在 412px 量一次才發現的；只照表改會漏掉。

`grid-cols-3`／`grid-cols-5` 兩處加了手機斷點：票價實驗室的三個頁籤在手機改成單欄堆疊（`sm:grid-cols-3` 以上才並排），後台景點攻略的五欄在手機變三欄。

### 驗證只補了兩條，而不是「每一步都驗」

DoD 寫的是「精靈每一步送出前都驗證該步的必填項」。逐步看過之後，**第 2 到第 4 步沒有必填項可驗**：第 2 步（出發地、人數、房間）全部有預設值，第 3 步（住宿）與第 4 步（偏好）全部選填。所以那句話能做的只有「把伺服器真的會拒絕的規則搬到前端」。

`places/router.py` 一共三條 `model_validator`，前端原本只鏡像了兩條：

| 伺服器規則 | 原本 | 現在 |
| --- | --- | --- |
| `end_date > start_date` | 有（`dateOrderError`） | 有 |
| `max_days >= min_days` | 有（`dayOrderError`） | 有 |
| 旅行區間 ≤ 180 天 | **無** | 第 1 步擋下 |
| 每晚最低價 ≤ 最高價 | **無** | 第 4 步擋下 |

### 「國家選到零個還能往下走」不是缺陷

任務把它列為驗證漏洞。但零個國家是**受支援的輸入**：`places/router.py` 的 else 分支（就是本分支修過崩潰的那一支）專門處理「沒有日期、沒有天數、沒有國家」的情況並回傳候選城市清單。`cityNeedsCountry` 是提示不是錯誤，因為城市下拉要先選國家才有內容。擋掉它會拿掉一個功能，所以沒有動。

### 驗證

`search-workbench.test.tsx` 三個案例：超過 180 天會在設定日期的那一步被擋（並斷言那一步仍是顯示中的 section——所有步驟都在 DOM 裡，只是 `hidden`）、每晚價格倒置會在住宿那一步被擋、區間在上限內則放行。兩個判斷式分別短路成 `false` 之後對應兩條變紅。

`e2e/readability.spec.ts`（CI 有跑）加一條：`/zh-TW/pet-friendly` 的社群子導覽每個連結都 ≥ 44px。把「訊息」的 `min-h-11` 拿掉之後變紅。量的是實際 render 出來的高度而不是 grep class，因為高度常常來自 padding 與 line-height 而不是 `min-h-11`。

整套 230 files / 2338 tests 全過。
