#!/usr/bin/env bash
# st1.sh NN : stage 1 (960x544 hero drafts) of every part manifest of episode NN on one G4 session,
# each clip detached on the runtime (h3_detached.py), retrying only the missing shots.
set -u
N=$1
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
M=${2:-/root/mokaair-work/videos/zhong-tian-qu-qi-e0$N-dh/colab/a/st1}
export COLAB_GPU=G4
S=zt${N}
cd $M
echo "start $(date -u +%FT%TZ)"
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
H3_PROFILE=hero bash $K/bootstrap.sh patch 2>&1 | grep -o "profile=[a-z]*"
ensure() { colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || bash $K/h3.sh start --session $S 2>&1 | tail -1; colab sessions 2>&1 | grep -q "$S.*Hardware: G4"; }
ensure || { echo "NOT G4"; exit 3; }
missing() { python3 -c "
import json,os,sys
print(','.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs'] if not os.path.exists(j['output_path'])))" "$1"; }
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
    # detached on the runtime (h3_detached.py): a dropped `colab exec` tunnel costs one poll, not the clip
    python3 -I $K/h3_detached.py ${p%.json}.todo.json --session $S --poll 30 --attempts 2 >> detached.log 2>&1
    echo "$p try $try exit=$? $(date -u +%T)"
  done
done
echo "have $(ls out/*.mp4 2>/dev/null | wc -l) drafts"
bash $K/h3.sh stop --session $S 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
