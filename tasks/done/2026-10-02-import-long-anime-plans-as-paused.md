---
id: 2026-10-02-import-long-anime-plans-as-paused
title: Import long anime plans as paused admin series
status: done
priority: P2
area: api
owner: codex-root
claimed_at: 2026-10-02T08:03:01Z
created_at: 2026-10-02T08:01:07Z
completed_at: 2026-10-02T08:56:39Z
branch: codex/anime-planning-import
depends_on: []
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/messages.py
  - apps/api/app/video_automation/planning.py
  - apps/api/app/video_automation/planning_cli.py
  - apps/api/migrations/versions/0121_video_series_planning.py
  - apps/api/tests/test_video_anime_planning.py
  - apps/api/tests/test_video_anime_planning_cli.py
  - apps/api/tests/test_video_anime_planning_guards.py
  - apps/api/tests/test_video_anime_planning_messages.py
  - apps/api/tests/test_migration_0121_video_series_planning.py
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - ops/video/import_anime_plan.py
  - docs/videos/ANIME-PLANNING-IMPORT.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Import long anime plans as paused admin series

## Why

The owner explicitly asked to create The Borrowed Dawn in the real admin after its separate planning PR #1113 was merged. Existing ordinary drama creation rejects its 22-minute body, cannot represent ensemble leads or anime category on a series, and applies short-drama retention rules to the authored chapters. Provide a faithful planning-only import rather than shortening the work or starting production.

## Definition of done

- [x] A verified source package can become one paused anime series, twelve review documents and 120 planned episode rows in one transaction, preserving the original 22-minute body and ensemble.
- [x] A planning-only series is visible in the admin with its category and clear state, and cannot be resumed, auto-approved, scheduled or started as ordinary drama.
- [x] Dry-run, exact source hashes, administrator audit, idempotent retry and collision rejection protect the real import.
- [x] Regression checks cover original drama limits, malformed bundles, rollback/collision, worker holds, UI visibility and schema migration.
- [x] A concrete import bundle and host instructions are ready; actual production creation is separately tracked and will only be reported after production readback.

## Steps

- [x] Inspect current contracts, safe import precedent, credentials and task/remote/PR collisions.
- [x] Add narrowly scoped planning persistence and hold guards without changing production readiness.
- [x] Add validated atomic import and operator CLI; prepare the authored bundle.
- [x] Show the native planning series and disable unsupported production actions in the admin.
- [x] Complete final checks and open the separately requested draft PR with host instructions; track actual production import in its own operational ticket.

## How to verify

API: focused planning/import/guard/migration tests plus existing series/document/message tests, schema and dialect tests, ruff and mypy. Web: admin-video-series tests, lint, i18n and typecheck. Run npm run check:tasks. Prepare a bundle from docs/videos/series-plans/borrowed-dawn, then exercise dry-run, apply, readback and replay against isolated PostgreSQL. Real-host execution follows the runbook after deployment and is tracked separately.

## Notes

Host SSH 187.127.118.6:7788 returned ECONNREFUSED from the cloud; public HTTPS is reachable. The owner said they will test from their local computer. No production backend creation or remote write has been claimed.

At claim time, the collision helper found five old review claims aged 89–114 hours with no local worktree, remote branch or open PR. The only open PR then, #1118, changed Shorts UI and its own translation namespace. This work changes the series namespace. Claiming this new ticket with --force was limited to stale scope overlap; no other ticket is edited, released or closed. The branch has since been rebased without conflicts onto origin/main 7f76864f5, preserving the merged #1118/#1119 changes.

This is planning persistence, not full 22-minute production support. The existing 2026-10-02-anime-long-episode-support task remains open for writer budgets, narration/media timing, production QA and compatible narrative policy.

The owner's latest instruction is to open a separate PR. Real-host deployment/import is now tracked by 2026-10-02-create-borrowed-dawn-in-the-production; closing this implementation ticket does not claim production creation.

Independent read-only review passed after fixing the source mount directory, exact-base-slug request collisions and E120 actual/declared final tension consistency. The importer has 80 passing source/transaction/idempotence/collision regressions. Complete source hashes and regenerated Markdown/JSON/CSV twins are checked in Python without executing source JavaScript.

An isolated PostgreSQL 17 CLI smoke created one paused planning series, twelve review documents and 120 planned episodes preserving all 240 tension events and the exact source bodies. Read-only preflight and apply replay both returned unchanged; direct readback found one audit, zero requests/videos, no worker job and successful native API serialization. Bundle SHA256: 154228eaa3ed9f200fbd2de3096914bf36e9aa6bd36e1d29b774146936ca92dc. This is local fixture evidence only.

Final API regression commands with RUN_INTEGRATION_TESTS=1 on isolated PostgreSQL passed 241 planning/CLI/guard/messages/migration/series/document/binge/schema/dialect tests plus 74 existing settings/request/explainer-duration tests. Full API ruff passed; mypy app checked 458 files and mypy tests checked 352. Web lint/i18n/typecheck passed, and the full pre-rebase suite passed 342 files / 3754 tests; after the conflict-free rebase, seven affected/context suites passed 108 tests and i18n/typecheck passed again. The authored source build --check passed 17 generated files / 10 seasons / 120 episodes. The disposable local PostgreSQL container was stopped after verification.

The full Node tools suite passed 1220/1220 after a genuine independent DURATION_ONLY increment refreshed only the ten changed bound files and report SHA. The checker and all sixty other bindings remain unchanged. check:tasks and git diff --check passed.

Separate draft PR opened as #1125: https://github.com/x812033727/travel_scanner/pull/1125. The PR includes deployment/import/readback instructions and explicitly states that no production import has occurred. This ticket is closed for the implementation and PR delivery only; the operational follow-up remains open.
