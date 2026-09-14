---
id: 2026-09-14-codex-learning-series
title: Codex learning hub - 60 in-depth multilingual tutorials
status: in-progress
priority: P2
area: docs
owner: codex-integration-fc2e
claimed_at: 2026-09-14T06:50:58Z
created_at: 2026-09-14T01:13:26Z
completed_at:
branch: codex/codex-learning-complete
depends_on: []
scope:
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/app/[locale]/life/page.tsx
  - docs/codex-learning
  - tools/codex-learning
  - apps/web/lib/codex-learning
  - apps/web/components/codex-learning
  - apps/web/lib/content-blocks.ts
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/lib/guides.ts
  - apps/web/components/guides/article-page.tsx
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_codex_learning.py
  - tasks/open/2026-09-13-life-ai-batch-04.md
  - apps/api/app/guides/content/codex-beginner-guide.json
  - apps/web/public/guides/codex-beginner-guide
  - apps/api/app/guides/content/codex-account-usage.json
  - apps/web/public/guides/codex-account-usage
  - apps/api/app/guides/content/codex-desktop-getting-started.json
  - apps/web/public/guides/codex-desktop-getting-started
  - apps/api/app/guides/content/codex-mobile-guide.json
  - apps/web/public/guides/codex-mobile-guide
  - apps/api/app/guides/content/codex-cli-getting-started.json
  - apps/web/public/guides/codex-cli-getting-started
  - apps/api/app/guides/content/codex-first-project.json
  - apps/web/public/guides/codex-first-project
  - apps/api/app/guides/content/codex-prompting.json
  - apps/web/public/guides/codex-prompting
  - apps/api/app/guides/content/codex-plan-mode.json
  - apps/web/public/guides/codex-plan-mode
  - apps/api/app/guides/content/codex-markdown-basics.json
  - apps/web/public/guides/codex-markdown-basics
  - apps/api/app/guides/content/codex-agents-md.json
  - apps/web/public/guides/codex-agents-md
  - apps/api/app/guides/content/codex-commands.json
  - apps/web/public/guides/codex-commands
  - apps/api/app/guides/content/codex-troubleshooting.json
  - apps/web/public/guides/codex-troubleshooting
  - apps/api/app/guides/content/codex-project-management.json
  - apps/web/public/guides/codex-project-management
  - apps/api/app/guides/content/codex-ide-getting-started.json
  - apps/web/public/guides/codex-ide-getting-started
  - apps/api/app/guides/content/codex-cloud-tasks-github.json
  - apps/web/public/guides/codex-cloud-tasks-github
  - apps/api/app/guides/content/codex-config-toml.json
  - apps/web/public/guides/codex-config-toml
  - apps/api/app/guides/content/codex-model-selection.json
  - apps/web/public/guides/codex-model-selection
  - apps/api/app/guides/content/codex-permissions.json
  - apps/web/public/guides/codex-permissions
  - apps/api/app/guides/content/codex-git-basics.json
  - apps/web/public/guides/codex-git-basics
  - apps/api/app/guides/content/codex-debugging.json
  - apps/web/public/guides/codex-debugging
  - apps/api/app/guides/content/codex-testing-review.json
  - apps/web/public/guides/codex-testing-review
  - apps/api/app/guides/content/codex-context-handoff.json
  - apps/web/public/guides/codex-context-handoff
  - apps/api/app/guides/content/codex-skills.json
  - apps/web/public/guides/codex-skills
  - apps/api/app/guides/content/codex-plugins.json
  - apps/web/public/guides/codex-plugins
  - apps/api/app/guides/content/codex-mcp.json
  - apps/web/public/guides/codex-mcp
  - apps/api/app/guides/content/codex-browser-images.json
  - apps/web/public/guides/codex-browser-images
  - apps/api/app/guides/content/codex-worktrees.json
  - apps/web/public/guides/codex-worktrees
  - apps/api/app/guides/content/codex-subagents.json
  - apps/web/public/guides/codex-subagents
  - apps/api/app/guides/content/codex-automations.json
  - apps/web/public/guides/codex-automations
  - apps/api/app/guides/content/codex-exec-scripting.json
  - apps/web/public/guides/codex-exec-scripting
  - apps/api/app/guides/content/codex-website-workshop.json
  - apps/web/public/guides/codex-website-workshop
  - apps/api/app/guides/content/codex-csv-workshop.json
  - apps/web/public/guides/codex-csv-workshop
  - apps/api/app/guides/content/codex-learning-hub.json
  - apps/web/public/guides/codex-learning-hub
  - apps/api/app/guides/content/codex-platforms-guide.json
  - apps/web/public/guides/codex-platforms-guide
  - apps/api/app/guides/content/codex-terminal-paths.json
  - apps/web/public/guides/codex-terminal-paths
  - apps/api/app/guides/content/codex-cli-windows.json
  - apps/web/public/guides/codex-cli-windows
  - apps/api/app/guides/content/codex-cli-macos.json
  - apps/web/public/guides/codex-cli-macos
  - apps/api/app/guides/content/codex-cli-linux-wsl.json
  - apps/web/public/guides/codex-cli-linux-wsl
  - apps/api/app/guides/content/codex-mobile-ios.json
  - apps/web/public/guides/codex-mobile-ios
  - apps/api/app/guides/content/codex-mobile-android.json
  - apps/web/public/guides/codex-mobile-android
  - apps/api/app/guides/content/codex-remote-setup.json
  - apps/web/public/guides/codex-remote-setup
  - apps/api/app/guides/content/codex-cross-device-workflow.json
  - apps/web/public/guides/codex-cross-device-workflow
  - apps/api/app/guides/content/codex-agents-md-scopes.json
  - apps/web/public/guides/codex-agents-md-scopes
  - apps/api/app/guides/content/codex-rules-and-context-files.json
  - apps/web/public/guides/codex-rules-and-context-files
  - apps/api/app/guides/content/codex-config-troubleshooting.json
  - apps/web/public/guides/codex-config-troubleshooting
  - apps/api/app/guides/content/codex-sessions-resume.json
  - apps/web/public/guides/codex-sessions-resume
  - apps/api/app/guides/content/codex-understand-codebase.json
  - apps/web/public/guides/codex-understand-codebase
  - apps/api/app/guides/content/codex-implement-feature.json
  - apps/web/public/guides/codex-implement-feature
  - apps/api/app/guides/content/codex-skill-resources.json
  - apps/web/public/guides/codex-skill-resources
  - apps/api/app/guides/content/codex-skill-testing.json
  - apps/web/public/guides/codex-skill-testing
  - apps/api/app/guides/content/codex-plugin-troubleshooting.json
  - apps/web/public/guides/codex-plugin-troubleshooting
  - apps/api/app/guides/content/codex-templates-cheatsheet.json
  - apps/web/public/guides/codex-templates-cheatsheet
  - apps/api/app/guides/content/codex-mcp-troubleshooting.json
  - apps/web/public/guides/codex-mcp-troubleshooting
  - apps/api/app/guides/content/codex-subagent-quality.json
  - apps/web/public/guides/codex-subagent-quality
  - apps/api/app/guides/content/codex-parallel-integration.json
  - apps/web/public/guides/codex-parallel-integration
  - apps/api/app/guides/content/codex-json-output.json
  - apps/web/public/guides/codex-json-output
  - apps/api/app/guides/content/codex-ci-workflows.json
  - apps/web/public/guides/codex-ci-workflows
  - apps/api/app/guides/content/codex-automation-recovery.json
  - apps/web/public/guides/codex-automation-recovery
  - apps/api/app/guides/content/codex-maintain-existing-project.json
  - apps/web/public/guides/codex-maintain-existing-project
  - apps/api/app/guides/content/codex-project-data-safety.json
  - apps/web/public/guides/codex-project-data-safety
  - apps/api/app/guides/content/codex-usage-efficiency.json
  - apps/web/public/guides/codex-usage-efficiency
  - tasks/open/2026-09-14-codex-depth-content.md
  - tasks/open/2026-09-14-codex-depth-plan-alignment.md
  - apps/api/app/guides/series.py
  - apps/api/app/guides/series_data/codex-zh-TW.json
  - apps/api/app/guides/series_data/codex-zh-CN.json
  - apps/api/app/guides/series_data/codex-en.json
  - apps/api/app/guides/series_data/codex-ja.json
  - apps/api/app/guides/series_data/codex-ko.json
  - apps/api/tests/test_guide_series.py
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/lib/guide-series-copy.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/components/guides/series-hub.tsx
  - apps/web/components/guides/series-hub.test.tsx
  - apps/web/components/guides/series-navigation.tsx
  - apps/web/components/guides/series-navigation.test.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guide-blocks.test.tsx
  - apps/api/tests/test_guide_packs.py
  - apps/api/tests/test_guides.py
