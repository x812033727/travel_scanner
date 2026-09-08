---
id: 2026-09-08-admin-domain-regression-compatibility-tests
title: Admin domain regression compatibility tests
status: review
priority: P1
area: web
owner: codex-admin-regression
claimed_at: 2026-09-08T10:38:38Z
created_at: 2026-09-08T10:38:37Z
completed_at:
branch: codex/admin-domain-workspaces
depends_on: []
scope:
  - apps/web/e2e/merchant-styles.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/components/admin-foods-workspace.test.tsx
  - apps/web/components/admin-partial-payload.test.tsx
  - apps/web/components/admin-hotspots-workspace.test.tsx
---

# Admin domain regression compatibility tests

## Why

Old assertions must validate the actual new domain structure without dropping partial-payload safety or filter behavior.

## Definition of done

- [x] Existing food workspace and partial payload tests reflect the new hierarchy.
- [x] Real status filters, legacy/current taxonomy links and Back/Forward remain covered.
- [x] Hotspot identity/missing-location and all pending queues have regressions.
- [ ] Full PR checks and authorized merge complete.

## Steps

- [x] Update provider metadata and Next navigation fixtures.
- [x] Preserve meaningful partial-payload controls/table assertions.
- [x] Add hotspot workspace coverage.

## How to verify

Run Vitest admin-foods-workspace.test.tsx, admin-partial-payload.test.tsx and admin-hotspots-workspace.test.tsx (15 focused cases pass).

## Notes

No product changes in this task. Tests deliberately use domain-scoped requests rather than expecting obsolete mixed pending totals.
Legacy browser compatibility: 24 cases pass on desktop and Pixel 7 (merchant styles and admin contrast/44px controls). Original style review/publish boundaries remain asserted.
The readability claim was handed off from the already-merged planner weather work; merchant E2E claim was released by its owner in d243d287.
