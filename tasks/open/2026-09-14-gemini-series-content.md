---
id: 2026-09-14-gemini-series-content
title: Gemini series additional tutorials and hub
status: in-progress
priority: P2
area: docs
owner: codex-gemini-series
claimed_at: 2026-09-14T06:01:04Z
created_at: 2026-09-14T06:01:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/gemini-guide.json
  - apps/web/public/guides/gemini-guide
  - apps/api/app/guides/content/gemini-beginner-guide.json
  - apps/web/public/guides/gemini-beginner-guide
  - apps/api/app/guides/content/gemini-web-desktop-guide.json
  - apps/web/public/guides/gemini-web-desktop-guide
  - apps/api/app/guides/content/gemini-mac-app-guide.json
  - apps/web/public/guides/gemini-mac-app-guide
  - apps/api/app/guides/content/gemini-ios-app-guide.json
  - apps/web/public/guides/gemini-ios-app-guide
  - apps/api/app/guides/content/gemini-prompt-writing-guide.json
  - apps/web/public/guides/gemini-prompt-writing-guide
  - apps/api/app/guides/content/gemini-file-analysis-guide.json
  - apps/web/public/guides/gemini-file-analysis-guide
  - apps/api/app/guides/content/gemini-canvas-guide.json
  - apps/web/public/guides/gemini-canvas-guide
  - apps/api/app/guides/content/gemini-spark-workflows-guide.json
  - apps/web/public/guides/gemini-spark-workflows-guide
  - apps/api/app/guides/content/gemini-connected-apps-guide.json
  - apps/web/public/guides/gemini-connected-apps-guide
  - apps/api/app/guides/content/gemini-cli-getting-started.json
  - apps/web/public/guides/gemini-cli-getting-started
  - apps/api/app/guides/content/gemini-cli-authentication.json
  - apps/web/public/guides/gemini-cli-authentication
  - apps/api/app/guides/content/gemini-cli-command-reference.json
  - apps/web/public/guides/gemini-cli-command-reference
  - apps/api/app/guides/content/gemini-cli-files-and-shell.json
  - apps/web/public/guides/gemini-cli-files-and-shell
  - apps/api/app/guides/content/gemini-cli-sessions-context.json
  - apps/web/public/guides/gemini-cli-sessions-context
  - apps/api/app/guides/content/gemini-cli-coding-workflow.json
  - apps/web/public/guides/gemini-cli-coding-workflow
  - apps/api/app/guides/content/gemini-markdown-basics.json
  - apps/web/public/guides/gemini-markdown-basics
  - apps/api/app/guides/content/gemini-cli-gemini-md.json
  - apps/web/public/guides/gemini-cli-gemini-md
  - apps/api/app/guides/content/gemini-cli-memory-hierarchy.json
  - apps/web/public/guides/gemini-cli-memory-hierarchy
  - apps/api/app/guides/content/gemini-cli-settings.json
  - apps/web/public/guides/gemini-cli-settings
  - apps/api/app/guides/content/gemini-cli-permissions-sandbox.json
  - apps/web/public/guides/gemini-cli-permissions-sandbox
  - apps/api/app/guides/content/gemini-cli-custom-commands.json
  - apps/web/public/guides/gemini-cli-custom-commands
  - apps/api/app/guides/content/gemini-cli-mcp-extensions.json
  - apps/web/public/guides/gemini-cli-mcp-extensions
  - apps/api/app/guides/content/gemini-cli-agent-skills.json
  - apps/web/public/guides/gemini-cli-agent-skills
  - apps/api/app/guides/content/gemini-cli-hooks.json
  - apps/web/public/guides/gemini-cli-hooks
  - apps/api/app/guides/content/gemini-cli-subagents.json
  - apps/web/public/guides/gemini-cli-subagents
  - apps/api/app/guides/content/gemini-cli-headless-automation.json
  - apps/web/public/guides/gemini-cli-headless-automation
  - apps/api/app/guides/content/gemini-cli-troubleshooting.json
  - apps/web/public/guides/gemini-cli-troubleshooting
  - apps/api/app/guides/content/gemini-api-files-structured-output.json
  - apps/web/public/guides/gemini-api-files-structured-output
  - apps/api/app/guides/content/gemini-api-cost-errors-guide.json
  - apps/web/public/guides/gemini-api-cost-errors-guide
  - apps/api/app/guides/content/gemini-api-document-assistant.json
  - apps/web/public/guides/gemini-api-document-assistant
---

# Gemini series additional tutorials and hub

## Why

Complete the additional Gemini tutorials and hub in the approved 1 + 50 series, preserving existing slugs and coordinating the 20 existing batch-05 topics. Every lesson needs original Traditional Chinese prose, steps, examples, expected results, FAQs, official sources, images and navigable links.

## Definition of done

- [x] All 51 pages are complete, source-checked and illustrated; no empty or coming-soon articles.
- [x] Every ordinary lesson has 1,800–3,000 body characters; the command lookup has a documented length exception.
- [x] All links, code/config examples and images pass applicable checks.
- [ ] Publish the exact series only after acceptance, with children verified before the hub.

## Steps

- [x] Prepare CLI/API manuscripts 29–50, source records and example files.
- [x] Prepare device/getting-started manuscripts 01–08 and current Taiwan pricing evidence.
- [x] Finish manuscripts 09–28 and the hub.
- [x] Create and visually review all topic-specific covers and instructional diagrams.
- [x] Finish code/config execution checks, editorial review and cross-link validation.
- [ ] Complete pack dry-run, scoped publication and public/browser/sitemap verification.

## How to verify

Compile manuscripts with `apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py`. Validate the full catalogue and packs with `node tools/gemini-series.mjs check`; use the existing API content-pack lint/ingest dry run. Preserve CLI memory/command and SDK validation records under `docs/gemini-series/`; follow the series release tool and journal for any publication.

## Notes

2026-09-14: CLI 0.59.0 actual loader yields 45 stable built-ins with optional features enabled; `/memory reload` has `refresh` alias and `/tasks` replaces old documentation's `/shells`. Actual memory manager tests cover loading, reload and scope. API examples use google-genai 2.23.0 / @google/genai 2.22.0; four offline Python SDK/validation tests pass, no live Google API credentials are available. Taiwan Google One browser verification found Plus NT$165, Pro NT$650, Ultra 5x NT$3,300 and 20x NT$6,500 per month. Windows now has an official native download and is documented separately from web shortcuts and Mac. Apple Taiwan storefront currently requires iOS/iPadOS 17.4. All 51 packs and 102 original illustrations are complete and visually reviewed. Syntax checks cover 109 snippets. Full local import and desktop/mobile browser checks passed. Integration with latest main and production release remain pending.

2026-09-14 integration acceptance: reconciled with main f5b814cb and preserved Claude Code shared blocks/series. The 51 complete packs and 102 reviewed illustrations pass catalogue, length, assets and links; 109 snippets and four deterministic executions pass. Final production-build Playwright: 8 passed (all 50 lessons on desktop/mobile, no-JavaScript 360px, copy, anchors, six searches, unpublished-hub gate). API: 32 passed / 16 PostgreSQL-dependent skipped locally; web integration: 68 passed plus final 34 UI tests; tools: 48 passed. Build, lint, typecheck, i18n, Ruff and mypy pass. CI and production publication are still pending. Existing twenty batch-05 slugs are reused; the comparison is labeled official-feature comparison and reproducible test procedure, without fabricated benchmark results.
