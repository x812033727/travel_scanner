---
id: 2026-09-14-claude-code-tutorial-center
title: Claude Code 教學中心：60 篇系列、導覽與可複製範例
status: done
priority: P2
area: web
owner: codex-claude-tutorials
claimed_at: 2026-09-14T05:17:19Z
created_at: 2026-09-14T01:51:28Z
completed_at: 2026-09-14T13:32:38Z
branch: codex/claude-code-tutorial-center
depends_on: []
scope:
  - apps/web/lib/adsense.ts
  - apps/web/lib/adsense.test.ts
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/app/guides/series.py
  - apps/api/app/guides/series_data
  - apps/api/tests/test_guide_series.py
  - apps/api/tests/test_guides_content_pack.py
  - apps/web/lib/content-blocks.ts
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guide-series.ts
  - apps/web/lib/guide-series-copy.ts
  - apps/web/lib/guide-series.test.ts
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/guide-rich-editor.tsx
  - apps/web/components/guide-rich-editor.test.tsx
  - apps/web/components/guide-code-block.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/e2e/claude-code-series.spec.ts
  - apps/web/e2e/fixtures/claude-code-series.ts
  - apps/web/public/tutorials/claude-code
  - docs/claude-code-series
  - tools/claude-code-series
  - tools/claude-code-series.test.mjs
  - apps/api/app/guides/content/claude-code-getting-started.json
  - apps/web/public/guides/claude-code-getting-started
  - apps/api/app/guides/content/claude-code-accounts-and-access.json
  - apps/web/public/guides/claude-code-accounts-and-access
  - apps/api/app/guides/content/claude-code-platforms-guide.json
  - apps/web/public/guides/claude-code-platforms-guide
  - apps/api/app/guides/content/claude-code-terminal-git-basics.json
  - apps/web/public/guides/claude-code-terminal-git-basics
  - apps/api/app/guides/content/claude-code-practice-project-setup.json
  - apps/web/public/guides/claude-code-practice-project-setup
  - apps/api/app/guides/content/claude-code-task-prompts.json
  - apps/web/public/guides/claude-code-task-prompts
  - apps/api/app/guides/content/claude-code-install-windows.json
  - apps/web/public/guides/claude-code-install-windows
  - apps/api/app/guides/content/claude-code-install-macos.json
  - apps/web/public/guides/claude-code-install-macos
  - apps/api/app/guides/content/claude-code-install-linux-wsl.json
  - apps/web/public/guides/claude-code-install-linux-wsl
  - apps/api/app/guides/content/claude-code-desktop-setup.json
  - apps/web/public/guides/claude-code-desktop-setup
  - apps/api/app/guides/content/claude-code-desktop-workflow.json
  - apps/web/public/guides/claude-code-desktop-workflow
  - apps/api/app/guides/content/claude-code-ide-integration.json
  - apps/web/public/guides/claude-code-ide-integration
  - apps/api/app/guides/content/claude-code-on-the-web.json
  - apps/web/public/guides/claude-code-on-the-web
  - apps/api/app/guides/content/claude-code-mobile-ios.json
  - apps/web/public/guides/claude-code-mobile-ios
  - apps/api/app/guides/content/claude-code-mobile-android.json
  - apps/web/public/guides/claude-code-mobile-android
  - apps/api/app/guides/content/claude-code-remote-control.json
  - apps/web/public/guides/claude-code-remote-control
  - apps/api/app/guides/content/claude-code-desktop-dispatch.json
  - apps/web/public/guides/claude-code-desktop-dispatch
  - apps/api/app/guides/content/claude-code-cross-device-workflow.json
  - apps/web/public/guides/claude-code-cross-device-workflow
  - apps/api/app/guides/content/claude-code-markdown-basics.json
  - apps/web/public/guides/claude-code-markdown-basics
  - apps/api/app/guides/content/claude-code-claude-md-guide.json
  - apps/web/public/guides/claude-code-claude-md-guide
  - apps/api/app/guides/content/claude-code-claude-md-scopes.json
  - apps/web/public/guides/claude-code-claude-md-scopes
  - apps/api/app/guides/content/claude-code-rules-and-imports.json
  - apps/web/public/guides/claude-code-rules-and-imports
  - apps/api/app/guides/content/claude-code-auto-memory.json
  - apps/web/public/guides/claude-code-auto-memory
  - apps/api/app/guides/content/claude-code-settings-json.json
  - apps/web/public/guides/claude-code-settings-json
  - apps/api/app/guides/content/claude-code-cli-command-guide.json
  - apps/web/public/guides/claude-code-cli-command-guide
  - apps/api/app/guides/content/claude-code-help-status-doctor.json
  - apps/web/public/guides/claude-code-help-status-doctor
  - apps/api/app/guides/content/claude-code-sessions-resume.json
  - apps/web/public/guides/claude-code-sessions-resume
  - apps/api/app/guides/content/claude-code-context-compact-clear.json
  - apps/web/public/guides/claude-code-context-compact-clear
  - apps/api/app/guides/content/claude-code-models-usage-config.json
  - apps/web/public/guides/claude-code-models-usage-config
  - apps/api/app/guides/content/claude-code-permissions-plan-mode.json
  - apps/web/public/guides/claude-code-permissions-plan-mode
  - apps/api/app/guides/content/claude-code-files-and-context.json
  - apps/web/public/guides/claude-code-files-and-context
  - apps/api/app/guides/content/claude-code-understand-codebase.json
  - apps/web/public/guides/claude-code-understand-codebase
  - apps/api/app/guides/content/claude-code-implement-feature.json
  - apps/web/public/guides/claude-code-implement-feature
  - apps/api/app/guides/content/claude-code-debug-and-test.json
  - apps/web/public/guides/claude-code-debug-and-test
  - apps/api/app/guides/content/claude-code-git-review-pr.json
  - apps/web/public/guides/claude-code-git-review-pr
  - apps/api/app/guides/content/claude-code-checkpoints-rewind.json
  - apps/web/public/guides/claude-code-checkpoints-rewind
  - apps/api/app/guides/content/claude-code-hooks-and-skills.json
  - apps/web/public/guides/claude-code-hooks-and-skills
  - apps/api/app/guides/content/claude-code-skills-skill-md.json
  - apps/web/public/guides/claude-code-skills-skill-md
  - apps/api/app/guides/content/claude-code-skill-arguments-resources.json
  - apps/web/public/guides/claude-code-skill-arguments-resources
  - apps/api/app/guides/content/claude-code-custom-commands.json
  - apps/web/public/guides/claude-code-custom-commands
  - apps/api/app/guides/content/claude-code-hooks-getting-started.json
  - apps/web/public/guides/claude-code-hooks-getting-started
  - apps/api/app/guides/content/claude-code-hooks-recipes.json
  - apps/web/public/guides/claude-code-hooks-recipes
  - apps/api/app/guides/content/claude-code-mcp-servers.json
  - apps/web/public/guides/claude-code-mcp-servers
  - apps/api/app/guides/content/claude-code-mcp-setup-troubleshooting.json
  - apps/web/public/guides/claude-code-mcp-setup-troubleshooting
  - apps/api/app/guides/content/claude-code-plugins-guide.json
  - apps/web/public/guides/claude-code-plugins-guide
  - apps/api/app/guides/content/claude-code-subagents-guide.json
  - apps/web/public/guides/claude-code-subagents-guide
  - apps/api/app/guides/content/claude-code-worktrees-parallel.json
  - apps/web/public/guides/claude-code-worktrees-parallel
  - apps/api/app/guides/content/claude-code-agent-teams.json
  - apps/web/public/guides/claude-code-agent-teams
  - apps/api/app/guides/content/claude-code-chrome-browser.json
  - apps/web/public/guides/claude-code-chrome-browser
  - apps/api/app/guides/content/claude-code-computer-use.json
  - apps/web/public/guides/claude-code-computer-use
  - apps/api/app/guides/content/claude-code-headless-json.json
  - apps/web/public/guides/claude-code-headless-json
  - apps/api/app/guides/content/claude-code-scheduled-tasks.json
  - apps/web/public/guides/claude-code-scheduled-tasks
  - apps/api/app/guides/content/claude-code-github-actions.json
  - apps/web/public/guides/claude-code-github-actions
  - apps/api/app/guides/content/claude-code-agent-sdk.json
  - apps/web/public/guides/claude-code-agent-sdk
  - apps/api/app/guides/content/claude-code-build-todo-app.json
  - apps/web/public/guides/claude-code-build-todo-app
  - apps/api/app/guides/content/claude-code-maintain-existing-project.json
  - apps/web/public/guides/claude-code-maintain-existing-project
  - apps/api/app/guides/content/claude-code-project-data-safety.json
  - apps/web/public/guides/claude-code-project-data-safety
  - apps/api/app/guides/content/claude-code-usage-cost-optimization.json
  - apps/web/public/guides/claude-code-usage-cost-optimization
  - apps/api/app/guides/content/claude-code-troubleshooting.json
  - apps/web/public/guides/claude-code-troubleshooting
  - apps/api/app/guides/content/claude-code-templates-cheatsheet.json
  - apps/web/public/guides/claude-code-templates-cheatsheet
  - apps/api/app/guides/content/claude-code-tutorials.json
  - apps/web/public/guides/claude-code-tutorials
