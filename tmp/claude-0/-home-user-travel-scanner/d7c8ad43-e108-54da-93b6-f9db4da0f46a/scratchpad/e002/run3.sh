#!/usr/bin/env bash
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad; W=$S/e002
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
export COLAB_GPU=G4; SS=${SESSION:-tn-e002b}
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
[ -n "${REUSE:-}" ] || bash $K/h3.sh start --session $SS --gpu G4 || exit 1
draft() { local d=$1 m=$2 id=$3; [ -s $d/out/$id.mp4 ] && return 0
  python3 -c "import json,sys;d=json.load(open(sys.argv[1]));json.dump({'jobs':[j for j in d['jobs'] if j['id']==sys.argv[2]]},open(sys.argv[3],'w'))" $d/$m $id $d/one-$id.json
  for try in 1 2; do (cd $d && timeout 600 bash $K/h3.sh batch --manifest one-$id.json --output-dir out --progress one-$id.p.json --session $SS >/dev/null 2>&1)
    [ -s $d/out/$id.mp4 ] && { echo "== draft $id ok (try $try) $(date -u +%T)"; return 0; }
    echo "== draft $id failed (try $try)"; timeout 120 colab restart-kernel --session $SS >/dev/null 2>&1; sleep 10; done; }
refine_ids() { local m=$1; shift; for id in "$@"; do [ "${SKIPDONE:-}" ] && [ $W/st2/refined/$id.mp4 -nt $m ] && continue;
  for try in 1 2; do (cd $W && timeout 540 bash $K/h3.sh refine --manifest $m --output-dir st2/refined --session $SS --only $id >/dev/null 2>&1)
    [ $W/st2/refined/$id.mp4 -nt $m ] && { echo "== refined $id ok (try $try) $(date -u +%T)"; break; }
    echo "== refine $id failed (try $try)"; timeout 120 colab restart-kernel --session $SS >/dev/null 2>&1; sleep 10; done; done; }
for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$W/r2/retake.json'))['jobs']))"); do draft $W/r2 retake.json $id; done
(cd $W && bash $K/h3.sh cuts --input-dir r2/out --output-dir r2/trimmed | grep -v "no cut")
echo "== drafts done $(date -u +%T)"
KEEP="c04 c08 c09 c10 c13 c14 c20 c21"
python3 -c "import json,sys;ids=sys.argv[3].split();json.dump({'jobs':[j for j in json.load(open(sys.argv[1]))['jobs'] if j['id'] in ids]},open(sys.argv[2],'w'),indent=1)" $W/r2/st1-all.json $W/r2/st1-keep.json "$KEEP"
[ -d $W/st2keep ] || python3 -I $P/st2.py --st1 $W/r2/st1-keep.json --drafts $W/trimmed --work $W/st2keep
python3 $K/refine.py --manifest $W/st2keep/st2-part1.json --check && refine_ids $W/st2keep/st2-part1.json $KEEP
echo "== keep refined $(date -u +%T); waiting for picks.txt"
for i in $(seq 1 90); do [ -f $W/picks.txt ] && break; sleep 20; done
if [ -f $W/picks.txt ]; then
  ids=$(cut -d= -f1 $W/picks.txt | tr '\n' ' '); takes=$(sed 's/^/--take /' $W/picks.txt | tr '\n' ' ')
  python3 -c "import json,sys;ids=sys.argv[3].split();json.dump({'jobs':[j for j in json.load(open(sys.argv[1]))['jobs'] if j['id'] in ids]},open(sys.argv[2],'w'),indent=1)" $W/r2/st1-all.json $W/r2/st1-picks.json "$ids"
  [ -d $W/st2picks ] || python3 -I $P/st2.py --st1 $W/r2/st1-picks.json --drafts $W/r2/trimmed $takes --work $W/st2picks
  for f in $W/st2picks/st2-part*.json; do python3 $K/refine.py --manifest $f --check && refine_ids $f $(python3 -c "import json,sys;print(' '.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs']))" $f); done
else echo "== no picks after 30 min"; fi

echo "== round 3 drafts $(date -u +%T)"
for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$W/r3/retake.json'))['jobs']))"); do draft $W/r3 retake.json $id; done
(cd $W && bash $K/h3.sh cuts --input-dir r3/out --output-dir r3/trimmed | grep -v "no cut")
echo "== round 3 drafts done $(date -u +%T); waiting for picks3.txt"
for i in $(seq 1 90); do [ -f $W/picks3.txt ] && break; sleep 20; done
if [ -f $W/picks3.txt ]; then
  ids=$(cut -d= -f1 $W/picks3.txt | tr '\n' ' '); takes=$(sed 's/^/--take /' $W/picks3.txt | tr '\n' ' ')
  python3 -c "import json,sys;ids=sys.argv[3].split();json.dump({'jobs':[j for j in json.load(open(sys.argv[1]))['jobs'] if j['id'] in ids]},open(sys.argv[2],'w'),indent=1)" $W/r3/st1-all.json $W/r3/st1-picks.json "$ids"
  rm -rf $W/st2r3; python3 -I $P/st2.py --st1 $W/r3/st1-picks.json --drafts $W/r3/trimmed $takes --work $W/st2r3
  for f in $W/st2r3/st2-part*.json; do python3 $K/refine.py --manifest $f --check && refine_ids $f $(python3 -c "import json,sys;print(' '.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs']))" $f); done
else echo "== no picks3 after 30 min"; fi
bash $K/h3.sh stop --session $SS; bash $K/bootstrap.sh patch >/dev/null
echo "== done $(date -u +%T) refined $(ls $W/st2/refined/*.mp4 2>/dev/null | wc -l)"; bash $K/h3.sh usage | tail -1
bash $S/tn-backup-e002.sh | tail -1
