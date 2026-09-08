---
id: 2026-09-08-admin-catalog-review-filters-and-canonical
title: Admin catalog review filters and canonical location editor
status: review
priority: P1
area: web
owner: codex-admin-editors
claimed_at: 2026-09-08T10:29:58Z
created_at: 2026-09-08T10:29:58Z
completed_at:
branch: codex/admin-domain-workspaces
depends_on: []
scope:
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/admin-food-merchants-panel.test.tsx
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-hotspots-panel.test.tsx
  - apps/web/components/admin-hotspot-places-panel.tsx
  - apps/web/components/admin-hotspot-places-panel.test.tsx
  - apps/web/components/admin-foods-panel.tsx
  - apps/web/components/admin-foods-panel.test.tsx
  - apps/web/components/admin-restaurant-scans-panel.tsx
  - apps/web/components/admin-restaurant-scans-panel.test.tsx
  - apps/api/app/hotspots/admin_router.py
  - apps/api/tests/test_admin_domain_filters.py
  - apps/web/lib/admin-catalog-copy.ts
---

# Admin catalog review filters and canonical location editor

## Why

A new review tab must really request pending items. Place identities and restaurant automation must not have conflicting editors.

## Definition of done

- [x] Attractions/dishes/merchants catalog and review share editors with correct server filters.
- [x] Place identity editing has one destination with an exact-ID/missing-location filter and clear-filter control.
- [x] Google profile website saves never resubmit a stale Place ID.
- [x] Restaurant automation shows status and links to Food settings; explicit scan/retry remains available.
- [ ] PR checks and authorized merge complete.

## Steps

- [x] Add canonical links and five-language copy.
- [x] Add real SQLite API filtering tests plus disposable PostgreSQL variants.
- [x] Verify permanent coordinate/Naver identity and review workflows remain intact.

## How to verify

Run tests/test_admin_domain_filters.py and hotspot tests.
Run focused hotspot/places/foods/merchants/restaurant-scans Vitest tests, ESLint and TypeScript.

## Notes

No source or publication changes. Clear location filters remove only hotspot_id and missing_location while preserving locale and other query parameters.
