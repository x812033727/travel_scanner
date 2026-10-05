---
id: 2026-10-05-reference-video-offline-analysis
title: Reference video analysis offline: yt-dlp plus ffmpeg scene, motion and speech measures of any length
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:27Z
completed_at:
branch:
depends_on:
  - 2026-10-05-slideshow-risk-craft-rows
scope:
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
  - tools/reference-analysis.test.mjs
  - .agents/skills/youtube-video/references/drama-craft.md
  - docs/videos/drama-craft/README.md
---

# Reference video analysis offline: yt-dlp plus ffmpeg scene, motion and speech measures of any length

## Why

`yt_shot_probe.js` measures a reference video's cut rhythm inside a browser and stops at
60 seconds (`2026-10-05-re-run-yt-shot-probe-past`). The drama craft targets were measured
from five references that way. An offline measurement (yt-dlp download, ffmpeg scene
detection, frame-difference motion share, silence detection) works on any length and writes
the same JSON as the existing reference studies, so the two compare.

## Definition of done

- [ ] `reference_analysis.mjs --url … --out <json>` downloads with yt-dlp (invoked, never
      vendored; Unlicense) to a temp dir and measures cuts (`select='gt(scene,T)'` +
      `showinfo`), motion share (`signalstats` frame differences) and speech density
      (`silencedetect`), writing the shape of `docs/videos/drama-craft/reference-study-*.json`.
- [ ] Re-measures the two videos the browser probe could not finish (`xVXEefk1vWs` 0–120 s,
      `m2qhz2n9618` full); numbers in `drama-craft.md` §8.
- [ ] Only derived numbers enter the repository; downloads are the owner's call (YouTube ToS).

## Steps

- [ ] The script and a test on a lavfi-made clip with known cuts; `drama-craft/README.md`.

## How to verify

```bash
node --test tools/reference-analysis.test.mjs
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url <youtube> --out /tmp/ref.json
```

## Notes

- Supersedes the live-probe need of `2026-10-05-re-run-yt-shot-probe-past` (P3).
- Technique as OpenMontage's video analyzer (AGPL — idea only): yt-dlp + scene detection + ffmpeg.
