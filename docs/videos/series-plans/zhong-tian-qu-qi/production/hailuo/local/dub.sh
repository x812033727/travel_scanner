#!/usr/bin/env bash
# dub.sh NNN <en|ja|ko|es|pt|id|vi|th> : the dub of a finished episode, picture and timing untouched.
#   1. check docs/videos/zhong-tian-qu-qi-eNNN/dub.<locale>.json (every line, right script, length);
#   2. record the lines that are new or changed into <workdir>/audio-<locale>/ (dub-lines.mjs);
#   3. DUB=<locale> assemble-v4.mjs: cut/eNNN-dh.<locale>.m4a (zh lines' starts, same music and
#      effects, as long as the cut) and cut/eNNN-dh.<locale>.srt; it stops and lists the lines to
#      shorten when one does not fit its slot even at 1.3x (edit dub.<locale>.json, run again);
#   4. measure: lengths and loudness against the zh cut, into cut/dub-<locale>.log;
#   5. cut/eNNN-dh.<locale>-preview.mp4: the phone copy's picture, the dub and its CC, to listen to;
#   6. copy the track and CC into the admin import folder as dub.<locale>.m4a and <locale>.srt.
# CHECK=1 stops after step 1.
set -u
H=$(cd "$(dirname "$0")/.." && pwd)
R=$(cd "$H/../../../../../.." && pwd)
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
D="$R/docs/videos/zhong-tian-qu-qi-e$1"
W="$V/zhong-tian-qu-qi-e$1-dh"
L=$2
C="$W/cut"
LOG="$C/dub-$L.log"
[ -f "$C/e$1-dh.mp4" ] || { echo "no zh cut $C/e$1-dh.mp4"; exit 1; }
node "$H/local/dub-lines.mjs" "$R" "$D/video.json" "$L" "$W/audio-$L" --check || exit 2
[ "${CHECK:-0}" = 1 ] && exit 0
node "$H/local/dub-lines.mjs" "$R" "$D/video.json" "$L" "$W/audio-$L" 2>&1 | grep -v ': ok (' | tee "$LOG"
rec=${PIPESTATUS[0]}
if [ "$rec" -ne 0 ]; then echo "dub-lines.mjs failed ($rec): not assembling over old takes"; exit 4; fi
# assemble-v4 rewrites the episode's shared segments-v4/lines on every run, so two locales (or a
# compilation) of one episode must not assemble at once: wait for the episode's lock directory.
LOCK="$W/.dub-lock"
n=0
until mkdir "$LOCK" 2>/dev/null; do n=$((n+1)); [ $n -gt 360 ] && { echo "$LOCK held for 30 min (remove it if no dub is running)"; exit 5; }; sleep 5; done
trap 'rmdir "$LOCK"' EXIT
DUB=$L node "$H/assemble-v4.mjs" "$D/video.json" "$D/overlays.json" "$H/edit-dh-e$1.json" "$W" "$C/e$1-dh.mp4" >> "$LOG" 2>&1
rc=$?
if [ $rc -ne 0 ]; then tail -30 "$LOG"; exit 3; fi
iso() { case $1 in en) echo eng;; ja) echo jpn;; ko) echo kor;; es) echo spa;; pt) echo por;; id) echo ind;; vi) echo vie;; th) echo tha;; *) echo und;; esac; }
dur() { ffprobe -v error -select_streams "$2" -show_entries stream=duration -of csv=p=0 "$1"; }
lufs() { ffmpeg -nostats -i "$1" -map 0:a -af ebur128 -f null - 2>&1 | grep -A2 'Integrated loudness' | grep -o -- '-\?[0-9.]* LUFS' | head -1; }
{
  echo "zh video $(dur "$C/e$1-dh.mp4" v:0) s, zh audio $(dur "$C/e$1-dh.mp4" a:0) s, $L audio $(dur "$C/e$1-dh.$L.m4a" a:0) s"
  echo "loudness zh $(lufs "$C/e$1-dh.mp4"), $L $(lufs "$C/e$1-dh.$L.m4a")"
} | tee -a "$LOG"
ffmpeg -v error -y -i "$C/e$1-dh-phone.mp4" -i "$C/e$1-dh.$L.m4a" -i "$C/e$1-dh.$L.srt" -map 0:v -map 1:a -map 2:s -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:a:0 language="$(iso "$L")" -metadata:s:s:0 language="$(iso "$L")" \
  -t "$(dur "$C/e$1-dh.$L.m4a" a:0)" -movflags +faststart "$C/e$1-dh.$L-preview.mp4" && echo "preview $C/e$1-dh.$L-preview.mp4" | tee -a "$LOG"
I="$V/zhong-tian-qu-qi-import/zhong-tian-qu-qi-e$1"
if [ -d "$I" ]; then cp "$C/e$1-dh.$L.m4a" "$I/dub.$L.m4a" && cp "$C/e$1-dh.$L.srt" "$I/$L.srt" && echo "import folder: $I/dub.$L.m4a, $I/$L.srt" | tee -a "$LOG"; fi
grep -E "^$L: [0-9]+ lines" "$LOG"
