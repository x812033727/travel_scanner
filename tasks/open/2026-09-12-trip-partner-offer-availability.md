---
id: 2026-09-12-trip-partner-offer-availability
title: Trip payloads carry partner offer availability and trip-sourced options carry the trip placement
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T13:27:21Z
created_at: 2026-09-12T13:27:18Z
completed_at:
branch: claude/trip-partner-offers
depends_on: []
scope:
  - apps/api/app/travel_services/service.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/affiliates/router.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_affiliate_brand_channels.py
  - apps/api/tests/test_travel_services.py
  - apps/api/tests/test_trip_share_payload.py
  - apps/api/tests/test_integration_postgres_redis.py
  - docs/travel-services.md
  - docs/affiliate-configuration.md
---

# Trip payloads carry partner offer availability and trip-sourced options carry the trip placement

## Why

The trip planner may not make a partner request on first paint (calm-planner rule, pinned by
`trip-editor.test.tsx` and `e2e/planner-premium.spec.ts`), so the page needs to know whether a
partner block exists before anything is fetched. Separately, branded offers minted for a trip
by `/affiliates/options?trip_id=` were labelled `placement=destination`, so trip-page clicks
were indistinguishable from services-page clicks in the click report.

## Definition of done

- [x] `GET /trips/{id}` (full payload) carries `partner_offers: {destination_id, modules}` — the
      modules with a ready destination offer for the `trip` surface; availability only.
- [x] `GET /shared-trips/{token}` carries the same shape computed for the new `share` surface
      (off by default, not added to the owner allowlist).
- [x] `/affiliates/options?trip_id=` mints branded offers with `placement=trip`; search keeps
      `destination`.
- [x] `BookingPlacement` gains `share`; the Stay22 placement test covers it automatically.

## Steps

- [x] `ready_destination_offers` / `partner_offer_modules` in `travel_services/service.py`; the
      affiliates router keeps `_ready_destination_offers` as a thin wrapper (tests patch it).
- [x] Trip and share serialisers; docs.

## How to verify

```
cd apps/api && uv run pytest tests/test_affiliates.py tests/test_affiliate_brand_channels.py tests/test_travel_services.py tests/test_stay22_routes.py tests/test_trip_share_payload.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_integration_postgres_redis.py -q   # CI
```

## Notes

`trip.data["destination_id"]` is never written in production; the id is derived with
`_option_destination_id` (an Osaka/Kyoto trip resolves to `osaka-kyoto`). The full payload
now costs one settings read, one config read and, only when the catalog is on, one offers
query. `2026-09-07-contextual-travel-services` (open, unowned) lists these directories.
