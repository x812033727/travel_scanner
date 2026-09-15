# Anti-scraping: bounding public reads

Mokaair's catalogue is meant to be read. Five locales of guides, food merchants and
hotspot rankings are server-rendered specifically so search engines can index them
([`docs/seo.md`](seo.md)), and a runtime sitemap advertises up to 365 URLs. So the
question this answers is not "how do we keep crawlers out" but "how do we keep the
search engines we want while bounding the wholesale copying we don't".

This document covers what is implemented. The layer that would actually absorb a
determined scrape — request limiting at the edge — is **not** implemented; see
[Known gaps](#known-gaps).

It also covers the other half of bounding a caller, which is not about reading at all:
[what one account can spend](#bounding-what-a-caller-can-spend) on the AI planner, where the
request is cheap to make and expensive to serve. Same counters, opposite failure mode — a
read we cannot count still renders, a paid call we cannot count does not happen.

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

## Bounding what a caller can spend

Reads are bounded because copying the catalogue is cheap for whoever does it. AI itinerary
planning is the opposite problem: every call is cheap for the caller and expensive for us,
because `AIItineraryPlanner` fails over across the whole provider roster and Gemini repairs
its own invalid JSON once, so a single request can be several billed completions at
`AI_PLANNER_MAX_OUTPUT_TOKENS` each.

Creating a blank trip was the widest door. It charges the usage ledger nothing by design
(planning at creation is free), and the twenty-saved-trips cap it sits behind is undone by
one `DELETE /trips/{id}` -- so create, delete, create was an unbounded loop. Every
user-facing path onto the planner now goes through one door, `plan_within_budget`
(`apps/api/app/ai/itinerary.py`), which counts before it spends.

| Setting | Default | What it does |
| --- | --- | --- |
| `AI_PLANNER_USER_BUDGET` | 40 | Planner attempts per account per window |
| `AI_PLANNER_IP_BUDGET` | 120 | Planner attempts per source address per window |
| `AI_PLANNER_USER_BUDGET_WINDOW_SECONDS` | 3600 | The window both use |

Per address as well as per account, because an account costs nothing to mint: `/auth/register`
returns a token immediately, so per account alone is `AUTH_REGISTER_IP_LIMIT` budgets an hour
from one machine. The account is counted first and the address only if the account is still
inside its own budget, so one caller on an office network cannot spend their colleagues'
share on requests that were never going to run.

### Over the budget, planning degrades instead of refusing

This is the difference from every other limit in this document. On trip creation
(`ai_draft`), `/itinerary/preview` and the deprecated `/itinerary/generate`, a spent budget
does not produce a `429`; it produces the itinerary the deterministic catalogue planner
builds, which is the same plan a total provider outage produces. Refusing to create a trip is
the harshest outcome available and teaches the caller to retry; a plainer first draft costs
nothing and teaches them nothing. `apps/api/app/ai/trip_parser.py` already makes the same
trade when its own gate closes.

It says which of the two happened. A budget degrade carries `planner_budget_reached`, not
`planner_fallback_used`, because the badge for a fallback reads "AI is temporarily
unavailable" and that is false when a budget, not the roster, is what ran out.

`POST /trips/{id}/intents` is the exception. A refinement is the traveller's sentence, and
the catalogue planner never reads one, so a catalogue plan there would be the old itinerary
re-sorted and presented as their request. A spent budget answers `429`
`planner_budget_reached` instead, and the route still gives its two intent fair-use slots
back, because the traveller got nothing; the planner budget itself is not given back. A trip
with no plannable places answers `422` `itinerary_exact_locations_required` on the same
route, since that is a property of the trip and waiting out a window would not change it.

### A count for an attempt that reached the roster is never refunded

The fair-use limiters around this one give a slot back when every provider failed
(`trips/intents.py`), which is right: an outage should not also cost a traveller their hour.
It is also why they cannot be the ceiling -- a caller who can provoke a failure gets the
calls attempted and the budget handed back, indefinitely. This counter is never refunded for
an attempt that reached the provider roster, so it bounds the attempts themselves and the
refunds above stay as they are.

The one refund is when the address budget turns an attempt away. The account is counted
first, so by then it has already counted that attempt, and that count goes back: no provider
was asked, and keeping it would let a busy NAT address spend every traveller's own hour on
attempts that never cost anything.

### An unreachable counter counts as spent

`budget_spent` (`apps/api/app/infra.py`) fails closed, unlike `over_named_rate_limit` which
guards the public reads above and fails open. A window we cannot count must not become an
unmetered hour against a provider billed per call, and "take Redis down" is a state worth
assuming someone would try to produce. It costs availability nothing, because the caller
still gets an itinerary.

### Requests that can only come back empty are not sent at all

Separate from the budget, and it removes more waste than the budget does for the cheapest
attack. Every item a provider returns must name a `candidate_key` the request supplied, or
`normalize_draft` drops it -- so a request with no candidates can only come back empty,
after the whole roster has been asked and billed. `_load_ai_planner_candidates` returns an
empty list the moment `match_destination` misses, which made a destination the catalogue
does not know ("Narnia") the cheapest way there has ever been to spend four vendors at once.
Those requests now go straight to the catalogue and are not counted, because nothing was
spent.

### Reading these counters

```bash
redis-cli hgetall abuse:ai-planner-llm-user:$(date -u +%F)
redis-cli hgetall abuse:ai-planner-llm-ip:$(date -u +%F)
```

Same reading as above: many sources with a few hits each means the number is too low; a few
with hundreds is what it is for.

## Known gaps

- **Edge rate limiting is written but not known to be applied.** [`ops/nginx/`](../ops/nginx)
  now holds the `limit_req` zones, connection cap and header hygiene, with an installer and
  a verification runbook; CI syntax-checks it. But nginx runs on the host, outside this
  repository and outside any deploy this project performs, so the repo cannot tell you
  whether the running proxy matches those files. The runbook's forged-address check is what
  answers that, and until someone runs it on the host, INF-10 in
  [`security-audit-2026-09.md`](security-audit-2026-09.md) is addressed on paper only.
- **Account farming is bounded, not closed.** `AI_PLANNER_IP_BUDGET` is what stands between
  a scripted attacker and `AUTH_REGISTER_IP_LIMIT` fresh accounts an hour, each with its own
  planner budget. That bounds each address, not the attacker: registration is not email
  verified, and `AUTH_REGISTER_IP_LIMIT` lets one address mint enough accounts to reach
  `AI_PLANNER_IP_BUDGET` (three at the defaults, 120 / 40), so the residual ceiling for
  someone with many addresses is `AI_PLANNER_IP_BUDGET` attempts per address per window
  (120 an hour by default) times however many addresses they have, not the per-account
  budget times that number. Distinguishing that from a large office is the same measurement
  problem as the read limits, and the counters above are how it gets answered.
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
