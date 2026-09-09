---
id: 2026-09-09-stay22-hotel-clickout
title: Stay22 exact hotel affiliate clickouts
status: done
priority: P1
area: api
owner: codex-stay22
claimed_at: 2026-09-09T11:09:58Z
created_at: 2026-09-09T11:08:28Z
completed_at: 2026-09-09T12:04:46Z
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
- [x] Backend, frontend and fixture browser validation; PR opened without enabling live tracking.

## Steps

- [x] Implement and review independent API, admin and frontend changes.
- [x] Run checks, document release boundary and open PR.

## How to verify

Ruff, mypy, pytest; ESLint, TypeScript, i18n, Vitest, build; desktop/Pixel fixture Playwright. No real affiliate test clicks or bookings.

## Notes

Base origin/main 95122362. Canonical checkout is dirty and untouched. README.md remains claimed by the merchant task; all feature documentation goes in docs/stay22-allez.md. Existing catalog.tsx is also claimed, so booking context uses a narrow shared context provider around the existing stay catalog slot instead of editing that file.

Completed validation: all PR CI checks passed on 6e7e0d4ad186a36e0c50442ddef86af8aa39e3fb, including API (2691 passed, 13 skipped), web lint/type/i18n/tests/build, containers and PostgreSQL/Redis/RQ full-stack smoke. Local production Playwright passed 148 desktop/Pixel fixture tests. An early redirect fixture escaped interception using a fixture AID; this was disclosed in PR #379 and replaced with a same-origin fixture plus external-traffic blocking. No order or commission verification was performed.

On explicit user merge authorization, PR #379 was squash-merged into main as a8be96cd5bc0fca3f35c1f13fe5086fb2b0b219d on 2026-09-09. Remote main containment was verified. No deployment or live Allez activation was requested or performed. This post-merge task closure is retained locally; no extra main push is part of the merge request.
