---
id: 2026-10-04-yt-shot-probe-merges-back-to
title: yt_shot_probe merges back-to-back cuts and counts flashes in high-motion videos
status: done
priority: P3
area: tools
owner: claude-opus-5-5-yt-shot-probe-cuts
claimed_at: 2026-10-05T01:19:20Z
created_at: 2026-10-04T18:49:05Z
completed_at: 2026-10-05T02:05:55Z
branch: claude/yt-shot-probe-cuts
depends_on: []
scope:
  - .agents/skills/youtube-video/scripts/yt_shot_probe.js
  - .agents/skills/youtube-video/references/drama-craft.md
  - tools/yt-shot-probe.test.mjs
---

# yt_shot_probe merges back-to-back cuts and counts flashes in high-motion videos

## Why

Measuring the 真一隻布袋喵 battle videos (2026-10-04,
`docs/videos/drama-craft/reference-study-20261004-budaimiao.md`) showed the probe is wrong in both
directions on effect-heavy AI action edits. Inside one shot, lightning, particles and a camera
that never stops change the luma by 20-60 per 0.25 s, as much as a real cut. The probe's `cuts()`
keeps only the first sample of a run of flagged samples, so a stretch of 0.25-0.5 s shots
collapses into one cut (video B, 19.75-26 s and 213.5-220.5 s: no probe cuts, 8 or more real
ones). A finer step flags lightning, explosions growing and whip blur as cuts instead. Two
independent re-measurements against frame strips found the default output about 30% short and a
by-eye contact-sheet count about 50% over. Anyone who quotes the probe's median on such a video
quotes a number that is off by a factor.

## Definition of done

- [x] On a high-motion video the probe reports the stretches where a run of flagged samples may
      hold several cuts ("suspected multi-cut runs", with start and end), instead of silently
      keeping one cut.
- [x] `drama-craft.md` §8 (re-measuring reference videos) says that effect-heavy videos need a
      contact-sheet reconciliation and that only ranges may be quoted.
- [x] The dialogue videos measured on 2026-10-03 give the same cuts as before (no regression).

## Steps

- [ ] Re-run the probe on m2qhz2n9618 and compare with the verified cut list in
      `docs/videos/drama-craft/reference-study-20261004-budaimiao.json` (`cross_check`).
- [x] Design the run report; keep the default cut list unchanged so earlier studies stay comparable.

## How to verify

Run the probe in the in-app browser on xVXEefk1vWs (2026-10-03 study, 0-120 s) and on
m2qhz2n9618 (2026-10-04 study); the first gives the same 46 cuts, the second lists the runs at
19.75-26 s and 213.5-220.5 s.

## Notes

- A 1/30 s frame-difference scan was tried as a tie-breaker and was too noisy (in-shot
  differences of 20-50, held frames read as zero); 1/8 s and 1/16 s contact-sheet strips decided
  the disputed cuts.
- Nothing was downloaded; the measurement ran on watch pages with the player muted.
- Claimed with `--force` on 2026-10-05 (claude-opus-5-5-yt-shot-probe-cuts). The only overlap was
  2026-10-03-illustrated-slides-round-2-a-family (claude-fable-5-1-illustration-round2, `review`,
  41 h old, scope `.agents/skills/youtube-video/references`). Its work landed as #1172
  (b0a264567), and the board sweep #1231 has since released that claim.
- Scope: `tools/yt-shot-probe.test.mjs` was added for the regression test. `test:tools` collects
  `tools/*.test.mjs`, so a `tools/tests/` folder would not have run. No `.claude/skills/**`
  copy is in scope: only SKILL.md is mirrored there (#1222), and the youtube-video SKILL.md did not
  change.
- What changed: the cut rule moved into `flagged()`, and `cuts()` folds its output exactly as
  before. `runs(options, { min = 3 })` returns `{ start, end, flagged }` for every stretch of three
  or more flagged samples in a row, which `cuts()` keeps as one cut at `start`. `stats()` adds
  `suspected_multi_cut_runs` and `high_motion_share`: the share of samples inside shots whose luma
  difference is 20 or more, on the same base as `near_frozen_share`. Every earlier field is
  unchanged. `flagged` and `runs` are exposed on `window.__probe`. The header gained step 6
  (sheet each run at 1/8 s and quote a range) and a paragraph on effect-heavy edits.
- No regression, in code: `tools/yt-shot-probe.test.mjs` runs the file in `node:vm` with a stub
  page. It compares `cuts()` and every earlier `stats()` field with a frozen copy of the
  2026-10-03 code. The comparison covers 142 synthetic series (dialogue-like, a 0.125 s step, a
  range starting at 1800 s, and 40 effect-heavy ones) under 3 option sets. Six one-constant
  mutations of the rule (spike factor, `mad`, `hd`, `soft`, the fold distance, `>=` against `>`)
  each failed it. The seventh, raising the spike floor from 4 to 5, changes nothing while `soft`
  is 16.
- Live, 2026-10-05, first 60 s only. The in-app pane was hidden: the paused video stayed at
  readyState 1 and seeks failed, so that try was stopped. The installed Chrome was driven headless
  through Playwright instead (muted, throwaway profile, no sign-in, nothing downloaded). Two
  0-120 s attempts never finished. The second one, which had set an ordinary Chrome user agent,
  showed the player's "發生錯誤，請重新整理或稍後再試" once a seek passed the 60 s already buffered.
  That looks like the site refusing an automated browser. It was not worked around: the user
  agent override was dropped, and the measured runs below kept the headless one and stayed under
  60 s. Measured 0-59.75 s at 0.25 s:
  - xVXEefk1vWs (360x640): 23 cuts, identical to the first 23 of the 46 recorded, with the same
    opening counts (5 and 14). No runs; `high_motion_share` 0.014.
  - m2qhz2n9618 (640x274, then 854x366): 33 cuts against the verifier's 32 in the same span. 30 are
    the same; 9.75 and 36.75 sit 0.25 s from the verifier's 10 and 37; 20.5 is extra. There are 11
    suspected runs, including 15-18.25 (14 flagged) and 20.5-25.25 (20 flagged), and
    `high_motion_share` is 0.646. A 1/8 s sheet of 19.5-26 s showed at least 8 changes of setup
    where the probe kept 2 cuts (19.75, 20.5).
  - At this lower quality the verifier's unbroken 19.75 run broke at 20.25 (histogram distance
    0.103, just under 0.11). On such videos the stream's quality moves the flags too.
- Left: the first Steps item past 60 s (the 213.5-220.5 s run) and the dialogue check for
  60-120 s, both live. Split to 2026-10-05-re-run-yt-shot-probe-past, which needs the pane
  visible. The 0.1 threshold for `high_motion_share` in §8 rests on the two first minutes above;
  that ticket confirms or corrects it.
