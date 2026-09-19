---
id: 2026-09-19-edge-rate-limit-refuses-search-crawlers
title: Edge rate limit refuses search crawlers with 429
status: done
priority: P2
area: ops
owner: claude-opus-5
claimed_at: 2026-09-19T14:05:00Z
created_at: 2026-09-19T13:55:14Z
completed_at: 2026-09-19T17:13:22Z
branch: claude/google-indexing-issues-efbfb9
depends_on: []
scope:
  - tools/nginx-crawler-ranges.mjs
  - tools/nginx-crawler-ranges.test.mjs
---

# Edge rate limit refuses search crawlers with 429

## Why

`location /` carries `limit_req zone=mokaair_content_pages burst=20 nodelay` at 5r/s and
answers refusals with 429, and nothing in the config could tell a search engine from anyone
else. Measured against production on 2026-09-19: 40 concurrent requests produced 17 × 429.
`/robots.txt`, `/sitemap.xml` and the eleven sitemap children fell under the same catch-all
budget, so a crawler could be refused the very files that tell it what to crawl.

**Correction to the original premise, which matters more than the fix.** The first pass at
this read `zgrep -hi googlebot access.log* | awk '$9==429'`, got 20, and concluded Googlebot
was being throttled. That was wrong, and wrong in the exact way the fix below is designed
against — it trusted the User-Agent string. Broken down by client address:

| Address | 429s | What it actually is |
| --- | --- | --- |
| `111.251.215.82` | 13 | the machine running the audit, sending `-A Googlebot` |
| `136.112.17.120` | 7 | a credential scanner spoofing the Googlebot UA |

The scanner's requests were `/config/env/aws_credentials.env`, `/.github/.env`,
`/ssl/localhost.key`, `/.env.development?import&raw`, `/@fs/proc/self/cmdline?raw??`.
Googlebot does not ask for those. The 429s it received were the limiter working correctly.

Bing addresses `40.77.167.4` and `52.167.144.169` show **9 × 200 each and no 429 at all**.

**So no real search engine was being refused, and this was not a cause of the indexing
problem.** It stays worth doing as a latent risk — the limiter still cannot recognise a
crawler, and crawl rate rises when a site gains indexable pages — but it is P2, not P1, and
the indexing work belongs in `2026-09-19-home-page-renders-as-a-skeleton` and
`2026-09-19-orphan-pages-hotspots-foods-and-explore`.

## Definition of done

- [x] verified search engines are not counted against the page budget
- [x] the exemption cannot be obtained by setting a User-Agent
- [x] `/robots.txt`, `/sitemap.xml`, `/sitemaps/*` and `/llms.txt` are never rate limited
- [x] "was it a crawler that got refused?" is answerable with one grep
- [x] ordinary traffic is still limited
- [x] the same changes are merged into `ops/nginx/` in the repository (#568)

## Steps

- [x] `tools/nginx-crawler-ranges.mjs` generates the `geo` block from the engines' published
      address files; 7 unit tests, `npm run test:tools` green
- [x] `conf.d/05-mokaair-crawler-ranges.conf` on the host — 617 prefixes from googlebot.json,
      special-crawlers.json (Search Console's live test fetches from there) and bingbot.json
- [x] chained key maps so a verified crawler has an empty key in `mokaair_content_pages` and a
      real one in the new `mokaair_crawlers` zone at 30r/s — the two never both count a request
- [x] four `location` blocks for the crawl-control files, exempt like `/_next/static/`
- [x] `log_format mokaair_limited` + `access_log … if=$mokaair_is_limited` recording the UA

## How to verify

Applied to `hostinger2` on 2026-09-19 with backup, `nginx -t` before reload, and automatic
restore on failure (`/root/nginx-backup-2026-09-19-142847`). Measured after reload:

```
/robots.txt   x40 concurrent -> 40 x 200      (was sharing the 5r/s page budget)
/sitemap.xml  x40 concurrent -> 40 x 200
/zh-TW        x60 concurrent -> 28 x 200, 32 x 429   (ordinary address, still limited)
```

The allowlist path was then proved end-to-end rather than assumed: the audit machine's own
address was temporarily added to the geo block, and 60 requests at 8 concurrent returned
**60 × 200** on both `/zh-TW` and `/sitemap.xml`. The temporary entry was removed and nginx
reloaded; `grep TEMP-VERIFY` on the host returns nothing.

Worth knowing: a 60-at-once burst still yields 429s even from an allowlisted address, and the
limit log names the reason — `limiting connections by zone "mokaair_conns"`, the server-level
`limit_conn 20`, not the request limiter. Left alone deliberately: 20 simultaneous connections
from one address is far more than a crawler opens, and HTTP/2 multiplexes besides.

Ongoing:

```bash
grep -iE 'googlebot|bingbot' /var/log/nginx/mokaair-limited.log   # should stay empty
```

Do not answer that question from the User-Agent alone — check the client address against
`conf.d/05-mokaair-crawler-ranges.conf`, which is what caught the spoofing scanner.

## Notes

**The drift is closed (#568).** For a while the host was ahead of the repository: `ops/nginx/`
was held by `2026-09-12-nginx-deploy-checks-false-pass`, so `claim` refused the scope and this
task was narrowed to `tools/`. That mattered more than housekeeping -- `install.sh:27`
overwrites `conf.d/mokaair-rate-limit.conf` from the repo, and that ticket's own step 1 runs
`install.sh`, so its verification could not pass until the repo carried this config. The two
halves were ordered, which is why the site owner had the ops ticket taken over and both done
together. `ops/nginx/` now carries `05-crawler-ranges.conf`, the chained key maps, the
crawl-control locations and the `ci-validate.conf` include that keeps CI's `nginx -t` green.

Confirmed afterwards on the host: `install.sh` run twice is idempotent, and the only thing it
changes is an eight-line comment. 40 concurrent requests to `/robots.txt` -> 40 x 200, the same
to `/zh-TW` -> 20 x 429.

**Why addresses and not User-Agents.** `docs/anti-scraping.md:94` already says there is no
User-Agent blocking on purpose. Exempting on a UA is the same mistake pointed the other way:
`curl -A Googlebot` would have bought `136.112.17.120` — the scanner above — an unmetered
crawl of the whole site. Checked after generating: that address is **not** in the allowlist,
while `66.249.72.168` (Googlebot) and `40.77.167.4` (Bingbot) both are.

**The generator makes no runtime fetch.** Google and Bing move these ranges; re-run the tool,
commit the diff, and copy the file to the host. It refuses to emit an empty allowlist and
drops any row that is not a bare CIDR, because its output goes straight into a file nginx
parses.
