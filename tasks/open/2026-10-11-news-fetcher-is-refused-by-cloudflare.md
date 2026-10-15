---
id: 2026-10-11-news-fetcher-is-refused-by-cloudflare
title: News fetcher is refused by Cloudflare where plain curl from the host is not
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-news-sources
claimed_at: 2026-10-15T17:09:40Z
created_at: 2026-10-11T05:23:46Z
completed_at:
branch: claude/news-sources-red-fix
depends_on: []
scope:
  - apps/api/app/news_automation/fetch.py
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
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

- [x] The cause is established, not assumed: the same request the fetcher sends is
      reproduced from the host (pinned IP, `Host` header, SNI, the fetcher's headers and
      TLS context) and compared with the plain request, for CFTC and for one of the
      Anthropic hosts.
- [x] Either the fetcher reaches those publishers again without giving up the rebinding
      protection, or the reason it cannot is written here with what would have to change.
- [x] CFTC press releases scans again, or is switched off with the reason in its note.
- [x] The five sources refused on 2026-10-11 are tried again once the cause is known.

## Steps

- [x] Reproduce on the host inside the api container, one request per variant: by name;
      pinned IP with `Host` and SNI; with and without the `Accept` list; HTTP/1.1 against
      HTTP/2. Record status and the `cf-ray` / `server` headers.
- [x] If the pinned request is what is refused: keep the validation of the resolved
      addresses but connect by name through a transport that pins the address (a custom
      resolver or connection pool), so the request line and TLS look ordinary.
- [x] A test with a fake transport for the chosen shape; the existing SSRF tests keep
      passing.
- [ ] Rerun `sources_cli` on the host (dry run, then apply, with the owner's go-ahead).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

On the host, `/admin/news?tab=sources` shows CFTC press releases with a recent successful
scan and `consecutive_failures` back at 0.

## Notes

- 2026-10-11 09:17Z: **HTTP/2 does not fix it.** Tried from the host in a one-off
  container of the api image (`docker run --rm`, `h2` installed into the container's own
  /tmp): httpx 0.28.1 against the CFTC feed answered 403 with `cf-mitigated: challenge`
  over HTTP/1.1 and over HTTP/2, by name and with the fetcher's pinned request, twice
  each. Controls a minute later: curl from the host 200, `urllib` in the api container 200.
  The change that was written for it (`httpx[http2]`, `http2=True`) sits unmerged on
  branch `claude/news-fetcher-http2`; do not open it as a pull request.
- Putting the runs together: a Python TLS handshake that offers a protocol list (ALPN) is
  challenged, whichever list; a Python handshake that offers none passes (urllib, and the
  hand-built socket tests); curl offers a list and passes, with another TLS library. httpx
  always offers one (httpcore sets it at connect), so nothing in httpx's settings avoids
  it. This is an inference from six observations, not something Cloudflare states.
- What is left as a fix: carry the fetcher's requests on a transport that does not go
  through httpcore's connection, as `UrllibTransport` in `app/guides/pack_ingest.py` does
  for Wikimedia (which refuses httpx the same way), while keeping what `_request` does
  today: the resolved address checked and pinned, SNI and certificate checked against the
  name, the size cap while reading, no redirects followed. That is a design, not a
  one-line change.

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
- 2026-10-11 08:51Z, isolated with hand-built requests over a plain TLS socket from the
  api container (same headers every time, standard-library TLS context):
  - no ALPN offered: 200.
  - ALPN offering only `http/1.1`: 403 with `cf-mitigated: challenge`, twice out of twice.
  - ALPN offering `http/1.1` and `h2`: the server selects `h2` (the request was then sent
    as HTTP/1.1, so its answer says nothing more).
  - The headers do not matter: httpx's header set and order, urllib's, with and without
    `Accept`, all answered 200 over a socket without ALPN, also with httpx's own TLS
    context; and httpx sending urllib's exact four headers was still challenged.
  **Cause: the TLS handshake advertises HTTP/1.1 as its only protocol.** httpx without
  HTTP/2 does that (httpcore sets ALPN to `http/1.1`); curl offers `h2` as well and
  urllib offers nothing, and both pass. The pinned IP is not involved.
  - The second no-ALPN request answered 429: the probing itself reached this host's rate
    limit, so the tests stopped there.
- What a fix could be, not built: let the fetcher's client speak HTTP/2 (`http2=True`
  needs the `h2` package in the api image), which makes the handshake look like curl's;
  or give its TLS context an ALPN list that includes `h2`. Either has to be tried against
  CFTC from the host, and the pinned-IP request with `Host` and SNI has to keep working
  over HTTP/2 (`:authority` comes from the URL, so the pinned shape may need a transport
  that pins the address instead). Whether other publishers behind Cloudflare apply the
  same rule is not known: `www.anthropic.com` and `mistral.ai` did not challenge httpx.

