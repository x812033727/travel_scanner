---
id: 2026-09-20-codex-learning-finalize-release
title: Finish, publish, and deploy the Codex learning center
status: done
priority: P1
area: docs
owner: gpt-6
claimed_at: 2026-09-20T01:16:22Z
created_at: 2026-09-20T01:15:00Z
completed_at: 2026-09-20T07:31:03Z
branch: codex/codex-learning-finalize
depends_on: []
scope:
  - apps/api/app/guides/content/codex-learning-hub.json
  - apps/api/app/guides/content/codex-desktop-getting-started.json
  - apps/api/app/guides/content/codex-first-project.json
  - apps/api/app/guides/content/codex-debugging.json
  - apps/api/app/guides/content/codex-mcp.json
  - apps/api/app/guides/content/codex-browser-images.json
  - apps/api/app/guides/content/codex-worktrees.json
  - apps/api/app/guides/content/codex-subagents.json
  - apps/api/app/guides/content/codex-automations.json
  - apps/api/app/guides/content/codex-plugin-troubleshooting.json
  - apps/api/app/guides/content/codex-templates-cheatsheet.json
  - apps/api/app/guides/content/codex-mcp-troubleshooting.json
  - apps/api/app/guides/content/codex-parallel-integration.json
  - apps/api/app/guides/content/codex-account-usage.json
  - apps/api/app/guides/content/codex-agents-md-scopes.json
  - apps/api/app/guides/content/codex-agents-md.json
  - apps/api/app/guides/content/codex-automation-recovery.json
  - apps/api/app/guides/content/codex-beginner-guide.json
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
  - apps/api/app/guides/content/codex-exec-scripting.json
  - apps/api/app/guides/content/codex-git-basics.json
  - apps/api/app/guides/content/codex-ide-getting-started.json
  - apps/api/app/guides/content/codex-implement-feature.json
  - apps/api/app/guides/content/codex-json-output.json
  - apps/api/app/guides/content/codex-maintain-existing-project.json
  - apps/api/app/guides/content/codex-markdown-basics.json
  - apps/api/app/guides/content/codex-mobile-android.json
  - apps/api/app/guides/content/codex-mobile-guide.json
  - apps/api/app/guides/content/codex-mobile-ios.json
  - apps/api/app/guides/content/codex-model-selection.json
  - apps/api/app/guides/content/codex-permissions.json
  - apps/api/app/guides/content/codex-plan-mode.json
  - apps/api/app/guides/content/codex-platforms-guide.json
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
  - apps/api/app/guides/content/codex-terminal-paths.json
  - apps/api/app/guides/content/codex-testing-review.json
  - apps/api/app/guides/content/codex-troubleshooting.json
  - apps/api/app/guides/content/codex-understand-codebase.json
  - apps/api/app/guides/content/codex-usage-efficiency.json
  - apps/api/app/guides/content/codex-website-workshop.json
  - apps/api/app/guides/series_data
  - apps/api/tests/test_codex_learning.py
  - apps/web/public/guides/codex-learning-hub
  - apps/web/public/guides/codex-desktop-getting-started
  - apps/web/public/guides/codex-first-project
  - apps/web/public/guides/codex-debugging
  - apps/web/public/guides/codex-mcp
  - apps/web/public/guides/codex-browser-images
  - apps/web/public/guides/codex-worktrees
  - apps/web/public/guides/codex-subagents
  - apps/web/public/guides/codex-automations
  - apps/web/public/guides/codex-plugin-troubleshooting
  - apps/web/public/guides/codex-templates-cheatsheet
  - apps/web/public/guides/codex-mcp-troubleshooting
  - apps/web/public/guides/codex-parallel-integration
  - apps/web/public/guides/codex-website-workshop
  - apps/web/components/codex-learning
  - apps/web/lib/codex-learning
  - apps/web/e2e/codex-learning.spec.ts
  - docs/codex-learning
  - tools/codex-learning
  - tasks/open/2026-09-14-codex-learning-series.md
  - tasks/open/2026-09-14-codex-depth-content.md
