#!/usr/bin/env bash
# Final paid-stage barrier before either compose up in /root/deploy-travel-scanner.sh.
# The caller holds the deploy flock. The ready receipt binds a rollback to the
# successful normal drain in that same deployment, including a zero-container
# state left by a partially failed compose up.
set -euo pipefail

REPO=${VIDEO_STAGE_GUARD_REPO:-/root/travel_scanner}
COMPOSE_FILE=${VIDEO_STAGE_GUARD_COMPOSE_FILE:-docker-compose.prod.yml}
MARKER=${VIDEO_STAGE_DRAIN_MARKER:-/run/travel-scanner-deploy/video-ai-drain.pending}
NONCE=${VIDEO_STAGE_DRAIN_NONCE:-}
LOCAL_SHA=${VIDEO_STAGE_DRAIN_LOCAL_SHA:-}
READY_FILE=${VIDEO_STAGE_DRAIN_READY_FILE:-}
umask 077

refuse() {
  printf 'VIDEO STAGE DRAIN REFUSED: %s\n' "$*" >&2
  exit 3
}

[[ $# -eq 1 && ( $1 == --normal || $1 == --rollback ) ]] || refuse 'expected --normal or --rollback'
mode=$1
[[ $NONCE =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] \
  || refuse 'missing or invalid deployment nonce'
[[ $LOCAL_SHA =~ ^[0-9a-f]{40}$ ]] || refuse 'missing or invalid rollback SHA'
[[ $READY_FILE == /* && ${READY_FILE##*/} == "video-ai-drain.ready.$NONCE" ]] \
  || refuse 'invalid ready receipt path'
cd "$REPO" || refuse 'cannot enter repository'
compose=(docker compose -f "$COMPOSE_FILE" --profile video)

# An outer watchdog can kill the deploy shell while Docker is still waiting for
# the RQ horse. A second SIGTERM forces RQ shutdown; never send it while this
# marker remains. An operator must reconcile the exact worker/RQ/DB first.
[[ ! -e $MARKER && ! -L $MARKER ]] || refuse "previous warm drain is unresolved ($MARKER)"

if [[ $mode == --rollback ]]; then
  [[ -f $READY_FILE && ! -L $READY_FILE ]] || refuse 'rollback has no successful normal drain receipt'
  mapfile -t receipt < "$READY_FILE" || refuse 'cannot read normal drain receipt'
  [[ ${#receipt[@]} -eq 2 && ${receipt[0]} == "$LOCAL_SHA" && -n ${receipt[1]} ]] \
    || refuse 'rollback drain receipt does not match this deployment'
  head=$(git rev-parse HEAD) || refuse 'cannot verify rollback checkout'
  [[ $head == "$LOCAL_SHA" ]] || refuse 'rollback checkout is not the original SHA'
else
  [[ ! -e $READY_FILE && ! -L $READY_FILE ]] || refuse 'normal drain receipt already exists'
fi

# A missing worker is allowed only during rollback after a successful normal
# drain. In every other case zero/duplicate workers are a configuration fault.
ids_text=$("${compose[@]}" ps --all -q video-ai-worker) || refuse 'cannot locate video-ai-worker'
ids=()
if [[ -n $ids_text ]]; then mapfile -t ids <<< "$ids_text"; fi
if [[ $mode == --rollback && ${#ids[@]} -eq 0 ]]; then
  id=${receipt[1]}
  zero_after_normal_drain=1
else
  [[ ${#ids[@]} -eq 1 && -n ${ids[0]} ]] \
    || refuse "expected one video-ai-worker container, found ${#ids[@]}"
  id=${ids[0]}
  zero_after_normal_drain=0
  state=$(docker inspect --format '{{.State.Running}}|{{.State.ExitCode}}|{{.State.OOMKilled}}|{{json .Config.Entrypoint}}|{{json .Config.Cmd}}' "$id") \
    || refuse 'cannot inspect video-ai-worker'
  IFS='|' read -r running code oom entrypoint command <<< "$state"
  [[ $entrypoint == null && $command == '["python","-m","app.video_automation.run_jobs"]' ]] \
    || refuse "unexpected video-ai-worker command: $command"
  [[ $oom == false ]] || refuse 'video-ai-worker was OOM killed'

  if [[ $running == true ]]; then
    mkdir -p "$(dirname "$MARKER")" || refuse 'cannot create warm-drain marker directory'
    if ! (set -C; printf '%s\n' "$id" > "$MARKER"); then
      refuse "cannot create warm-drain marker ($MARKER)"
    fi
    printf 'VIDEO STAGE DRAIN: waiting for RQ warm shutdown of %s\n' "${id:0:12}"
    # Docker's ten-second default would SIGKILL a paid operation. -1 waits
    # indefinitely. If interrupted, leave the marker to block a second signal.
    docker container stop --signal=SIGTERM --timeout=-1 "$id" >/dev/null \
      || refuse 'warm stop failed; do not recreate the worker'
  elif [[ $running != false ]]; then
    refuse "invalid container running state: $running"
  fi

  current=$("${compose[@]}" ps --all -q video-ai-worker) || refuse 'cannot recheck worker identity'
  [[ $current == "$id" ]] || refuse 'video-ai-worker changed while draining'
  state=$(docker inspect --format '{{.State.Running}}|{{.State.ExitCode}}|{{.State.OOMKilled}}|{{json .Config.Entrypoint}}|{{json .Config.Cmd}}' "$id") \
    || refuse 'cannot inspect drained worker'
  IFS='|' read -r running code oom entrypoint command <<< "$state"
  [[ $running == false && $code == 0 && $oom == false ]] \
    || refuse "worker did not exit cleanly (running=$running exit=$code oom=$oom)"
fi

# Once the unique worker is stopped (or absent after this deployment's normal
# drain), queued work cannot become running before the next compose recreation.
if ! count=$("${compose[@]}" exec -T postgres psql -U travel -d travel_scanner \
  -X -q -A -t -v ON_ERROR_STOP=1 -c \
  "select count(*) from video_stage_jobs where status = 'running'"); then
  refuse 'cannot read running video_stage_jobs count'
fi
count=${count//$'\r'/}
[[ $count =~ ^[0-9]+$ ]] || refuse "invalid running count: $count"
[[ $count == 0 ]] || refuse "$count running stage job(s) remain after worker stopped"

if [[ -e $MARKER ]]; then
  [[ $(cat "$MARKER") == "$id" ]] || refuse 'warm-drain marker changed during shutdown'
  rm -- "$MARKER" || refuse 'cannot clear completed warm-drain marker'
fi
if [[ $mode == --normal ]]; then
  mkdir -p "$(dirname "$READY_FILE")" || refuse 'cannot create ready receipt directory'
  if ! (set -C; printf '%s\n%s\n' "$LOCAL_SHA" "$id" > "$READY_FILE"); then
    refuse 'cannot write normal drain receipt'
  fi
  [[ $(cat "$READY_FILE") == "$(printf '%s\n%s' "$LOCAL_SHA" "$id")" ]] \
    || refuse 'normal drain receipt readback mismatch'
fi
printf 'VIDEO STAGE DRAIN: worker stopped cleanly; running jobs=0; queued/uncertain allowed; mode=%s; zero-worker=%s\n' \
  "$mode" "$zero_after_normal_drain"
