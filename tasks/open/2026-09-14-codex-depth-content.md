---
id: 2026-09-14-codex-depth-content
title: Codex deep content and isolated learning components
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T02:33:43Z
completed_at:
branch:
depends_on: []
scope:
  - docs/codex-learning
  - tools/codex-learning
  - apps/web/lib/codex-learning
  - apps/web/components/codex-learning
  - apps/api/tests/test_codex_learning.py
  - tasks/open/2026-09-14-codex-learning-series.md
  - apps/api/app/guides/content/codex-beginner-guide.json
  - apps/web/public/guides/codex-beginner-guide
  - apps/api/app/guides/content/codex-account-usage.json
  - apps/web/public/guides/codex-account-usage
  - apps/api/app/guides/content/codex-platforms-guide.json
  - apps/web/public/guides/codex-platforms-guide
  - apps/api/app/guides/content/codex-terminal-paths.json
  - apps/web/public/guides/codex-terminal-paths
  - apps/api/app/guides/content/codex-first-project.json
  - apps/web/public/guides/codex-first-project
  - apps/api/app/guides/content/codex-prompting.json
  - apps/web/public/guides/codex-prompting
  - apps/api/app/guides/content/codex-cli-getting-started.json
  - apps/web/public/guides/codex-cli-getting-started
  - apps/api/app/guides/content/codex-cli-windows.json
  - apps/web/public/guides/codex-cli-windows
  - apps/api/app/guides/content/codex-cli-macos.json
  - apps/web/public/guides/codex-cli-macos
  - apps/api/app/guides/content/codex-cli-linux-wsl.json
  - apps/web/public/guides/codex-cli-linux-wsl
  - apps/api/app/guides/content/codex-desktop-getting-started.json
  - apps/web/public/guides/codex-desktop-getting-started
  - apps/api/app/guides/content/codex-ide-getting-started.json
  - apps/web/public/guides/codex-ide-getting-started
  - apps/api/app/guides/content/codex-mobile-guide.json
  - apps/web/public/guides/codex-mobile-guide
  - apps/api/app/guides/content/codex-mobile-ios.json
  - apps/web/public/guides/codex-mobile-ios
  - apps/api/app/guides/content/codex-mobile-android.json
  - apps/web/public/guides/codex-mobile-android
  - apps/api/app/guides/content/codex-remote-setup.json
  - apps/web/public/guides/codex-remote-setup
  - apps/api/app/guides/content/codex-cloud-tasks-github.json
  - apps/web/public/guides/codex-cloud-tasks-github
  - apps/api/app/guides/content/codex-cross-device-workflow.json
  - apps/web/public/guides/codex-cross-device-workflow
  - apps/api/app/guides/content/codex-markdown-basics.json
  - apps/web/public/guides/codex-markdown-basics
  - apps/api/app/guides/content/codex-agents-md.json
  - apps/web/public/guides/codex-agents-md
  - apps/api/app/guides/content/codex-agents-md-scopes.json
  - apps/web/public/guides/codex-agents-md-scopes
  - apps/api/app/guides/content/codex-rules-and-context-files.json
  - apps/web/public/guides/codex-rules-and-context-files
  - apps/api/app/guides/content/codex-config-toml.json
  - apps/web/public/guides/codex-config-toml
  - apps/api/app/guides/content/codex-config-troubleshooting.json
  - apps/web/public/guides/codex-config-troubleshooting
  - apps/api/app/guides/content/codex-commands.json
  - apps/web/public/guides/codex-commands
  - apps/api/app/guides/content/codex-sessions-resume.json
  - apps/web/public/guides/codex-sessions-resume
  - apps/api/app/guides/content/codex-context-handoff.json
  - apps/web/public/guides/codex-context-handoff
  - apps/api/app/guides/content/codex-model-selection.json
  - apps/web/public/guides/codex-model-selection
  - apps/api/app/guides/content/codex-plan-mode.json
  - apps/web/public/guides/codex-plan-mode
  - apps/api/app/guides/content/codex-permissions.json
  - apps/web/public/guides/codex-permissions
  - apps/api/app/guides/content/codex-project-management.json
  - apps/web/public/guides/codex-project-management
  - apps/api/app/guides/content/codex-understand-codebase.json
  - apps/web/public/guides/codex-understand-codebase
  - apps/api/app/guides/content/codex-implement-feature.json
  - apps/web/public/guides/codex-implement-feature
  - apps/api/app/guides/content/codex-debugging.json
  - apps/web/public/guides/codex-debugging
  - apps/api/app/guides/content/codex-git-basics.json
  - apps/web/public/guides/codex-git-basics
  - apps/api/app/guides/content/codex-testing-review.json
  - apps/web/public/guides/codex-testing-review
  - apps/api/app/guides/content/codex-skills.json
  - apps/web/public/guides/codex-skills
  - apps/api/app/guides/content/codex-skill-resources.json
  - apps/web/public/guides/codex-skill-resources
  - apps/api/app/guides/content/codex-skill-testing.json
  - apps/web/public/guides/codex-skill-testing
  - apps/api/app/guides/content/codex-plugins.json
  - apps/web/public/guides/codex-plugins
  - apps/api/app/guides/content/codex-plugin-troubleshooting.json
  - apps/web/public/guides/codex-plugin-troubleshooting
  - apps/api/app/guides/content/codex-templates-cheatsheet.json
  - apps/web/public/guides/codex-templates-cheatsheet
  - apps/api/app/guides/content/codex-mcp.json
  - apps/web/public/guides/codex-mcp
  - apps/api/app/guides/content/codex-mcp-troubleshooting.json
  - apps/web/public/guides/codex-mcp-troubleshooting
  - apps/api/app/guides/content/codex-worktrees.json
  - apps/web/public/guides/codex-worktrees
  - apps/api/app/guides/content/codex-subagents.json
  - apps/web/public/guides/codex-subagents
  - apps/api/app/guides/content/codex-subagent-quality.json
  - apps/web/public/guides/codex-subagent-quality
  - apps/api/app/guides/content/codex-parallel-integration.json
  - apps/web/public/guides/codex-parallel-integration
  - apps/api/app/guides/content/codex-browser-images.json
  - apps/web/public/guides/codex-browser-images
  - apps/api/app/guides/content/codex-automations.json
  - apps/web/public/guides/codex-automations
  - apps/api/app/guides/content/codex-exec-scripting.json
  - apps/web/public/guides/codex-exec-scripting
  - apps/api/app/guides/content/codex-json-output.json
  - apps/web/public/guides/codex-json-output
  - apps/api/app/guides/content/codex-ci-workflows.json
  - apps/web/public/guides/codex-ci-workflows
  - apps/api/app/guides/content/codex-automation-recovery.json
  - apps/web/public/guides/codex-automation-recovery
  - apps/api/app/guides/content/codex-website-workshop.json
  - apps/web/public/guides/codex-website-workshop
  - apps/api/app/guides/content/codex-csv-workshop.json
  - apps/web/public/guides/codex-csv-workshop
  - apps/api/app/guides/content/codex-maintain-existing-project.json
  - apps/web/public/guides/codex-maintain-existing-project
  - apps/api/app/guides/content/codex-project-data-safety.json
  - apps/web/public/guides/codex-project-data-safety
  - apps/api/app/guides/content/codex-usage-efficiency.json
  - apps/web/public/guides/codex-usage-efficiency
  - apps/api/app/guides/content/codex-troubleshooting.json
  - apps/web/public/guides/codex-troubleshooting
  - apps/api/app/guides/content/codex-learning-hub.json
  - apps/web/public/guides/codex-learning-hub
