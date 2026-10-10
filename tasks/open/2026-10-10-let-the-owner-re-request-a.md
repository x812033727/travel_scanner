---
id: 2026-10-10-let-the-owner-re-request-a
title: Let the owner re-request a skipped dub from the languages card
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T06:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews
  - tools/video/automation/flow.mjs
  - apps/web/components/admin-video-reviews.tsx
---

# Let the owner re-request a skipped dub from the languages card

## Why

On 2026-10-09 the latest languages batch of the forty videos on production showed 49 dub
tracks skipped against 21 ready (`2026-10-09-dub-skipped-because-jev-still-hears` and its
two siblings fixed the three causes). The fixes only help videos made afterwards: a dub
the worker gave up on stays given up. A part's state comes from the languages batches
(`language_states()` in `apps/api/app/video_reviews/admin_service.py`),
`locales_decided_at` is written on the first save only, `dubs/<locale>/skipped.json` in the
work directory is never cleared, and `languages()` in `flow.mjs` passes over a locale whose
dub is skipped. So un-ticking and re-ticking the dub on the panel does nothing, and the
only way to try again is `dub --locale` by hand in the worker container.

The owner asked on 2026-10-10 to fill in the audio the published videos are missing and
is arranging that elsewhere; this ticket is the product path for the same need.

## Definition of done

- [ ] The panel's dub cell in the skipped state offers "再做一次" (content.manage only). It
      records the request against that video and locale, with an audit row.
- [ ] The worker's next round clears that locale's `skipped.json`, resets its dub rounds,
      makes the dub with the current rules and sends a new languages batch; the card shows
      the new result. A request for a part that is not skipped is refused.
- [ ] The request costs synthesis: the cell says so, and the monthly speech budget is
      checked before it is accepted, as for any other paid stage.
- [ ] The languages card shows `kept_lines` (a retake that did not fit kept the earlier
      take) beside the track it belongs to.

## Steps

- [ ] API: a request field or table for "retry this locale's dub", its endpoint and the
      worker's read of it.
- [ ] Flow: honour the request in `languages()`; clear the skip and the rounds.
- [ ] Web: the cell's button and state; `kept_lines` on the card. The strings go in the five
      `admin.json` files, which the duration review receipt binds: the PR needs its increment.

## How to verify

API and automation tests for the request and the retry; then on the host, one video whose
ja dub was skipped for a window over by 0.03 s (`gemini-4-argon-who-can-use-it`) asked
again from the panel ends with a ja track on its card.

## Notes

- Found while fixing `2026-10-09-dub-given-up-as-the-retake`, whose first draft of the
  give-up reason said "tick it again"; that would have been false.
