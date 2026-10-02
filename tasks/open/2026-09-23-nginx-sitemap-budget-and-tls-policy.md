---
id: 2026-09-23-nginx-sitemap-budget-and-tls-policy
title: Edge: sitemap and well-known locations have no request budget and TLS policy lives only on the host
status: in-progress
priority: P3
area: ops
owner: claude-opus-5-5-nginx-edge
claimed_at: 2026-10-02T16:35:04Z
created_at: 2026-09-23T15:57:50Z
completed_at:
branch: claude/nginx-sitemap-budget-tls
depends_on: []
scope:
  - ops/nginx/mokaair.conf.example
  - ops/nginx/10-rate-limit.conf
  - ops/nginx/ci-validate.conf
  - ops/nginx/tls-policy.conf
  - ops/nginx/install.sh
  - ops/nginx/README.md
  - tools/test-guide-image-rate-limit.py
---

# Edge: sitemap and well-known locations have no request budget and TLS policy lives only on the host

## Why

`mokaair.conf.example` exempts `/sitemap.xml`, `^~ /sitemaps/`, `/llms.txt`, `/robots.txt`,
`/ads.txt` and the whole `/.well-known/` prefix from `limit_req`, on the sound reasoning that
a 429 on a crawl-control file costs more than serving it. But both sitemap routes in Next are
`force-dynamic` with `Cache-Control: max-age=0`, so every hit is a fresh server render that
reads the guides index, and a miss under `/.well-known/anything` renders the full Next 404
document. The only bound left is `limit_conn 20`: one address can hold 20 connections looping
on `/sitemaps/guides.xml` and never see a 429. Verified crawlers already leave the page budget
through `$mokaair_verified_crawler`, so the exemption no longer needs to be unlimited for
everyone else.

Separately, the example inherits `ssl_protocols` / `ssl_ciphers` from the host `nginx.conf`
and never sets `server_tokens off`, so the repository cannot show that TLS 1.0/1.1 are off or
that the version banner is hidden; the README smoke test even expects a `Server:` header.

## Definition of done

- [x] Sitemap, llms.txt and well-known locations count against a finite zone (their own,
      larger than the page budget, still keyed off for verified crawlers) or are served from
      cache with `s-maxage`.
- [x] `/.well-known/` becomes a set of exact-match locations for the files Apple and ACME
      actually fetch, so unknown paths fall into the page budget.
- [x] The example carries `ssl_protocols TLSv1.2 TLSv1.3;`, `ssl_prefer_server_ciphers off;`
      and `server_tokens off;`, and `ci-validate.conf` plus the CI behavioural test still
      pass. (CI is the run that proves this; see Notes.)

## Steps

- [x] Add a `mokaair_crawl_files` zone in `10-rate-limit.conf` (for example 10 r/s burst 30,
      keyed like the page zone).
- [x] Rewrite the six locations; keep the comments explaining why crawlers must not get 429s.
- [x] Add the TLS and banner lines, with a note that the host `nginx.conf` must not override
      them.
- [x] Update the README smoke test that expects a `Server:` header (that file belongs to
      `2026-09-23-scrub-host-details-from-docs`; coordinate or land after it).
- [ ] Apply on the host -- a separate, owner-approved step through the `prod-host-ops` skill;
      filed as its own task (see Notes).

## How to verify

The CI job that loads `ci-validate.conf` (see `.github/workflows/ci.yml`) and, after the host
merge, `curl -sI https://mokaair.com/sitemap.xml | grep -i server` prints no version.

## Notes

- Found in the 2026-09-23 security review (findings L6, L12). The host merge follows the
  `deploy` skill and `ops/nginx/README.md`: this file is an example the host config is merged
  from, and the live file carries extra blocks (ACME webroot, extra domains) that must not be
  lost.
- 2026-10-02, claude-opus-5-5-nginx-edge. Claimed with `--force`: the only blocker was
  `2026-09-22-ads-txt-is-exempt-from-the` (claude-opus-5, same `ops/nginx` scope), a stale
  claim whose branch `claude/ads-txt-status-missing-9c05a3` is PR #656, MERGED, with no open
  PR on it. That task file was left alone.
