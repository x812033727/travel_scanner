---
id: 2026-09-29-revise-image-trust-long-video-opening
title: Revise image-trust long-video opening and packaging
status: done
priority: P2
area: docs
owner: codex-image-trust-opening
claimed_at: 2026-09-29T01:43:18Z
created_at: 2026-09-29T01:42:40Z
completed_at: 2026-09-29T02:06:01Z
branch: codex/image-trust-opening
depends_on: []
scope:
  - docs/videos/image-trust-opening-v2
---

# Revise image-trust long-video opening and packaging

## Why

The image-trust thumbnail asks viewers to pick a picture, then the opening says
the video is not a real/fake identification test. The owner approved revising
this long video's packaging and opening while another conversation handles
Shorts. Produce an isolated review cut without touching shared episode inputs.

## Definition of done

- [x] A long-only source aligns the title, thumbnail and opening demonstration.
- [x] A new thumbnail is visually reviewed and exported at 1280x720 under 2 MB.
- [x] New zh-TW narration, chapter times and subtitles match the revised full video.
- [x] The first chapter completes within 30 seconds; three captions change over
      the same clearly fictional illustration in sync with their narration.
- [x] Technical validation and visual review evidence are recorded, with human
      listening and production review explicitly left pending.

## Steps

- [x] Check ownership: the other conversation claims season-one for Shorts;
      use a new isolated directory and output path with a long-only source.
- [x] Independently refresh NIST, C2PA and YouTube source support.
- [x] Build and inspect the revised long cut and 30-second preview.
- [x] Save the review package in an isolated branch for a draft PR; do not publish
      or replace the current production review during this editing pass.

## How to verify

Run this directory's build.py with an output path outside Git, then check the
technical report, full decode, audio measurement, first-chapter timing, captions,
new thumbnail and contact sheet. Validate tasks and the diff before pushing.

## Notes

The source material came from the merged season-one package (PR #880). No active
PR was editing this new directory at claim time. PR #964 is a separate queue
recovery fix and is not part of this content revision. The current branch uses
the pre-existing origin/main baseline 4d406942.

The shared source paths and original media remain read-only. Outputs go to
`C:/Users/x8120/mokaair-work/long-revisions/image-trust-20260929`. Publication,
production review replacement, listening acceptance and performance lift are
not claimed by local technical checks.

This iteration produces the zh-TW review cut. Any selected additional languages
must be regenerated from the new source/timing before a later production release.

Completed media checks: 1920x1080 at 24 fps, 467.554 seconds, first chapter
23.158 seconds; 91 speech units with 75 original WAVs reused and 16 newly
synthesized. Final AAC measures -14.30 LUFS and -0.96 dBTP against -14/-1
targets (about 0.04 dB encoded peak overshoot). Full video/audio decode passed,
opening illustration is unchanged across the three claims, timestamps derive
from real WAV lengths, and original helper hashes remain unchanged. The updated
thumbnail and contact sheet were visually inspected. Human listening/final-edit
acceptance remain pending, as do production replacement and any extra languages.
