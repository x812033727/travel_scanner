#!/usr/bin/env bash
# retry the retake batch until a pod starts (no stock -> 409), at most 20 tries, 3 min apart
cd /home/user/travel_scanner
R=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e043-dh/runpod/a/retake1
for i in $(seq 1 20); do
  echo "=== try $i $(date -u +%T)"
  bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh batch --manifest $R/retake.json --output-dir $R/out --progress $R/out/progress.json \
    --profile hero --label e043-retake1 --slug zhong-tian-qu-qi-e043
  rc=$?
  grep -q "started pod\|reusing pod" $R/run.log && { echo "=== batch exit $rc"; exit $rc; }
  sleep 180
done
echo "=== gave up: no stock"
