#!/usr/bin/env bash
#
# Redeploy travel_scanner from origin/main.
#
#   ./deploy-travel-scanner.sh              # deploy if origin/main is ahead
#   ./deploy-travel-scanner.sh --dry-run    # show what would happen, change nothing
#   ./deploy-travel-scanner.sh --force      # rebuild even when already up to date
#   ./deploy-travel-scanner.sh --no-rollback
#   ./deploy-travel-scanner.sh --ignore-hold  # deploy although another release is in progress
#
# Backs up PostgreSQL only when the incoming commits touch migrations, then
# fast-forwards, rebuilds, and requires three consecutive health checks.
# A failed deploy rolls the code back and rebuilds the previous commit.
# Refuses to start while a release driven by other tooling is in progress.

set -euo pipefail

# A restrictive umask is what took the site down on 2026-09-07: something ran git
# from a shell with `umask 077`, the fast-forward rewrote 55 files as -rw-------,
# the non-root user inside the images could not read them, the migrate container
# died on `PermissionError: '/app/app/models.py'`, and mokaair.com served 502 for
# two and a half minutes. Nothing about that commit was wrong. Setting the umask
# here makes every file this script's git commands write world-readable no matter
# what the invoking shell had.
umask 022

REPO=/root/travel_scanner
COMPOSE_FILE=docker-compose.prod.yml
PROFILE=hotspots
BRANCH=main

API_HEALTH=http://127.0.0.1:8090/health
API_READY=http://127.0.0.1:8090/ready
WEB_URL=http://127.0.0.1:8091/
PUBLIC_URL=https://mokaair.com/

LOG_DIR=/root/deploy-logs
BACKUP_DIR=/root
BACKUP_KEEP=3
LOCK_FILE=/var/lock/travel-scanner-deploy.lock
HOLD_FILE=/root/travel-scanner-deploy.hold

FORCE=0
NO_ROLLBACK=0
DRY_RUN=0
IGNORE_HOLD=0
# A01_EXACT_MAIN_AND_ENV_GUARD_V1: opt-in, immutable cutover inputs.
EXPECTED_MAIN_SHA=""
EXPECTED_ENV_SHA256=""
EXPECTED_REDIS_URL_SHA256=""
EXPECTED_HOLD_SHA256=""
PINNED_ENV_FILE=""
cleanup_pinned_env() {
  [[ -z "$PINNED_ENV_FILE" ]] || rm -f -- "$PINNED_ENV_FILE"
}
trap cleanup_pinned_env EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)       FORCE=1 ;;
    --no-rollback) NO_ROLLBACK=1 ;;
    --dry-run)     DRY_RUN=1 ;;
    --ignore-hold) IGNORE_HOLD=1 ;;
    --expected-main-sha=*)
      EXPECTED_MAIN_SHA=${1#*=}
      [[ $EXPECTED_MAIN_SHA =~ ^[0-9a-f]{40}$ ]] || { echo 'invalid expected main SHA' >&2; exit 2; } ;;
    --expected-env-sha256=*)
      EXPECTED_ENV_SHA256=${1#*=}
      [[ $EXPECTED_ENV_SHA256 =~ ^[0-9a-f]{64}$ ]] || { echo 'invalid expected env SHA' >&2; exit 2; } ;;
    --expected-redis-url-sha256=*)
      EXPECTED_REDIS_URL_SHA256=${1#*=}
      [[ $EXPECTED_REDIS_URL_SHA256 =~ ^[0-9a-f]{64}$ ]] || { echo 'invalid expected Redis URL SHA' >&2; exit 2; } ;;
    --expected-hold-sha256=*)
      EXPECTED_HOLD_SHA256=${1#*=}
      [[ $EXPECTED_HOLD_SHA256 =~ ^[0-9a-f]{64}$ ]] || { echo 'invalid expected hold SHA' >&2; exit 2; } ;;
    -h|--help)     sed -n '3,14p' "$0" | sed 's/^# \?//'; exit 0 ;;
    *)             echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
