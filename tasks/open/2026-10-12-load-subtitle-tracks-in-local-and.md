---
id: 2026-10-12-load-subtitle-tracks-in-local-and
title: Load subtitle tracks in local and admin final video review players
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T03:40:48Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/pages.mjs
  - tools/video/review/cli.mjs
  - tools/video/review/pages.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
---

# Load subtitle tracks in local and admin final video review players

## Why

H03 has verified zh-TW SRT/VTT files, but its native local `review/final.html`
contains no `<track>`, and the official admin 720p preview reports `video.textTracks.length === 0`.
The preview plays successfully, yet owners cannot review actual subtitle appearance or toggle CC.
Do not treat caption-file validation as player rendering verification.

## Definition of done

- [ ] Current caption files are attached to the corresponding local and admin final-review players.
- [ ] Owners can enable/disable CC and read the selected language during playback.
- [ ] Subtitle tracks bind to the reviewed cut and branding offset; stale/missing files are explicit.
- [ ] Authenticated preview delivery serves VTT safely with the correct MIME type and access control.
- [ ] Unselected languages are not required or silently generated.

## Steps

- [ ] Trace the local page, review file upload roles and admin preview component.
- [ ] Add source-bound track delivery and focused tests, then inspect real browser rendering.

## How to verify

Run the affected review page/sync tests and admin component tests. Generate an approved
sample cut with a branding offset, load its VTT in both players, toggle CC, and inspect
the beginning/middle/end against cue text and timestamps. Check an unselected locale and a stale VTT.

## Notes

H03 final SHA e786669f5a392fde7f281c617c28f885d25df8b13535b4a37f9e2ae6eaea304e,
139 zh-TW cues, 5-second intro, 694.3-second branded duration. The admin preview was
observed playing at 28.77 seconds and paused at 67.22 seconds with readyState=4 and zero tracks.
This task records the shared product gap; H03's complete caption files remain intact.
