# 實際 Next.js 頁面整合驗證

文章頁、Gemini 總目錄、前後篇與生活分享入口已接入伺服器可見清單。正式 `guide-series.json` 保留原 50 篇；深入 36 篇只寫入本測試的隔離副本，沒有改動公開資料庫或部署環境。

## 資料邊界

`article-page.tsx` 重用目前文章或另讀 hub 的發布狀態，產生一次 `getVisibleGeminiSeries()`；`GuideArticle`、目錄、導航均接收同一份資料。`gemini-series.ts` 已不再匯入原始 JSON。只有 server loader 能讀正式 catalogue，client bundle 只含純搜尋 helper、UI 與文案，收到的 props 已過濾。

`GEMINI_ADVANCED_SERIES_ENABLED` 未設定或不等於字串 `true` 時，完整 86 篇測試資料只顯示 01–50。開啟時顯示 01–86、原五條與新增六條路線。正式檔仍是 50 篇時不會從課綱自動補篇；開關不是授權或匯入程序。

正文也在 server render 前過濾：隱藏目標的具名連結改成可讀純文字，原始網址改成「相關教學」；保留原二級標題的位置與 section-N。清理 rich_paragraph 的兩類連結、link、list、table、code／一般文字、來源與 article_links。life 列表卡片及其 ItemList 共用同一集合。其他系列保留原 API 導覽，Claude 有獨立回歸測試。

本邊界限制入口、目錄和連結。逐篇匯入後的直接文章 URL 仍按既有 API 發布狀態可讀；完成新舊子文章驗收後才開總目錄的順序仍由 release 任務負責。

## 重跑

從 repository 根目錄，使用 Node 22 以上與已安裝的 Next／Playwright Chromium：

```powershell
node docs/gemini-series/advanced/platform/next-integration/prepare.mjs
node docs/gemini-series/advanced/platform/next-integration/build.mjs
$env:GEMINI_E2E_ADVANCED = 'false'
node node_modules/@playwright/test/cli.js test --config docs/gemini-series/advanced/platform/next-integration/playwright.config.ts
$env:GEMINI_E2E_ADVANCED = 'true'
node node_modules/@playwright/test/cli.js test --config docs/gemini-series/advanced/platform/next-integration/playwright.config.ts
Remove-Item Env:GEMINI_E2E_ADVANCED
```

prepare 建立新 `.workspaces/next-*` 副本，排除 `.env` 與建置暫存；node_modules、public 以 junction 共用，只讀用於測試。它保存複製來源雜湊，核對正式 JSON 沒有變更。build 保留完整日誌及退出碼，使用 canonical 網址建置，API 只指向 loopback，不呼叫正式網站。沒有跳過 Next 的 generated route type checks；本次發現並修正兩個既有文章路由的 generateMetadata 第二參數，改成框架要求的 ResolvingMetadata。

Playwright 啟動兩個 loopback 程序：fixture API 與實際 `next start`。瀏覽器顯示 canonical URL，但所有請求經攔截改到 loopback，其餘網路封鎖。API 回傳本機 87 份實際文章包；額外在 hub 植入所有 36 篇的 rich_paragraph／article／link／list 參照，確認隱藏效果涵蓋正文與 RSC。此紀錄不證明 Google 帳號、模型、收費、發布或 production sitemap 已驗收。

## 覆蓋範圍

- 每種開關各跑 desktop 1200×900 與 mobile 360×800，五項流程共十項測試。
- 逐篇檢查 50／86 篇真實正文、標題、目錄入口、前後篇、指令錨點與整頁橫向溢出。
- 六個搜尋別名、八類、五／十一條路線、深入／MD 交集、清除篩選。
- 基礎 18、36、47、50 與深入 69、73、81、86 的真實 code 區塊複製；只正規化 Windows 換行。
- 停用 JavaScript 時全部連結仍存在，能按固定 slug 進入第 36 篇，顯示圖解。
- hub 未發布時入口與專用導航不出現；發布後可見。查詢參數不能繞過 server flag。
- HTML 與 `text/x-component` RSC 逐一檢查隱藏 slug；載入的 client JS 在兩種狀態均不得包含任何深入 slug。

結果以 `build-results.json`、`base-results.json`、`advanced-results.json` 與已挑選的 evidence 截圖為準。未完成的測試不得只以這份覆蓋清單視為通過。

初次 advanced 桌面跑到第 19 篇時，trace 記錄 loopback `route.fetch` 讀取兩個 chunk 發生 `ECONNRESET`，使瀏覽器報 ChunkLoadError。測試代理現在只為 GET 的 ECONNRESET 重試一次（Playwright 原生 `maxRetries`）；不重試 HTTP 錯誤、不改產品或放寬斷言。保留 [初次傳輸錯誤摘要](evidence/initial-transport-failure.json)、[初次 9 過／1 失敗報告](evidence/initial-advanced-results.json) 與原 trace 雜湊，完整 trace 留在忽略的 `.workspaces/initial-failure`。接續 advanced 全套重跑十項全部通過。

## 2026-09-15 驗收結果（台灣時間）

[完整驗證摘要](verification.json) 記錄：Next 16.3.3 production build、來源型別、ESLint、五語系同 key 通過；[相關單元及整合測試](unit-results.json) 13 檔／160 項全過，系列工具 17 項與 87 份草稿包檢查全過。

[50 篇模式](base-results.json) 10 項全過，348.74 秒；[86 篇模式重跑](advanced-results.json) 10 項全過，254.30 秒。兩份成功紀錄共逐篇讀取 272 次正文頁，另含 hub、無 JS 與發布狀態測試；無略過、失敗或整項測試重試。兩輪測試代理的差異與程式雜湊另存 [runner-revisions](evidence/runner-revisions.json)。最終手機案例有四個預取回應已釋放的診斷訊息，頁面斷言全部通過，紀錄未移除。

已人工目視 [桌面深入目錄](evidence/advanced-desktop-directory.png)、[360px 基礎目錄](evidence/base-mobile-directory.png)、[360px 深入目錄](evidence/advanced-mobile-directory.png)、[無 JS 的 MD 圖解](evidence/mobile-diagram-no-js.png) 與程式區塊。手機選單為單欄，較長的篩選面板以垂直捲動使用；程式長行留在區塊內水平捲動，沒有整頁橫向溢出。這些都是隔離 Next 實際頁面截圖。

正式 catalogue 仍為 50 篇，原檔雜湊保持不變；本次未寫入 production。整套深入系列尚待作者票的必要真實 Google 帳號／模型與影片驗收，再由 release 票整合 catalogue、重查價格、發布及檢查公開 sitemap。
