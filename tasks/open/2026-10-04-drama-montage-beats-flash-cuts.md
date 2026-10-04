---
id: 2026-10-04-drama-montage-beats-flash-cuts
title: Sub-second montage beats and flash cuts for battle scenes in the Budaimiao style
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-04T15:45:51Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/drama.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - docs/videos/DRAMA.md
---

# Sub-second montage beats and flash cuts for battle scenes in the Budaimiao style

## Why

The owner pointed at 真一隻布袋喵 as the reference. Its battle videos cut very fast: the measured
video 斬天之招 (m2qhz2n9618, 2026-10-04) has about 287 shots in 267 s, median 0.75 s, and re-cuts one
generated clip at lightning or white flashes so it plays as several beats. Our drama format cannot
express that: a silent beat's `action_seconds` is a whole number from 1 to 8
(`tools/video/core/schema.mjs`), a shot with a line is at least about 1.2 s by the lint estimate, and
`transition` is only `cut` or `dissolve` (`tools/video/core/drama.mjs`), so there is no flash cut.

## Definition of done

- [ ] A drama can hold sub-second silent beats (for example a fractional `action_seconds` down to 0.25 s, or a montage shot whose beats are cuts of one source clip) and assemble times them to the frame.
- [ ] A flash transition (a few white or coloured frames) exists for cuts inside one source clip, and its frames are counted in the timeline.
- [ ] drama-craft targets stay as they are for dialogue scenes; montage scenes are measured separately.

## Steps

- [ ] Ask the owner whether battle montages are wanted in our productions.
- [ ] Design the schema change; plan the review receipt (schema.mjs, drama.mjs and timeline.mjs are bound by `docs/videos/long-form/review.json`).

## How to verify

`node --test tools/video/assemble/drama.test.mjs tools/video/core/*.test.mjs tools/video/long-form/review.test.mjs`

## Notes

- Measurement in `docs/videos/drama-craft/` (the 2026-10-04 Budaimiao study) once it lands.
