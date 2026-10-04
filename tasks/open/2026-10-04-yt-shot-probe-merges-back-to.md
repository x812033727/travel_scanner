---
id: 2026-10-04-yt-shot-probe-merges-back-to
title: yt_shot_probe merges back-to-back cuts and counts flashes in high-motion videos
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-04T18:49:05Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/scripts/yt_shot_probe.js
  - .agents/skills/youtube-video/references/drama-craft.md
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

- [ ] On a high-motion video the probe reports the stretches where a run of flagged samples may
      hold several cuts ("suspected multi-cut runs", with start and end), instead of silently
      keeping one cut.
- [ ] `drama-craft.md` §8 (re-measuring reference videos) says that effect-heavy videos need a
      contact-sheet reconciliation and that only ranges may be quoted.
- [ ] The dialogue videos measured on 2026-10-03 give the same cuts as before (no regression).

## Steps

- [ ] Re-run the probe on m2qhz2n9618 and compare with the verified cut list in
      `docs/videos/drama-craft/reference-study-20261004-budaimiao.json` (`cross_check`).
- [ ] Design the run report; keep the default cut list unchanged so earlier studies stay comparable.

## How to verify

Run the probe in the in-app browser on xVXEefk1vWs (2026-10-03 study, 0-120 s) and on
m2qhz2n9618 (2026-10-04 study); the first gives the same 46 cuts, the second lists the runs at
19.75-26 s and 213.5-220.5 s.

## Notes

- A 1/30 s frame-difference scan was tried as a tie-breaker and was too noisy (in-shot
  differences of 20-50, held frames read as zero); 1/8 s and 1/16 s contact-sheet strips decided
  the disputed cuts.
- Nothing was downloaded; the measurement ran on watch pages with the player muted.
