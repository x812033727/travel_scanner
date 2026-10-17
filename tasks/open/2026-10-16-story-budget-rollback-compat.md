---
id: 2026-10-16-story-budget-rollback-compat
title: Stage rollback compatibility before USD 5 story migration
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-16T01:08:20Z
completed_at:
branch: codex/story-budget-rollback-compat-20261016
depends_on: []
scope:
  - apps/api/app/admin/operations_service.py
  - apps/api/app/database_admin/service.py
  - apps/api/app/schema.py
  - apps/api/app/migration_guard.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/tests/test_admin_operations.py
  - apps/api/tests/test_database_admin.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_story_budget_rollback_integration.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_story_policy.py
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/media/client.mjs
  - tools/video/media/client.test.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/tts/cli.mjs
  - docker-compose.prod.yml
  - .agents/skills/deploy/scripts/host-verify.sh
  - tasks/open/2026-10-16-story-budget-rollback-compat.md
---

# Stage rollback compatibility before USD 5 story migration

## Why

The planned 0133 migration lowers B18 v2 from USD 25 to USD 5 and seeds five more
accounts. Production runs the migration before switching the API; a failed release
rolls back application code without downgrading the database. The currently deployed
API rejects B18 v2 at USD 5 and rejects revision 0133 at `/ready`, which would make
the rollback unusable. This compatibility release must deploy before 0133.

## Definition of done

- [x] The 0132 API can serve `/ready` against exactly reviewed revision 0133.
- [x] Existing B18 v2 ledger/status and reconciliation work at both stored limits.
- [x] No fresh B18 v2 paid dispatch while the stored limit remains USD 25.
- [x] Five later story slugs are already fail-closed in the 0132 application; status skips absent follow-on accounts only while the database is exactly at 0132, and exposes each USD 5 account after 0133.
- [x] Rollback health displays use the same exact schema compatibility as `/ready`.

## Steps

- [x] Add exact-revision compatibility and tests.
- [x] Add B18 v2 read/settlement compatibility, paid gate and tests.
- [x] Add five follow-on fail-closed routing, missing-account status handling, and rollback dashboard tests.
- [x] Keep all five follow-on slugs on the pilot paths in the automation, media and speech clients, including audition attribution.
- [x] Make the actual migrate container and host verifier accept only the reviewed 0133-on-0132 rollback state, with exact ledger and schema readback; keep other unknown revisions fatal.
- [ ] Run focused API checks and CI; deploy this release before 0133.

## How to verify

`cd apps/api && uv run ruff check app/admin/operations_service.py app/database_admin/service.py app/schema.py app/video_budget app/video_media/admin_api.py tests/test_admin_operations.py tests/test_database_admin.py tests/test_schema.py tests/test_video_media_api.py tests/test_video_pilot_budget.py tests/test_video_story_policy.py && uv run pytest tests/test_admin_operations.py tests/test_database_admin.py tests/test_schema.py tests/test_video_media_api.py tests/test_video_pilot_budget.py tests/test_video_story_policy.py -q`; then verify `/ready` and pilot budget status after the compatibility deployment, before 0133.

## Notes

The prior USD 25 task is still in-progress under an old owner from 2026-10-15,
although its PR was merged. Its broad scope overlaps this exact repair, so the
claim used `--force`; this work touches only the listed files and is isolated in
its own branch. Do not deploy 0133 in the same release as this compatibility code.

2026-10-16 local: 20 focused API tests passed, 2 PostgreSQL-only tests skipped;
targeted mypy and ruff passed. CI and production deployment are pending. The
follow-on migration remains in a separate draft PR and must not ship first.

Independent review found that the first candidate recognized only the original four pilot slugs. A rollback after follow-on jobs were queued could therefore bypass their USD 5 reservations. The compatibility application now recognizes the exact five follow-on slugs even before 0133 creates their accounts: paid calls fail closed; media status skips genuinely absent rows only when the database revision is still exactly 0132. After 0133, a missing follow-on row or a present row with the wrong limit remains a 503 error. The admin overview and database revision view now apply the same exact 0133-on-0132 acceptance as `/ready`. B18 v2 can settle and release old operations while its stored row is still USD 25, but new paid reservations wait for USD 5. This is code and test preparation only; no deployment or paid work has started.

