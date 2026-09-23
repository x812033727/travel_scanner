---
id: 2026-09-23-internal-proxy-token-required-in-production
title: Production accepts forwarded client addresses without the internal proxy token
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-23T15:57:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/config.py
  - apps/api/app/infra.py
  - apps/api/tests/test_public_read_rate_limit.py
  - apps/api/tests/test_security_config.py
  - .env.example
  - docs/anti-scraping.md
---

# Production accepts forwarded client addresses without the internal proxy token

## Why

`app/infra.py::_from_our_proxy` returns `True` whenever `INTERNAL_PROXY_TOKEN` is empty,
`docker-compose.prod.yml` passes `${INTERNAL_PROXY_TOKEN:-}` to both `api` and `web`, and
`Settings.validate_api_serving_security()` requires `TRUST_PROXY_CLIENT_IP=true` in production
but never requires the token. A production host whose `.env` never set the token therefore
believes `X-Travel-Client-IP` from every caller that can reach the API: any container on the
flat compose bridge and any process on the host (the API also listens on `127.0.0.1:8090`).
nginx strips the header from the internet (`proxy-headers.conf`), so the exposure is on-host
only, but it silently turns per-visitor metering on the AI planner, login and the public reads
into "pick your own bucket".

The 2026-09-13 review stated that three conditions were required (trust flag, token match,
valid IP). The token match is only required once a token exists. The done note in
`tasks/done/2026-09-12-edge-rate-limit-and-header-hygiene.md` chose the empty default on
purpose, because a token set on one side only collapses every visitor into one bucket. That
outage is now the cheaper failure: a startup refusal is loud and immediate, a missing token is
invisible.

## Definition of done

- [ ] An API process started with `APP_ENV=production` and an empty `INTERNAL_PROXY_TOKEN`
      refuses to start with a message that names the variable, like the other
      `validate_api_serving_security` refusals.
- [ ] The production host has the token set for both `api` and `web` before the change
      deploys, so the refusal never fires there.
- [ ] `.env.example` and `docs/anti-scraping.md` say the token is required in production.

## Steps

- [ ] `config.py`: in `validate_api_serving_security`, append an error when
      `self.production and not self.internal_proxy_token` (minimum 32 characters, the same
      bar as `APP_SECRET_KEY`).
- [ ] `infra.py`: keep the empty-token pass-through for development, but log once at startup
      when it is in effect.
- [ ] Tests: production settings without the token raise; with a 32+ character token they
      pass; a request with the wrong token still gets `None` from `forwarded_client_ip`.
- [ ] Before merging: confirm the host env file has the token for both services (a read-only
      `grep -c INTERNAL_PROXY_TOKEN` on the env file), and generate one if it is missing.
      Read the `deploy` skill first; the env file lives outside the repository.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_public_read_rate_limit.py tests/test_security_config.py -q
```

After the deploy, `docker compose -f docker-compose.prod.yml logs --since 5m api | grep -c "without our proxy token"`
should stay 0 under normal traffic.

## Notes

- Found in the 2026-09-23 security review (`docs/security-review-2026-09-23.md`, finding M1).
- `docker-compose.prod.yml` is deliberately outside this scope:
  `2026-09-13-prod-compose-network-segmentation` holds it. The `:-` default there becomes
  harmless once the API refuses to start without the value.
