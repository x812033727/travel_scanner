---
id: 2026-10-02-import-long-anime-plans-as-paused
title: Import long anime plans as paused admin series
status: in-progress
priority: P2
area: api
owner: codex-root
claimed_at: 2026-10-02T08:03:01Z
created_at: 2026-10-02T08:01:07Z
completed_at:
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
- [ ] Complete final checks and open the separately requested draft PR with host instructions; track actual production import in its own operational ticket.

## How to verify

API: focused planning/import/guard/migration tests plus existing series/document/message tests, schema and dialect tests, ruff and mypy. Web: admin-video-series tests, lint, i18n and typecheck. Run npm run check:tasks. Prepare a bundle from docs/videos/series-plans/borrowed-dawn, then exercise dry-run, apply, readback and replay against isolated PostgreSQL. Real-host execution follows the runbook after deployment and is tracked separately.

## Notes

Host SSH 187.127.118.6:7788 returned ECONNREFUSED from the cloud; public HTTPS is reachable. The owner said they will test from their local computer. No backend creation or remote write has been claimed.

The collision helper found five old review claims aged 89–114 hours with no local worktree, remote branch or open PR. The only open PR #1118 changes Shorts UI and its own translation namespace; this work changes the series namespace and will preserve/rebase those independent changes. Claiming this new ticket with --force is limited to stale scope overlap; no other ticket is edited, released or closed.

This is planning persistence, not full 22-minute production support. The existing 2026-10-02-anime-long-episode-support task remains open for writer budgets, narration/media timing, production QA and compatible narrative policy.

The owner's latest instruction is to open a separate PR. Real-host deployment/import is now tracked by 2026-10-02-create-borrowed-dawn-in-the-production; closing this implementation ticket does not claim production creation.

Independent read-only review passed after fixing the source mount directory, exact-base-slug request collisions and E120 actual/declared final tension consistency. The importer has 80 passing source/transaction/idempotence/collision regressions. Complete source hashes and regenerated Markdown/JSON/CSV twins are checked in Python without executing source JavaScript.

An isolated PostgreSQL 17 CLI smoke created one paused planning series, twelve review documents and 120 planned episodes preserving all 240 tension events and the exact source bodies. Read-only preflight and apply replay both returned unchanged; direct readback found one audit, zero requests/videos, no worker job and successful native API serialization. Bundle SHA256: 154228eaa3ed9f200fbd2de3096914bf36e9aa6bd36e1d29b774146936ca92dc. This is local fixture evidence only.
