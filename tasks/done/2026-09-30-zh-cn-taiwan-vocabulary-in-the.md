---
id: 2026-09-30-zh-cn-taiwan-vocabulary-in-the
title: zh-CN Taiwan vocabulary in the Codex series (61 articles, about 2,200 words)
status: done
priority: P2
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T13:31:28Z
created_at: 2026-09-30T13:31:12Z
completed_at: 2026-09-30T13:58:43Z
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/guides/content/codex-account-usage.json
  - apps/api/app/guides/content/codex-agents-md.json
  - apps/api/app/guides/content/codex-agents-md-scopes.json
  - apps/api/app/guides/content/codex-automation-recovery.json
  - apps/api/app/guides/content/codex-automations.json
  - apps/api/app/guides/content/codex-beginner-guide.json
  - apps/api/app/guides/content/codex-browser-images.json
  - apps/api/app/guides/content/codex-ci-workflows.json
  - apps/api/app/guides/content/codex-cli-getting-started.json
  - apps/api/app/guides/content/codex-cli-linux-wsl.json
  - apps/api/app/guides/content/codex-cli-macos.json
  - apps/api/app/guides/content/codex-cli-windows.json
  - apps/api/app/guides/content/codex-cloud-tasks-github.json
  - apps/api/app/guides/content/codex-commands.json
  - apps/api/app/guides/content/codex-config-toml.json
  - apps/api/app/guides/content/codex-config-troubleshooting.json
  - apps/api/app/guides/content/codex-context-handoff.json
  - apps/api/app/guides/content/codex-cross-device-workflow.json
  - apps/api/app/guides/content/codex-csv-workshop.json
  - apps/api/app/guides/content/codex-debugging.json
  - apps/api/app/guides/content/codex-desktop-getting-started.json
  - apps/api/app/guides/content/codex-exec-scripting.json
  - apps/api/app/guides/content/codex-first-project.json
  - apps/api/app/guides/content/codex-git-basics.json
  - apps/api/app/guides/content/codex-ide-getting-started.json
  - apps/api/app/guides/content/codex-implement-feature.json
  - apps/api/app/guides/content/codex-json-output.json
  - apps/api/app/guides/content/codex-learning-hub.json
  - apps/api/app/guides/content/codex-maintain-existing-project.json
  - apps/api/app/guides/content/codex-markdown-basics.json
  - apps/api/app/guides/content/codex-mcp.json
  - apps/api/app/guides/content/codex-mcp-troubleshooting.json
  - apps/api/app/guides/content/codex-mobile-android.json
  - apps/api/app/guides/content/codex-mobile-guide.json
  - apps/api/app/guides/content/codex-mobile-ios.json
  - apps/api/app/guides/content/codex-model-selection.json
  - apps/api/app/guides/content/codex-parallel-integration.json
  - apps/api/app/guides/content/codex-permissions.json
  - apps/api/app/guides/content/codex-plan-mode.json
  - apps/api/app/guides/content/codex-platforms-guide.json
  - apps/api/app/guides/content/codex-plugin-troubleshooting.json
  - apps/api/app/guides/content/codex-plugins.json
  - apps/api/app/guides/content/codex-project-data-safety.json
  - apps/api/app/guides/content/codex-project-management.json
  - apps/api/app/guides/content/codex-prompting.json
  - apps/api/app/guides/content/codex-remote-setup.json
  - apps/api/app/guides/content/codex-rules-and-context-files.json
  - apps/api/app/guides/content/codex-sessions-resume.json
  - apps/api/app/guides/content/codex-skill-resources.json
  - apps/api/app/guides/content/codex-skill-testing.json
  - apps/api/app/guides/content/codex-skills.json
  - apps/api/app/guides/content/codex-subagent-quality.json
  - apps/api/app/guides/content/codex-subagents.json
  - apps/api/app/guides/content/codex-templates-cheatsheet.json
  - apps/api/app/guides/content/codex-terminal-paths.json
  - apps/api/app/guides/content/codex-testing-review.json
  - apps/api/app/guides/content/codex-troubleshooting.json
  - apps/api/app/guides/content/codex-understand-codebase.json
  - apps/api/app/guides/content/codex-usage-efficiency.json
  - apps/api/app/guides/content/codex-website-workshop.json
  - apps/api/app/guides/content/codex-worktrees.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/news-2026-batch-4/translation-corrections.json
---

# zh-CN Taiwan vocabulary in the Codex series (61 articles, about 2,200 words)

## Why

The zh-CN locale of the Codex series was written with Taiwan vocabulary: a scan on
2026-09-30 counted about 2,200 occurrences in 61 packs (档案 597, 设定 371, 专案 310,
资料夹 270, 终端机 259, 帐号 217, …). Mainland readers write 文件, 设置, 项目, 文件夹, 终端,
账号. The owner chose to fix the whole series now (2026-09-30); the other 73 articles have a
task of their own. The AI index's five stale ja/ko link texts are fixed in the same pass.

## Definition of done

- [x] Every Codex pack's zh-CN uses mainland vocabulary; code blocks, code inlines, URLs and
      the other four locales are byte-identical.
- [x] zh-CN links to the retitled Codex articles carry the new titles.
- [x] AI index link texts match their targets' titles (`align_links.py`).
- [ ] Packs re-imported on the host after the deploy (listed under "after merge" in the PR).

## Steps

- [x] Mechanical glossary pass (script in the workspace), longest compounds first
- [x] Per-article review by three opus zh-CN agents, corrections through `apply_corrections.py`
- [x] Link texts to retitled articles
- [x] Checks

## What was done (2026-09-30)

- Mechanical pass over reader text, longest compounds first: 设定档→配置文件, 档案总管→文件资源管理器,
  档案→文件, 专案→项目, 资料夹→文件夹, 终端机→终端, 帐号→账号, 设定→设置, 预设→默认, 支援→支持,
  网路→网络, 透过→通过, 伺服器→服务器, 登入→登录, 连结→链接, 视窗→窗口, 装置→设备, 程式码→代码, and more.
  Code blocks, code inlines, backtick spans, URLs and machine fields were never touched.
- Three reviewers read every changed sentence, split into three groups of about 20 packs. They
  returned 3,405 context corrections and 172 path-addressed ones. Examples: 设置 vs 配置 for
  configuration nouns, 程序 vs 代码, 资料 as data vs materials, 指令 vs 命令, 储存库→仓库, 远端→远程.
  All were applied through `apply_corrections.py`, which records them in `translation-corrections.json`.
- Second pass:
  - article-inline and site-link anchor texts inside the Codex packs (61 strings);
  - code-block captions (`label` is reader text shown above a block; 155 strings). `code` itself
    is unchanged.
- The anchors are prose ("终端机与路径"), not titles. No zh-CN link anywhere on the site had text
  equal to an old Codex title, so there was nothing to align there.
- Checks:
  - the zh-TW, en, ja and ko locales and every code node (excluding `label`) are identical to
    before, apart from the AI index's intended ja/ko link texts;
  - a scan for 档案 资料夹 专案 终端机 帐号 设定 预设 支援 网路 透过 软体 萤幕 资讯 伺服器 登入 连结 视窗 选单
    游标 记忆体 硬碟 装置 外挂 程式 远端 使用者 储存 介面 finds none left in Codex zh-CN;
  - 文档 appears 209 times, against 230 of 文件 in zh-TW, so no file→文档 drift;
  - `pack_cli lint --kind life` reports 0 errors.
- Kept as they are: quotes and official product or UI names, where the source wording rules.
