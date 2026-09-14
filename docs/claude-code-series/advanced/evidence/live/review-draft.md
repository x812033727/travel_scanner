在既有 Claude Code 教學中心新增 36 篇深入教學，系列擴充為 96 篇加總目錄，共 97 頁。目錄、搜尋別名、12 條學習路線、前後篇與內文引用統一更新；提供 36 個獨立練習 ZIP、6 組合集及 43 組新增／更新內容包和圖解。

練習涵蓋規則、Skills、Hooks、MCP、協作、自動化與完整待辦網站。SDK runner 改用串流輸入，讓 Ctrl+C 取消與中斷 session 接續可實際驗證。加入僅手動觸發、預設不呼叫模型的 GitHub Actions 驗證流程。

驗證紀錄包含 97 頁內容零錯誤／警告、36 ZIP 的 81 項檢查、六個試作包各 21 項工具測試、真實 CLI 主流程與邊界案例、SDK 取消／恢復、兩位 Teams 隊友、一次性排程及實際模型製作的待辦網站。先前 Windows 2,809 項前端與隔離 PostgreSQL／SQLite 164 項通過的紀錄保留為歷史快照；同步 main 後另跑目前環境檢查，最終狀態以本 PR 的 CI 為準。

實體手機、遠端 MCP OAuth、支援平台 Bash sandbox、完整 Teams 功能整合和付費 Actions 模型工作仍有待驗證範圍，逐項列於 tasks/open/2026-09-14-claude-advanced-live-validation.md。claude-lab 已建立並限制 main，但尚無 ANTHROPIC_API_KEY。本 PR 不執行正式部署、資料庫匯入或公開發布。
