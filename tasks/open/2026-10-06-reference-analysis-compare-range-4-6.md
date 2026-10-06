---
id: 2026-10-06-reference-analysis-compare-range-4-6
title: reference_analysis --compare --range 4-6 fails with this machine's ffmpeg
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T00:24:03Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
  - tools/reference-analysis.test.mjs
---

# reference_analysis --compare --range 4-6 fails with this machine's ffmpeg

## Why

`tools/reference-analysis.test.mjs` "--compare matches the measured cuts against a study
record's lists" (added by #1300) fails on the owner's Windows machine. The first two runs of the
script in that test pass; the third, `--range 4-6` on the synthetic clip, makes ffmpeg exit with
4294967274 (-22, EINVAL):

```
[vost#0:0/wrapped_avframe @ …] Terminating thread with error: Invalid argument
[out#0/null @ …] Nothing was written into output file, because at least one of its streams received no packets.
frame=    0 … time=00:00:02.00 …
Conversion failed!
```

so `reference_analysis.mjs` exits 1 and the test's `assert.equal(other.status, 0)` fails. The
message suggests the video stream gets no frame inside the 4–6 s window while the audio runs to
2 s of output; if so, a range near the end of a short clip makes the whole measurement fail
instead of reporting zero cuts, and a real reference measured by range could hit the same thing
on this ffmpeg build.

## Definition of done

- [ ] `node --test tools/reference-analysis.test.mjs` passes on the owner's Windows machine with
  its installed ffmpeg, and still passes in CI.
- [ ] A range whose video stream yields no frame is reported (zero cuts, or a clear message
  naming the range), not a failed ffmpeg run.

## Steps

- [ ] Reproduce with `node --test --test-name-pattern="--compare matches" tools/reference-analysis.test.mjs`
  and run the script's ffmpeg command for `--range 4-6` by hand to see which option the build
  rejects (the seek, the trim of the video stream, or the null muxer with an empty stream).
- [ ] Fix the command (or treat "no packets" for a range as an empty measurement) in
  `.agents/skills/youtube-video/scripts/reference_analysis.mjs`, keeping the measured values the
  other cases pin.

## How to verify

`node --test tools/reference-analysis.test.mjs`, then `npm run test:tools`. The script lives only
under `.agents/skills/` (no `.claude/skills/` copy; `node --test tools/skills.test.mjs` checks that).

## Notes

- Seen 2026-10-06 by claude-opus-5-5-video-package-check during `npm run test:tools` on
  a9e4c3851 plus an unrelated change (no shared import), twice: once with TEMP pointed at an
  empty directory and once with the default TEMP. Local ffmpeg:
  `N-125875-g5d4d3bdc61-20260731`. CI's ffmpeg was not checked; the test may be green on Linux.
- Not diagnosed further; nothing in this note is a measurement of the fix.
