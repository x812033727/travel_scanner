---
id: 2026-09-08-planner-weather-dark-contrast
title: Fix weather and itinerary intent panel contrast in dark mode
status: review
priority: P2
area: web
owner: codex
claimed_at: 2026-09-08T08:42:18Z
created_at: 2026-09-08T07:36:05Z
completed_at:
branch: codex/planner-nearby-followup
depends_on: []
scope:
  - apps/web/components/trip-weather-panel.tsx
  - apps/web/components/trip-weather-panel.test.tsx
  - apps/web/components/itinerary-diff.tsx
  - apps/web/components/itinerary-diff.test.tsx
---

# Fix weather and itinerary intent panel contrast in dark mode

## Why

The already-merged readability E2E scope was handed to the admin domain regression task on 2026-09-08; planner-specific tests remain here.

The itinerary weather card retains a fixed pale gradient in dark mode, while its heading and warning text inherit light theme tokens. The user also reported the white surface of the "What would you like to change?" intent panel. Its responsive/translucent white utilities are not covered by legacy dark-mode compatibility styles. Both panels need theme-aware surfaces, nested fields and legible accents without changing planning or provider behaviour.

## Definition of done

- [x] Weather titles, forecast values, warnings and attribution are readable in light, dark and system themes, meeting the applicable WCAG AA contrast thresholds.
- [x] Desktop and Pixel 7 layouts retain the existing forecast/source/range behaviour and 44px controls.
- [x] Theme regression tests and browser visual evidence cover out-of-range and available-forecast states.
- [x] The intent panel remains readable collapsed/expanded on mobile and desktop, with input, scope selection, examples and preview behaviour preserved.

## Steps

- [x] Replace the hard-coded light-only weather surface with a theme-aware treatment.
- [x] Add regression coverage and validate actual computed colours in both themes.
- [x] Replace light-only intent surfaces and test both panels in the same editor.

## How to verify

Run the weather panel Vitest tests, ESLint, TypeScript and relevant readability Playwright checks. In the in-app browser inspect a signed-in trip with dark mode and the trip date beyond forecast range, then repeat with fixture-backed available weather at 412x915 and desktop sizes. Do not change the user's real itinerary or trigger a paid weather provider solely for testing.

## Notes

- Production release 4343454: `trip-weather-panel.tsx:152` uses `linear-gradient(135deg,#f8fcff,#eef8f8)` in all themes. Computed dark-mode heading colour is rgb(237,245,242); muted text rgb(169,187,183); warning text rgb(253,230,138).
- The user subsequently requested both this weather fix and the intent panel fix. They are included in PR #366 alongside its existing nearby-discovery fixes; not yet merged or deployed.
- Both panels and nested fields now use opaque semantic surface/paper tokens. Scope and example controls are at least 44px; the icon-only mobile preview submit button now has its translated accessible name. Provider, preview/apply and usage behaviour are unchanged.
- Focused weather/intent Vitest: 26 passed. Whole-web ESLint, TypeScript, five-locale i18n checks and production build passed. Independent read-only review found no actionable regressions.
- New Playwright cases: 8 passed on desktop Chromium and Pixel 7, repeated with screenshots. They measure real painted text contrast (at least 4.5:1), reject unmeasured gradients, check dark surfaces, placeholder/hover/focus, 44px controls, no horizontal overflow, range handling, loading/error/retry and light/system overrides. All trip mutations are intercepted and asserted absent.
- Visual evidence: the signed-in production page confirmed the out-of-range weather and desktop intent failures without changing real trip data. Local in-app preview navigation was blocked (`ERR_BLOCKED_BY_CLIENT`), so repaired dark/light weather and expanded intent were visually inspected from the production-build Playwright screenshots instead. The production browser viewport was restored and the empty preview tab closed.
