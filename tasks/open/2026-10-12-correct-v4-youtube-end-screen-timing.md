---
id: 2026-10-12-correct-v4-youtube-end-screen-timing
title: Correct v4 YouTube end-screen timing after the CTA transition
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-12T13:32:50Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/branding-release/2026-10-12-endscreen-outro.md
---

# Correct v4 YouTube end-screen timing after the CTA transition

## Why

The approved 21-second v4 outro fades the CTA icons out and the end-screen slot
outlines in between 4 and 5 seconds. Existing shared release guidance recommends
the last 17 seconds, which places clickable YouTube elements over that transition.
Direct frame inspection confirms that the slot canvas is clear at outro +5 seconds,
so the safe Studio start is full video duration minus 16 seconds.

## Definition of done

- [ ] Shared v4 release instructions use the verified last-16-second Studio anchor.
- [ ] References distinguish the 21-second outro asset from the 16-second interval
      for clickable elements, without changing the owner-approved media.

## Steps

- [ ] Coordinate with the active channel-branding owner and update shared guidance.
- [ ] Locate other documented v4 minus-17 recommendations and correct matching ones.

## How to verify

Inspect v4 frames 120/121 (full CTA), 135 (faint CTA), 150/165 (clear slot canvas)
at 30 fps. Preserve the asset SHA below. The five Curio remasters already use a
separate metadata-only correction with media-before/after hashes; this ticket is
for the shared instructions outside that task's scope.

## Notes

- Approved v4 SHA: 00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396.
- Evidence: C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/outro-timing-probe/.
- Implementation reference: tools/video/branding/outro.mjs, FADE_FRAMES = 15.
- Remaster correction: docs/videos/curio-five-recuts-20261012/endscreen-timing.mjs.
