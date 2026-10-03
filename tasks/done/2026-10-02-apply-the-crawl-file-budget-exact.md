---
id: 2026-10-02-apply-the-crawl-file-budget-exact
title: Apply the crawl-file budget, exact well-known location and TLS include on the host
status: done
priority: P3
area: ops
owner: claude-fable-5-1-illustration-polish
claimed_at: 2026-10-03T04:35:34Z
created_at: 2026-10-02T16:41:37Z
completed_at: 2026-10-03T04:37:57Z
branch: claude/illustration-polish-followups
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

- [x] The host serves the six crawl-control locations under `mokaair_crawl_files`, an unknown
      `/.well-known/` path under the page budget, and the TLS policy from the include.
- [x] `curl -sI https://mokaair.com/sitemap.xml | grep -i '^server:'` prints `Server: nginx`
      with no version.
- [x] `nginx-edge.md` describes the zones, exemptions and TLS source as they now are.

## Steps

- [x] Ask the owner before touching the host (prod-host-ops rule 3); follow the skill's
      backup, upload/`install.sh`/`nginx -t` in one call, reload in another.
- [x] Record the host's current `ssl_protocols` / `ssl_ciphers` /
      `ssl_prefer_server_ciphers` (`nginx -T`) here; decide with the owner whether any
      difference from `tls-policy.conf` is kept (in the snippet, not the site file).
- [x] Merge the changed blocks of `mokaair.conf.example` into `sites-available/mokaair.com`,
      keeping the ACME webroot, mocair.io servers and `default_server`; put the TLS include
      and `server_tokens off` into the mocair.io servers as well.
- [x] Run the README checks "Crawl-control files have a budget of their own" and "TLS policy
      and version banner".
- [x] Update the zone table and the exemption paragraph in `nginx-edge.md`.

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

- **Applied 2026-10-03 04:32Z** with the owner's approval in the session, right after deploying
  main (90c52e19e) so the host work tree carried the new `ops/nginx`. Backup
  `/root/nginx-backups/20261003T043228Z/etc-nginx`; one call for backup, `install.sh`, the
  site-file merge and `nginx -t`; a second call for `systemctl reload nginx`.
- The host's inline TLS values before the change were `ssl_protocols TLSv1.2 TLSv1.3;`,
  `ssl_prefer_server_ciphers off;` and the same six ECDHE GCM/CHACHA20 suites as
  `tls-policy.conf`, in all three ssl servers: identical, so no difference to keep.
- The site file was merged by exact-match edits (11 edits, each required to match its expected
  count) and re-counted afterwards: three TLS includes, four `server_tokens off`, six locations
  in `mokaair_crawl_files`, header-hygiene includes and `proxy_pass` 11 each, ACME webroot and
  `default_server` untouched.
- Readings after the reload: banner `nginx` on all four servers (was `nginx/1.28.3 (Ubuntu)`);
  60 parallel fetches of `/sitemaps/sitemap/static.xml` gave 39 refusals, 27 naming
  `mokaair_crawl_files` and 12 `mokaair_conns` (before: 21, all `mokaair_conns`); 40 parallel
  fetches of an unknown `/.well-known/` path gave 19 refusals, all `mokaair_content_pages`;
  TLS 1.1 refused with alert 70; a CBC-only client refused with and without SNI; the port-80
  ACME probe still answers 404 from the webroot; the `www` OAuth redirect is unchanged.
- The README's example child `/sitemaps/guides.xml` is a 404 on this site; the real children
  are `/sitemaps/sitemap/<id>.xml`.
- `install.sh` has a pipe race that can seed an unread `sites-available/mokaair.conf`
  (task `2026-10-03-nginx-install-sh-loses-a-pipe`); it did not fire this time.
- Still to watch for a few days: `grep -c 'mokaair_crawl_files' /var/log/nginx/mokaair-limit.log`
  by source address, to confirm no verified crawler is refused by that zone.
