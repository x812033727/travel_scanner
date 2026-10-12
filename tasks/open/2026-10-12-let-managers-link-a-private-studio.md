---
id: 2026-10-12-let-managers-link-a-private-studio
title: Let managers link a private Studio video to a pending imported final
status: in-progress
priority: P2
area: web
owner: codex-admin-studio-link-ui-8bc3
claimed_at: 2026-10-12T17:16:11Z
created_at: 2026-10-12T17:16:07Z
completed_at:
branch: codex/curio-five-recuts-20261012
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-production-state.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_reviews_youtube.py
---

# Let managers link a private Studio video to a pending imported final

## Why

The admin already has a manual `POST /admin/videos/{slug}/youtube` link flow, but
its paste form appears only after an upload package is approved. A separately
uploaded private recut imported with a pending final review therefore has no
visible way to record its new YouTube ID without first approving the review or
using the publish/sync flow. A project with an ID but no public timestamp is
also mislabeled "Published" in the admin.

## Definition of done

- [x] A content manager can paste a private Studio URL for a pending imported
      final with its full-cut content hash and preview (the review has no full
      MP4 file role). The request contains `url`, `publish_at: null`, and
      `private_only: true`; no review decision or YouTube publish/sync request.
- [x] A reader, a dropped project, a project with an existing YouTube ID, and
      one with active sync cannot use this early-link entry.
- [x] An ID with no public timestamp displays as linked without claiming it
      is public; scheduled and public records keep their existing labels.
- [x] The opt-in private link refuses videos that are not confirmed private and
      unscheduled and fully processed with positive duration on the connected
      channel, an already-linked target, or an ID linked to another project.
      Existing manual-link semantics remain intact.
- [x] The admin browse tab names records with a YouTube ID as linked, including
      private records, in all five locales.

## Steps

- [x] Check active task scopes and the existing endpoint and form behavior.
- [x] Add the narrow pending-final entry and five-locale copy.
- [x] Add meaningful UI/guard and state tests, run web and task checks.
- [x] Add opt-in API validation and rejection tests, run API checks.

## How to verify

Run targeted Vitest for `admin-video-reviews.test.tsx` and
`admin-video-review-card.test.tsx`, then `npm run check:i18n`,
`npm run lint:web`, `npm run typecheck:web`, `npm run test:web`, and
`npm run check:tasks`.

## Notes

`POST /admin/videos/{slug}/youtube` calls `admin_service.link_youtube`; with a
null publish time it records the ID and asks the linked channel for publication
time, but it does not call `/youtube/publish` or decide a review. The existing
`UploadedForm` already parses Studio URLs and will be reused in a mode that
cannot send a publish time and opts into strict `private_only` verification.
The entry will require `content.manage`, a pending
`final` review marked `payload.imported` with its content hash and preview, no
old ID, no approved upload package, and no active sync.
Five actual imported recut reviews carry `preview`, `thumbnail` and
`captions_zh-TW`; they do not carry a `final` file role. Linkage must not turn
their pending final reviews into an apparent approval or offer the resync form.
The private-only flag is a separate opt-in contract for the early-link form:
the backend must read YouTube and reject public, scheduled, unlisted, missing,
foreign-channel, unprocessed, zero-duration, duplicate and already-linked video
IDs without committing. PostgreSQL serializes claims of the same YouTube ID
with a transaction advisory lock and locks the target project row before checks.

Validation on this branch: `test_video_reviews_youtube.py` 68 passed; targeted web
Vitest 3 files/100 tests passed; full web Vitest completed in two shards (180
files/1944 tests and 180 files/2208 tests, both exit 0) before the final opt-in
body and copy edit, which targeted tests covered afterward. `ruff check` on
touched API files, `mypy app` (472 files), `mypy tests` (390 files),
`lint:web`, `typecheck:web`, `check:i18n` (5 locales/25 namespaces), and
`check:tasks` passed. Production deploy, backend readback and independent
duration-receipt rebind remain with the parent work; keep this ticket in progress.
