# 官方來源與驗證界線

[回第二階段總目錄](README.md)

製作時重新取得以下 19 個官方來源，保存日期、頁名、網址、狀態及 SHA-256；完整頁面僅作本機查閱，不附入教材。此清單是文件核對，不能證明真實帳號的操作成功。

| 官方來源 | 核對日期 | 證據類型 |
|---|---|---|
| [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) | 2026-09-14 | 文件核對 |
| [Work with sessions](https://code.claude.com/docs/en/agent-sdk/sessions) | 2026-09-14 | 文件核對 |
| [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) | 2026-09-14 | 文件核對 |
| [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | 2026-09-14 | 文件核對 |
| [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions) | 2026-09-14 | 文件核對 |
| [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) | 2026-09-14 | 文件核對 |
| [Hooks reference](https://code.claude.com/docs/en/hooks) | 2026-09-14 | 文件核對 |
| [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) | 2026-09-14 | 文件核對 |
| [How Claude remembers your project](https://code.claude.com/docs/en/memory) | 2026-09-14 | 文件核對 |
| [Configure permissions](https://code.claude.com/docs/en/permissions) | 2026-09-14 | 文件核對 |
| [Create plugins](https://code.claude.com/docs/en/plugins) | 2026-09-14 | 文件核對 |
| [Plugins reference](https://code.claude.com/docs/en/plugins-reference) | 2026-09-14 | 文件核對 |
| [Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control) | 2026-09-14 | 文件核對 |
| [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing) | 2026-09-14 | 文件核對 |
| [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) | 2026-09-14 | 文件核對 |
| [Extend Claude with skills](https://code.claude.com/docs/en/skills) | 2026-09-14 | 文件核對 |
| [Create custom subagents](https://code.claude.com/docs/en/sub-agents) | 2026-09-14 | 文件核對 |
| [or](https://github.com/modelcontextprotocol/typescript-sdk) | 2026-09-14 | 文件核對 |
| [Build an MCP server - Model Context Protocol](https://modelcontextprotocol.io/docs/develop/build-server) | 2026-09-14 | 文件核對 |

另核對 [GitHub Action 的固定提交與輸入契約](https://github.com/anthropics/claude-code-action/blob/9cdae7f0d995e3ba7c33f226087fdf82a59cd520/action.yml)，確認 structured_output、show_full_output、display_report 等欄位。範例是手動觸發、預設分支、固定假 diff 的實驗；不宣稱外部 CI 已跑過。

MCP 材料固定 @modelcontextprotocol/client、@modelcontextprotocol/server 2.0.0 與 zod 4.6.5，附 lockfile 並執行實際 stdio 工具呼叫。Agent SDK 固定 0.3.270；狀態解析測試與真正模型呼叫分開。CLI 2.1.233 首輪因 OAuth 到期失敗，之後已使用內建瀏覽器重新授權，61、67、73、79、91 五個主流程全部通過；兩輪紀錄分開保存。

## 撰稿時採用的範圍

- CLAUDE.md 提供指引，settings／權限控制行為；AGENTS.md 透過 CLAUDE.md 引用。
- Skill allowed-tools 用於預先授權，不能把它單獨描述成全面工具禁止清單。
- Hook 的 Write／Edit 路徑保護不覆蓋所有 shell 或外部操作；Stop 設計有重複事件的停止條件。
- 原生 Windows 的權限練習和支援平台的 Bash sandbox 分開。
- 本機 HTTP 假服務只能示範狀態碼，沒有實作或驗證完整遠端 MCP OAuth。
- Agent Teams 採文件當日的實驗功能與自然語言分工方式；Worktree 替代練習通過不表示 Teams 已使用。
- 手機篇區分本機 Remote Control、雲端工作與 Dispatch；資格、連線與休眠在讀者實際入口確認。
- CLI JSON 外層執行結果與內層結構資料分開驗證；故障輸出不能當成空結果成功。
- 排程結果、每次嘗試、取消與去重各自留證；本機去重不承諾外部副作用必定只執行一次。
- 比較資料為明示的合成案例，沒有把範例數字當成模型排名或真實費用。

## 發布前仍需補做

五篇 CLI 主流程與網頁雲端工作已通過，SDK 原範例 query／resume 與另建串流取消探針通過；另通過七個 CLI 邊界案例，包含 Read 權限、Hook 寫入拒絕、Skill 自動選用、MCP 啟動失敗及只讀子代理。其餘故障、Bash sandbox、Agent Teams 與真實比較仍依逐篇表補齊。第 81 篇需真正遠端服務授權，第 90 篇需手機與電腦，第 92 篇已指定 travel_scanner，但仍缺 claude-lab 環境與 Anthropic CI 憑證；第 94 篇原 runner 已補測缺少／無效 session、執行檔啟動失敗與重新建立 query；實體 Ctrl+C 與中斷 session 恢復仍待測。記錄環境、版本、輸入、輸出、退出碼和停止方式；不保存憑證。

每個結果標示「官方文件核對」「本機程式／固定事件」「Claude 實際操作」「真實裝置／服務」其中一種。未測項目保持待測，預覽、PR 合併、部署、匯入及公開狀態分開記錄。

補充核對：[SDK Streaming Input](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)（2026-09-14）。取消探針採串流輸入，確認開始收到文字後呼叫 AbortController，沒有完整成功結果。早期單次輸入探針的競態／普通成功回覆不算取消通過，原始嘗試均保留於 evidence/live/。

Hook 初測先被 Write 的讀檔前提拒絕，不能算 Hook 成功；更正後先 Read，再確認 Hook 回傳 protected fixture directory 且檔案未改變。子代理初測超時，後續使用 Haiku 在 33.84 秒完成一次只讀審查；保留初次失敗與模型差異，不能將其當作模型比較結果。

第 96 篇另完成實際 Claude 開發驗證：Sonnet 從 starter 製作篩選、畫面與保存；指定比較符號故障由 Haiku 修正，同一組獨立斷言先紅後綠。內建瀏覽器驗證 10 個指定案例，另從實際成果 ZIP 乾淨解壓縮重驗。驗收者更正原 handoff 對部分無效資料處理的一句說明；完整原始模型輸出保留，不把驗收者的修正歸因給模型。尺寸模擬不代表真實手機。
