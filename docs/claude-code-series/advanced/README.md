# Claude Code 深入教學：第二階段交付

新增 **36 篇完整教學（61–96）、36 份獨立練習包、六組合集**，整合到同一個 Claude Code 教學目錄。全系列現在有 **96 篇教學加 1 個總目錄，共 97 頁**。內容與本機預覽已製作；Claude 帳號及外部環境的實測仍有待辦，狀態見下表。

[第一階段紀錄](../README.md) · [作者任務書](lesson-briefs.md) · [編輯清單](curriculum.json) · [來源與驗證界線](source-review.md) · [本次驗收紀錄](evidence/delivery-checks.json) · [逐篇驗證表](evidence/lesson-verification.json)

本批沿用繁體中文、生活分享、AI／教學主題與原有文章格式。網址沒有加入篇號，舊篇網址保留。正式部署、資料庫匯入與公開發布均未執行。

## 開啟 97 頁預覽

在儲存庫根目錄執行；需要 Node.js 22 以上與已安裝的網站依賴：

```powershell
npm run build:web
node --experimental-strip-types tools/claude-code-series/preview.mjs
```

開啟命令印出的 `/zh-TW/life/claude-code-tutorials` 網址。預覽使用真正的 Next.js 公開呈現元件與本機唯讀資料服務，將全部內容包視為可閱讀，不更動任何資料庫發布狀態。按 Ctrl+C 停止本次預覽；修改內容後重啟，修改網站程式後重新建置。

目錄支援主題、程度、平台和推薦路線，搜尋與篩選保存在網址。每篇包含章節目錄、先備連結、內文交叉引用及上一篇／回目錄／下一篇。新增七條深入路線，原有五條路線保留；公開服務仍依目前語系與發布狀態過濾。

## 36 篇完整內容

下列連結直接開啟文章原稿；網站格式的 `article:` 引用由內容包與公開解析器轉成對應網址，可在上述預覽檢查。一般篇正文約 2,500–2,700 字，綜合實作約 4,000 字，程式碼另計。

| 完整教學 | 學習成果 | 獨立材料 |
|---|---|---|
| [61．替真實專案設計 CLAUDE.md](../lessons/61.md) | 把模糊、過期或重複的規則改成可操作的專案說明 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-61.zip) |
| [62．Monorepo 的分層 MD 與路徑規則](../lessons/62.md) | 讓前端、API 與共用目錄使用適合的指引 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-62.zip) |
| [63．Claude 沒照 MD 做：找出載入與規則衝突](../lessons/63.md) | 分辨沒有載入、規則矛盾、資料過期與任務描述不足 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-63.zip) |
| [64．權限與 Sandbox 邊界實驗](../lessons/64.md) | 用無害案例觀察允許、詢問、拒絕與執行隔離 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-64.zip) |
| [65．長任務的上下文整理與交接文件](../lessons/65.md) | 讓新的工作階段依檔案接手，而不依賴原對話 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-65.zip) |
| [66．把個人設定整理成團隊可維護的設定包](../lessons/66.md) | 建立共用範本、個人覆寫與更新檢查方式 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-66.zip) |
| [67．把一套工作 SOP 做成可重用 Skill](../lessons/67.md) | 將程式碼審查流程做成有輸入、輸出及停止條件的技能 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-67.zip) |
| [68．Skill 參數驗證：缺值、錯誤與危險字元](../lessons/68.md) | 讓技能接收可預期的參數並安全交給輔助程式 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-68.zip) |
| [69．拆分大型 Skill 的範本、參考文件與腳本](../lessons/69.md) | 建立能按需讀取的技能目錄 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-69.zip) |
| [70．Skill 何時啟動：手動呼叫與自動選用](../lessons/70.md) | 用正反例評估描述與呼叫設定 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-70.zip) |
| [71．替 Skills 建立回歸案例與評分表](../lessons/71.md) | 讓 Skill 修改後有可比較的品質紀錄 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-71.zip) |
| [72．把 Skills 與 Hooks 包成可版本管理的 Plugin](../lessons/72.md) | 讓同伴安裝、升級與回退同一套工作流程 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-72.zip) |
| [73．讀懂 Hook 事件：輸入、輸出與退出碼](../lessons/73.md) | 建立可重播事件的本機測試工具 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-73.zip) |
| [74．只處理變更檔案的格式化 Hook](../lessons/74.md) | 限制格式化範圍並避免事件重複執行 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-74.zip) |
| [75．建立可停止的品質檢查 Hook](../lessons/75.md) | 讓完成檢查能指出失敗並有清楚的退出機制 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-75.zip) |
| [76．用 Hook 保護指定檔案並測試路徑邊界](../lessons/76.md) | 為特定編輯工具設置範圍檢查及清楚的拒絕訊息 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-76.zip) |
| [77．任務通知與事件紀錄：有用而不洗版](../lessons/77.md) | 產生可追查、去重且不含敏感內容的通知紀錄 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-77.zip) |
| [78．跨平台 Hooks：中文路徑、逾時與遞迴排錯](../lessons/78.md) | 把 Hook 做成可測試、可停用、可移植的工具 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-78.zip) |
| [79．建立自己的唯讀 MCP 工具](../lessons/79.md) | 讓 Claude 查詢本機練習待辦資料 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-79.zip) |
| [80．設計 MCP 工具名稱、輸入 Schema 與分頁](../lessons/80.md) | 讓模型能選對工具，也能正確處理空值與大量結果 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-80.zip) |
| [81．遠端 MCP 登入、授權範圍與重新認證](../lessons/81.md) | 在測試服務演練連線與權限故障 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-81.zip) |
| [82．MCP 排錯實驗室：斷線、逾時與格式錯誤](../lessons/82.md) | 用固定故障重現診斷及復原流程 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-82.zip) |
| [83．MCP 回傳含有指令時：資料與操作權限分開](../lessons/83.md) | 以無害的對抗案例測試工具資料處理 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-83.zip) |
| [84．從 Issue 到變更草稿：串起工具與程式碼](../lessons/84.md) | 完成需求讀取、計畫、測試與 PR 說明稿 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-84.zip) |
| [85．真正走完一次重現、失敗測試與修正](../lessons/85.md) | 定位跨資料層及介面層的待辦狀態錯誤 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-85.zip) |
| [86．接手缺測試舊專案：先留住行為再重構](../lessons/86.md) | 用小步變更拆出可測試模組 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-86.zip) |
| [87．讓 Subagent 提出可核對的審查發現](../lessons/87.md) | 設計專責代理的範圍、工具及回報格式 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-87.zip) |
| [88．雙 Worktree 實作與衝突整合](../lessons/88.md) | 隔離兩項功能，最後完成整合與回歸 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-88.zip) |
| [89．Agent Teams 的分工、阻塞與成果整合](../lessons/89.md) | 比較單代理、專責代理與團隊協作成本 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-89.zip) |
| [90．桌面到手機：離線、中斷與返回工作現場](../lessons/90.md) | 確認執行位置，練習接續及故障後的核對 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-90.zip) |
| [91．把 claude -p 接進有驗證的 JSON 流程](../lessons/91.md) | 處理合法結果、錯誤、逾時與不完整輸出 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-91.zip) |
| [92．CI 審查助手：權限、fork 與結果附件](../lessons/92.md) | 在測試儲存庫跑一次可審閱的工作流程 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-92.zip) |
| [93．排程失敗怎麼辦：重複執行、漏跑與停止](../lessons/93.md) | 為一次排程建立可追查且不重複寫入的工作 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-93.zip) |
| [94．Agent SDK：保存狀態、取消與重新接續](../lessons/94.md) | 建立可中斷且可診斷的最小代理程式 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-94.zip) |
| [95．比較流程品質、用量與執行時間](../lessons/95.md) | 以同一資料集比較兩種工作方法 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-95.zip) |
| [96．期末實作：可維護的待辦專案工作流程](../lessons/96.md) | 整合規則、技能、工具及驗證，交付一次完整變更 | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-96.zip) |