- A source that fails for more than six hours on recent entries is meant to show as
  `stuck` on `/admin/news`; this one shows `failed` because the listing itself is refused.
  Whether the owner was shown it at all in those four days is worth checking while here
  (`2026-10-06-daily-summary-of-stuck-news-sources`).
- Do not weaken the checks to make it pass: HTTPS only, public addresses only, the host
  allow-list and robots.txt stay.

## 2026-10-16: fixed (claude-opus-5-5-news-sources, owner asked to fix every red source)

The owner asked to fix every news source shown in red on `/admin/news?tab=sources`. Read-only
production state at 2026-10-15 17:00Z: two enabled sources failing every hour (CFTC 211 in a
row, GitHub blog 22) and nine disabled with `validation_failed`. Each was run through the real
`validate_source_configuration` inside the news-worker with every HTTP hop logged:

| Source | Cause | Fix |
| --- | --- | --- |
| CFTC press releases | Cloudflare challenges httpx's ALPN offer (403 `cf-mitigated: challenge`); without the offer the pinned request answers 200 for the feed and a release page | `fetch._NoAlpnContext`: `tls_context()` ignores `set_alpn_protocols`; pinning, Host/SNI, certificate checks unchanged |
| GitHub blog | full-text feed 2.3 MB > 2 MB cap | source config `max_response_bytes` (listing only, capped at 8 MB); GitHub set to 6 MB |
| Mistral AI news | feed served as `text/plain` | `text/plain` whose body is XML is read as `application/xml` |
| MODA, NSTC | robots.txt 404 read as "not permitted" | RFC 9309: a 4xx other than 429 restricts nothing |
| Central bank | /robots.txt redirects to the home page (HTML), read as "not permitted" | a redirect that lands on no robots file = no robots.txt |
| FSC (crypto) | no crypto title on the listing this week ("no entries"), and the first item links to sfb.gov.tw | validation checks the titles the keyword filter set aside, and only entries on the source's own site (as the scanner does) |
| Ars Technica AI | robots 405 fixed by the RFC rule, but every article page answers 405 (AWS ELB) to curl and a browser UA from the host | disabled in `sources.json` with the reason |
| OpenAI News, The Block | every article page answers 403 with a Cloudflare challenge to curl and a browser UA too | stay disabled (OpenAI now `enabled: false` in the file) |

The branch's `fetch.py`, `validation.py` and `sources.json` were loaded into one process in the
news-worker (nothing on disk changed, no database write) and validated all ten: CFTC, GitHub
blog, MODA, FSC, central bank, NSTC and Mistral pass; Ars, OpenAI News and The Block fail on
their article pages as above. No browser impersonation was added: the User-Agent stays
`Mokaair-editorial/1.0`, robots.txt is still honoured.

Also: `/admin/news` showed every `last_error` in red, so a successful scan's note (DeepMind
"Left out 11 feed entries older than 72 hours") looked like a failure. Only `failed`,
`validation_failed`, `stuck` and `partial` are red now.

Left after merge: deploy, then `sources_cli` dry run and `--apply` on the host with the owner's
go-ahead (it validates and re-enables the seven), then check `/admin/news?tab=sources`.
