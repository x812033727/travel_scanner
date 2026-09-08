---
id: 2026-09-08-planner-nearby-followup
title: Fix nearby itinerary discovery across cities and reset insertion pagination
status: review
priority: P2
area: web
owner: codex
claimed_at: 2026-09-08T07:19:39Z
created_at: 2026-09-08T07:19:38Z
completed_at:
branch: codex/planner-nearby-followup
depends_on: []
scope:
  - apps/api/app/trips/place_options.py
  - apps/api/tests/test_trip_place_options.py
  - apps/web/components/itinerary-place-browser.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
---

# Fix nearby itinerary discovery across cities and reset insertion pagination

## Why

After PR #362, a Tokyo trip with a Yokohama stop still searches only the Tokyo catalogue. Repeated insertion from the second page also reuses the old page offset after its reference point changes, which can falsely show an empty neighbourhood.

## Definition of done

- [x] Nearby results follow the insertion coordinates across city boundaries, with bounded catalogue reads and accurate radius filtering.
- [x] Destination-only discovery and existing favourite visibility remain compatible.
- [x] Changing the previous or following stop starts at page one, cancels obsolete requests and ignores late results without losing the added-item confirmation.
- [ ] Regression checks pass and the follow-up is submitted for review.

## Steps

- [x] Fix catalogue query scope and add API regression coverage.
- [x] Reset picker pagination and abort obsolete requests with component regressions.
- [ ] Validate the deployed #362 desktop/mobile editor in the signed-in in-app browser.

## How to verify

Run Ruff, mypy and `pytest tests/test_trip_place_options.py`; run focused picker Vitest, ESLint, TypeScript, i18n and task-board checks. PostgreSQL integration cases are also required in CI. In the production in-app browser, inspect insertion gaps, move controls, favourites/nearby panels and responsive layout without modifying existing real trips.

## Notes

- #362 merged as `434345419dc4a4117830f611197707fa11ed9b04`; its completed task is moved to `tasks/done` in this follow-up.
- Osaka and Kyoto share `osaka-kyoto`; Tokyo/Yokohama are distinct catalogue destinations and provide a meaningful regression fixture.
- Nearby coordinates are authoritative; do not add a new restriction to the primary destination country, since a trip can include a cross-border stop.
- Production deployment of #362 is handled independently from this follow-up. These follow-up changes are not live until reviewed, merged and deployed.
- Local checks: full Ruff passed, mypy passed for 258 modules, focused API tests 22 passed / 2 PostgreSQL+Redis HTTP cases skipped without local services. New SQL regressions run on SQLite locally and additionally on PostgreSQL in CI.
- Web checks: 51 focused picker/editor/order tests passed; changed-file ESLint, TypeScript, five-locale i18n and task checks passed.
