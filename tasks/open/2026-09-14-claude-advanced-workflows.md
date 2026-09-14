---
id: 2026-09-14-claude-advanced-workflows
title: Claude Code 進階：協作與自動化十篇
status: in-progress
priority: P2
area: docs
owner: codex-claude-completion
claimed_at: 2026-09-14T13:54:38Z
created_at: 2026-09-14T11:13:02Z
completed_at:
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - docs/claude-code-series/lessons/85.md
  - apps/api/app/guides/content/claude-code-tdd-debugging-workshop.json
  - apps/web/public/guides/claude-code-tdd-debugging-workshop
  - docs/claude-code-series/lessons/86.md
  - apps/api/app/guides/content/claude-code-legacy-refactoring-workshop.json
  - apps/web/public/guides/claude-code-legacy-refactoring-workshop
  - docs/claude-code-series/lessons/87.md
  - apps/api/app/guides/content/claude-code-subagent-review-workshop.json
  - apps/web/public/guides/claude-code-subagent-review-workshop
  - docs/claude-code-series/lessons/89.md
  - apps/api/app/guides/content/claude-code-agent-teams-integration-lab.json
  - apps/web/public/guides/claude-code-agent-teams-integration-lab
  - docs/claude-code-series/lessons/90.md
  - apps/api/app/guides/content/claude-code-cross-device-recovery-workshop.json
  - apps/web/public/guides/claude-code-cross-device-recovery-workshop
  - docs/claude-code-series/lessons/92.md
  - apps/api/app/guides/content/claude-code-github-actions-review-workshop.json
  - apps/web/public/guides/claude-code-github-actions-review-workshop
  - docs/claude-code-series/lessons/93.md
  - apps/api/app/guides/content/claude-code-scheduled-workflow-reliability.json
  - apps/web/public/guides/claude-code-scheduled-workflow-reliability
  - docs/claude-code-series/lessons/94.md
  - apps/api/app/guides/content/claude-code-agent-sdk-stateful-runner.json
  - apps/web/public/guides/claude-code-agent-sdk-stateful-runner
  - docs/claude-code-series/lessons/95.md
  - apps/api/app/guides/content/claude-code-workflow-evaluation-cost.json
  - apps/web/public/guides/claude-code-workflow-evaluation-cost
  - docs/claude-code-series/lessons/96.md
  - apps/api/app/guides/content/claude-code-advanced-capstone.json
  - apps/web/public/guides/claude-code-advanced-capstone
---

# Claude Code 進階：協作與自動化十篇

## Why

完成 85–87、89–90、92–96 的開發與自動化教學。

## Definition of done

- [x] 完成十篇正文與可操作流程
- [x] 提供工作流、取消、恢復、成本評估及總實作材料
- [x] 驗證本機案例並明列外部裝置、CI 和帳號的待測範圍

- [x] 發布前文字終審：第 96 篇仍有「验收」「切换」「参考」等繁簡混用，修正原稿時同步內容包與下載快照；目前機器內容檢查未涵蓋此項。

## How to verify

本機模型、流程、Worktree 測試及整套預覽；不等同正式部署或公開

## Notes

2026-09-14：使用者已授權開始第二階段實作。只進行本機教材與預覽，不匯入正式資料庫或發布。Claude CLI 2.1.233 的實際驗證遇到 OAuth 過期；已請使用者重新登入，持續完成獨立材料。

2026-09-14 本機交付：36 篇正文、96 篇系列與 97 頁預覽；內容錯誤／警告皆 0，36 ZIP 共 81 項檢查，六篇試作各 21 個工具測試，9 類瀏覽器案例、73 個相關前端測試通過。API 87 通過／77 PostgreSQL 案例跳過；工具全套 51 通過，最終系列重驗 11 通過。build、lint、typecheck、i18n、Ruff 與 mypy 通過。

驗證紀錄：docs/claude-code-series/advanced/evidence/delivery-checks.json；完整目錄：docs/claude-code-series/advanced/README.md。Claude CLI 2.1.233 五次主流程嘗試因 OAuth 到期失敗；真實手機、遠端 OAuth、Teams、外部 CI、排程和 SDK 呼叫未完成，後續見 claude-advanced-live-validation 任務。

本批尚未開 PR／合併、部署、匯入或公開。完成本機成果後 release，保留 open 待審查；不使用代表合併完成的 done。原先第一階段任務封存變更與 .codex/ 均保持原狀。

2026-09-14 期末實作補驗：第 96 篇由 Claude Sonnet 從 starter 完成篩選、UI、localStorage 與測試；9 項專案測試、3 項獨立斷言、10 項內建瀏覽器案例通過。比較符號反轉在瀏覽器重現，獨立斷言先失敗，Haiku 只改 model.js 後同一斷言轉綠；新 ZIP 乾淨解壓重驗通過。驗收者更正 handoff 對部分無效資料處理的一句說明，模型原始輸出保留。實體手機／跨裝置不在此成果內；臨時伺服器已停止。詳見 evidence/live/capstone-clean-replay.json 與 capstone-result.zip。工具全套 52 項通過，425 個文件連結有效；尚未 PR、合併或發布。

2026-09-14 終審：已完成 15 篇繁簡混用修正並保留 fenced 程式碼原文；內容包與全部下載檔已重建。SDK runner 改為串流輸入，終端機 Ctrl+C 取消和同一中斷 session 恢復已通過。真實兩位 Teams 隊友、一次性產品排程與一組流程觀察完成，範圍見 interactive-products.json；不將簡短讀檔實測宣稱為完整雙角色功能開發。
