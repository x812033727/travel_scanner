#!/bin/sh
# The video worker's loop (docs/videos/AUTOMATION.md).
#
# First refresh the docs volume from this image, keeping worker-owned files (ops/video/README.md).
# Then it pairs with the site: `login` prints a code, the owner allows it on the video tool card
# in the admin AI settings, and the token lands in $HOME/.mokaair (a volume), never in the log.
# Then `auto` runs every few minutes; each run does units of work until every video waits on the
# owner or the next draft is not due, and exits. The settings decide everything else, including
# whether anything happens at all. Beside it, the Shorts knock keeps its own timer.
# video-worker-drain-protocol: 1
set -u
cd /opt/mokaair || exit 1
node ops/video/sync-docs.mjs || exit 1
interval="${VIDEO_WORKER_INTERVAL_SECONDS:-300}"
knock_every="${VIDEO_SHORTS_KNOCK_SECONDS:-300}"
credentials="$HOME/.mokaair/video-tool.json"
stop_file="${VIDEO_WORKDIR:-/var/lib/mokaair/video-work}/STOP"
drain_file="${VIDEO_WORKDIR:-/var/lib/mokaair/video-work}/DEPLOY_DRAIN"
ready_file="$drain_file.ready"

# A deployment's STOP prevents new units. DEPLOY_DRAIN additionally asks the
# shell to wait for both foreground auto and the independent Shorts tick before
# advertising that this particular container is idle. It stays alive until the
# host has stopped it; a restart under `unless-stopped` must not resume work.
drain_if_requested() {
  [ -e "$drain_file" ] || return 1
  ready_content=""
  if [ -n "$knocker" ]; then
    wait "$knocker" || { echo "video-worker: Shorts loop did not drain" >&2; exit 1; }
    knocker=""
  fi
  if [ ! -e "$stop_file" ]; then
    echo "video-worker: DEPLOY_DRAIN lacks STOP; holding without a ready receipt" >&2
  else
    nonce=$(cat "$drain_file") || exit 1
    if [ -n "$nonce" ] && [ "$nonce" = "$(cat "$drain_file")" ]; then
      boot=$(cat /proc/sys/kernel/random/boot_id) || exit 1
      started=$(awk '{print $22}' /proc/1/stat) || exit 1
      [ -n "$boot" ] && [ -n "$started" ] || exit 1
      tmp="$ready_file.$$"
      (umask 077; set -C; printf '%s\n%s\n%s\n' "$nonce" "$boot" "$started" > "$tmp") || exit 1
      mv -f -- "$tmp" "$ready_file" || exit 1
      ready_content=$(printf '%s\n%s\n%s' "$nonce" "$boot" "$started")
      echo "video-worker: auto and Shorts drained; waiting for guarded container stop"
    fi
  fi
  while [ -e "$drain_file" ]; do sleep 1; done
  # The host owns these files. Only remove a ready receipt written by this
  # process, and never remove an owner's STOP.
  if [ -n "$ready_content" ] && [ -e "$ready_file" ] \
    && [ "$(cat "$ready_file")" = "$ready_content" ]; then
    rm -- "$ready_file"
  fi
  return 0
}

sleep_until_due_or_drain() {
  remaining=$1
  while [ "$remaining" -gt 0 ]; do
    [ ! -e "$drain_file" ] || return 0
    sleep 1
    remaining=$((remaining - 1))
  done
}

# The Shorts calendar keeps its own time (docs/videos/SHORTS.md): the knock lets the site lock
# the slots that are due, send what is due to YouTube and read the numbers, whatever the draft
# settings say. The site reports the worker silent after 15 minutes without a knock
# (apps/api/app/video_shorts/rules.py), and one `auto` round can run for most of an hour, so the
# knock runs in one background loop of its own instead of between rounds; being one loop, two
# knocks never overlap. A STOP file in the work directory pauses it like everything else. A knock
# that fails is a line in the log and nothing more.
knock_loop() {
  paused=""
  while :; do
    [ ! -e "$drain_file" ] || return 0
    if [ -e "$stop_file" ]; then
      [ -n "$paused" ] || echo "video-worker: shorts: STOP found; the knock waits until it is removed"
      paused=1
    elif [ -s "$credentials" ]; then
      [ ! -e "$drain_file" ] || return 0
      [ -z "$paused" ] || echo "video-worker: shorts: STOP removed; knocking again"
      paused=""
      # Only stderr is kept, and printed with the prefix, so its lines stay apart from `auto`'s.
      said=$(MOKAAIR_SITE="${VIDEO_INTERNAL_SITE:-}" node tools/video/shorts/cli.mjs tick 2>&1 > /dev/null) \
        || echo "video-worker: shorts: the knock failed"
      [ -z "$said" ] || printf '%s\n' "$said" | sed 's/^/video-worker: shorts: /'
    fi
    sleep_until_due_or_drain "$knock_every"
  done
}

knocker=""
trap '[ -z "$knocker" ] || kill "$knocker" 2>/dev/null' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT

while :; do
  drain_if_requested && continue
  if [ ! -s "$credentials" ]; then
    echo "video-worker: not paired yet; allow the code below on the video tool card within 10 minutes"
    # The token is stored against the public site; MOKAAIR_SITE only redirects calls at run time.
    if ! env -u MOKAAIR_SITE node tools/video/cli.mjs login --name "video-worker"; then
      # The site allows few pairing starts an hour, so wait longer before offering a new code.
      sleep_until_due_or_drain 900
      continue
    fi
  fi
  # Started once, after pairing, so it never knocks without a token.
  if [ -z "$knocker" ]; then
    knock_loop &
    knocker=$!
  fi
  # Inside compose, calls go straight to the web container instead of out through nginx.
  MOKAAIR_SITE="${VIDEO_INTERNAL_SITE:-}" node tools/video/cli.mjs auto
  status=$?
  [ "$status" -eq 0 ] || echo "video-worker: auto exited with $status"
  drain_if_requested && continue
  sleep_until_due_or_drain "$interval"
done
