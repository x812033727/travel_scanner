---
id: 2026-10-20-finish-s39-stills-and-illustrated-film
title: Finish S39 stills and illustrated film
status: in-progress
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T01:39:14Z
created_at: 2026-10-20T01:39:09Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/video.json
  - docs/videos/curio-s39/verify-11.md
---

# Finish S39 stills and illustrated film

## Why

S39 narration, music, script, and source checks are ready, but its 86 stills
have not been generated. S04 and S23 share the MiniMax 240-submission hourly
quota, so S39 must wait for an assigned slot. Once available, finish the
illustrated film without exceeding its US$3.56 image-and-music ceiling.

## Definition of done

- [ ] Coordinate a safe MiniMax start window and produce 86 stills under the
  remaining US$3.48 image ceiling, retrying only flagged images.
- [ ] Visually audit every still for correct historical attribution, distinct
  Bruti, empty paper surfaces, readable cards, and series look; obtain a
  hash-bound storyboard approval under standing delegated instructions.
- [ ] Render, create motion clips, assemble and caption the episode; run the
  required audio, visual, source, link and package QA gates.
- [ ] Create a reviewable upload package and log exact media/QA hashes, costs,
  delegated gates and any remaining site-owner actions in `verify-11.md`.

## Steps

- [x] Independent R4a script, source and prompt preflight pass; 89/89 audio
  check has 0 flags, body is 8:25, and music is ready.
- [ ] Wait for `ten_topics` to confirm safe shared MiniMax capacity.
- [ ] Generate and inspect stills; fix any rejected prompts within scope.
- [ ] Complete storyboard, render, clips, assemble, captions, QA and package.

## How to verify

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s39 --dry-run`

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs status --slug curio-s39`

Use `docs/videos/curio-s39/verify-10.md` for exact script, audio, music,
budget and independent audit hashes before resuming.

## Notes

At 01:35 UTC, MiniMax window usage was 33/240, conservative stop at 200.
S04 had roughly 45 first-pass stills left, S23 roughly 14, plus unknown
repairs. `ten_topics` asked S39 to hold until their first passes finish or
the 02:23:28 UTC reset. S39 has made **zero** MiniMax requests; generated
music cost US$0.08 and will be looped by assembler because the returned MP3
is 176.09 seconds although the request/manifest says 569 seconds. Review
the loop seams in the final mix. The site audio card is pending; a local
approval on the exact timeline was recorded under the owner's delegated
instruction, clearly noting that the owner did not personally listen.

Budget precision (2026-10-20): 86 × 3 × US$0.0135 + US$0.08 music = US$3.563, slightly above the existing **US$3.56** hard stop because the site's US$3.48 image quote is rounded. Keep that stop: charge at most **257 of 258** possible image attempts and check the ledger before retries. Current ledger is US$0.08 music and US$0.00 images; see `docs/videos/curio-s39/verify-10.md`. No approval-bound file changes.
