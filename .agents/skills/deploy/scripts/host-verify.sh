#!/usr/bin/env bash
# Post-deploy verification for travel_scanner on the production host: one read-only script, one SSH
# connection, every check prints "PASS <id> <measured values>" or "FAIL <id> <measured values>" and the
# end prints "TOTAL pass=<n> fail=<n>". Send it as a file:
#
#   TMP=$(mktemp -d)   # any scratch directory outside the repo
#   sed 's/^EXPECTED_SHA=""$/EXPECTED_SHA="<squash sha>"/' host-verify.sh > "$TMP/verify.sh"
#   MSYS_NO_PATHCONV=1 <SSH> -m "$TMP/verify.sh"
#
# `plink -m` passes no positional arguments, so EXPECTED_SHA is filled in before sending ($1 also works
# when a transport does pass arguments). ALEMBIC_HEAD and UP_COUNT are the values of 2026-10-03; update
# them when a migration lands or a compose service is added, and the check will say so when they drift.
#
# Strictly read-only: git log/merge-base/status, a flock -n probe, docker inspect/logs, compose ps and
# `exec -T` one-liners that only read files, curl to 127.0.0.1:8090/8091 and exactly two sequential
# requests to https://mokaair.com (>= 1.2 s apart, the edge allows 5 r/s). No ps/who/last, no docker
# images, nothing reads .env, nothing writes. The permission classifier has let this shape through.
#
# This file holds the checks every deploy needs. The deploy-specific ones ("is the NEW code running?")
# go in the EXTRA CHECKS section near the end: read references/post-deploy.md for the three patterns
# (a python one-liner in the api container, a grep or node import in video-worker, a manifest grep in
# web) and for designing them with a propose/refute workflow when the deploy is large.
set -u

EXPECTED_SHA=""
ALEMBIC_HEAD="0122_video_anime_production"
UP_COUNT=13   # postgres, redis and the eleven app containers of docker-compose.prod.yml (all profiles)

REPO=/root/travel_scanner
COMPOSE="docker compose -f docker-compose.prod.yml"
PASS_N=0
FAIL_N=0

verdict() { # id ok(1/0) detail
  if [ "$2" -eq 1 ]; then
    echo "PASS $1 $3"; PASS_N=$((PASS_N + 1))
  else
    echo "FAIL $1 $3"; FAIL_N=$((FAIL_N + 1))
  fi
}
section() { echo; echo "== $1 =="; }
epoch() { # RFC3339(Nano) -> epoch seconds; 0 when unparsable
  local s
  s=$(printf '%s' "${1:-}" | sed -E 's/\.[0-9]+(Z|[+-][0-9:]+)$/\1/')
  date -u -d "$s" +%s 2>/dev/null || echo 0
}
count() { # count lines matching a regex in stdin (always prints a number)
  grep -cE "$1" || true
}

echo "== post-deploy verify $(date -u +%FT%TZ) =="
cd "$REPO" || { echo "FAIL cannot cd $REPO"; echo "TOTAL pass=0 fail=1"; echo "== end =="; exit 1; }

live_full=$(git rev-parse HEAD 2>/dev/null)
live_short=$(git rev-parse --short HEAD 2>/dev/null)
head_ct=$(git log -1 --format=%ct HEAD 2>/dev/null)
head_ct=${head_ct:-0}
subject=$(git log -1 --format=%s HEAD 2>/dev/null)

# ---------------------------------------------------------------- 1 live-head-and-deploy-gate
section live-head-and-deploy-gate
echo "live_head=$live_short $subject"
echo "head_committed=$(date -u -d @"$head_ct" +%FT%TZ 2>/dev/null)"
exp=$(printf '%s' "${1:-$EXPECTED_SHA}" | tr 'A-F' 'a-f')
sha_ok=0
if [ -z "$exp" ]; then
  echo "SHA MISMATCH (no expected SHA supplied: pass it as \$1 or set EXPECTED_SHA at the top)"
else
  case "$live_full" in
    "$exp"*) sha_ok=1; echo "SHA ok $live_full" ;;
    *) echo "SHA MISMATCH live=${live_full:-unknown} expected=$exp" ;;
  esac
