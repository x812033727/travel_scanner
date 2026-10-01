---
id: 2026-10-01-long-video-final-renewal
title: Renew approved long video cuts with preserved history and owner review
status: done
priority: P1
area: api
owner: codex-language-sync-fix
claimed_at: 2026-10-01T08:13:38Z
created_at: 2026-10-01T08:13:27Z
completed_at: 2026-10-01T08:44:40Z
branch: codex/branding-cc-prompt-20261001
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_long_review_renewal.py
---

# Renew approved long video cuts with preserved history and owner review

## Why

An approved long video cannot currently be deliberately replaced while retaining its
approval history and invalidating the old upload package. A new final submission only
supersedes pending reviews; an approved publish review can remain ready for upload.
The owner requested new channel bookends for existing cuts. This ticket supplies a
reviewable backend renewal operation, not a production activation or upload.

## Definition of done

- [x] An owner can renew an unuploaded approved long cut using a version-checked API.
- [x] The old final, publish, language and dub approvals stop authorizing upload while
      their decisions, notes and approved attachments remain available as history.
- [x] The replacement remains pending until the owner reviews it; a worker resend
      cannot auto-approve it or restore a completed stage.
- [x] Focused tests, lint, typing and independent review pass.

## Steps

- [x] Check claims, active worktrees and open PRs; no overlapping API scope found.
- [x] Add GET/POST /admin/videos/{slug}/final-renewal using content.manage.
- [x] Bind project/review state, old final id/hash, new content and attachment hashes.
- [x] Refuse Shorts, dropped videos, YouTube ids/history, upload sessions, any API
      sync history, completed stage signals and active/result-bearing VPS jobs.
- [x] Preserve pending renewal against ordinary tool resubmission and stale reports.
- [x] Finish validation and report exact operational/integration boundaries.

## How to verify

From apps/api:

```text
uv run pytest tests/test_video_long_review_renewal.py tests/test_video_review_renewal.py tests/test_video_reviews.py -q -p no:cacheprovider
uv run ruff check app/video_reviews/admin_service.py app/video_reviews/admin_api.py app/video_reviews/schemas.py tests/test_video_long_review_renewal.py
uv run mypy app
uv run mypy tests
```

Run `node tools/tasks.mjs check` from the repository root. PostgreSQL concurrency
requires integration CI; the local suite uses real SQLite rows and review-store files.

## Notes

- Claimed by the delegated backend agent on the root agent's existing branch; no
  production access, deployment, file adoption, activation receipt edits or commits.
- GET returns an opaque digest of the current project and review evidence plus final
  id/hash. POST accepts expected_version, expected_final_review_id,
  expected_final_sha256, reason, and a new final ReviewIn with uploaded preview files.
- Only the new renewal path changes long-video semantics. Legacy imported submissions
  keep their established workflow; the root's parallel imported-video work is untouched.
- The producer's stage is its next step. `stage=on YouTube` with exactly one
  `on_youtube` checklist item whose `done` is literally false is legitimately waiting
  to upload; it may renew when every other upload/history/ID/session guard passes.
  Missing, true, duplicate, or malformed on_youtube completion evidence is refused,
  as are the actual `published`, `uploaded`, and `done` stages. No force flag exists.
- For renewed videos, later publish/languages/dubs submissions must provide
  `payload.final_review_id`. Publish metadata must name the new final SHA/branding;
  language/dub manifest attachments must bind that final id/SHA/branding. Existing
  CLI producers do not yet send all these bindings. A producer integration and any
  website controls are separate scoped work; do not use this backend-only change as
  evidence that existing videos were rebuilt, approved, scheduled or deployed.
- Final validation after narrowing stage/checklist semantics: 129 tests passed
  (renewal, Shorts renewal, video reviews, YouTube API sync and VPS), full API ruff
  passed, and full mypy passed app (447 files) and tests (340 files), all exit 0.
  No unrelated baseline type failures were encountered. The API implementation is
  complete; its integration ticket stays open and no deployment is claimed.
- Independent review found that a later ordinary submission could prune superseded
  but undecided evidence. Fixed using server-owned retained_review_ids on replacement
  reviews; kept_files retains their attachments through subsequent renewals and
  ordinary pruning. A real-store regression covers both old pending languages and
  an earlier undecided replacement final. No old payload or decided_at is rewritten.
  Independent rereview found no remaining major/security finding.
- Fresh root production observation on 2026-10-01: imported videos 01/02/03 already
  have approved languages as well as approved final; imported 04/05/06 have only
  approved final. All six have no approved publish, YouTube id or upload jobs.
  This agent verified the deployed source commit 7606ff50 read-only: new import does
  not invalidate approved languages; approved reviews cannot be rejected again;
  changing locale choices does not invalidate language approvals. Hold 01/02/03 for
  proper renewal. 04/05/06 remain eligible for the existing import route only after
  the root's fresh preflight. Waiting for renewal for all six is also consistent.
- There is no supported deployed operation to revoke the approved language batch
  without deleting/rewriting history. Do not use a fake skipped batch, toggle locales,
  clear approval files or force-import to disguise the old source approval.
- Follow-up integration: 2026-10-01-long-video-renewal-tools-and-ui. That integration
  and production deployment are not completed here. Root's fresh inventory found all
  11 apparent on-YouTube/no-ID rows had on_youtube.done=false; no artificial stage
  change or identity reconciliation is required solely for that legitimate state.
  The complete authenticated channel inventory, campaign and duration checks remain
  operational evidence against an unrecorded manual upload before any live renewal.