if [[ -n $EXPECTED_MAIN_SHA || -n $EXPECTED_ENV_SHA256 || -n $EXPECTED_REDIS_URL_SHA256 ]]; then
  [[ -n $EXPECTED_MAIN_SHA && -n $EXPECTED_ENV_SHA256 && -n $EXPECTED_REDIS_URL_SHA256 ]] || { echo 'expected SHA flags must be paired' >&2; exit 2; }
fi
if [[ -n $EXPECTED_HOLD_SHA256 ]]; then
  [[ -n $EXPECTED_MAIN_SHA && -n $EXPECTED_ENV_SHA256 && -n $EXPECTED_REDIS_URL_SHA256 && $IGNORE_HOLD -eq 1 ]] || { echo "expected hold requires pinned deploy and --ignore-hold" >&2; exit 2; }
fi

mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/deploy_$STAMP.log"
exec > >(tee -a "$LOG_FILE") 2>&1

log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
fail() { log "FAILED: $*"; exit 1; }

# Only one deploy at a time. Two concurrent runs race on `compose up` and one
# loses with "container name is already in use", leaving the tree advanced and
# the containers half-recreated. Waiting is wrong here: the other run is
# probably deploying the same origin/main, so a second pass would be a no-op.
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  holder=$(cat "$LOCK_FILE" 2>/dev/null || true)
  log "another deploy is already running${holder:+ (pid $holder)}; not starting a second one"
  exit 3
fi
echo $$ >&9

# Other tooling deploys this host too. The release drivers under /root/mokaair-*/
# (release_host.py, publish_host.py) work in phases - prepare, wait for CI, activate,
# then publish content - and every phase refuses to go on if the containers changed
# since the phase before it. They take the lock above, but only while a phase runs,
# so the lock cannot see a release that is waiting between phases. On 2026-09-14 this
# script deployed #486 between that driver's prepare and activate, and the release
# had to be reconciled by hand before it could continue.
#
# Two signals hold a deploy back: a state.json from the last 24 hours that records a
# finished build but neither an activation nor a failure, and the operator hold file,
# which covers the phases state.json does not show (publishing content after
# activation). Put the reason in the hold file and delete it when that release is done.
pending_releases() {
  local state
  while IFS= read -r state; do
    grep -q '"built_at"' "$state" || continue
    grep -qE '"(activated_at|failed_at)"' "$state" && continue
    printf '%s ' "${state%/state.json}"
  done < <(find /root -maxdepth 2 -path '/root/mokaair-*/state.json' -type f -mmin -1440 2>/dev/null)
}

if [[ -n "$EXPECTED_HOLD_SHA256" ]]; then
  [[ -f "$HOLD_FILE" && ! -L "$HOLD_FILE" ]] || fail "pinned A01 hold missing"
  actual_hold=$(sha256sum -- "$HOLD_FILE") || fail "pinned A01 hold unreadable"
  [[ "${actual_hold%% *}" == "$EXPECTED_HOLD_SHA256" ]] || fail "pinned A01 hold changed"
fi
HOLD=""
[[ -f "$HOLD_FILE" ]] && HOLD="$HOLD_FILE says: $(head -c 600 "$HOLD_FILE" | tr '\n' ' ')"
PENDING=$(pending_releases)
[[ -z "$EXPECTED_HOLD_SHA256" || -z "$PENDING" ]] || fail "another staged release appeared"
[[ -n "$PENDING" ]] && HOLD="${HOLD:+$HOLD; }built but not activated: ${PENDING% }"
if [[ -n "$HOLD" ]]; then
  if (( IGNORE_HOLD == 1 )); then
    log "WARNING: --ignore-hold given, deploying anyway. $HOLD"
  elif (( DRY_RUN == 1 )); then
    log "NOTE: a real deploy would refuse to start. $HOLD"
  else
    log "NOT DEPLOYING: another release is in progress. $HOLD"
    log "re-run with --ignore-hold only once that release has finished or been abandoned"
    exit 3
  fi
fi

