# Gemini 完整教學系列

本系列有一個總目錄和 50 篇繁體中文教學，使用既有生活分享文章系統。網址為 `/zh-TW/life/gemini-guide`。完成編寫、程式測試或本機瀏覽器驗收，都不代表正式站已部署或發布；正式發布紀錄另存於發布日誌。

## 維護來源

- `apps/web/lib/guide-series.json`：唯一的篇序、slug、分類、難度、平台、用途、關鍵字、先修、延伸、路線與指令定位清單。
- `lessons/00.md`：總目錄使用說明；`01.md`–`50.md`：完整原稿。
- `sources.json`：全部 51 頁的官方來源；查證日為 2026-09-14。
- `artwork.json`、`artwork.py`：51 組原創封面與教學圖解；不使用產品標誌、產品介面或假造的實測截圖。
- `examples/`：可下載、執行與測試的完整範例。文章直接嵌入這些程式，避免兩份副本失去同步。
- `build.py`：將原稿轉成既有 `ArticlePack` JSON，保留既有網址。
- `tools/gemini-series.mjs`：內容、連結與白名單發布檢查。

一般教學正文約 1,800–3,000 字；第 31 篇內建指令總表以查找完整性為優先。總目錄說明另計。價格與額度集中在第 02、49 篇維護。首批只發布 zh-TW。

## 查證邊界

裝置、Gems、Canvas、Deep Research、Live、Spark、Workspace、NotebookLM、搜尋及影音操作，依查證當日官方文件整理，並在正文標明使用條件；沒有宣稱所有帳號、手機與作業系統均經實機測試。

Gemini CLI 使用 0.59.0：由實際安裝套件的指令載入器列出 45 個內建名稱，記錄條件式功能與別名。記憶驗證直接使用該版 `MemoryContextManager`，涵蓋全域、專案、匯入、子目錄、去重、重新載入與信任範圍，不呼叫雲端模型。

API 範例使用 Python `google-genai==2.23.0`、Pydantic `2.12.5` 與 JavaScript `@google/genai@2.22.0`。以真實 SDK 加本機 HTTP 回應驗證序列化、解析及資料約束；未使用付費 Google API 金鑰，因此不把本機通過寫成雲端呼叫成功。第 27 篇是官方功能比較及可重做的同題測試方法，未捏造三家模型的得分或結果。

原始查證與驗證紀錄：`device-verification.json`、`core-verification.json`、`ecosystem-verification.json`、`cli-command-inventory.json`、`cli-memory-verification.json`、`example-verification.json`、`art-verification.json`。`visual-review/` 是 102 張圖的檢視聯絡表；`renders/` 為逐張 PNG。

## 重新產生與檢查

從專案根目錄執行；Windows 的 Python 路徑如下，其他平台使用相同環境的 Python。

```powershell
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py
node docs/gemini-series/render-art.mjs
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/contact-sheets.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/verify-examples.py
node tools/gemini-series.mjs check
node --test tools/gemini-series.test.mjs
```

原稿中的 `[[36|GEMINI.md]]` 會轉成具名正文連結；一般清單項目保持純文字，跨篇連結應放在段落。程式區塊的語言與檔名分開儲存，程式文字只顯示及複製，不執行。修改章節順序後必須檢查 catalogue 的 `section-N` 定位。

前端、後端、後台共同支援 `rich_paragraph.inlines` 與 `code`（`label` 儲存檔名或輸入位置），舊文章格式不變。連結沿用網址及合作連結驗證，不能靠巢狀連結繞過限制。文章存檔、重新開啟、發布與匯入使用既有 API。

瀏覽器整合測試先建置前端，再執行 `apps/web/e2e/gemini-series.spec.ts`。測試使用全部 51 份真實內容包、獨立 Next 生產模式伺服器與隔離 API fixture，並禁止瀏覽器連到外部站點。它驗證桌面、手機、360px 無 JavaScript、複製與發布入口條件；它不代表正式站驗收。

## 整套發布程序

