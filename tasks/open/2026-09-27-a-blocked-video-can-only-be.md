---
id: 2026-09-27-a-blocked-video-can-only-be
title: A blocked video can only be resumed by editing auto.json on the host
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-27T07:32:11Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - apps/api/app/video_reviews
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
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

- [ ] A blocked video's card on `/admin/videos` has a "try again" action for someone with
      `content.manage`. On its next run the worker sets the video back to `active` and
      clears that stage's failure count.
- [ ] A video that fails the same way again is blocked again, with the same limit of two
      failures in a row. The action must not turn into a loop that spends tokens.

## Steps

- [ ] API: record the request on the project, the way `dropped_at` is recorded, and show it
      in the worker's `videos()` list. It probably needs a migration: add its path to the scope.
- [ ] Worker: in `step()`, before the active videos, move a blocked video with a pending
      retry back to `active`, then report the checklist.
- [ ] Web: the action on the card, and the five locales' strings. Add `apps/web/messages` to
      the scope.
- [ ] Tests on each side.

## How to verify

In `tools/video/automation/automation.test.mjs`, a blocked video with a retry request
becomes `active` and advances one step, and a second failure blocks it again. The API
and web tests cover the action and who may use it.

## Notes

- Until this exists, resume by hand. In the worker container, set `status` to `active` in
  `/var/lib/mokaair/video-work/<slug>/auto.json`, and delete `blocked` and that stage's
  `failures` entry. Keep a copy of the file before editing it; the 2026-09-27 copies are named
  `auto.json.before-unblock-20260927`. This is a production change that needs the owner's OK.
