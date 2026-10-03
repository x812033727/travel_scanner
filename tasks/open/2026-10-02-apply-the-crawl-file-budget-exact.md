---
id: 2026-10-02-apply-the-crawl-file-budget-exact
title: Apply the crawl-file budget, exact well-known location and TLS include on the host
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-02T16:41:37Z
completed_at:
branch:
depends_on:
  - 2026-09-23-nginx-sitemap-budget-and-tls-policy
scope:
  - .agents/skills/prod-host-ops/references/nginx-edge.md
---

# Apply the crawl-file budget, exact well-known location and TLS include on the host

## Why

Task `2026-09-23-nginx-sitemap-budget-and-tls-policy` changed only the repository: a
`mokaair_crawl_files` zone in `ops/nginx/10-rate-limit.conf`, the six crawl-control locations
in `mokaair.conf.example` counted against it (verified crawlers in `mokaair_crawlers` instead),
`/.well-known/` narrowed to one exact location for Apple's domain-association file, a new
`ops/nginx/tls-policy.conf` snippet, and `server_tokens off` in every server block. None of it
is live until the host's `sites-available/mokaair.com` is merged and nginx reloaded, and
`prod-host-ops/references/nginx-edge.md` still describes the old exemptions.

The TLS values in the snippet are Mozilla's "intermediate" profile, not a record of what the
host runs: the host's inline `ssl_protocols` / `ssl_ciphers` were never written down in the
repository. They have to be compared before the include replaces them.

## Definition of done

- [ ] The host serves the six crawl-control locations under `mokaair_crawl_files`, an unknown
      `/.well-known/` path under the page budget, and the TLS policy from the include.
- [ ] `curl -sI https://mokaair.com/sitemap.xml | grep -i '^server:'` prints `Server: nginx`
      with no version.
- [ ] `nginx-edge.md` describes the zones, exemptions and TLS source as they now are.

## Steps

- [ ] Ask the owner before touching the host (prod-host-ops rule 3); follow the skill's
      backup, upload/`install.sh`/`nginx -t` in one call, reload in another.
- [ ] Record the host's current `ssl_protocols` / `ssl_ciphers` /
      `ssl_prefer_server_ciphers` (`nginx -T`) here; decide with the owner whether any
      difference from `tls-policy.conf` is kept (in the snippet, not the site file).
- [ ] Merge the changed blocks of `mokaair.conf.example` into `sites-available/mokaair.com`,
      keeping the ACME webroot, mocair.io servers and `default_server`; put the TLS include
      and `server_tokens off` into the mocair.io servers as well.
- [ ] Run the README checks "Crawl-control files have a budget of their own" and "TLS policy
      and version banner".
- [ ] Update the zone table and the exemption paragraph in `nginx-edge.md`.

## How to verify

`ops/nginx/README.md`, sections "Crawl-control files have a budget of their own" and "TLS
policy and version banner"; then `grep -c 'mokaair_crawl_files' /var/log/nginx/mokaair-limit.log`
over the following days, to confirm no verified crawler address is ever refused by that zone.

## Notes

- Filed by the agent that made the repository change, which was told not to connect to the
  host.
- Apple's `apple-developer-domain-association.txt` is not committed yet
  (`apps/web/public/.well-known/` does not exist; Sign in with Apple is not enabled). The exact
  location answers Next's 404 until it is.