---

# Claude Code 教學中心：60 篇系列、導覽與可複製範例

## Why

生活分享需要一個可搜尋、篩選與循序閱讀的 Claude Code 教學中心。交付包含一份總目錄、60 篇繁體中文完整教學、共用練習專案與發布狀態安全的文章導覽。使用者已授權本機實作與預覽驗收，正式匯入、公開發布及部署另行授權。

## Definition of done

- [x] 61 個頁面內容完整並可在本機預覽驗收。
- [x] 目錄搜尋、組合篩選、學習路線與返回保留條件。
- [x] 頂部／底部導覽、站內文字引用與章節目錄正常。
- [x] 未公開、隱藏、撤回與缺語系文章不產生公開連結。
- [x] 程式碼可原樣複製，後台編輯與公開預覽一致。
- [x] 相關 API、web、內容包、瀏覽器、lint、型別、i18n 與 task 檢查通過。

## Steps

- [x] 建立同一來源的 60 篇系列清單、別名、先備、延伸閱讀與五條路線。
- [x] 建立 Todo 起始版、刻意錯誤版與參考完成版下載材料。
- [x] 實作系列 API、公開條件解析與 rich_paragraph／code 區塊。
- [x] 實作目錄、文章導覽、桌面／手機章節目錄與後台編輯能力。
- [x] 完成全部 60 篇與總目錄正文，01–59 均達 1,800 字；第 60 篇為速查用途。
- [x] 全部內容與範例逐篇複核，完成整套瀏覽器預覽。
- [x] 完成受影響檢查並整理交付紀錄。

