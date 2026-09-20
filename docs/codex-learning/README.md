# Codex 學習中心：實作與維護

**60 篇五語深入稿、五語總目錄與本機最終頁面驗收已於 2026-09-20 完成。** 系列對齊 Claude Code 教學中心的深度，保留既有 ID／網址，新增十單元、URL 篩選、指令索引、五語摘要與先備導覽；沒有短稿或待寫空篇。全文終審為 60/60，總目錄終審通過，修正紀錄見[最終編輯處置](evidence/final-editorial-resolution.json)。

逐篇補強使用[深入製作與驗收總目錄](deepening/README.md)：十份單元文件包含 60 篇獨立規格，每篇明列材料、操作、交付物、成功／失敗、還原與圖片需求，並連回作者稿及五語內容包。[共同驗收表](deepening/review-checklist.md)列出五篇代表稿及六組十篇的檢查順序；六組全文紀錄及缺漏的第三組證據均已補齊。

本系列有一個總目錄與 60 篇獨立教學，每篇提供繁中、簡中、英文、日文、韓文，共 61 個內容包、305 份語言文件。路由為 `/{locale}/life/codex-learning-hub` 與既有 `/life/<slug>`。本機 Edge 以 360／390／1280px 完成 920 筆整頁報告（915 項頁面驗收與 5 次明確記錄的首次取文重試），另有 12 項目錄／實戰頁檢查及 6 項練習資料復原檢查。PR、合併、正式匯入、部署與公開網址驗收仍是後續獨立步驟。

五篇代表稿與 A 至 J 十單元已完成定向補強及全文終審。先前被標為 changes-required 的 03、06、20、25–29、50–52、54 與總目錄已依精確問題修正；全文第三組證據亦已建立。現階段只等待整套 PR、CI、合併、正式內容發布、部署及公開頁面驗收。

## 內容與發布來源

接下來依[收尾進度安排](final-review-schedule.md)執行：五篇代表稿全文終審、六組檢查、產品證據與總目錄、最終整合驗收，全部通過才進入 PR 與部署。進度起點與 21 項待處置提示見[盤點紀錄](evidence/final-review-intake.json)，不把盤點或定向補強計成全文通過。

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

只重打包現有待辦練習材料時，執行 `apps/api/.venv/Scripts/python.exe tools/codex-learning/practice_archive.py`。這個工具不改寫練習來源，會以固定檔案排序、時間及 LF 換行更新 ZIP 與 `practice/manifest.json`；Windows 的 CRLF checkout 也會得到相同內容。`prepare-practice.py` 會重新產生 start／broken 變體，僅更新下載包時應使用前述打包工具。

```powershell
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-session-plan-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-git-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-worktree-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-skill-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-mcp-practice.py --codex (Get-Command codex).Source
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-subagent-reference.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-integration-practice.py
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-exec-practice.py --codex (Get-Command codex).Source
apps/api/.venv/Scripts/python.exe tools/codex-learning/check-workshop-practice.py
```

九組共 94 項參考檢查。Git 使用暫存庫；MCP 使用獨立程序設定及官方公開文件服務。exec 模擬模型程序，CI 只在本機執行精確輸出驗證器；沒有呼叫付費模型、真正觸發 GitHub 工作流程或啟動教材中的插件、子代理與排程。精確範圍及未實測項目見各自 evidence JSON。

## 查證、圖片與限制

本次變更篇章與總目錄的查證日為 **2026-09-20**；其他未變更篇章保留各自最後查證日。每篇記錄官方來源及 checked_on；[研究工具](../../tools/codex-learning/research.py) 從作者資料列舉官方 Markdown，儲存於未提交的 `.codex/codex-learning-research/`。主要查證入口：

