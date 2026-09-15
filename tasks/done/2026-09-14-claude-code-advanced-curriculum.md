---
id: 2026-09-14-claude-code-advanced-curriculum
title: Claude Code 深入教學第二階段：課程與驗收規劃
status: done
priority: P2
area: docs
owner: codex-claude-completion
claimed_at: 2026-09-14T15:15:19Z
created_at: 2026-09-14T11:02:28Z
completed_at: 2026-09-14T15:36:18Z
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - docs/claude-code-series/advanced
---

# Claude Code 深入教學第二階段：課程與驗收交付

## Why

使用者在課程規劃後授權開始製作。保留 36 篇任務書，交付完整文章索引、來源與逐篇驗證紀錄，並維護本機預覽與真實環境測試的界線。

## Definition of done

- [x] 36 篇原稿、36 包快照與六組合集均可由目錄取得
- [x] 編輯清單已轉成 96 篇正式系列資料；97 頁可本機預覽
- [x] 來源、材料雜湊、瀏覽器與逐篇驗證表已整理
- [x] 未通過的 Claude／裝置／外部服務操作另列待辦

## How to verify

python tools/claude-code-series/advanced/audit-delivery.py；見 docs/claude-code-series/advanced/evidence/delivery-checks.json。舊 advanced/validation.json 保留規劃階段歷史結果。

## Notes

2026-09-14 合併結案：本任務實作已隨 PR #501 合併，merge SHA 3e7f377237f36215f0fb3bac63d02c344dbe60e6。合併前最終提交的 14 個 CI 工作全部成功；主線手動 Actions baseline 成功（run 34862981734，model-review skipped）。WSL2 沙箱、完整 Teams 與 SDK 已有指定案例實測。未完成的實體手機、遠端 MCP OAuth 及付費 CI 模型測試保留在 live-validation／ci-validation 任務；正式部署、匯入與公開未執行。以下舊測試數量與阻塞狀態均保留為歷史。


2026-09-14 本機交付：36 篇正文、96 篇系列與 97 頁預覽；內容錯誤／警告皆 0，36 ZIP 共 81 項檢查，六篇試作各 21 個工具測試，9 類瀏覽器案例、73 個相關前端測試通過。API 87 通過／77 PostgreSQL 案例跳過；工具全套 51 通過，最終系列重驗 11 通過。build、lint、typecheck、i18n、Ruff 與 mypy 通過。

驗證紀錄：docs/claude-code-series/advanced/evidence/delivery-checks.json；完整目錄：docs/claude-code-series/advanced/README.md。Claude CLI 2.1.233 五次主流程嘗試因 OAuth 到期失敗；真實手機、遠端 OAuth、Teams、外部 CI、排程和 SDK 呼叫未完成，後續見 claude-advanced-live-validation 任務。

本批尚未開 PR／合併、部署、匯入或公開。完成本機成果後 release，保留 open 待審查；不使用代表合併完成的 done。原先第一階段任務封存變更與 .codex/ 均保持原狀。

2026-09-14 補驗完成：Windows 完整前端 258 檔、2,809 項通過；隔離 PostgreSQL 17.11 與 SQLite 164 項通過、0 跳過。新紀錄在 evidence/live/verification-summary.json；README、delivery-checks.json 與 review-bundle.zip 已更新。WSL 備援在 Windows 全套完成後停止，未宣稱全套通過。實際 Claude／裝置操作仍依 live-validation 任務補齊。剩餘 PostgreSQL 暫存目錄刪除被自動核准審查拒絕，資料庫已停止。

2026-09-14 後續：使用內建瀏覽器重新授權後，五篇 CLI 主流程、SDK query／resume／串流取消探針，以及使用者指定 travel_scanner 的網頁雲端 Node.js 任務均通過。更新 README、逐篇驗證表、來源界線與審查包，保留初期失敗。最新證據在 evidence/live/real-operations-summary.json；手機、外部 OAuth、Actions 環境／憑證、產品排程及其他故障／完整實作仍待補齊，不再把到期登入列為目前阻塞。

2026-09-14 邊界補驗：七個實際 CLI 案例通過（子目錄規則、Skill 缺參數／自動選用、Read deny、Hook Write deny、MCP 啟動失敗、只讀子代理）；Hook 初測是 Write 前提拒絕、子代理初測超時，均保留失敗紀錄，後續重驗才列成功。SDK 原 runner 另通過四種狀態／啟動／重新 query 案例，實體 Ctrl+C 與中斷 session 恢復仍待測。新 GitHub workflow 有專用任務維護，尚未合併或 dispatch；同名環境與 CI 憑證仍缺。逐篇表、來源界線、423 個有效文件連結及審查包同步更新；文章與下載 ZIP 本身未改動。

2026-09-14 期末實作補驗：第 96 篇由 Claude Sonnet 從 starter 完成篩選、UI、localStorage 與測試；9 項專案測試、3 項獨立斷言、10 項內建瀏覽器案例通過。比較符號反轉在瀏覽器重現，獨立斷言先失敗，Haiku 只改 model.js 後同一斷言轉綠；新 ZIP 乾淨解壓重驗通過。驗收者更正 handoff 對部分無效資料處理的一句說明，模型原始輸出保留。實體手機／跨裝置不在此成果內；臨時伺服器已停止。詳見 evidence/live/capstone-clean-replay.json 與 capstone-result.zip。工具全套 52 項通過，425 個文件連結有效；尚未 PR、合併或發布。
