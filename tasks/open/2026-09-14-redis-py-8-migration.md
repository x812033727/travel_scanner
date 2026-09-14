---
id: 2026-09-14-redis-py-8-migration
title: Migrate the API from redis-py 6 to redis-py 8
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-14T11:01:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - apps/api/app/infra.py
  - apps/api/app/crawlers/fx.py
  - apps/api/app/hotspots/guides.py
  - apps/api/app/locations/map_identity_router.py
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

- [ ] `redis` is on 8.x in `pyproject.toml` and `uv.lock`, still with an upper bound.
- [ ] `uv run mypy app` passes without new `cast` or `type: ignore` that hide a real change in
      what a command returns.
- [ ] Full CI is green, including the integration tests that run against the `redis:7.4-alpine`
      service. Production runs the same image (`docker-compose.prod.yml`).
- [ ] After a deploy, the worker still picks up and finishes a queued job.

## Steps

- [ ] Read the redis-py 7.0 and 8.0 release notes for breaking changes: removed APIs, changed
      defaults (protocol version, response decoding) and typing.
- [ ] Confirm that the locked `rq` (2.12) and `fakeredis` (2.38) support redis-py 8; the
      resolver accepting it proves nothing about behaviour.
- [ ] Fix the eight errors above. `map_identity_router.py` assigns a dict to a variable typed as
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
