---
id: 2026-10-04-illustrated-slides-finals-fit-the-review
title: Illustrated-slides finals fit the review store
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1-final-size
claimed_at: 2026-10-04T02:10:30Z
created_at: 2026-10-04T01:21:39Z
completed_at:
branch: claude/illustrated-final-size
depends_on: []
scope:
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - apps/api/app/config.py
  - .env.example
  - docs/videos/DRAMA.md
  - docs/videos/BINGE.md
  - docs/videos/HANDS-OFF.md
  - docs/videos/ILLUSTRATED.md
  - .agents/skills/youtube-video/references/automated.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Illustrated-slides finals fit the review store

## Why

An illustrated slides video's final cut is far larger than the pipeline assumed, and the
publish gate refused it.

What happened on 2026-10-04 with `openai-devday-2026-recap` (illustrated slides, 74 pictures
under camera moves, look preset `riso-navy` with halftone grain, 13:22 at 1080p30, made on the
owner's machine):

- `assemble` wrote a `final.mp4` of 895 MB, 67 MB a minute, 8.9 Mbit/s overall.
- `review-push --gate publish` sends the whole upload package, the 1080p `final.mp4` included
  (`tools/video/review/sync.mjs` `publishSubmission`; only a compilation keeps its file at
  home). The site answered 413 `video_review_file_too_large`: `apps/api/app/video_reviews/storage.py`
  enforces `video_review_max_file_bytes`, whose default was 400,000,000. The final gate before
  it sends a 720p preview (90 MB here), so nothing warned earlier.
- `docs/videos/HANDS-OFF.md` said a final is "about 90–100 MB". That is a plain slides video.
- Stopgap, with the owner's consent: the production host's `.env` got
  `VIDEO_REVIEW_MAX_FILE_BYTES=1500000000` and the api container was recreated. The store's
  total limit stayed 20 GB and held 6.5 GB before this file.

Where the bytes are (the segments of that final, x264 CRF 18):

| Segments | Count | Running time | Size | Bitrate |
| --- | --- | --- | --- | --- |
| pictures under a camera move (`motion`, `-tune film`) | 74 | 422 s (53%) | 804 MB (90%) | 15.3 Mbit/s; 6.6 to 24.4 |
| single-state cards that drift (also `motion`) | 11 | 60 s | 18 MB | 2.4 Mbit/s |
| cards with reveals (`stills`, `-tune stillimage`) | 22 | 321 s | 41 MB | 1.0 Mbit/s |
| audio (AAC 384 kbit/s) | | 802 s | 33 MB | |

YouTube asks 8 Mbit/s of a 1080p30 SDR upload. The motion segments average twice that and
peak at three times it: halftone dots and paper grain are resampled on every frame of a move
and CRF 18 codes all of it.

Three fixes were on the table:

1. **Encode smaller.** Measured (below): a third of the size is not clean. Half is.
2. **Treat a large final like a compilation** (the file stays in the work directory and the site
   serves it from there). Rejected: the site reads the worker's volume, so it only works for
   videos made on the host; this one was made on the owner's machine. It also needs API and
   tool changes in receipt-bound files for a path nothing else needs.
3. **Raise the limit.** Needed whatever the encoder does: no clean setting brings a 13-minute
   illustrated final under 400 MB, and since #1186 a video has no upper length.

Decision: a bitrate cap on motion segments at YouTube's own figure (1), and a default limit
that fits what the pipeline makes (3).

## Definition of done

- [x] The encoder setting is chosen from measurements on the real pictures, with frames compared,
      and the numbers are in `docs/videos/ILLUSTRATED.md` §成片大小.
- [x] The same video re-assembled with the new setting passes `assemble`'s own checks and its
      `final.mp4` is 535 MB (was 895).
- [x] A site with no `VIDEO_REVIEW_MAX_FILE_BYTES` in its environment accepts that file
      (default 1.5 GB).
- [x] `docs/videos/HANDS-OFF.md`, `docs/videos/ILLUSTRATED.md` and the `youtube-video` skill's
      `references/automated.md` state sizes that were measured, and what 413 and 507 mean.
- [x] The duration receipt binds the changed `automated.md`, signed by a reviewer who is not
      the author.
- [x] This ticket says what the host setting should be afterwards (Notes).

## Steps

- [x] Break the 895 MB down by segment kind and by camera move.
- [x] Sweep CRF and `-maxrate` on eight shots against a lossless render of the repo's own
      picture chain: size, VMAF, the worst shot's worst 1% of frames, PSNR; then the same after
      a second encode at 4 Mbit/s, standing in for the platform's transcode.
- [x] Compare frames at 1:1 and at 2× on the hardest shot.
- [x] `MOTION_MAX_RATE` 8M, `MOTION_RATE_BUFFER` 16M on motion segments only;
      `MOTION_ENCODER_VERSION` v4; clip and slide segments and their versions untouched.
- [x] Re-assemble the real video in a copy of its work directory.
- [x] Default `video_review_max_file_bytes` 1.5 GB; `.env.example` says so.
- [x] Documents; `DRAMA.md` and `BINGE.md` no longer say a motion segment encodes exactly like
      a clip.
- [x] Independent DURATION_ONLY increment for `automated.md`.

## How to verify

```bash
node --test tools/video/assemble/drama.test.mjs     # the cap is on motion segments, not on clips
node tools/video/long-form/cli.mjs check            # PASS: the receipt binds automated.md
cd apps/api && uv run python -c "from app.config import Settings; print(Settings.model_fields['video_review_max_file_bytes'].default)"   # 1500000000
```

The size, on any illustrated slides video with a work directory: run `assemble` and look at
`final.mp4`. Expect about 40 MB a minute when half the running time is pictures; no motion
segment in `segments/` above about 10 Mbit/s (`ffprobe -show_entries format=bit_rate`).

To repeat the measurement: render a shot with `motionSegmentArgs`'s inputs and graph to a
lossless file (`-c:v libx264 -qp 0`), encode that file with `encodeArgs`'s flags changing only
the setting under test, and compare with
`[0:v]setpts=N/(30*TB)[a];[1:v]setpts=N/(30*TB)[b];[a][b]libvmaf=feature=name=psnr`. Without the
two `setpts` a `.mkv` reference pairs every third frame with its neighbour and the scores are
wrong by ten points.

## Notes

### The host setting afterwards

**Leave `VIDEO_REVIEW_MAX_FILE_BYTES=1500000000` in the production `.env` as it is.** Once this
change is deployed the code's default is the same number, so the line no longer carries the
publish gate, and removing it or keeping it changes nothing; there is nothing to do on the
host for this ticket, and nothing was done on it. Two cases that do need the owner:

- Before the first binge compilation: 2,500,000,000 a file and
  `VIDEO_REVIEW_MAX_TOTAL_BYTES=30000000000` (`docs/videos/BINGE.md`; never set on the host, which
  has no compilation yet).
- The total, still the default 20 GB: an illustrated final now stays in the store at about
  0.63 GB with its preview (0.99 GB before the cap) from the publish gate until seven days after
  it is marked published. Thirty fit; two a day published promptly is fourteen alive, about
  9 GB, beside the 6.5 GB already there. A final that waits in 「可以上架」 unpublished stays until
  it is published, and that is what would fill the store (507 `video_review_store_full`).

### What was measured

Eight shots, 43.1 s, one or more of every move, 6.6 to 24.4 Mbit/s at CRF 18. Size is against
CRF 18; VMAF and PSNR against the lossless render; "after" is VMAF once re-encoded at 4 Mbit/s
(five shots).

| Motion segments | Mbit/s | Size | VMAF | Worst shot, worst 1% | PSNR-Y | After |
| --- | --- | --- | --- | --- | --- | --- |
| CRF 18 (before) | 16.6 | 100% | 97.7 | 94.2 | 41.4 | 93.4 |
| CRF 20 | 12.5 | 75% | 97.3 | 93.3 | 39.8 | |
| CRF 22 | 9.3 | 56% | 96.7 | 92.4 | 38.3 | |
| **CRF 18, maxrate 8M, bufsize 16M (chosen)** | **8.3** | **50%** | **96.7** | **91.0** | **38.4** | **92.4** |
| CRF 23 | 8.0 | 48% | 96.4 | 91.9 | 37.5 | |
| CRF 24 | 6.8 | 41% | 96.0 | 91.2 | 36.7 | 92.5 |
| CRF 20, maxrate 6M | 6.3 | 38% | 95.9 | 89.8 | 37.0 | 92.0 |
| CRF 24, maxrate 6M | 5.6 | 33% | 95.4 | 89.6 | 36.0 | |
| CRF 26 | 5.0 | 30% | 94.9 | 89.6 | 35.2 | 91.9 |
| CRF 28 | 3.7 | 22% | 93.4 | 87.7 | 33.8 | 91.2 |

- Frames, `kitchen-wide` frame 112 (dense dots across the frame, 23.9 Mbit/s at CRF 18): at 1:1
  the 8 Mbit/s cap cannot be told from CRF 18 or the lossless render; at 2× its densest dot
  fields are a little more uneven than CRF 18's, which are already uneven against lossless. The
  one-third settings are not clean: at 2× the dots clump under a 6 Mbit/s cap and at CRF 26,
  and at CRF 28 the densest field is a grey smear at 1:1.
- A third of the whole file would need the motion segments at 3.9 Mbit/s, half of what YouTube
  asks for. Even a 4 Mbit/s cap projects to 324 MB (36%).
- Why a cap and not a higher CRF: at the same size the cap scores the same or better on
  average (it leaves easy pictures at CRF 18 and takes the bits from the hard ones; the worst
  1% is a point lower), it has a reason behind its number, it does not touch pictures that
  were never the problem (flat looks, drifting cards, a drama's stills), and it bounds the
  size per minute whatever look comes next.
- Capped segments land at 8.4 to 9.1 Mbit/s in the sample, not 8.0: a short segment may spend
  its buffer.
- After a platform-style transcode the cap costs 1.0 VMAF against the CRF 18 master; the
  transcode itself costs 4.8.
- Removing `-tune film` saves 4% and sits on the same curve. P frames are 1.4 dB above B frames
  at CRF 18 and 0.55 dB under the cap, so the cap does not make the picture pulse.

### The real video

`assemble` in a copy of the work directory, new setting: `final.mp4` 534.9 MB (59.7% of 895.5),
40 MB a minute, 5.3 Mbit/s overall; `checks.json` ok with no problems, 24,061 frames, -14 LUFS.
85 of 107 segments were re-encoded (the 74 pictures and the 11 drifting cards; the 22 reveal
cards kept their cached segments) in 32 minutes on an 8-core laptop that was also running the
measurements. The 74 picture segments went from 804 MB at 15.3 Mbit/s to 444 MB at 8.4; the
largest is 10.0 Mbit/s (a 2.1-second shot spending its buffer), five are above 9, and the one
that was under the cap (`three-kilns`, 6.6) is within 0.2% of its old size, as are the drifting
cards (18.2 MB in all; not byte-identical, x264 plans its bits differently once a cap is set,
and PSNR on `three-kilns` is 45.5 dB either way). The file decodes end to end; ffmpeg prints one
duplicate-timestamp warning at frame 16466, and prints the same one for the 895 MB final.

### Not done, on purpose

- **The published DevDay final stays 895 MB.** A new `MOTION_ENCODER_VERSION` re-encodes every
  motion segment the next time a video is assembled, which changes `final.mp4` and voids its
  final approval. Do not re-assemble an approved cut to shrink it; the setting is for videos
  assembled from now on.
- Clip segments (a drama's generated clips, `CLIP_ENCODER_VERSION`) were not measured and are
  not capped. `docs/videos/BINGE.md` estimates 150–250 MB for a three-minute episode, 7 to 11
  Mbit/s; if dramas run long, measure them the same way.
- Other looks were not measured. The cap only acts on a segment that would exceed 8 Mbit/s.
- The measuring scripts are not in the repository; "How to verify" has the method.

### Found on the way

- Camera moves travel in steps: `2026-10-04-still-shot-camera-moves-travel-in`.
- `tasks claim` needed `--force`: the scope overlaps four active tickets. Three are work that is
  already on main (`2026-09-30-video-worker-moves-two-videos-at`, #999;
  `2026-10-03-illustrated-slides-round-2-a-family`, #1172; `2026-10-03-video-length-floor-only`,
  #1186) and were never marked done; the fourth
  (`2026-10-03-video-worker-narration-takes-made-stale`) shares only the two receipt files, which
  every change to a bound file has to edit. Whichever of the two merges second redoes its
  receipt increment on top of the other's.
