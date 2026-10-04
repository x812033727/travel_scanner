---
id: 2026-10-04-still-shot-camera-moves-travel-in
title: Still-shot camera moves travel in steps, not smoothly
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-04T01:41:20Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - docs/videos/DRAMA.md
  - docs/videos/ILLUSTRATED.md
---

# Still-shot camera moves travel in steps, not smoothly

## Why

A still shot's camera move (`motionSegmentArgs` in `tools/video/assemble/drama.mjs`: the keyframe
scaled 1.25×, then `zoompan`) does not glide. Found on 2026-10-04 while measuring why an
illustrated slides final was 895 MB (`2026-10-04-illustrated-slides-finals-fit-the-review`):
the picture holds for a few frames, then jumps.

Measured on the picture chain alone (lossless, before any encoding) for five shots of
`openai-devday-2026-recap`, counting consecutive frame pairs that are bit-identical:

| Shot | Move | Length | Identical pairs | In the middle third | Longest hold |
| --- | --- | --- | --- | --- | --- |
| `alley-van` | pan-left | 4.9 s | 51% | 29% | 11 frames |
| `steamer-lift` | pan-right | 2.8 s | 47% | 21% | 7 frames |
| `bike-talk` | drift | 4.3 s | 31% | 7% | 11 frames |
| `kitchen-wide` | push-in | 7.5 s | 16% | 0% | 8 frames |
| `kiln-talk` | pull-out | 4.3 s | 12% | 0% | 5 frames |

The numbers fit a crop window that only sits on even source pixels: `steamer-lift` travels 88.9
source pixels in 82 steps, which is 44 two-pixel jumps and 46% of the pairs held. `zoompan`
aligns the window to the chroma grid of its input, and this video's keyframes are JPEGs, which
reach it as 4:2:0, so every jump is two source pixels: 1.6 pixels of the 1080p picture, with
held frames between. The same two keyframes converted to RGB PNGs and run through the same
chain hold 17% (`steamer-lift`) and 20% (`alley-van`) of their pairs instead of 47% and 51%:
one source pixel a step, 0.8 of an output pixel. So which way a still moves depends today on
the file type the image model returned. A pan at its fastest moves about 1.6 source pixels a
frame, so it alternates between holding and jumping all the way through; a zoom changes the
window's size a whole pixel at a time. On a slow move over fine detail (the halftone of the
riso looks) this reads as a faint judder rather than a camera, and each jump lands the dots on a
new sub-pixel phase that the encoder has to code again, which is part of why these segments
cost 15 Mbit/s at CRF 18.

Not fixed in that ticket: it changes how every still moves, which the owner should see before
it ships, and it changes the segments' size again.

## Definition of done

- [ ] On the same five shots, a pan or drift holds no frame in the middle third of the move and
      its largest jump is under one pixel of the 1080p picture.
- [ ] Frame 0 of a move that starts at identity still matches the keyframe (the existing check,
      PSNR ≥ 22), and the last frame still lands where `zoompanExpr` says.
- [ ] The size of a re-assembled illustrated final is measured before and after and written into
      `docs/videos/ILLUSTRATED.md` §成片大小 (the 8 Mbit/s cap on motion segments bounds it either way).
- [ ] The owner has seen one shot of each move before and after, side by side.

## Steps

- [ ] Reproduce the table: render a shot's picture chain to a lossless file and compare each
      frame with the next (`psnr` between the stream and itself delayed one frame; `inf` is a
      held frame).
- [ ] Try the cheap fix first: a 4:4:4 format (`format=yuv444p` or `gbrp`) ahead of `zoompan`, so
      the window sits on every source pixel (0.8 output pixels a step) whatever the keyframe's
      file type; the PNG run above says this halves the step and still leaves about a fifth
      of a short pan's pairs held (where in the move was not looked at).
- [ ] If that is not smooth enough, a larger `MOTION_SOURCE_SCALE` (the worker has 3 GB and no GPU:
      measure memory and time at 2× and 3×), or a per-frame `scale`+`crop` with sub-pixel offsets
      in place of `zoompan`.
- [ ] Bump `MOTION_ENCODER_VERSION` (every motion segment is re-encoded; approved finals are not
      touched until someone re-assembles them) and update the tests that pin the graph.
- [ ] Shorts (`tools/video/shorts/motion.mjs`) use their own linear `zoompan`: check whether they
      step the same way and say so here, without widening this ticket.

## How to verify

```bash
node --test tools/video/assemble/drama.test.mjs
# one shot's chain to a lossless file, then frame n against frame n+1:
ffmpeg -i shot-ref.mkv -lavfi "[0:v]setpts=N/(30*TB),split[a][b];[b]trim=start_frame=1,setpts=N/(30*TB)[c];[a][c]psnr=stats_file=pairs.txt" -f null -
grep -c "psnr_y:inf" pairs.txt   # held pairs; expect none in the middle third
```

## Notes

- Compare the two files with `setpts=N/(30*TB)` on both inputs: a `.mkv` rounds timestamps to
  milliseconds and `psnr`/`libvmaf` then pair every third frame with its neighbour.
- A smooth move makes every frame differ from the last, so expect the uncapped bitrate to rise;
  the cap added by `2026-10-04-illustrated-slides-finals-fit-the-review` keeps the size bounded,
  and the quality under the cap is what to look at.
