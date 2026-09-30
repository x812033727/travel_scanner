---
id: 2026-09-30-zh-cn-taiwan-vocabulary-in-the
title: zh-CN Taiwan vocabulary in the Codex series (61 articles, about 2,200 words)
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T13:31:28Z
created_at: 2026-09-30T13:31:12Z
completed_at:
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

- [ ] Every Codex pack's zh-CN uses mainland vocabulary; code blocks, code inlines, URLs and
      the other four locales are byte-identical.
- [ ] zh-CN links to the retitled Codex articles carry the new titles.
- [ ] AI index link texts match their targets' titles (`align_links.py`).
- [ ] Packs re-imported on the host after the deploy.

## Steps

- [ ] Mechanical glossary pass (script in the workspace), longest compounds first
- [ ] Per-article review by three opus zh-CN agents, corrections through `apply_corrections.py`
- [ ] Link texts to retitled articles
- [ ] Checks