## How to verify

內容生成：`apps/api/.venv/Scripts/python.exe -X utf8 tools/claude-code-series/generate.py`

素材產生：`node tools/claude-code-series/render-art.mjs`

完整內容檢查：`apps/api/.venv/Scripts/python.exe -X utf8 tools/claude-code-series/validate.py`

工具測試：`node --test tools/claude-code-series.test.mjs`

執行相關 API 與前端測試、正式 build 後的系列 Playwright 案例，並在 360px、390px、桌面檢查可讀性、搜尋、導覽與程式碼複製。

## Notes

- 已由既有批次 `2026-09-13-life-ai-batch-04` 移交五個 Claude Code slug 至此任務，原批次已 release，避免重複製作；其他 15 篇未動。
- 避開現有進行中的 messages／API i18n 範圍；新 UI 文案集中於本任務的 guide-series-copy.ts。
- 官方來源查證 metadata 在 docs/claude-code-series/source-checks.json，完整抓取只在暫存目錄。這是官方文件核對，沒有操作真實 Claude 訂閱、手機、Dispatch 或付費 API。
- 2026-09-14 官方資料有更新：Git for Windows 現為建議而非原生 CLI 必要條件；Desktop 有 Linux beta；Dispatch 為部分 Pro／Max 限量 beta，現行引導不統一要求 QR 配對；claude doctor 與 /doctor 行為不同。
- API 最終相關整合測試 163 passed、99 skipped（可選 PostgreSQL 參數案例未配置）；ruff 全 API 與 mypy app 327 個檔案通過。相關 web 五檔 114 passed、廣告插入回歸 41 passed。
- 下載包實際解壓縮執行：starter 4 項通過、complete 6 項通過；bug-toggle 的指定識別碼測試如預期失敗。Node 子測試需要移除繼承的 NODE_TEST_CONTEXT，已處理並驗證。
- 全部 61 組封面與圖解已產生，畫布文字邊界檢查通過。桌面與 360／390px 的目錄、CLAUDE.md、Hooks、速查與待辦完成版已有截圖與目視檢查。
- 不使用 tasks done：此分支尚未合併。交付時依協議 release 並保留最終驗證紀錄。

