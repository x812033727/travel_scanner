# Codex 學習中心：實作與維護

**60 篇五語深入稿已編譯，依 [深入教學計畫](depth-plan.md)與[作者模板](article-template.md)等待最終驗收。** 已對齊「規劃 Claude Code 教學目錄」的深度，保留五語、既有 ID／網址與截圖要求。現在有 60 筆目錄、十個單元、URL 篩選與先備導覽；沒有短稿或待寫空篇。正式深入驗收仍為 0/60，缺口與本輪證據見[製作進度](progress.md)。

本系列有一個總目錄與 60 篇獨立教學，每篇提供繁中、簡中、英文、日文、韓文，共 61 個內容包、305 份語言文件。路由為 `/{locale}/life/codex-learning-hub` 與既有 `/life/<slug>`。**沒有 push、PR、匯入、正式發布或部署**。使用者已授權全部完成且驗收後，再開 PR、合併與部署；完成前不提前交付部分 PR。

## 內容與發布來源

- [系列清單](../../apps/web/lib/codex-learning/catalog.json)：固定識別碼、排序、三批次、程度、平台、需求、指令別名、相關篇章及五語標題。目錄和篇尾導覽共用。
- [初版資料](lessons/)：原 32 篇的歷史基礎。深入作者稿已取代其正文，不可用舊生成器覆寫現行內容。
- [深入作者稿](deep/)：60 篇、300 份深入語言文件；55 份 modules 保存四語完整段落及單一份程式碼，由 render-authors.py 產生作者檔，其餘 5 篇代表稿維護四語 Markdown。只解析明確作者來源，簡中轉換保留 fenced code 原文。
- [內容包](../../apps/api/app/guides/content/)：生成的 61 個 `codex-*.json`，含總目錄共 305 份語言文件。既有入門、CLI、雲端 slug 保留。
- [實戰原始檔](examples/)：虛構網站、CSV、資料整理程式及測試。網站不含外部請求；CSV 使用 example.test 地址。
- [共用待辦網站](practice/)：獨立的 start、broken、expected、測試、技能與下載包。參考版支援新增、完成、刪除、篩選、儲存與錯誤處理。
- [驗證紀錄](evidence/)：本機瀏覽器及內容稽核結果，不能作為已上線證明。

`ready` 表示已有內容，不等於網站發布。入口、上一篇／下一篇、相關文章均查詢 API 的當前語言發布清單。共用系列 API 查詢各語言的已發布版本；失敗時不猜測發布狀態。正文涉及被撤回的系列文章時降為純文字。語言切換及 SEO 沿用既有公開版本機制。

## 重建

在儲存庫根目錄執行：

```powershell
python tools/codex-learning/prepare-practice.py
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/rebuild-depth.py
uv run --directory apps/api python ../../tools/codex-learning/audit.py
```

舊 `build.py` 已加保護，避免把深入作者稿及 60 筆目錄覆寫回初始 32 篇。新增課程時，在 `deep/planned.json` 維護五語標題與成果，在 depth-plan.md 保持穩定 ID／slug。rebuild-depth.py 依序產生作者檔、驗證並編譯、更新目錄與產生圖片，任一步失敗立即停止；需要已安裝相依套件的 apps/api/.venv 做正式 schema 驗證。`build-depth.py --check` 只檢查，不寫內容包；目錄以來源與內容包的 hash 確認深入稿已編譯。

生成器不存取資料庫。五語程式碼與區塊結構有獨立測試，避免翻譯改壞命令。60 篇分列閱讀與操作時間，內容包存在不等於正式公開。表格、清單及提示框的作者連結另生成可點擊的結構化引用，保留舊純文字格式；既有一般文字不自動解析為 Markdown。

完整性與來源網址可分別檢查：

```powershell
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/build-depth.py --check
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/render-authors.py --check
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/check-series.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-sources.py
```

全系列檢查比對每個作者連結、五語程式碼、圖片、來源及內容 hash；不代替翻譯與預覽驗收。來源網址檢查保留 HEAD／GET 回應，不能單憑狀態碼判定操作說明正確。

## 教材下載與參考檢查

待辦網站材料為 `/guides/codex-first-project/todo-practice.zip`；CSV 材料為 `/guides/codex-csv-workshop/contacts-practice.zip`。CSV 五檔含基本與 Unicode 輸入、整理程式、三項測試及五語使用說明，由 check-workshop-practice.py 產生可重現的 ZIP。

```powershell
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-session-plan-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-git-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-worktree-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-skill-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-mcp-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-subagent-reference.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-integration-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-exec-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-workshop-practice.py
```

九組共 74 項參考檢查。Git 使用暫存庫；MCP 使用獨立程序設定及官方公開文件服務。exec 模擬模型程序，CI 只在本機執行精確輸出驗證器；沒有呼叫付費模型、真正觸發 GitHub 工作流程或啟動教材中的插件、子代理與排程。精確範圍及未實測項目見各自 evidence JSON。

## 查證、圖片與限制

查證日為 **2026-09-14**。每篇記錄官方來源及 checked_on；[研究工具](../../tools/codex-learning/research.py) 從作者資料列舉官方 Markdown，儲存於未提交的 `.codex/codex-learning-research/`。主要查證入口：

