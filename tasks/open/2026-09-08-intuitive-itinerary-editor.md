---
id: 2026-09-08-intuitive-itinerary-editor
title: Intuitive itinerary ordering and contextual place picker
status: review
priority: P1
area: web
owner: codex
claimed_at: 2026-09-08T06:03:51Z
created_at: 2026-09-08T05:27:53Z
completed_at:
branch: codex/intuitive-itinerary-editor
depends_on: []
scope:
  - apps/api/app/trips/schedule.py
  - apps/api/app/trips/router.py
  - apps/api/app/trips/itinerary.py
  - apps/api/app/trips/place_options.py
  - apps/api/tests/test_itinerary_ordering.py
  - apps/api/tests/test_trip_place_options.py
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/itinerary-place-browser.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
  - apps/web/components/itinerary-timeline.tsx
  - apps/web/components/editable-itinerary-timeline.tsx
  - apps/web/lib/itinerary-order.ts
  - apps/web/lib/itinerary-order.test.ts
  - apps/web/app/globals.css
  - apps/web/lib/itinerary-copy.ts
  - apps/web/e2e/itinerary-editor.spec.ts
  - apps/web/e2e/fixtures/itinerary-editor.ts
  - apps/web/e2e/navigation.spec.ts
  - apps/web/e2e/full-stack.spec.ts
---

# Intuitive itinerary ordering and contextual place picker

## Why

The signed-in mobile planner only offers a blank form for a new stop. Its sort
control is disabled for a single ordinary stop, system-card gaps have no insert
entry, and backend time sorting can undo manual positions after saving.

## Definition of done

- [x] A single stop can move across meals or days; save/reload preserves positions.
- [x] Every valid city-route gap opens saved/nearby discovery with repeated add and undo.
- [x] System anchors, fixed times, offline drafts, conflicts and route/manual policies survive.
- [x] Desktop and Pixel 7 browser validation and focused API/Web regression tests pass.

## Steps

- [x] Inspect the signed-in Seoul and Tokyo journeys using the in-app browser.
- [x] Implement position-based ordering and site-catalog discovery without paid browsing calls.
- [x] Validate editor, picker, pointer/keyboard interaction and API persistence.

## How to verify

Run Ruff, mypy, pytest, ESLint, i18n, TypeScript, Vitest, build and Playwright.
In the editor, insert before lunch, add a saved place and a nearby place, undo,
drag across dinner, move to day 2, reload, and confirm the same positions.

## Notes

Isolated worktree from origin/main 9ca88c2; the original dirty checkout is untouched.
The active merchant-style task owns apps/web/messages, so feature-local typed
copy provides all five languages without colliding with that translation batch.
Existing read-only ItineraryTimeline remains unchanged. No production trip was edited.
Docker is unavailable locally; PostgreSQL integration and container checks run in CI.

Local checks: Ruff and mypy (258 modules) pass; pytest excluding the Windows-
unsupported Unix deployment-center module passes (1717 passed, 110 skipped).
Desktop/Pixel 7 Playwright covers repeated add, undo, pointer drag, keyboard focus,
cross-day move, reload and the existing mobile autosave/optimization workflow.
The unmocked full-stack scenario and the PostgreSQL catalogue-ownership/save test
are included in existing CI suites. Nearby browsing calls no map providers.
Saved choices include reviewed hotspots/merchants, merchants for saved dishes,
and saved restaurants only when their identity matches a published merchant.
Unreviewed or transient-only locations are not silently presented as route-ready.
In-app browser visual QA uses a localhost fixture, not production mutation.
Its dark-mode contrast, persistent footer Undo, and post-Undo focus were refined.
