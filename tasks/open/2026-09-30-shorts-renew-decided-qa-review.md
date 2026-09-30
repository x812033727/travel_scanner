---
id: 2026-09-30-shorts-renew-decided-qa-review
title: Renew decided Shorts final reviews when QA evidence changes without a new MP4
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-30T00:09:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews_integration.py
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

- [ ] Changed Shorts QA evidence/verdicts on the same MP4 can receive a fresh
      final review without inheriting a prior approval or rejection.
- [ ] Unchanged resubmissions remain idempotent, including an owner's explicit
      approval of a failed QA report; old review decisions remain auditable.
- [ ] Long-video approval semantics and existing upload/file checks stay intact.

## Steps

- [ ] Check current work on admin_service.py before claiming; choose a review
      identity or supersession rule that also handles concurrent submissions.
- [ ] Add API regressions for approved-pass -> fresh-fail, rejected -> corrected,
      same-input changed remote verdict, unchanged resend and human override.
- [ ] Document how an existing decided Short obtains its renewed final review.

## How to verify

`cd apps/api && uv run pytest tests/test_video_reviews_integration.py -q`

Use an unchanged MP4 hash with two distinct `payload.qa` reports. The second
report must be reviewed on its own, while resending it unchanged returns the same
decision. Run API lint/type checks and PostgreSQL integration CI.

## Notes

- Found on 2026-09-30 during independent review of
  `2026-09-29-bind-shared-shorts-narration-and-qa` at main cb4d0b44.
- Relevant branch: codex/shorts-evidence-bindings. The local client mitigation
  lives in tools/video/shorts/push.mjs; regression coverage is in
  tools/video/shorts/bindings.test.mjs. Compare the entire returned QA report,
  not only local input hashes: a remote policy verdict can change on identical
  local files.
- No production review or approval was modified to investigate this behavior.
