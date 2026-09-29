---
id: 2026-09-23-google-weather-key-in-url
title: Google Weather still sends the Maps key in the query string and api and worker do not quiet httpx
status: done
priority: P2
area: api
owner: codex-weather-headers
claimed_at: 2026-09-29T09:24:36Z
created_at: 2026-09-23T15:57:49Z
completed_at: 2026-09-29T09:33:18Z
branch: codex/weather-key-headers
depends_on: []
scope:
  - apps/api/app/weather/google.py
  - apps/api/app/main.py
  - apps/api/app/worker.py
  - apps/api/tests/test_api_keys_not_in_urls.py
  - apps/api/tests/test_google_weather.py
---

# Google Weather still sends the Maps key in the query string and api and worker do not quiet httpx

## Why

`2026-09-19-api-keys-in-logged-urls` moved six Google calls from `?key=` to the
`X-Goog-Api-Key` header after the collector logged a YouTube key in plain text.
`app/weather/google.py` was not on its list: it still builds
`params={"key": settings.google_maps_api_key, ...}` for every trip weather lookup and for the
admin connection test, and the source-scan regression test
(`tests/test_api_keys_not_in_urls.py::test_no_google_client_builds_a_key_query_parameter`)
checks only three modules, so nothing fails today.

The api and worker processes never call `logging.basicConfig`, so httpx's INFO line has no
handler there yet. The first `basicConfig`, uvicorn `--log-config` or observability agent
added to those processes writes the Maps key (which also unlocks Places, Routes and Photos)
once per lookup. Ekispert (`trips/routing.py`, `key=`) and ODsay (`apiKey=`) accept keys only
in the query string by vendor design, so they share the latent exposure and can only be
protected on the logging side.

## Definition of done

- [x] `weather/google.py` sends the key as `X-Goog-Api-Key`; no Google client in `app/`
      builds a `"key":` params entry.
- [x] `httpx` and `httpcore` loggers are pinned to WARNING in the api and worker entry
      points, not only in the hotspot collector.
- [x] The source-scan test covers every module that talks to a Google API, so the next client
      cannot slip past it.

## Steps

- [x] Move the key into the header (import `GOOGLE_API_KEY_HEADER` from `hotspots/guides.py`);
      adjust the `test_google_weather.py` fixtures.
- [x] Add `weather/google.py` to the module list in `test_api_keys_not_in_urls.py`, or
      replace the list with a walk over `app/` that looks for `googleapis.com`.
- [x] `main.py` and `worker.py`: set the two logger levels at startup; add a test that asserts
      the level.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_api_keys_not_in_urls.py tests/test_google_weather.py tests/test_trip_weather.py -q
```

## Notes

- 2026-09-29: claimed after checking main `eddcc3ee`, 11 open PRs, 42 remote
  heads and 218 registered worktrees. The five scoped files have no active
  competing implementation. Claim required `--force` only because the older
  2026-09-19 API-key ticket still lists the shared regression test: its code
  merged in PR #561 (`f521b902`), its branch is gone, and it remains open for
  owner credential rotation. That ticket and its outstanding owner steps are
  unchanged; this claim covers only the new Weather/logging implementation.
- Found in the 2026-09-23 security review (finding L2).
- Google API keys are accepted in `X-Goog-Api-Key` across googleapis.com; confirm once
  against the live Weather endpoint before relying on it (the admin connection test is the
  cheapest way).

### Implementation and validation (2026-09-29)

- Weather sets a per-request header in both injected and owned-client paths.
  Existing caller headers are preserved, including the caller's default API key;
  only the request uses the service key. Coordinates, language, units, forecast
  length, timeout, cache and per-operation usage accounting remain unchanged.
- API import and worker startup pin only the two HTTP library loggers to WARNING;
  no root logging configuration is replaced. Uvicorn initializes its loggers
  before loading the app, and RQ later configures only its own loggers.
- The syntax guard discovers Python modules through Google endpoints, the shared
  header or Google settings references. It checks key dictionaries, assignments
  and literal query fragments. Its sole exception is the Ekispert key in that
  provider's `_params` method; a Google sibling in the same file is still checked.
  Fourteen small scanner fixtures exercise discovery and the exception. This is
  a bounded regression guard, not a complete data-flow security proof.
- Regression baseline: **5 failed / 19 passed** on the unchanged code, covering
  Weather query credentials and both entrypoint logging levels. Fixed Weather,
  key-handling, trip-weather, provider-fallback and worker suites: **30 passed**.
  Both Weather client paths produce two real mocked HTTP requests whose INFO
  logs contain no credential; borrowed-client defaults/lifetime, owned-client
  closure, cache hits and usage counters are asserted.
- Existing adjacent logging/settings suites: **143 passed**. Full API Ruff,
  `mypy app` (**443 files**), Linux-targeted `mypy tests` (**329 files**), scoped
  Windows mypy and format checks pass. Independent review found no remaining
  issue; tests restore logger state and avoid replacing cached settings imports.
- Official contract checked on 2026-09-29:
  [Google system parameters](https://docs.cloud.google.com/apis/docs/system-parameters)
  maps `key`/`$key` to `X-Goog-Api-Key`, and the
  [Weather REST reference](https://developers.google.com/maps/documentation/weather/reference/rest)
  identifies both endpoints. No live Weather call, credential read/rotation or
  production operation occurred. The live connection check above remains an
  owner-authorized rollout step; mock transport tests do not establish it.
- Default full Windows test typing has the pre-existing Unix fixture limitation
  fixed separately in draft PR #975; it is not duplicated in this independent PR.
