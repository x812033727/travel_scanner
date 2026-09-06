---
id: 2026-09-06-planner-mobile-chrome
title: 手機版行程頁的浮動元件佔掉三分之一畫面
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T14:02:00Z
completed_at:
branch:
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

- [ ] 手機上行程頁的常駐浮動高度砍到一層（工具列）加一個可展開的入口。
- [ ] 意圖列在手機上預設收合成一顆帶標籤的按鈕，點開才是輸入框與範圍選擇。
- [ ] 桌機維持現狀。

## Steps

- [ ] `itinerary-diff.tsx`：手機斷點下把意圖列收成一顆按鈕，展開後是同一張表單。
- [ ] `globals.css`：`--planner-dock-clearance` 隨收合狀態調整，`.planner-app-shell`
      的底部保留區跟著縮小。
- [ ] 補上 `itinerary-diff.test.tsx` 的收合／展開案例。

## How to verify

`cd apps/web && npx playwright test e2e/navigation.spec.ts --project=mobile-chromium`
應該不需要先把卡片捲到畫面中間就能點到「編輯」；量一下 390×844 下常駐浮動元件的
總高度應該低於 8rem。

## Notes

- 2026-09-06 先在 e2e 裡把那次點擊改成「先捲到畫面中間再點」，並讓
  `.planner-app-shell` 的底部保留區從 10rem 改成跟 `--planner-dock-clearance` 綁
  在一起（12.75rem）。那是止血，不是這張任務要的結果。