---

# Finish, publish, and deploy the Codex learning center

## Why

PR #525 merged the five-language 60-lesson Codex learning center and its shared UI, but the final editorial record still marks twelve lessons and the hub as changes-required. The final integrated browser run, production import/publication, guarded deployment, and public five-language verification also remain outstanding. Finish those gates on current `main` without changing unrelated guide work.

## Definition of done

- [x] Resolve every recorded editorial correction for lessons 03, 06, 20, 25, 26, 27, 28, 29, 50, 51, 52, and 54 in all five locales.
- [x] Complete and verify the missing checkpoint-3 editorial record so all 60 lessons have a current five-language disposition.
- [x] Replace the sparse five-language hub body with searchable/filterable usage guidance, ten A-J study routes, publication-gated starting points, state/evidence labels, and current official-source dates.
- [x] Rebuild the generated author files and content packs, preserving code, source, image, slug, and navigation contracts.
- [x] Pass affected content, compiler, API, frontend, browser, build, task, and import checks, including 360/390/1280 responsive page acceptance.
- [x] Open a reviewable PR only after local completion, obtain green CI, merge the exact reviewed head, and verify the remote merge.
- [x] Back up and deploy the exact green merged SHA, import and publish the hub plus all 60 lessons in five locales, and verify public signed-out pages and navigation.

## Steps

- [x] Recheck current official product documentation and implement the editorial fixes.
- [x] Rebuild, audit, and complete the missing editorial evidence.
- [x] Run local API/import and browser acceptance against the final content.
- [x] Create, validate, and merge the finalization PR.
- [x] Perform the guarded production release, publish content, and verify the live site.

## How to verify

Use the commands in `docs/codex-learning/README.md`, the repository-wide affected checks from `AGENTS.md`, a disposable full-series import, and the automated responsive browser suite. Record exact commit, CI, backup, deployment, import/publication, and public URL evidence separately.

## Notes

The earlier broad parent task overlaps active guide/API work. This task uses exact Codex pack paths and the existing Codex-specific source, UI, evidence, and asset directories. Preserve the untracked `.codex/codex-learning-research/` and `.codex/environments/` directories.

All official product facts were rechecked against OpenAI documentation on 2026-09-20. The rebuilt set contains the hub plus 60 lesson packs, each with five locales and a rendered summary block; the remaining gates are final local acceptance, PR/CI/merge, and production publication.

Final local acceptance passed: Next production build generated 308 static pages; frontend Vitest passed 3,217 tests; API Pytest passed 3,980 tests with 343 integration skips under UTF-8 mode; tool tests passed 75 with one Windows-only skip; Codex reference checks passed 94; and the browser report passed 915 page checks with five recorded first-attempt fixture retries. This host has neither Docker nor PostgreSQL, so the database-difference `guides-import --dry-run` stopped at the expected loopback connection refusal after loading all 61 whitelisted packs. Repeat that read-only dry-run against production after deployment and before `--publish`.

PR #578 merged the completed 61-pack series, and PR #583 merged the tutorial-hub query fix; their reviewed commits and required checks passed. The guarded production release published 300 article locale documents and 5 hub locale documents, then deployed green main SHA `6532eaa6e7e9d5a34b94cfe8f8a62ed2e0fba9a1`. A fresh 123,585,075-byte PostgreSQL custom-format backup passed `pg_restore --list`, and the database/Redis containers were preserved. The post-deploy import preview reports 305 `unchanged` documents and no pending publication. Signed-out Edge deep QA passed 300 articles, 5 hubs and 317 checks; 390px/1280px samples and Claude Code hub filter reload also passed. Production Codex link findings are zero in every locale. See `docs/codex-learning/production-release-2026-09-20.md` and its structured receipt for precise hashes, retry counts and untested devices.
