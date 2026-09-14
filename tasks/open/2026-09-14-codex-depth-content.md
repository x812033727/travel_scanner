---
id: 2026-09-14-codex-depth-content
title: Codex deep content and isolated learning components
status: in-progress
priority: P2
area: docs
owner: codex-unit-f-fc2e
claimed_at: 2026-09-14T12:20:08Z
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
- [x] Deepen Unit D (09, 42, 43, 16, 44), label 32 existing blocks, add four examples and verify nested Markdown and 13 document/configuration reference cases.
- [x] Deepen Unit E (45, 22, 17, 08, 18), label 29 existing blocks, add six input/record examples and verify the 16-case reference suite (10 E-specific checks).
- [x] Deepen Unit F (13, 46, 47, 20, 19, 21), label 38 existing blocks, add eight examples and verify 13 Git/review plus 20 reference checks (10 F-specific).
- [x] Deepen Unit G (48, 49, 24, 50, 51), preserve 28 original code blocks, add seven examples and verify ten skill/template reference checks; lesson 23 retains representative evidence.
- [x] Deepen Unit H (25, 52, 27, 28, 53, 54), correct MCP surface usage, preserve 44 original code blocks, add three examples and verify 25 MCP/Git/Node reference checks.
- [ ] Continue targeted depth review for the remaining 12 lessons, starting with Unit I (26, 29, 30, 55, 56, 57).
- [ ] Complete remaining full-text five-language editorial acceptance and representative product UI evidence.
- [ ] Complete final integrated browser acceptance for all 60 lessons and the hub. The preview-start restriction remains unresolved.
- [ ] After all acceptance gates pass, proceed with the already authorized PR, exact-head CI/merge, guarded import/publication/deployment and public verification. No partial PR.

## Unit H revision

After 1cb4df54, revised all six H lessons in four author languages and five compiled locales. Corrected CLI-only /mcp versus desktop/IDE settings and task activity; added dirty-worktree removal refusal, checkout attribution, a separate duplicate-ID fault copy and exact integration SHA comparison. All 44 original copyable blocks remain in order; three labelled blocks added. Original images, sources and shared series_data unchanged.

Evidence: docs/codex-learning/evidence/unit-h-depth-review.json. Twenty-five Windows reference checks pass (MCP 6, worktree 7, subagent reference 6, integration 6), alongside integrity 60/300, 9 API, 9 compiler, five catalogues and affected-tool Ruff. Audit is 0 errors/21 warnings. No model/subagent, role activation, OAuth, product UI or other-OS execution. Coverage is 48 unique lessons, 12 pending (I next). Final acceptance remains 0/60, with the preview restriction unresolved; no partial PR, publication or deployment.

## Unit G revision

After e191e927, revised 48/49/24/50/51 in four author languages and five compiled locales. Added wrong-directory recovery, a second input, explicit-only invocation policy with scoped restoration, independent plugin source markers, three fictional diagnostic cases and an adapted read-only request. Corrected the old Bug-template example to the actual broken Completed-filter scenario. All 28 original code blocks, sources, images and the six-file base ZIP remain unchanged; seven new code blocks have labels.

docs/codex-learning/evidence/unit-g-depth-review.json records ten Windows Node reference checks, including wrong-cwd failure/recovery, distinct 3/1/2 versus 2/2/0 inputs, eight baseline skill tests, the seven-pass/one-failure deliberate defect and restoration, and expected/broken template commands with preserved source bytes. No skill installation/invocation, policy behavior, plugin/OAuth/service operation or browser run occurred. New policy and plugin cases remain documented exercises, not product-test results.

Integrity 60/300, 9 API, 9 compiler, five shared catalogues and affected-tool Ruff pass. The first expanded English pass produced four extra length advisories; repeated wording was condensed while preserving requirements and recovery steps. Final audit returns to 0 errors/23 warnings, without threshold changes. No shared series_data/source-list edits.

Targeted coverage is 42 unique lessons with 18 pending; next H: 25/52/27/28/53/54. All full-text five-language and final browser acceptance remain open (0/60). No partial PR, import, publication or deployment.