assert_pinned_env() {
  [[ -z "$EXPECTED_ENV_SHA256" ]] && return 0
  [[ -f "$PINNED_ENV_FILE" && ! -L "$PINNED_ENV_FILE" ]] || fail "pinned env snapshot missing"
  [[ "${RUNTIME_ENV_FILE:-}" == "$PINNED_ENV_FILE" ]] || fail "runtime env path changed"
  local actual
  actual=$(sha256sum -- "$PINNED_ENV_FILE")
  [[ "${actual%% *}" == "$EXPECTED_ENV_SHA256" ]] || fail "pinned env snapshot changed"
}
compose() {
  if [[ -n "$PINNED_ENV_FILE" ]]; then
    assert_pinned_env
    docker compose --env-file "$PINNED_ENV_FILE" -f "$COMPOSE_FILE" --profile "$PROFILE" --profile news --profile video "$@"
  else
    docker compose -f "$COMPOSE_FILE" --profile "$PROFILE" --profile news --profile video "$@"
  fi
}
assert_pinned_redis_config() {
  [[ -z "$EXPECTED_REDIS_URL_SHA256" ]] && return 0
  if ! compose config --format json 2>/dev/null | python3 -c 'import hashlib,json,sys; d=json.load(sys.stdin); e=sys.argv[1]; snap=sys.argv[2]; s=d["services"]; required=("api","video-ai-worker"); names=tuple(n for n,v in s.items() if "REDIS_URL" in v.get("environment",{})); paths=lambda x:[v.get("path") if isinstance(v,dict) else v for v in x]; ok=set(required).issubset(names) and all(hashlib.sha256(s[n]["environment"]["REDIS_URL"].encode()).hexdigest()==e and ("env_file" not in s[n] or paths(s[n]["env_file"])==[snap]) for n in names); sys.exit(0 if ok else 1)' "$EXPECTED_REDIS_URL_SHA256" "$PINNED_ENV_FILE"; then
    fail "rendered API or video AI worker Redis URL drifted"
  fi
}

# Repair modes an earlier git run may already have left behind. The umask above only
# covers what this script writes; a `git pull` run by hand from a root shell with a
# restrictive umask still leaves the work tree unreadable to the image user, and that
# failure only shows up as the migrate container dying with the site already down.
#
# Targeted on purpose, never a recursive chmod of $REPO: .env sits at the top level
# and must stay 600. Directories that do not exist are skipped, so adding or removing
# a top-level directory in the repo cannot abort a deploy through `set -e`.
ensure_readable() {
  local d
  for d in apps ops tools docs tasks; do
    [[ -d "$d" ]] || continue
    find "$d" -type d ! -perm -005 -exec chmod a+rx {} +
    find "$d" -type f ! -perm -004 -exec chmod a+r {} +
  done
}

cd "$REPO"

# ---------------------------------------------------------------- preflight
[[ -n "$(git status --porcelain)" ]] && fail "working tree is dirty - commit, stash or clean it first
$(git status --short)"

log "fetching origin"
git fetch origin --quiet

LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse "origin/$BRANCH")
if [[ -n "$EXPECTED_MAIN_SHA" ]]; then
  [[ "$REMOTE_SHA" == "$EXPECTED_MAIN_SHA" ]] || fail "fetched main SHA changed; refusing deploy"
  [[ -f .env && ! -L .env ]] || fail "host env source missing or symlink"
  actual_env=$(sha256sum -- .env)
  [[ "${actual_env%% *}" == "$EXPECTED_ENV_SHA256" ]] || fail "host env source changed; refusing deploy"
  PINNED_ENV_FILE=$(mktemp /run/mokaair-a01-deploy-env.XXXXXXXX)
  cat -- .env > "$PINNED_ENV_FILE"
  chmod 600 "$PINNED_ENV_FILE"
  assert_pinned_env
  export RUNTIME_ENV_FILE="$PINNED_ENV_FILE"
fi
BEHIND=$(git rev-list --count "HEAD..$REMOTE_SHA")
AHEAD=$(git rev-list --count "$REMOTE_SHA..HEAD")

(( AHEAD > 0 )) && fail "local is $AHEAD commit(s) ahead of origin/$BRANCH - refusing to deploy a diverged tree"

log "local     $(git log -1 --format='%h %s')"
log "origin    $(git log -1 "$REMOTE_SHA" --format='%h %s')"

if (( BEHIND == 0 )); then
  if (( FORCE == 0 )); then
    log "already up to date - nothing to do (use --force to rebuild anyway)"
    exit 0
  fi
  log "already up to date, but --force given: rebuilding current commit"
