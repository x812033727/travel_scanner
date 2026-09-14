---
id: 2026-09-14-claude-advanced-labs
title: Claude Code 進階：六組材料與 36 份練習快照
status: in-progress
priority: P2
area: docs
owner: codex-claude-completion
claimed_at: 2026-09-14T13:54:24Z
created_at: 2026-09-14T11:12:39Z
completed_at:
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - tools/claude-code-series/advanced
  - apps/web/public/tutorials/claude-code/advanced
---

# Claude Code 進階：六組材料與 36 份練習快照

## Why

為六組深入教學提供可獨立開始、具故障材料與參考結果的下載包。

## Definition of done

- [x] 共用 Node 材料、實際 MCP stdio 及 Worktree 實驗已建立
- [x] 36 篇快照與 6 組材料包完整、無 node_modules 或登入資料
- [x] 從實際 ZIP 解壓縮執行成功與故障案例

## How to verify

node --test tools/claude-code-series/advanced/lab/tests/*.test.mjs; python tools/claude-code-series/advanced/package-labs.py

## Notes

2026-09-14：使用者已授權開始第二階段實作。只進行本機教材與預覽，不匯入正式資料庫或發布。Claude CLI 2.1.233 的實際驗證遇到 OAuth 過期；已請使用者重新登入，持續完成獨立材料。

2026-09-14 本機交付：36 篇正文、96 篇系列與 97 頁預覽；內容錯誤／警告皆 0，36 ZIP 共 81 項檢查，六篇試作各 21 個工具測試，9 類瀏覽器案例、73 個相關前端測試通過。API 87 通過／77 PostgreSQL 案例跳過；工具全套 51 通過，最終系列重驗 11 通過。build、lint、typecheck、i18n、Ruff 與 mypy 通過。

驗證紀錄：docs/claude-code-series/advanced/evidence/delivery-checks.json；完整目錄：docs/claude-code-series/advanced/README.md。Claude CLI 2.1.233 五次主流程嘗試因 OAuth 到期失敗；真實手機、遠端 OAuth、Teams、外部 CI、排程和 SDK 呼叫未完成，後續見 claude-advanced-live-validation 任務。

本批尚未開 PR／合併、部署、匯入或公開。完成本機成果後 release，保留 open 待審查；不使用代表合併完成的 done。原先第一階段任務封存變更與 .codex/ 均保持原狀。

2026-09-14 補驗：審查包產生器加入 evidence/live/ 的原始補驗、重現腳本與審查說明，另產生 ZIP 雜湊收據；驗收與 README 產生器讀取實際補驗摘要。Windows 全套前端 258 檔／2,809 項，以及隔離 PostgreSQL／SQLite 164 項皆通過，無跳過。ZIP 內容與雜湊見 review-bundle-receipt.json；真實 Claude 登入及外部操作狀態保持待辦。

2026-09-14 後續：CLI 已重新授權、五篇真實主流程通過；SDK 原範例 query／resume 通過，另建串流輸入取消探針通過。原 SDK runner 未改動，Ctrl+C／故障恢復仍待實測，下載 ZIP 與既有測試雜湊保持有效。產生器改為讀取最新成功實測並保留失敗歷史，審查包包含新的 .mjs 探針；不將單次輸入的正常回覆競態當作取消成功。

2026-09-14 邊界補驗：七個實際 CLI 案例通過（子目錄規則、Skill 缺參數／自動選用、Read deny、Hook Write deny、MCP 啟動失敗、只讀子代理）；Hook 初測是 Write 前提拒絕、子代理初測超時，均保留失敗紀錄，後續重驗才列成功。SDK 原 runner 另通過四種狀態／啟動／重新 query 案例，實體 Ctrl+C 與中斷 session 恢復仍待測。新 GitHub workflow 有專用任務維護，尚未合併或 dispatch；同名環境與 CI 憑證仍缺。逐篇表、來源界線、423 個有效文件連結及審查包同步更新；文章與下載 ZIP 本身未改動。

2026-09-14 期末實作補驗：第 96 篇由 Claude Sonnet 從 starter 完成篩選、UI、localStorage 與測試；9 項專案測試、3 項獨立斷言、10 項內建瀏覽器案例通過。比較符號反轉在瀏覽器重現，獨立斷言先失敗，Haiku 只改 model.js 後同一斷言轉綠；新 ZIP 乾淨解壓重驗通過。驗收者更正 handoff 對部分無效資料處理的一句說明，模型原始輸出保留。實體手機／跨裝置不在此成果內；臨時伺服器已停止。詳見 evidence/live/capstone-clean-replay.json 與 capstone-result.zip。工具全套 52 項通過，425 個文件連結有效；尚未 PR、合併或發布。
