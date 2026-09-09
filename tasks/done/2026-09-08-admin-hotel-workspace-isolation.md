---
id: 2026-09-08-admin-hotel-workspace-isolation
title: Admin hotel workspace isolation
status: done
priority: P1
area: api
owner: codex-admin-hotel
claimed_at: 2026-09-08T10:04:05Z
created_at: 2026-09-08T10:03:38Z
completed_at: 2026-09-08T13:16:24Z
branch: codex/admin-domain-workspaces
depends_on: []
scope:
  - apps/api/tests/test_hotel_platforms.py
  - apps/api/app/travel_services/admin.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/travel_services/imports.py
  - apps/api/app/travel_services/hotel_admin.py
  - apps/api/app/main.py
  - apps/api/tests/test_admin_hotels.py
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/admin.test.tsx
  - apps/web/components/travel-services/hotel-options-admin.tsx
  - apps/web/components/travel-services/hotel-admin.test.tsx
  - apps/web/app/[locale]/admin/hotels
  - apps/web/app/[locale]/admin/partners
  - apps/web/lib/admin-hotels-copy.ts
---

# Admin hotel workspace isolation

## Why

Hotel management was mixed with flights, eSIM and other services; changing a hotel setting must not alter unrelated global config.

## Definition of done

- [x] Hotel-only overview, products, reviews, platform links, offers/import/coverage and settings are available.
- [x] Versioned hotel PATCH preserves global, non-hotel, city and Airalo configuration.
- [x] Both CSV phases reject non-hotel rows and cross-kind source-key replacement.
- [x] Shared brands have one Partners editor; product/platform/offer/brand review gates remain distinct.
- [x] First-row and existing-row config writes share a transaction lock with legacy PUT.
- [x] PR integration checks and authorized merge complete.

## Steps

- [x] Add hotel endpoints and reuse domain-scoped travel-service components.
- [x] Preserve existing platform types, legacy URLs and non-secret draft versions.
- [x] Cover narrow updates, imports, counts and concurrency.

## How to verify

Run pytest tests/test_admin_hotels.py and travel service tests; PostgreSQL race tests require isolated RUN_INTEGRATION_TESTS=1.
Run Vitest travel-services/hotel-admin.test.tsx and admin.test.tsx (17 focused cases passed).
Full-stack admin Playwright logs into CLI-created fixture accounts and persists a hotel setting.

## Notes

No hotel publishing, provider switching or paid calls performed. Existing Stay22 and shared travel service behavior are preserved.
The first-config-row lock is shared by both hotel PATCH and legacy global PUT, including safe 409 rollback.
CI exposed an existing collection-time clock fixture: quotes expired after two minutes before their test ran. The hotel-platform test now freezes its own clock, with separate expired/valid quote regressions (21 focused cases pass); production expiry behavior is unchanged.