else
  log "$BEHIND new commit(s):"
  git log --oneline "HEAD..$REMOTE_SHA" | sed 's/^/    /'
fi

# ------------------------------------------------------------ change survey
NEEDS_BACKUP=0
if (( BEHIND > 0 )); then
  if git diff --name-only HEAD "$REMOTE_SHA" | grep -qE 'migrations/versions/'; then
    NEEDS_BACKUP=1
    log "migrations change -> database backup required"
    git diff --name-status HEAD "$REMOTE_SHA" -- '*migrations/versions/*' | sed 's/^/    /'
  else
    log "no migration changes -> skipping database backup"
  fi

  if git diff --quiet HEAD "$REMOTE_SHA" -- "$COMPOSE_FILE"; then :; else
    log "NOTE: $COMPOSE_FILE changes in this update - review it after deploying"
  fi

  # Report .env.example keys that are not present in the live .env.
  NEW_KEYS=$(git diff HEAD "$REMOTE_SHA" -- .env.example \
    | sed -n 's/^+\([A-Z][A-Z0-9_]*\)=.*/\1/p' || true)
  for key in $NEW_KEYS; do
    grep -q "^${key}=" .env || log "NOTE: new setting $key is not in .env (code default applies)"
  done
fi

if (( DRY_RUN == 1 )); then
  log "--dry-run: stopping before any change"
  exit 0
fi

