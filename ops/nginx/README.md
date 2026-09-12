# Reverse proxy configuration

Production terminates TLS on an nginx that runs on the host, outside any container. This
directory is the version-controlled template for the parts of it that belong to this
project; the host keeps the instance. Nothing here is deployed by CI, exactly like
[`ops/deployer/`](../deployer).

It exists to close two gaps that the application cannot close by itself:

- **Volume.** The API bounds public reads per source ([`docs/anti-scraping.md`](../../docs/anti-scraping.md)),
  but a refused request has still occupied a worker by the time it is refused. The edge is
  where a flood is actually cheap to turn away.
- **Provenance.** That per-source counting reads `X-Travel-Client-IP`. If the proxy does not
  discard the caller's own copy of that header and set its own, a caller picks which bucket
  it lands in and the counting means nothing.

| File | Installs to | Contents |
| --- | --- | --- |
| `10-rate-limit.conf` | `conf.d/mokaair-rate-limit.conf` | The `limit_req` / `limit_conn` zones (http context only) |
| `proxy-headers.conf` | `snippets/mokaair-proxy-headers.conf` | Header hygiene, included by every proxying location |
| `mokaair.conf.example` | `sites-available/mokaair.conf` | Server blocks. Seeded once; yours thereafter |
| `ci-validate.conf` | — | A self-contained wrapper so CI can run `nginx -t` |
| `install.sh` | — | Idempotent installer |

## Install

```bash
sudo bash ops/nginx/install.sh
```

Then edit every `EDIT` marker in `/etc/nginx/sites-available/mokaair.conf` (server names and
certificate paths), link it into `sites-enabled/`, and:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

The installer never reloads nginx itself. Re-run it after upgrading a release: it overwrites
the two files this project owns and leaves your site file alone.

## Verify

### The forged address is ignored

This is the check that matters. Everything else here is a convenience; this one is the
reason the directory exists.

The application's counters are keyed `rate:{namespace}:{sha256(identifier)}`
(`apps/api/app/infra.py`), so you can ask Redis directly whether a forged address managed to
open a bucket of its own:

```bash
curl -s -o /dev/null \
  -H 'X-Travel-Client-IP: 198.51.100.1' \
  -H 'X-Forwarded-For: 198.51.100.1' \
  https://example.com/zh-TW/foods

key="rate:public-read-ip-minute:$(python3 -c "import hashlib;print(hashlib.sha256(b'198.51.100.1').hexdigest())")"
docker compose -f docker-compose.prod.yml exec redis redis-cli -a "$REDIS_PASSWORD" EXISTS "$key"
```

`0` passes. `1` means the forged header was believed the whole way through and per-source
counting can be bypassed. (`PUBLIC_READ_RATE_LIMIT_MODE` must be `observe` or `enforce`;
`observe` counts without refusing, which is enough for this check.)

### The limits apply to pages but not to assets

```bash
for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' https://example.com/zh-TW; done | sort | uniq -c
for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' https://example.com/_next/static/<a real filename>; done | sort | uniq -c
```

The first should show 429s once the burst is spent; the second should be all 200. Then check
who is actually being limited — if it is Googlebot, the rate is too low:

```bash
sudo grep 'limiting requests' /var/log/nginx/error.log | tail -20
```

### The canonical-origin redirect still works

Sign-in breaks permanently if the site answers on more than one hostname, because the OAuth
flow cookie is host-only. Test an OAuth path, not `/`: a redirect covering only the site root
would still break sign-in and testing `/` cannot tell the two apart.

```bash
curl -sSI https://www.example.com/api/auth/oauth/google/start | grep -iE '^HTTP|^location'
# expect 301 -> https://example.com/api/auth/oauth/google/start
```

### Whether a CDN is in front

The rate limits key on `$remote_addr`, which is the visitor only while nginx is the
internet-facing hop. Behind a CDN it becomes the CDN's egress address and every visitor
shares a handful of buckets.

```bash
curl -sI https://example.com | grep -iE '^(server|cf-ray|cf-cache-status|via|x-served-by):'
```

A `Server:` naming nginx means you are directly exposed and the `real_ip` block in the site
config must stay commented out. A `cf-ray` header, or a `Server:` naming a CDN, means it must
be uncommented and filled in before any of these limits mean anything.

## Trust boundary

- **These files have only been syntax-checked, never run on a real host by anyone who
  wrote them.** CI runs `nginx -t` over the snippets through `ci-validate.conf`; the site
  template is not covered by it, because it names certificates that exist only on the host,
  and was checked structurally instead. Rehearse on staging before applying to production. This is the
  same caveat this repository records for `ops/deployer/install.sh`.
- The rate limits bound volume per address. They do not identify anyone, and they do not
  stop a distributed crawl: many addresses each staying under the limit is not something
  this layer can see.
- Header hygiene stops an *outside* caller choosing its rate-limit bucket. It does nothing
  about anything already inside the Compose network, which reaches the API without passing
  through nginx at all; that is what `INTERNAL_PROXY_TOKEN` is for.
- Thresholds are deliberately loose. Corporate NAT and carrier-grade NAT put many real
  people behind one address, and a wrong refusal here breaks a whole page rather than one
  API call. Tighten only against what the error log actually shows.
- The API on `127.0.0.1:8090` is not proxied here and must not be. Reaching it directly
  skips the BFF's same-origin check and header allowlist.

## Open question

`docs/security-audit-2026-09.md` §6 asks how the LINE webhook reaches FastAPI, since the
BFF's origin check and header allowlist would reject it. The answer is that it does not go
through the BFF proxy at all. `apps/web/app/api/line/webhook/route.ts` is a Next route
handler of its own: it rejects a request with no `x-line-signature`, caps the streamed body,
and forwards the raw bytes and that header to `POST /api/v1/line/webhook`, where the
signature is actually verified. So it arrives on the same upstream as every other page,
which is why this config gives it a location of its own -- exempt from rate limiting -- and
not a separate route.
