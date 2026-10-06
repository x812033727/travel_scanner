---
id: 2026-10-06-reference-analysis-compare-range-4-6
title: reference_analysis --compare --range 4-6 fails on Windows with ffmpeg's pcm encoder never opening
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T00:33:57Z
completed_at:
branch:
depends_on: []
scope:
  - tools/reference-analysis.test.mjs
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
---

# reference_analysis --compare --range 4-6 fails on Windows with ffmpeg's pcm encoder never opening

## Why

`tools/reference-analysis.test.mjs` (added by #1300 on 2026-10-05) has one test that is red on
the Windows development machine and green in CI (`Video tooling` on main, Linux): "--compare
matches the measured cuts against a study record's lists". Its third call measures the synthetic
clip with `--range 4-6`, and ffmpeg exits with 4294967274 (-22, EINVAL):

```text
measuring 4-6 s of synthetic.mp4 (160x120, 25 fps)
[aost#0:2/pcm_s16le] [enc:pcm_s16le] Could not open encoder before EOF
[out#0/null] Nothing was written into output file, because at least one of its streams received no packets.
frame=    0 ... time=00:00:02.00 ...
Conversion failed!
```

ffmpeg says the pcm audio output of the one-pass filter graph received no packet for that range,
so its encoder never opened and the whole command failed, although the synthetic clip's sine
tone runs the full 6 s. Why it gets none was not looked into. The ffmpeg here is a nightly
build (`ffmpeg version N-125875-g5d4d3bdc61-20260731`); CI's is whatever its runner installs.
Whether a real reference video hits the same thing with a range near its end, on the host or on
a laptop, is not known; the earlier test "ranges are measured where they are asked, times stay
absolute, and the end is clamped to the file" passes on the same machine.

Seen while running `node --test tools/*.test.mjs` for
`2026-10-05-video-worker-image-lacks-locale-thumbnail` on 2026-10-06; red twice in a row (once in
the full top-level run, once alone), so not load.

## Definition of done

- [ ] `node --test tools/reference-analysis.test.mjs` passes on the Windows machine with its
      ffmpeg, or the reason it cannot is written into the dev-and-ci skill's Windows baseline.
- [ ] If the script is at fault, a range that ends at the file's end measures the same on
      Windows as in CI.

## Steps

- [ ] Re-run the failing ffmpeg command by hand (build it from `filterGraph` in the script) and
      see why the audio output gets no packet for 4-6 s, or whether the nightly build changed
      how a stream that ends at the trim point is flushed.
- [ ] Try the same with a release ffmpeg (the version CI uses) to tell the build apart from the
      script.
- [ ] Fix the script or the test, or record the build in the Windows baseline.

## How to verify

```bash
node --test tools/reference-analysis.test.mjs
```

## Notes

- Not related to the font change it was found beside; that pull request touched no file this
  test reads.