fi
dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if flock -n /var/lock/travel-scanner-deploy.lock true 2>/dev/null; then lock=free; else lock=HELD; fi
if [ -f /root/travel-scanner-deploy.hold ]; then hold=PRESENT; else hold=none; fi
echo "dirty_lines=$dirty lock=$lock hold=$hold"
[ "$lock" = HELD ] && echo "WARN deploy lock is HELD: a deploy is still running, everything below describes a moving target"
ok=0
if [ "$sha_ok" -eq 1 ] && [ "$dirty" = 0 ] && [ "$lock" = free ] && [ "$hold" = none ]; then ok=1; fi
verdict live-head-and-deploy-gate "$ok" "sha_ok=$sha_ok head=$live_short dirty=$dirty lock=$lock hold=$hold"

# ---------------------------------------------------------------- 2 deploy-logs
section deploy-logs
rel=$(find /root -maxdepth 2 -path '/root/mokaair-*' -name state.json -mmin -1440 2>/dev/null | wc -l | tr -d ' ')
echo "release state.json touched <24h: $rel"
echo '-- newest deploy logs --'
ls -lt --time-style=+%FT%TZ /root/deploy-logs 2>/dev/null | head -4
# Only the logs written since the live HEAD commit: two through host-deploy.sh (wrapper + script), one
# when the owner ran /root/deploy-travel-scanner.sh directly.
logs_n=0; logs_fresh=0; logs_33=0; logs_rb=0
for f in $(find /root/deploy-logs -maxdepth 1 -name '*.log' -newermt "@$head_ct" 2>/dev/null | xargs -r ls -t | head -2); do
  logs_n=$((logs_n + 1))
  mt=$(stat -c %Y "$f" 2>/dev/null || echo 0)
  echo "== $f (mtime $(date -u -d @"$mt" +%FT%TZ 2>/dev/null))"
  grep -v -E '^#[0-9]+ ' "$f" | tail -4
  c33=$(count '3/3' <"$f"); rb=$(grep -ciE 'rolling back|rolled back' "$f" || true)
  echo "   lines with 3/3: $c33   rollback lines: $rb"
  if [ "$mt" -ge "$head_ct" ]; then logs_fresh=$((logs_fresh + 1)); else echo "   -> older than the live HEAD commit"; fi
  [ "$c33" -ge 1 ] && logs_33=$((logs_33 + 1))
  [ "$rb" -gt 0 ] && logs_rb=$((logs_rb + 1))
done
# The script's "health 3/3 ok" is printed AFTER a rollback too (2026-09-29): a rollback line with a
# matching SHA means the previous attempt rolled back and this one deployed; without the SHA it failed.
ok=0
if [ "$logs_n" -ge 1 ] && [ "$logs_fresh" -eq "$logs_n" ] && [ "$logs_33" -eq "$logs_n" ] && { [ "$logs_rb" -eq 0 ] || [ "$sha_ok" -eq 1 ]; }; then ok=1; fi
verdict deploy-logs "$ok" "logs_newer_than_head_commit=$logs_n (2 via host-deploy.sh, 1 when the owner ran the deploy script directly) with_3of3=$logs_33 with_rollback_lines=$logs_rb release_state_json=$rel"

# A service is rebuilt and recreated only when its build context changed: `up --build -d` without
# --force-recreate keeps a container whose image id did not move. So "fresh" means "newer than the
# last commit that touched that service's build context", not "newer than HEAD" (a docs-only or
# tools/video-only commit leaves api and web exactly as they were, and that is correct).
api_ct=$(git log -1 --format=%ct HEAD -- apps/api 2>/dev/null); api_ct=${api_ct:-0}
web_ct=$(git log -1 --format=%ct HEAD -- apps/web package.json package-lock.json 2>/dev/null); web_ct=${web_ct:-0}
vw_ct=$(git log -1 --format=%ct HEAD -- tools/video ops/video .agents/skills/youtube-video docs/videos apps/api/app/guides/content 2>/dev/null); vw_ct=${vw_ct:-0}
cutoff_for() { case "$1" in travel_scanner-web-1|web) echo "$web_ct" ;; travel_scanner-video-worker-1|video-worker) echo "$vw_ct" ;; *) echo "$api_ct" ;; esac; }
echo "build-context cutoffs: api/worker $(date -u -d @"$api_ct" +%FT%TZ 2>/dev/null) web $(date -u -d @"$web_ct" +%FT%TZ 2>/dev/null) video-worker $(date -u -d @"$vw_ct" +%FT%TZ 2>/dev/null)"

