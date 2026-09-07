---
id: 2026-09-07-applied-filter-chip-is-all-delete
title: The whole applied-filter chip is a delete button
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T08:50:39Z
created_at: 2026-09-07T02:06:16Z
completed_at: 2026-09-07T08:53:56Z
branch:
depends_on: []
scope:
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/food-browser.tsx
---

# The whole applied-filter chip is a delete button

## Why

Both browsers show the filters in use as pills with an × on the end. The whole pill is
the button, which is the right target size but reads as a label with a close control, so
tapping the words removes a filter the reader did not mean to touch. Nothing on either
page said what the row was or what tapping it does — `已選條件` existed only as an
`aria-label` on `/hotspots`, invisible to everyone who can see the screen.

`/foods` had two more problems in the same row: the chips were `min-h-9` (36px, under the
44px this site holds everywhere else) and their accessible name came out as
`清除條件: 東京` — the clear-everything label reused for one chip.

## Definition of done

- [x] The row says what the chips are and that tapping one removes it.
- [x] Every chip and the clear-all button is at least 44px tall on both pages.
- [x] A chip announces as "移除 澀谷", not as the clear-everything label.

## How to verify

`npx vitest run components/food-browser.test.tsx` — the new case reads the row label,
finds the chip by its own name and expects the filter to be gone after one click.

## Notes

The finding suggested shrinking the target to the ×. That is the wrong direction for this
audience: a 44px pill is easier to hit than a 15px icon, and the fix for a surprise is to
stop it being a surprise. The row now reads 已選條件（點一下取消）.

`/foods` also gains the `removeFilter` key `/hotspots` already had, and its chips take the
same teal outline, so the two pages stop looking like different products.
