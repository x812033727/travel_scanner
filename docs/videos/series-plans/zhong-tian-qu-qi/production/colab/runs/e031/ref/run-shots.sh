#!/bin/bash
# One shot at a time, with retries: a lost websocket does not sink the batch. For each id in
# jobs/order.txt: skip when the output already decodes; else run h3.sh batch on jobs/<id>.json;
# on failure poll `colab download` for the remote output for up to 15 minutes (the kernel often
# finishes after the client loses the connection), then restart the kernel and generate again
# (3 attempts). A lost session is recreated. Everything goes to run-shots.log.
S=${1:?session}
R=/root/mokaair-work/videos/zhong-tian-qu-qi-e031-dh/colab/ref
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
CLIPS=/root/mokaair-work/videos/zhong-tian-qu-qi-e031-dh/clips
L=$R/run-shots.log
cd $R || exit 2
log() { echo "$(date -u +%H:%M:%S) $*" >> $L; }
ok() { ffprobe -v error -select_streams v -show_entries stream=nb_frames -of csv=p=0 "$1" 2>/dev/null | grep -qE '^[0-9]+$'; }
have_session() { timeout 60 colab status --session $S 2>&1 | grep -q "Status:"; }
ensure_session() { have_session || { log "session $S missing, starting"; bash $K/h3.sh start --session $S >> $L 2>&1; }; }
outpath() { python3 -c "import json;print(json.load(open('$R/jobs/$1.json'))['jobs'][0]['output_path'])"; }
log "run start session=$S"
for id in $(cat $R/jobs/order.txt); do
  out=$(outpath $id)
  if ok "$out"; then log "$id already done"; continue; fi
  for attempt in 1 2 3; do
    ensure_session
    log "$id attempt $attempt generate"
    bash $K/h3.sh batch --no-check --manifest $R/jobs/$id.json --output-dir $CLIPS --progress $R/jobs/$id.progress.json --session $S --timeout 1500 >> $L 2>&1
    if ok "$out"; then log "$id done ($attempt)"; break; fi
    if ! have_session; then log "$id attempt $attempt failed: session gone (runtime reclaimed), retrying on a new one"; continue; fi
    log "$id attempt $attempt failed; polling remote output"
    for i in $(seq 1 15); do
      sleep 60
      timeout 300 colab download --session $S /content/h3_${id}_output.mp4 "$out" >> $L 2>&1 && ok "$out" && break
      rm -f "$out"
    done
    if ok "$out"; then log "$id recovered from remote ($attempt)"; break; fi
    log "$id not recoverable; restarting kernel"
    timeout 120 colab restart-kernel --session $S >> $L 2>&1
  done
  ok "$out" || log "$id GAVE UP"
done
log "run end"
echo "episode done" >> $L