# ---------------------------------------------------------------- 3 containers-up-local-images-disk
section containers-up-local-images-disk
ps_out=$($COMPOSE --profile hotspots --profile news --profile video ps -a --format '{{.Name}} {{.Image}} {{.Status}}' 2>&1 | sort)
echo "$ps_out"
up_n=$(echo "$ps_out" | count ' Up')
nonlocal=$(echo "$ps_out" | grep ' Up' | grep -vE ' (postgres|redis):' | grep -vc ':local ' || true)
bad_state=$(echo "$ps_out" | grep -ciE 'restarting|unhealthy' || true)
migrate_ok=$(echo "$ps_out" | count '^travel_scanner-migrate-1 .*Exited \(0\)')
echo '-- state --'
not_running=0; restarts_bad=0; old_start=0
for name in $(echo "$ps_out" | grep ' Up' | awk '{print $1}'); do
  st=""; rc=""; sa=""
  read -r st rc sa <<< "$(docker inspect -f '{{.State.Status}} {{.RestartCount}} {{.State.StartedAt}}' "$name" 2>/dev/null)"
  echo "$name $st restarts=$rc started=$sa"
  [ "$st" = running ] || not_running=$((not_running + 1))
  [ "${rc:-1}" = 0 ] || restarts_bad=$((restarts_bad + 1))
  case "$name" in
    travel_scanner-postgres-1|travel_scanner-redis-1) ;;
    *) [ "$(epoch "$sa")" -ge "$(cutoff_for "$name")" ] || { echo "   -> started before the last commit that touched its build context (not recreated by this deploy)"; old_start=$((old_start + 1)); } ;;
  esac
done
echo '-- disk --'
df -h / /var/lib/containerd 2>/dev/null | sort -u
disk_pct=$(df -P / /var/lib/containerd 2>/dev/null | awk 'NR>1 {v=$(NF-1); sub("%","",v); if (v+0>m) m=v+0} END{print m+0}')
ok=0
if [ "$up_n" -eq "$UP_COUNT" ] && [ "$nonlocal" -eq 0 ] && [ "$bad_state" -eq 0 ] && [ "$migrate_ok" -eq 1 ] \
   && [ "$not_running" -eq 0 ] && [ "$restarts_bad" -eq 0 ] && [ "$old_start" -eq 0 ] && [ "$disk_pct" -lt 80 ]; then ok=1; fi
verdict containers-up-local-images-disk "$ok" "up=$up_n/$UP_COUNT non_local_app_images=$nonlocal restarting_or_unhealthy=$bad_state migrate_exited0=$migrate_ok not_running=$not_running restarts_nonzero=$restarts_bad app_started_before_head=$old_start disk_use_pct=$disk_pct"

# ---------------------------------------------------------------- 4 containers-rebuilt-this-deploy
section containers-rebuilt-this-deploy
rb_ok=1; api_img=""; worker_img=""; rebuilt_n=0
for c in api worker web video-worker; do
  n=travel_scanner-$c-1
  id=$(docker inspect -f '{{.Image}}' "$n" 2>/dev/null) || { echo "$c: no container"; rb_ok=0; continue; }
  started=$(docker inspect -f '{{.State.StartedAt}}' "$n" 2>/dev/null)
  created=$(docker inspect -f '{{.Created}}' "$id" 2>/dev/null)
  echo "$c started=$started image=${id#sha256:} image_created=$created"
  fresh=1; cut=$(cutoff_for "$c")
  [ "$(epoch "$created")" -ge "$cut" ] || { echo "   -> image built before the last commit that touched its build context (stale image)"; fresh=0; }
  [ "$(epoch "$started")" -ge "$cut" ] || { echo "   -> container started before the last commit that touched its build context"; fresh=0; }
  if [ "$fresh" -eq 1 ]; then rebuilt_n=$((rebuilt_n + 1)); else rb_ok=0; fi
  [ "$c" = api ] && api_img=$id
  [ "$c" = worker ] && worker_img=$id
done
same_img=0
if [ -n "$api_img" ] && [ "$api_img" = "$worker_img" ]; then same_img=1; else rb_ok=0; echo "api/worker image ids differ or missing"; fi
verdict containers-rebuilt-this-deploy "$rb_ok" "rebuilt_after_context_commit=$rebuilt_n/4 api_worker_same_image=$same_img"

# ---------------------------------------------------------------- 5 alembic-head
section alembic-head
out=$($COMPOSE exec -T api alembic current 2>&1)
revs=$(echo "$out" | grep -E '^0[0-9]{3}_' || true)
if [ -n "$revs" ]; then echo "$revs"; else echo "no revision line; raw output:"; echo "$out" | tail -5; fi
rev_n=$(echo "$revs" | count '^0[0-9]{3}_')
ok=0
if [ "$rev_n" -eq 1 ]; then case "$revs" in "$ALEMBIC_HEAD (head)"*) ok=1 ;; esac; fi
verdict alembic-head "$ok" "revision_lines=$rev_n current=$(echo "$revs" | head -1 | tr -d '\r') expected=$ALEMBIC_HEAD"

