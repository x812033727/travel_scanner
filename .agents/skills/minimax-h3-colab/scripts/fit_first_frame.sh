#!/usr/bin/env bash
# Fit a keyframe to the H3 canvas without stretching it:
#
#   fit_first_frame.sh <in.png> <out.png> [WIDTH HEIGHT]     default 1312x736
#
# The upstream notebook stretches a first frame whose aspect ratio differs from the canvas by
# more than 0.01 (a 1920x1080 keyframe is 1.778, the default 1344x768 canvas is 1.75). This
# crops the centre to the canvas ratio and scales to the exact size. No 16:9 size under the
# 1344x768 area limit is a multiple of 32 (1280x720 is not: 720/32 = 22.5); 1312x736 (1.783) is
# within 0.005 of 16:9, 0.97 MP (the trained size) and above qc.mjs's 1280x720 floor, so a 16:9
# keyframe loses a 0.3% sliver; 1344x768 (1.75) trims 1.5% off the sides.
set -Eeuo pipefail

[[ $# -eq 2 || $# -eq 4 ]] || { sed -n '2,10p' "$0"; exit 2; }
in="$1"; out="$2"; w="${3:-1312}"; h="${4:-736}"
[[ -s "$in" ]] || { echo "[fit_first_frame] no such image: $in" >&2; exit 2; }
[[ "$w" =~ ^[0-9]+$ && "$h" =~ ^[0-9]+$ && $((w % 32)) -eq 0 && $((h % 32)) -eq 0 && $((w * h)) -le $((1344 * 768)) ]] \
  || { echo "[fit_first_frame] size must be multiples of 32 with area <= 1344x768, got ${w}x${h}" >&2; exit 2; }
command -v ffmpeg >/dev/null 2>&1 || { echo "[fit_first_frame] ffmpeg is not on PATH" >&2; exit 2; }

# crop to the target ratio (whichever side is too long), then scale; lanczos keeps the lines sharp.
ffmpeg -v error -y -i "$in" \
  -vf "crop='min(iw,ih*${w}/${h})':'min(ih,iw*${h}/${w})',scale=${w}:${h}:flags=lanczos,format=rgb24" \
  -frames:v 1 "$out"
echo "[fit_first_frame] $out ${w}x${h}"
