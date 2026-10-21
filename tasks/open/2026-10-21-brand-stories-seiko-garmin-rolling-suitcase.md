---
id: 2026-10-21-brand-stories-seiko-garmin-rolling-suitcase
title: Brand stories seiko, garmin, rolling-suitcase: unblock the worker and make their eight languages
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-21T16:37:42Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/brand-stories/languages-unblock-20261021.md
---

# Brand stories seiko, garmin, rolling-suitcase: unblock the worker and make their eight languages

## Why

Five brand stories have all eight languages ticked and every part still "working" on the site:
story-adapt-doraemon-after-fujiko, story-adapt-seiko-quartz-astron, story-garmin-smartphone-pivot-worker-2026,
story-dyson-japan-first-20261021, story-rolling-suitcase-v2. The host worker makes these itself, but three show
`blocked` in the worker list (seiko, garmin, rolling-suitcase; seiko's dub retries read `blocked` for en ja ko),
so their languages will not start until the block is cleared. The reason lives in the worker's `auto.json` on the
host, which a cloud session without SSH cannot read.

## Definition of done

- [ ] The three blocked stories are unblocked (or dropped with a reason) and each of the five has a languages batch.

## Steps

- [ ] On /admin/videos open each blocked story, read its block reason, press 「重試這支影片」 when it is transient.
- [ ] Otherwise on the host (prod-host-ops skill): read `<VIDEO_WORKDIR>/<slug>/auto.json` and the worker log, fix, retry.
- [ ] Confirm the languages batch arrives for all five.

## Notes

Filed 2026-10-21 by claude-opus-5-5-curio-remake-langs at the owner's request.
