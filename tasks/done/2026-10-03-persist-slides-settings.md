---
id: 2026-10-03-persist-slides-settings
title: Persist illustrated slides settings on save
status: done
priority: P1
area: api
owner: codex-slides-save
claimed_at: 2026-10-03T01:31:34Z
created_at: 2026-10-03T01:31:14Z
completed_at: 2026-10-03T01:54:56Z
branch: codex/fix-slides-settings-save
depends_on: []
scope:
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
---

# Persist illustrated slides settings on save

## Why

Saving the illustrated slides settings returns HTTP 200, but the illustration switch is
still off after saving or reloading. The settings writer flattens the nested drama object
onto mapped database columns, while assigning the slides object to an unmapped `slides`
attribute. None of the six slides settings are persisted. A stored null image choice also
reads back as the default model instead of following the drama's image model.

## Definition of done

- [x] All six illustrated slides settings survive a save and a fresh database read.
- [x] Partial saves preserve omitted settings and the drama's separate budget and options.
- [x] The illustration switch can be turned off, the budget can be zero, and nullable image,
  music and sound-effect choices can be cleared. Missing columns still read their defaults.
- [x] Audit entries name the changed mapped slides fields rather than the nested container.

## Steps

- [x] Reproduce the failure with a mapped ORM row and a real PostgreSQL PUT/read round trip.
- [x] Flatten both nested settings groups and preserve the explicit null image choice.
- [x] Run the complete settings suite with PostgreSQL, scoped Ruff and mypy, and task checks.

## How to verify

From `apps/api`, with a migrated local PostgreSQL database:

```bash
DATABASE_URL=postgresql+asyncpg://postgres@127.0.0.1:55432/slides_settings_test RUN_INTEGRATION_TESTS=1 .venv/bin/pytest tests/test_video_automation_settings.py -q
.venv/bin/ruff check app/video_automation/settings.py tests/test_video_automation_settings.py
.venv/bin/mypy app/video_automation/settings.py tests/test_video_automation_settings.py
```

From the repository root: `npm run check:tasks` and `git diff --check`.

## Notes

- Baseline evidence: both new fast regressions failed, and the real PostgreSQL save returned
  HTTP 200 with all six slides values unchanged. After the fix, the full settings suite passed
  **48 tests**, including three PostgreSQL integration tests; Ruff and scoped mypy passed.
- The PostgreSQL regression uses the actual settings writer through the admin route, GETs
  with a new session, expunges and reloads the ORM row, then verifies field-level audit diffs.
  It covers enabled/model/cap/storyboard/music/sfx, an unrelated settings save, a slides-only
  budget update, and off/null/zero values while preserving the drama's complete settings.
- `slides_values` previously discarded explicit null image models. It now distinguishes an
  existing nullable choice from a missing attribute; missing/nonnullable null fields retain
  their default behavior. The schema and database columns already support these values.
- Claim used `--force` because the broad module scope of
  `2026-09-27-video-drama-room-withdraw-a-one` overlapped this narrow fix. The parent checked
  local branches and remote heads: the older claim was about 135 hours old and its branch
  had no remote head. A final per-file check found the parent's existing draft PR #1139
  also touches settings.py in separate anime-approval sections; this fix changes only
  slides_values and _flat. No other open PR touched the test file. The older ticket and
  the existing anime PR were left unchanged.
- The coordinator also ran API-wide Ruff and mypy: app (458 source files) and tests
  (354 source files) passed. No frontend, schema migration or production access change is
  needed for this fix.
- Detailed red/green logs are outside the checkout at
  `/workspace/knowledge-stories-production-20261003/live/debug-slides-save/code-fix/`.
- This is an independently authorized coding fix. No cloud configuration, frontend,
  migration, live settings PUT or production deployment was changed by this work.
