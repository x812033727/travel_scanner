---
id: 2026-10-11-news-fetcher-is-refused-by-cloudflare
title: News fetcher is refused by Cloudflare where plain curl from the host is not
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T05:23:46Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/fetch.py
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# News fetcher is refused by Cloudflare where plain curl from the host is not

## Why

"CFTC press releases" has failed on every hourly scan for about four days: on 2026-10-11
04:38Z the source row showed `last_status = failed`, `consecutive_failures = 99` and
`HTTPStatusError: Client error '403 Forbidden' for url 'https://104.18.25.94/RSS/RSSGP/rssgp.xml'`.

The host is not blocked. The same minute, from the host, a plain
`curl -A 'Mokaair-editorial/1.0 (...)' https://www.cftc.gov/RSS/RSSGP/rssgp.xml` answered
200 with `application/rss+xml`, and its robots.txt answered 200.

The difference is how `SafeNewsFetcher` connects (`apps/api/app/news_automation/fetch.py`,
`_request`): it resolves the host, then requests the URL with the IP in place of the name,
sending `Host` and SNI separately, to close the DNS-rebinding gap. The refused URL in the
error is that pinned address, which belongs to Cloudflare. That Cloudflare refuses this
shape of request is an inference from those two observations; it has not been tested.

It may not be one source. On 2026-10-10, probing from a development machine through the
same fetcher, `claude.com`, `claude.dev`, `code.claude.com` and `www.anthropic.com` (all
behind Cloudflare) answered 403, robots.txt included, after a handful of requests, and
passed minutes later. Five sources loaded on 2026-10-11 were refused validation from the
host with `UnsafeNewsUrl` (Mistral AI news and four Taiwan government sites); a 403 on
robots.txt is read as "not permitted" and raises that same error.

## Definition of done

- [ ] The cause is established, not assumed: the same request the fetcher sends is
      reproduced from the host (pinned IP, `Host` header, SNI, the fetcher's headers and
      TLS context) and compared with the plain request, for CFTC and for one of the
      Anthropic hosts.
- [ ] Either the fetcher reaches those publishers again without giving up the rebinding
      protection, or the reason it cannot is written here with what would have to change.
- [ ] CFTC press releases scans again, or is switched off with the reason in its note.
- [ ] The five sources refused on 2026-10-11 are tried again once the cause is known.

## Steps

- [ ] Reproduce on the host inside the api container, one request per variant: by name;
      pinned IP with `Host` and SNI; with and without the `Accept` list; HTTP/1.1 against
      HTTP/2. Record status and the `cf-ray` / `server` headers.
- [ ] If the pinned request is what is refused: keep the validation of the resolved
      addresses but connect by name through a transport that pins the address (a custom
      resolver or connection pool), so the request line and TLS look ordinary.
- [ ] A test with a fake transport for the chosen shape; the existing SSRF tests keep
      passing.
- [ ] Rerun `sources_cli` on the host (dry run, then apply, with the owner's go-ahead).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

On the host, `/admin/news?tab=sources` shows CFTC press releases with a recent successful
scan and `consecutive_failures` back at 0.

## Notes

- 2026-10-11 08:46Z, reproduced read-only inside the api container on the host. **The
  pinned-IP guess in "Why" is wrong.** For the CFTC feed:
  - httpx answers 403 with `cf-mitigated: challenge` whether it connects by name or by
    pinned IP with `Host` and SNI, with httpx's TLS context, the fetcher's, or the standard
    library's default one (also with ALPN forced to http/1.1), and with or without `Accept`
    and `Accept-Encoding`. `h2` is not installed, so HTTP/2 was not tried.
  - From the same container and address, `urllib.request` with the same User-Agent answers
    200. From the host, curl answers 200 over HTTP/2 and over HTTP/1.1.
  - So Cloudflare challenges something about how httpx talks that these variants did not
    change. Not yet isolated: the header order (httpx sends Host, Accept, Accept-Encoding,
    Connection, User-Agent; urllib sends Accept-Encoding, Host, User-Agent, Connection),
    the `Accept: */*` httpx always adds, or the TLS handshake below what the context sets.
  - `robots.txt` on the same host answers 200 to every variant, so only the feed path is
    challenged.
  - `robots.txt` of `mistral.ai` and `www.anthropic.com` answered 200 to httpx in all four
    shapes at that moment; the 403s seen on 2026-10-10 were not reproduced from the host.
- The five sources refused on 2026-10-11 do not share this cause:
  - **Mistral AI news**: robots allows it; the fetcher refuses the feed with
    "unsupported content type: text/plain". The feed is served as text/plain, which is not
    in `ALLOWED_TYPES`.
  - **Taiwan MODA**: robots.txt answers 404, which the fetcher reads as refused (the same
    rule as `2026-10-10-decide-whether-the-news-fetcher-follows`).
  - Taiwan central bank, NSTC and FSC were not looked at here.
- Claiming this task was refused on 2026-10-11: `2026-10-10-let-the-owner-re-request-a`
  is in progress with all of `apps/api/tests` in its scope. Nothing in the repository was
  changed for this note beyond the note itself.
- Next: send httpx's exact header set through urllib, and urllib's through httpx, to see
  which side the challenge follows; try `http2=True` with `h2` in a throwaway environment.

- A source that fails for more than six hours on recent entries is meant to show as
  `stuck` on `/admin/news`; this one shows `failed` because the listing itself is refused.
  Whether the owner was shown it at all in those four days is worth checking while here
  (`2026-10-06-daily-summary-of-stuck-news-sources`).
- Do not weaken the checks to make it pass: HTTPS only, public addresses only, the host
  allow-list and robots.txt stay.