---

# Codex deep content and isolated learning components

## Why

Execute the approved 60-lesson depth plan in `docs/codex-learning/depth-plan.md`. The existing 32 multilingual packs are short drafts; readers need complete exercises, failure cases, platform instructions and equivalent translations before these qualify as in-depth tutorials.

## Definition of done

- [x] Five pilot lessons (stable IDs 03, 10, 04, 11, 23) have complete authored instructions in all five locales, working materials, sources and explicit verification boundaries.
- [x] All 60 lessons are represented in the learning catalog, with unfinished entries clearly marked and no empty article links.
- [ ] Complete remaining pilot editorial and product-screen evidence checks; documentation-only platform verification stays explicitly labeled.
- [ ] The remaining 55 lessons meet the depth plan in batches of ten, with no publication implied by content generation.
- [ ] Shared-series integration follows the final compatible contract without overwriting the active Claude Code task.

## Steps

- [x] Inspect the active Claude Code task and isolate content/component ownership.
- [x] Build independent start, deliberately broken and expected todo exercises; package a download.
- [x] Verify core behavior, expected exercise failures and browser behavior at 360/390/1280 px.
- [x] Author and compile the five pilot lessons, preserving exact code across locales.
- [x] Review lesson-specific sources, illustrations, cross-links and localized browser previews.
- [ ] Expand the catalog and finish subsequent batches according to the depth plan.

## How to verify

`node --test docs/codex-learning/practice/expected/core.test.mjs`

`node tools/codex-learning/practice-browser.mjs`

`uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/build-depth.py --check`

Run the content audit, affected web/API tests and `npm run check:tasks` after compilation and integration.

## Notes

