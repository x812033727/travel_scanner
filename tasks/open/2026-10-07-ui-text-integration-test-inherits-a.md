---
id: 2026-10-07-ui-text-integration-test-inherits-a
title: UI text integration test inherits a Redis client from a closed event loop
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-ui-text-redis
claimed_at: 2026-10-07T05:43:13Z
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

- [x] The module starts on a fresh engine pool and a fresh Redis client, whatever ran before
  it in the shard.

## Steps

- [x] Before the fixture's `yield`, add `await engine.dispose(close=False)` and
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
- Root cause, reproduced on 2026-10-07 with local PostgreSQL 16 and Redis
  (`RUN_INTEGRATION_TESTS=1 uv run pytest --shard 1/4` fails the same way). The module that leaves
  the client behind is `tests/test_analytics_integration.py`. Its tests run on a module-scoped loop
  through the app, so `app/infra.py`'s real `get_redis()` client is created there. It never clears
  that client, so the client outlives its loop.
  `uv run pytest tests/test_analytics_integration.py tests/test_ui_text_integration.py` fails
  without the fix and passes with it.
- Why main passed and #1364 failed with the same files: `tests/sharding.py` `assign` takes one
  entry per collected test, not per file. The estimate for a file missing from
  `shard_durations.json` is the median over that list, so it moves when a listed file gains tests.
  #1364 added 60 test cases to the three speech test files. That reshuffled the shards:
  `test_ui_text_integration.py` moved from shard 3 (on main) to shard 1, after
  `test_analytics_integration.py`. The module docstring says "the median of the ones that are"
  listed, meaning files. Left as is; recorded here.
- Not done: clearing the client in `test_analytics_integration.py` too, or one autouse fixture in
  `conftest.py` for every module. Either would stop the leak at its source, but both are outside
  this scope. The other integration modules already guard themselves as this one now does.
