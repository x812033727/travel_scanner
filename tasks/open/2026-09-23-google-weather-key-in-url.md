---
id: 2026-09-23-google-weather-key-in-url
title: Google Weather still sends the Maps key in the query string and api and worker do not quiet httpx
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-23T15:57:49Z
completed_at:
branch:
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

- [ ] `weather/google.py` sends the key as `X-Goog-Api-Key`; no Google client in `app/`
      builds a `"key":` params entry.
- [ ] `httpx` and `httpcore` loggers are pinned to WARNING in the api and worker entry
      points, not only in the hotspot collector.
- [ ] The source-scan test covers every module that talks to a Google API, so the next client
      cannot slip past it.

## Steps

- [ ] Move the key into the header (import `GOOGLE_API_KEY_HEADER` from `hotspots/guides.py`);
      adjust the `test_google_weather.py` fixtures.
- [ ] Add `weather/google.py` to the module list in `test_api_keys_not_in_urls.py`, or
      replace the list with a walk over `app/` that looks for `googleapis.com`.
- [ ] `main.py` and `worker.py`: set the two logger levels at startup; add a test that asserts
      the level.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_api_keys_not_in_urls.py tests/test_google_weather.py tests/test_trip_weather.py -q
```

## Notes

- Found in the 2026-09-23 security review (finding L2).
- Google API keys are accepted in `X-Goog-Api-Key` across googleapis.com; confirm once
  against the live Weather endpoint before relying on it (the admin connection test is the
  cheapest way).
