---
id: 2026-09-06-planner-mobile-chrome
title: 手機版行程頁的浮動元件佔掉三分之一畫面
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T19:00:31Z
created_at: 2026-09-06T14:02:00Z
completed_at: 2026-09-06T19:03:41Z
branch: claude/planner-chrome
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

- [x] 手機上行程頁的常駐浮動高度砍到一層（工具列）加一個可展開的入口。
- [x] 意圖列在手機上預設收合成一顆帶標籤的按鈕，點開才是輸入框與範圍選擇。
- [x] 桌機維持現狀。

## Steps

- [x] `itinerary-diff.tsx`：手機斷點下把意圖列收成一顆按鈕，展開後是同一張表單。
- [x] `globals.css`：`--planner-dock-clearance` 隨收合狀態調整，`.planner-app-shell`
      的底部保留區跟著縮小。
- [x] 補上 `itinerary-diff.test.tsx` 的收合／展開案例。

## How to verify

`cd apps/web && npx playwright test e2e/navigation.spec.ts --project=mobile-chromium`
應該不需要先把卡片捲到畫面中間就能點到「編輯」；量一下 390×844 下常駐浮動元件的
總高度應該低於 8rem。


## Notes

### 做完之後（2026-09-07，claude-opus-5）

**大部分已經被另一個 PR 做掉了。** 開始動工前先讀 `itinerary-diff.tsx`，
意圖列的收合已經在 main 上：`intentOpen` 預設 `false`、手機上是一顆帶
`aria-expanded` 的按鈕、表單 `hidden lg:grid`、桌機不受影響，連
`itinerary-diff.test.tsx` 的收合／展開案例都有了。程式碼裡的註解描述的正是這張票的症狀，
所以是同一輪 UX 整理順手做的，只是沒有回來關這張票。

剩下沒做的是 Steps 的第二條：`.planner-app-shell` 的底部保留區。
那裡是 `calc(var(--planner-dock-clearance) + 6rem)`，六個 rem 是照「四排、永遠展開」
的意圖列估的。現在手機上它預設只有一顆按鈕，而且它是 `sticky` 不是 `fixed`——
本來就佔版面空間，捲到底時最後一張卡片自然在它上面。多出來的部分只是每次捲到底
都會看到的空白，改成 2.5rem。

沒有做「保留區隨收合狀態動態調整」：那需要把元件的狀態送到 shell 那一層
（CSS 變數或 data attribute），而收合是預設值、展開是短暫動作，為了那幾秒讓
兩個元件互相知道彼此的狀態不划算。
