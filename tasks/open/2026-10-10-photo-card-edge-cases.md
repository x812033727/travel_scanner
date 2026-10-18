---
id: 2026-10-10-photo-card-edge-cases
title: Photo card: three edge cases render lets through or refuses without saying why
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-10T15:13:44Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/render.test.mjs
  - tools/video/core/lint.mjs
---

# Photo card: three edge cases render lets through or refuses without saying why

## Why

Measured on 2026-10-10 by the pre-deploy review of #1425 (headless Chromium against that
commit's `templates.mjs` and `theme.css`, the same check `render/browser.mjs` makes). All three
affect locally made videos only; the host cannot draw a photo card.

1. **A photo card with no caption and a wide photograph can fail render on its default tilt.**
   `PHOTO_CSS` leaves 26px for the rotated corners; with no `tilt` the angle comes from the
   scene id's hash (plus or minus 1.5, 2 or 2.5 degrees). A 16:9 photograph overflows by 2px at
   2.5 degrees and 8px at 3; one wider than about 2.2:1 overflows from 2 degrees. Render ends
   with "the slide's content is 2px taller than its area", which does not mention the tilt, and
   lint says nothing beforehand. With a caption, or with 4:3 and portrait photographs, every
   angle passes. A panorama wider than about 2.2:1 is also cropped at both sides by
   `object-fit: cover` without a word.
2. **A long credit on a narrow portrait photograph runs off the left edge and render does not
   notice.** The credit pill is anchored at the print's bottom right with `nowrap` and may be
   1,400px wide; lint allows 60 characters. Sixty full-width characters are 1,353px: on a 2:3
   portrait the pill starts at x = -201, on a 1:3 strip at -309. `browser.mjs` compares
   `scrollWidth`, and overflow to the left is not scrollable, so it reports nothing.
3. **An `assets[]` entry with no `url` and no `author` satisfies render but prints no credit.**
   `plan.mjs` only matches the entry's `path` (its message says "without it the description
   carries no credit"); the schema requires `path`, `source`, `license`; `creditedAssets` in
   `core/metadata.mjs` lists only entries with an author or a url. A hand-registered CC BY
   photograph with the three required fields and no on-screen credit ships with no attribution
   at all.

## Definition of done

- [ ] 1: the default tilt of a caption-less photo card never fails the layout check (more room,
      or a smaller default angle for wide photographs), or lint warns before render; the
      message names the tilt.
- [ ] 2: a credit that would start left of the frame is refused or wrapped.
- [ ] 3: a photo scene whose asset's licence requires attribution and has neither `author` nor
      `url` nor an on-screen `credit` is a lint error.
- [ ] Tests for each; the fixtures' existing pages stay byte-identical.

## Steps

- [ ] Reproduce each with the reviewer's numbers before changing anything.
- [ ] `templates.mjs` and `plan.mjs` may be bound by the duration receipt: run
      `node tools/video/long-form/cli.mjs check` after the change.

## How to verify

`node --test tools/video/templates/templates.test.mjs tools/video/render/render.test.mjs`.

## Notes

- 2026-10-10 filed from the pre-deploy review of #1425; ticket `2026-10-10-photo-paste-card`
  shipped the card. Workarounds until then: write a caption or `"tilt": 2` or less; keep
  credits to a usual length; register `url` or `author` for every photograph.
