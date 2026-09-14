# Claude Code 第二階段：PR 審查材料

在原有 60 篇入門教學上新增 36 篇深入教學，涵蓋分層規則、Skills、Hooks、自建 MCP、開發協作與可靠自動化。讀者可從同一個總目錄搜尋、選擇學習路線、跳轉先備與相關文章，並下載每篇獨立練習材料。

本批交付 96 篇教學加 1 個總目錄、36 份獨立 ZIP 與六組合集；新增 36 篇及總目錄、六篇既有文章的內容包與圖片共 43 組。既有五條路線保留，新增七條深入路線。預覽沿用網站呈現元件，發布狀態仍由正式服務過濾。

## 已完成的驗證

- Windows 前端全套：258 個測試檔、2,809 項通過，0 項跳過。
- 獨立 PostgreSQL 17.11 與 SQLite：164 項通過，0 項跳過；臨時資料庫已停止，測試 schema 已清空。
- 97 頁內容重驗：缺頁、錯誤、警告均為 0；系列工具加入儲存庫 workflow 檢查後 12 項通過。
- 既有本批紀錄包含 36 份 ZIP 的 81 項檢查、六篇各 21 個工具測試、9 類瀏覽器驗收，以及 build、lint、typecheck、i18n、Ruff 和 mypy。
- 2,761 個來源檔雜湊與測試快照一致。WSL 備援測試在 Windows 全套通過後停止，不宣稱 Linux 全套通過。
- 內建瀏覽器完成既有 CLI 重新授權；61、67、73、79、91 五個主流程通過，並保存真正的 PostToolUse/Read 事件。
- 使用者指定 travel_scanner 的雲端任務實際執行 Node.js，結果正確，Changes 顯示 No changes to show。
- 七個 CLI 邊界案例通過：子目錄規則、Skill 缺參數／自動選用、權限拒絕、Hook 拒絕 Write、MCP 啟動失敗及只讀子代理。初次 Hook 誤歸因與子代理超時保存為失敗歷史。
- SDK 0.3.270 原 runner 的 query、同一 session resume、缺少／無效狀態拒絕、啟動失敗及全新 query 恢復通過；另建串流輸入探針驗證 AbortController 取消。原 runner 的實體 Ctrl+C 與中斷 session 恢復仍待測。
- 儲存庫專用手動 GitHub workflow 已備妥，預設不呼叫模型；其 8 項基礎測試本機通過。遠端尚未執行。
- 工具全套重驗 52 項通過；初次缺少 Action 版本註記造成的失敗已修正並保存結果。
- 第 96 篇已實際由 Claude 從 starter 完成篩選、UI 與保存：9 項專案測試、3 項獨立斷言、10 項內建瀏覽器案例、指定故障紅綠與乾淨 ZIP 重驗通過。[實際成果](capstone-result.zip)附驗收者更正的一句 handoff 說明；原始模型輸出另存。臨時伺服器已停止。

[本次原始結果與執行範圍](verification-summary.json) · [整批驗收紀錄](../delivery-checks.json) · [完整教學目錄](../../README.md)

## 審查與合併前仍需處理

CLI 登入問題已排除，最新實測見 [真實操作摘要](real-operations-summary.json)。真實手機、MCP OAuth、Agent Teams、外部 GitHub Actions、產品排程、更多故障情境與真實比較仍有明列待辦。Actions 已獲准使用 travel_scanner，已準備符合 monorepo 路徑的 workflow，但尚未合併／安裝，且仍缺 claude-lab 環境與 Anthropic CI 憑證；沒有將本機登入憑證移交 GitHub。[操作與驗證方式](../../github-actions-validation.md)已附於審查包。

這份文件是審查用說明，尚未建立第二階段 PR。測試對應目前工作目錄與基準提交 46298e2863e9c2c4d6776e9d58a821be683a4b32；合併前需同步最新 main，核對實際 PR head 的 CI。第一階段任務封存變更與 .codex/ 保持原狀。部署、資料庫匯入及公開發布尚未執行。

臨時 PostgreSQL 已停止。剩餘暫存目錄的刪除遭自動核准審查拒絕（blocked by policy），目前保留；詳見原始驗證紀錄的 cleanup_note。
