---
id: 2026-11-12-fixture-trips-dated-2026-11-10
title: Fixture trips dated 2026-11-10/11 expired: API integration and e2e travel-services fail on main
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-12T02:05:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/api/tests/test_alerts_integration.py
  - apps/web/e2e/travel-services.spec.ts
---

# Fixture trips dated 2026-11-10/11 expired: API integration and e2e travel-services fail on main

## Why

Since 2026-11-12 (UTC) every CI run fails in `api-tests` and `web-e2e`, whatever the change:
fixture trips start on 2026-11-10 or 2026-11-11, and `SaveTripRequest`
(`apps/api/app/trips/router.py`, "開始日期不可早於今天", one day of slack) now refuses them with a
422, while the planner hides blocks for days that have passed. `main`'s last green CI run
(43119128115) finished 2026-11-11 23:37 UTC, just before the date rolled over. Seen first on
x812033727/travel_scanner#2081 (run 43136712819), whose diff touches none of these files.

Failing there:
- `apps/api/tests/test_integration_postgres_redis.py`: 13 tests (blank trip creation, manual blank
  trip, schedules, AI regeneration, notes, expenses, share link, reoptimize, copy shared trip,
  pasted place, search from trip, flight anchor, flight status), all `assert 422 == 201`.
- `apps/api/tests/test_alerts_integration.py::test_an_alert_leads_back_to_the_trip_and_search_it_came_from`.
- The other three `api-tests` shards fail too (not yet itemised; the same 18 fixed dates under
  `apps/api/tests` are the likely cause: `grep -rn "start_date.*2026-11-1[0-2]" apps/api/tests`).
- `apps/web/e2e/travel-services.spec.ts`: "Klook direct hotel booking stays separate from
  destination discovery" (5 locales) and "unified hotel panel preserves context and honest
  external pricing" (15), fixture trip 2026-11-11..13.

Already handled elsewhere: `apps/web/components/trip-editor.test.tsx` (pinned clock, open PR
#2060 and #2081) and `apps/api/tests/test_trip_creation.py` (relative dates, #2081). #2066 and
#2079 pinned the clock in earlier e2e and API tests the same way.

## Definition of done

- [ ] No API or e2e test depends on a fixture trip date staying in the future: dates are
  relative to today, or the clock is pinned before the fixture dates.
- [ ] `api-tests` (4 shards) and `web-e2e` (3 shards) are green on `main`.

## Steps

- [ ] Itemise the failures in all four `api-tests` shards.
- [ ] API: build fixture dates from `date.today()` (as `test_trip_creation.py` now does), or a
  shared helper, rather than pinning `datetime.now` inside the validator.
- [ ] e2e: pin the browser clock before the fixture dates, as #2079 did for the planner specs.

## How to verify

`cd apps/api && uv run pytest tests/test_integration_postgres_redis.py tests/test_alerts_integration.py`
(needs the CI Postgres and Redis) and `npx playwright test e2e/travel-services.spec.ts` in `apps/web`.

## Notes

Filed from the #2081 session (MiniMax speech), which does not fix these, to keep that PR to its
own change.
