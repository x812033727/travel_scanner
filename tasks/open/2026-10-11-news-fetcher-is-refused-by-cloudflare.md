---
id: 2026-10-11-news-fetcher-is-refused-by-cloudflare
title: News fetcher is refused by Cloudflare where plain curl from the host is not
status: in-progress
priority: P2
area: api
owner: codex-news-hourly-backlog
claimed_at: 2026-10-13T08:39:45Z
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
- [x] A test with a fake transport for the chosen shape; the existing SSRF tests keep
      passing locally (216 passed, 6 skipped in `test_news_automation.py`).
- [ ] Rerun `sources_cli` on the host (dry run, then apply, with the owner's go-ahead).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

On the host, `/admin/news?tab=sources` shows CFTC press releases with a recent successful
scan and `consecutive_failures` back at 0.

## Notes

- 2026-10-13 (`codex-news-hourly-backlog`): PR #1480 加了**只在原生 httpx 收到 `403` 且 `cf-mitigated: challenge`** 時，每輪啟動一次標準函式庫 TLS 後備請求。沿用已驗的 allow-list URL 與已解析的 public IP，連線固定該 IP、SNI／憑證仍核原網域、同一 host rate limit、原有 robots／轉址／內容型別檢查，逐塊以 2 MiB 上限讀 body，且提早拒絕時關閉回應；後備連線不自動跟轉址，要求 `identity`，若服務端仍回壓縮內容即拒絕。每次請求限 20 秒，429／5xx 沿用最多三輪重試；其他 403 不改路徑，也沒有降低 Cloudflare 以外來源的原閘。本機 `test_news_automation.py` **218 passed、6 skipped**，Ruff／mypy 通過；從本機對 CFTC 9307-26 的單次完整 SafeNewsFetcher 抓取讀回 `200 text/html 37348`，**這不證明正式主機曾啟動後備或已恢復**。未部署、未呼叫主機 `sources_cli`，全站掃描與候選終態仍待部署後獨立驗證。先前對主機 SSH 的呼叫遭自動審核阻擋，不改通道重試；主機專屬驗收維持未完成。
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