## 推薦路線

- **MD 與專案規則**：[61](../lessons/61.md) → [62](../lessons/62.md) → [63](../lessons/63.md) → [65](../lessons/65.md) → [66](../lessons/66.md)
- **Skills 與自訂指令**：[67](../lessons/67.md) → [68](../lessons/68.md) → [69](../lessons/69.md) → [70](../lessons/70.md) → [71](../lessons/71.md) → [72](../lessons/72.md)
- **Hooks 與檢查流程**：[73](../lessons/73.md) → [74](../lessons/74.md) → [75](../lessons/75.md) → [76](../lessons/76.md) → [77](../lessons/77.md) → [78](../lessons/78.md)
- **自建 MCP 工具**：[79](../lessons/79.md) → [80](../lessons/80.md) → [81](../lessons/81.md) → [82](../lessons/82.md) → [83](../lessons/83.md) → [84](../lessons/84.md)
- **完整開發與協作**：[85](../lessons/85.md) → [86](../lessons/86.md) → [87](../lessons/87.md) → [88](../lessons/88.md) → [89](../lessons/89.md) → [96](../lessons/96.md)
- **桌面與手機接續**：[65](../lessons/65.md) → [90](../lessons/90.md)
- **CLI 與可靠自動化**：[91](../lessons/91.md) → [92](../lessons/92.md) → [93](../lessons/93.md) → [94](../lessons/94.md) → [95](../lessons/95.md) → [96](../lessons/96.md)

各篇先備知識另列於文章開頭；推薦順序不取代真正的依賴條件。

## 六組合集

- [專案規則與工作上下文：config-lab](../../../apps/web/public/tutorials/claude-code/advanced/config-lab.zip)
- [Skills 工程化與共用外掛：skill-kit](../../../apps/web/public/tutorials/claude-code/advanced/skill-kit.zip)
- [Hooks 事件、檢查與故障處理：hook-lab](../../../apps/web/public/tutorials/claude-code/advanced/hook-lab.zip)
- [MCP 工具開發與串接：mcp-lab](../../../apps/web/public/tutorials/claude-code/advanced/mcp-lab.zip)
- [開發驗證、多代理與跨裝置：todo-workbench](../../../apps/web/public/tutorials/claude-code/advanced/todo-workbench.zip)
- [可追蹤、可恢復的自動化：automation-lab](../../../apps/web/public/tutorials/claude-code/advanced/automation-lab.zip)

