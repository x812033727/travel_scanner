#!/usr/bin/env bash
# Root-host watcher for the exact cutover nonce. Run in the background and treat any exit,
# failed check, Redis-container replacement, or missing heartbeat as a stop condition.
set -Eeuo pipefail
# This script handles a private nonce. An inherited `bash -x`/SHELLOPTS must not
# echo command substitutions or comparisons into systemd/SSH audit logs.
set +x

job_id=b721a65d-8c8d-4ae8-834c-391cfc267a6f
key="video-media:lock:$job_id"
receipt=
redis_id=
heartbeat_dir=/run/a01-media-dispatch-fence
heartbeat="$heartbeat_dir/heartbeat.json"
while (($#)); do
  case "$1" in
    --receipt) receipt=$2; shift 2 ;;
    --redis-container-id) redis_id=$2; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
[[ $(id -u) -eq 0 && -f "$receipt" && ! -L "$receipt" ]] || exit 2
[[ "$redis_id" =~ ^[0-9a-f]{64}$ ]] || exit 2
[[ $(stat -c %a -- "$receipt") == 600 ]] || { echo 'receipt mode must be 0600' >&2; exit 3; }
nonce=$(python3 - "$receipt" "$job_id" "$key" <<'PY'
import json
import re
import sys

path, job_id, key = sys.argv[1:]
with open(path, encoding='utf-8') as stream:
    receipt = json.load(stream)
nonce = receipt.get('nonce')
if (receipt.get('job_id') != job_id or receipt.get('key') != key or
        receipt.get('durable') is not True or not isinstance(nonce, str) or
        re.fullmatch(r'[0-9a-f]{64}', nonce) is None):
    raise SystemExit('invalid or non-durable receipt')
print(nonce)
PY
)
nonce_sha256=$(printf '%s' "$nonce" | sha256sum | cut -d ' ' -f 1)
if [[ -e "$heartbeat_dir" || -L "$heartbeat_dir" ]]; then
  [[ ! -L "$heartbeat_dir" && -d "$heartbeat_dir" ]] || exit 3
  [[ $(stat -c '%u:%a' -- "$heartbeat_dir") == 0:700 ]] || exit 3
else
  mkdir -m 0700 -- "$heartbeat_dir"
fi
if [[ -e "$heartbeat" || -L "$heartbeat" ]]; then
  [[ -f "$heartbeat" && ! -L "$heartbeat" ]] || {
    echo 'heartbeat target is not an ordinary file' >&2; exit 3;
  }
fi
umask 077
verify_container() {
  # A replacement Redis may briefly coexist with the old container. Require this ID
  # to be the only running Compose Redis service, not merely a still-running old copy.
  compose_id=$(cd /root/travel_scanner && docker compose -f docker-compose.prod.yml ps -q redis)
  [[ "$compose_id" == "$redis_id" ]]
  listed=$(docker ps --no-trunc \
    --filter label=com.docker.compose.project=travel_scanner \
    --filter label=com.docker.compose.service=redis \
    --format '{{.ID}}')
  [[ "$listed" == "$redis_id" ]]
  [[ $(docker inspect --format '{{.Id}}' "$redis_id") == "$redis_id" ]]
  [[ $(docker inspect --format '{{.State.Running}}' "$redis_id") == true ]]
  [[ $(docker inspect --format '{{index .Config.Labels "com.docker.compose.project"}}' "$redis_id") == travel_scanner ]]
  [[ $(docker inspect --format '{{index .Config.Labels "com.docker.compose.service"}}' "$redis_id") == redis ]]
}
verify_container || { echo 'Redis container identity drift' >&2; exit 3; }
iteration=0
while :; do
  verify_container || { echo 'Redis container stopped or changed' >&2; exit 3; }
  observed=$(docker exec "$redis_id" sh -c 'REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli --raw GET "$1"' sh "$key")
  ttl=$(docker exec "$redis_id" sh -c 'REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli --raw TTL "$1"' sh "$key")
  [[ "$observed" == "$nonce" && "$ttl" == -1 ]] || {
    echo 'exact Redis nonce lost, replaced or expiring' >&2; exit 3;
  }
  iteration=$((iteration + 1))
  checked_at=$(date -u +%FT%TZ)
  temp=$(mktemp -- "$heartbeat_dir/.heartbeat.XXXXXXXX")
  printf '{"schema_version":1,"job_id":"%s","redis_container_id":"%s","checked_at_utc":"%s","checks":%s,"nonce_sha256":"%s","owned":true,"no_expiry":true}\n' \
    "$job_id" "$redis_id" "$checked_at" "$iteration" "$nonce_sha256" > "$temp"
  mv -- "$temp" "$heartbeat"
  if ((iteration == 1 || iteration % 15 == 0)); then
    printf 'utc=%s exact_nonce_owned=true no_expiry=true checks=%s\n' "$checked_at" "$iteration"
  fi
  sleep 2
done