- Current checkpoint (2026-09-14): 26 deep drafts, 18 short drafts, 16 planned; 45 packs / 225 locale documents including the hub. Reading positions 01–25 plus the Skills pilot have full five-language drafts. Formal editorial acceptance remains 0/60. No PR or deployment before all 60 and shared integration pass.
- Latest evidence: 240 browser checks for the 15-lesson CLI batch and 90 for five IDE/mobile/Markdown additions; 60 additional cloud/cross-device browser checks passed. Compiler 7 tests and API 9 tests passed; current content audit 0 errors / 91 retained warnings. See progress.md for exact report links.
- Added Markdown nested-fence preservation, missing-file/fence practice checks, native Windows CLI path/backup checks, and alternative platform prerequisites. New cloud/cross-device lessons use documentation-checked UI flows and locally verified reference behavior, not claims of actual cloud/phone execution.

- Added IDs 42, 43, 16 and 44, with 5 real CLI prompt-input discovery checks and 12 offline documentation/config checks. Empty override behavior differs from a naive fallback assumption in this installed build; the lesson records actual markers and the rename-based recovery. No raw global prompt data was saved.

### Earlier checkpoints (historical, superseded by progress.md)

- 2026-09-14 user direction: finish all 60 lessons, all five locales, shared integration and acceptance before opening the PR and deploying. PR and deployment are now authorized after that completion gate. Do not open a partial-content PR or deploy unfinished drafts. Merge, content import/publication and deployment must each have their actual outcome recorded.
- 2026-09-14 follow-up: first-unit IDs 01, 02, 33, 34, 06 and 07 now have complete four-language parallel author modules plus exact-code simplified Chinese compilation. Total is 11 deep drafts, 23 short drafts, 26 unwritten; 35 packs / 175 locale documents including the hub. Forty-nine lessons still need deepening or authoring, plus editorial/product evidence and shared integration.
- Added Windows path exercise checks (4 passed), actual browser reference-edit checks (6 passed at 360/390/1280px), localized reference screenshots, complete comparison tables and source records. Model execution is explicitly distinguished from deterministic reference edits.
- Compiler now validates the full batch using the real API schema before replacing packs; a late parse failure leaves earlier packs unchanged. Catalog deep-draft flags verify source and pack hashes. Render-authors --check and 5 compiler tests passed; content audit reports 0 errors / 111 retained editorial warnings. Current full-page browser verification is in progress.

- 2026-09-14: The Claude Code tutorial task is active in worktree `1cff` and owns shared article/schema/editor files. This task owns only Codex content and isolated components. No files in that worktree were modified.
- Shared formats currently differ (`spans` versus `inlines`, code labels and language allow-list, series API). Migration needs compatibility review; do not blindly replace either schema.
- Practice evidence: expected core 3/3 passed; start and broken variants each fail the intended filter test. These failures are exercise fixtures, not failing production tests. Browser report: `docs/codex-learning/evidence/practice-browser.json`; Windows / Edge 153.0.4234.32. Mobile screenshots are responsive browser viewports, not iOS/Android device tests.
- Authored Markdown is an explicit build input. Legacy plain-text content is never automatically parsed as Markdown. Compiling drafts does not import, approve, publish or deploy them.
- Pilot drafts are in `docs/codex-learning/deep/{zh-TW,en,ja,ko}`; simplified Chinese is compiled with exact code preservation. `build-depth.py` and `expand-catalog.py` replace the old 32-lesson bootstrap, which now refuses to overwrite them.
- Browser acceptance: 90 checks across five locales, five pilots plus hub, 360/390/1280px. URL filters survive reload/history. Copy buttons now wait for hydration; Windows clipboard CRLF is normalized only when comparing the readback. Source/rendered code remains exact.
- Current checks: 136 web tests; 38 API tests passed / 5 database tests skipped; 28 tools; 4 author compiler; 3 expected core tests; skill format validation. ESLint, TypeScript, i18n, Ruff and production build pass. Content audit: 0 errors / 127 retained editorial warnings. See `docs/codex-learning/progress.md`.
- At the five-pilot checkpoint, shared integration remained with the Claude Code workstream; 27 old drafts and 28 new lessons remained. No PR, merge, import, publication or deployment performed.

- 2026-09-14 接續至 31 篇五語深化草稿（閱讀 01–30 加 Skills），正式深入驗收仍 0/60；新增 45、22、17、08、18。精確範例及還原 10 項通過，API 9 項通過，內容稽核 0 錯誤／75 警告；新增五篇整頁檢查進行中。Claude 系列已結案合併 #485，共用功能可接入，此工作目錄尚未整合 main。未開 PR、推送、匯入、發布或部署。

- 最新 checkpoint：34 篇五語深化草稿，閱讀 01–33 加 Skills；48 包／240 語言文件，剩 26 篇。新增 13、46、47；工作階段整頁 90、專案批次整頁 60、精確材料 14、功能畫面 6 項通過。47 參考圖片已目視核對且有五語圖說。API 9、編譯器 7、稽核 0 錯誤／71 警告；47 最終整頁待檢查。仍無 PR／推送／合併／匯入／發布／部署。
