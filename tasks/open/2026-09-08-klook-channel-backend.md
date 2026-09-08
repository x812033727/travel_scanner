---
id: 2026-09-08-klook-channel-backend
title: Klook channel aware affiliate backend and secure clickout
status: review
priority: P1
area: api
owner: codex-klook-backend
claimed_at: 2026-09-08T16:51:43Z
created_at: 2026-09-08T16:31:23Z
completed_at:
branch: codex/klook-product-integration
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/migrations/versions/0064_klook_affiliate_channels.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/affiliates/registry.py
  - apps/api/app/affiliates/schemas.py
  - apps/api/app/affiliates/service.py
  - apps/api/app/affiliates/router.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/travel_services/registry.py
  - apps/api/app/travel_services/service.py
  - apps/api/app/travel_services/admin.py
  - apps/api/app/travel_services/imports.py
  - apps/api/app/travel_services/router.py
  - apps/api/app/travel_services/hotel_options.py
  - apps/api/app/travel_services/hotel_admin.py
  - apps/api/app/travel_services/network.py
  - apps/api/app/travel_services/channels.py
  - apps/api/tests/test_klook_affiliates.py
  - apps/api/tests/test_affiliate_brand_channels.py
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_travel_services.py
  - apps/api/tests/test_travel_services_integration.py
  - apps/api/tests/test_admin_hotels.py
  - apps/api/tests/test_admin_provider_settings.py
  - .env.example
---

# Klook channel aware affiliate backend and secure clickout

## Why

Klook direct Affiliate enrollment must not impersonate a Travelpayouts project or imply
approval for a pricing API. Reviewed products, destination discovery, hotel booking options,
imports and clickouts need the same explicit channel/account boundary.

## Definition of done

- [x] Existing enrollments retain their IDs and default Travelpayouts channel; direct Klook uses a separate channel and numeric AID.
- [x] Exact product and destination links are reviewed, expire after 30 days and fail closed after AID rotation.
- [x] Direct links require www.klook.com and reject foreign AIDs, redirects and ambiguous tracking; hotel short/detail redirects retain the same numeric property identity.
- [x] Direct browser attestation requires exact identity evidence, safe DNS and an actor audit; it cannot bypass Travelpayouts checks.
- [x] Imports remain pending/idempotent and hotel platform options remain independently reviewed; clickouts never book or charge usage.
- [x] Focused tests, complete Ruff, complete mypy and Alembic head validation pass locally.
- [ ] Real PostgreSQL migration/integration checks pass in CI, including fresh metadata and frozen 0063 schema paths.

## Steps

- [x] Add channel-aware model, enrollment schema, settings and guarded migration 0064.
- [x] Dispatch admin review, CSV import, product/destination/hotel clickouts and audit partner by channel.
- [x] Add direct URL, network redirect, HTTP, import, identity, freshness and migration regressions.
- [ ] Second sub-task.

## How to verify

Run with apps/api as cwd and PYTHONPATH pointing at this worktree's apps/api. The sibling
mokaair-admin-domains/apps/api/.venv/Scripts/python.exe provides dependencies without installation.

- `python -m ruff check .`: passed.
- `python -m mypy app`: passed, 262 source files.
- Final focused Klook/channel/hotel-direct/services/affiliate bundle after privacy and alias fixes: 152 passed, 2 skipped (PostgreSQL-only migration variants).
- Broader services/affiliates/admin-hotels/provider-settings/hotel-platform/direct-link bundle: 236 passed, 25 skipped before the final five added direct network redirect cases (those five pass in the new-test bundle).
- `python -m alembic heads`: one head, `0064_klook_affiliate_channels`.
- `npm run check:tasks`: 190 task files passed after models/hotel-admin scope handoffs.

## Notes

No local PostgreSQL or Docker runtime was available/authorized. The actual migration tests use
isolated PostgreSQL schemas and rollback all fixture DDL; RUN_INTEGRATION_TESTS=1 enables them.
Downgrade refuses while any direct enrollment exists, preventing accidental conversion of
Klook approval into Travelpayouts approval. Travelpayouts verification hashes remain compatible;
Klook hashes include the explicit channel and AID.

The verified enrollment evidence origin is affiliate.klook.com, distinct from www.klook.com
click destinations. No API adapter, price feed, automatic publication or real provider calls were
introduced. Klook's final hotel detail path is supported; different hotel IDs remain rejected.
Hotel option health accepts only the same typed numeric Klook hotel ID through a short/detail
redirect; option-to-offer matching additionally preserves query parameters bidirectionally.
Klook generic template sub_id is coarse module/locale only, never member/trip-derived, while
other providers retain their established behavior.
