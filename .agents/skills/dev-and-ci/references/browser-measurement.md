# 版面量測：手機點擊落空、CLS

共同原則：量到完美的數字時，先證明這個量法有能力回報不完美的數字。

## Playwright 手機專案一直 `intercepts pointer events`

**症狀。** `mobile-chromium`（Pixel 7）或窄視窗的測試，點一個看得見、enabled、穩定的元素，整個逾時期間都回報 `<div>…</div> intercepts pointer events`，而且每次重試指名的元素不同；同一個測試在桌面過。

**成因：水平溢出把 layout viewport 撐寬了**，不是 z-index、不是時序。Chrome 的手機模擬遇到比裝置寬的內容，會把 layout viewport 放大（Pixel 7 的 `window.innerWidth` 從 412 變 522；320px 的視窗變 342）。Playwright 的 `boundingBox()` 還在裝置座標裡，於是之後每個點擊座標都指到別處，命中測試落在剛好在那裡的元素，通常是某個父層 `<div>`。

看過的兩種來源：
- 一段含裸 URL 的授權文字。URL 沒有斷行點，撐出卡片的最小寬度；`break-words`（`overflow-wrap: break-word`）一個 class 就修好。任何可能含 URL 或長 token 的新 UI 字串，上線前就要有換行 class。
- 手機 header 多了第六個 2.75rem 的圖示，320px 下整列比 header 的內容框寬。

**不要猜，印出真相。** 開一個一次性的 commit，在目標中心點記錄 `window.innerWidth`／`innerHeight`、`scrollY`、`document.elementFromPoint(x, y)`，花一輪 CI 就結束爭論。那次先猜了三個原因（開著的下拉選單、視窗邊緣的固定元件、資料載入時的位移），每個花一輪 CI、全錯。

**會抓到它的斷言。** `document.documentElement.scrollWidth > innerWidth` **永遠抓不到**：瀏覽器把 `innerWidth` 放大到跟內容一樣寬，兩者按定義相等。要斷言：

```ts
await page.setViewportSize({ width, height: 740 });
await page.evaluate(() => { document.documentElement.dataset.textSize = "largest"; });
expect(box.x + box.width).toBeLessThanOrEqual(width);                         // 那一列自己的右緣
expect(await page.evaluate(() => window.innerWidth)).toBeLessThanOrEqual(width); // viewport 沒被撐寬
```

範例與完整註解：`apps/web/e2e/discovery.spec.ts` 的 header 寬度測試。

**字級的兩個陷阱。** 用 `rem` 排的列，寬度由讀者選的字級決定（`html[data-text-size="largest"]` 是 125%，字級在 `apps/web/lib/text-size.ts`）：斷點要從最大那一級算、也要測最大那一級，否則只在你剛好量的字級上有效。media query 無法跟著調整，因為 media query 裡的 `rem`／`em` 是初始的 16px，不是選的根字級。

## CLS 要在頂層頁面量

內建瀏覽器（Browser pane）裡的 `PerformanceObserver({ type: "layout-shift" })` **什麼都不回報**，連故意插一個 220px 的 div 都沒有；`PerformanceObserver.supportedEntryTypes` 卻照樣列出 `layout-shift`，所以沉默看起來跟「這頁 CLS 0」一模一樣。layout shift 只對最外層的 main frame 回報，而面板不是。

量法：
1. 用 Playwright：`chromium.launch()`、一個全新的 context（沒有存過的字級偏好）、`page.addInitScript` 在第一次繪製前裝好 observer，累加沒有 `hadRecentInput` 的 `value`。
2. **先對一個故意會位移的對照頁跑同一支腳本**，確認它回報非零，再相信目標頁的數字。
3. 腳本放 scratchpad，套件用 `createRequire("<worktree>/apps/web/package.json")("playwright")` 解析；本機完整版 Chromium 起不來時見 local-env.md 的 headless shell。

同一條規則推廣：任何回來是完美數字的量測（CLS 0、零溢出、零錯誤），先證明儀器量得出不完美的。
