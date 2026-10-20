#!/usr/bin/env bash
L="$(cd "$(dirname "$0")" && pwd)"
for pair in s1:skill p1:paste b1:bare v1:vague s2:skill p2:paste b2:bare v2:vague s3:skill p3:paste b3:bare v3:vague x1:slash; do
  n="${pair%%:*}"; a="${pair##*:}"
  "$L/run.sh" "$n" "$a" 2>&1 | tail -1
done
echo BATCH_DONE