---

# Codex learning hub and multilingual tutorial series

2026-09-14 計畫已依使用者要求與「規劃 Claude Code 教學目錄」對齊。有效製作規格見 `docs/codex-learning/depth-plan.md` 與 `article-template.md`：一個總目錄、60 篇、五語，保留 32 篇既有 ID／slug，新增 28 篇；當前深入驗收為 0/60。以下已勾選項是前一輪的草稿與網站基礎，不等於深入教學完成。

## Why

在生活分享建立五語 Codex 學習中心，將零散入門、CLI、雲端文章整合為可搜尋的 60 篇課程，提供相互連結、可複製程式碼與維護來源。

## Definition of done

- [x] 總目錄與 32 篇的五語內容包、系列清單及公開路由整合。
- [x] 程度／平台／需求篩選、指令索引、發布狀態守門及雙向導覽。
- [x] 結構化文字連結、程式碼區塊、API 驗證、後台編輯和預覽，保持舊格式相容。
- [x] 原創配圖、實戰 CSV 和網站範例、五語圖說及可重現驗證紀錄。
- [ ] 依深入模板重寫／擴充既有 32 篇，新增規劃中的 28 篇；一般繁中操作篇約 1,800–3,000 字，五語步驟等義。
- [ ] 先驗收原 ID 03／10／04／11／23 五篇代表篇，包含完整範例、成功／失敗案例、排錯與停止／還原。
- [x] 將待辦網站補為可獨立起步的 HTML／CSS／JavaScript 共用練習，保留 CSV 第二實戰路線。
- [ ] 核對 Claude Code 任務持有人後整合共用格式：spans／inlines 轉接、站內引用、行內 code、用途 label、TOML／CSV 相容。
- [ ] 整合共用系列 API、五語資料、穩定 ID 與閱讀順序、推薦路線、先備文章、URL 篩選及目錄集合頁 SEO。
- [ ] 補上桌面側欄章節目錄／手機可展開目錄與 360px 驗證。
- [ ] 按新閱讀次序完成三批各 20 篇，每十篇一次五語、範例、連結與圖文驗收；共 60 篇＋目錄均可預覽。
- [ ] 審查並合併工作目錄變更；未建立 PR、未合併。
- [ ] 正式發布前補齊所需 Codex 介面截圖與跨平台實機審核；目前仅官方文件查證及 Windows 瀏覽器實測。
- [ ] 後續明確批准後才可匯入、發布、部署與驗證公開網址。

