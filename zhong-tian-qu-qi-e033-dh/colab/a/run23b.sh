#!/usr/bin/env bash
# stages 2+3 on one G4 session, with a watchdog for silent `colab exec` hangs and --only retries
set -u
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/a
export COLAB_GPU=G4
S=zt33
watch_progress() { # $1 progress file: kill the colab exec if the file is stale for 8 min
  while sleep 60; do
    [ -f "$1" ] || continue
    age=$(( $(date +%s) - $(stat -c %Y "$1") ))
    if [ $age -gt 480 ]; then
      pid=$(pgrep -f "colab --auth=oauth2 exec --session $S" | head -1)
      [ -n "$pid" ] && { echo "watchdog: $1 stale ${age}s, killing colab exec $pid"; kill $pid; touch "$1"; }
    fi
  done
}
missing() { python3 -c "
import json,os,sys
m,d=sys.argv[1:]
print(','.join(j['id'] for j in json.load(open(m))['jobs'] if not os.path.exists(os.path.join(d,j['id']+'.mp4'))))" "$1" "$2"; }
echo "start $(date -u +%FT%TZ)"
colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || bash $K/h3.sh start --session $S 2>&1 | tail -1
colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || { echo "NOT G4"; exit 3; }
cd $A/st2
for p in a b c; do
  for try in 1 2 3; do
    left=$(missing st2$p.json refined-$p); [ -z "$left" ] && break
    echo "refine-$p try $try: $left $(date -u +%T)"
    watch_progress refined-$p/progress.json & W=$!
    bash $K/h3.sh refine --manifest st2$p.json --output-dir refined-$p --progress refined-$p/progress.json --session $S --only "$left" 2>&1 | tail -1
    kill $W 2>/dev/null
  done
  echo "refine-$p left: [$(missing st2$p.json refined-$p)] $(date -u +%T)"
done
mkdir -p $A/final
for p in a b c; do
  for try in 1 2; do
    n=$(ls refined-$p/*.mp4 2>/dev/null | wc -l); have=0
    for f in refined-$p/*.mp4; do [ -f "$A/final/$(basename ${f%.mp4})_1080.mp4" ] && have=$((have+1)); done
    [ $have -ge $n ] && break
    echo "upscale-$p try $try ($have/$n) $(date -u +%T)"
    bash $K/h3.sh upscale --input-dir refined-$p --output-dir $A/final --session $S 2>&1 | tail -1
  done
done
bash $K/h3.sh stop --session $S 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