- [桌面版](https://learn.chatgpt.com/docs/app)、[Windows](https://learn.chatgpt.com/docs/windows/windows-app)、[Linux 預覽](https://learn.chatgpt.com/docs/linux/linux-app)：產品名稱、下載與平台限制。
- [Remote](https://learn.chatgpt.com/docs/remote)：iOS／Android 的遠端入口、主機必須可用；不能把手機當作可直接讀取任意電腦檔案的本機 CLI。
- [CLI 指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)、[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)：依介面區分指令及規則層級。
- [登入](https://learn.chatgpt.com/docs/auth)、[方案](https://learn.chatgpt.com/docs/pricing)、[模型](https://learn.chatgpt.com/docs/models)：變動資訊集中於 02／17，不在多篇硬寫價格、額度或模型排行榜。

所有 SVG 與封面是本系列原創示意圖，署名 Mokaair；不冒充產品畫面。部分操作篇附 Windows／Edge 的實際練習頁截圖，五語圖說標記日期、版本與模擬畫面寬度。沒有使用第三方授權不明圖片或私人帳號畫面。跨平台操作依官方文件查證；**未完成 macOS、Linux、iOS、Android 實機操作驗證，也沒有 Codex 桌面／手機真實介面截圖**。圖中的操作順序與步驟文字對照；手機寬度截圖不等同手機實測。

## 可重現的本機整頁驗證

**本節為重現說明，目前最終驗收尚未執行。** 本任務的 Next 預覽啟動被自動核准審查拒絕，限制為只監聽本機後仍回覆 `blocked by policy`，未提供具體原因。沒有改用其他啟動方式繞過；既有 fixture 是舊快照，不能用來證明最終 60 篇通過。

在第一個終端機啟動僅限 localhost 的唯讀假發布 API：

```powershell
apps/api/.venv/Scripts/python.exe tools/codex-learning/preview_api.py
```

在第二個終端機啟動網站，不修改 `.env`：

```powershell
$env:API_INTERNAL_URL = 'http://127.0.0.1:8123'
npm run build:web
npm run start --workspace @travel-scanner/web -- --port 3123
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

`preview_api.py` 的 published 回應僅是本機 UI 測試資料，不可接到正式網站；內容包更新後需重新啟動 fixture。深度瀏覽器檢查涵蓋五語、360／390／1280px、60 筆目錄及 60 條測試文章連結、URL 篩選重新整理與返回、已編入目錄的全部深入稿、複製、語言連結及整頁橫向溢出。測試依目錄自動選入新稿。增量檢查可用 `--slugs codex-cloud-tasks-github,codex-cross-device-workflow --report depth-browser-cloud-batch.json`；每份報告保存自己的範圍，不把前一批通過數當成後一批驗收。Windows 剪貼簿會將 LF 轉為 CRLF，因此讀回時只正規化該換行；渲染文字與 writeText 的輸入仍逐字核對。

## 初版歷史驗證與後續發布

2026-09-14 驗證結果：前端原有及受影響頁面 485 項通過；後续新增發布分頁與後台編輯測試的集中測試 30 項通過。API／內容包 37 項通過、5 項資料庫測試略過。CSV 範例 3 項通過。ESLint、TypeScript、正式建置、API Ruff／Mypy、多語檢查與工具測試 28 項通過。內容稽核零錯誤、143 個警告：133 個正文長度、目錄五語各一個「無正文示意圖」及「無靜態內部連結」；目錄的圖片與連結實際由封面及互動目錄提供。詳見保存的 JSON，沒有將警告隱藏或修改既有檢查門檻。

以上是原 32 篇草稿基礎的歷史檢查；新製作順序是 60 篇、三批各 20 篇、每十篇檢查。本輪結果以 progress.md 與最新 JSON 為準，不能把歷史通過數當成新稿完整驗收。未實測平台與介面截圖缺口持續保留。既有 AI 第四批任務的 CLI／雲端兩篇已移交此任務，其餘篇章未改動。

依本輪「全部完成後再開 PR 部署」授權，後續順序為：全套內容與功能驗收 → 開 PR、確認 CI 與合併 → 匯入並核對五語內容 → 正式發布與部署 → 公開網址驗證。每步記錄實際結果，前一步完成不代表後一步已執行。

共用系統已於本機整合：checkpoint 5f5b0b11 後，以 7abe6057 將 main 3b8df68c693eb81ccde7793a2f89d71999dbb2c2 合入本分支，包含 Claude 系列 PR #485 的能力。新版使用 inlines／article 引用與 code label；build-series.py 由前端唯一課程資料生成五語 API 目錄。這不是本系列已合入 main。

最新 60 篇快照：168 項受影響前端、9 項編譯器、59 項 API／系列／內容包及 39 項工具測試通過；18 項依賴 PostgreSQL 的案例略過。全站 ESLint、TypeScript／正式建置、API Ruff／Mypy、多語與任務檢查通過。內容稽核 0 錯誤、24 個篇幅與集合頁編輯提示；完整範圍及尚未完成的瀏覽器與圖文驗收見 progress.md。
