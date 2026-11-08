#!/usr/bin/env bash
# speed-guard.sh LOG LIMIT PATTERN : watch a retry loop's log; when a clip after the first on the
# current pod takes more than LIMIT seconds ("done in N s"), kill the processes matching PATTERN
# (the inner driver and runpod_runner.py, never the retry loop itself) so the driver's trap stops
# the pod and the retry loop starts a fresh one. Same-type GPUs ran 4-10x slower on some pods
# (e045, e046). Exits when the log says "##### done", "##### gave up" (st1-retry, st23-retry)
# or "=== batch done", "=== gave up" (retake-run).
set -u
LOG=$1; LIMIT=$2; PAT=$3
seen=0; fseen=0
while :; do
  sleep 30
  grep -q "##### done\|##### gave up\|=== batch done\|=== gave up" "$LOG" 2>/dev/null && exit 0
  # a pod whose GPU is gone fails every job at once ("ComfyUI failed", "no result after"): three
  # failures in a row since the last start means a dead pod, not a bad clip (e049 2026-11-03:
  # SeedVR2 hung 3600 s then "[Errno 6] No such device or address" on every clip).
  f=$(awk '/started pod|reusing pod|done in/{c=0} /ComfyUI failed|no result after/{c++} END{print c+0}' "$LOG")
  if [ "${f:-0}" -ge 3 ] && [ "$f" != "$fseen" ]; then
    fseen=$f
    echo "speed-guard $(date -u +%H:%M:%S): $f failures in a row, pod looks dead, switching pod" | tee -a "$LOG"
    for p in $(ps -eo pid,args | grep -E "$PAT" | grep -v -E "grep|speed-guard|retry.sh|retake-run.sh" | awk '{print $1}'); do kill "$p"; done
    sleep 5
    bash "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)/.agents/skills/minimax-h3-runpod/scripts/h3r.sh" stop || true
    continue
  fi
  # clips finished since the last "started pod" line
  n=$(awk '/started pod|reusing pod/{c=0} /done in/{c++} END{print c+0}' "$LOG")
  last=$(awk '/started pod|reusing pod/{t=""} /done in/{t=$(NF-1)} END{print t}' "$LOG")
  if [ "${n:-0}" -ge 2 ] && [ -n "$last" ] && [ "$n" != "$seen" ]; then
    seen=$n
    if awk -v a="$last" -v b="$LIMIT" 'BEGIN{exit !(a+0>b+0)}'; then
      echo "speed-guard $(date -u +%H:%M:%S): clip $n took ${last}s > ${LIMIT}s, switching pod" | tee -a "$LOG"
      for p in $(ps -eo pid,args | grep -E "$PAT" | grep -v -E "grep|speed-guard|retry.sh|retake-run.sh" | awk '{print $1}'); do kill "$p"; done
      sleep 5
      # drivers run with KEEP=1 do not stop the pod on exit: stop it here so the retry gets a new one
      bash "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)/.agents/skills/minimax-h3-runpod/scripts/h3r.sh" stop || true
      seen=0
    fi
  fi
done
