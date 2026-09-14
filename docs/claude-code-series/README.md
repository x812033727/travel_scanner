# Claude Code 教學中心交付

> 第二階段已新增 36 篇，現在可預覽 97 頁；請見[深入教學交付目錄](advanced/README.md)。下列 60／61 篇與驗證數量保留第一階段的歷史紀錄。

本機實作包含 **1 個總目錄、60 篇繁體中文教學、61 組封面與圖解、3 份練習專案下載包**。第 01–59 篇正文約 1,800–2,100 字，另外提供完整程式碼；總目錄與第 60 篇速查表依用途縮短。全文約 11 萬字，沒有只放標題的待補文章。

系列入口：`/zh-TW/life/claude-code-tutorials`。原生內容包沿用 `kind: life`、`zh-TW`、`ai`、`tutorial`，可交給既有後台與匯入流程。**本次沒有寫入正式資料庫、沒有公開發布，也沒有部署。**

## 立即預覽

在儲存庫根目錄，先確保 Node.js 22+、npm dependencies 與 API Python 開發環境已備妥：

```powershell
npm run build:web
node --experimental-strip-types tools/claude-code-series/preview.mjs
```

命令會印出 `http://127.0.0.1:<port>/zh-TW/life/claude-code-tutorials`，直接開啟即可閱讀全部 61 頁。這個預覽使用唯讀 HTTP fixture，將版本控管中的草稿內容交給真正的 Next.js 公開呈現元件；不連接正式 API、不匯入資料、不更動發布狀態。按 Ctrl+C 同時停止預覽與其本機 API。

預覽使用正式建置；修改 UI 後要重新 build 並重啟。內容也在啟動時載入，改文章後重啟預覽。其他網站功能在此 fixture 中不作功能承諾。

## 檔案位置

| 內容 | 位置 |
|---|---|
| 唯一系列清單、60 篇順序、五條路線、別名與依賴 | `apps/api/app/guides/series_data/claude-code.json` |
| 作者原稿，00 為總目錄 | `docs/claude-code-series/lessons/00.md` 至 `60.md` |
| 原生文章包 | `apps/api/app/guides/content/claude-code-*.json` |
| 封面與圖解 | `apps/web/public/guides/claude-code-*/` |
| 起始／錯誤／完成版 ZIP | `apps/web/public/tutorials/claude-code/` |
| 練習原始碼與產生器 | `tools/claude-code-series/lab/`、`build_lab.py` |
| 官方來源日期、回應狀態與 SHA-256 | `source-checks.json` |
| 篇幅、來源、連結、素材與瀏覽器證據 | `evidence/` |
| 可攜式內容交付包 | `review-bundle.zip`（由 bundle.py 產生） |

原排程批次 04 的五個 Claude Code slug 已移交本系列，網址沿用，沒有再建立同題不同網址；該批次其餘十五篇保留原狀。一般文章排序的既有任務未改動，生活分享的固定系列入口獨立於分頁。

## 功能與資料約定

- `GET /api/v1/guides/series/claude-code?locale=zh-TW` 以系列清單排序，使用目前可公開的語系版本產生標題與連結。
- 公開文章可選擇帶有 `series` 與 `article_links`；非系列舊文章不需補資料。
- 未公開、隱藏、撤回、過期或缺少目前語系的目標不出現在可點擊導覽中。缺少公開 revision 的異常採失敗關閉，回報暫時不可用。
- `rich_paragraph` 保存 text、code、article 或 link 片段。article 使用 kind/slug 識別，由後端核對公開狀態、前端產生目前語系網址；無法解析時呈現純文字。
- `code` 保存 language、label 與原始 code 字串，以跳脫文字顯示，不執行範例 HTML。複製按鈕傳入原始字串；Windows 原生剪貼簿可能將 LF 轉為 CRLF，內容、縮排、引號與換行仍保留。
- 後台編輯與預覽使用相同區塊呈現元件。JSON／Markdown 範例保留縮排，表格與程式碼局部水平捲動。
- 目錄先輸出完整可閱讀 HTML，再以 JavaScript 加上搜尋與篩選。q/group/level/platform/path 保存於 URL，重新整理或從文章返回可恢復條件。
- 總目錄使用 CollectionPage 與 ItemList；分篇沿用文章 SEO，sitemap 仍採原有公開條件。

