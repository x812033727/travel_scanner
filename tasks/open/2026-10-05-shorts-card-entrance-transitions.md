---
id: 2026-10-05-shorts-card-entrance-transitions
title: Shorts card entrance transitions captured with the long video's paused-animation renderer
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:23Z
completed_at:
branch:
depends_on:
  - 2026-10-03-illustrated-slides-lint-heuristics-the-shorts
scope:
  - tools/video/render/browser.mjs
  - tools/video/render/browser.test.mjs
  - tools/video/shorts/build.mjs
  - tools/video/shorts/motion.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/layouts.mjs
  - tools/video/shorts/motion.test.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/shorts/smoke.mjs
  - docs/videos/SHORTS.md
  - .agents/skills/youtube-video/references/shorts.md
---

# Shorts card entrance transitions captured with the long video's paused-animation renderer

## Why

A Short's cards cut in hard: `shorts/build.mjs renderFrames` screenshots one still per phrase
with JavaScript off, and `motion.mjs` holds it. The long video's renderer
(`render/browser.mjs`) already captures CSS entrances deterministically by pausing
`document.getAnimations()` and seeking frame by frame (up to 18 frames). Reusing that gives
every scene's first card a rise-in without a per-frame renderer (Remotion is out: company
licence) and without changing how layout is measured.

## Definition of done

- [ ] The first card of each scene enters over ≤ 12 frames (headline, rule, rows staggered by
      CSS `animation-delay`), captured by pausing and seeking the page's animations at 1/30 s
      steps in the existing `renderFrames` session.
- [ ] `cardsList` carries one-frame entries for the entrance then the still; segments still
      join with `-c copy`; `MOTION_VERSION` is bumped.
- [ ] The layout measurement is taken on the settled still, never on an entrance frame.
- [ ] The smoke asserts the entrance frames exist and that frame 0 of a scene differs from its still.

## Steps

- [ ] Export `pauseAnimations` / `seekAnimations` page functions from `render/browser.mjs`.
- [ ] Theme CSS for the entrance in `layouts.mjs` / `core.mjs` (rise + fade, no bounce).
- [ ] `build.mjs`: seek, screenshot each entrance frame to `frames/NNN-eKK.png`, measure the
      settled still; `motion.mjs cardsList` entries; version bump; tests and smoke.
- [ ] Docs: `SHORTS.md` §工具端, `references/shorts.md`.

## How to verify

```bash
node --test tools/video/shorts/*.test.mjs
node tools/video/shorts/smoke.mjs --workdir /tmp/shorts-smoke
ffmpeg -i <build>/upload/final.mp4 -vf "select='lt(n\,12)'" -fps_mode vfr /tmp/e-%02d.png   # the card rises in
```

## Notes

- After `2026-10-05-shorts-karaoke-captions-estimated-timing` (PR #1292): the caption layer
  is separate, so later cues of a scene can share one card; add that ticket to `depends_on`
  once it is in `tasks/done/`.
- `2026-10-03-illustrated-slides-lint-heuristics-the-shorts` names `shorts/motion.mjs`; only
  its receipt step is left.
- The deterministic capture needs `--disable-gpu --disable-threaded-animation` and two
  `requestAnimationFrame`s before each screenshot (the long video's lesson of 2026-10-02).
