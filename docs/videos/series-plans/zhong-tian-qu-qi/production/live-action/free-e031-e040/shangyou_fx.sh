#!/bin/bash
# arc 4 (2026-11-17, e031 review 必改 1, plan A; coordinator's decision): set-shangyou-ba-l1 (round 3, seed 37042 with
# clean_shangyou_box.py) mirrored left to right as a new id, so the Liuxi side is on the LEFT and the dam on the RIGHT as the
# bible's 31->32 hand-over and every e031 close shot have it (rule 9 forbids flipping cross-collared PEOPLE; a set with no
# writing and no person may be flipped). Then five close crops of the flipped picture (boxes from writer-tools/e031-r2/review.md,
# lanczos to 1312x736, each a new id with its own l1).
# Usage: bash shangyou_fx.sh refs-live/set-shangyou-ba-l1.png OUTDIR
set -e
Q=$1; O=$2
F="$O/set-shangyou-ba-fx-l1.png"
ffmpeg -v error -y -i "$Q" -vf hflip -flags +bitexact -fflags +bitexact "$F"
c() { ffmpeg -v error -y -i "$F" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-shangyou-ba-fx-ding-l1 512:288:500:60    # hazy sky, bamboo valley, a little green field: s34, s36 (low angle, Qian Yuanwai)
c set-shangyou-ba-fx-tang-l1 640:360:672:200   # bamboo slope, the far line of stones, the muddy pond, sack tops at lower left: s37
c set-shangyou-ba-fx-jiao-l1 480:270:150:420   # the muddy ditch, the stone-edged path, the sack slope at right: s35
c set-shangyou-ba-fx-lu-l1   640:360:150:376   # the same, wider, the sacks running back at the right: s38, s40
c set-shangyou-ba-fx-shan-l1 448:252:0:100     # soft green bamboo slope only: s33, s39
