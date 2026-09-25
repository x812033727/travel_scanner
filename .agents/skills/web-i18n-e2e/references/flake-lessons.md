# 不會 flake 的測試：從結案的票學到的

每一條都有票可查。原則只有一個：**flake 是還沒找到的成因，不是運氣**。不要放寬斷言、不要加長逾時、不要 skip、不要加 retry 讓它變綠；「紅了就重跑」會訓練大家把真正的失敗也一起重跑掉。

## Playwright

### 1. 等條件，不要等時間；等「那一個」回應

- 斷言某段內容前，先想清楚它是哪一支請求畫出來的，用 `page.waitForResponse` 等**那一支**，而且在觸發動作**之前**建立 promise：

  ```ts
  const sessionReady = page.waitForResponse((response) =>
    new URL(response.url()).pathname === "/api/travel/auth/me" && response.request().method() === "GET");
  await page.goto("/en/my");
  await sessionReady;
  ```

- 兩個頁面都會打同一支 API 時，各自建一個 promise，不要讓第一頁的回應滿足第二頁的等待（`apps/web/e2e/site-pages.spec.ts` 的做法）。
- `expect(locator).toBeVisible()` 這類 web-first 斷言會自己重試；`waitForTimeout` 永遠是錯的。
- 網址斷言用 predicate 比 pathname：`await expect(page).toHaveURL((url) => url.pathname === "/zh-TW/trips")`。regex 會被 `?next=/trips` 這種查詢字串提早滿足（`apps/web/e2e/full-stack.spec.ts` 的註解）。

### 2. 測試結束時不能有還在跑的 route handler

`page.route` 裡 `await route.fetch()` 之後再 `await response.json()`：測試如果在這兩步之間結束，context 關閉會丟掉 body，handler 丟出 `Response has been disposed`，把一個早就通過的測試變紅（trace 顯示 `json()` 在 Close context 之後 4 ms 才跑）。修法：測試的最後一個斷言之前，先等那支被代理的回應完成。來源：`tasks/done/2026-09-15-ci-recurring-flakes.md` 第 4 點。

### 3. dev server 的冷編譯不是測試的問題

CI 曾經讓 Playwright 起 `next dev`，每頁第一次打開才編譯，30 秒逾時要同時吃掉編譯與 API，偶爾超過；伴隨的 `SyntaxError: Unexpected end of JSON input` 是編譯中被打斷的回應。修法是 `PLAYWRIGHT_SERVE_BUILD=true`，不是加長逾時。本機看到同樣症狀，先 build 再用這個旗標重跑。來源：`tasks/done/2026-09-06-flaky-navigation-e2e.md`。

### 4. keep-alive 連線被伺服器先關掉

`APIRequestContext`（`request` fixture、`page.request`）會重用 keep-alive socket，沒有 client 端閒置逾時也不重試。Node 預設 5 秒就關閒置連線，測試隔了約 6 秒再用同一個 context 就 `read ECONNRESET`。`apps/web/package.json` 的 `start` 因此是 `next start --keepAliveTimeout 65000`；自己寫的測試伺服器也要比 client 活得久。來源同第 2 點。

### 5. 測試量得到的才算數

- `context.setOffline(true)` 與 `page.route` 都碰不到 service worker 的 fetch；「離線後重新載入」在沒有 app shell 快取的架構下本來就不成立。寫不出能證明那件事的 e2e，就不要留一支斷言比名字弱的 e2e。來源：`tasks/done/2026-09-11-offline-today-e2e.md`。
- 後台頁掉進 error boundary 不觸發 `pageerror`（見 `references/e2e-local.md`）。一個新頁面至少要有一個「資料真的畫出來才成立」的斷言，並且反向驗證：拿掉 fixture，測試要紅。

### 6. 假資料的漂移會偽裝成 flake

假 API 或 spec 裡手抄的清單（操作、導覽、角色）沒跟上正式那份，錯誤會出現在不相干的頁面上，看起來像隨機。加一個讀兩份原始碼比對的單元測試（範本：`apps/web/lib/usage-catalog-e2e-fixture.test.ts`），失敗訊息直接列出缺的名字。

