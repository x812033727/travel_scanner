---
id: 2026-09-14-redis-py-8-migration
title: Migrate the API from redis-py 6 to redis-py 8
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:33:47Z
created_at: 2026-09-14T11:01:03Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - apps/api/app/infra.py
  - apps/api/app/crawlers/fx.py
  - apps/api/app/hotspots/guides.py
  - apps/api/app/locations/map_identity_router.py
  - apps/api/tests/test_google_places.py
  - apps/api/tests/test_hotspot_restaurants.py
  - apps/api/tests/test_social_login.py
---

# Migrate the API from redis-py 6 to redis-py 8

## Why

`apps/api/pyproject.toml` pins `redis>=6.4,<7`. Dependabot opened
[#483](https://github.com/x812033727/travel_scanner/pull/483) on 2026-09-14 to install 8.1.0
and widen the pin to `<9`. That skips two major versions of the client that the RQ worker
queue and the API's caches run on, so it was closed rather than merged.

Its `api` job failed at `uv run mypy app`
([job log](https://github.com/x812033727/travel_scanner/actions/runs/34809374419/job/103867450444)),
which means **pytest never ran**: nothing is known yet about runtime behaviour under 7.x or
8.x. The type errors show where the client's annotations changed:

```text
app/crawlers/fx.py:49: error: Argument 1 to "wait_for" has incompatible type "Awaitable[bytes | str | None]"; expected "Future[str] | Awaitable[str]"  [arg-type]
app/infra.py:23: error: Redundant cast to "Redis"  [redundant-cast]
app/infra.py:95: error: Redundant cast to "Awaitable[Any]"  [redundant-cast]
app/infra.py:168: error: Redundant cast to "Awaitable[Any]"  [redundant-cast]
app/hotspots/guides.py:738: error: Redundant cast to "Awaitable[Any]"  [redundant-cast]
app/locations/map_identity_router.py:159: error: Incompatible types in assignment (expression has type "dict[str, object]", variable has type "bytes | str | None")  [assignment]
app/locations/map_identity_router.py:182: error: Unsupported target for indexed assignment ("bytes | str | None")  [index]
app/locations/map_identity_router.py:185: error: Incompatible return value type (got "bytes | str | None", expected "dict[str, Any]")  [return-value]
```

Staying on 6.x is not free either. Closing a Dependabot pull request only skips that one
release, so the next 8.x release will open another one.

## Definition of done

- [x] `redis` is on 8.x in `pyproject.toml` and `uv.lock`, still with an upper bound.
- [x] `uv run mypy app` passes without new `cast` or `type: ignore` that hide a real change in
      what a command returns.
- [ ] Full CI is green, including the integration tests that run against the `redis:7.4-alpine`
      service. Production runs the same image (`docker-compose.prod.yml`).
- [ ] After a deploy, the worker still picks up and finishes a queued job.

## Steps

- [x] Read the redis-py 7.0 and 8.0 release notes for breaking changes: removed APIs, changed
      defaults (protocol version, response decoding) and typing.
- [x] Confirm that the locked `rq` (2.12) and `fakeredis` (2.38) support redis-py 8; the
      resolver accepting it proves nothing about behaviour.
- [x] Fix the eight errors above. `map_identity_router.py` assigns a dict to a variable typed as
      a Redis reply, which is worth reading as a possible real bug rather than silencing.
- [ ] Run the API checks, push, and read the integration results in CI (there is no local
      PostgreSQL/Redis on the Windows machine).

## How to verify

```bash
cd apps/api
uv run ruff check .
uv run mypy app
uv run pytest
```

## Notes

- Filed from the 2026-09-14 review of the first Dependabot batch (#475–#484).

### 2026-09-19 done in repo (claude-fable-5-1)

Claimed with `--force` over two review tickets of the same owner (merged code) that hold
`app/hotspots/guides.py`. Scope widened with three test files that pass a `GET` reply straight
to `json.loads` and now need `assert raw is not None` (CI runs `mypy tests`).

- `redis>=8.1,<9`; `uv lock --upgrade-package redis` moved only redis (6.4.0 → 8.1.0).
  rq 2.12.0 (`redis!=6,>=3.5`, ships explicit 8.x connection-kwarg handling) and fakeredis
  2.38.0 (`redis>=4.3`, emulates RESP3) accept it; an in-process rq SimpleWorker on fakeredis
  enqueued, finished and failed jobs correctly.
- The eight mypy errors, none silenced: `fx.py` bound `value` twice (str from the memory
  cache, then the GET reply) so `wait_for` inferred `str`; the reply is now `stored`, decoded
  when bytes. The `cast(Redis, from_url(...))`, the four `cast(Awaitable[Any], eval(...))`
  and the hincrby/expire casts are gone (8.x types the async commands as awaitables).
  `map_identity_router.py` was **not** a bug: `state` was reused for the idempotency-replay
  GET reply and, later, the new batch dict; the reply is now `stored` and `state` is annotated.
- One real behaviour change caught and handled: 8.x defaults `socket_timeout=5` (6.x: none)
  and retries a timed-out read ten times. The shared `get_redis()` client serves
  `XREAD … BLOCK 15000` (search SSE) and 2 s pubsub polls, so it now passes
  `socket_timeout=None` (connect timeout kept). rq workers set their own 415 s timeout.
- Wire protocol is RESP3 with legacy response shapes by default; every command family the app
  uses (SET NX, GET, EXISTS, GETDEL, INCR, EXPIRE, HINCRBY, HGETALL, HGET, MGET, XADD, XREAD,
  pipelines, WATCH/MULTI, pubsub, aclose then reuse) returns the 6.x shapes on fakeredis.
- New under 8.1: `redis.setex` is deprecated (`app/places/router.py:198`); left for
  `2026-09-19-app-places-router-py-redis-setex` (one line, `set(..., ex=)`).
- Local: ruff clean, `mypy app` 338 files clean, `mypy tests` 252 files clean,
  pytest 3940 passed / 343 skipped.

**Not verifiable here, CI's integration job is the check**: HELLO 3 against `redis:7.4-alpine`,
the RESP3 pubsub/XREAD paths on a real server (`app/search/router.py` SSE,
`app/community/messaging.py`, `app/search/events.py`), the EVAL rate-limit scripts
(`app/infra.py`, `app/hotspots/guides.py`; fakeredis has no Lua), the timeout/retry behaviour on
a real socket. **After the deploy the owner confirms a worker still picks up a queued job**:

```bash
docker compose -f docker-compose.prod.yml logs --since 10m worker | grep -c "Job OK"   # > 0 after any enqueue
docker compose -f docker-compose.prod.yml exec -T api python -c "import redis; print(redis.__version__)"   # 8.1.0
```
