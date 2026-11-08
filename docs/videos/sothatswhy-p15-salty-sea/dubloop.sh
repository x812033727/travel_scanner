#!/bin/bash
# usage: dubloop.sh <slug> <locale...>: dub each locale (forget uncertain journal entries and retry on disconnects),
# check-audio, and redo flagged lines up to two rounds. Logs to $S/<short>-dub2-<locale>.log
S=/tmp/claude-0/-home-user-travel-scanner/6066c9db-4b01-5bf7-b159-6887844afe1e/scratchpad
cd /home/user/travel_scanner
export VIDEO_WORKDIR=/root/mokaair-work/videos NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 PLAYWRIGHT_BROWSERS_PATH=/root/pw-shim
slug=$1; shift; short=$(echo $slug | cut -d- -f2); W=$VIDEO_WORKDIR/$slug
dub() { # dub with retries; args passed through
  for i in 1 2 3 4 5 6; do
    out=$(node tools/video/cli.mjs dub --slug $slug "$@" 2>&1); rc=$?; echo "$out" | tail -3
    [ $rc -eq 0 ] && return 0
    shas=$(echo "$out" | grep -o 'forget --dir "[^"]*" --sha [0-9a-f]*' )
    if [ -n "$shas" ]; then echo "$shas" | while read -r line; do eval node tools/video/tts/speech-journal.mjs $line; done; sleep 10; continue; fi
    return $rc
  done; return 1
}
for l in "$@"; do
  log=$S/$short-dub2-$l.log
  { echo "== $l"; dub --locale $l; echo "dub rc $?"
    for round in 1 2 3; do
      node tools/video/cli.mjs check-audio --slug $slug --locale $l > $S/$short-dubcheck-$l.log 2>&1; rc=$?
      head -1 $S/$short-dubcheck-$l.log; [ $rc -eq 0 ] && break
      [ $round -eq 3 ] && break
      dub --locale $l --redo $W/review/check-flags.$l.json; echo "redo $round rc $?"
    done; } >> $log 2>&1
  tail -2 $log
done