- [桌面版](https://learn.chatgpt.com/docs/app)、[Windows](https://learn.chatgpt.com/docs/windows/windows-app)、[Linux](https://learn.chatgpt.com/docs/linux/linux-app)：產品名稱、下載與平台限制。
- [Remote](https://learn.chatgpt.com/docs/remote)：iOS／Android 的遠端入口、主機必須可用；不能把手機當作可直接讀取任意電腦檔案的本機 CLI。
- [CLI 指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)、[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)：依介面區分指令及規則層級。
- [登入](https://learn.chatgpt.com/docs/auth)、[方案](https://learn.chatgpt.com/docs/pricing)、[模型](https://learn.chatgpt.com/docs/models)：變動資訊集中於 02／17，不在多篇硬寫價格、額度或模型排行榜。

所有 SVG 與封面是本系列原創示意圖，署名 Mokaair；不冒充產品畫面。部分操作篇附 Windows／Edge 的實際練習頁截圖，五語圖說標記日期、版本與模擬畫面寬度。沒有使用第三方授權不明圖片或私人帳號畫面。跨平台操作依官方文件查證；**未完成 macOS、Linux、iOS、Android 實機操作驗證，也沒有 Codex 桌面／手機真實介面截圖**。圖中的操作順序與步驟文字對照；手機寬度截圖不等同手機實測。

## 可重現的本機整頁驗證

**2026-09-20 已依本節重現並通過。** 使用正式 Next production build 與只綁定 localhost 的假發布 API；假 API 僅提供公開狀態，不接觸資料庫或正式服務。完整報告見 `browser-check.json`、`depth-browser.json` 與 `practice-browser.json`。

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
uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python -m unittest discover -s tools/codex-learning -p 'test_*.py'
apps/api/.venv/Scripts/python.exe -m unittest discover -s docs/codex-learning/examples -v
```

`preview_api.py` 的 published 回應僅是本機 UI 測試資料，不可接到正式網站；內容包更新後需重新啟動 fixture。深度瀏覽器檢查涵蓋五語、360／390／1280px、60 筆目錄及 60 條測試文章連結、URL 篩選重新整理與返回、已編入目錄的全部深入稿、複製、語言連結及整頁橫向溢出。測試依目錄自動選入新稿。增量檢查可用 `--slugs codex-cloud-tasks-github,codex-cross-device-workflow --report depth-browser-cloud-batch.json`；每份報告保存自己的範圍，不把前一批通過數當成後一批驗收。Windows 剪貼簿會將 LF 轉為 CRLF，因此讀回時只正規化該換行；渲染文字與 writeText 的輸入仍逐字核對。

## 初版歷史驗證與後續發布

2026-09-14 驗證結果：前端原有及受影響頁面 485 項通過；後续新增發布分頁與後台編輯測試的集中測試 30 項通過。API／內容包 37 項通過、5 項資料庫測試略過。CSV 範例 3 項通過。ESLint、TypeScript、正式建置、API Ruff／Mypy、多語檢查與工具測試 28 項通過。內容稽核零錯誤、143 個警告：133 個正文長度、目錄五語各一個「無正文示意圖」及「無靜態內部連結」；目錄的圖片與連結實際由封面及互動目錄提供。詳見保存的 JSON，沒有將警告隱藏或修改既有檢查門檻。

以上是原 32 篇草稿基礎的歷史檢查；新製作順序是 60 篇、三批各 20 篇、每十篇檢查。本輪結果以 progress.md 與最新 JSON 為準，不能把歷史通過數當成新稿完整驗收。未實測平台與介面截圖缺口持續保留。既有 AI 第四批任務的 CLI／雲端兩篇已移交此任務，其餘篇章未改動。

依本輪「全部完成後再開 PR 部署」授權，後續順序為：全套內容與功能驗收 → 開 PR、確認 CI 與合併 → 匯入並核對五語內容 → 正式發布與部署 → 公開網址驗證。每步記錄實際結果，前一步完成不代表後一步已執行。

共用系統已於本機整合：checkpoint 5f5b0b11 後，以 7abe6057 將 main 3b8df68c693eb81ccde7793a2f89d71999dbb2c2 合入本分支，包含 Claude 系列 PR #485 的能力。新版使用 inlines／article 引用與 code label；build-series.py 由前端唯一課程資料生成五語 API 目錄。這不是本系列已合入 main。

最新本機快照：60 篇／300 份文章文件及 61 個內容包通過 schema、連結、圖片、五語程式碼與來源檢查；每份文件新增兩至五句、取自既有內容的五語摘要。內容稽核 0 錯誤、27 項提示：22 項為深入英文篇幅或總目錄短於一般文章建議，5 項為專用目錄沒有正文 SVG；門檻未調低，互動目錄及封面仍另行驗收。最終 CI 數字以 PR 為準。
