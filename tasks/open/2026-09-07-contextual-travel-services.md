---
id: 2026-09-07-contextual-travel-services
title: Contextual travel services and affiliate catalog
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-07T07:56:29Z
completed_at:
branch: codex/contextual-travel-services
depends_on: []
scope:
  - apps/api/app/travel_services
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/config.py
  - apps/api/app/affiliates
  - apps/api/app/saved
  - apps/api/app/trips/stay_router.py
  - apps/api/app/trips/schedule.py
  - apps/api/app/worker.py
  - apps/api/app/i18n.py
  - apps/api/app/ui_text/schemas.py
  - apps/api/app/analytics/scheduler.py
  - apps/api/migrations/versions
  - apps/api/tests/test_travel_services.py
  - apps/api/tests/test_travel_services_integration.py
  - apps/api/tests/test_ui_text.py
  - apps/web/components/travel-services
  - apps/web/components/trip-editor.tsx
  - apps/web/components/stay-area-flow.tsx
  - apps/web/components/hotspot-guide-panel.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/components/saved-items-provider.tsx
  - apps/web/components/account-saved-items.tsx
  - apps/web/lib/api.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/proxy-context.ts
  - apps/web/app/api/travel/[...path]/route.test.ts
  - apps/web/i18n
  - apps/web/lib/ui-text.ts
  - apps/web/lib/ui-text.test.ts
  - apps/web/messages/en/travelServices.json
  - apps/web/messages/ja/travelServices.json
  - apps/web/messages/ko/travelServices.json
  - apps/web/messages/zh-TW/travelServices.json
  - apps/web/messages/zh-CN/travelServices.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/app/[locale]/destinations
  - apps/web/app/[locale]/admin/travel-services
  - apps/web/e2e/travel-services.spec.ts
  - apps/web/vitest.setup.tsx
  - docs/travel-services.md
  - tools/check-i18n.mjs
  - .env.example
  - .github/workflows/ci.yml
---

# Contextual travel services and affiliate catalog

## Why

Implement the user-approved contextual hotel, transfer, tour and eSIM catalog plan.
Keep live prices separate from unpriced reviewed catalog products, with gated brands
and server-resolved affiliate links. Preserve existing manual itinerary items.

## Definition of done

- [x] Reviewed catalog and brands, guarded links, privacy-safe click tracking.
- [x] Trip recommendations, lodging anchors, planned services, saved items.
- [x] Five-locale public/admin UI and responsive accessibility.
- [x] Imports, maintenance, review coverage and safe feature switches.
- [x] API, web, migrations, browser checks and PR.
- [ ] Release gates: real six-city inventory, live tracking verification and explicit enablement.

## Steps

- [x] Backend contracts and tests.
- [x] Frontend integrations and tests.

## How to verify

Run focused pytest, Ruff, mypy, i18n, TypeScript, ESLint, Vitest, production build,
fresh PostgreSQL migrations and Playwright; report unavailable infrastructure.

## Notes

Isolated worktree C:/Users/x8120/travel-services-worktree from main 44646de.
Root checkout is dirty and untouched. Current approved-brand state and real product
data require live verification; features remain off until reviewed and link-tested.

Implementation validation on head 106f8b1: all four CI jobs passed (run 34105073171):
API/Ruff/mypy/fresh PostgreSQL, web/i18n/types/lint/Vitest/build/Playwright,
containers and the existing PostgreSQL/Redis/RQ full-stack smoke. Local new browser
spec passed 20 desktop + 20 mobile tests; screenshots use explicit fixtures.
Follow-up hardening covers DNS-pinned redirect chains, marker-wide rolling quotas,
Naver lodging identity and airport transfer flight-number confirmation. Rebased on
main 516713d. All four jobs passed again on code head 1f417c7 (run 34106782777),
including unsafe-redirect disabling and transient maintenance-failure rotation.
PR https://github.com/x812033727/travel_scanner/pull/336 was merged and deployed as
8853695 on 2026-09-07. The content release gates below remain open; this task is released
for follow-up rather than marked done. Ordinary hotel booking is tracked separately
in 2026-09-07-hotel-direct-booking.
Subsequent task-only status commits do not change the tested application code.

Read-only live account check on 2026-09-07 is recorded in docs/travel-services.md:
12 in-scope brands available, seven still under Unlock more. No account settings,
production data or secrets were changed. The plan's 36 hotels, 18 tours, 12 transfers
and nine country eSIM plans are NOT verified/populated yet; zero fabricated seed
products. Real brand imports, content review, feed access and actual affiliate
landing/tracking checks remain explicit pre-release work. The software can be
reviewed independently with all public/category switches off. Do not mark this
task done or the service production-ready merely because automated tests pass.
