---
id: 2026-09-08-admin-domain-navigation-and-workspaces
title: Admin domain navigation and workspaces
status: done
priority: P1
area: web
owner: codex-admin-root
claimed_at: 2026-09-08T10:04:04Z
created_at: 2026-09-08T10:03:37Z
completed_at: 2026-09-08T13:16:23Z
branch: codex/admin-domain-workspaces
depends_on: []
scope:
  - apps/api/app/i18n.py
  - .github/workflows/ci.yml
  - apps/web/e2e/admin-domains-full-stack.spec.ts
  - apps/web/app/[locale]/admin/travel-services/page.tsx
  - apps/web/app/[locale]/admin/catalog-review/page.tsx
  - apps/web/components/admin-tabs.tsx
  - apps/web/components/admin-tabs.test.tsx
  - apps/web/app/[locale]/admin/page.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/components/admin-hotspots-workspace.tsx
  - apps/web/components/admin-foods-workspace.tsx
  - apps/web/components/admin-domain-workspaces.test.tsx
  - apps/web/components/admin-dashboard.tsx
  - apps/web/components/admin-dashboard.test.tsx
  - apps/web/components/admin-domain-workspace.tsx
  - apps/web/lib/admin-workspace-navigation.ts
  - apps/web/lib/admin-workspace-navigation.test.ts
  - apps/web/lib/admin-domains-copy.ts
  - apps/web/lib/admin-domains-messages
  - apps/web/app/[locale]/admin/hotspots/page.tsx
  - apps/web/app/[locale]/admin/foods/page.tsx
  - apps/web/e2e/admin-domains.spec.ts
  - docs/admin-domains.md
  - apps/api/app/admin/dashboard_router.py
  - apps/api/tests/test_admin_dashboard.py
---

# Admin domain navigation and workspaces

## Why

Admin data and settings were scattered by implementation rather than the domain an administrator manages.

## Definition of done

- [x] Overview, Attractions, Food and Hotels are the primary entries.
- [x] Secondary operations/system groups are searchable and preserve backend capability checks.
- [x] Canonical tabs and legacy bookmarks work on desktop and mobile without triggering paid queries.
- [x] Domain counts, missing-data and pending-review links have real scoped destinations.
- [x] PR checks pass and the user-authorized merge is verified.

## Steps

- [x] Build on isolated origin/main 7d20ffb, preserving Stay22 and the original dirty checkout.
- [x] Integrate domain editors/settings and five-locale copy.
- [x] Test and fix Next destination-commit, URL-encoding and rapid-Back races.
- [x] Add isolated browser journeys and a CI-only unmocked admin journey.

## How to verify

Run the repository web lint/typecheck/Vitest/build/i18n commands and API dashboard tests.
Run Playwright e2e/admin-domains.spec.ts on desktop and Pixel 7.
CI creates isolated administrators for e2e/admin-domains-full-stack.spec.ts; never register reserved admin emails publicly.

## Notes

Implementation and API contracts are documented in docs/admin-domains.md.
Desktop/Pixel 7 fixture journeys pass (20 tests); visually inspected dark overview and restaurant scans.
Full local Vitest: 951 tests pass across 146 files. API: 1818 pass, 120 integration skips; Linux-only deployment module runs in CI.
PR: https://github.com/x812033727/travel_scanner/pull/369
No provider enablement or data backfill performed. PostgreSQL/Redis integration runs in CI, not an unknown local database.

## Merge and deployment receipt

- User-authorized PR #369 squash merge verified at `b675f5d34a353eddfb789a953968c3c6d45eac4a` on 2026-09-08; exact main CI run `34229595628` passed all four jobs.
- Production deployed from a verified clean Git archive, keeping the `travel_scanner` Compose project and runtime environment. All eight application services run the merged SHA with zero restarts.
- Protected PostgreSQL backup verified: 12,604,578 bytes, mode 0600, archive index readable. Alembic remains `0063_destination_offers` (no migration change).
- Three consecutive readiness checks passed. Database/Redis container IDs, mounts, environment hash and permissions remained unchanged. Prior images/source and backup retained for rollback.
- Read-only production checks: admin overview/attractions/food/hotels and trips shells return 200; the new hotel API returns `401 authentication_required` anonymously through both direct API and public BFF, with BFF `Cache-Control: no-store`. Provider settings also rejects anonymous access. Community remains disabled.
- Full-stack authenticated administrator behavior was tested in isolated CI, not by mutating production data.
