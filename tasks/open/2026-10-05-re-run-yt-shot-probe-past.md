---
id: 2026-10-05-re-run-yt-shot-probe-past
title: Re-run yt_shot_probe past 60 s with a visible in-app browser pane
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T02:00:51Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/references/drama-craft.md
---

# Re-run yt_shot_probe past 60 s with a visible in-app browser pane

## Why

Split from 2026-10-04-yt-shot-probe-merges-back-to. That ticket gave
`.agents/skills/youtube-video/scripts/yt_shot_probe.js` a run report (`runs()`,
`stats().suspected_multi_cut_runs`, `stats().high_motion_share`) and left `cuts()` as it was. Its
live check reached only the first 60 s of each reference video. The in-app browser pane was hidden,
so the paused video never decoded a frame after a seek (readyState stayed at 1). Headless Chrome
through Playwright stopped with the player's "發生錯誤，請重新整理或稍後再試" as soon as a seek passed
the 60 s already buffered. That looks like the site refusing an automated browser, and it was not
worked around. So the second half of the dialogue regression check (xVXEefk1vWs 60-120 s) and the
second run named in the study (m2qhz2n9618, 213.5-220.5 s) have not been seen live yet. The
`high_motion_share` threshold of about 0.1 in `drama-craft.md` §8 also rests on first minutes only.

## Definition of done

- [ ] xVXEefk1vWs, `measure({ start: 0, end: 120 })`: the 46 cuts recorded in
      `docs/videos/drama-craft/reference-study-20261003.json` (cumulative `lengths` of the 0-240
      range below 120 s), and no suspected multi-cut run, or each one explained.
- [ ] m2qhz2n9618, `measure({ start: 0, end: 266.5 })`: suspected runs cover about 19.75-26 s and
      213.5-220.5 s, and the full-length `high_motion_share` is recorded.
- [ ] `drama-craft.md` §8 keeps or corrects the 0.1 threshold and the two measured shares.

## Steps

- [ ] Ask the owner to show the Browser pane (Ctrl+Shift+B) first. `tabs_context` must say the
      pane is displayed, and `document.visibilityState` must be `visible` in the tab.
- [ ] Follow the steps at the top of the probe: viewport 1200x800, paste the file's text, skip any
      pre-roll with a real click, `void __probe.measure(...)`, then poll `__probe.state.status`.
- [ ] Compare against the recorded cut lists. Write the numbers into this ticket's Notes, and into
      §8 only if they change the threshold.

## How to verify

In the in-app browser with the pane visible, run the two measures above. `__probe.stats()` gives
`cuts`, `suspected_multi_cut_runs` and `high_motion_share`. Compare `cuts` with the 2026-10-03
record and with `cross_check[1].verifier_cut_times` in
`docs/videos/drama-craft/reference-study-20261004-budaimiao.json`.

## Notes

- What the split-off ticket measured on 2026-10-05, 0-59.75 s at 0.25 s, headless Chrome, muted,
  throwaway profile, nothing signed in or downloaded:
  - xVXEefk1vWs (360x640 stream): 23 cuts, the same as the first 23 recorded, with the same
    opening counts (5 and 14). No runs; `high_motion_share` 0.014; `near_frozen_share` 0.046.
  - m2qhz2n9618 (640x274, then 854x366; the 2026-10-04 verifier had 1280x548): 33 cuts against
    the verifier's 32. 30 are the same; 9.75 and 36.75 sit 0.25 s from the verifier's 10 and 37;
    20.5 is extra. 11 suspected runs, including 15-18.25 (14 flagged) and 20.5-25.25 (20 flagged).
    `high_motion_share` 0.646. A 1/8 s sheet of 19.5-26 s showed at least 8 changes of setup where
    the probe kept 2 cuts.
- The stream's quality moves the flags on an effect-heavy video. At 20.25 s the histogram distance
  was 0.103, just under 0.11, so the run that the verifier saw unbroken from 19.75 broke into
  19.75-20 and 20.5-25.25 here. Record the frame size with every measurement.
