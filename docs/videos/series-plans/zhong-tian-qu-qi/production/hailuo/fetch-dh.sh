#!/usr/bin/env bash
# The 3D donghua version's downloads, from "label status path" lines on stdin:
# dh-<name>-tK -> _series/zhong-tian-qu-qi/refs-dh/<name>-tK.png, aN-sNN-tK -> zhong-tian-qu-qi-e00N-dh/first-frames/sNN-tK.png,
# c:aN-sNN -> zhong-tian-qu-qi-e00N-dh/clips/sNN-t1.mp4. Appends to the series receipts.
V=~/mokaair-work/videos
while read -r label status path; do
  [ "$status" = "2" ] && [ -n "$path" ] || continue
  url="https://cdn.hailuoai.video/moss/prod/$path"
  if [[ $label =~ ^dh-(.+)$ ]]; then d=$V/_series/zhong-tian-qu-qi/refs-dh; f=$d/${BASH_REMATCH[1]}.png
  elif [[ $label =~ ^c:a([0-9])-(s[0-9a-z]+)$ ]]; then d=$V/zhong-tian-qu-qi-e00${BASH_REMATCH[1]}-dh/clips; f=$d/${BASH_REMATCH[2]}-t1.mp4
  elif [[ $label =~ ^a([0-9])-(s[0-9a-z]+)-(t[0-9])$ ]]; then d=$V/zhong-tian-qu-qi-e00${BASH_REMATCH[1]}-dh/first-frames; f=$d/${BASH_REMATCH[2]}-${BASH_REMATCH[3]}.png
  else continue; fi
  mkdir -p "$d"; [ -s "$f" ] && continue
  curl -s -f -o "$f" "$url" || { echo "FAIL $label"; rm -f "$f"; continue; }
  echo "{\"label\":\"$label\",\"file\":\"$f\",\"url\":\"$url\",\"at\":\"$(date -u +%FT%TZ)\"}" >> "$V/zhong-tian-qu-qi-receipts.jsonl"
  echo "got $label"
done