- **Budget.** `mokaair_crawl_files`, 10 r/s burst 30, keyed on `$mokaair_page_limit_key` --
  the page zone's own key, so a verified crawler has an empty key there with no new map. All
  six locations (`/robots.txt`, `/ads.txt`, `/sitemap.xml`, `/llms.txt`, `^~ /sitemaps/`,
  Apple's file) carry the same pair as `location /`: the crawl-file zone plus
  `mokaair_crawlers burst=60`, so Googlebot/Bingbot are counted only in the crawler zone and
  never refused by a budget sized for visitors. `/robots.txt` and `/ads.txt` were included
  too ("the six locations"): Google-Adstxt is not a verified crawler and now meets a 30-fetch
  burst instead of nothing, which it never comes near. Chosen over `s-maxage` caching because
  that is an application change outside this scope.
- **`/.well-known/`.** One exact location, `/.well-known/apple-developer-domain-association.txt`
  (docs/social-login.md; the file itself is not committed yet). No ACME location on 443: the
  host answers http-01 from its port-80 webroot before the redirect, so it never reaches that
  server, and challenge tokens cannot be exact matches anyway. Everything else under the
  prefix is a page now.
- **Logging unchanged.** No `access_log` moved or added; `$mokaair_is_crawl_control` still
  maps the same five paths (Apple's file is deliberately not added to `mokaair-crawl.log`).
  Refusals by the new zone reach `mokaair-limit.log` (zone name) and `mokaair-limited.log`
  (status 429) through the existing lines.
- **TLS.** New `ops/nginx/tls-policy.conf` (installed as `snippets/mokaair-tls-policy.conf`,
  hence `install.sh` in scope) with Mozilla intermediate 6.0: TLS 1.2/1.3, six ECDHE AEAD
  ciphers, `ssl_prefer_server_ciphers off`. It is a proposal, not the host's values -- those
  were never recorded in the repository; the snippet header and the follow-up task say how to
  compare. Curves deliberately unpinned (X25519MLKEM768 needs OpenSSL 3.5; pinning without it
  turns hybrid PQ off). Included in both 443 servers; `server_tokens off` in all three.
  Two `ssl_protocols` lines in one block are not reliably rejected by `nginx -t`, so the
  README check reads `nginx -T` and probes TLS 1.1 with `@SECLEVEL=0` (an OpenSSL 3 client
  refuses to offer 1.1 itself, which would read as a false pass).
- **README.** Taken into scope although it is also in
  `2026-09-23-scrub-host-details-from-docs` (open, unclaimed): the merge text said the host's
  inline TLS parameters must survive, which now contradicts the example, and the file table
  had to name the new snippet. The `Server:` smoke test needed no change: `server_tokens off`
  keeps `Server: nginx` and drops only the version. Added two checks ("Crawl-control files
  have a budget of their own", "TLS policy and version banner") and the missing
  `05-crawler-ranges.conf` table row.
- **CI.** `ci-validate.conf` mirrors the six locations and adds a `listen 8443 ssl` server with
  `ssl_reject_handshake on` that includes the TLS snippet: without a certificate nginx never
  builds a TLS context and would not hand the cipher string to OpenSSL at all.
  `tools/test-guide-image-rate-limit.py` (in scope for that reason) now also: statically
  checks the example (every crawl location carries both limits, no `/.well-known/` prefix
  location, `server_tokens off` in all three servers, the TLS include in both 443 ones --
  verified to fail against main's example); checks the six files answer while the page budget
  is spent; unknown `/.well-known/` paths get 429 like pages; 60 rapid sitemap fetches hit a
  429 after the first 20 pass; a verified crawler (127.0.0.2 added to a temporary copy of
  `05-crawler-ranges.conf`) gets 50 in a row and is then bounded by `mokaair_crawlers`
  (200 concurrent); `Server: nginx` with no version on a 200 and a 429. This machine has no
  nginx or docker, so the CI `containers` job is the run that executes it.
- Applying it on the host is task `2026-10-02-apply-the-crawl-file-budget-exact`
  (owner-approved, through `prod-host-ops`), which also updates
  `prod-host-ops/references/nginx-edge.md`.
