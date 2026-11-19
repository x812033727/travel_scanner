---
id: 2026-11-19-heimao-series-start-with-no-intro
title: Heimao-style series start with no intro (sothatswhy, curio, story)
status: in-progress
priority: P1
area: tools
owner: claude-opus-elegant-hypatia
claimed_at: 2026-11-19T01:18:43Z
created_at: 2026-11-19T01:10:00Z
completed_at:
branch: claude/elegant-hypatia-07i3yx
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/assemble/branding.mjs
  - tools/video/assemble/branding.test.mjs
  - tools/video/assemble/cli.mjs
  - docs/videos/BRANDING.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Heimao-style series start with no intro (sothatswhy, curio, story)

## Why

Owner 2026-11-19: 「以後開頭就不要有片頭了，直接開始」. New episodes of 原來如此事務所 (`sothatswhy-`),
奇聞檔案局 (`curio-`) and the brand stories (`story-`, `isStory(series)`) open on their first line at
0:00; the outro stays. Today `defaultIntroAt` (tools/video/core/branding.mjs) puts the intro at the
start for all three, and `validateBranding({ enabled: false })` would drop the outro too.

Blocked only by two stale October claims that still list `tools/video/core/branding.mjs`
(2026-10-12-lengthen-the-channel-outro-to-20, 2026-10-24-episodes-of-a-compilation-series-carry;
no remote branches). The owner must allow taking over those scopes (`claim --force`).

## Definition of done

- [x] A new placement `intro_at: "none"` (INTRO_NONE): the final is body + outro, `intro_frames: 0`
      in the applied record, its own branding hash (v2 tag carries the placement).
- [x] `defaultIntroAt` returns `none` for `sothatswhy-`, `curio-`, `story-` and `isStory(series)`.
      Pinned `branding.json` cuts keep their placement (nothing already built moves).
- [x] Dubs, captions, presentation timeline and QA accept a zero-length intro.

## Steps (plan)

- [x] core/branding.mjs: `INTRO_NONE`, add to `INTRO_PLACEMENTS`; `introAtFrame` returns 0 for none;
      `presentationTimeline` offset = 0 for none (helper `introFrames(branding)`); `defaultIntroAt`.
- [x] assemble/branding.mjs: `checkedIntroAt` (none -> frame 0), `clipsOf` (none -> [body, outro]),
      `wrapVideo` join list [body, outro] without encoding the intro, `appliedRecord` intro_frames 0.
- [x] assemble/cli.mjs:316 only re-places `after_first_chapter` to start when there is no second chapter, never `none`.
- [x] renewal.mjs / renewal-handoff.mjs already refuse any pin with `intro_at`; leave them.
- [x] duration.mjs `bookendFrames` already accepts 0.
- [x] BRANDING.md §片頭位置 table; tests.

## Notes

- Owner allowed `--force` over the two stale October claims (2026-11-19).
- Real ffmpeg check: a 300-frame body with a 90-frame outro and `intro_at: "none"` gives a 390-frame final.

## How to verify

```bash
npm run test:tools
```
