---
id: 2026-10-20-build-and-review-curio-s28-vertical
title: Build and review Curio S28 vertical Short
status: in-progress
priority: P2
area: docs
owner: codex-s07-shorts
claimed_at: 2026-10-20T05:42:06Z
created_at: 2026-10-20T05:42:03Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on:
  - 2026-10-20-curio-s28-one-sourced-short-script
scope:
  - docs/videos/curio-s28/shorts.json
  - docs/videos/curio-s28/short-verify-2.md
---

# Build and review Curio S28 vertical Short

## Why

S28 has an approved long film and a source-checked one-Short script, but its
vertical film has not been built. Reuse the long film's approved pictures,
synthesize the channel voice after S34 releases its voice/ASR window, and
separate a locally complete cut from any site/YouTube gate still pending.

## Definition of done

- [ ] The one-Short cut has measured 1080×1920/30 fps and 25–55 seconds,
      correct spoken text, safe captions, a source check bound to exact script
      hash, and visible opening/loop frames.
- [ ] Local QA/package results and any site or full-film URL blockers are
      recorded without claiming a private/public upload that has not happened.

## Steps

- [ ] Wait for S34 producer to release the voice/ASR call window.
- [ ] Run `from-episode` server build against S28's existing keyframes, then
      `check-audio`; repair only flagged phrases if needed.
- [ ] Bind an independent factual `verify.json` to the resolved script, run
      QA, inspect source/ending frames, and package or record exact blockers.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --check`;
`node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --workdir /workspace/.video-work --speech server`;
`node tools/video/shorts/cli.mjs check-audio --dir <build>`;
`node tools/video/shorts/cli.mjs qa --dir <build> --verify <verify.json>`;
`node tools/video/shorts/cli.mjs package --dir <build>`.

## Notes

Preflight `short-verify-1.md` and script commit `d60b3c03` pass one-Short
validation, sourced claims, and five unique keyframe hashes. The long film
has no YouTube video ID at this point, so a package may rightly fail the
full-film-link item; keep that explicit until a real ID is linked.
