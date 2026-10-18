---
id: 2026-10-11-imported-cuts-carry-no-channel-mark
title: Imported cuts carry no channel mark
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T16:48:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/import
  - tools/video/shorts/import.mjs
  - docs/videos/WATERMARK.md
---

# Imported cuts carry no channel mark

## Why

New videos carry the channel mark in their top right corner (docs/videos/WATERMARK.md): the
owner asked for it on 2026-10-11 against copies re-uploaded to other platforms. The mark is laid
where a scene is drawn or encoded, so a cut the pipeline did not encode never gets one:

- `import` (tools/video/import) sends a long video finished by another tool to the final review
  as it is; only a 720p preview is encoded.
- `shorts import` (tools/video/shorts/import.mjs) copies the cut's bytes.

Several finished long videos reach the channel this way, so they are the largest group of new
uploads without a mark.

## Definition of done

- [ ] The owner has chosen one: the maker of an imported cut burns the mark in before importing
      (and import refuses or warns when it cannot tell), import offers one re-encode with the
      mark before the final review is sent, or imported cuts stay unmarked.
- [ ] Whatever is chosen is written in docs/videos/WATERMARK.md under 「不會有標記的東西」.

## Steps

- [ ] Ask the owner with the three options and what each costs (a re-encode changes the bytes,
      so it has to happen before the final gate, never after an approval).
- [ ] If import re-encodes: reuse `markStages` (tools/video/shorts/motion.mjs) and the PNG of
      core/watermark.mjs, at the cut's own bitrate, and record `watermark` in its checks.

## How to verify

Import a stand-in cut and read frame 0 at the box `tools/video/core/watermark.mjs` registers.

## Notes

- A cut imported after it was approved elsewhere must not be re-encoded here: the approval is of
  those bytes.
