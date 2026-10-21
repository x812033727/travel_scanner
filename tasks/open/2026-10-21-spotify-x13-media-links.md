---
id: 2026-10-21-spotify-x13-media-links
title: Finish Spotify X13 formal media and links
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-21T01:01:06Z
completed_at:
branch:
depends_on:
  - 2026-10-20-brand-story-spotify-x13
scope:
  - docs/videos/story-everyday-spotify-x13/media-receipts
  - docs/videos/story-everyday-spotify-x13/publishing-handoff.md
  - docs/videos/story-everyday-spotify-x13/README.md
---

# Finish Spotify X13 formal media and links

## Why

The reviewed X13 preproduction packet has a frozen, source-audited script and two standalone Shorts, but this cloud environment does not hold the formal video worker's media workspace, approved channel intro/outro files or a video-tool token (`readCredentials()` reports no token). The paper runtime estimate does not prove the spoken body is at least eight minutes. Real media, uploads and link receipts must be completed and checked separately; no placeholder URL may be presented as published.

## Definition of done

- [ ] One approved main MP4 and two standalone 25–55-second portrait Short MP4s match the reviewed X13 story, use the official 5-second intro after the condensed opener and 21-second v4 outro after the three-line close, and carry optional Traditional Chinese CC rather than burned subtitles.
- [ ] Measured substantive main narration is at least 8:00; images, audio, captions, 9:16 crops, thumbnail and final 16-second clickable end-screen elements pass the repository's video QA and phone review.
- [ ] A real whole-episode expense ledger, including generation, retries, reviews, transcription and fees, is at or below US$25; the platform IDs and main/Shorts/playlist/condensed-content links in the handoff are filled only after actual uploads and verified on the live platform.

## Steps

- [ ] Obtain the formal worker workspace, a valid video-tool credential through safe configuration and the approved channel 5-second/21-second files; confirm source ingestion for S2/S3/S5/S7 beyond the 40k-character preview using targeted original passages or `reviewer_only`.
- [ ] Import the exact reviewed X13 v13 package and record the video/Shorts hashes before any paid generation. If the script, source matrix or visual plan changes, invalidate the old audit and repeat independent source and two-reader narrative gates.
- [ ] Generate TTS and measure body-only duration; run image and Short shot QA before full render, then render and inspect main/Shorts, CC, thumbnail, intro/outro and end screen within the single US$25 cap.
- [ ] Upload only reviewed assets with the site owner's approved channel workflow; verify real URLs and write media, timing, cost and upload receipts under `media-receipts/`, then update `publishing-handoff.md` and `README.md`.

## How to verify

Use `ffprobe` or the repository's media QA on each final MP4 and on the body-only audio, inspect selectable Traditional Chinese CC and phone crops, compare intro/outro timing to the approved media files, and sum the actual expense ledger. Verify each platform ID opens the intended uploaded main or Short, and test the main end-screen links during the last 16 seconds. See `docs/videos/story-everyday-spotify-x13/publishing-handoff.md` for the exact production handoff.

## Notes

The X13 v13 preproduction packet's source and merged two-reader narrative reviews passed at `video.json` SHA-256 `1e17d3e2b3fba5f7376986b952c4345224da68d771820799c75fc179a53ac2d9` and `shorts.json` `7fe87423bed274677ce10d4699b8fd343d6a4760afe50240eb069b2ab2674579`. Formal worker access and official media were unavailable in this cloud environment on 2026-10-21; no paid calls or uploads were made. The independent source audit records S2/S3/S5/S7 passages beyond the worker's ordinary 40k preview. Do not reuse old approval after a content edit; do not claim an MP4, actual spend, runtime or URL from the paper package.
