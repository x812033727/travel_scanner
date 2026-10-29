#!/usr/bin/env bash
# API media-call barrier before either host-only compose up. The caller owns the
# deploy flock. This does not drain the independent shell/Node video-worker.
set -euo pipefail

REPO=${VIDEO_MEDIA_GUARD_REPO:-/root/travel_scanner}
COMPOSE_FILE=${VIDEO_MEDIA_GUARD_COMPOSE_FILE:-docker-compose.prod.yml}
MARKER=${VIDEO_MEDIA_DRAIN_MARKER:-/run/travel-scanner-deploy/video-api-drain.pending}
NONCE=${VIDEO_MEDIA_DRAIN_NONCE:-}
LOCAL_SHA=${VIDEO_MEDIA_DRAIN_LOCAL_SHA:-}
READY_FILE=${VIDEO_MEDIA_DRAIN_READY_FILE:-}
umask 077

refuse() {
  printf 'VIDEO MEDIA DRAIN REFUSED: %s\n' "$*" >&2
  exit 3
}

[[ $# -eq 1 && ( $1 == --precheck || $1 == --normal || $1 == --rollback ) ]] \
  || refuse 'expected --precheck, --normal or --rollback'
mode=$1
[[ $NONCE =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] \
  || refuse 'missing or invalid deployment nonce'
[[ $LOCAL_SHA =~ ^[0-9a-f]{40}$ ]] || refuse 'missing or invalid rollback SHA'
[[ $READY_FILE == /* && ${READY_FILE##*/} == "video-api-drain.ready.$NONCE" ]] \
  || refuse 'invalid ready receipt path'
cd "$REPO" || refuse 'cannot enter repository'
compose=(docker compose -f "$COMPOSE_FILE" --profile video)

# A killed deploy shell must not issue a second TERM to a possibly still
# running vendor request. Only an operator can reconcile and clear this marker.
[[ ! -e $MARKER && ! -L $MARKER ]] || refuse "previous API drain is unresolved ($MARKER)"

if [[ $mode == --rollback ]]; then
  [[ -f $READY_FILE && ! -L $READY_FILE ]] || refuse 'rollback lacks a normal drain receipt'
  mapfile -t receipt < "$READY_FILE" || refuse 'cannot read normal drain receipt'
  [[ ${#receipt[@]} -eq 2 && ${receipt[0]} == "$LOCAL_SHA" && -n ${receipt[1]} ]] \
    || refuse 'rollback receipt does not match this deployment'
  head=$(git rev-parse HEAD) || refuse 'cannot verify rollback checkout'
  [[ $head == "$LOCAL_SHA" ]] || refuse 'rollback checkout is not the original SHA'
else
  [[ ! -e $READY_FILE && ! -L $READY_FILE ]] || refuse 'normal drain receipt already exists'
fi

queued_count() {
  local count
  if ! count=$("${compose[@]}" exec -T postgres psql -U travel -d travel_scanner \
    -X -q -A -t -v ON_ERROR_STOP=1 -c \
    "select count(*) from video_media_jobs where status = 'queued'"); then
    refuse 'cannot read queued video_media_jobs count'
  fi
  count=${count//$'\r'/}
  [[ $count =~ ^[0-9]+$ ]] || refuse "invalid queued count: $count"
  [[ $count == 0 ]] || refuse "$count queued media job(s) may still dispatch; reconcile exact IDs before deployment"
}

unresolved_locks() {
  local locks
  if ! locks=$("${compose[@]}" exec -T redis sh -c \
    'REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli --raw --scan --pattern "video-media:lock:*"'); then
    refuse 'cannot inspect video-media Redis locks'
  fi
  [[ -z $locks ]] || refuse 'video-media Redis lock(s) remain; reconcile exact keys before deployment'
}

# Cheap first gate: the known stale queued job or an unresolved Redis lock
# refuses while the old API still serves the site. A second check after the
# graceful stop closes the arrival-after-preflight race.
queued_count
unresolved_locks

ids_text=$("${compose[@]}" ps --all -q api) || refuse 'cannot locate API container'
ids=()
if [[ -n $ids_text ]]; then mapfile -t ids <<< "$ids_text"; fi
if [[ $mode == --rollback && ${#ids[@]} -eq 0 ]]; then
  id=${receipt[1]}
  zero_after_normal_drain=1
else
  [[ ${#ids[@]} -eq 1 && -n ${ids[0]} ]] || refuse "expected one API container, found ${#ids[@]}"
  id=${ids[0]}
  zero_after_normal_drain=0
  state=$(docker inspect --format \
    '{{.State.Running}}|{{.State.ExitCode}}|{{.State.OOMKilled}}|{{json .Config.Entrypoint}}|{{json .Config.Cmd}}' "$id") \
    || refuse 'cannot inspect API container'
  IFS='|' read -r running code oom entrypoint command <<< "$state"
  [[ $entrypoint == null && $command == '["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]' ]] \
    || refuse "unexpected API command: $command"
  [[ $oom == false ]] || refuse 'API was OOM killed'
  if [[ $running == true ]]; then
    # The reviewed live image is Uvicorn 0.52.4 with no graceful timeout.
    # SIGTERM closes listeners and waits for current HTTP tasks. Refuse an
    # image/config drift before stopping it, rather than assuming grace.
    version=$("${compose[@]}" exec -T api python -c \
      'import uvicorn; from uvicorn.config import Config; c = Config("app.main:app"); print(uvicorn.__version__, c.timeout_graceful_shutdown, c.workers, c.lifespan, c.log_level, sep="|")') \
      || refuse 'cannot verify Uvicorn graceful shutdown setting'
    [[ $version == '0.52.4|None|1|auto|None' ]] \
      || refuse "unreviewed Uvicorn shutdown setting: $version"
    log_driver=$(docker inspect --format '{{.HostConfig.LogConfig.Type}}' "$id") \
      || refuse 'cannot inspect API Docker log driver'
    [[ $log_driver == json-file ]] || refuse "unreviewed API Docker log driver: $log_driver"
    docker logs --tail 1 "$id" >/dev/null 2>&1 \
      || refuse 'API Docker logs are unreadable before SIGTERM'
  elif [[ $running != false || $mode != --rollback || $id != "${receipt[1]}" || $code != 143 ]]; then
    refuse "API is not a reviewed stopped rollback container (running=$running exit=$code)"
  fi
fi

if [[ $mode == --precheck ]]; then
  [[ $zero_after_normal_drain == 0 && $running == true ]] || refuse 'precheck requires a running API'
  printf 'VIDEO MEDIA DRAIN: precheck passed; API remains running; queued=0; locks=0\n'
  exit 0
fi

# Recheck just before SIGTERM; an arrival here still finishes under Uvicorn's
# graceful shutdown and is checked after Docker reports exit 143.
queued_count
unresolved_locks
if [[ $zero_after_normal_drain == 0 && $running == true ]]; then
  mkdir -p "$(dirname "$MARKER")" || refuse 'cannot create API drain marker directory'
  stop_started_at=$(date -u +'%Y-%m-%dT%H:%M:%S.%NZ') \
    || refuse 'cannot record API stop timestamp'
  if ! (set -C; printf '%s\n%s\n' "$id" "$stop_started_at" > "$MARKER"); then
    refuse "cannot create API drain marker ($MARKER)"
  fi
  printf 'VIDEO MEDIA DRAIN: waiting for API HTTP requests to finish on %s\n' "${id:0:12}"
  # Docker's default ten-second stop escalates to SIGKILL. -1 waits without
  # escalation; Uvicorn then re-raises TERM and Docker records exit 143.
  # A hung request leaves the deploy waiting; interruption leaves
  # MARKER in place and prohibits a blind restart or second TERM.
  docker container stop --signal=SIGTERM --timeout=-1 "$id" >/dev/null \
    || refuse 'graceful API stop failed; do not recreate the API'
fi

current=$("${compose[@]}" ps --all -q api) || refuse 'cannot recheck API identity'
if [[ $zero_after_normal_drain == 0 ]]; then
  [[ $current == "$id" ]] || refuse 'API container changed during drain'
  state=$(docker inspect --format \
    '{{.State.Running}}|{{.State.ExitCode}}|{{.State.OOMKilled}}|{{json .Config.Entrypoint}}|{{json .Config.Cmd}}' "$id") \
    || refuse 'cannot inspect drained API'
  IFS='|' read -r running code oom entrypoint command <<< "$state"
  [[ $running == false && $code == 143 && $oom == false ]] \
    || refuse "API did not exit cleanly (running=$running exit=$code oom=$oom)"
  if [[ -n ${stop_started_at:-} ]]; then
    # Uvicorn 0.52.4 re-raises SIGTERM after graceful shutdown, so Docker
    # records exit 143. That exit alone does not prove tasks finished: a
    # second signal can set force_exit. Require the lifespan-complete and
    # server-finished lines, in that order, from this container after TERM.
    expected_completion=$'INFO:     Application shutdown complete.\nINFO:     Finished server process [1]'
    completion=''
    for attempt in 1 2 3 4 5; do
      logs=$(docker logs --since "$stop_started_at" "$id" 2>&1) \
        || refuse 'cannot read API completion logs after SIGTERM'
      completion=$(printf '%s\n' "$logs" | grep -Fx \
        -e 'INFO:     Application shutdown complete.' \
        -e 'INFO:     Finished server process [1]' || true)
      [[ $completion == "$expected_completion" ]] && break
      [[ $attempt == 5 ]] || sleep 1
    done
    [[ $completion == "$expected_completion" ]] \
      || refuse 'API graceful completion lines missing after SIGTERM; retain marker'
  fi
else
  [[ -z $current ]] || refuse 'API appeared after rollback zero-container check'
fi

# A queued job can be inside provider.submit before a vendor reference is
# committed. Any such row, or a lock left by a cancelled task, is a hard hold.
queued_count
unresolved_locks
if [[ -e $MARKER ]]; then
  [[ $(cat "$MARKER") == "$(printf '%s\n%s' "$id" "$stop_started_at")" ]] \
    || refuse 'API drain marker changed during shutdown'
  rm -- "$MARKER" || refuse 'cannot clear completed API drain marker'
fi
if [[ $mode == --normal ]]; then
  mkdir -p "$(dirname "$READY_FILE")" || refuse 'cannot create ready receipt directory'
  if ! (set -C; printf '%s\n%s\n' "$LOCAL_SHA" "$id" > "$READY_FILE"); then
    refuse 'cannot write normal API drain receipt'
  fi
  [[ $(cat "$READY_FILE") == "$(printf '%s\n%s' "$LOCAL_SHA" "$id")" ]] \
    || refuse 'normal API drain receipt readback mismatch'
fi
printf 'VIDEO MEDIA DRAIN: API stopped cleanly; queued=0; locks=0; mode=%s; zero-API=%s\n' \
  "$mode" "$zero_after_normal_drain"
