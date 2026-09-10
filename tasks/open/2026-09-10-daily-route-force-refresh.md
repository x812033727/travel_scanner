---
id: 2026-09-10-daily-route-force-refresh
title: Preserve force refresh in daily route background jobs
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-10T06:02:14Z
completed_at:
branch:
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

- [ ] An explicit full-day refresh actually refreshes eligible saved routes.
- [ ] Single-leg overrides and optimistic version checks remain intact.

## Steps

- [ ] Trace refresh through API, queue and worker, with backwards-compatible defaults.
- [ ] Add tests distinguishing ordinary reuse from explicit refresh.

## How to verify

Run route_tasks and routing API tests using fixed provider fixtures; verify the
provider call count when a saved route has not expired. Do not use live quotas.

## Notes

Found in review against fe26ff8c plus the Seoul transport UX changes. Not changed
by that task; no production operation was performed.