# ----------------------------------------------------------------- backup
if (( NEEDS_BACKUP == 1 )); then
  DUMP="$BACKUP_DIR/travel_scanner_predeploy_${STAMP}.dump"
  log "backing up database -> $DUMP"
  compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$DUMP" \
    || fail "database backup failed - not deploying"
  [[ -s "$DUMP" ]] || fail "database backup is empty - not deploying"
  log "backup ok ($(du -h "$DUMP" | cut -f1))"

  # Rotate: keep only the newest $BACKUP_KEEP dumps this script made. Backups
  # taken by hand under any other name are never touched, and the dump above is
  # the newest so it always survives.
  mapfile -t STALE < <(
    ls -1t "$BACKUP_DIR"/travel_scanner_predeploy_*.dump 2>/dev/null |
      tail -n +$(( BACKUP_KEEP + 1 ))
  )
  if (( ${#STALE[@]} > 0 )); then
    log "rotating backups, keeping the newest $BACKUP_KEEP"
    for old in "${STALE[@]}"; do
      rm -f -- "$old" && log "    removed $(basename "$old")"
    done
  fi
fi

# ----------------------------------------------------------------- health
http_code() { curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$1" || echo 000; }

check_once() {
  local api ready web
  api=$(http_code "$API_HEALTH")
  ready=$(http_code "$API_READY")
  web=$(http_code "$WEB_URL")
  [[ "$api" == 200 && "$ready" == 200 && "$web" =~ ^(200|307|308)$ ]]
}

wait_healthy() {
  local need=3 streak=0 attempt=0 max=40
  while (( attempt < max )); do
    attempt=$(( attempt + 1 ))
    if check_once; then
      streak=$(( streak + 1 ))
      log "health $streak/$need ok"
      (( streak >= need )) && return 0
    else
      (( streak > 0 )) && log "health streak reset"
      streak=0
    fi
    sleep 3
  done
  return 1
}

# ----------------------------------------------------------------- deploy
log "rollback point: $(git rev-parse --short "$LOCAL_SHA")"

if (( BEHIND > 0 )); then
  git merge --ff-only "$REMOTE_SHA" --quiet || fail "fast-forward merge failed"
  log "now at $(git log -1 --format='%h %s')"
fi

# Roll the checkout back to where this run started and rebuild. Used by BOTH
# the start failure and the health failure - an aborted `compose up` leaves the
# tree advanced with half-recreated containers, which is no safer than an
# unhealthy one.
rollback() {
  local why="$1"
  if (( NO_ROLLBACK == 1 )); then
    fail "$why; --no-rollback left the new checkout in place. The video worker may be stopped or missing. Reconcile its exact container, RQ and DB receipts before any recovery; use a guarded deployment under the deploy lock, never a raw compose up. Log: $LOG_FILE"
  fi
  log "rolling back to $(git rev-parse --short "$LOCAL_SHA")"
  git reset --hard "$LOCAL_SHA" --quiet || fail "$why; rollback checkout reset failed; worker may be stopped. Log: $LOG_FILE"
  ensure_readable || fail "$why; rollback checkout permissions failed; worker may be stopped. Log: $LOG_FILE"
  /opt/travel-scanner-deploy/video_stage_drain.sh --rollback || fail "$why; video AI worker did not drain before rollback; checkout is at original SHA, worker may be stopped. Log: $LOG_FILE"
  assert_pinned_redis_config
  compose up --build -d || fail "$why, and the rollback rebuild also failed - MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"
  if wait_healthy; then
    fail "$why; rolled back to $(git rev-parse --short HEAD) and the site is healthy again"
  fi
  fail "$why AND the rollback is unhealthy - MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"
}

ensure_readable
unset VIDEO_STAGE_GUARD_REPO VIDEO_STAGE_GUARD_COMPOSE_FILE VIDEO_STAGE_DRAIN_MARKER
VIDEO_STAGE_DRAIN_NONCE=$(cat /proc/sys/kernel/random/uuid) || fail "cannot create video drain nonce"
VIDEO_STAGE_DRAIN_LOCAL_SHA=$LOCAL_SHA
VIDEO_STAGE_DRAIN_READY_FILE=/run/travel-scanner-deploy/video-ai-drain.ready.$VIDEO_STAGE_DRAIN_NONCE
export VIDEO_STAGE_DRAIN_NONCE VIDEO_STAGE_DRAIN_LOCAL_SHA VIDEO_STAGE_DRAIN_READY_FILE
trap 'rm -f -- "$VIDEO_STAGE_DRAIN_READY_FILE"; cleanup_pinned_env' EXIT
if ! /opt/travel-scanner-deploy/video_stage_drain.sh --normal; then
  log "video AI warm drain refused; worker state unknown and may be stopped"
  if (( BEHIND > 0 )); then
    git reset --hard "$LOCAL_SHA" --quiet || fail "video drain refused and checkout reset failed; worker may be stopped. Log: $LOG_FILE"
    ensure_readable || fail "video drain refused and checkout permissions failed; worker may be stopped. Log: $LOG_FILE"
  fi
  restored_sha=$(git rev-parse HEAD) || fail "video drain refused and checkout readback failed; worker may be stopped. Log: $LOG_FILE"
  restored_status=$(git status --porcelain) || fail "video drain refused and checkout status failed; worker may be stopped. Log: $LOG_FILE"
  [[ $restored_sha == "$LOCAL_SHA" && -z $restored_status ]] || fail "video drain refused; checkout restore did not read back cleanly; worker may be stopped. Log: $LOG_FILE"
  fail "video AI worker did not drain before compose up; checkout restored to original SHA; worker may be stopped. Log: $LOG_FILE"
fi
log "building and starting (profiles: $PROFILE news)"
assert_pinned_redis_config
if ! compose up --build -d; then
  log "COMPOSE UP FAILED"
  compose ps --format 'table {{.Name}}\t{{.Status}}' | sed 's/^/    /' || true
  rollback "compose up failed"
fi

log "waiting for health checks"
if wait_healthy; then
  log "healthy"
else
  log "HEALTH CHECKS FAILED after deploy"
  compose ps --format 'table {{.Name}}\t{{.Status}}' | sed 's/^/    /'
  log "--- last 30 api log lines ---"
  docker logs --tail 30 travel_scanner-api-1 2>&1 | sed 's/^/    /' || true
  log "--- last 30 web log lines ---"
  docker logs --tail 30 travel_scanner-web-1 2>&1 | sed 's/^/    /' || true
  rollback "health checks failed after deploy"
fi

# ------------------------------------------------------------------ report
log "alembic: $(compose run --rm --no-deps -T migrate alembic current 2>&1 | tail -1)"
log "public $PUBLIC_URL -> $(curl -s -o /dev/null -w '%{http_code} in %{time_total}s' -L --max-time 20 "$PUBLIC_URL")"
compose ps --format 'table {{.Name}}\t{{.Status}}' | sed 's/^/    /'
log "deployed $(git log -1 --format='%h %s')"
log "log: $LOG_FILE"
