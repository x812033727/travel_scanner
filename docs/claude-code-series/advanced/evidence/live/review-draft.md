在既有 Claude Code 教學中心新增 36 篇深入教學，系列擴充為 96 篇加總目錄，共 97 頁。目錄、搜尋別名、12 條學習路線、前後篇與內文引用統一更新；提供 36 個獨立練習 ZIP、6 組合集及 43 組新增／更新內容包和圖解。

練習涵蓋規則、Skills、Hooks、MCP、協作、自動化與完整待辦網站。SDK runner 改用串流輸入，讓 Ctrl+C 取消與中斷 session 接續可實際驗證。加入僅手動觸發、預設不呼叫模型的 GitHub Actions 驗證流程。

驗證紀錄包含 97 頁內容零錯誤／警告、36 ZIP 的 81 項檢查、六個試作包各 21 項工具測試、真實 CLI 主流程與邊界案例、SDK 取消／恢復、Teams 雙角色功能開發、阻塞決策、一次性排程及實際模型製作的待辦網站。先前 Windows 2,809 項前端與隔離 PostgreSQL／SQLite 164 項通過的紀錄保留為歷史快照；同步 main 後另跑目前環境檢查，最終狀態以本 PR 的 CI 為準。

實體手機、遠端 MCP OAuth和付費 Actions 模型工作仍有待驗證範圍，逐項列於 tasks/open/2026-09-14-claude-advanced-live-validation.md。claude-lab 已建立並限制 main，但尚無 ANTHROPIC_API_KEY。本 PR 不執行正式部署、資料庫匯入或公開發布。

CI 首輪發現下載包採 Windows CRLF、Git 原稿採 LF，造成 Linux 的一致性斷言失敗。封裝器現將文字統一為 LF、保留二進位位元組，42 ZIP 已重建；新增 Windows／Linux 等價輸入產生相同 ZIP 的回歸驗證，36 包與六份完整工具包重新實跑。探索頁首輪僅附件上傳 403，測試步驟通過，已安排失敗工作重跑。

WSL2 補驗：官方 CLI 2.1.270 的真實 Bash 完成專案內讀寫、指定檔案拒讀、外部寫入拒絕與主機 loopback 隔離。HTTP 在主機前後皆成功，外部檔案維持原樣；沒有放寬沙箱或宣稱網域／Unix socket 全面覆蓋。
