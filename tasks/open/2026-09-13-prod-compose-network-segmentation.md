---
id: 2026-09-13-prod-compose-network-segmentation
title: Production compose has no network segmentation or read-only root
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-13T23:37:47Z
completed_at:
branch:
depends_on: []
scope:
  - docker-compose.prod.yml
  - ops/nginx/README.md
---

# Production compose has no network segmentation or read-only root

## Why

`docker-compose.prod.yml` declares no `networks:`, so every container sits on one default
bridge and can reach every other. `web` can open a socket to `postgres` directly; so can
anything else that ends up on that bridge.

That flat bridge is load-bearing in a way that is easy to miss. `app/infra.py` believes
`X-Travel-Client-IP` from any caller that presents the matching `INTERNAL_PROXY_TOKEN`,
and the comment in `lib/client-address.ts` says why the token exists at all:

> nothing at the network layer separates our own web container from anything else that can
> reach the API: neither Compose file declares `networks:`, so addresses are dynamic and
> the whole bridge is one flat trust domain.

So the shared token is currently standing in for network isolation. It works, and it is
the right belt — but the braces are missing, and per-visitor rate limiting across the
whole API keys off that header.

The containers are otherwise well hardened: non-root, `cap_drop: ALL`,
`no-new-privileges: true`, and only loopback publishes (`127.0.0.1:8090`, `127.0.0.1:8091`).
What is absent is `read_only: true` with an explicit `tmpfs`, and healthchecks on `api`
and `web` — `postgres` and `redis` have them, the two application services do not.

`docs/security-audit-2026-09.md` filed this as INF-06 and API-11, and recommendation #4.

## Definition of done

- [ ] `web` cannot open a connection to `postgres` or `redis`; `api` and the workers still
      can.
- [ ] `api` and `web` have healthchecks, so a container that is up but not serving is
      visible to `docker compose ps` and to the deployment agent's health gate.
- [ ] `read_only: true` on the application containers with whatever `tmpfs` they actually
      need, or a note here naming the service that cannot take it and why.

## Steps

- [ ] Add a `frontend` and a `backend` network. `web` joins `frontend` only; `api` joins
      both; `postgres`, `redis` and the workers join `backend` only.
- [ ] Check what still has to cross: `web` reaches `api` over `API_INTERNAL_URL`, which
      stays inside `frontend`. Server-side rendering calls the API directly — confirm that
      path still resolves after the split.
- [ ] Add `healthcheck` to `api` (`/health`) and `web`. Do not point `api`'s at `/ready`:
      that one fails when Postgres, the schema revision or Redis are unavailable, which is
      a dependency signal, not a liveness one.
- [ ] Try `read_only: true` plus `tmpfs: [/tmp]` on `api` and `web` in staging.
      Next.js standalone writes into `.next/cache` and uvicorn wants a writable `/tmp`;
      find the real set rather than guessing.
- [ ] Re-read `deployment_agent/executor.py::APPLICATION_SERVICES` before changing service
      names or adding one — a service missing from that tuple is never started on an
      agent-managed host, which is how the analytics scheduler and hotspot collector once
      silently stayed off.

## How to verify

```bash
docker compose -f docker-compose.prod.yml config --quiet
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec web sh -c 'nc -z postgres 5432' ; echo "expect non-zero: $?"
docker compose -f docker-compose.prod.yml exec api sh -c 'nc -z postgres 5432' ; echo "expect zero: $?"
docker compose -f docker-compose.prod.yml ps
```

Then exercise the site end to end: sign in, load a trip, load `/explore`, and confirm the
server-rendered pages still reach the API.

## Notes

- Staging first. A wrong network split takes the whole site down at once, and the symptom
  (DNS resolves, connection hangs) looks nothing like a config error.
- This does not remove the need for `INTERNAL_PROXY_TOKEN`; it is defence in depth behind
  it, not a replacement.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
