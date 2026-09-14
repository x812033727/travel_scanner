---
id: 2026-09-14-claude-advanced-rules-skills
title: Claude Code 進階：規則與 Skills 十篇
status: done
priority: P2
area: docs
owner: codex-claude-completion
claimed_at: 2026-09-14T13:54:28Z
created_at: 2026-09-14T11:12:52Z
completed_at: 2026-09-14T15:36:17Z
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - docs/claude-code-series/lessons/62.md
  - apps/api/app/guides/content/claude-code-monorepo-rules-workshop.json
  - apps/web/public/guides/claude-code-monorepo-rules-workshop
  - docs/claude-code-series/lessons/63.md
  - apps/api/app/guides/content/claude-code-rules-loading-diagnostics.json
  - apps/web/public/guides/claude-code-rules-loading-diagnostics
  - docs/claude-code-series/lessons/64.md
  - apps/api/app/guides/content/claude-code-permissions-sandbox-lab.json
  - apps/web/public/guides/claude-code-permissions-sandbox-lab
  - docs/claude-code-series/lessons/65.md
  - apps/api/app/guides/content/claude-code-context-handoff-workshop.json
  - apps/web/public/guides/claude-code-context-handoff-workshop
  - docs/claude-code-series/lessons/66.md
  - apps/api/app/guides/content/claude-code-team-config-maintenance.json
  - apps/web/public/guides/claude-code-team-config-maintenance
  - docs/claude-code-series/lessons/68.md
  - apps/api/app/guides/content/claude-code-skill-input-validation.json
  - apps/web/public/guides/claude-code-skill-input-validation
  - docs/claude-code-series/lessons/69.md
  - apps/api/app/guides/content/claude-code-skill-resource-design.json
  - apps/web/public/guides/claude-code-skill-resource-design
  - docs/claude-code-series/lessons/70.md
  - apps/api/app/guides/content/claude-code-skill-invocation-control.json
  - apps/web/public/guides/claude-code-skill-invocation-control
  - docs/claude-code-series/lessons/71.md
  - apps/api/app/guides/content/claude-code-skill-regression-testing.json
  - apps/web/public/guides/claude-code-skill-regression-testing
  - docs/claude-code-series/lessons/72.md
  - apps/api/app/guides/content/claude-code-plugin-team-distribution.json
  - apps/web/public/guides/claude-code-plugin-team-distribution
---

# Claude Code 進階：規則與 Skills 十篇

## Why

完成 62–66、68–72 的規則與 Skills 深入實作。

## Definition of done

- [x] 完成十篇正文與獨立材料
- [x] 核對參數、規則來源、升級及還原案例
- [x] 驗證內容包、站內引用、圖片和下載

## How to verify

內容驗證器、JSON/JavaScript 範例測試及 ZIP 測試

## Notes

2026-09-14 合併結案：本任務實作已隨 PR #501 合併，merge SHA 3e7f377237f36215f0fb3bac63d02c344dbe60e6。合併前最終提交的 14 個 CI 工作全部成功；主線手動 Actions baseline 成功（run 34862981734，model-review skipped）。WSL2 沙箱、完整 Teams 與 SDK 已有指定案例實測。未完成的實體手機、遠端 MCP OAuth 及付費 CI 模型測試保留在 live-validation／ci-validation 任務；正式部署、匯入與公開未執行。以下舊測試數量與阻塞狀態均保留為歷史。


2026-09-14：使用者已授權開始第二階段實作。只進行本機教材與預覽，不匯入正式資料庫或發布。Claude CLI 2.1.233 的實際驗證遇到 OAuth 過期；已請使用者重新登入，持續完成獨立材料。

2026-09-14 本機交付：36 篇正文、96 篇系列與 97 頁預覽；內容錯誤／警告皆 0，36 ZIP 共 81 項檢查，六篇試作各 21 個工具測試，9 類瀏覽器案例、73 個相關前端測試通過。API 87 通過／77 PostgreSQL 案例跳過；工具全套 51 通過，最終系列重驗 11 通過。build、lint、typecheck、i18n、Ruff 與 mypy 通過。

驗證紀錄：docs/claude-code-series/advanced/evidence/delivery-checks.json；完整目錄：docs/claude-code-series/advanced/README.md。Claude CLI 2.1.233 五次主流程嘗試因 OAuth 到期失敗；真實手機、遠端 OAuth、Teams、外部 CI、排程和 SDK 呼叫未完成，後續見 claude-advanced-live-validation 任務。

本批尚未開 PR／合併、部署、匯入或公開。完成本機成果後 release，保留 open 待審查；不使用代表合併完成的 done。原先第一階段任務封存變更與 .codex/ 均保持原狀。
