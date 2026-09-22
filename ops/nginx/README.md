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
| `upstream-keepalive.conf` | `snippets/mokaair-upstream-keepalive.conf` | Connection pool to Next.js, included inside `upstream mokaair_web` |
| `mokaair.conf.example` | `sites-available/mokaair.conf`, on a fresh host only | Server blocks. On a host that already has a site file, whatever its name, a merge source and not a drop-in |
| `ci-validate.conf` | — | A self-contained wrapper so CI can run `nginx -t` |
| `install.sh` | — | Idempotent installer |

## Install

```bash
sudo bash ops/nginx/install.sh
```

The installer overwrites the three files this project owns, never reloads nginx, and looks at
what is enabled before it goes near the site file. It says which of these two cases it found:

- **Nothing enabled looks like this site.** It seeds `sites-available/mokaair.conf` from
  `mokaair.conf.example`. Edit every `EDIT` marker (server names and certificate paths), link
  the file into `sites-enabled/`, then test and reload.
- **The site is already enabled from a file of its own.** Production is
  `sites-enabled/mokaair.com -> sites-available/mokaair.com`. The installer seeds nothing and
  prints that file. Merge `mokaair.conf.example` into it; do not copy the example over it. The
  example's header lists what the host copy has that the example does not (the ACME webroot
  certbot renews through, the extra domains and their certificates, inline TLS parameters,
  `default_server`), and all of it has to survive the merge. A second site file next to the
  enabled one is what made the 2026-09-12 rollout a no-op: its `EDIT` markers were edited,
  `nginx -t` passed, the reload succeeded, and nginx had not read a byte of it.