1. 完成內容、來源、圖片、範例、型別、前後端、工具與任務檢查，保存驗收紀錄。檢查 Git 差異限定於已認領範圍。
2. 使用既有程式碼審查與部署流程，先讓正式環境具備新內容區塊、導覽及全部圖片。不要先發布會被舊版前端忽略的內容。
3. 在正式環境先執行下方 dry-run。僅使用 catalogue 的 51 個 slug，不匯入整個內容目錄。
4. 確認 dry-run 後執行 publish：工具重新 dry-run，逐篇匯入 50 篇子文章，每篇比對公開 API 的標題、摘要、封面、區塊與來源；再重新確認全部 50 篇，最後才發布總目錄。
5. 既有匯入每篇提交，任何錯誤即停止。檢查 JSONL 日誌中 `starting` 與 `verified` 的差異，核對已發布部分及草稿，再決定是否重跑。重跑沿用既有冪等匯入，不自動刪除文章或回滾其他編輯。
6. 最後在正式站以桌面與手機確認生活分享入口、總目錄、六組搜尋、章節定位、複製、所有子文章與 sitemap。此步完成後才能記錄「整套推出」。

```text
node tools/gemini-series.mjs dry-run --python <正式環境 Python>
node tools/gemini-series.mjs publish --python <正式環境 Python> --actor-email <管理員信箱> --api-origin http://127.0.0.1:8090 --journal <持久保存的 JSONL 路徑>
```

`--api-origin` 指向可匿名讀取指南的 FastAPI 服務；正式站的 `/api/` 由 Next BFF 接收，不能直接假設網站網域會轉送 `/api/v1/guides`。在主機上使用已確認的 localhost API 位址，逐篇比對後仍須另驗公開網站頁面。`reviewed-files.json` 記錄 Git 正規化後的 LF 位元組，應對照 release archive，不對照 Windows 的 CRLF 工作副本。

總目錄和生活分享入口由總目錄的已發布狀態控制。搜尋是互動增強；所有分類及文章連結在伺服器首次輸出的 HTML 中已存在。站內文章使用同一分頁；手機導覽與程式區塊在容器內換行或捲動。

## 與其他教學系列共存

主線另有 Claude Code 教學中心。共用正文、後台與 API 區塊採用既有 `inlines` / `label` 格式，Gemini 的 TOML 語言支援及換行處理一併納入；保留其文章引用及系列 API。Gemini 搜尋與導航讀取 `guide-series.json`，專用輔助函式位於 `apps/web/lib/gemini-series.ts`，避免與通用系列型別混淆。介面文案儲存在五語系 `common.geminiSeries`；本系列仍只開放 zh-TW 內容。

## 2026-09-14 正式推出

完整系列已上線：https://mokaair.com/zh-TW/life/gemini-guide 。PR #490 合併為 `4ba38e81cd48e2c3f8920b9dee1108b5cdba50d6`；該合併提交的 CI 全數通過後，驗證備份並啟用八個應用服務，既有 PostgreSQL / Redis 容器維持原樣。部署收據記錄所選資料表的核對雜湊，不代表每個動態資料表都停止變動。

51 頁 dry-run 通過：更新既有入門篇、新增其餘 50 頁。逐篇匯入並驗證全部子文章後才發布總目錄。最後一次總目錄讀回發生 Node fetch 錯誤，流程依設計停止；查明總目錄已成功寫入後，重新匿名讀取全部 51 頁、比對五個正文欄位，確認其他文章與所選設定資料未變，再補記最後的 verified 事件，沒有重複匯入。

正式站 Chromium 驗收於 2026-09-14 完成：50 篇各跑桌面與手機，共 100 個文章檢查；每種裝置測六組關鍵字、八個分類、五條路線、上一篇／下一篇、指令章節及四篇複製範例。360px 停用 JavaScript 仍能找到全部 50 篇並閱讀 MD 圖解。另逐一核對 102 張公開圖片的原始位元組，以及 sitemap 的 51 個唯一網址。來源連線檢查 127 個網址均成功。瀏覽器驗收排除廣告與分析流量，正文、圖片、程式碼和網站 API 都來自正式站。

證據：`acceptance.json`、`release-ci.json`、`deployment-receipt.json`、`publication.jsonl`、`publication-receipt.json`、`public-browser.json`、`public-assets.json`、`public-sitemap.json`、`source-links.json`，以及 `visual-review/public-*.png`。`verify-public-browser.cjs`、`verify-public-assets.py`、`verify-public-sitemap.py` 可從專案根目錄執行，僅執行公開頁面驗收，不發布文章。付費 Google API、所有真實裝置與三家助手 benchmark 的查證邊界仍依前文，正式站驗收不會改變這些邊界。
