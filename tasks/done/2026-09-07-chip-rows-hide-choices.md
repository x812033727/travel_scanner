---
id: 2026-09-07-chip-rows-hide-choices
title: Filter chip rows hide most of their choices behind a silent sideways scroll
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T01:48:32Z
created_at: 2026-09-07T01:47:02Z
completed_at: 2026-09-07T02:11:06Z
branch:
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/components/hotspot-theme-chips.tsx
  - apps/web/components/food-filter-chips.tsx
  - apps/web/components/account-saved-items.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/messages
---

# Filter chip rows hide most of their choices behind a silent sideways scroll

## Why

`.app-chip-row` scrolled sideways with `scrollbar-width: none` and no fade, so on a
390px phone the reader saw three chips and had no way to learn the rest existed.
Measured on production at 350px of usable width:

- `/zh-TW/hotspots` 主題 row: 7 chips, 697px of content — 賞雪, 燈飾 and 花火 unreachable
- `/zh-TW/hotspots` 購物 row: 8 chips, 997px — five of eight unreachable
- `/zh-TW/foods?destination_id=tokyo` 分類 row: 10 chips, 1151px

The same two pages announced their phone filter button as "熱門景點搜尋 0" and
"篩選 0", because the applied-filter count sits inside the button as text.

## Definition of done

- [x] Every chip in a row is reachable without a horizontal gesture.
- [x] A row too long to show in full says how many chips it folded away, and opens.
- [x] The reader's current selection is never the thing folded away.
- [x] The phone filter button reads as a sentence, count included.
- [x] `e2e/readability.spec.ts` fails if a chip row starts scrolling sideways again.

## Notes

`ChipRow` (`apps/web/components/chip-row.tsx`) is shared by the hotspot theme rows,
the food area/category rows and the saved-items tablist. It keeps the first six
chips and folds the rest, but only when the selection is inside those six — so
expanding is never needed to see what you already picked.