- 61 份原生內容包：0 缺漏、0 錯誤、0 警告。工具完整測試 36 passed，涵蓋下載材料、JSON／JavaScript、真實 starter 資料的功能與重構範例，以及 Hooks 人工事件輸入。
- 回歸測試發現既有廣告插入邏輯未辨認 rich_paragraph；先 release、擴充 adsense.ts 與測試範圍再 claim，已修正並通過 41 項測試。
- 唯讀本機預覽啟動方式與交付內容見 docs/claude-code-series/README.md；查證／驗收紀錄見 evidence/verification.md，逐批檢查見 evidence/batch-review.json。正式部署、匯入、發布均未執行。

- 另以本機 Windows Claude Code 2.1.233 實際執行 --version／--help，16 個列示參數與四個子命令存在；未登入或啟動代理。已補入第 25 篇與 evidence/claude-cli-check.json。

- 最終完整 web：256 個檔案、2,778 項測試全數通過（exit 0，1,576.67 秒）。lint:web、typecheck:web、check:i18n、build:web、check:tasks 與 git diff --check 通過；check:tasks 保留佇列原有過期認領及其他任務 i18n 範圍重疊警告，與本任務無關。
- 最終 Playwright：7 passed，追加主題／程度／平台組合與 MD 路線順序後，該案例再 1 passed。全部 61 頁已遍歷；360／390px、原生剪貼簿與練習成品已驗收。
- 本機已完成，尚未建立 PR／合併。後續接手應先審閱本分支與 review-bundle.zip；部署、匯入、發布需要各自接續授權，不能把本機 preview 視為公開完成。

- 交付 ZIP 已實際開啟驗證：338 個項目、337 個 SHA-256 全部一致，含 61 份內容、61 份 Markdown、61 張封面、61 張圖解與 3 份練習下載包；約 10.4 MB。整包 SHA-256：16077c1eb9682070e6af00cd682c85d63a3f7969eb02c80469da49de67993d6f。

- 2026-09-14 使用者授權開 PR 並合併。已建立 PR #485：https://github.com/x812033727/travel_scanner/pull/485；整合 main 24af1490，兩個呈現元件保留 GuideImage 與系列功能的 imports。相關 API 重驗 23 passed／13 skipped，ruff 全 API 與 mypy app 328 個檔案通過；其餘檢查以 PR CI 及後續紀錄為準。
- main 新帶入的三十篇文章任務仍以 review 狀態認領整個 content／public/guides 目錄，造成任務檢查範圍警告；其實際 #468 變更已在 main，本系列 61 個精確 slug 與其新增文章不同，未修改該批次檔案。
