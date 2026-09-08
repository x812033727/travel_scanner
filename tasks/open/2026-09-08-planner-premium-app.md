---
id: 2026-09-08-planner-premium-app
title: Premium app-style itinerary planning flow
status: in-progress
priority: P1
area: web
owner: codex-planner-premium
claimed_at: 2026-09-08T23:07:26Z
created_at: 2026-09-08T21:19:04Z
completed_at:
branch: codex/planner-premium-app
depends_on: []
scope:
  - .github/workflows/planner-premium.yml
  - apps/web/e2e/full-stack.spec.ts
  - apps/web/e2e/trip-stay-areas.spec.ts
  - apps/web/e2e/stay22-maps.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/components/itinerary-diff.tsx
  - apps/web/components/itinerary-diff.test.tsx
  - apps/web/components/itinerary-place-browser.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
  - apps/web/e2e/navigation.spec.ts
  - apps/api/app/trips/search_criteria.py
  - apps/api/app/trips/stay_areas.py
  - apps/api/app/trips/stay_router.py
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
  - apps/web/components/planner
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/app/globals.css
  - apps/web/lib/planner-copy.ts
  - apps/web/lib/planner-copy.test.ts
  - apps/api/app/trips/router.py
  - apps/api/tests/test_trip_preferences.py
  - apps/web/e2e/planner-premium.spec.ts
  - docs/planner-premium-app.md
---

# Premium app-style itinerary planning flow

## Why

The itinerary was below a tall hero, AI status, service shortcuts and weather. New trips required a wizard; mobile controls and contextual panels competed with the actual timeline. Travelers need a calm, itinerary-first workspace with manual and AI planning equally accessible.

## Definition of done

- [x] City and dates create a manual blank trip in one page without paid provider requests.
- [x] Timeline and day navigation precede supporting services; tools mount on demand.
- [x] Add, move, edit, undo, AI preview/apply and route selection retain existing data contracts.
- [x] Traveler/preference patches preserve omitted fields and invalidate only affected quotes.
- [ ] Desktop/mobile browser regressions, full tests and CI are verified; PR is ready for review.

## Steps

- [x] Claim an isolated branch from current origin/main and preserve the shared checkout.
- [x] Implement single-page creation, premium timeline and contextual sheets.
- [x] Add safe preference updates, pending-operation guards and regression tests.
- [ ] Finish visual checks and all automated validation, then create PR. Do not merge or deploy without new authorization.

## How to verify

Run API pytest/ruff/mypy; npm run lint:web, typecheck:web, check:i18n, check:tasks; Web Vitest with --pool=threads --maxWorkers=1; production build; Playwright navigation.spec.ts and planner-premium.spec.ts with one worker. CI adds Linux/PostgreSQL/Redis, container and full-stack smoke coverage.

Browser scenarios use isolated fixture trips, not production accounts or paid provider data. Verify 390px timeline visibility, continuous additions, More actions, cross-day movement, Tools categories, explicit AI preview/apply and single-page creation.

## Notes

Base: b675f5d34a353eddfb789a953968c3c6d45eac4a. Worktree: C:/Users/x8120/.codex/worktrees/mokaair-planner-premium.

Feature-local five-language copy avoids overlapping the active merchant-style task's messages scope. Existing completed #366 and #368 task records were archived only after remote merge/release evidence was checked.

First browser run exposed an oversized configured hotel card; lodging details now expand on demand. Pending metadata/intent requests prevent panel switching and stale-response overwrites. API full Windows run excludes test_deployment_center.py because socketserver.UnixStreamServer is Linux-only; CI must cover it.
