---
id: 2026-09-28-video-shorts-tab-browser-fixes
title: Video shorts tab: fix what a real browser showed after W1 merged
status: in-progress
priority: P2
area: web
owner: claude-fable-5-1-shorts
claimed_at: 2026-09-28T13:24:00Z
created_at: 2026-09-28T13:19:57Z
completed_at:
branch: claude/video-shorts-tab-browser-fixes
depends_on: []
scope:
  - apps/web/components/admin-video-shorts.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/components/admin-video-shorts-calendar.tsx
  - apps/web/components/admin-video-shorts-calendar.test.tsx
  - apps/web/components/admin-video-shorts-data.ts
  - apps/web/components/admin-video-shorts-metrics.tsx
  - apps/web/components/admin-video-shorts-metrics.test.tsx
  - apps/web/components/admin-video-shorts-costs.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video shorts tab: fix what a real browser showed after W1 merged

## Why

Shorts 分頁（`2026-09-28-video-shorts-admin-tab`，PR #912）合併時只有元件測試。元件測試的環境不做版面計算，回應也是手寫的，所以有些事要到真的瀏覽器裡才看得到。合併之後第一次對著一支照伺服器格式回答的假 API，把分頁的每個畫面在瀏覽器裡看過一遍，找到六件事。都是畫面上說錯話或少說話，不影響資料，也不影響送到 YouTube 的東西：

1. 單支 Shorts 的頁面，標題旁邊出現「等你決定語言」。Shorts 的語言由 Shorts 設定決定，伺服器算 `ready_to_upload` 時本來就不等這個決定（`apps/api/app/video_reviews/admin_service.py` 的 `_summary`），網頁的 `publishState` 沒有跟上，這支還會因此被算進「需要你」。
2. 同一個位置有兩個講同一件事的標籤：上架流程的「已上架」與 Shorts 自己的「已公開」。
3. 花費把一筆 NT$0.29 的旁白寫成 NT$0（四捨五入到整數）。旁白一筆就是幾毛錢，寫成 0 讀起來像沒花錢。
4. 成效：已下架的 Shorts，沒有數字的格子寫「時間還沒到」「等下一次讀取」，但伺服器在下架之後不會再讀它。
5. 月曆與頂列：空格的狀態與標題都寫「空格」；標成不發的那一格還寫「空格」或「還沒有排影片」。
6. 片庫：桌面 App 內建的瀏覽器面板（Chromium 152）一打開片庫整頁就停住，連 `1 + 1` 都不回。

## Definition of done

- [x] Shorts 沒有上架流程的那五個狀態（`publishState` 回 `null`）：頁面只用 Shorts 自己的狀態說一次，也不會因為語言被算進「需要你」。教學影片與漫劇的行為不變。
- [x] 帳目、合計與頂列的金額保留到小數兩位，整數照舊。
- [x] 已下架的 Shorts：下架時還沒關閉的時間窗與「最新」寫「已下架，不再讀取」（五個語系的新鍵 `videoShorts.metrics.blank.removed`）；下架前就關閉的時間窗照舊寫「沒有在時間窗內讀到」。
- [x] 月曆的空格寫一次「空格」，下面是「還沒有排影片」；錯過與不發的格子只寫狀態與備註。頂列「今天」「明天」裡不發與錯過的時段也只寫狀態。
- [x] 片庫卡片的封面框不用 `aspect-ratio`，測試擋住改回去。
- [x] 成效表的四個欄位等寬：空欄不會被擠成一行一個字。
- [x] 每一項都有元件測試；八個畫面在 Chrome 153 裡以桌機與手機寬度看過，沒有一頁比視窗寬。

## Steps

- [x] 用假 API 加 `npm --prefix apps/web run dev` 把每個畫面打開，記下看到的事。
- [x] 片庫停住的原因：把卡片一段一段換掉，直到找出是哪一段。
- [x] 逐項修、逐項補測試。
- [x] 在獨立啟動的 Chromium 151、Chrome 153、Edge 154 確認片庫；在 Chrome 153 截圖。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run --no-file-parallelism components/admin-video-shorts components/admin-video-reviews components/admin-video-youtube
```

## Notes

- 認領時用了 `--force`，理由跟 W1 那張票一樣：工具說重疊的四張票（`2026-09-27-video-drama-room-web`、`…-drama-room-withdraw-a-one`、`…-languages-web`、`…-split-settings-web`）的工作都在 PR #870 合併了，票只是還沒被 `done`。那四張票我沒有動。
- **片庫停住只發生在一個地方**：桌面 App 內建的瀏覽器面板（Chromium 152.0.7977）。同一頁在獨立啟動的 Chromium 151、Chrome 153、Edge 154 都正常（用 Playwright 量：頁面答得出 `1 + 1`、封面框是 72×128）。條件是「`<button>` 裡有一個靠 `aspect-ratio` 決定高度的框」：把 `<button>` 換成 `<div>`、或把框換成固定高度，就不會停；`<button>` 是不是格線容器沒有差別。站主用的瀏覽器不受影響。改成固定高度是因為它比較簡單，而且之後用那個面板驗證頁面的人不會再卡在這裡。
- 元件測試看不到這種事：jsdom 不做版面計算。要看版面，用真的瀏覽器；要量，用獨立啟動的瀏覽器（面板隱藏時不載入延遲載入的圖，截圖也不可靠）。
- 在忙碌的機器上，後台外殼讀 bootstrap 會逾時，頁面顯示「營運控制台暫時無法連線」；伺服器先畫出來的是預設分頁（空的），讀到網址之後才換到 Shorts。截圖的腳本要等「Shorts 分頁被選上、而且頁面連續幾秒沒有在讀取」才拍，否則拍到的是過渡畫面。這兩件事都是既有的行為，不在這張票的範圍。
- `dollars()` 原本的說明寫「整數」。改成最多兩位小數之後，1,234.5 會寫成 NT$1,234.5；整數金額（上限、預算）不變。
- 已下架的判斷用的是網站「發現」下架的時間（`youtube_removed_at`），不是 YouTube 上實際下架的時間；後者 API 不給。
- 這一版仍然沒有對著真的 API 與真的頻道看過，那是 `2026-09-28-video-shorts-pilot-launch` 的事。
