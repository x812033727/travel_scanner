#!/usr/bin/env bash
# Host-only barrier for the shell/Node video-worker, before either compose up.
# The caller owns the deployment flock. Never TERM a worker with an unproven
# auto, Shorts tick, manual exec, or descendant: a paid vendor result may be
# unknown. An interrupted attempt leaves a persistent marker and volume STOP.
set -euo pipefail

REPO=${VIDEO_WORKER_GUARD_REPO:-/root/travel_scanner}
COMPOSE_FILE=${VIDEO_WORKER_GUARD_COMPOSE_FILE:-docker-compose.prod.yml}
MARKER=${VIDEO_WORKER_DRAIN_MARKER:-/var/lib/travel-scanner-deploy/video-worker-drain.pending}
NONCE=${VIDEO_WORKER_DRAIN_NONCE:-}
LOCAL_SHA=${VIDEO_WORKER_DRAIN_LOCAL_SHA:-}
READY_FILE=${VIDEO_WORKER_DRAIN_READY_FILE:-}
WAIT_SECONDS=${VIDEO_WORKER_DRAIN_WAIT_SECONDS:-3600}
umask 077

refuse() { printf 'VIDEO WORKER DRAIN REFUSED: %s\n' "$*" >&2; exit 3; }
[[ $# -eq 1 && ( $1 == --precheck || $1 == --normal || $1 == --rollback ) ]] \
  || refuse 'expected --precheck, --normal or --rollback'
mode=$1
[[ $NONCE =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] \
  || refuse 'missing or invalid deployment nonce'
[[ $LOCAL_SHA =~ ^[0-9a-f]{40}$ ]] || refuse 'missing or invalid rollback SHA'
[[ $READY_FILE == /* && ${READY_FILE##*/} == "video-worker-drain.ready.$NONCE" ]] \
  || refuse 'invalid ready receipt path'
[[ $WAIT_SECONDS =~ ^[1-9][0-9]*$ ]] || refuse 'invalid wait bound'
cd "$REPO" || refuse 'cannot enter repository'
compose=(docker compose -f "$COMPOSE_FILE" --profile video)

[[ ! -e $MARKER && ! -L $MARKER ]] \
  || refuse "previous worker drain is unresolved ($MARKER)"
if [[ $mode == --rollback ]]; then
  [[ -f $READY_FILE && ! -L $READY_FILE ]] || refuse 'rollback lacks normal worker receipt'
  mapfile -t receipt < "$READY_FILE" || refuse 'cannot read normal worker receipt'
  [[ ${#receipt[@]} -eq 3 && ${receipt[0]} == "$LOCAL_SHA" \
    && ${receipt[1]} == "$NONCE" && -n ${receipt[2]} ]] \
    || refuse 'rollback worker receipt does not match this deployment'
  [[ $(git rev-parse HEAD) == "$LOCAL_SHA" ]] || refuse 'rollback checkout is not original SHA'
else
  [[ ! -e $READY_FILE && ! -L $READY_FILE ]] || refuse 'normal worker receipt already exists'
fi

ids_text=$("${compose[@]}" ps --all -q video-worker) || refuse 'cannot locate video-worker'
ids=()
if [[ -n $ids_text ]]; then mapfile -t ids <<< "$ids_text"; fi
if [[ $mode == --rollback && ${#ids[@]} -eq 0 ]]; then
  refuse 'rollback has no worker to verify; STOP and drain volume need owner reconciliation'
fi
[[ ${#ids[@]} -eq 1 && -n ${ids[0]} ]] \
  || refuse "expected one video-worker container, found ${#ids[@]}"
id=${ids[0]}
state=$(docker inspect --format \
  '{{.State.Running}}|{{.State.ExitCode}}|{{.State.OOMKilled}}|{{json .Config.Cmd}}' "$id") \
  || refuse 'cannot inspect video-worker'
IFS='|' read -r running code oom command <<< "$state"
[[ $oom == false && $command == '["/usr/local/bin/video-worker"]' ]] \
  || refuse "unreviewed video-worker state/command (oom=$oom command=$command)"
[[ $running == true ]] || refuse "worker not running (running=$running exit=$code)"

# The initial deployment of this protocol must be handled as a separate,
# reviewed maintenance change. An old image cannot acknowledge an in-flight
# Shorts tick or the auto child; STOP alone is not a drain receipt.
"${compose[@]}" exec -T video-worker sh -c \
  'grep -Fxq "# video-worker-drain-protocol: 1" /usr/local/bin/video-worker' \
  || refuse 'running worker lacks drain protocol 1; do not TERM the old image'

volume_state() {
  docker exec "$id" sh -eu -c '
    base=${VIDEO_WORKDIR:-/var/lib/mokaair/video-work}
    test -d "$base" && test ! -L "$base/STOP" && test ! -L "$base/DEPLOY_DRAIN" \
      && test ! -L "$base/DEPLOY_DRAIN.ready"
    if test -e "$base/DEPLOY_DRAIN"; then
      cat "$base/DEPLOY_DRAIN"
    fi
  ' || refuse 'cannot read safe worker drain volume state'
}
existing=$(volume_state)
if [[ $mode == --rollback ]]; then
  [[ $existing == "$NONCE" ]] || refuse 'rollback drain nonce missing or changed'
else
  [[ -z $existing ]] || refuse 'worker drain already present; reconcile previous attempt'
fi
if [[ $mode == --precheck ]]; then
  printf 'VIDEO WORKER DRAIN: protocol present; no active drain; worker unchanged\n'
  exit 0
fi

# Marker survives host reboots. A failed wait or interrupted deploy must block
# any second stop until the exact container, STOP, LEASE and vendor receipts are
# reconciled by the owner. Rollback reuses the same volume DRAIN nonce.
mkdir -p "$(dirname "$MARKER")" || refuse 'cannot create marker directory'
if ! (set -C; printf '%s\n%s\n%s\n' "$mode" "$NONCE" "$id" > "$MARKER"); then
  refuse "cannot create drain marker ($MARKER)"
fi
if [[ $mode == --normal ]]; then
  if ! docker exec --env "VIDEO_DRAIN_NONCE=$NONCE" "$id" sh -eu -c '
    base=${VIDEO_WORKDIR:-/var/lib/mokaair/video-work}
    drain="$base/DEPLOY_DRAIN"; stop="$base/STOP"
    test ! -e "$drain" && test ! -L "$drain" && test ! -L "$stop"
    if test ! -e "$stop"; then
      (set -C; printf "deploy-video-worker:%s\n" "$VIDEO_DRAIN_NONCE" > "$stop")
    fi
    (set -C; printf "%s\n" "$VIDEO_DRAIN_NONCE" > "$drain")
  '; then
    refuse 'cannot atomically request STOP and worker drain; retain marker'
  fi
fi

ready_probe() {
  docker exec --env "VIDEO_DRAIN_NONCE=$NONCE" "$id" sh -eu -c '
    base=${VIDEO_WORKDIR:-/var/lib/mokaair/video-work}
    test -e "$base/STOP" && test ! -L "$base/STOP"
    test "$(cat "$base/DEPLOY_DRAIN")" = "$VIDEO_DRAIN_NONCE"
    boot=$(cat /proc/sys/kernel/random/boot_id)
    started=$(awk "{print \$22}" /proc/1/stat)
    test "$(cat "$base/DEPLOY_DRAIN.ready")" = "$(printf "%s\n%s\n%s" "$VIDEO_DRAIN_NONCE" "$boot" "$started")"
  ' >/dev/null 2>&1
}

printf 'VIDEO WORKER DRAIN: waiting for auto and Shorts to finish on %s\n' "${id:0:12}"
elapsed=0
until ready_probe; do
  [[ $elapsed -lt $WAIT_SECONDS ]] \
    || refuse "worker did not acknowledge drain within ${WAIT_SECONDS}s; retain marker and STOP"
  current=$("${compose[@]}" ps --all -q video-worker) || refuse 'cannot recheck worker identity'
  [[ $current == "$id" ]] || refuse 'worker changed before drain acknowledgment'
  state=$(docker inspect --format '{{.State.Running}}|{{.State.OOMKilled}}' "$id") \
    || refuse 'cannot inspect worker while waiting'
  [[ $state == 'true|false' ]] || refuse "worker stopped before drain acknowledgment ($state)"
  sleep 1
  elapsed=$((elapsed + 1))
done

# A manual `docker compose exec` is outside PID 1's auto/Shorts accounting.
# Refuse rather than sever a manual paid command. Require only the init, idle
# worker shell and its one-second sleep in the container process table.
exec_ids=$(docker inspect --format '{{json .ExecIDs}}' "$id") \
  || refuse 'cannot inspect active manual exec sessions'
[[ $exec_ids == '[]' || $exec_ids == null ]] \
  || refuse "manual exec session remains ($exec_ids); retain marker and STOP"
init_pid=$(docker inspect --format '{{.State.Pid}}' "$id") \
  || refuse 'cannot inspect worker init PID'
[[ $init_pid =~ ^[1-9][0-9]*$ ]] || refuse 'invalid worker init PID'
processes=$(docker top "$id" -eo pid,ppid,comm) || refuse 'cannot inspect worker processes'
# Command names alone are insufficient: another manual shell or a header-only
# result used to pass the old allowlist. Prove exactly init -> worker shell ->
# optional idle sleep, tied to Docker's host PID for this container.
if ! process_proof=$(printf '%s\n' "$processes" | awk -v init="$init_pid" '
  NR == 1 { if ($1 != "PID" || $2 != "PPID" || $3 != "COMMAND" || NF != 3) bad = "unknown top header"; next }
  {
    if (NF != 3 || $1 !~ /^[0-9]+$/ || $2 !~ /^[0-9]+$/ || seen[$1]++) bad = "invalid or repeated process row"
    count++
    pid[count] = $1; parent[count] = $2; comm[count] = $3
  }
  END {
    if (count < 2 || count > 3) bad = "expected init, shell and optional sleep"
    for (i = 1; i <= count; i++) if (pid[i] == init) {
      roots++
      if (comm[i] != "tini" && comm[i] != "docker-init") bad = "unknown init command"
    }
    if (roots != 1) bad = "init PID missing from top"
    for (i = 1; i <= count; i++) if (parent[i] == init) {
      workers++
      worker = pid[i]
      if (comm[i] != "sh" && comm[i] != "video-worker") bad = "unknown worker command"
    }
    if (workers != 1) bad = "expected one child worker shell"
    for (i = 1; i <= count; i++) if (pid[i] != init && pid[i] != worker) {
      sleepers++
      if (parent[i] != worker || comm[i] != "sleep") bad = "unknown worker descendant"
    }
    if (sleepers > 1) bad = "multiple worker sleepers"
    if (bad != "") { print bad; exit 1 }
  }
'); then
  refuse "unproven worker process tree ($process_proof); retain marker and STOP"
fi
ready_probe || refuse 'worker drain acknowledgment changed before stop'

# Only after this container-specific acknowledgment may TERM reach the shell.
# The shell has no paid child now. -1 forbids Docker's default SIGKILL timer.
docker container stop --signal=SIGTERM --timeout=-1 "$id" >/dev/null \
  || refuse 'worker stop failed; retain marker and STOP'
current=$("${compose[@]}" ps --all -q video-worker) || refuse 'cannot recheck stopped worker identity'
[[ $current == "$id" ]] || refuse 'worker changed during stop'
state=$(docker inspect --format '{{.State.Running}}|{{.State.ExitCode}}|{{.State.OOMKilled}}' "$id") \
  || refuse 'cannot inspect stopped worker'
[[ $state == 'false|143|false' ]] || refuse "worker stop is unproven ($state); retain marker and STOP"
if [[ $mode == --normal ]]; then
  mkdir -p "$(dirname "$READY_FILE")" || refuse 'cannot create receipt directory'
  if ! (set -C; printf '%s\n%s\n%s\n' "$LOCAL_SHA" "$NONCE" "$id" > "$READY_FILE"); then
    refuse 'cannot write normal worker receipt; retain marker and STOP'
  fi
  [[ $(cat "$READY_FILE") == "$(printf '%s\n%s\n%s' "$LOCAL_SHA" "$NONCE" "$id")" ]] \
    || refuse 'normal worker receipt readback mismatch; retain marker and STOP'
fi
[[ $(cat "$MARKER") == "$(printf '%s\n%s\n%s' "$mode" "$NONCE" "$id")" ]] \
  || refuse 'worker drain marker changed; retain marker and STOP'
rm -- "$MARKER" || refuse 'cannot clear completed worker marker'
printf 'VIDEO WORKER DRAIN: stopped after auto and Shorts; STOP and DEPLOY_DRAIN remain; mode=%s\n' "$mode"