## 元件測試（Vitest），同一個家族

`apps/web/vitest.config.ts`：jsdom、單執行緒、`testTimeout` Linux 5 秒、Windows 15 秒。整套跑與單檔跑的時序不同，負載下才紅。

### 7. passive effect 比 commit 晚一個 scheduler task

`tasks/done/2026-09-11-modal-escape-flake-under-load.md` 查了四天、推翻五個假設才找到：React 19 對非 sync lane 的更新（例如 `fetch` 回來後在 `act` 外面的 `setState`），**DOM 已經 commit、`useEffect` 還沒跑**；RTL 的 `waitFor`／`findBy` 條件成立後用 `setTimeout(0)` 收尾，可能排在 Scheduler 下一個 task 前面。測試（或真的使用者）就落在空檔：Escape 還沒有 listener、overlay 還沒註冊成最上層所以「關閉」被守門擋掉、關閉 handler 還是舊的 closure、焦點還沒移到結果區。

寫元件時：

- 「讓 DOM 可以被操作」所需的東西——註冊 modal layer、掛 keydown listener、鎖捲動、同步給事件 handler 讀的 ref、移動焦點——用 `useLayoutEffect`，跟 DOM 在同一個 commit。
- 例外：**關閉後把焦點還給開啟者要留在 passive 階段**。layout cleanup 跑在 mutation 階段，React 會在同一個 commit 把焦點還原到 commit 前的元素，蓋掉你的 focus（`apps/web/lib/modal-sheet.ts` 的做法：layout cleanup 記下 opener，無 deps 的 `useEffect` cleanup 才 focus）。
- 從延後的 callback（effect、`requestAnimationFrame`、請求回來後）搶焦點之前，確認焦點還在觸發時的位置；讀者可能已經移走了（`apps/web/components/route-mode-panel.tsx` 的 `previewFocusOriginRef`）。

寫測試時：

- 要把這個空檔變成確定的，用 `apps/web/lib/testing/commit-before-passive-effects.ts` 的 `commitBeforePassiveEffects(update, committed)`：在 `act` 外觸發更新、讓 Scheduler 在 commit 後一定讓出，commit 一到位就把控制權交回測試。範例在 `apps/web/lib/modal-sheet.test.tsx`、`apps/web/components/planner-overlay.test.tsx`、`apps/web/components/route-mode-panel.test.tsx`。修正前要紅、修正後要綠，兩個方向都跑過才算。

### 8. 查 flake 的方法

- 整套輸出先導到檔案再看：`npx vitest run > run.log 2>&1`。診斷輸出只在紅的那一次存在，用 grep 只看 `×` 會把它丟掉（那張票真的丟過一次）。
- 裝探針比猜測有用：暫時包住 `HTMLElement.prototype.focus` 或 keydown listener，用 `process.stderr.write` 記「從哪裡到哪裡、哪一行」（vitest 會攔 `console.log`）。有證據再改。
- `npx vitest run --sequence.shuffle` 很划算：一跑就撈到兩條真的順序相依（URL 狀態沒在測試間重設、沒設路徑就斷言），它們是缺陷不是 flake。
- 斷言失敗時印出現場（幾個 dialog、有沒有被 `inert`／`aria-hidden` 蓋住、body 的 position／overflow），下一次紅的時候才有東西可看。
- 同一個 commit 一紅一綠是最乾淨的非決定性證據；CI 的 run 連結會過期，趁早記進票裡。

### 9. 時鐘

模組載入時讀一次今天日期、呼叫時再讀一次的測試，跨 UTC 午夜就紅（api 那邊的例子：票 `2026-09-22-fix-midnight-utc-rollover-flake-in`）。web 測試同理：把時間固定（`vi.useFakeTimers()`／`vi.setSystemTime()`），或從受測程式讀時間的同一個來源取期望值。
