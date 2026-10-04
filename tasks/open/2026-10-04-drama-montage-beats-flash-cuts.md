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
  - .agents/skills/youtube-video/scripts/drama_craft_check.mjs
  - .agents/skills/youtube-video/references/drama-craft.md
---

# Sub-second montage beats and flash cuts for battle scenes in the Budaimiao style

## Why

The owner pointed at 真一隻布袋喵 as the reference. Its battle videos cut very fast: across seven
measured videos the battle stretches cut every 0.2-0.5 s, and the two videos a second agent
cross-checked have a median shot of about 0.75-1.0 s (斬天之招, m2qhz2n9618: 225-246 shots in
266.5 s after the verdicts, median 0.88-1.0 s). Hits are joined by a white or coloured flash of a
few frames. (An early reading that the channel re-cuts one clip at lightning flashes was refuted:
the five places that looked like it are lightning inside one shot.) Our drama format cannot
express that: a silent beat's `action_seconds` is a whole number from 1 to 8
(`tools/video/core/schema.mjs`), a shot with a line is at least about 1.2 s by the lint estimate, and
`transition` is only `cut` or `dissolve` (`tools/video/core/drama.mjs`), so there is no flash cut.

## Definition of done

- [ ] A drama can hold sub-second silent beats (for example a fractional `action_seconds` down to 0.25 s, or a montage shot whose beats are cuts of one source clip) and assemble times them to the frame.
- [ ] A flash transition (a few white or coloured frames) exists for cuts inside one source clip, and its frames are counted in the timeline.
- [ ] drama-craft targets stay as they are for dialogue scenes; montage scenes are measured separately (`drama_craft_check.mjs` reads a scene type, so a battle scene is not failed on `size.face`, `size.wide` or `pace.median`).

## Steps

- [ ] Ask the owner whether battle montages are wanted in our productions.
- [ ] Design the schema change; plan the review receipt (schema.mjs, drama.mjs and timeline.mjs are bound by `docs/videos/long-form/review.json`).

## How to verify

`node --test tools/video/assemble/drama.test.mjs tools/video/core/*.test.mjs tools/video/long-form/review.test.mjs`

## Notes

- Measurement: `docs/videos/drama-craft/reference-study-20261004-budaimiao.md` and its per-shot JSON.
- Until this lands, `animation-preproduction` tells agents to mark each scene's type in P2 and
  explain battle scenes row by row in the report; one-second `action_seconds` beats get a battle
  scene to a median of about 1 s.
