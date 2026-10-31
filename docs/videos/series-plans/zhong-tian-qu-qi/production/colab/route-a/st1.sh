#!/usr/bin/env bash
# st1.sh NN : stage 1 (960x544 hero drafts) of every part manifest of episode NN on one G4 session,
# retrying only the missing shots, with a watchdog for silent `colab exec` hangs.
set -u
N=$1
K=${REPO:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel)}/.agents/skills/minimax-h3-colab/scripts
M=${2:-${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e0$N-dh/colab/a/st1}
export COLAB_GPU=G4
S=zt${N}
cd $M
echo "start $(date -u +%FT%TZ)"
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
H3_PROFILE=hero bash $K/bootstrap.sh patch 2>&1 | grep -o "profile=[a-z]*"
ensure() { colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || bash $K/h3.sh start --session $S 2>&1 | tail -1; colab sessions 2>&1 | grep -q "$S.*Hardware: G4"; }
ensure || { echo "NOT G4"; exit 3; }
watch_progress() { while sleep 60; do f=$(ls -t out/progress-*.json 2>/dev/null | head -1); [ -n "$f" ] || continue
  age=$(( $(date +%s) - $(stat -c %Y "$f") )); if [ $age -gt 600 ]; then pid=$(pgrep -f "colab --auth=oauth2 exec --session $S" | head -1)
  [ -n "$pid" ] && { echo "watchdog: $f stale ${age}s, killing $pid"; kill $pid; touch "$f"; }; fi; done; }
missing() { python3 -c "
import json,os,sys
print(','.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs'] if not os.path.exists(j['output_path'])))" "$1"; }
watch_progress & W=$!
for p in $(ls ref-e0$N-part*.json | grep -v todo); do
  for try in 1 2 3; do
    left=$(missing $p); [ -z "$left" ] && break
    ensure || { echo "session lost"; break 2; }
    python3 - "$p" "$left" <<'PY'
import json,sys
p,left=sys.argv[1],set(sys.argv[2].split(','))
j=json.load(open(p)); j['jobs']=[x for x in j['jobs'] if x['id'] in left]
json.dump(j,open(p.replace('.json','.todo.json'),'w'),ensure_ascii=False,indent=1)
PY
    echo "$p try $try: $left $(date -u +%T)"
    bash $K/h3.sh batch --manifest ${p%.json}.todo.json --output-dir out --progress out/progress-${p%.json}-$try.json --session $S > /dev/null 2>&1
    echo "$p try $try exit=$? $(date -u +%T)"
  done
done
kill $W 2>/dev/null
echo "have $(ls out/*.mp4 2>/dev/null | wc -l) drafts"
bash $K/h3.sh stop --session $S 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
