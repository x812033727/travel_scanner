---
id: 2026-10-02-ten-drama-backend-production-sync
title: Sync ten drama production plans into backend review revisions
status: done
priority: P1
area: ops
owner: codex-ten-drama-sync
claimed_at: 2026-10-02T08:10:17Z
created_at: 2026-10-02T08:09:51Z
completed_at: 2026-10-05T00:24:45Z
branch: codex/ten-drama-backend-sync-20261002
depends_on: []
scope:
  - ops/video/sync_drama_plan_revisions.py
  - apps/api/tests/test_video_drama_plan_sync.py
  - docs/videos/series-plans/production-20261002-sync
---

# Sync ten drama production plans into backend review revisions

## Why

The owner could not see the ten dramas' new production direction in the admin.
PR #1094 was already included in the deployed release, but the database still
contained the sixty original 2026-09-28 v1 review documents. Every original body
and authored series field matched the historical import at `a14d45f8a`; no admin
editing or episode production had occurred on these works.

## Definition of done

- [x] The original ten works expose the latest six review documents each, including
  source corrections, forty episode production plans, selected voices and CC.
- [x] Keep all sixty v1 documents unchanged and preserve all series identities.
- [x] Retain `drama_enabled=false`, no episodes/requests, and no automatic approval.
- [x] Verify persisted bodies and the admin's latest-document serializer against
  the prepared source-bound package; record browser acceptance separately.
- [x] Save the guarded updater, validation tests and a concise operations receipt.

## Steps

- [x] Read the live deployment and database; compare the exact historical import.
- [x] Rebuild source-bound candidates from current main rather than stale bundles.
- [x] Make and verify a fresh PostgreSQL backup before the transaction.
- [x] Independently review and test snapshot guards, rollback and idempotent replay.
- [x] Dry-run, apply the exact reviewed package and read back every latest body.

## How to verify

Run `python -m pytest tests/test_video_drama_plan_sync.py` in the API environment,
then focused Ruff/mypy. `production-check` validates ten works and 400 episode
designs. Use the sync CLI without `--apply` first; apply requires its exact
`--expected-sha256`. Re-run without applying to prove unchanged replay.

The backend is `/zh-TW/admin/videos?tab=drama`. Open a work, then expand the setting
document's full text or production data. Successful SQL/serializer verification
alone is not authenticated browser acceptance.

## Notes

Source Git SHA: `0d7267d8d` (full SHA is pinned in the operational package).
Package SHA-256: `5010ee303ae536bc0e994ff2de67e80b6ebc6ac4739c9d099b91fc77b0ec580e`.
The ten works have no episodes and all sixty current documents are undecided
review. The series premise/note corrections and `visual_tier=clips` are included;
no other series fields or global media settings are targeted.

Fresh backup verification passed: 175,550,845 bytes, mode 0600, PostgreSQL archive
listing readable. Keep full live snapshots, package and server receipts outside Git.
The new documents remain planning-only: no auditions, media, pilot, multilingual
dubs, YouTube upload or publication has been performed.

Completed production read-back verified ten works, sixty new v2 review documents,
sixty unchanged v1 documents, 400 production episode plans, unchanged global
settings and no next worker job. Read-only replay returned ten unchanged works.
The sync suite passed 31 tests; Ruff and mypy passed. Independent review resolved
the actor/audit FK lock interaction and rejected suspended/deleted actors.

See `docs/videos/series-plans/production-20261002-sync/README.md` and
`verification.json` for the concise operations receipt. Authenticated browser
rendering remains unverified; the database and admin serializer were checked.
The operational update is complete; this task remains review until the updater
and receipt PR is merged.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-ten-drama-sync (since 2026-10-02T08:10:17Z) was stale; the work landed in #1122 and every box was already ticked, so the ticket is closed.
