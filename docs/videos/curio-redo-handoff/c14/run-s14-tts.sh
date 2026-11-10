#!/bin/bash
S=/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad/c14; slug=curio-s14-v2; W=/root/mokaair-work/videos/$slug
cd /home/user/wt-prod; export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1
st() { echo "$(date -u +%H:%M:%S) $*" >> $S/run-s14.status; }
for i in 1 2 3 4 5; do
  node tools/video/cli.mjs tts --slug $slug > $S/tts-s14.$i.log 2>&1; rc=$?; st "tts try$i EXIT $rc"; [ $rc -eq 0 ] && break
  for sha in $(grep -oE '(request sha256|--sha) [0-9a-f]{64}' $S/tts-s14.$i.log | awk '{print $NF}' | sort -u); do
    node tools/video/tts/speech-journal.mjs forget --dir $W/audio/speech-journal --sha $sha >/dev/null; st "forgot $sha"; done
done
[ $rc -eq 0 ] || { st "TTS FAILED"; exit 1; }
for r in 0 1 2; do
  for k in 1 2 3 4; do
    node tools/video/cli.mjs check-audio --slug $slug > $S/check-s14.$r.log 2>&1; rc=$?
    [ $rc -ne 3 ] && break
    shas=$(grep -oE '\-\-sha [0-9a-f]{64}' $S/check-s14.$r.log | awk '{print $2}' | sort -u); [ -n "$shas" ] || break
    for sha in $shas; do node tools/video/tts/speech-journal.mjs forget --dir $W/audio/speech-journal --sha $sha >/dev/null; st "forgot $sha"; done
  done
  st "check$r EXIT $rc $(grep -oE '[0-9]+ flagged' $S/check-s14.$r.log)"
  [ $rc -eq 0 ] && break; [ $r -eq 2 ] && break; [ $rc -eq 3 ] && break
  node tools/video/cli.mjs tts --slug $slug --redo $W/review/check-flags.json > $S/tts-s14-redo$r.log 2>&1; st "redo$r EXIT $?"
done
st DONE
