#!/usr/bin/env bash
# Reads "label status path" lines (from __zt.done() / __ztc.done()) on stdin and downloads every
# finished one that is not on disk yet: e1-s07-t1 -> zhong-tian-qu-qi-e001/first-frames/s07-t1.png,
# c:e1-s07 -> zhong-tian-qu-qi-e001/clips/s07-t1.mp4. Appends to receipts.jsonl.
V=~/mokaair-work/videos
while read -r label status path; do
  [ "$status" = "2" ] && [ -n "$path" ] || continue
  url="https://cdn.hailuoai.video/moss/prod/$path"
  if [[ $label =~ ^c:e([0-9])-(s[0-9a-z]+)$ ]]; then
    d=$V/zhong-tian-qu-qi-e00${BASH_REMATCH[1]}/clips; f=$d/${BASH_REMATCH[2]}-t1.mp4
  elif [[ $label =~ ^e([0-9])-(s[0-9a-z]+)-(t[0-9])$ ]]; then
    d=$V/zhong-tian-qu-qi-e00${BASH_REMATCH[1]}/first-frames; f=$d/${BASH_REMATCH[2]}-${BASH_REMATCH[3]}.png
  else continue; fi
  mkdir -p "$d"; [ -s "$f" ] && continue
  curl -s -f -o "$f" "$url" || { echo "FAIL $label"; rm -f "$f"; continue; }
  echo "{\"label\":\"$label\",\"file\":\"$f\",\"url\":\"$url\",\"at\":\"$(date -u +%FT%TZ)\"}" >> "$V/zhong-tian-qu-qi-receipts.jsonl"
  echo "got $label"
done
