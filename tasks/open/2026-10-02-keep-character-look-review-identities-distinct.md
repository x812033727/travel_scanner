---
id: 2026-10-02-keep-character-look-review-identities-distinct
title: Keep character look review identities distinct by subject
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-look-review-subject
claimed_at: 2026-10-04T15:54:43Z
created_at: 2026-10-02T16:05:07Z
completed_at:
branch: claude/look-review-identity-by-subject
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/models.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/migrations/versions/0124_video_review_subject.py
  - apps/api/tests/test_migration_0124_video_review_subject.py
---

# Keep character look review identities distinct by subject

## Why

The CLI can submit each character look with the same manifest SHA, while
submit_review deduplicates by project/gate/content_sha256 and the database unique
constraint omits subject. A second character can receive the first character's
review instead of its own, preventing trustworthy complete-cast approval.
Found while preparing the two wedding episodes; no existing review was changed.

## Definition of done

- [x] Reproduce same manifest SHA with two distinct character subjects.
- [x] Preserve idempotency for the same subject without merging other subjects.
- [x] Evaluate existing data/unique constraint and migrate compatibly if required.
- [x] Verify latest approved look lookup and re-submission for each character.

## Steps

- [x] Check concurrent PR #1132 before shared review-service changes.
- [x] Decide compatible identity change and exact migration/test scopes.
- [ ] Implement focused regression coverage, independent review and validation.

## How to verify

Two characters submitting one shared manifest SHA retain separate subjects and
approval decisions; repeating either submission reuses only its own record.

## Notes

Observed in tools/video/review/sync.mjs lookSubmissions,
apps/api/app/video_reviews/admin_service.py submit_review same lookup, and
VideoReview's project/gate/content_sha256 unique constraint in app/models.py.
The wedding scoped runner rejects missing cast approvals. Its narrowly scoped
producer may submit a distinct real per-character artifact through the existing
API as an interim path; it must not fabricate approval or reuse another subject.
This follow-up is unclaimed and no shared backend code is changed here.

### 2026-10-04 claude-opus-5-5-look-review-subject

- Claimed with `--force` over `2026-10-03-illustrated-slides-round-2-a-family`
  (scope `apps/api/tests`, claim 31 h old): its work landed as PR #1172 (`b0a264567`).
- PR #1132 (the concurrent review-service PR named in Steps) merged on 2026-10-03
  02:34Z; it changed `tools/video/review/sync.mjs` and other tools, no API file.
- Reproduced on a real SQLite database before the fix
  (`test_each_character_keeps_its_own_look_review_of_one_shared_manifest`): the
  second character's submission came back with the first character's review id, and
  the identity test's distinct-subject rows hit `UNIQUE constraint failed:
  video_reviews.project_id, gate, content_sha256, revision`. The shared hash has been
  sent since the look stage arrived (#800): `lookSubmissions` hashes the whole
  `characters/manifest.json` once and sends it with every character. When the first
  review was still pending, the second character's payload, summary and files
  overwrote it (subject unchanged); when it was decided, the second character got no
  review at all, and review-pull waited for it forever.
- Fix, server only (the CLI already sends `subject` and `recordLook` keys picks by it):
  `submit_review` reuses a review only when gate, subject and hash all match, and
  `VideoReview`'s identity becomes (project, gate, subject, hash, revision) as two
  partial unique indexes, `uq_video_review_no_subject` (`subject IS NULL`, the old
  columns) and `uq_video_review_subject` (`subject IS NOT NULL`). Two indexes because
  a NULL never collides in a unique constraint: a single five-column constraint would
  have stopped enforcing anything for the gates without a subject. Those gates, and a
  subject resent with its own hash, behave exactly as before; the Shorts revision path
  is unchanged.
- Migration `0124_video_review_subject` (head was `0123_video_stage_jobs`) creates
  both indexes, then drops `uq_video_review_content_revision`. Production data can
  take it as is: the old constraint was stricter than either index (no subject in the
  key), so no existing row can violate them; nothing is read, changed or deleted.
  Downgrade refuses while two rows share the old identity. The PostgreSQL migration
  test runs only in CI (no local Postgres here).
- Rows an earlier submission overwrote are not repaired here. After deploy, running
  `review-push --gate look` again for a drama waiting on a character creates the
  missing reviews and lets a pending, overwritten one take its own payload back; a
  decided one that showed another character's sheets is filed as
  `2026-10-04-audit-look-reviews-another-character-overwrote`.
- Unticked step: regression coverage and validation are done; the independent review
  is the long-form duration receipt increment (`admin_service.py` is bound in
  `docs/videos/long-form/review.json`), which the coordinator's reviewer adds to this
  PR before it leaves draft.