每份 lesson ZIP 都有 README、文章、預期結果、停止／重新開始說明、starter 與 reference；fixtures 放在兩個專案裡。使用 Node.js 22 以上，核心測試不需要額外套件。MCP 材料附固定依賴與 lockfile，執行 `npm ci --ignore-scripts` 後可跑整套測試。Agent SDK 在 automation/sdk 另行安裝。

第 85 篇 starter 刻意含錯誤，核心測試預期失敗；reference 與相同回歸測試應通過。第 96 篇 reference 附完整待辦網站。參考檔案不是帳號、手機或外部服務已完成操作的證明。

## 驗證狀態

補驗：整站前端 258 個測試檔、2809 項通過。執行環境與原始結果見[補充驗收紀錄](evidence/live/verification-summary.json)；此前未完成的執行保留於歷史紀錄。

| 層級 | 證據／限制 |
|---|---|
| 文件核對 | 2026-09-14 核對 19 個官方來源；另核對 GitHub Action 固定提交的輸入契約 |
| 本機程式 | 模型、Skill 參數、Hook 固定事件、實際 MCP stdio、HTTP 假授權、故障與恢復案例；見下載測試紀錄 |
| Git | 在臨時儲存庫建立兩個 worktree、製造並解決衝突、重跑整合測試；沒有修改遠端儲存庫 |
| 網站 | 97 頁、導覽、篩選、手機寬度、原始內容複製、下載版綜合實作；見瀏覽器紀錄 |
| API | 隔離 PostgreSQL 17.11 與 SQLite：164 項通過、0 項跳過；包含發布狀態、文章版本與系列導覽 |
| SDK | 0.3.270 的原範例 query、同一 session resume 通過；另用串流輸入探針驗證 AbortController 取消。原 runner 另通過缺少／無效 session、執行檔啟動失敗及全新 query 恢復；實體 Ctrl+C 與中斷 session 恢復仍待測 |
| 雲端網頁 | 使用者指定 travel_scanner，實際 Node.js 計算通過；工具輸出與 No changes to show 均已在內建瀏覽器確認 |
| CLI 邊界案例 | 七項通過：子目錄規則、Skill 缺參數／自動選用、Read 權限拒絕、Hook 拒絕 Write、MCP 啟動失敗、只讀子代理。只涵蓋指定案例，不代表各功能所有情境 |
| Claude CLI | 2.1.233 已透過內建瀏覽器重新授權；61、67、73、79、91 的五個主流程全部通過，故障情境另列待辦 |
| 外部環境 | 真實 MCP OAuth、手機接續、Agent Teams、外部 GitHub Actions、產品排程與完整故障演練仍待實測 |
| GitHub Actions | [儲存庫驗證流程](../../../.github/workflows/claude-tutorial-validation.yml)已備妥；12 項系列測試與 8 項基礎測試通過。尚未合併或遠端執行；[設定與驗證步驟](github-actions-validation.md) |
| 第 96 篇實際開發 | Claude 從 starter 完成篩選、畫面與保存；9 項專案測試、3 項獨立斷言、10 個內建瀏覽器案例、故障紅綠與乾淨解壓重驗通過。[實際成果 ZIP](evidence/live/capstone-result.zip)；一處交接文字由驗收者更正，真實手機仍待測 |
| 發布 | 本批尚未開 PR、合併、部署、匯入或公開 |

[內容檢查](evidence/content-validation.json) · [封面與圖解檢查](evidence/art-validation.json) · [36 包核心測試](evidence/downloads-quick-tests.json) · [六篇試作完整工具測試](evidence/downloads-tests.json) · [瀏覽器結果與重驗紀錄](evidence/browser-verification.json) · [最新真實操作](evidence/live/real-operations-summary.json) · [首輪 OAuth 失敗歷史](evidence/claude-live-all.json)

## 重建與驗收

```powershell
python tools/claude-code-series/advanced/build.py
python tools/claude-code-series/advanced/verify-downloads.py --quick
python tools/claude-code-series/advanced/verify-downloads.py --only 61 67 73 79 88 91
node --test tools/claude-code-series.test.mjs
npx playwright test --config tools/claude-code-series/advanced/playwright.config.mjs
```

首次使用 Playwright 需安裝對應瀏覽器。build.py 只重建本批擁有的 43 組內容／圖片（總目錄、六篇舊文章與 36 篇新文章），不改寫第一階段其他文章或歷史驗收紀錄。第一階段的 validation.json 保留原意；本資料夾的 validation.json 也是先前「課程規劃一致性」紀錄，不能當作本次執行結果。

內容包保持未發布。後續先補真實環境驗證，再依網站既有的預覽、審查、匯入與發布流程逐步記錄結果。
