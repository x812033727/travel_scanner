# Claude Code 系列驗收紀錄

查證／驗收日期：2026-09-14。環境為 Windows、PowerShell、Node.js 22+、Next.js 16.3.3、Chromium 與 API 的 uv 開發環境。此紀錄只代表此工作分支的本機結果。

## 交付與內容

- 1 個總目錄、60 篇教學；61 個原生內容 JSON、61 份作者 Markdown、61 組 JPG 封面／SVG 原稿／SVG 圖解。
- 60 個網址、十個單元與五條推薦路線集中於版本控管的系列清單；沿用既有排程的五個 Claude Code 網址。
- 第 01–59 篇正文均達 1,800 字，總目錄與速查表依用途調整。精確逐篇數值在 content-validation.json。
- 49 個官方來源實際取得，保存 2026-09-14 日期、URL、HTTP 狀態、標題與 SHA-256；sources 清單逐篇對照。每十篇的檢查摘要在 batch-review.json。
- 三份下載包為 starter、bug-toggle、complete；沒有資料庫或外部套件依賴，Node.js 22+ 可啟動及測試。

## 已執行檢查

| 檢查 | 命令／範圍 | 結果 |
|---|---|---|
| 本機 Claude CLI | `claude --version`、`claude --help` | Windows 2.1.233，兩個命令 exit 0；只讀說明，不啟動代理或登入 |
| 原生內容包 | `python -X utf8 tools/claude-code-series/validate.py` | 61 頁、0 缺漏、0 錯誤、0 警告 |
| 封面／圖解 | `node tools/claude-code-series/render-art.mjs` | 全部 61 組通過 SVG 文字邊界檢查與 JPG 輸出 |
| 相關 API | `uv run pytest tests/test_guide_series.py tests/test_guides_content_pack.py tests/test_guides.py tests/test_site_pages.py`，位於 apps/api | 163 passed、99 skipped；未設定可選 PostgreSQL 測試連線的參數案例跳過 |
| API lint | `uv run ruff check .`，位於 apps/api | 通過 |
| API 型別 | `uv run mypy app`，位於 apps/api | 327 個來源檔通過 |
| 相關前端元件 | admin-guides-panel、content-blocks、guide-rich-editor、guide-series、guides/article 的 Vitest | 114 passed |
| 廣告插入回歸 | `npx vitest run lib/adsense.test.ts`，位於 apps/web | 41 passed；rich_paragraph 納入段落辨識，code 保持完整 |
| 完整前端測試 | `npx vitest run --reporter=verbose --bail=1`，位於 apps/web | 256 個檔案、2,778 項全部通過，exit 0（1,576.67 秒）；完整輸出在 web-suite.log |
| 工具測試 | `npm run test:tools` | 36 passed，含本系列 8 個頂層案例 |
| 前端 lint | `npm run lint:web` | 通過 |
| i18n | `npm run check:i18n` | 五個語系、25 個 namespace 通過 |
| 正式建置／型別 | `npm run build:web`、`npm run typecheck:web` | 通過（包含最後目錄摘要微調與追加的瀏覽器測試型別） |
| 瀏覽器 | `npx playwright test --config tools/claude-code-series/playwright.config.mjs` | 7 passed（3.9 分鐘）；追加完整組合篩選與路線順序後，該案例另 1 passed（58.4 秒），見 filters-browser.log |
| 任務／差異 | `npm run check:tasks`、`git diff --check` | 通過；任務佇列原有過期認領與其他任務範圍重疊警告仍保留，與本系列無重疊 |

## 瀏覽器驗收範圍

使用真正 Next.js 正式建置與唯讀本機 API fixture。測試不連接正式 API，也不以更改正式發布狀態取得預覽。API 的真實公開條件另由資料庫整合測試覆蓋。

七項瀏覽器案例包含：

1. 關閉 JavaScript 後，總目錄仍顯示 60 篇連結與 CollectionPage／ItemList 結構化資料。
2. 搜尋 MD、手機、權限、/compact、MCP；組合主題／程度／平台／路線、URL 重新整理與返回、無結果與一鍵清除。
3. 遍歷 61 頁，檢查標題、站內引用、上一篇／下一篇與桌面頁寬。
4. 360px、390px 的 CLAUDE.md、Hooks、指令速查頁，檢查可展開目錄、表格與程式碼局部捲動、整頁不溢出。
5. 真正解壓 complete.zip 後，新增、勾選、篩選、刪除、重新整理持久化、惡意 HTML 純文字呈現與損壞儲存資料恢復。
6. Markdown、JSON、HTML 複製按鈕將原始字串傳入瀏覽器原生剪貼簿。讀回時僅正規化 Windows 自動轉換的 CRLF；縮排、引號及特殊字元一致。
7. 生活分享分頁仍有固定入口，系列 API 503 可重試，缺少語系時不出現系列內容連結。

最終七項機器報告為 browser-tests.json，追加篩選驗收見 filters-browser.log。補入第 25 篇本機 CLI 版本紀錄後，再次通過內容包檢查，並以最新預覽 HTTP 200 確認更新文字可見，見 final-preview.json。已目視檢查 hub-controls-desktop.png、claude-md-guide-code-390.png、hooks-getting-started-code-360.png、templates-cheatsheet-code-360.png、practice-complete-360.png；全文截圖也保存在同目錄。目視確認字體與按鈕可讀、內容不撐寬頁面，長程式碼可於區塊內捲動。

## 範例的實際驗證與限制

工具測試實際解壓並執行三個 ZIP：starter 4 項通過，complete 6 項通過，bug-toggle 的指定測試依教學設計失敗。全部文章 JSON 範例能解析，JavaScript 範例通過 Node 語法檢查；第 33、34、56 篇功能／除錯／重構範例以 starter 的真實資料形狀執行。第 41、42 篇 Hook 腳本以人工 JSON 事件輸入驗證正常、缺少 cwd、語法錯誤、合法檔案與重複 Stop 分支。

**官方文件核對不等於產品實機操作。** 未操作 Claude 訂閱登入、iOS／Android 實機、Dispatch 配對、Remote Control 真實連線、第三方 MCP、Claude Computer Use、付費 SDK 呼叫或外部 GitHub Actions。這些篇章提供核對過的步驟與成功判準，並在文章中標明驗證範圍。發布前仍需重查變動中的資格與介面。

## 發布狀態

本機可預覽、可檢查內容包。**未部署、未匯入正式資料庫、未公開發布、未建立 PR 或合併。** 本機 fixture 中的可閱讀狀態只是審閱材料；正式資料庫的發布條件與 sitemap 仍由既有流程管理。

後續需依部署、內容匯入、公開發布各自的授權與執行結果接續，先支援新 renderer／API，再匯入新格式內容。交付 ZIP 只包含內容、素材與審閱文件，應用程式修改保留於此工作分支。
