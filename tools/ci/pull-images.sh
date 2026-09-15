#!/usr/bin/env bash
# Pull every image a later step will `docker run`, retrying what a registry drops for a moment.
#
# `docker run` pulls a missing image once and exits 125 on the first error. The requests that
# failed in CI - the registry ping, the auth token, the manifest and its config (quay.io 502,
# 504 and connection resets; auth.docker.io resets and client timeouts) - are outside dockerd's
# max-download-attempts, which retries layer downloads only, so nothing tried a second time.
# In each case a sibling job pulled the same image within seconds: it was the network or the
# registry, not the image, and not the change under test.
#
# The workflows call this in its own early step and then `docker run --pull=never`. If the pull
# list and a run line drift apart, the run fails loudly with "No such image" instead of quietly
# going back to a single unretried pull. A refusal is not retried: a tag that is gone, or a
# registry that now wants a login (Docker Hub for minio/minio on 2026-09-11), will not come
# back, and waiting would only turn a one-second failure into a three-minute one.
#
# Usage: bash tools/ci/pull-images.sh IMAGE [IMAGE...]
#   PULL_ATTEMPTS     tries per image, default 5
#   PULL_RETRY_DELAY  base backoff in seconds, multiplied by the attempt number; default 10.
#                     The tests set it to 0.
set -euo pipefail

attempts="${PULL_ATTEMPTS:-5}"
delay="${PULL_RETRY_DELAY:-10}"

if ! [[ "$attempts" =~ ^[0-9]+$ ]] || [ "$((10#$attempts))" -lt 1 ]; then
  echo "::error::PULL_ATTEMPTS must be a whole number of at least 1, not '$attempts'"
  exit 2
fi
if ! [[ "$delay" =~ ^[0-9]+$ ]]; then
  echo "::error::PULL_RETRY_DELAY must be a whole number of seconds, not '$delay'"
  exit 2
fi
if [ "$#" -eq 0 ]; then
  echo "::error::usage: pull-images.sh IMAGE [IMAGE...]"
  exit 2
fi
attempts=$((10#$attempts))
delay=$((10#$delay))

# The output goes to a file rather than through a pipe, so `status` is docker's own exit code
# (or 124 from `timeout`) and the refusal check below reads exactly what docker printed.
output="$(mktemp)"
trap 'rm -f "$output"' EXIT

for image in "$@"; do
  attempt=1
  while :; do
    status=0
    # A pull that hangs instead of failing would otherwise sit until the job timeout. Two
    # minutes is far more than these images take on a healthy runner, and it keeps five hung
    # attempts plus backoff under about twelve minutes -- inside discovery-browser's 25-minute
    # job timeout, so the job still ends on this script's error rather than being cancelled.
    timeout 120 docker pull --quiet "$image" >"$output" 2>&1 || status=$?
    cat "$output"
    if [ "$status" -eq 0 ]; then
      break
    fi
    if grep -Eqi 'denied|unauthorized|manifest unknown|not found|repository does not exist' "$output"; then
      echo "::error::docker pull $image was refused (exit $status); a refusal is not retried"
      exit 1
    fi
    if [ "$attempt" -ge "$attempts" ]; then
      echo "::error::docker pull $image failed $attempts times (last exit $status)"
      exit 1
    fi
    wait_seconds=$((attempt * delay))
    echo "::warning::docker pull $image failed (attempt $attempt/$attempts, exit $status); retrying in ${wait_seconds}s"
    sleep "$wait_seconds"
    attempt=$((attempt + 1))
  done
done
