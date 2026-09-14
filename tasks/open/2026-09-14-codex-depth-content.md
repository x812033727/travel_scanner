---
id: 2026-09-14-codex-depth-content
title: Codex deep content and isolated learning components
status: in-progress
priority: P2
area: docs
owner: codex-unit-c-fc2e
claimed_at: 2026-09-14T11:52:25Z
created_at: 2026-09-14T02:33:43Z
completed_at:
branch: codex/codex-learning-complete
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

Complete the approved 60-lesson, five-language learning series while keeping editorial acceptance, executable examples, browser evidence and publication distinct. The latest 60-lesson draft checkpoint is d3f28a25; earlier counts in this task's Git history are superseded by docs/codex-learning/progress.md.

## Definition of done

- [x] All 60 lessons plus the hub are authored and compiled into 305 locale documents.
- [x] The catalog, stable IDs/slugs, ten units and published-only navigation are implemented.
- [x] Shared article/API/editor integration is complete in this branch after the Claude Code PR #485 merge; the other task's worktree was not edited.
- [x] Complete fictional practice materials and reference checks, with platform and model-execution limits recorded.
- [x] Run a targeted Japanese terminology review across the series and correct 26 affected lessons without changing copyable code or link targets.
- [x] Visually inspect six existing 390/1280px practice screenshots and provide accurate five-language alternative text and dimension captions.
- [x] Deepen five representative drafts with independent comparison, host identification, rule-condition checks, CLI input/resume details and skill missing-material recovery; compile matching five-language packs and record the exact targeted review scope.
- [x] Deepen Unit A (01, 02, 33, 34, 06, 07) and the remaining Unit B drafts (05, 35, 36, 37, 14), label 58 existing code blocks, add two path examples, and verify isolated Windows/Node reference exercises.
- [x] Deepen Unit C (38, 39, 40, 15, 41), label 15 existing code blocks, add six examples, and verify isolated Git/Node cases for complete diffs and incomplete handoffs.
- [ ] Continue targeted depth review for the remaining 39 lessons, starting with Unit D (09, 42, 43, 16, 44); representative 10 already has a targeted record.
- [ ] Complete remaining full-text five-language editorial acceptance and representative product UI evidence.
- [ ] Complete final integrated browser acceptance for all 60 lessons and the hub. The preview-start restriction remains unresolved.
- [ ] After all acceptance gates pass, proceed with the already authorized PR, exact-head CI/merge, guarded import/publication/deployment and public verification. No partial PR.

## Unit C revision

After 07761788, revised five mobile/Remote/cloud/handoff drafts and all five locale packs. Evidence: docs/codex-learning/evidence/unit-c-depth-review.json. Host markers require a fresh read without leaking the expected value; remote access, pairing and task state are separate. The cloud PR template records actual results, and final inspection includes already committed changes. Seven handoff queries cover staged, unstaged and untracked work; ignored material requires separate handling.

Independent temporary Git/Node reference checks passed: same HEAD can coexist with missing source work; a committed fix leaves plain git diff empty while baseline comparison identifies core.mjs. Tests change from 2 pass/1 fail to 3 pass/0 fail with the original test unchanged. No physical mobile, Remote, cloud task, Handoff, new image or browser execution is claimed. Official source body hashes, exact review scope, code preservation and two intentional code replacements are recorded.

Latest integrity (60/300), API content (9), compiler (9), and five shared catalogue checks pass. Audit remains 0 errors/26 warnings after trimming redundant English mobile prose without losing conditions. Source metadata and shared series_data remain unchanged. Targeted coverage is 21 unique lessons; 39 pending, next Unit D. Full-text five-language and final browser acceptance remain open (0/60). No partial PR, import, publication or deployment.

## Unit A and B revision

After a80bc077, revised eleven modules and their five-language packs. Unit A adds capability and usage exercises, relative-path recovery, precise input labels, and independent reference copies. Unit B adds Windows support prerequisites and a script-block guard for new folders, a macOS missing-file exercise, WSL distribution selection, saved-session/file distinctions, and explicit IDE selection/file attachment plus saved-file checks.

