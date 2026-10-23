---
id: 2026-10-21-render-layout-check-misses-a-big
title: Render layout check misses a big card whose second text line is covered by its sub (icon + two lines + sub)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-22T00:40:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/render
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
---

# Render layout check misses a big card whose second text line is covered by its sub (icon + two lines + sub)

## Why

The owner watched the first paper-look tutorial (`claude-md-house-rules`, 2026-10-22) and saw text
cut off at 4:10. The card was a `big` scene with `icon: "checklist"`, a two-line `text`
(「寫得出「怎麼算做對」\n的才寫」) and a `sub`: with the key band's `--safe-bottom:274px` the icon
(150 px) plus two 150 px lines plus the sub no longer fit, and the second text line was drawn
under the sub line. `render` reported no layout problem for that state: its checks catch content
taller than the area and text that does not fit at 60 %, but not one element overlapping another
inside the content box. Three cards had the shape (`verifiable`, `draft-keep`, `answer`); the fix
in the video was to drop their icons.

## Definition of done

- [ ] `render` reports a layout problem when two elements of a `big` card (icon, word, sub,
      kicker) overlap, or when the `.word` block is taller than the room the icon and sub leave it.
- [ ] A `big` card with icon + two-line text + sub either fits (the icon shrinks or the word wraps
      smaller) or is refused before any frame is drawn.
- [ ] templates.test.mjs / render.test.mjs cover the case.

## Steps

- [ ] In `tools/video/render/browser.mjs` layout checks, compare bounding boxes of `.t-big .ic`,
      `.t-big .word`, `.t-big .sub` (and the numeral row) and report overlaps.
- [ ] Or in NUMERAL/ICON CSS give `.t-big .word` a max-height that accounts for the icon and the
      sub, and let `.fit` shrink it.

## How to verify

Render `tools/video/templates/fixtures/paper/video.json` with an added big card of that shape and
see the problem reported; render `claude-md-house-rules` and see none.

## Notes

Found on 2026-10-22 from the owner's first viewing; the render's "content is N px taller than its
area" check did fire for the eight numeral cards (icon + numeral + sub) earlier the same day, so
the gap is specifically overlap without overflow.