## Steps

- [x] 確認原 AI 第四批任務未被持有，將 CLI／雲端兩篇精確範圍移交，其他 18 篇未動。
- [x] 第一批 01–12 ＋目錄五語內容包。
- [x] 第二批 13–22 五語內容包。
- [x] 第三批 23–32 五語內容包與實戰原始檔。
- [x] API／前端／瀏覽器／內容與圖片驗證；見下列交接文件。

## How to verify

完整命令與資料流程見 `docs/codex-learning/README.md`。主要驗證：

- `npm run lint:web`、`npm run typecheck:web`、`npm run build:web`
- `npm exec --workspace @travel-scanner/web -- vitest run components/codex-learning components/content-blocks.test.tsx components/guides components/admin-guides-panel.test.tsx app/ --pool=threads --maxWorkers=1`
- `npm run check:i18n`、`npm run check:tasks`、`npm run test:tools`
- `uv run --directory apps/api pytest tests/test_codex_learning.py tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q`
- `uv run --directory apps/api python ../../tools/codex-learning/audit.py`
- `node tools/codex-learning/browser-check.mjs`（須先啟動 README 記錄的唯讀假 API 與本機網站）

## Notes

使用者要求開始執行後，拆出 `2026-09-14-codex-depth-content` 精確範圍，避免與活躍 Claude Code 任務共用檔案互相覆寫。本輪已落實 60 筆目錄、十單元、URL 篩選、先備與同單元導覽；五篇代表稿已編成 25 份深化文件，仍有 27 篇短稿及 28 篇新稿待完成。代表篇產品介面證據與共享系統整合仍未全部完成，不提升正式深入驗收。最新檢查與接手入口見 `docs/codex-learning/progress.md`。

前一次對齊僅更新計畫，當時尚未插入 60 筆 runtime catalog；上述新一輪實作已取代該狀態。新增 28 篇的範圍已列在子任務；整合共用檔案前仍須確認 `1cff` 的持有人。兩邊 schema 同名但不相容，不能直接覆寫合併。對方任務仍在製作，不能把已批准規格稱為已完成成果。

使用者此次五語／截圖要求取代舊 brief 的繁中／無截圖限制。未使用正式專案私人資料，也未存取正式資料庫。

公開目錄從 API 讀取實際發布清單，不以 `catalog.ready` 推定可公開。分頁失敗或循環均停止產生連結。正文撤回連結降為文字。第一個輸入曾在 hydration 前遺失，已讓搜尋框在互動準備完成後才啟用，瀏覽器驗證確認結果由 32 縮小為 2。

`docs/codex-learning/evidence/` 留有五語 390／1280px 瀏覽器紀錄與內容稽核。短篇以可完成操作為目標，保留正文長度編輯警告，不填充字數；這不表示每篇已完成正式發布審核。所有 OS 仍需依文件逐項核對當時帳號與版本；不能把 Windows 模擬手機畫面稱為 iPhone／Android 實測。

沒有發布、部署、開 PR 或合併。工作目錄的既有 `.codex/` 未納入內容交付；研究快取也放在該未追蹤目錄，不提交整份官方文件。

最終驗證：build:web 成功；lint:web、TypeScript、Ruff、Mypy 成功；前端受影響頁面 485 項及新增集中測試 30 項通過；API 37 passed / 5 skipped；CSV 3 passed；tools 28 passed。內容稽核零錯誤、143 個保留的編輯警告。先交還任務供後續審核，不標為已合併或已發布。

- 共用整合接續：Claude 系列 #485 已結案合併，將本地已完成 37 篇深化稿與既有共用元件修改先保存，再整合該主分支版本；不開部分 PR。接續統一 inlines、發布解析與五語系列資料，仍需完成剩餘 23 篇及全部驗收。
