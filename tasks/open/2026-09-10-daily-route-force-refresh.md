---
id: 2026-09-10-daily-route-force-refresh
title: Preserve force refresh in daily route background jobs
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T08:40:00Z
created_at: 2026-09-10T06:02:14Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/route_tasks.py
  - apps/api/tests/test_route_tasks.py
---

# Preserve force refresh in daily route background jobs

## Why

Read-only review during the Seoul route fix found that compute-day accepts
payload.refresh but does not pass it through enqueue_trip_routing to the worker.
The flag changes rate-limit handling, while valid persisted routes are still
reused. This is an existing issue, not a Google fallback blocker for unqueried legs.

## Definition of done

- [x] An explicit full-day refresh actually refreshes eligible saved routes.
- [x] Single-leg overrides and optimistic version checks remain intact.

## Steps

- [x] Trace refresh through API, queue and worker, with backwards-compatible defaults.
- [x] Add tests distinguishing ordinary reuse from explicit refresh.

## How to verify

Run route_tasks and routing API tests using fixed provider fixtures; verify the
provider call count when a saved route has not expired. Do not use live quotas.

## Notes

Found in review against fe26ff8c plus the Seoul transport UX changes. Not changed
by that task; no production operation was performed.

### 2026-09-19 done in repo (claude-fable-5-1)

- Trace: `compute_trip_routes_for_day` read `payload.refresh` for the rate-limit bucket only;
  `enqueue_trip_routing` queued three arguments, `run_trip_routing_job` and `_run` had no
  flag, while `compute_and_apply_routes` already accepted `refresh`. The flag now travels
  the whole way: `enqueue_trip_routing(..., refresh=payload.refresh)` queues it as the fourth
  positional job argument, `run_trip_routing_job(trip_id, expected_version, target_day=None,
  refresh=False)` passes it to `_run`, which passes it to `compute_and_apply_routes`.
- Backwards compatible: a job queued by an older API process carries three arguments and
  runs with `refresh=False`, exactly as before. The other enqueue sites (whole-trip
  compute, preferences, reorder) are unchanged and keep reusing saved legs. Single-leg
  overrides and the `expected_version` check are untouched.
- Tests `tests/test_route_tasks.py`: the queued job arguments with and without the flag,
  the job signature's trailing default, and `_run` forwarding `refresh` to the computation.
  `test_trip_preferences` still passes (its fakes take `*args, **kwargs`).
- After deploy: a compute-day call with `refresh: true` on a day whose legs are already
  saved should show fresh `computed_at`/provider fields on those legs; one without it
  should not. The Postgres integration tests for the endpoint run in CI.
