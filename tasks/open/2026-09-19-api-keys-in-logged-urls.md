---
id: 2026-09-19-api-keys-in-logged-urls
title: Google API keys ride in request URLs and the collector logs them
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-19T08:01:09Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/guides.py
  - apps/api/app/hotspots/scheduler.py
  - apps/api/app/places/router.py
  - apps/api/app/providers/google_travel_impact.py
  - apps/api/tests/test_api_keys_not_in_urls.py
---

# Google API keys ride in request URLs and the collector logs them

## Why

On 2026-09-19, reading `docker compose logs hotspot-collector` on the production host showed lines like
`INFO:httpx:HTTP Request: GET https://www.googleapis.com/youtube/v3/search?key=AIza…&part=snippet…`: the
**full YouTube Data API key in plain text**, once per search, kept by Docker's log driver and readable by
anyone with log access.

Two things combine:

- `apps/api/app/hotspots/scheduler.py` calls `logging.basicConfig(level=logging.INFO)`, and httpx logs
  every request URL at INFO.
- The key travels in the query string. `hotspots/guides.py` does it on three YouTube calls
  (`search`, and `videos` twice), `places/router.py` on the Places photo media call, and
  `providers/google_travel_impact.py` on two Travel Impact Model calls. Google's APIs accept the same
  key in the `X-Goog-Api-Key` header, which httpx does not log.

The Places photo call is server-side and only the `photoUri` reaches the browser, so the key is not
public there. It still reaches any process log that runs httpx at INFO.

## Definition of done

- [ ] No Google API key is sent in a URL query string; each call uses the `X-Goog-Api-Key` header.
- [ ] The collector no longer logs request URLs at INFO (httpx/httpcore at WARNING), or logs them redacted.
- [ ] A regression test fails if any of these clients puts `key=` in a request URL.
- [ ] The owner has rotated the YouTube key, since the old one sits in the retained container logs.
      The Maps and Travel Impact keys too, if their process logs show them.

## Steps

- [ ] Move `key` from `params` to a header in the six calls; keep the request counters and budgets as they are.
- [ ] Quiet httpx in `scheduler.py` next to its `basicConfig`; check the api and worker processes for the same.
- [ ] Add `apps/api/tests/test_api_keys_not_in_urls.py` (mock transport, assert header present and URL has no `key`).
- [ ] After the deploy, `docker compose logs --since 10m hotspot-collector | grep -c 'key=AIza'` is 0.
- [ ] Ask the owner to rotate the keys in Google Cloud and update them in /admin/settings.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_api_keys_not_in_urls.py -q
docker compose -f docker-compose.prod.yml logs --since 30m hotspot-collector | grep -c 'key=AIza'   # on the host, after deploy: 0
```

## Notes

- Found while verifying the 2026-09-19 host steps (claude-opus-5). The key itself is deliberately not
  copied here or anywhere else; read it from /admin/settings when rotating.
- `2026-09-14-redis-py-8-migration` (open, unowned) also lists `hotspots/guides.py`; the changes do not
  touch the same lines.