# ---------------------------------------------------------------- 6 api-health-ready-200
section api-health-ready-200
h_ok=1; h_detail=""
for p in health ready; do
  r=$(curl -s -o /dev/null -m 10 -w '%{http_code} %{time_total}s' "127.0.0.1:8090/$p")
  echo "api /$p $r"
  case "$r" in 200*) ;; *) h_ok=0 ;; esac
  h_detail="$h_detail /$p=${r%% *}"
done
verdict api-health-ready-200 "$h_ok" "${h_detail# }"

# ---------------------------------------------------------------- 7 api-log-no-traceback
section api-log-no-traceback
since=$(docker inspect -f '{{.State.StartedAt}}' travel_scanner-api-1 2>/dev/null)
echo "api log since ${since:-<no container>}"
tb=0; su=0; ln=0
if [ -n "$since" ]; then
  log=$(docker logs --since "$since" travel_scanner-api-1 2>&1)
  tb=$(echo "$log" | count 'Traceback')
  su=$(echo "$log" | count 'Application startup complete')
  ln=$(echo "$log" | wc -l | tr -d ' ')
  echo "api since start: Traceback=$tb startup_complete=$su lines=$ln"
  echo "$log" | grep -E 'Application startup complete|Uvicorn running|Traceback' | head -5
fi
ok=0; [ "$tb" -eq 0 ] && [ "$su" -ge 1 ] && ok=1
verdict api-log-no-traceback "$ok" "Traceback=$tb startup_complete=$su lines=$ln"

