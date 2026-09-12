# Anti-scraping: bounding public reads

Mokaair's catalogue is meant to be read. Five locales of guides, food merchants and
hotspot rankings are server-rendered specifically so search engines can index them
([`docs/seo.md`](seo.md)), and a runtime sitemap advertises up to 365 URLs. So the
question this answers is not "how do we keep crawlers out" but "how do we keep the
search engines we want while bounding the wholesale copying we don't".

This document covers what is implemented. The layer that would actually absorb a
determined scrape — request limiting at the edge — is **not** implemented; see
[Known gaps](#known-gaps).

## What is enforced

`PublicReadRateLimitMiddleware` (`apps/api/app/middleware.py`) counts `GET`/`HEAD`
requests under `/api/v1` per source address, in two windows, and refuses what is over.

| Setting | Default | What it does |
| --- | --- | --- |
| `PUBLIC_READ_RATE_LIMIT_MODE` | `observe` | `off`, `observe` (count and log only), `enforce` (refuse) |
| `PUBLIC_READ_IP_LIMIT` | 180 | Burst allowance per window |
| `PUBLIC_READ_IP_WINDOW_SECONDS` | 60 | The burst window |
| `PUBLIC_READ_IP_HOUR_LIMIT` | 2400 | Sustained allowance per hour |

Two windows because they catch different things. The per-minute window stops a crawler
that fetches as fast as it can; the hourly window stops one polite enough to stay under
that and still empty the catalogue by evening.

A refusal is a `429` with `Retry-After`. There is deliberately no `X-RateLimit-Remaining`:
reporting the remaining budget on every response tells a scraper exactly how slowly to go
to avoid being noticed.

### It ships in `observe`

The number that stops a scraper and the number that stops a school, an office or a mobile
carrier behind one NAT address are not known to be far apart until real traffic has been
measured. `observe` counts and records without refusing anything. Move to `enforce` on
evidence from the counters below, not on principle.

### Only forwarded addresses are counted

This is the load-bearing detail. Two different paths reach the API:

- **Browser JSON calls** go through the BFF (`apps/web/app/api/travel/[...path]/route.ts`),
  which forwards the visitor's address as `X-Travel-Client-IP`.
- **Server-rendered pages** call `API_INTERNAL_URL` directly, bypassing the BFF. Those
  loaders now forward the same header via `publicServerHeaders`
  (`apps/web/lib/public-server-fetch.ts`), so a page render is metered against the visitor
  who asked for it rather than against the web container.

A request with no forwarded address is first-party internal traffic and is never counted.
Without that rule, every server render would share one bucket and the site would take
itself down the first time anyone browsed quickly.

The header is only believed when `TRUST_PROXY_CLIENT_IP` is true, which production
requires (`apps/api/app/config.py`). **The edge must strip inbound `X-Travel-Client-IP`
and `X-Forwarded-For` before setting its own**, or a caller can pick its own bucket;
[`ops/nginx/proxy-headers.conf`](../ops/nginx/proxy-headers.conf) is that configuration.

Inside the Compose network nothing reaches the API through nginx at all, and nothing at the
network layer separates our own web container from anything else on the bridge: neither
Compose file declares `networks:`, so addresses are dynamic and the subnet is one flat trust
domain. `INTERNAL_PROXY_TOKEN`, shared by the API and the web container, is what distinguishes
them. Leaving it empty keeps the previous behaviour — set on the API alone, no forwarded
address would be believed at all and every visitor would collapse into one bucket.

### Public reads fail open

`over_named_rate_limit` (`apps/api/app/infra.py`) returns "not over" when Redis cannot be
reached, unlike `enforce_named_rate_limit`, which refuses with a 503. The asymmetry is
deliberate: losing the login guard for the length of a Redis blink is dangerous, while
returning 503 on the public catalogue takes the site down for every reader and every
crawler at once.

## What is declared, not enforced

`apps/web/app/robots.ts` refuses a list of content harvesters — GPTBot, ClaudeBot, CCBot,
Google-Extended, Applebot-Extended, Bytespider, Amazonbot, meta-externalagent,
PerplexityBot, Diffbot.

`Google-Extended` and `Applebot-Extended` are training-only tokens: Googlebot and Applebot
do not consult them when crawling or ranking, so refusing them costs no search visibility.
`ChatGPT-User` and `OAI-SearchBot` are deliberately *not* refused — they fetch on a
person's behalf and cite the source, which is the same bargain a search engine offers.

This stops the crawlers honest enough to read it and nothing else. Volume from the rest is
the rate limit's problem, and the rate limit does not care what a request calls itself.

**There is no User-Agent blocking**, on purpose. A user agent is a string the caller
chooses, so blocking on it filters the honest and misses the rest, while risking real
traffic: `apps/web/e2e/seo.spec.ts` runs the whole suite as `Twitterbot/1.0` with
JavaScript disabled precisely because link previewers and crawlers are traffic we want.

## Reading the counters

Blocked-or-would-block requests are recorded as a daily Redis hash of hashed sources, kept
for seven days, and logged at `WARNING` with the path and window.

```bash
redis-cli --scan --pattern 'abuse:public-read-ip:*'
redis-cli hgetall abuse:public-read-ip:$(date -u +%F)   # hashed source -> hits that day
```

Before moving to `enforce`, look for the shape of the distribution rather than the total.
Many sources with a handful of hits each is ordinary traffic near the line, and means the
threshold is too low. A few sources with thousands is what the limit is for.

## Known gaps

- **Edge rate limiting is written but not known to be applied.** [`ops/nginx/`](../ops/nginx)
  now holds the `limit_req` zones, connection cap and header hygiene, with an installer and
  a verification runbook; CI syntax-checks it. But nginx runs on the host, outside this
  repository and outside any deploy this project performs, so the repo cannot tell you
  whether the running proxy matches those files. The runbook's forged-address check is what
  answers that, and until someone runs it on the host, INF-10 in
  [`security-audit-2026-09.md`](security-audit-2026-09.md) is addressed on paper only.
- **No WAF, CAPTCHA or challenge.** Out of scope by decision: the brief was to bound
  volume without a normal visitor noticing anything.
- **Whole-dataset endpoints are still unpaginated** — `GET /guides/sitemap`,
  `/discovery/suggestions`, `/hotspots/facets`, `/foods/cities`, `/foods/categories`,
  `/guides/topics`. These are hit on ordinary page loads, so tightening their limit would
  hurt readers first; the fix is to make them cheap (shared caching or pagination), not to
  meter them harder.
- **Distributed scraping is not addressed.** Many accounts across many addresses defeats
  per-source counting by construction. That needs per-user read budgets and cross-account
  correlation, which costs considerably more than this does.
