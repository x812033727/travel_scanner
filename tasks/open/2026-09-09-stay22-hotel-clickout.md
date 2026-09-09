---
id: 2026-09-09-stay22-hotel-clickout
title: Stay22 exact hotel affiliate clickouts
status: review
priority: P1
area: api
owner: codex-stay22
claimed_at: 2026-09-09T11:09:58Z
created_at: 2026-09-09T11:08:28Z
completed_at:
branch: codex/stay22-hotel-clickout
depends_on: []
scope:
  - .github/workflows/ci.yml
  - apps/api/app/travel_services/stay22.py
  - apps/api/app/travel_services/hotel_options.py
  - apps/api/app/travel_services/hotel_admin.py
  - apps/api/app/travel_services/admin.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/travel_services/router.py
  - apps/api/app/travel_services/service.py
  - apps/api/app/travel_services/errors.py
  - apps/api/app/trips/stay_router.py
  - apps/api/tests/test_stay22_clickout.py
  - apps/api/tests/test_stay22_admin.py
  - apps/api/tests/test_stay22_context.py
  - apps/api/tests/test_stay22_routes.py
  - apps/api/tests/test_hotel_options.py
  - apps/web/components/travel-services/booking-panel.tsx
  - apps/web/components/travel-services/booking-panel.test.tsx
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/stay22-admin.tsx
  - apps/web/components/travel-services/stay22-admin.test.tsx
  - apps/web/components/stay-area-flow.tsx
  - apps/web/components/stay-area-flow.test.tsx
  - apps/web/components/stay22-map-panel.tsx
  - apps/web/components/stay22-map-panel.test.tsx
  - apps/web/lib/stay22-booking-context.tsx
  - apps/web/lib/stay22-allez-copy.ts
  - apps/web/lib/stay22-allez-copy.test.ts
  - apps/web/lib/stay22-allez-messages
  - apps/web/lib/hotel-clickout-error.ts
  - apps/web/lib/hotel-clickout-error.test.ts
  - apps/web/app/api/travel/[...path]/hotel-clickout.test.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/e2e/stay22-allez.spec.ts
  - apps/web/e2e/travel-services.spec.ts
  - apps/web/e2e/stay22-maps.spec.ts
  - docs/stay22-allez.md
---

# Stay22 exact hotel affiliate clickouts

## Why

Known, reviewed hotel pages should offer direct OTA booking links without requiring a Stay22 map. Existing affiliate contracts remain first priority; Allez fills eligible gaps only.

## Definition of done

- [x] Server-built Allez links with exact reviewed identities, strict context and privacy gates.
- [x] Versioned default-off admin controls and readiness counts, without a migration.
- [x] Five-language hotel booking panel and catalog-first stay flow, safe failure UX.
- [ ] Backend, frontend and fixture browser validation; PR opened without merging or enabling live tracking.

## Steps

- [x] Implement and review independent API, admin and frontend changes.
- [ ] Run checks, document release boundary and open PR.

## How to verify

Ruff, mypy, pytest; ESLint, TypeScript, i18n, Vitest, build; desktop/Pixel fixture Playwright. No real affiliate test clicks or bookings.

## Notes

Base origin/main 95122362. Canonical checkout is dirty and untouched. README.md remains claimed by the merchant task; all feature documentation goes in docs/stay22-allez.md. Existing catalog.tsx is also claimed, so booking context uses a narrow shared context provider around the existing stay catalog slot instead of editing that file.

Implementation checkpoint: exact-hotel/channel/context tests and first-party HTTP persistence tests pass; admin capability/config tests and five-locale UI checks added. Full checks and desktop/Pixel fixture validation are still in progress. Allez remains default-off; no real affiliate click, order, commission claim, merge or deployment performed.
