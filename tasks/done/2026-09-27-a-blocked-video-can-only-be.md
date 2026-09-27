---
id: 2026-09-27-a-blocked-video-can-only-be
title: A blocked video can only be resumed by editing auto.json on the host
status: done
priority: P3
area: tools
owner: codex-video-retry
claimed_at: 2026-09-27T15:26:06Z
created_at: 2026-09-27T07:32:11Z
completed_at: 2026-09-27T15:45:05Z
branch: codex/video-retry
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - apps/api/app/video_reviews
  - apps/api/app/models.py
  - apps/api/migrations/versions/0104_video_retry_request.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/api/tests/test_migration_0104_video_retry_request.py
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# A blocked video can only be resumed by editing auto.json on the host

## Why

The host worker blocks a video when a stage fails twice in a row (`retryLater` →
`block()`), or when a step needs a person, such as render layout problems. `block()` writes
`status: "blocked"` and the reason into `auto.json` in the `video_work` volume.
`/admin/videos` shows the reason as the first checklist item, `卡住，需要人處理：…`. But
`step()` only advances videos whose status is `active`, and nothing ever sets a blocked
video back.

Once the cause is gone, the owner's only choices on the page are to drop the video or to
wait. On 2026-09-27 both blocked videos were resumed by hand over SSH, by editing `auto.json`
in the worker container: `openai-academy-learning-paths` after its chat scene was fixed, and
`gpt-6-sol-luna-where-to-use` after the source URL fix (ticket
`2026-09-27-video-drafts-read-their-source-article`). The owner has said they only want to
decide when videos are published (docs/videos/HANDS-OFF.md), so a blocked video should not
need a person with host access.

## Definition of done

- [x] A blocked video's card on `/admin/videos` has a "try again" action for someone with
      `content.manage`. On its next run the worker sets the video back to `active` and
      clears that stage's failure count.
- [x] A video that fails the same way again is blocked again, with the same limit of two
      failures in a row. The action must not turn into a loop that spends tokens.

## Steps

- [x] API: record the request on the project, the way `dropped_at` is recorded, and show it
      in the worker's `videos()` list. It probably needs a migration: add its path to the scope.
- [x] Worker: in `step()`, before the active videos, move a blocked video with a pending
      retry back to `active`, then report the checklist.
- [x] Web: the action on the card, and the five locales' strings. Add `apps/web/messages` to
      the scope.
- [x] Tests on each side.

## How to verify

In `tools/video/automation/automation.test.mjs`, a blocked video with a retry request
becomes `active` and advances one step, and a second failure blocks it again. The API
and web tests cover the action and who may use it.

## Notes

- 2026-09-27: `codex/video-retry` implements an idempotent request UUID and worker
  acknowledgement UUID on `video_projects` (migration 0104). The worker stores the request in
  `auto.json` before another paid stage, clears the blocked stage's consecutive failure count,
  reports the acknowledgement, then advances one step. A later two-failure block needs a new
  explicit request. Old `auto.json` files have no request field and are accepted.
- Local verification: worker automation 23/23 (Node 24.19.0); admin video web 20/20;
  API video unit 25/25; schema and migration checks 33 passed, 1 PostgreSQL-only skip;
  Ruff, mypy, lint:web, typecheck:web, check:i18n and check:tasks passed. Full `test:tools`
  with Node 24.19.0 had 460 pass, 1 skip, 1 unrelated Windows Temp `EPERM` rename in an
  audio test; that test's 18 cases passed on isolated rerun. Node 24.13.0 crashed on video
  test processes, so use bundled Node 24.19.0 here.
- Production `/admin/videos` state, worker logs, settings, STOP file, deployment and actual
  resume were not checked in this branch; they require the main guarded release flow.

- Until this is deployed, resume by hand. In the worker container, set `status` to `active` in
  `/var/lib/mokaair/video-work/<slug>/auto.json`, and delete `blocked` and that stage's
  `failures` entry. Keep a copy of the file before editing it; the 2026-09-27 copies are named
  `auto.json.before-unblock-20260927`. This is a production change that needs the owner's OK.
