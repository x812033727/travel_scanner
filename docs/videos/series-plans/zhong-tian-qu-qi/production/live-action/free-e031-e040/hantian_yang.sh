#!/bin/bash
# arc 4 (2026-11-20, e035 r2 d1 prep): free grades and crops of set-hantian-yang-l1 (screen test round 2, 37039: set-hantian-l1
# with the paddy in front of the low ridge flooded and planted with sparse green seedlings; the dry cracked field behind the
# ridge, a row of small houses and far hills at the left and middle, a big old tree with yellow leaves and a raised grassy bank
# at the right), each a new id, lanczos to 1312x736 (rules 19, 35). e035 scene 2 (the ducks, two days after the swarm night, to
# the next dawn); the picture's own light is a clear low sun, the script's is three others, so three grades:
#   -zong: the afternoon under the swarm, a dull brown half-light (darker, drained, warm-brown balance; the blue sky turns a dull
#          olive brown): the whole picture (s12, the wide with the cages) and the crops -zong-geng (the left: the paddy, the
#          ridge, the dry field, the houses and hills; s15, s18), -zong-liu (the right: the big tree, the grassy bank and the
#          paddy; s12b, s16), -zong-an (the grassy bank by the water, the tree's trunk; s13, s17), -zong-tian (the sky and the far
#          hills over a strip of field; s14), -zong-shui (the water and the seedlings only; s17b, the close-up of the ducks);
#   -xi:   the same evening, A-ling alone with the ducks, a low orange light (warmer, the sky pulled toward amber): the whole
#          picture (s19);
#   -chen: the next dawn, a soft grey-gold light with a thin white mist (lower contrast and saturation, cool shadows, warm
#          highlights, a blurred bright layer screened over at 45%): the whole picture (s20) and -chen-liu (s20b, s22, s23, s24),
#          -chen-an (s25), -chen-shui (the water and the seedlings only, for the insert s21), -chen-geng (not sent in d1; kept
#          for a fix).
# First: hantian_yang_clean.py paints out the three tiny dark verticals on the far field line (as hantian_clean.py on
# set-hantian-l1; set-hantian-yang-l1 carries the same three a few pixels to the right).
# Usage: bash hantian_yang.sh refs-live/set-hantian-yang-l1.png OUTDIR
set -e
S=$1; O=$2; A="$O/.hantian-yang-clean.png"
python3 -I "$(dirname "$0")/hantian_yang_clean.py" "$S" "$A"
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
g() { ffmpeg -v error -y -i "$A" -filter_complex "$2" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
g set-hantian-yang-zong-l1 "eq=brightness=-0.18:saturation=0.45:contrast=0.84:gamma=0.86,colorbalance=rs=0.12:gs=0.05:bs=-0.16:rm=0.12:gm=0.04:bm=-0.15:rh=0.14:gh=0.06:bh=-0.20"
g set-hantian-yang-xi-l1 "eq=brightness=-0.10:saturation=1.00:contrast=1.02:gamma=0.88,colorbalance=rs=0.20:gs=0.03:bs=-0.26:rm=0.20:gm=0.02:bm=-0.24:rh=0.22:gh=0.04:bh=-0.30"
g set-hantian-yang-chen-l1 "eq=brightness=0.00:saturation=0.55:contrast=0.80:gamma=1.04,colorbalance=rs=-0.03:bs=0.04:rm=0.02:bm=0.00:rh=0.08:gh=0.05:bh=-0.04,split[a][b];[b]gblur=sigma=30,eq=brightness=0.20:saturation=0.25[c];[a][c]blend=all_mode=screen:all_opacity=0.45"
Z="$O/set-hantian-yang-zong-l1.png"; C="$O/set-hantian-yang-chen-l1.png"
c "$Z" set-hantian-yang-zong-geng-l1 640:360:0:220
c "$Z" set-hantian-yang-zong-liu-l1  640:360:672:170
c "$Z" set-hantian-yang-zong-an-l1   512:288:800:330
c "$Z" set-hantian-yang-zong-tian-l1 640:360:330:60
c "$Z" set-hantian-yang-zong-shui-l1 480:270:300:466
c "$C" set-hantian-yang-chen-geng-l1 640:360:0:220
c "$C" set-hantian-yang-chen-liu-l1  640:360:672:170
c "$C" set-hantian-yang-chen-an-l1   512:288:800:330
c "$C" set-hantian-yang-chen-shui-l1 480:270:300:466
rm -f "$A"
