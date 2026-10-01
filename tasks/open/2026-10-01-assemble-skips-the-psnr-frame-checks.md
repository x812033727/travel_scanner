---
id: 2026-10-01-assemble-skips-the-psnr-frame-checks
title: assemble skips the PSNR frame checks for plain slides videos
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-01T07:44:20Z
completed_at:
branch:
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

- [ ] Assembling a plain slides video samples every stills scene again (`checks.json` `metrics.psnr` is not empty).
- [ ] A test fails if `layoutScenes` stops marking its scenes as stills.

## Steps

- [ ] Give `layoutScenes`' scenes `kind: "stills"` (the smallest fix; the cli check then matches).
- [ ] Extend `tools/video/assemble/assemble.test.mjs`.
- [ ] Run `node tools/video/assemble/smoke.mjs --fixture minimal --channel msedge` and confirm `checks.json` has PSNR samples and still passes.

## How to verify

```bash
node --test tools/video/assemble/assemble.test.mjs
node tools/video/assemble/smoke.mjs --fixture minimal --channel msedge --until assemble
```

## Notes

Turning the check back on may surface frames that drifted unnoticed since #861; read
`.agents/skills/youtube-video/references/automated.md` §坑 on the PSNR thresholds before
changing any of them (do not lower them).
