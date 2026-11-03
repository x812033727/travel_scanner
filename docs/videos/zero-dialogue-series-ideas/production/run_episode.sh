#!/usr/bin/env bash
# One episode on the shared Colab session: first frames one image at a time under a hard timeout
# (a hung `colab exec` costs at most PER_IMAGE seconds), then the clips with the detached runner.
#   run_episode.sh <episode workdir> [session]
set -u
EP="$1"; SESSION="${2:-wj-clips}"
REPO=/home/user/travel_scanner
W="$EP/colab"; PER_IMAGE=${PER_IMAGE:-300}
cd "$REPO"
ids=$(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$W/ff.json'))['jobs']))")
mkdir -p "$W/ff"
for id in $ids; do
  for attempt in 1 2 3; do
    [ -s "$W/ff/$id.png" ] && break
    echo "$(date -u +%T) image $id attempt $attempt"
    timeout -k 10 "$PER_IMAGE" bash .agents/skills/minimax-h3-colab/scripts/h3.sh images --manifest "$W/ff.json" \
      --output-dir "$W/ff" --progress "$W/ff-$id.progress.json" --only "$id" --session "$SESSION" > "$W/ff-$id.log" 2>&1
    pkill -f "exec --session $SESSION --timeout 1800 --env QIE" 2>/dev/null
  done
  [ -s "$W/ff/$id.png" ] && echo "$(date -u +%T) image $id ok" || echo "$(date -u +%T) image $id FAILED"
done
echo "$(date -u +%T) clips start"
python3 -I .agents/skills/minimax-h3-colab/scripts/h3_detached.py "$W/clips.json" --session "$SESSION" > "$W/clips-run.log" 2>&1
tail -n 2 "$W/clips-run.log"
echo "$(date -u +%T) episode done: $EP"
