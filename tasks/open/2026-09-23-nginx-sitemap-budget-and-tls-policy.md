---
id: 2026-09-23-nginx-sitemap-budget-and-tls-policy
title: Edge: sitemap and well-known locations have no request budget and TLS policy lives only on the host
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-23T15:57:50Z
completed_at:
branch:
depends_on: []
scope:
  - ops/nginx/mokaair.conf.example
  - ops/nginx/10-rate-limit.conf
  - ops/nginx/ci-validate.conf
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

- [ ] Sitemap, llms.txt and well-known locations count against a finite zone (their own,
      larger than the page budget, still keyed off for verified crawlers) or are served from
      cache with `s-maxage`.
- [ ] `/.well-known/` becomes a set of exact-match locations for the files Apple and ACME
      actually fetch, so unknown paths fall into the page budget.
- [ ] The example carries `ssl_protocols TLSv1.2 TLSv1.3;`, `ssl_prefer_server_ciphers off;`
      and `server_tokens off;`, and `ci-validate.conf` plus the CI behavioural test still
      pass.

## Steps

- [ ] Add a `mokaair_crawl_files` zone in `10-rate-limit.conf` (for example 10 r/s burst 30,
      keyed like the page zone).
- [ ] Rewrite the six locations; keep the comments explaining why crawlers must not get 429s.
- [ ] Add the TLS and banner lines, with a note that the host `nginx.conf` must not override
      them.
- [ ] Update the README smoke test that expects a `Server:` header (that file belongs to
      `2026-09-23-scrub-host-details-from-docs`; coordinate or land after it).

## How to verify

The CI job that loads `ci-validate.conf` (see `.github/workflows/ci.yml`) and, after the host
merge, `curl -sI https://mokaair.com/sitemap.xml | grep -i server` prints no version.

## Notes

- Found in the 2026-09-23 security review (findings L6, L12). The host merge follows the
  `deploy` skill and `ops/nginx/README.md`: this file is an example the host config is merged
  from, and the live file carries extra blocks (ACME webroot, extra domains) that must not be
  lost.
