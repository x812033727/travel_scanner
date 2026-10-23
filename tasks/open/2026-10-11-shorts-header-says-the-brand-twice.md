---
id: 2026-10-11-shorts-header-says-the-brand-twice
title: Shorts header says the brand twice beside the channel mark
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T16:49:20Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/layouts.mjs
  - tools/video/shorts/core.mjs
---

# Shorts header says the brand twice beside the channel mark

## Why

A card Short's header row now reads the theme's brand line on the left
(`MOKAAIR / AI 真的可以？`, `MOKAAIR / 長片精華`, `MOKAAIR`: tools/video/shorts/layouts.mjs) and the
channel mark on the right (`Mokaair` over `YouTube @Mokaair`, docs/videos/WATERMARK.md). The
channel is named twice in one row. The mark was added without touching the themes, so every
theme's contact sheet stayed as the owner approved it.

## Definition of done

- [ ] The owner has looked at a contact sheet with both and chosen: keep both, or drop the
      channel name from the brand line and keep only the series name there.
- [ ] If the line changes, `cut:illustrated` (whose brand is the bare `MOKAAIR`) has something
      to say on the left, or the row is laid out for one item.

## Steps

- [ ] Draw the six themes' first cards with the mark and show the owner.
- [ ] Change `THEMES[*].brand` and, if needed, the header's CSS in shorts/core.mjs.

## How to verify

`node tools/video/shorts/smoke.mjs` and its contact sheet.

## Notes

- `themeText()` feeds the font subset: a changed brand string changes the glyphs embedded.
