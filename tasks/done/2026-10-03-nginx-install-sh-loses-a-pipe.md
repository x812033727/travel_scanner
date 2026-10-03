---
id: 2026-10-03-nginx-install-sh-loses-a-pipe
title: nginx install.sh loses a pipe race under pipefail and seeds an unread site file
status: done
priority: P3
area: ops
owner: codex-nginx-detection-20261003
claimed_at: 2026-10-03T09:44:07Z
created_at: 2026-10-03T04:28:04Z
completed_at: 2026-10-03T09:50:09Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - ops/nginx/install.sh
  - tools/nginx-install.test.mjs
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

- [x] The site detection cannot be lost to SIGPIPE: the reader consumes its whole input (send
      the match to /dev/null instead of using -q, or use one awk), or the function does not run
      under pipefail.
- [x] A test (or a documented manual check) with a site file larger than one pipe buffer shows
      the enabled site is detected every time.

## Steps

- [x] Fix `looks_like_mokaair_site` in `ops/nginx/install.sh`.
- [x] Extend the CI nginx check, or add a small shell test, with a site file over 4096 bytes.

## How to verify

Run the detection a few hundred times in a loop against a copy of the host's site file; it must
never report the site as absent.

## Notes

Until it is fixed: after running `install.sh` on the host, check that
`/etc/nginx/sites-available/mokaair.conf` was not created, and delete it if it was.

### 2026-10-03 local repair

- The second grep now consumes its full input with `grep -E ... >/dev/null`.
  Marker matching, comment exclusion, missing-file behavior and `pipefail` stay intact.
- Added `tools/nginx-install.test.mjs` to this ticket's scope before implementation.
  It runs the actual marker declaration and detector in an isolated Bash process,
  without running the installer or writing `/etc`. The existing `test:tools` glob
  automatically includes the regression in CI.
- Regression first reproduced the old detector's failure on attempt 1 against
  2,031,616 bytes of uncommented padding after an early site marker. After the fix,
  all six cases passed with zero skips: 300 early-marker detections, a late marker,
  comment-only markers, rate-limit declarations, an unrelated site and an absent file.
  Local command: Node 24.19.0 `--test tools/nginx-install.test.mjs`, with Git Bash
  5.3.15 first on PATH. Only the absent-file test's display name changed afterward.
- An independent native Linux / WSL Bash 5.3.9 check repeated the same six fixture
  behaviors, including another 300 early-marker detections; every exit code was 0.
  The tested installer SHA-256 is
  `34050640c161208536ce43c63004cb904cde92a60d815dbb88d5691101196f60`.
- Before claiming, checked 493 local/remote refs, 38 registered worktrees, live
  remote heads and the four open PRs. No active or unlanded candidate change was
  found; the existing draft #1175 is the delivery PR for this repair.
- This completes the source repair and local regression. No production connection,
  installation, nginx reload or live-site acceptance was performed.
