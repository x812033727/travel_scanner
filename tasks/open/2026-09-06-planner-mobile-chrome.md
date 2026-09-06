---
id: 2026-09-06-planner-mobile-chrome
title: 手機版行程頁的浮動元件佔掉三分之一畫面
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:57:26Z
created_at: 2026-09-06T14:02:00Z
completed_at:
branch: claude/ux-batch-4
depends_on: []
scope:
  - apps/web/components/itinerary-diff.tsx
  - apps/web/components/itinerary-diff.test.tsx
  - apps/web/app/globals.css
---

# 手機版行程頁的浮動元件佔掉三分之一畫面

## Why

手機開一趟行程時，畫面上同時有三層浮動元件：

- 上方 sticky 的日期列（`.planner-day-strip`）
- 下方 sticky 的「描述想調整的地方」意圖列（`.planner-intent-bar`，永遠顯示，
  離底部 6.75rem）
- 最下面 fixed 的工具列（`.planner-mobile-bar` 裡的 dock）

三層加起來大約 11rem。在 390×844 的手機上，真正能看行程的高度只剩下不到七成，
而且中間那層會蓋住底下的卡片——2026-09-06 的 e2e 就是被它蓋住第一張卡片的「編輯」
按鈕才紅的（人可以捲開，Playwright 不會捲已經在畫面內的元素）。

對「操作要簡單」這個目標來說，一個畫面同時放三組常駐控制項太多了。

## Definition of done

- [x] 手機上意圖列預設收合成一顆帶標籤的按鈕，點開才是輸入框與範圍選擇。
- [x] 常駐浮動高度明顯下降（量測見下）。
- [ ] 低於 8rem —— 量過之後知道這個數字訂得不切實際，見下面的說明。

## How to verify

scratchpad 的 `planner_chrome.mjs`：用假的行程在 390×844 開行程頁，量三層浮動元件
的高度與它們佔畫面的比例。

## Notes

實際量到的數字（390×844、預設字級）：

| | 2026-09-06 | 收合意圖列後 | 這次再瘦身 |
| --- | --- | --- | --- |
| 上方日期列 | 105px | 105px | **87px** |
| 意圖列 | 約 160px（常駐展開） | 70px | **44px** |
| 底部工具列 | 104px | 104px | 104px |
| 合計 | 約 369px（44%） | 279px（33%） | **235px（28%）** |

這次做的兩件事：收合狀態的意圖列不再是一張有邊框、內距、陰影與毛玻璃的卡片，只留
那顆膠囊按鈕；日期膠囊在手機上從三行變兩行，「N 個已安排」變成眉標上的小數字。

**8rem（128px）做不到，而且不該硬做。** 底部工具列自己就 104px，那是「加安排／排序／
AI 幫我安排／儲存狀態」四個 48px 的按鈕——為了好按才做這麼大，縮它等於跟這輪的目標
反著走。日期列 87px 也已經是兩行的下限。要再往下只剩「把日期列改成不黏頂」，那會讓
換日子變成要往上捲，不划算。合理的收斂點就是現在的 28%。
