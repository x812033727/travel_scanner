---
id: 2026-10-07-ui-text-integration-test-inherits-a
title: UI text integration test inherits a Redis client from a closed event loop
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-07T05:11:43Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_ui_text_integration.py
---

# UI text integration test inherits a Redis client from a closed event loop

## Why

`tests/test_ui_text_integration.py::test_override_reaches_the_public_payload_and_restores_cleanly`
failed in CI shard `api-tests (1/4)` on PR #1364. The run was 37574453603, job 112640206322, at
head 08d04996, which changes no code the test reaches. The error was
`RuntimeError: Event loop is closed`.

The first request, `POST /api/v1/auth/register`, reaches `enforce_named_rate_limit` →
`app/infra.py` `_incr_window` → `get_redis().eval(...)`. `get_redis` is cached for the whole
process (`functools.lru_cache`). Its pooled connection had been opened under an earlier module's
event loop. That loop was closed, so reading the connection failed and so did disconnecting it.

The module's autouse fixture `dispose_engine_after_module` disposes the engine and clears
`get_redis` only after its test. The other integration modules do both before and after
(`isolate_async_clients_for_module` in `test_usage_settings_integration.py`,
`test_registration_settings_integration.py`, `test_deployments_integration.py`,
`test_saved_items_integration.py`). So this module is the one that can start on a client another
module left behind.

The same shard passed on main at ddbf0e4b with the same files, so the failure depends on what
the modules before it leave in the pool. Whatever the order, it is a test-isolation gap.

## Definition of done

- [ ] The module starts on a fresh engine pool and a fresh Redis client, whatever ran before
  it in the shard.

## Steps

- [ ] Before the fixture's `yield`, add `await engine.dispose(close=False)` and
  `get_redis.cache_clear()`, as `isolate_async_clients_for_module` does, and rename the fixture
  to match.

## How to verify

From `apps/api`, with PostgreSQL and Redis running (`RUN_INTEGRATION_TESTS=1`), run
`uv run pytest --shard 1/4`. Also run `uv run pytest tests/test_trip_route_tasks.py
tests/test_ui_text_integration.py`, which puts the module after one that used the app's Redis
client.

## Notes

- Found on PR #1364 (2026-10-07). This is not that PR's failure: no test file of that PR runs in
  shard 1, and its diff does not touch `app/infra.py`, auth or ui_text.
