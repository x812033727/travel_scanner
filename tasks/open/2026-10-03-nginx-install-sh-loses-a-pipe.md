---
id: 2026-10-03-nginx-install-sh-loses-a-pipe
title: nginx install.sh loses a pipe race under pipefail and seeds an unread site file
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-03T04:28:04Z
completed_at:
branch:
depends_on: []
scope:
  - ops/nginx/install.sh
---

# nginx install.sh loses a pipe race under pipefail and seeds an unread site file

## Why

`ops/nginx/install.sh` decides whether the site is already enabled with one grep piped into
`grep -Eq` under `set -o pipefail` (`looks_like_mokaair_site`). The second grep exits on its
first match and closes the pipe; when the first grep has not finished writing (the host's site
file is over 4 KB without comments, so it writes twice), it dies of SIGPIPE, the pipeline
returns non-zero, and the enabled `sites-available/mokaair.com` is taken for "not this site".
The installer then seeds `sites-available/mokaair.conf`, a file nginx never reads, and still
exits 0. That file is what made the 2026-09-12 rollout a no-op.

A review of the host merge on 2026-10-03 reproduced the race locally. The apply that day did not
hit it, and its script would have removed a stray seed.

## Definition of done

- [ ] The site detection cannot be lost to SIGPIPE: the reader consumes its whole input (send
      the match to /dev/null instead of using -q, or use one awk), or the function does not run
      under pipefail.
- [ ] A test (or a documented manual check) with a site file larger than one pipe buffer shows
      the enabled site is detected every time.

## Steps

- [ ] Fix `looks_like_mokaair_site` in `ops/nginx/install.sh`.
- [ ] Extend the CI nginx check, or add a small shell test, with a site file over 4096 bytes.

## How to verify

Run the detection a few hundred times in a loop against a copy of the host's site file; it must
never report the site as absent.

## Notes

Until it is fixed: after running `install.sh` on the host, check that
`/etc/nginx/sites-available/mokaair.conf` was not created, and delete it if it was.
