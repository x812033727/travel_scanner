---
id: 2026-11-10-planner-premium-today-timebomb
title: planner-premium e2e fails while its fixture trip is today in Tokyo
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-11-10T15:30:32Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/planner-premium.spec.ts
  - apps/web/e2e/fixtures/itinerary-editor.ts
---

# planner-premium e2e fails while its fixture trip is today in Tokyo

## Why

`apps/web/e2e/planner-premium.spec.ts:43` expects a day chip named `DAY 1`. The fixture trip
(`e2e/fixtures/itinerary-editor.ts`) runs 2026-11-11 to 2026-11-12 in `Asia/Tokyo`, and
`components/trip-editor.tsx` labels the chip of the local current day `te("today")` instead of
`DAY n`. From 2026-11-10T15:00Z (midnight in Tokyo) to 2026-11-12T15:00Z the chip reads "today",
the locator finds nothing, and the test fails on desktop and mobile in both `planner-browser`
(Planner UX) and `web-e2e (3/3)` — on every branch, whatever it changes. Seen on PR #2050
(docs-only) at 2026-11-10T15:27Z; the same code passed at 14:05Z.

## Definition of done

- [ ] The spec passes regardless of the real date: freeze the page clock before navigation
      (`await page.clock.setFixedTime(new Date("2026-11-01T03:00:00Z"))`, as
      `admin-video-shorts.spec.ts:39` does), or move the fixture dates out of reach.
- [ ] Any other spec that uses `editorFixture` checked for the same dependency.

## Steps

- [ ] Add the fixed clock to `planner-premium.spec.ts` (and others using the fixture if needed).
- [ ] Run `npm run test:e2e -- planner-premium` with the system date inside the trip window.

## How to verify

Run the spec with the browser clock set to 2026-11-11T09:00+09:00; it must still find `DAY 1`.

## Notes

Self-heals after 2026-11-12T15:00Z, but the same fixture will bite again whenever someone moves its dates near "now".
