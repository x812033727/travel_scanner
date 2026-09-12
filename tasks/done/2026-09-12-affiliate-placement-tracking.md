---
id: 2026-09-12-affiliate-placement-tracking
title: Placement-aware destination offers and per-surface affiliate switch
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T05:36:20Z
created_at: 2026-09-12T05:36:15Z
completed_at: 2026-09-12T12:08:16Z
branch: claude/affiliate-controls-and-guide-cta
depends_on: []
scope:
  - apps/api/app/affiliates/router.py
  - apps/api/app/travel_services/stay22.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/tests/test_affiliate_brand_channels.py
  - apps/api/tests/test_stay22_routes.py
  - apps/api/tests/test_affiliate_sub_id.py
  - apps/api/tests/test_travel_services.py
  - apps/web/lib/hotel-booking-placement.ts
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
  - apps/web/components/travel-services/catalog.test.tsx
  - docs/travel-services.md
---

# Placement-aware destination offers and per-surface affiliate switch

## Why

Destination offers could only be listed and clicked as `placement="destination"`, so a click
from an article and a click from the services page were indistinguishable in
`affiliate_clicks` and in the partner-side `sub_id`. There was also no way to switch a public
surface off without deploying. Both are needed before offers appear on first-party content.

## Definition of done

- [x] `GET /affiliates/destination-offers` and its clickout accept `placement` from the closed
      `BookingPlacement` set, which now includes `guide` and `city`.
- [x] Every destination-offer click records `placement` and ends its `sub_id` with it
      (`dst_hotel_hiroshima_zh-TW_guide`).
- [x] `CatalogConfig.affiliate_placements` lists the surfaces that may show offers; a surface not
      in the list gets an empty list and a 404 on click. Legacy surfaces default on, `guide` and
      `city` default off.
- [x] The web component sends its placement and keys its request on it.

## Steps

- [x] Move `BookingPlacement` into `travel_services/schemas.py` (re-exported from `stay22.py`).
- [x] Thread `placement` through `_ready_destination_offers`, `_destination_option` and the clickout.
- [x] Tests: HTTP gating and labelling, sub_id pass-through, config defaults and ordering.

## How to verify

```
cd apps/api && uv run pytest tests/test_affiliate_brand_channels.py tests/test_affiliate_sub_id.py tests/test_travel_services.py tests/test_stay22_routes.py -q
cd apps/web && npx vitest run components/destination-affiliate-options.test.tsx
```

## Notes

The placement rides the clickout URL (`?placement=guide`) and is re-validated on the POST, so a
page rendered before the surface was switched off cannot click through. `BookingPlacement` is
also the Stay22 campaign vocabulary, so the parametrised Stay22 placement test covers the two
new tokens automatically. Member-tokened clickouts keep no request placement; see
`2026-09-12-affiliate-click-placement`.
