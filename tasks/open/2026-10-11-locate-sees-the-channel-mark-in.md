---
id: 2026-10-11-locate-sees-the-channel-mark-in
title: Locate sees the channel mark in frames pulled from a marked cut
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T16:48:14Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/from-drama.mjs
  - tools/video/shorts/from-drama.test.mjs
---

# Locate sees the channel mark in frames pulled from a marked cut

## Why

`shorts from-drama` asks the site's `locate` where the subject of each shot is. When the work
directory has no keyframe for a shot it pulls a frame out of the episode's cut
(`locateShots` in tools/video/shorts/from-drama.mjs) and uploads that. A cut made with the
channel mark (docs/videos/WATERMARK.md) carries it in every frame, so locate can answer with a
box around the letters. With no named character found, `pickSubject` takes the surest box,
which may be the mark: the window then heads for the top right corner, where the range that
keeps windows off the mark (`windowRange`) stops it, or the build refuses the shot.

Keyframes are clean, so this only happens to shots without one.

## Definition of done

- [ ] A frame pulled from a marked cut reaches locate with the mark's box painted out, or boxes
      inside the mark's box are dropped before a subject is picked.
- [ ] A test with the fake site shows the window staying on the real subject.

## Steps

- [ ] The episode's `checks.json` `watermark.box` is already read by `readEpisode`; use it in
      `locateShots` (drawbox on the pulled frame, as `psnrArgs` masks it in assemble/plan.mjs).
- [ ] Extend the end-to-end test in from-drama.test.mjs.

## How to verify

`node --test tools/video/shorts/from-drama.test.mjs`

## Notes

- Not seen in practice yet: no marked episode had been cut into a Short when this was filed.
