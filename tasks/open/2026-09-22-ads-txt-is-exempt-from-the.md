---
id: 2026-09-22-ads-txt-is-exempt-from-the
title: ads.txt is exempt from the page budget and crawl-control fetches are logged
status: in-progress
priority: P2
area: ops
owner: claude-opus-5
claimed_at: 2026-09-22T06:17:43Z
created_at: 2026-09-22T06:17:24Z
completed_at:
branch: claude/ads-txt-status-missing-9c05a3
depends_on: []
scope:
  - ops/nginx/10-rate-limit.conf
  - ops/nginx/mokaair.conf.example
  - ops/nginx/ci-validate.conf
  - ops/nginx/README.md
---

# ads.txt is exempt from the page budget and crawl-control fetches are logged

## Why

On 2026-09-22 the owner reported that AdSense had flipped this site's ads.txt status from
"authorised" to "not found". Every check that could be made from outside said the file was
fine: `https://mokaair.com/ads.txt` answered 200 `text/plain; charset=utf-8` with the exact
59 bytes Google wants, ten times in a row, for `Googlebot` and `Google-Adstxt` alike, over
http and https, apex and www. There is no fail2ban on the host, ufw is inactive, and no
iptables rule drops anything.

What could not be checked is the only thing that mattered: **whether Google fetched it, and
what it got.** The site's own requests have not been logged since 2026-09-19, when
`access_log /var/log/nginx/mokaair-limited.log ... if=$mokaair_is_limited` was added to the
server block. A server-level `access_log` replaces the inherited one rather than adding to
it, so from that line onward this server records 429s and nothing else. The last fetch of
`/ads.txt` anyone can point at is 2026-09-13. "AdSense says not found" cannot be answered
against reality, only guessed at.

The second half is a gap the same server block already argues against in its own comment.
`/robots.txt`, `/sitemap.xml`, `/llms.txt` and `/sitemaps/` are exempt from the page budget
because "a 429 on /robots.txt or /sitemap.xml is a crawler losing its instructions for the
whole site". `/ads.txt` is that kind of file and was never added: it falls through to
`location /` and the 5r/s page budget. Worse than the others, Google's ads.txt fetcher is
`Google-Adstxt`, which publishes its addresses in `special-crawlers.json`, not the
`googlebot.json` ranges `05-crawler-ranges.conf` is built from -- so it is not a verified
crawler here and is keyed into the page zone by address like any visitor. Nothing in the
limit log shows it being refused, so this is not the 2026-09-22 cause; it is the way this
would happen silently next time.

## Definition of done

- [x] A fetch of `/ads.txt`, `/robots.txt`, `/sitemap.xml`, `/llms.txt` or `/sitemaps/*`
      leaves a line naming its status and User-Agent, so "did Google come, and what did it
      get" is one grep.
- [x] 429s still reach `mokaair-limited.log` exactly as before.
- [x] `/ads.txt` is not counted against the page budget.

## Steps

- [x] Map the crawl-control paths in `10-rate-limit.conf`, beside `$mokaair_is_limited`.
- [x] Add the second server-level `access_log` and a `location = /ads.txt` to
      `mokaair.conf.example`.
- [x] Exercise both in `ci-validate.conf` so `nginx -t` covers them.
- [x] Write the merge and the check into `README.md`.
- [x] Merge into `/etc/nginx/sites-available/mokaair.com` on the host, `nginx -t`, reload.
- [x] Confirm `mokaair-crawl.log` fills.
- [ ] Re-check the AdSense ads.txt status a day later, against what the log says Google got.

## How to verify

On the host, after the reload:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/ads.txt
tail -3 /var/log/nginx/mokaair-crawl.log          # the fetch above, with its User-Agent
grep ' /ads.txt ' /var/log/nginx/mokaair-crawl.log | grep -i 'google'
```

In CI, `nginx -t -c ops/nginx/ci-validate.conf` covers the map and both directives.

## Notes

- The web container restarted 2026-09-22T05:05:59Z, the deploy that replaced
  `apps/web/public/ads.txt` with the `app/ads.txt/route.ts` handler. The live response is
  the handler (chunked, `cache-control: public, max-age=3600`, the `vary: rsc, ...` Next
  adds), and it is byte-correct. nginx logged five upstream failures all day, at 04:02,
  04:25 and 05:05 -- restart-length, not an outage.
- `mocair.io/ads.txt` is a cross-domain 301 to `mokaair.com/ads.txt`. Harmless for the site
  AdSense actually lists, but it is why the domain in the AdSense row matters before anyone
  concludes anything from a "not found".
- Applied on the host 2026-09-22T06:23Z: `conf.d/mokaair-rate-limit.conf` reinstalled from
  this directory (it was byte-identical to the repo before), the two blocks merged into
  `sites-available/mokaair.com`, `nginx -t`, reload. Backups beside each file, suffixed
  `.bak-...-20260922062352`. Proof: 40 concurrent fetches of `/ads.txt` all answered 200
  where the page budget would have refused about fifteen of them, and `mokaair-crawl.log`
  now carries every crawl-control fetch while page requests stay out of it.
- `combined` counts `$body_bytes_sent`, which for a chunked response includes the framing:
  the Route Handler's 59-byte line logs as **70**, the old static `public/ads.txt` logged as
  59. That is how to tell from a log line alone which of the two answered -- and the 59/70
  alternation in `access.log` on 2026-09-19 is someone switching between them, not drift.
- `combined` is nginx's stock format and carries the User-Agent, which `mokaair_limited`
  also does; `mokaair-limit.log` (the error-log side) does not.
