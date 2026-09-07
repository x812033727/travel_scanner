---
id: 2026-09-07-contextual-travel-services
title: Contextual travel services and affiliate catalog
status: in-progress
priority: P1
area: api
owner: codex-travel-services
claimed_at: 2026-09-07T07:57:23Z
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
  - apps/web/components/travel-services
  - apps/web/components/trip-editor.tsx
  - apps/web/components/stay-area-flow.tsx
  - apps/web/components/hotspot-guide-panel.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/saved-items-provider.tsx
  - apps/web/components/account-saved-items.tsx
  - apps/web/lib/api.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/proxy-context.ts
  - apps/web/app/api/travel/[...path]/route.test.ts
  - apps/web/i18n
  - apps/web/lib/ui-text.ts
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

- [ ] Reviewed catalog and brands, guarded links, privacy-safe click tracking.
- [ ] Trip recommendations, lodging anchors, planned services, saved items.
- [ ] Five-locale public/admin UI and responsive accessibility.
- [ ] Imports, maintenance, review coverage and safe feature switches.
- [ ] API, web, migrations, browser checks and PR.

## Steps

- [ ] Backend contracts and tests.
- [ ] Frontend integrations and tests.

## How to verify

Run focused pytest, Ruff, mypy, i18n, TypeScript, ESLint, Vitest, production build,
fresh PostgreSQL migrations and Playwright; report unavailable infrastructure.

## Notes

Isolated worktree C:/Users/x8120/travel-services-worktree from main 44646de.
Root checkout is dirty and untouched. Current approved-brand state and real product
data require live verification; features remain off until reviewed and link-tested.
