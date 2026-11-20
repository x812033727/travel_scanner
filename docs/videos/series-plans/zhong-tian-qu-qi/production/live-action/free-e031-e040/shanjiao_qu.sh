#!/bin/bash
# arc 4 (2026-11-20, e036 r2 d1 prep): free crops and one grade of set-shanjiao-qu-l1 (screen test round 4, 37044: a freshly dug
# dry channel running straight from the foreground away into the distance, its bed cracked dry earth; on the LEFT bank a long
# mound of dug brown earth and a heap of dry straw, beyond it a flat dry yellow field and a dark line of pines and trees at the
# far left; across the channel in the middle distance one wooden board standing upright with a plank laid over it; on the RIGHT
# bank a strip of dry grass and a green paddy of young rice; blue sky, clear morning light). Each a new id, lanczos to 1312x736
# (rules 19, 35). e036 scene 2 (the new channel at the foot of the hills, opening day to half a month later):
#   (the day picture itself is sent to the wides of the opening days, noon and the afternoon: s13; its light is the script's
#    「上午白光」, and noon / the afternoon are written in the light sentence only)
#   -zhuo: the flat dry yellow ground on the left bank beyond the earth mound, the line of dark pines behind (the account table:
#          s14, s16, s18, s20, s26, s27)
#   -an:   the mound of dug earth and the heap of dry straw on the left bank (close-up backgrounds: s19, s24, s25; the insert s23)
#   -di:   the cracked dry bed of the channel only (the inserts s15, s17, s22)
#   -tian: the right bank, its dry grass and the green paddy beyond (s21: Qin Shuang comes along the paddy's edge)
#   -xi:   the same picture at dusk, the low sun from the right (warmer, the sky pulled to amber, darker, long shadows read from the
#          picture's own): the whole picture (s29) and -xi-an (the earth mound and the straw at dusk: s30)
# Usage: bash shanjiao_qu.sh refs-live/set-shanjiao-qu-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
c "$S" set-shanjiao-qu-zhuo-l1 640:360:0:200
c "$S" set-shanjiao-qu-an-l1   560:315:40:400
c "$S" set-shanjiao-qu-di-l1   400:225:520:500
c "$S" set-shanjiao-qu-tian-l1 560:315:752:330
ffmpeg -v error -y -i "$S" -vf "eq=brightness=-0.12:saturation=1.05:contrast=1.04:gamma=0.86,colorbalance=rs=0.22:gs=0.04:bs=-0.30:rm=0.20:gm=0.02:bm=-0.26:rh=0.24:gh=0.05:bh=-0.34,vignette=PI/6" -flags +bitexact -fflags +bitexact "$O/set-shanjiao-qu-xi-l1.png"
c "$O/set-shanjiao-qu-xi-l1.png" set-shanjiao-qu-xi-an-l1 560:315:40:400