## 查證與實測的分界

49 個官方來源於 **2026-09-14** 實際取得並保存日期、URL、HTTP 狀態與內容雜湊。來源更新較快，發布前仍應重查資格、模型、命令與介面步驟。

另於本機 Windows 的 Claude Code **2.1.233** 執行 `--version` 與 `--help`，核對啟動參數；結果見 `evidence/claude-cli-check.json`，這項檢查不包含登入或代理工作。

**已實際驗證的範圍**：此網站的 API／UI／內容包、下載 ZIP 中的 Node 程式、文章可離線執行的 JSON／JavaScript、Hook 腳本的人工事件輸入，以及待辦完成版的瀏覽器操作。

**沒有代讀者操作的範圍**：Claude 訂閱登入、iOS／Android 裝置、Dispatch 配對、Remote Control 真實連線、Notion／GitHub MCP、Claude Computer Use、付費 SDK 呼叫、GitHub Actions 外部執行。文章提供依官方文件核對的操作與成功判準，不將文件查證當成這些服務已由作者實機操作。

來源包括 [Claude Code 平台](https://code.claude.com/docs/en/platforms)、[記憶與規則](https://code.claude.com/docs/en/memory)、[Skills](https://code.claude.com/docs/en/skills)、[Hooks](https://code.claude.com/docs/en/hooks-guide)、[MCP](https://code.claude.com/docs/en/mcp)、[Agent SDK](https://code.claude.com/docs/en/agent-sdk/quickstart)；逐篇來源列在各內容包的 sources，完整清單在 source-checks.json。

## 重建與檢查

PowerShell，在儲存庫根目錄：

```powershell
apps/api/.venv/Scripts/python.exe -X utf8 tools/claude-code-series/build_lab.py
apps/api/.venv/Scripts/python.exe -X utf8 tools/claude-code-series/generate.py
node tools/claude-code-series/render-art.mjs
apps/api/.venv/Scripts/python.exe -X utf8 tools/claude-code-series/validate.py
node --test tools/claude-code-series.test.mjs
npx playwright test --config tools/claude-code-series/playwright.config.mjs
```

文章產生器只寫內容 JSON 與 SVG，不匯入資料庫。`render-art.mjs` 在本機瀏覽器輸出 JPG 並檢查所有 SVG 文字邊界。`research.py` 可重新查官方來源，會更新查證日期與雜湊，應與原稿逐篇比對後才提交。

每十篇的檢查紀錄在 `evidence/batch-review.json`。瀏覽器驗收遍歷 61 頁、檢查站內目標、前後篇、五個指定搜尋字詞、組合篩選、URL 返回、無 JavaScript HTML、360／390px 閱讀、原生剪貼簿與載入失敗重試。實際執行結果與限制以 `evidence/verification.md` 為準。

## 既有發布流程的接續點

本次交付停在本機可預覽與內容包檢查。取得後續授權後，先部署支援新區塊與系列 API 的應用程式，再做內容匯入，最後才公開發布。

匯入時應只選這 61 份內容，避免把其他批次一起匯入。`review-bundle.zip` 中的 `content/` 是此系列專用目錄；`web-public/` 中的素材需放到相應公開路徑。先解壓並確認路徑，再依既有 `guides-import` 使用有效管理員及 dry-run。下列是操作格式，**本次未執行**：

```text
python -m app.cli guides-import --actor-email <active-admin> --dir <series-content-directory> --locale zh-TW --dry-run
```

核對 dry-run 結果後，另依匯入授權建立草稿；公開發布需要其自己的授權與結果紀錄，不把移除 dry-run 或加入 publish 當成本次已批准的動作。匯入後依後台 preview 再核對當前資料庫版本、來源、圖片與導覽，公開後驗證真正網站與 sitemap。

內容 ZIP 不包含應用程式功能更新，不能只上傳內容就預期舊版 renderer 能認識新格式。部署、匯入、發布三個狀態應分別記錄，且保留當次 actor、來源版本與結果。