In both cases the site's main `server {}` block needs these four lines. The example carries
them; a host file merged before they existed does not. Why the `error_log` pair, and what goes
wrong without it, is under [the rate-limit log](#the-limits-apply-to-pages-but-not-to-assets)
below; the `access_log` pair is under [crawl-control fetches](#crawl-control-fetches-are-visible).

```nginx
error_log /var/log/nginx/error.log error;
error_log /var/log/nginx/mokaair-limit.log warn;
access_log /var/log/nginx/mokaair-limited.log mokaair_limited if=$mokaair_is_limited;
access_log /var/log/nginx/mokaair-crawl.log combined if=$mokaair_is_crawl_control;
```

Then:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

Re-run the installer after upgrading a release: it overwrites the three files this project owns
and leaves your site file alone. A site file written before `upstream-keepalive.conf` existed
has `keepalive 32;` in its upstream block; replace that line with the `include` from
`mokaair.conf.example`, or the new snippet is installed and never read. The installer prints a
reminder while no enabled config includes it.

## Verify

The order below is the deployment order. The edge goes live before the application release
that reads the headers it sets, so the first check needs nothing but nginx, and the second
needs the application -- and says so, instead of passing, while the application is not there
yet. Every check in this section was rewritten after a rollout on which all of them passed and
none of them had proved anything (task `2026-09-12-nginx-deploy-checks-false-pass`). A check
that cannot fail is the one thing this section must not contain.

### 1. The forged address is discarded at the edge

This is the reason the directory exists: nginx must drop the caller's `X-Travel-Client-IP`,
`X-Forwarded-For` and `X-Real-IP` and send its own. The proof is a second nginx process that
reads the **installed** snippet and proxies to an echo server. It touches neither the live
configuration nor the application, so it can run the moment `install.sh` has put the snippet
on disk -- before the reload, and before any application release. As root on the host:

```bash
ss -ltn '( sport = :9080 or sport = :9081 )'    # both ports must be free
mkdir -p /root/nginxtest && cd /root/nginxtest

cat > test.conf <<'NGINX'
# An isolated instance: its own pid file (without one it would overwrite the live nginx's
# /run/nginx.pid), its own log and temp paths, one location, the installed snippet.
pid       /root/nginxtest/nginx.pid;
error_log /root/nginxtest/error.log warn;
events {}
http {
    access_log off;
    client_body_temp_path /root/nginxtest/client_body;
    proxy_temp_path       /root/nginxtest/proxy;
    fastcgi_temp_path     /root/nginxtest/fastcgi;
    uwsgi_temp_path       /root/nginxtest/uwsgi;
    scgi_temp_path        /root/nginxtest/scgi;
    server {
        listen 127.0.0.1:9080;
        location / {
            include /etc/nginx/snippets/mokaair-proxy-headers.conf;
            proxy_pass http://127.0.0.1:9081;
        }
    }
}
NGINX

# The echo server answers every GET with the request headers it received, one per line.
cat > echo.py <<'PY'
import http.server
class Echo(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = "".join(f"{k}: {v}\n" for k, v in self.headers.items()).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *_):
        pass
http.server.HTTPServer(("127.0.0.1", 9081), Echo).serve_forever()
PY
python3 echo.py & echo_pid=$!

nginx -t -c /root/nginxtest/test.conf -p /root/nginxtest
nginx -c /root/nginxtest/test.conf -p /root/nginxtest
curl -s -H 'X-Travel-Client-IP: 198.51.100.1' -H 'X-Forwarded-For: 198.51.100.1' \
     -H 'X-Real-IP: 198.51.100.1' http://127.0.0.1:9080/ | tee upstream-saw.txt

nginx -c /root/nginxtest/test.conf -p /root/nginxtest -s quit; kill "$echo_pid"
```

Expected output. The two address lines and the missing `X-Travel-Client-IP` are what the
2026-09-12 run on `hostinger2` (nginx 1.28.3) recorded; the rest follows from the snippet and
curl's defaults, and the header order and curl version are incidental:

```
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Forwarded-Proto: http
Host: 127.0.0.1
User-Agent: curl/8.5.0
Accept: */*
```

Three things make that a pass, and this decides all three at once:

```bash
if ! grep -q '198.51.100.1' upstream-saw.txt \
   && ! grep -qi '^x-travel-client-ip:' upstream-saw.txt \
   && [ "$(grep -ciE '^x-(forwarded-for|real-ip): 127.0.0.1$' upstream-saw.txt)" = 2 ]; then
  echo PASS
else
  echo FAIL
fi
```

The forged value appears nowhere: replaced, not appended, which is what
`$proxy_add_x_forwarded_for` would have done. `X-Travel-Client-IP` is absent altogether, not
present and empty; an empty `proxy_set_header` value removes the header. And both address
headers carry the connection's own address, which is what the application's per-source counting
will read. A `FAIL` means the snippet on disk is not the one in this directory:
`cmp ops/nginx/proxy-headers.conf /etc/nginx/snippets/mokaair-proxy-headers.conf` says where.

This proves the snippet. It does not prove that every proxying location in the live site
includes it, which is a separate way to lose the property, so count both in the loaded
configuration -- the two numbers must be equal:

```bash
sudo nginx -T 2>/dev/null | grep -cE '^\s*include\s+\S*mokaair-proxy-headers\.conf;'
sudo nginx -T 2>/dev/null | grep -cE '^\s*proxy_pass\s'
```

### 2. The forged address opens no counter

The application keys its counters `rate:{namespace}:{sha256(identifier)}`
(`apps/api/app/infra.py`), and `PublicReadRateLimitMiddleware` writes
`rate:public-read-ip-minute:…` for the address the BFF forwarded to it. So Redis can say
whether a forged address managed to open a bucket of its own -- **but only once something is
writing those keys.** The middleware and this nginx configuration shipped in the same pull
request (#411) and the edge is meant to go live first, so at the natural moment to run this
the answer is `0` whatever nginx does. On 2026-09-12 the edge went live while production still
ran #406, `EXISTS` returned `0`, and the check "passed". It therefore has two preconditions, and
each one fails out loud.

**Is anything counting?** The setting reaches the container through `env_file`:

```bash
cd /srv/travel-scanner/current
docker compose -f docker-compose.prod.yml exec -T api sh -c 'printenv PUBLIC_READ_RATE_LIMIT_MODE' \
  || echo 'NOT YET: PUBLIC_READ_RATE_LIMIT_MODE is not in the api container environment. This check cannot be done until a release carrying PublicReadRateLimitMiddleware runs with it set; check 1 is the proof until then.'
```

`observe` or `enforce` means go on (`observe` counts without refusing, which is enough). `off`,
or the `NOT YET` line, means stop here and write down that this check has not been done: the
Redis command below would print `0` now and read as a pass. A value proves that the variable
reached the container, not yet that the code reading it is what is running; the second
precondition covers that.

**Was this very request counted?** Send one request carrying the forged headers, then ask for
two keys: the one for the address nginx actually saw, which must exist, and the forged one,
which must not. The minute key expires after `PUBLIC_READ_IP_WINDOW_SECONDS` (60 s by default),
so run the block as one:

```bash
stamp=$(date +%s)
curl -s -o /dev/null -H 'X-Travel-Client-IP: 198.51.100.1' -H 'X-Forwarded-For: 198.51.100.1' \
     -H 'X-Real-IP: 198.51.100.1' "https://example.com/zh-TW/foods?edge=$stamp"
me=$(sudo grep -F "edge=$stamp" /var/log/nginx/access.log | tail -n 1 | awk '{print $1}')   # what nginx saw, hence what it forwarded
key() { python3 -c 'import hashlib, sys; print("rate:public-read-ip-minute:" + hashlib.sha256(sys.argv[1].encode()).hexdigest())' "$1"; }
rexists() { docker compose -f docker-compose.prod.yml exec -T redis sh -c 'REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli EXISTS "$1"' _ "$1"; }
echo "mine ($me): $(rexists "$(key "$me")")   forged: $(rexists "$(key 198.51.100.1)")"
```

`mine: 1   forged: 0` is the pass. `mine: 0` means nothing counted this request -- the running
release predates the setting, the mode is `off`, the forwarded address was not believed
(`TRUST_PROXY_CLIENT_IP`, or `INTERNAL_PROXY_TOKEN` set on one side only), or the page did not
reach `/api/v1` -- and the `forged: 0` next to it proves nothing; stop and find out which.
`forged: 1` means the forged header was believed the whole way through and per-source counting
can be bypassed.

### The limits apply to pages but not to assets

```bash
for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' https://example.com/zh-TW; done | sort | uniq -c
for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' https://example.com/_next/static/<a real filename>; done | sort | uniq -c
```

The first should show 429s once the burst is spent (2026-09-12: 72 × 200 and 128 × 429); the
second should be all 200 (200 × 200 that day). Then check who is actually being limited -- if
it is Googlebot, the rate is too low.

**That needs a log that accepts `warn`.** `10-rate-limit.conf` sets `limit_req_log_level warn`,
which names a level and not a destination, and the stock Debian/Ubuntu `nginx.conf` says
`error_log /var/log/nginx/error.log;` -- no level, which means `error`, one step above `warn`.
So every limiting event is dropped before it is written. On 2026-09-12 that was 200 requests
and 128 refusals, all of them in `access.log` and `error.log` never touched, and
`grep 'limiting requests' /var/log/nginx/error.log` returned nothing and looked like "nobody
is being limited". The site's main `server {}` block must carry both of these lines. They are
in `mokaair.conf.example`; a host file merged before they existed has to be given them:

```nginx
error_log /var/log/nginx/error.log error;
error_log /var/log/nginx/mokaair-limit.log warn;
```

Both, because a server-level `error_log` replaces the inherited one rather than adding to it:
with the second line alone this server's real errors would stop reaching `error.log`. The
stock `/etc/logrotate.d/nginx` rotates `/var/log/nginx/*.log`, so the new file needs no
rotation of its own. Confirm the lines are loaded, then count. The number of new
`limiting requests` lines must equal the number of 429s you just received:

```bash
sudo nginx -T 2>/dev/null | grep -c 'mokaair-limit.log'      # at least 1
before=$(sudo grep -c 'limiting requests' /var/log/nginx/mokaair-limit.log 2>/dev/null || true)
codes=$(seq 1 80 | xargs -P 8 -I{} curl -s -o /dev/null -w '%{http_code}\n' https://example.com/zh-TW)
after=$(sudo grep -c 'limiting requests' /var/log/nginx/mokaair-limit.log || true)
printf '%s\n' "$codes" | sort | uniq -c
echo "429s: $(printf '%s\n' "$codes" | grep -c '^429$')   logged: $(( ${after:-0} - ${before:-0} ))"   # equal, unless someone else was limited meanwhile
sudo tail -n 20 /var/log/nginx/mokaair-limit.log
```

A line there names the zone, the client address, the request and the host, but not the user
agent. `mokaair-limited.log` is the same events with the agent, written by the first of the
two `access_log` lines above; do not reach for `access.log`, which this server no longer
writes.

### Crawl-control fetches are visible

A server-level `access_log` replaces the inherited one rather than adding to it, so the moment
`mokaair-limited.log` went into the server block this server stopped recording anything that
was not refused. That is a deliberate trade for pages and a bad one for `/ads.txt`,
`/robots.txt`, `/sitemap.xml`, `/llms.txt` and `/sitemaps/`: every question ever asked about
those five is "did the crawler come, and what did it get". On 2026-09-22 AdSense reported this
site's `ads.txt` as not found, every check from outside said the file was correct and fast, and
the most recent fetch anyone could point at was nine days old -- there was no way to tell a
failed crawl from a stale status. The second `access_log` line is that record; two directives
at the same level both apply, so it adds a log rather than replacing the refusals one.

```bash
curl -s -o /dev/null -w '%{http_code}
' https://example.com/ads.txt      # expect 200
sudo tail -n 3 /var/log/nginx/mokaair-crawl.log                           # the fetch, with its User-Agent
sudo grep ' /ads.txt ' /var/log/nginx/mokaair-crawl.log | grep -i google  # what Google actually got
```

`/ads.txt` has a `location` of its own for the same reason `/robots.txt` does: a 429 is not a
"slow down" to Google's ads.txt fetcher, it is the site reporting that it has no `ads.txt` at
all. It needs its own exemption rather than the crawler zone, because that fetcher is
`Google-Adstxt`, whose addresses Google publishes in `special-crawlers.json` and not in the
`googlebot.json` ranges `05-crawler-ranges.conf` is generated from -- so it is not a verified
crawler here and would otherwise be counted in the page budget by address, like a visitor.

### The canonical-origin redirect still works

Sign-in breaks permanently if the site answers on more than one hostname, because the OAuth
flow cookie is host-only. Test an OAuth path, not `/`: a redirect covering only the site root
would still break sign-in and testing `/` cannot tell the two apart.

```bash
curl -sSI https://www.example.com/api/auth/oauth/google/start | grep -iE '^HTTP|^location'
# expect 301 -> https://example.com/api/auth/oauth/google/start
```

### Idle connections to Next.js are closed by nginx, not by Next.js

When the Next.js server is the one to close an idle pooled connection, nginx now and then sends a
request down a connection that is already gone. A GET is retried without anyone noticing; a POST
is not, and the browser gets a 502 while the error log says `upstream prematurely closed
connection`. Check both halves, because each is applied by a different route:

```bash
# The server's idle timeout, from KEEP_ALIVE_TIMEOUT in docker-compose.prod.yml (reaches the host
# with a deploy). timeout=5 means the container still runs with Node's default.
curl -sI http://127.0.0.1:8091/ | grep -i '^keep-alive:'        # expect timeout=65

# nginx's idle timeout, from this directory (reaches the host with install.sh, the include, a reload).
sudo nginx -T 2>/dev/null | grep -E 'mokaair-upstream-keepalive|keepalive_timeout 4s'
```

`nginx -T` reads the files on disk, not what the running workers loaded, so also watch one pooled
connection end. Whichever side closes a TCP connection first holds it in TIME-WAIT for a minute:

```bash
curl -s -o /dev/null https://example.com/zh-TW
ss -tn state established '( dport = :8091 )'    # note nginx's local port(s)
sleep 8
ss -tan '( dport = :8091 )'    # -a matters: without it ss hides TIME-WAIT
```

The same local port in `TIME-WAIT` means nginx closed it: the nginx half is live. Still `ESTAB`
means nginx keeps idle connections longer than 8 seconds, so its half is not. Gone altogether means
Next.js closed it first, which is exactly the race; neither half is in effect.

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

- **Applied to production once, by hand, on 2026-09-12** (`hostinger2`, nginx 1.28.3): the
  three owned files through `install.sh`, the server blocks merged into the host's
  `sites-available/mokaair.com`. The numbers quoted in the checks above are from that run; the
  record, including where the previous `/etc/nginx` was backed up, is in task
  `2026-09-12-nginx-deploy-checks-false-pass`. CI runs `nginx -t` over the snippets through
  `ci-validate.conf`; the site template is not covered by it, because it names certificates
  that exist only on the host, and was checked structurally instead. Rehearse a merge on
  staging, and run check 1 against the installed snippet, before reloading production. This is
  the same caveat this repository records for `ops/deployer/install.sh`.
- The rate limits bound volume per address. They do not identify anyone, and they do not
  stop a distributed crawl: many addresses each staying under the limit is not something
  this layer can see.
- Header hygiene stops an *outside* caller choosing its rate-limit bucket. It does nothing
  about anything already inside the Compose network, which reaches the API without passing
  through nginx at all; that is what `INTERNAL_PROXY_TOKEN` is for.
- Thresholds are deliberately loose. Corporate NAT and carrier-grade NAT put many real
  people behind one address, and a wrong refusal here breaks a whole page rather than one
  API call. Tighten only against what `mokaair-limit.log` actually shows.
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
