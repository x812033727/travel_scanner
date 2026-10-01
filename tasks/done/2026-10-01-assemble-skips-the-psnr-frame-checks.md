---
id: 2026-10-01-assemble-skips-the-psnr-frame-checks
title: assemble skips the PSNR frame checks for plain slides videos
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-01T21:01:58Z
created_at: 2026-10-01T07:44:20Z
completed_at: 2026-10-01T21:03:44Z
branch: claude/assemble-psnr
depends_on: []
scope:
  - tools/video/assemble/plan.mjs
  - tools/video/assemble/assemble.test.mjs
---

# assemble skips the PSNR frame checks for plain slides videos

## Why

`assemble` is supposed to prove each scene's segment shows its frames: it samples the first,
second and last frame of every stills segment and compares it with the source PNG by PSNR
(`segmentSamples`, `sampleProblem` in `tools/video/assemble/plan.mjs`; DESIGN.md "每章開頭抽格比對來源 PNG").
In `tools/video/assemble/cli.mjs` the loop only samples scenes with `scene.kind === "stills"`.
`layoutDrama` (drama and illustrated videos) sets that kind, but `layoutScenes`, which lays out
every plain slides video, returns `{ id, frames, start_frame, entries }` with no `kind`. So for a
plain slides video `checks.json` has `metrics.psnr: []` and a misplaced frame would pass. The
condition came in with #861 (binge series). Found on 2026-10-01 while assembling the screencast
fixture (`tools/video/screencast/fixtures/tutorial/video.json`): 5 stills scenes, 0 PSNR samples.

## Definition of done

- [x] Assembling a plain slides video samples every stills scene again (`checks.json` `metrics.psnr` is not empty).
- [x] A test fails if `layoutScenes` stops marking its scenes as stills.

## Steps

- [x] Give `layoutScenes`' scenes `kind: "stills"` (the smallest fix; the cli check then matches).
- [x] Extend `tools/video/assemble/assemble.test.mjs`.
- [x] Run `node tools/video/assemble/smoke.mjs --fixture minimal --channel msedge` and confirm `checks.json` has PSNR samples and still passes.

## How to verify

```bash
node --test tools/video/assemble/assemble.test.mjs
node tools/video/assemble/smoke.mjs --fixture minimal --channel msedge --until assemble
```

## Notes

Turning the check back on may surface frames that drifted unnoticed since #861; read
`.agents/skills/youtube-video/references/automated.md` §坑 on the PSNR thresholds before
changing any of them (do not lower them).
- 2026-10-02 (claude-opus-5-5): `layoutScenes` now returns `kind: "stills"`; drama's own
  `{ ...laid, kind: "stills" }` is unchanged. New test: every laid-out scene is stills and
  has PSNR samples. `node --test tools/video/assemble/*.test.mjs`: 40 pass. Smoke
  (`--fixture minimal --channel msedge --until assemble`): ok, `checks.json`
  `metrics.psnr` has 9 samples (3 scenes x first/second/last), 45.1–48.8 dB, checks ok.
  No threshold touched.
