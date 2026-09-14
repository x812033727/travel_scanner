# Codex 學習中心：實作與維護

**目前依 [60 篇深入教學](depth-plan.md)與[作者模板](article-template.md)實作中。** 依使用者要求對齊「規劃 Claude Code 教學目錄」的深度，保留五語、既有 ID／網址與截圖要求。現在已有 60 筆目錄、十個單元、URL 篩選與先備導覽；37 篇已有五語深化稿，18 篇仍是短篇草稿、16 篇規劃中。正式深入驗收仍為 0/60，缺口與本輪證據見[製作進度](progress.md)。

本系列規劃一個總目錄與 60 篇獨立教學，每篇提供繁中、簡中、英文、日文、韓文。現有 48 個內容包共 240 份語言文件；16 篇規劃項目沒有空白內容包。路由為 `/{locale}/life/codex-learning-hub` 與既有 `/life/<slug>`。**沒有執行匯入、正式發布或部署**。使用者最新授權為全部完成且驗收後，再開 PR、合併與部署；完成前不提前交付部分 PR。

## 內容與發布來源

- [系列清單](../../apps/web/lib/codex-learning/catalog.json)：固定識別碼、排序、三批次、程度、平台、需求、指令別名、相關篇章及五語標題。目錄和篇尾導覽共用。
- [作者資料](lessons/)：01–32 的各語言操作步驟、範例、預期結果、問題排除、官方來源。簡中由繁中以固定版本 OpenCC 轉換，生成後的五語 JSON 可獨立審核。
- [深入作者稿](deep/)：閱讀順序前 25 篇及 Skills 代表稿，共 37 篇完整 Markdown；新稿於 modules 保存四語完整段落及單一份程式碼，由 render-authors.py 產生作者檔。只對明確作者來源解析 Markdown，簡中轉換保留 fenced code 原文。
- [內容包](../../apps/api/app/guides/content/)：生成的 45 個 `codex-*.json`，共 240 份語言文件。既有入門、CLI、雲端 slug 保留。
- [實戰原始檔](examples/)：虛構網站、CSV、資料整理程式及測試。網站不含外部請求；CSV 使用 example.test 地址。
- [共用待辦網站](practice/)：獨立的 start、broken、expected、測試、技能與下載包。參考版支援新增、完成、刪除、篩選、儲存與錯誤處理。
- [驗證紀錄](evidence/)：本機瀏覽器及內容稽核結果，不能作為已上線證明。

`ready` 表示已有內容，不等於網站發布。入口、上一篇／下一篇、相關文章均查詢 API 的當前語言發布清單。清單支援分頁；中途失敗時不猜測發布狀態。正文涉及被撤回的系列文章時降為純文字。語言切換及 SEO 沿用既有公開版本機制。

## 重建

在儲存庫根目錄執行：

```powershell
python tools/codex-learning/prepare-practice.py
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/rebuild-depth.py
uv run --directory apps/api python ../../tools/codex-learning/audit.py
```

舊 `build.py` 已加保護，避免把深入作者稿及 60 筆目錄覆寫回初始 32 篇。新增課程時，在 `deep/planned.json` 維護五語標題與成果，在 depth-plan.md 保持穩定 ID／slug。rebuild-depth.py 依序產生作者檔、驗證並編譯、更新目錄與產生圖片，任一步失敗立即停止；需要已安裝相依套件的 apps/api/.venv 做正式 schema 驗證。`build-depth.py --check` 只檢查，不寫內容包；目錄以來源與內容包的 hash 確認深入稿已編譯。

生成器不存取資料庫。五語程式碼與區塊結構有獨立測試，避免翻譯改壞命令。代表篇分列閱讀與操作時間；舊短篇仍保留初版估計，待深化時更新。後台公開內容仍是讀者看到的正式版本。

## 查證、圖片與限制

查證日為 **2026-09-14**。每篇記錄官方來源及 checked_on；[研究工具](../../tools/codex-learning/research.py) 從作者資料列舉官方 Markdown，儲存於未提交的 `.codex/codex-learning-research/`。主要查證入口：

