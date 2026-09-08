---
id: 2026-09-08-planner-weather-dark-contrast
title: Fix itinerary weather card contrast in dark mode
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-08T07:36:05Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-weather-panel.tsx
  - apps/web/components/trip-weather-panel.test.tsx
  - apps/web/app/globals.css
---

# Fix itinerary weather card contrast in dark mode

## Why

The itinerary weather card retains a fixed pale gradient in dark mode, while its heading and warning text inherit light theme tokens. Signed-in production inspection on 2026-09-08 confirmed near-white heading text against the pale card, making the trip weather hard to read. This predates the #362 planner editor release.

## Definition of done

- [ ] Weather titles, forecast values, warnings and attribution are readable in light, dark and system themes, meeting the applicable WCAG AA contrast thresholds.
- [ ] Desktop and Pixel 7 layouts retain the existing forecast/source/range behaviour and 44px controls.
- [ ] Theme regression tests and browser visual evidence cover out-of-range and available-forecast states.

## Steps

- [ ] Replace the hard-coded light-only weather surface with a theme-aware treatment.
- [ ] Add regression coverage and validate actual computed colours in both themes.

## How to verify

Run the weather panel Vitest tests, ESLint, TypeScript and relevant readability Playwright checks. In the in-app browser inspect a signed-in trip with dark mode and the trip date beyond forecast range, then repeat with fixture-backed available weather at 412x915 and desktop sizes. Do not change the user's real itinerary or trigger a paid weather provider solely for testing.

## Notes

- Production release 4343454: `trip-weather-panel.tsx:152` uses `linear-gradient(135deg,#f8fcff,#eef8f8)` in all themes. Computed dark-mode heading colour is rgb(237,245,242); muted text rgb(169,187,183); warning text rgb(253,230,138).
- Observed during #362 post-deployment QA; intentionally not folded into the coordinate/pagination fixes in #366. No weather UI code has been changed for this task.