Evidence: docs/codex-learning/evidence/unit-a-depth-review.json and unit-b-depth-review.json. Windows path checks passed; a second execution of the Windows creation block failed as intended without overwriting its file. The exact IDE reference function produces 2 pass/1 fail -> 3 pass/0 fail -> restored 2 pass/1 fail with original tests unchanged. First-project data tests also pass with an intentionally wrong heading, so they do not establish visual correctness. All fixture originals remained unchanged. No install/auth changes, model request, IDE UI, Remote, preview or screenshot execution.

Final scope inspection found that the compiler projected the added IDE source into five API series_data files held by the active Claude tutorial task. Reverted only those generated additions and kept the source as an explicit link in the IDE article body. The five projections and existing source metadata remain unchanged; do not claim the other task has released that shared scope.

Series integrity passed for 60 lessons/300 documents, with 9 API and 9 compiler tests. Audit remains 0 errors/26 warnings after Unit B; the one new advisory is Unit A account-usage English length. Five-language new/changed sections are aligned, including generated Simplified Chinese; no full-text editorial acceptance is claimed. There are now 16 unique lessons with targeted depth revisions and 44 others pending. Final acceptance remains 0/60. Earlier sections below preserve their own historical counts.

## Representative depth revision

After planning checkpoint 2011e83b, revised lessons 03, 04, 10, 11 and 23 in four author languages and rebuilt all five locale packs. Added independent backup/comparison, a host-side Remote marker, instruction-condition evidence, CLI flags/resume behavior, and missing-material skill recovery. New sections are aligned across languages; this is not full-text editorial sign-off.

docs/codex-learning/evidence/representative-depth-review.json records final source/pack hashes, seven official document bodies reviewed, read-only CLI help checks, and isolated practice tests. Expected: 3 pass; broken: 2 pass/1 fail; missing test file: error; restored: 3 pass. No model, skill invocation, Remote pairing, browser preview or new screenshots.

Series integrity passed for all 60 lessons/300 documents; 9 API content tests and 9 compiler tests passed. All original code, source lists and image blocks in the five revised packs remain intact. Audit: 0 errors/25 warnings, including one added English-length advisory for the necessary skill failure/recovery explanation. Full editorial review of the representatives and remaining 55 lessons, product evidence and browser acceptance stay open. No partial PR or deployment.

## Earlier review evidence

docs/codex-learning/evidence/editorial-review.json records this review's precise scope and image hashes. Relative to d3f28a25, all 300 lesson documents retain identical executable code, article/external link targets and sources. Non-Japanese prose remains identical; image text is localized.

The Japanese pass separates AI agents from API/network proxies, corrects executable filenames and function/global/resource terminology, and repairs mixed Chinese wording. This is a targeted terminology review, not a claim that every translation has received full final editorial acceptance.

Six existing image artifacts were inspected: baseline todo, first-project reference and prompting reference, each at 390 and 1280px. They show fictional practice data and Windows Edge responsive viewports. No new browser session or product UI capture was performed.

After compilation: series integrity passed for 60 lessons/300 documents; 9 Codex API content tests and 9 compiler tests passed. Content audit remains 0 errors and 24 advisory warnings. Prior broader checks remain documented under their actual scope in progress.md.

## Remaining work and blocker

The latest user instruction repeats the existing completion gate: finish everything before opening a PR and deploying. It does not change the unfinished browser/product-evidence status.

The local Next preview startup was rejected by automatic approval review with blocked by policy, including a loopback-only retry, with no specific reason supplied. No alternate server, launcher, port or rendering route was used to bypass that rejection. Final acceptance remains 0/60; the existing failed browser report is preserved.

Full editorial review and product-screen evidence still need completion. macOS/Linux/iOS/Android instructions retain their documentation-only labels; responsive Windows screenshots do not establish physical-device testing.

The parent task remains tasks/open/2026-09-14-codex-learning-series.md. This content task is released after saving the bounded review checkpoint so its remaining work stays visible to the next run. No push, PR, import, publication or deployment has occurred.

## How to verify

Run from the repository root:

- python tools/codex-learning/render-authors.py --check
- uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/build-depth.py --check
- uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/check-series.py
- uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python -m unittest discover -s tools/codex-learning -p test_compiler.py
- apps/api/.venv/Scripts/python.exe -m pytest apps/api/tests/test_codex_learning.py -q
- apps/api/.venv/Scripts/python.exe tools/codex-learning/audit.py
- npm run check:tasks

Preview commands and full implementation history are in docs/codex-learning/README.md and progress.md. Do not substitute static checks or historical browser results for the blocked final preview.