- [桌面版](https://learn.chatgpt.com/docs/app)、[Windows](https://learn.chatgpt.com/docs/windows/windows-app)、[Linux 預覽](https://learn.chatgpt.com/docs/linux/linux-app)：產品名稱、下載與平台限制。
- [Remote](https://learn.chatgpt.com/docs/remote)：iOS／Android 的遠端入口、主機必須可用；不能把手機當作可直接讀取任意電腦檔案的本機 CLI。
- [CLI 指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)、[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)：依介面區分指令及規則層級。
- [登入](https://learn.chatgpt.com/docs/auth)、[方案](https://learn.chatgpt.com/docs/pricing)、[模型](https://learn.chatgpt.com/docs/models)：變動資訊集中於 02／17，不在多篇硬寫價格、額度或模型排行榜。

所有 SVG 與封面是本系列原創示意圖，署名 Mokaair；不冒充產品畫面。37 篇附 Windows／Edge 的實際練習頁截圖，五語圖說標記日期、版本與模擬畫面宽度。沒有使用第三方授權不明圖片或私人帳號畫面。跨平台操作依官方文件查證；**未完成 macOS、Linux、iOS、Android 實機操作驗證，也沒有 Codex 桌面／手機真實介面截圖**。圖中的操作順序與步驟文字對照；手機寬度截圖不等同手機實測。

## 可重現的本機整頁驗證

在第一個終端機啟動僅限 localhost 的唯讀假發布 API：

```powershell
apps/api/.venv/Scripts/python.exe tools/codex-learning/preview_api.py
```

在第二個終端機啟動網站，不修改 `.env`：

```powershell
$env:API_INTERNAL_URL = 'http://127.0.0.1:8123'
npm run dev --workspace @travel-scanner/web -- --port 3123
```

在第三個終端機執行（需要 Windows Edge）：

```powershell
node tools/codex-learning/browser-check.mjs
node tools/codex-learning/depth-browser.mjs
node tools/codex-learning/practice-browser.mjs
node --test docs/codex-learning/practice/expected/core.test.mjs
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python -m unittest discover -s tools/codex-learning -p test_compiler.py
apps/api/.venv/Scripts/python.exe -m unittest discover -s docs/codex-learning/examples -v
```

`preview_api.py` 的 published 回應僅是本機 UI 測試資料，不可接到正式網站；內容包更新後需重新啟動 fixture。深度瀏覽器檢查涵蓋五語、360／390／1280px、60 筆目錄及目前 44 條測試文章連結、URL 篩選重新整理與返回、已編入目錄的全部深入稿、複製、語言連結及整頁橫向溢出。測試依目錄自動選入新稿。增量檢查可用 `--slugs codex-cloud-tasks-github,codex-cross-device-workflow --report depth-browser-cloud-batch.json`；每份報告保存自己的範圍，不把前一批通過數當成後一批驗收。Windows 剪貼簿會將 LF 轉為 CRLF，因此讀回時只正規化該換行；渲染文字與 writeText 的輸入仍逐字核對。

## 初版歷史驗證與後續發布

2026-09-14 驗證結果：前端原有及受影響頁面 485 項通過；後续新增發布分頁與後台編輯測試的集中測試 30 項通過。API／內容包 37 項通過、5 項資料庫測試略過。CSV 範例 3 項通過。ESLint、TypeScript、正式建置、API Ruff／Mypy、多語檢查與工具測試 28 項通過。內容稽核零錯誤、143 個警告：133 個正文長度、目錄五語各一個「無正文示意圖」及「無靜態內部連結」；目錄的圖片與連結實際由封面及互動目錄提供。詳見保存的 JSON，沒有將警告隱藏或修改既有檢查門檻。

以上是原 32 篇草稿基礎的歷史檢查；新製作順序是 60 篇、三批各 20 篇、每十篇檢查。本輪結果以 progress.md 與最新 JSON 為準，不能把歷史通過數當成新稿完整驗收。未實測平台與介面截圖缺口持續保留。既有 AI 第四批任務的 CLI／雲端兩篇已移交此任務，其餘篇章未改動。

依本輪「全部完成後再開 PR 部署」授權，後續順序為：全套內容與功能驗收 → 開 PR、確認 CI 與合併 → 匯入並核對五語內容 → 正式發布與部署 → 公開網址驗證。每步記錄實際結果，前一步完成不代表後一步已執行。