2026-10-16 expanded local check: the initial focused API suite had 95 passed, 3 skipped. After independent review tightened the status omission to exact database revision 0132, the media API suite passed again with 12 tests. Targeted ruff, `npm run check:tasks`, and `git diff --check` passed. Full app/tests mypy and PR CI remain pending at this note.

After rebase onto main `0b6844a4a`, the focused suite exposed one test fixture missing the `alembic_version` table that the new status guard reads; its other 95 tests passed and 3 skipped. The SQLite fixture now explicitly represents 0132, and that status regression passed in isolation. This is test setup only; paid routing remains fail-closed and the PR remains draft.

Independent release review found three JS clients still knew only the four earlier pilot slugs. On rollback after 0133, a five-film speech call without `video_slug` would bypass the API's per-film reserve, and automation/media clients would take ordinary transport paths. The exact client and test files are added to this ticket's scope before repair. Keep the PR draft until the nine-slug behavior is tested; this code has not been deployed and no paid call has run.

The same review found that Compose recreates `migrate` on rollback; its existing `alembic upgrade head` fails before API starts when the database is at 0133 but the rollback image only knows 0132. The host verifier also rejects that intentional state. Root approved a code-only guarded runner and explicit verifier classification while retaining the true 0133 migration solely in #1510. Added these exact code, Compose, test and verifier paths to scope before editing. Do not call this release rollback-safe until #1510's real PostgreSQL/Compose rollback integration passes.

The separate real-PostgreSQL integration test may be copied into this compatibility PR after its author finishes it. This ticket now includes only that exact new test path. The test must run the source-hash-bound 0133 migration inside a temporary API tree; the #1521 application tree must remain at migration head 0132. Keep deployment on HOLD until that CI test passes on this PR head and release review clears the actual Compose/API path.

The exact test source was copied from the separate authoring worktree at SHA256 `E24C6D086675E8186DFC205AA9C2ED96DD1A97B8BBC3522C432BB0529AD8C917`; the compatibility branch still has no 0133 migration file. On Windows, the focused API suite passed 101 tests with three PostgreSQL-only skips, and targeted ruff/mypy passed. The copied PostgreSQL test itself was skipped locally because no PostgreSQL service is available. The media-client tests passed 8/8; TTS/automation tests requiring the shared `sandbox()` fixture exited at file level without diagnostics on this Windows host, while the isolated TTS paid-routing test passed. These are not release-green evidence: CI's real PostgreSQL and full JS suite are required before #1521 can leave HOLD.

Independent review of the first guard head found that named constraints could retain their names but have weaker definitions. The guard now compares normalized definitions for both primary keys, the operation unique key, foreign key source and target, all operation checks, and the account's exact 5/25 limit set; the database integration test mutates unique/status/limit definitions and requires rejection. Review also found that preproduction audition samples under `brand-stories-five-20261014` used A29/A16/A37/B14/A21 IDs before a video slug existed. Those exact IDs now map to the five ledger slugs, while an ambiguous folder sample requires `--slug`; a mismatched ID/slug is refused before any speech request. The system Node 24.13 failure above is the repository's documented Windows fixture crash; bundled Node 24.19 passed the changed audition test. Full bundled-Node suites and CI remain release gates.

The three affected JS suites passed together with bundled Node 24.19: 67/67. The guard unit suite passed 5 tests, while the true PostgreSQL test remains skipped locally. Targeted ruff and mypy passed. The CI PostgreSQL result on the tightened head and independent re-review remain required; the preceding #1521 head has neither approval nor deployment status.

The first true PostgreSQL CI run exposed that asyncpg decodes `pg_constraint.contype` and `confdeltype` as byte values. String-only checks would reject a valid 0133 database. The guard now normalizes these single-byte catalog fields before comparing exact constraints, and the integration test normalizes its own independent catalog readback. A byte-valued unit fixture guards this driver behavior; a new CI PostgreSQL run must prove the whole rollback path.


### 2026-10-17 owner-authorized claim release

Implementation in #1521 is merged. The owner authorized releasing this obsolete claim for independent A01 lexicon integration. This ticket remains open only pending archival; do not reimplement the merged work. No production action is authorized by this metadata change.
