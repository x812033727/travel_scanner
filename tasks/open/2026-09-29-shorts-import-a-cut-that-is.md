---
id: 2026-09-29-shorts-import-a-cut-that-is
title: "Shorts import: a cut that is not 30 fps fails with a misleading caption-length error"
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-29T00:08:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/import.mjs
  - tools/video/shorts/pipeline.test.mjs
---

# Shorts import: a cut that is not 30 fps fails with a misleading caption-length error

## Why

`node tools/video/shorts/cli.mjs import` takes the length of the cut as its frame count divided
by 30 (`PROFILE.fps`), whatever the file's frame rate is. A 24 fps cut of 28.97 s comes out as
23.17 s, and the import stops with "the captions run to 28.97s, the cut to 23.17s", which sends
the reader to the captions when the problem is the frame rate. All twelve season-one Shorts of
PR #880 (24 fps review cuts) failed this way on 2026-09-29; re-encoding them to 30 fps first
fixed it.

## Definition of done

- [ ] A cut whose frame rate is not the Shorts profile's is refused with a message that names
      the frame rate (and says to re-encode to 30 fps), before the captions are compared.
- [ ] The caption comparison uses the cut's real length.
- [ ] A test with a 24 fps probe.

## Steps

- [ ] Check `measured.video.r_frame_rate` right after `measureFinal`, and read the length from
      the stream's duration.
- [ ] Test.

## How to verify

`node --test tools/video/shorts/pipeline.test.mjs`; an import of a 24 fps cut names the frame rate.

## Notes

- The re-encode that worked (picture and sound only, content unchanged):
  `-vf fps=30,scale=1080:1920,format=yuv420p -c:v libx264 -crf 18` and a two-pass
  `loudnorm=I=-14:TP=-1.5:LRA=11` into AAC at 48 kHz. A one-pass loudnorm left a 29 s cut at
  −15.55 LUFS, outside the check's −14 ± 1.
