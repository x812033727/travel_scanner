---
id: 2026-10-03-split-the-api-ci-job-s
title: Split the api and web CI jobs into parallel shards
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-api-ci-shards
claimed_at: 2026-10-03T10:00:07Z
created_at: 2026-10-03T09:59:57Z
completed_at:
branch:
depends_on: []
scope:
  - .github/workflows/ci.yml
  - .github/BRANCH_PROTECTION.md
  - apps/api/tests/conftest.py
  - apps/api/tests/sharding.py
  - apps/api/tests/shard_durations.json
  - apps/api/tests/test_sharding.py
  - apps/api/tests/test_integration_postgres_redis.py
  - .agents/skills/dev-and-ci
  - .claude/skills/dev-and-ci
  - .agents/skills/backend-conventions/references/migration-tests.md
  - tools/ci-images.test.mjs
---

# Split the api CI job's pytest run into parallel shards

## Why

The `api` CI job took about 25 minutes, 23 of them in one `uv run pytest --cov=app`
process (CI run 37111019702 on main, 2026-10-03). Every pull request waited on it.

## Why (web)

The `web` job took about 20 minutes in the same run: vitest 7m45s (350 files, one at a
time by vitest.config.ts) and the isolated Playwright set 7m47s, plus ~4 minutes of
lint, typecheck, test:tools and build.

## Definition of done

- [x] The main pytest run is split into four parallel jobs, `api-tests (n/4)`, each with
      its own PostgreSQL, Redis and S3 companion.
- [x] `api` stays the required check name: a gate job that passes only when `api-checks`
      and every shard passed, and fails when one failed or was cancelled.
- [x] `web` is the same kind of gate over `web-checks`, three `web-unit (n/3)` vitest
      shards and three `web-e2e (n/3)` Playwright shards, each building the app itself.
- [x] Shards are balanced by measured per-file time, and a new test file runs without
      touching the durations file.

## Steps

- [x] `tests/sharding.py` and `--shard INDEX/TOTAL` in `tests/conftest.py`.
- [x] `tests/shard_durations.json` from a full local run (1052 s of test time over 354 files).
- [x] ci.yml split into `api-checks`, `api-tests` (matrix 1..4) and the `api` gate.
- [x] BRANCH_PROTECTION.md and the dev-and-ci / backend-conventions skills describe it.

## How to verify

    cd apps/api
    uv run pytest tests/test_sharding.py
    uv run pytest --co -q --shard 1/4   # one quarter of the suite

In CI: four `api-tests (n/4)` jobs plus `api-checks` and `api` on the pull request.

## Notes

- Whole files are kept together so module fixtures and cross-module fixture imports
  behave as unsharded. The largest file is ~68 s, so four shards balance to ~4.5 min each.
- `--cov=app` was dropped from the shard run: each shard would print a partial report,
  nothing enforced a threshold, and coverage slowed the run (local 18 min without it,
  CI 23 min with it). Combining shard coverage via artifacts is possible if anyone wants
  the number back.
- Refresh the estimates with the command in the sharding.py docstring when the split
  drifts out of balance.
- Sharding exposed one hidden order dependency: `test_flight_anchor_from_offer` only
  passed because `test_analytics_integration.py` had already switched analytics on in
  the shared database. It now turns analytics on itself. Locally all four shards passed
  on fresh databases (4 min 35 s to 4 min 52 s each; the unsharded run was 18 min), but
  without the MinIO companion, so the `COMMUNITY_TEST_S3` cases were first run by CI.
- web: vitest and Playwright both shard natively (`--shard=n/3`), so no durations file.
  vitest has to be called directly in CI: `npm run test:web -- --shard=…` gives the flag
  to the inner `npm run --workspace`. The Playwright failure-trace artifact is now
  `site-experience-browser-results-<n>` and the manual-upload evidence
  `youtube-manual-browser-evidence-<n>`; tools/ci-images.test.mjs reads the whole name.
- web, measured locally: vitest shard 1/3 ran 117 files in 4.8 min (11 min unsharded);
  the three Playwright shards ran 3.5–3.8 min each and added up to the unsharded run
  exactly (554 passed, 9 skipped, 5 failed). The 5 failures (admin-video-shorts portrait
  player, offline-day-view, one mobile navigation case) also fail unsharded here and pass
  on main's CI: this container only has Chromium 1194 while the project's Playwright
  expects 1243.
