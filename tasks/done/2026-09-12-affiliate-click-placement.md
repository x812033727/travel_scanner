---
id: 2026-09-12-affiliate-click-placement
title: Record placement on every affiliate click
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T05:36:33Z
created_at: 2026-09-12T05:34:52Z
completed_at: 2026-09-12T12:08:19Z
branch: claude/affiliate-controls-and-guide-cta
depends_on:
  - 2026-09-12-affiliate-readiness-matrix
scope:
  - apps/api/app/affiliates/router.py
  - apps/api/app/affiliates/schemas.py
  - apps/api/app/trips/stay_router.py
  - apps/api/app/search/router.py
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_trip_stay_router.py
  - apps/api/tests/test_trip_stay_areas.py
---

# Record placement on every affiliate click

## Why

Three of the six `AffiliateClick` writers never set `placement`, so the click report could not
tell a search-page click from a trip-page click.

## Definition of done

- [x] Member-tokened clickouts record `search` or `trip` from the token source.
- [x] The stay-area clickout records `stay`; the Skyscanner flight clickout records `search`.
- [x] The request-validated `BookingPlacement` set is not widened for these paths; a typing-only
      `AffiliatePlacement` documents the union.

## Steps

- [x] `affiliates/router.py`, `trips/stay_router.py`, `search/router.py`.

## How to verify

```
cd apps/api && uv run pytest tests/test_affiliates.py tests/test_trip_stay_router.py -q
```

## Notes

Rows written before this change keep `NULL` and show as `unknown` in the report; the table is
append-only, so there is no backfill.