## Unit F revision

After 9c474d68, revised 13/46/47/20/19/21 in four author languages and rebuilt the matching five-language packs. Added two-project/three-task identity, source-backed failure-path reading, a duplicate-title defect rejected by regression tests, uncompleting and empty-list checks, staged-versus-unstaged MM snapshots, and accurate Review/final-version scope. All 38 original code blocks retain exact contents and gain input labels; eight new blocks are shared across locales. Images and source metadata remain unchanged.

Evidence is in docs/codex-learning/evidence/unit-f-depth-review.json. Thirteen Git/review checks and 20 reference checks pass; the latter contain 10 F-specific and 10 existing E checks. The faulty deduplication variant passes the original three tests but fails the new identity case; restoration recovers six passes. Staged Plan and unstaged Compare are independently verified, and an unchanged HEAD with dirty files is shown to invalidate old passing results. Isolated reference exercises do not establish product UI or model execution.

Integrity 60/300, 9 API, 9 compiler, five shared catalogues and affected-tool Ruff pass. Audit is 0 errors/23 warnings; three earlier minimum-length advisories resolve through meaningful Japanese/Korean debugging and Korean Git explanations, without changing thresholds. A first evidence-hash assertion stopped on Windows CRLF versus the compiler's LF normalization; canonical-text comparison then passed. No shared series_data or deep source-list writes occurred.

Targeted coverage is 37 unique lessons, 23 pending; next G: 48/49/24/50/51, with 23 already revised. Added/changed sections were compared across languages, not signed off as a full-text editorial review. All final acceptance remains open (0/60), including the preview-start restriction. No actual project/archive UI, model Review, GitHub push/PR or browser run. No partial PR, import, publication or deployment.

## Unit E revision

After b0bf7fa4, revised sessions, context, model selection, Plan and permission drafts in all five locales. Evidence: docs/codex-learning/evidence/unit-e-depth-review.json. Added a read-only fork/picker exercise with shared-file limits, post-compact fresh reads, fictional invalid-comparison cases, actual Power/model/effort controls, a revision-only Plan prompt and permission evidence records. Twenty-nine original code blocks labeled, six new blocks added; original code/images/source lists retained.

The reference suite passes 16 checks (10 Unit E, 6 other existing cases); other checks do not count as new targeted lessons. Actual CLI help and official selected sections were inspected. No interactive fork/resume/compact, model run/comparison, OS sandbox, settings change or browser verification. Full integrity (60/300), 9 API, 9 compiler and five shared catalogues pass; audit stays 0 errors/26 warnings. Shared series_data/source metadata remain unchanged.

Targeted coverage is now 31 unique lessons with 29 pending, next F: 13/46/47/20/19/21. All full-text five-language acceptance and final browser acceptance remain open (0/60). No partial PR, import, publication or deployment; the prior preview auto-review rejection remains unresolved.

## Unit D revision

After cf4929f6, revised five MD/rules/configuration drafts and all locale packs. Evidence: docs/codex-learning/evidence/unit-d-depth-review.json. Added nested Markdown with a short-closing-fence failure/repair, a five-case rule-discovery/compliance record, external document backups and actual-result handoff fields, three setting-evidence cases and an unchecked-key parser boundary. Thirty-two original code blocks now have labels and four new blocks were added; original copyable content remains intact.

Thirteen exact document/configuration practice checks pass; four original faults return 1, fixed copies return 0 and the unchecked extra key demonstrates the narrow scope. Mistune AST checks preserve literal inner fences, reproduce and repair the short closing fence. The original macOS preview shortcut is retained after actual current VS Code page review; no editor preview execution. Prior rule-discovery sample hashes still match, without claiming a new diagnostic or model run.

Latest integrity (60/300), API (9), compiler (9), shared catalogues (5), and affected-tool Ruff pass; audit stays 0 errors/26 warnings. Source metadata and shared series_data are unchanged. Targeted coverage is 26 unique lessons, 34 pending; next E: 45/22/17/08/18. Full five-language final acceptance and browser acceptance remain open (0/60). No partial PR, import, publication or deployment.

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
