---
id: 2026-10-02-keep-character-look-review-identities-distinct
title: Keep character look review identities distinct by subject
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-02T16:05:07Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/models.py
  - apps/api/tests/test_video_reviews.py
---

# Keep character look review identities distinct by subject

## Why

The CLI can submit each character look with the same manifest SHA, while
submit_review deduplicates by project/gate/content_sha256 and the database unique
constraint omits subject. A second character can receive the first character's
review instead of its own, preventing trustworthy complete-cast approval.
Found while preparing the two wedding episodes; no existing review was changed.

## Definition of done

- [ ] Reproduce same manifest SHA with two distinct character subjects.
- [ ] Preserve idempotency for the same subject without merging other subjects.
- [ ] Evaluate existing data/unique constraint and migrate compatibly if required.
- [ ] Verify latest approved look lookup and re-submission for each character.

## Steps

- [ ] Check concurrent PR #1132 before shared review-service changes.
- [ ] Decide compatible identity change and exact migration/test scopes.
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
