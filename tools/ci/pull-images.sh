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
# registry that now wants a login (Docker Hub for minio/minio on 2026-09-11, quay.io on
# 2026-09-24), will not come back, and waiting would only turn a one-second failure into a
# three-minute one.
#
# One kind of "denied" is retried all the same. dockerd prints any HTTP 403 as `denied: <body>`,
# including one on a blob after the registry has already served the manifest. On 2026-09-24
# cgr.dev answered the config blob of the pinned MinIO digest with an HTML 403 page ("error
# pulling image configuration: download failed after attempts=1: denied: <!doctype html>...403
# Forbidden"), while seven other jobs pulled the same digest between 15:37 and 15:40 and the
# full-stack-smoke job of the same run pulled it 38 seconds later. So a 403 on a blob or config
# download is retried like a 502; `unauthorized` (a 401, quay.io's answer) and a denial of the
# manifest or token are still refusals.
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
    # dockerd's own image store names the step ("error pulling image configuration", "download
    # failed after attempts=N") and says `denied:`; the containerd image store prints the blob
    # URL and `403 Forbidden`. A 401 says neither, so it stays a refusal below.
    blob_denied=false
    if grep -Eqi '(error pulling image configuration|download failed after attempts|/blobs/sha256:).*(denied|403 Forbidden)' "$output"; then
      blob_denied=true
    elif grep -Eqi 'denied|unauthorized|manifest unknown|not found|repository does not exist' "$output"; then
      echo "::error::docker pull $image was refused (exit $status); a refusal is not retried"
      exit 1
    fi
    if [ "$attempt" -ge "$attempts" ]; then
      hint=""
      if [ "$blob_denied" = true ]; then
        # A 403 on the blobs of every attempt is the one case the manifest does not reveal: the
        # registry no longer serving this digest's content anonymously.
        hint=", the last a 403 on a blob download; if every attempt above got one, the registry has stopped serving this image's content anonymously"
      fi
      echo "::error::docker pull $image failed $attempts times (last exit $status)$hint"
      exit 1
    fi
    wait_seconds=$((attempt * delay))
    what="failed"
    if [ "$blob_denied" = true ]; then
      what="got a 403 on a blob download after the manifest was served"
    fi
    echo "::warning::docker pull $image $what (attempt $attempt/$attempts, exit $status); retrying in ${wait_seconds}s"
    sleep "$wait_seconds"
    attempt=$((attempt + 1))
  done
done
