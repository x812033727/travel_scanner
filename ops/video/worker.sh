#!/bin/sh
# The video worker's loop (docs/videos/AUTOMATION.md).
#
# First it pairs with the site: `login` prints a code, the owner allows it on the video tool card
# in the admin AI settings, and the token lands in $HOME/.mokaair (a volume), never in the log.
# Then `auto` runs every few minutes; each run does units of work until every video waits on the
# owner or the next draft is not due, and exits. The settings decide everything else, including
# whether anything happens at all.
set -u
cd /opt/mokaair || exit 1
interval="${VIDEO_WORKER_INTERVAL_SECONDS:-300}"
credentials="$HOME/.mokaair/video-tool.json"

while :; do
  if [ ! -s "$credentials" ]; then
    echo "video-worker: not paired yet; allow the code below on the video tool card within 10 minutes"
    # The token is stored against the public site; MOKAAIR_SITE only redirects calls at run time.
    if ! env -u MOKAAIR_SITE node tools/video/cli.mjs login --name "video-worker"; then
      # The site allows few pairing starts an hour, so wait longer before offering a new code.
      sleep 900
      continue
    fi
  fi
  # Inside compose, calls go straight to the web container instead of out through nginx.
  MOKAAIR_SITE="${VIDEO_INTERNAL_SITE:-}" node tools/video/cli.mjs auto
  status=$?
  [ "$status" -eq 0 ] || echo "video-worker: auto exited with $status"
  sleep "$interval"
done