# ---------------------------------------------------------------- 8 admin-routes-mounted-and-guarded
section admin-routes-mounted-and-guarded
# 401 = router mounted and the guard answers; 404 = router not mounted; 502/504 on the bff line = web
# cannot reach api. An unauthenticated POST answers 403 whether or not the route exists, so only GETs.
r_ok=1; r_detail=""
for pair in "api-admin-settings 127.0.0.1:8090/api/v1/admin/video-automation/settings" \
            "bff-admin-settings 127.0.0.1:8091/api/travel/admin/video-automation/settings" \
            "api-tool-settings 127.0.0.1:8090/api/v1/video/automation/settings"; do
  label=${pair%% *}; url=${pair##* }
  code=$(curl -s -o /dev/null -m 10 -w '%{http_code}' "$url")
  echo "$label $code"
  [ "$code" = 401 ] || r_ok=0
  r_detail="$r_detail $label=$code"
done
verdict admin-routes-mounted-and-guarded "$r_ok" "${r_detail# }"

# ---------------------------------------------------------------- 9 web-home-200-under-1s
section web-home-200-under-1s
# Measured inside the host: from a laptop the same page takes 1.1-1.3 s of network time (2026-09-30).
r1=$(curl -s -o /dev/null -m 10 -w '%{http_code} %{time_total}' 127.0.0.1:8091/zh-TW); echo "web /zh-TW #1 $r1"
sleep 1
r2=$(curl -s -o /dev/null -m 10 -w '%{http_code} %{time_total}' 127.0.0.1:8091/zh-TW); echo "web /zh-TW #2 $r2"
tag=$(curl -s -m 10 127.0.0.1:8091/zh-TW | grep -o '<html[^>]*>' | head -1 | cut -c1-120); echo "html tag: $tag"
code2=${r2%% *}; t2=${r2##* }
fast=$(awk -v t="$t2" 'BEGIN{print (t+0 < 1.0) ? 1 : 0}')
lang_ok=0; case "$tag" in *'lang="zh-TW"'*) lang_ok=1 ;; esac
ok=0; [ "$code2" = 200 ] && [ "$fast" -eq 1 ] && [ "$lang_ok" -eq 1 ] && ok=1
verdict web-home-200-under-1s "$ok" "second_request=$code2 time=${t2}s under_1s=$fast lang_zh_TW=$lang_ok first_request=${r1%% *}"

# ---------------------------------------------------------------- 10 video-worker-started
section video-worker-started
st=""; rc=""; sa=""
read -r st rc sa <<< "$(docker inspect -f '{{.State.Status}} {{.RestartCount}} {{.State.StartedAt}}' travel_scanner-video-worker-1 2>/dev/null)"
echo "travel_scanner-video-worker-1 ${st:-<no container>} restarts=$rc started=$sa"
w_started_ok=0; [ "$(epoch "$sa")" -ge "$head_ct" ] && w_started_ok=1
wlog=$(docker logs --tail 30 travel_scanner-video-worker-1 2>&1 | grep -v '^[[:space:]]*$')
echo "$wlog" | tail -8
# The first Shorts knock right after a restart fails while api is still starting: expected, once.
knock=$(echo "$wlog" | count 'the knock failed')
exited=$(echo "$wlog" | count 'auto exited with')
unpaired=$(echo "$wlog" | count 'not paired yet')
echo "knock_failed=$knock (1 right after start is expected) auto_exited=$exited not_paired=$unpaired"
ok=0
if [ "$st" = running ] && [ "${rc:-1}" = 0 ] && [ "$w_started_ok" -eq 1 ] && [ "$knock" -le 1 ] && [ "$exited" -eq 0 ] && [ "$unpaired" -eq 0 ]; then ok=1; fi
verdict video-worker-started "$ok" "state=${st:-none} restarts=${rc:-?} started_after_head=$w_started_ok knock_failed=$knock auto_exited=$exited not_paired=$unpaired"

# ---------------------------------------------------------------- EXTRA CHECKS: this deploy's new code
# Add one section per thing the diff changed, each proving a string or behaviour that exists only
# AFTER the change (pick it from the diff; the pre-change image must print the opposite). Patterns:
#
#   api, one python read:
#     section api-<what>
#     out=$($COMPOSE exec -T -e PYTHONIOENCODING=utf-8 api python -c 'import pathlib; t = pathlib.Path("/app/app/<module>.py").read_text(encoding="utf-8"); print("marker=%d" % t.count("<string only after the change>"))' 2>&1)
#     ok=0; [ "$(echo "$out" | count '^marker=1$')" -eq 1 ] && ok=1; verdict api-<what> "$ok" "$out"
#   video-worker, a grep (its code lives under /opt/mokaair) or a node import that calls the new function:
#     section worker-<what>
#     out=$($COMPOSE --profile video exec -T video-worker sh -c 'cd /opt/mokaair && grep -c "<symbol>" tools/video/<file>.mjs' 2>&1)
#     ok=0; [ "$(echo "$out" | tr -d '\r')" = "<expected count>" ] && ok=1; verdict worker-<what> "$ok" "count=$out"
#     out=$($COMPOSE --profile video exec -T video-worker node --input-type=module -e 'import { f } from "/opt/mokaair/tools/video/<file>.mjs"; console.log(JSON.stringify(f(<input>)))' 2>&1)
#     ok=0; [ "$(echo "$out" | tail -1)" = '<expected JSON>' ] && ok=1; verdict worker-<what> "$ok" "$out"
#   web (busybox: no grep --include), the standalone copy of the manifest:
#     section web-<package>-version
#     out=$($COMPOSE exec -T web sh -c 'grep -o "\"<package>\": \"[^\"]*\"" /app/apps/web/package.json' 2>&1)
#     ok=0; case "$out" in *'"<version>"'*) ok=1 ;; esac; verdict web-<package>-version "$ok" "$out"
#
# Every check is `section <id>` + the command + `ok=...` + `verdict <id> "$ok" "<values>"`: only verdict
# lines reach PASS/FAIL and TOTAL, so a check without one is invisible to the gate.
# Non-ASCII in a one-liner goes in as code points (python chr(), node String.fromCharCode) so the
# transport cannot mangle it. psql only for the simplest single select; jsonb operators get blocked.

# ---------------------------------------------------------------- last: public-edge-two-requests
section public-edge-two-requests
p1=$(curl -s -o /dev/null -m 10 -w '%{http_code} %{time_total}' https://mokaair.com/zh-TW); echo "public-zh-TW $p1 (time is network-informational)"
sleep 1.2
p2=$(curl -s -o /dev/null -m 10 -w '%{http_code}' https://mokaair.com/); echo "public-root $p2"
# A 502 with every container Up is the 8-second recreation gap: run the script again.
ok=0; [ "${p1%% *}" = 200 ] && [ "$p2" = 307 ] && ok=1
verdict public-edge-two-requests "$ok" "zh-TW=${p1%% *} root=$p2"

echo
echo "TOTAL pass=$PASS_N fail=$FAIL_N"
echo "== end =="
