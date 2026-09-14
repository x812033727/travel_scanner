---
id: 2026-09-14-claude-advanced-integration
title: Claude Code 進階：96 篇目錄與內容工具整合
status: in-progress
priority: P2
area: docs
owner: codex-claude-completion
claimed_at: 2026-09-14T13:54:26Z
created_at: 2026-09-14T11:12:36Z
completed_at:
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - apps/api/app/guides/series_data/claude-code.json
  - tools/claude-code-series/generate.py
  - tools/claude-code-series/render-art.mjs
  - tools/claude-code-series/validate.py
  - tools/claude-code-series/preview.mjs
  - tools/claude-code-series.test.mjs
  - apps/api/tests/test_guide_series.py
  - apps/web/e2e/claude-code-series.spec.ts
  - apps/web/e2e/fixtures/claude-code-series.ts
  - docs/claude-code-series/README.md
  - docs/claude-code-series/source-checks.json
  - docs/claude-code-series/lessons/00.md
  - docs/claude-code-series/lessons/20.md
  - docs/claude-code-series/lessons/38.md
  - docs/claude-code-series/lessons/41.md
  - docs/claude-code-series/lessons/43.md
  - docs/claude-code-series/lessons/47.md
  - docs/claude-code-series/lessons/51.md
  - apps/api/app/guides/content/claude-code-tutorials.json
  - apps/web/public/guides/claude-code-tutorials
  - apps/api/app/guides/content/claude-code-claude-md-guide.json
  - apps/web/public/guides/claude-code-claude-md-guide
  - apps/api/app/guides/content/claude-code-skills-skill-md.json
  - apps/web/public/guides/claude-code-skills-skill-md
  - apps/api/app/guides/content/claude-code-hooks-getting-started.json
  - apps/web/public/guides/claude-code-hooks-getting-started
  - apps/api/app/guides/content/claude-code-mcp-servers.json
  - apps/web/public/guides/claude-code-mcp-servers
  - apps/api/app/guides/content/claude-code-worktrees-parallel.json
  - apps/web/public/guides/claude-code-worktrees-parallel
  - apps/api/app/guides/content/claude-code-headless-json.json
  - apps/web/public/guides/claude-code-headless-json
---

# Claude Code 進階：96 篇目錄與內容工具整合

## Why

將第二階段 36 篇接入同一目錄、導覽、搜尋與可下載材料，保留第一階段驗證紀錄。

## Definition of done

- [x] 96 篇清單、16 分組、12 路線已整合
- [x] 產生全部內容包及封面，更新原始入口與六篇先備文章
- [x] 驗證連結、API 發布邊界、手機版與程式碼複製

## How to verify

npm run test:tools; uv run python tools/claude-code-series/validate.py --output docs/claude-code-series/advanced/evidence/content-validation.json; 使用 advanced/playwright.config.mjs

## Notes

2026-09-14：使用者已授權開始第二階段實作。只進行本機教材與預覽，不匯入正式資料庫或發布。Claude CLI 2.1.233 的實際驗證遇到 OAuth 過期；已請使用者重新登入，持續完成獨立材料。

2026-09-14 本機交付：36 篇正文、96 篇系列與 97 頁預覽；內容錯誤／警告皆 0，36 ZIP 共 81 項檢查，六篇試作各 21 個工具測試，9 類瀏覽器案例、73 個相關前端測試通過。API 87 通過／77 PostgreSQL 案例跳過；工具全套 51 通過，最終系列重驗 11 通過。build、lint、typecheck、i18n、Ruff 與 mypy 通過。

驗證紀錄：docs/claude-code-series/advanced/evidence/delivery-checks.json；完整目錄：docs/claude-code-series/advanced/README.md。Claude CLI 2.1.233 五次主流程嘗試因 OAuth 到期失敗；真實手機、遠端 OAuth、Teams、外部 CI、排程和 SDK 呼叫未完成，後續見 claude-advanced-live-validation 任務。

本批尚未開 PR／合併、部署、匯入或公開。完成本機成果後 release，保留 open 待審查；不使用代表合併完成的 done。原先第一階段任務封存變更與 .codex/ 均保持原狀。

2026-09-14 補驗：下載連結檢查只檢查 URL 的 path，避免外部連結 query 含下載字串時誤判。97 頁內容重驗無缺頁、錯誤或警告；系列工具 11 項通過。隔離 PostgreSQL 17.11 與 SQLite 合計 164 項通過、0 skipped，詳見 advanced/evidence/live/。

Windows 完整前端最終 258 檔、2,809 項通過、0 skipped。第二階段文件 414 個本機連結均有效；自有 scope 外的既存變更保留。審查 ZIP 已重建並附雜湊；後續依 live-validation 任務補真實操作，再同步 main 與核對 PR head 的 CI。

2026-09-14 後續：已由內建瀏覽器完成 CLI 重新授權，五篇主流程與網頁雲端驗證通過；SDK query／resume 與獨立串流取消探針通過。重新產生交付文件時沿用本任務的根目錄導覽，不改寫既有文章內容或發布狀態。詳細剩餘範圍見 evidence/live/real-operations-summary.json。

2026-09-14 邊界補驗：七個實際 CLI 案例通過（子目錄規則、Skill 缺參數／自動選用、Read deny、Hook Write deny、MCP 啟動失敗、只讀子代理）；Hook 初測是 Write 前提拒絕、子代理初測超時，均保留失敗紀錄，後續重驗才列成功。SDK 原 runner 另通過四種狀態／啟動／重新 query 案例，實體 Ctrl+C 與中斷 session 恢復仍待測。新 GitHub workflow 有專用任務維護，尚未合併或 dispatch；同名環境與 CI 憑證仍缺。逐篇表、來源界線、423 個有效文件連結及審查包同步更新；文章與下載 ZIP 本身未改動。

2026-09-14 期末實作補驗：第 96 篇由 Claude Sonnet 從 starter 完成篩選、UI、localStorage 與測試；9 項專案測試、3 項獨立斷言、10 項內建瀏覽器案例通過。比較符號反轉在瀏覽器重現，獨立斷言先失敗，Haiku 只改 model.js 後同一斷言轉綠；新 ZIP 乾淨解壓重驗通過。驗收者更正 handoff 對部分無效資料處理的一句說明，模型原始輸出保留。實體手機／跨裝置不在此成果內；臨時伺服器已停止。詳見 evidence/live/capstone-clean-replay.json 與 capstone-result.zip。工具全套 52 項通過，425 個文件連結有效；尚未 PR、合併或發布。
