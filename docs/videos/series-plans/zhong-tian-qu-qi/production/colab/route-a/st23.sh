#!/usr/bin/env bash
# st23.sh NN : stages 2 (refine) and 3 (SeedVR2 7B, batches of five) of episode NN on one G4 session,
# with a watchdog for silent `colab exec` hangs, --only retries and a fresh session if Colab takes it.
set -u
N=$1
K=${REPO:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel)}/.agents/skills/minimax-h3-colab/scripts
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e0$N-dh/colab/a
export COLAB_GPU=G4
S=zt${N}r
echo "start $(date -u +%FT%TZ)"
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
ensure() { colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || bash $K/h3.sh start --session $S 2>&1 | tail -1; colab sessions 2>&1 | grep -q "$S.*Hardware: G4"; }
ensure || { echo "NOT G4"; exit 3; }
watch_progress() { while sleep 60; do f=$(ls -t $A/st2/refined/progress-*.json 2>/dev/null | head -1); [ -n "$f" ] || continue
  age=$(( $(date +%s) - $(stat -c %Y "$f") )); if [ $age -gt 600 ]; then pid=$(pgrep -f "colab --auth=oauth2 exec --session $S" | head -1)
  [ -n "$pid" ] && { echo "watchdog: $f stale ${age}s, killing $pid"; kill $pid; touch "$f"; }; fi; done; }
missing() { python3 -c "
import json,os,sys
print(','.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs'] if not os.path.exists(os.path.join(sys.argv[2],j['id']+'.mp4'))))" "$1" "$2"; }
cd $A/st2; mkdir -p refined $A/final
watch_progress & W=$!
for m in st2-*.json; do
  for try in 1 2 3; do
    left=$(missing $m refined); [ -z "$left" ] && break
    ensure || { echo "session lost"; break 2; }
    echo "refine $m try $try: $left $(date -u +%T)"
    bash $K/h3.sh refine --manifest $m --output-dir refined --progress refined/progress-${m%.json}-$try.json --session $S --only "$left" 2>&1 | tail -1
  done
  echo "refine $m left: [$(missing $m refined)] $(date -u +%T)"
done
kill $W 2>/dev/null
mkdir -p $A/st3; rm -rf $A/st3/up-*; i=0
for f in refined/*.mp4; do s=$(basename $f .mp4); [ -f $A/final/${s}_1080.mp4 ] && continue; d=$A/st3/up-$((i/5+1)); mkdir -p $d; ln -sf $PWD/$f $d/; i=$((i+1)); done
for d in $(ls -d $A/st3/up-* 2>/dev/null); do
  for try in 1 2 3; do
    left=0; for f in $d/*.mp4; do [ -f $A/final/$(basename ${f%.mp4})_1080.mp4 ] || left=$((left+1)); done
    [ $left -eq 0 ] && break
    ensure || { echo "session lost"; break 2; }
    echo "upscale $(basename $d) try $try ($left left) $(date -u +%T)"
    timeout 1800 bash $K/h3.sh upscale --input-dir $d --output-dir $A/final --session $S --timeout 1500 2>&1 | tail -1
  done
done
echo "have $(ls $A/final/*_1080.mp4 2>/dev/null | wc -l) finals"
bash $K/h3.sh stop --session $S 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
