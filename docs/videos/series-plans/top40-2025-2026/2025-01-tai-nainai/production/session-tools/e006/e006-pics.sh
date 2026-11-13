#!/usr/bin/env bash
# 第 6 集：等別人的 Colab 停了才開機；先畫場景與道具圖，等挑圖旗標，再畫首格；最後一定關機
S=${TN_WORK:-$HOME/mokaair-work/videos/_tn-work}
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts; export COLAB_GPU=G4
trap 'bash $K/h3.sh stop --session tn-e6 >/dev/null 2>&1; echo "== stopped $(date -u +%T)"' EXIT
while colab sessions 2>/dev/null | grep -q "^\[?\]"; do sleep 120; done
echo "== others idle $(date -u +%T)"
for i in $(seq 1 12); do bash $K/h3.sh start --session tn-e6 --gpu G4 2>&1 | grep -q ready && break; sleep 240; done
bash $K/h3.sh usage 2>&1 | tail -1 > $S/e006-cu-start.txt
run_images(){ # $1 manifest $2 outdir $3 expected count
  for t in 1 2 3; do
    rm -f $2.p.json
    timeout 2400 bash $K/h3.sh images --manifest $1 --output-dir $2 --progress $2.p.json --session tn-e6 >/dev/null 2>&1 &
    pid=$!; while kill -0 $pid 2>/dev/null; do sleep 20; grep -q "Connection was lost" $2.p.json 2>/dev/null && { pkill -f "h3.sh images"; break; }; done; wait $pid 2>/dev/null
    [ $(ls $2/*.png 2>/dev/null | wc -l) -ge $3 ] && return 0
    timeout 120 colab restart-kernel --session tn-e6 >/dev/null 2>&1; sleep 10
  done
}
cd $S/e006sets && run_images sets.json out 6; echo "== sets done $(date -u +%T)"
for i in $(seq 1 60); do [ -f $S/e006sets/picked ] && break; sleep 20; done
cd $S/e006ff && mkdir -p st && run_images stills-m.json st 56; echo "== stills done $(date -u +%T)"
