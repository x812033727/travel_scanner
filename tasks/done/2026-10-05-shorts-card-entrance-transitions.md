---
id: 2026-10-05-shorts-card-entrance-transitions
title: Shorts card entrance transitions captured with the long video's paused-animation renderer
status: done
priority: P2
area: tools
owner: claude-fable-5-1-entrances
claimed_at: 2026-10-05T18:38:56Z
created_at: 2026-10-05T16:08:23Z
completed_at: 2026-10-05T23:08:12Z
branch: claude/shorts-card-entrances
depends_on:
  - 2026-10-03-illustrated-slides-lint-heuristics-the-shorts
  - 2026-10-05-shorts-karaoke-captions-estimated-timing
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

- [x] The first card of each scene enters over ≤ 12 frames (headline, rule, rows staggered by
      CSS `animation-delay`), captured by pausing and seeking the page's animations at 1/30 s
      steps in the existing `renderFrames` session. (Every scene after the first: see Notes on
      why the first scene opens on its settled card.)
- [x] `cardsList` carries one-frame entries for the entrance then the still; segments still
      join with `-c copy`; `MOTION_VERSION` is bumped.
- [x] The layout measurement is taken on the settled still, never on an entrance frame.
- [x] The smoke asserts the entrance frames exist and that frame 0 of a scene differs from its still.

## Steps

- [x] Export `pauseAnimations` / `seekAnimations` page functions from `render/browser.mjs`.
- [x] Theme CSS for the entrance in `layouts.mjs` / `core.mjs` (rise + fade, no bounce).
- [x] `build.mjs`: seek, screenshot each entrance frame to `frames/NNN-eKK.png`, measure the
      settled still; `motion.mjs cardsList` entries; version bump; tests and smoke.
- [x] Docs: `SHORTS.md` §工具端, `references/shorts.md`.

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

### 2026-10-05 done (claude-fable-5-1-entrances, branch `claude/shorts-card-entrances` on top of `claude/shorts-six-beat`, PR #1310)

- Claimed with `--force`: the dependency `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`
  is open and unowned, and its one unticked step (rebinding the long-form duration receipt for
  `core/drama.mjs`, `core/drama.test.mjs`, `media/look-keyframes.test.mjs`) touches none of this
  scope; its `motion.mjs` item (the 32% comment) is already ticked. The karaoke ticket is in
  `tasks/done/`, so it is added to `depends_on` as the first note asked.
- **The first scene does not enter.** Frame 0 of an entrance is the card before anything has
  moved (`fill-mode: both` at time 0: content at opacity 0), and the six-beat ticket (#1310, on
  this branch) made the Short's frame 0 the cover (`grammar`: cover == frame 0, first headline
  ≤ 14 characters so the thumbnail reads) and the frame the loop tail returns to. A first scene
  that rose in would make the thumbnail an empty card. So `entering` in `renderFrames` is the
  first cue of every span but the first; `checks.json.motion[0].entrance` is 0 and the smoke
  asserts it. Everything else in the DoD holds for every later scene.
- **Scripts on for the card page.** Probed 2026-10-05 in the cloud container (Playwright 1.63,
  Chromium 141): with `javaScriptEnabled: false`, `document.getAnimations()` and
  `animation.pause()` work from `page.evaluate`, but a `requestAnimationFrame` callback never
  fires, so `seekAnimations` hangs forever (`page.evaluate` has no timeout). The cards are the
  tool's own escaped markup, so they are drawn in a second context of the same browser with
  scripts on; the evidence HTML keeps the scripts-off page and the `<script|iframe|object|embed>`
  refusal. The launch now carries the long video's `LAUNCH_ARGS`.
- Every card (not only the entering ones) is drawn with the entrance CSS and seeked past its
  end before the measurement and the still, so each still is drawn through the same layer
  treatment and a cue change inside a scene cannot shimmer the text.
- The entrance (`layouts.mjs ENTRANCE`): 28 px rise + fade, 240 ms, 40 ms stagger capped at the
  fifth element, `cubic-bezier(0.2, 0.7, 0.2, 1)` (no overshoot), `animation-play-state: paused`
  in the CSS so a card never moves on its own clock. Frame count = ceil(end / 33.33 ms) capped at
  `ENTRANCE_FRAMES` (12): the smoke's six scenes give 0, 12, 11, 11, 10, 9 (53 entrance frames).
- Measured 2026-10-05 on the smoke: frames 288–304 of `final.mp4` pulled with ffmpeg and looked
  at: the headline rises first, the rule, then each row a step later under the 15-frame
  dissolve from the previous card, settled by frame 300; two builds of the same script give the
  same sha256 for every PNG in `frames/` and `captions/`. 205 shorts + render tests green with
  `VIDEO_RENDER_BROWSER_TESTS=1` (the long video's regression and the new page test of the
  shared functions both ran in Chromium).
- The one-frame `duration 0.033333` entries sum 4 µs short of the exact grid over 12 frames; the
  concat demuxer's rounding to the 1/30 time base absorbs it (the long video's `concatList`
  rounds cumulatively for the same reason; the Shorts list stays per entry so the plain list is
  byte-identical).
- Not done here, by design: a flag to turn the entrance off (the DoD asks for the entrance on
  every build; imported cuts carry none); an entrance on the first scene (see above); any
  change to `segmentArgs`, `cardsList` or the caption layer.
- Environment notes: the worktree had no `node_modules`; the shared disk was full (0 MB), so this
  session removed its own partial `npm ci` and linked the main checkout's `node_modules` into the
  worktree instead; `npm cache clean --force` freed 291 MB. A sibling worktree
  (`claude/shorts-from-drama`) also edits `docs/videos/SHORTS.md` and `references/shorts.md`;
  expect a docs merge when both land.
