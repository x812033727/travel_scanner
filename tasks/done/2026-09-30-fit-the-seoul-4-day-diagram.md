---
id: 2026-09-30-fit-the-seoul-4-day-diagram
title: Fit the Seoul 4-day diagram's Hongdae and Myeongdong labels inside their boxes
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T09:40:18Z
created_at: 2026-09-30T01:29:08Z
completed_at: 2026-09-30T09:45:17Z
branch: claude/seoul-diagram-fit
depends_on:
  - 2026-09-21-91-ci
scope:
  - apps/web/public/guides/seoul-4-day-itinerary/diagram-1.svg
---

# Fit the Seoul 4-day diagram's Hongdae and Myeongdong labels inside their boxes

## Why

In `seoul-4-day-itinerary/diagram-1.svg` two 16 px lines already ran past their
boxes before `2026-09-21-91-ci` raised the 14 px labels: "홍대・연남동 (Hongdae)・方案 A"
in the Day 4 Hongdae box and "명동・남산 (Myeongdong / Namsan)" plus the N Seoul
Tower line in the Day 1 box. That ticket fitted only the labels it enlarged.

## Definition of done

- [x] Every label sits inside its box at 15 px or more, without shrinking below 15 px.
- [x] Rendered PNG checked for overlap; lint 0 errors.

## How to verify

Render with `render_svg` (see the content-pipeline skill) and look at the Day 1
and Day 4 boxes.

## Notes

- 2026-09-30 (claude-opus-5-5): widened three boxes, centred as before, no
  font size changed: Day 4 Hongdae 230 → 300 px, Day 1 Myeongdong 250 → 380 px
  (its Day badge moved with the corner; the N Seoul Tower icon now sits on the
  box), and the dashed Gangnam box 240 → 290 px, whose small line also ran past
  its border. Rendered and checked: every label is inside its box. Lint 0 errors.
  SVG-only, so it ships with the next deploy; no import needed.
