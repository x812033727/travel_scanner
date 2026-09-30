---
id: 2026-09-30-shorts-renew-decided-qa-review
title: Renew decided Shorts final reviews when QA evidence changes without a new MP4
status: done
priority: P2
area: api
owner: codex-shorts-evidence
claimed_at: 2026-09-30T00:20:17Z
created_at: 2026-09-30T00:09:59Z
completed_at: 2026-09-30T00:37:03Z
branch: codex/shorts-review-revisions
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/api/app/models.py
  - apps/api/migrations/versions/0115_video_review_revision.py
  - apps/api/tests/test_migration_0115_video_review_revision.py
  - apps/api/tests/test_video_review_renewal.py
  - apps/api/tests/test_video_shorts_integration.py
  - docs/videos/SHORTS.md
  - tools/video/shorts/push.mjs
  - tools/video/shorts/pipeline.test.mjs
  - tools/video/shorts/bindings.test.mjs
---

# Renew decided Shorts final reviews when QA evidence changes without a new MP4

## Why

`submit_review` finds final reviews by gate and `content_sha256` and returns an
existing non-pending review unchanged. For Shorts this hash is the MP4, while QA
also depends on script, facts, narration checks and other evidence. An approved
MP4 with corrected metadata or a newly failed facts receipt therefore returns
its old approval; a previously rejected MP4 cannot receive a fresh review after
its non-video evidence is corrected.

The shared Shorts client now compares the returned approved QA payload with the
submitted report and stops before the publish review when they differ. This
prevents stale approval reuse, but the API still needs a supported renewal path.

## Definition of done

- [x] Changed Shorts QA evidence/verdicts on the same MP4 can receive a fresh
      final review without inheriting a prior approval or rejection.
- [x] Unchanged resubmissions remain idempotent, including an owner's explicit
      approval of a failed QA report; old review decisions remain auditable.
- [x] Long-video approval semantics and existing upload/file checks stay intact.

## Steps

- [x] Check current work on admin_service.py before claiming; choose a review
      identity or supersession rule that also handles concurrent submissions.
- [x] Add API regressions for approved-pass -> fresh-fail, rejected -> corrected,
      same-input changed remote verdict, unchanged resend and human override.
- [x] Document how an existing decided Short obtains its renewed final review.

## How to verify

`cd apps/api && uv run pytest tests/test_video_review_renewal.py tests/test_video_reviews_integration.py tests/test_video_shorts_integration.py tests/test_migration_0115_video_review_revision.py -q`

Use an unchanged MP4 hash with two distinct `payload.qa` reports. The second
report must be reviewed on its own, while resending it unchanged returns the same
decision. Run API lint/type checks and PostgreSQL integration CI.

## Notes

- 2026-09-30 implementation: migration 0115 adds a revision to the review identity
  without changing the media SHA. Changed final QA supersedes live final/publish
  reviews, records their former status, preserves decision attachments and releases
  pre-upload slots. Publish reviews must name the current approved final ID.
  Project-row locks serialize renewal, decisions and uploader starts. Existing
  YouTube IDs, resumable uploads, queued/running sync and active/uncertain VPS jobs
  refuse renewal before review history changes. Downgrade refuses duplicate history.
- Local validation: 13 SQLite lifecycle regressions passed; schema/dialect/migration
  suite 15 passed and 1 PostgreSQL skip; existing review unit tests 29 passed.
  Full tools: 883 passed, 2 skipped, 0 failed (bundled Node 24.19).
  Full Ruff and mypy app (444 files) / tests (335 files) passed. PostgreSQL migration
  and concurrent-submission/decision tests require CI; no production records changed.

- 2026-09-30: PR #992 was independently marked ready and auto-merge enabled while
  this follow-up was being implemented. Continued on codex/shorts-review-revisions
  for a separate draft PR without changing #992's approved merge scope.

- 2026-09-30: Claimed by codex-shorts-evidence on the existing draft PR #992.
  Fresh main cb4d0b44, local/remote branches, worktree changes, open PRs #990/#991
  and expanded task scopes were checked; no competing active changes found.
  Existing UNIQUE(project_id, gate, content_sha256) requires an additive revision
  column and updated constraint to preserve prior review rows with the real MP4 hash.

- Found on 2026-09-30 during independent review of
  `2026-09-29-bind-shared-shorts-narration-and-qa` at main cb4d0b44.
- Relevant branch: codex/shorts-evidence-bindings. The local client mitigation
  lives in tools/video/shorts/push.mjs; regression coverage is in
  tools/video/shorts/bindings.test.mjs. Compare the entire returned QA report,
  not only local input hashes: a remote policy verdict can change on identical
  local files.
- No production review or approval was modified to investigate this behavior.
