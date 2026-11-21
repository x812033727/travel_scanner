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
# After the e036 independent review (2026-11-20, 必改 7, 建議 6, 7, 9), new ids from a cleaned copy (the first ones stay, unsent):
#   shanjiao_qu_clean.py paints out the white modern guard rail on the terraced bank at the left and turns the flat upright
#   board under the plank into one thin post (a flat board grows writing);
#   -jing:   the cleaned picture itself (s13)
#   -zhuo2:  -zhuo's crop of the cleaned picture (s14, s16, s18, s19, s20, s26, s27, s28)
#   -tian2:  -tian's crop of the cleaned picture (s21, s24)
#   -xi2:    a new dusk grade of the cleaned picture: a warm orange glow added over the upper half of the sky (geq), warmer and less
#            green than -xi (which read as an olive / teal filter), a soft vignette (s29); -xi2-zhuo its crop of the flat left bank
#            and the pines (s30: the three far backs need ground to walk on, 建議 9)
# -an and -di are not touched by the cleaning (the rail and the board lie outside them) and stay as they are.
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
J="$O/set-shanjiao-qu-jing-l1.png"
python3 -I "$(dirname "$0")/shanjiao_qu_clean.py" "$S" "$J"
c "$J" set-shanjiao-qu-zhuo2-l1 640:360:0:200
c "$J" set-shanjiao-qu-tian2-l1 560:315:752:330
ffmpeg -v error -y -i "$J" -vf "format=rgb24,geq=r='min(255,r(X,Y)+80*max(0,1-Y/(H*0.48)))':g='min(255,g(X,Y)+22*max(0,1-Y/(H*0.48)))':b='max(0,b(X,Y)-30*max(0,1-Y/(H*0.48)))',eq=brightness=-0.07:saturation=1.1:contrast=1.05:gamma=0.9,colorbalance=rs=0.14:gs=0.00:bs=-0.18:rm=0.16:gm=0.00:bm=-0.24:rh=0.22:gh=0.00:bh=-0.36,vignette=PI/6" -frames:v 1 -flags +bitexact -fflags +bitexact "$O/set-shanjiao-qu-xi2-l1.png"
c "$O/set-shanjiao-qu-xi2-l1.png" set-shanjiao-qu-xi2-zhuo-l1 640:360:0:200
# After the e936 cut review 2 (2026-11-21, 中等 1: the model grew the small square bump on the far skyline into modern tower
# blocks in s21 and s29), new ids again from a second cleaned copy (the -jing / -tian2 / -xi2 ones stay, already sent):
#   shanjiao_qu_clean2.py paints the bump, a thin spike and the faint blocky shapes in the haze out of -jing into tree line,
#   sky and haze; -jing2 the result, -tian3 / -xi3 the same crop and dusk grade as -tian2 / -xi2 (-xi2-zhuo is untouched by
#   the cleaning, its crop lies left of it: bit-identical, so it stays as it is).
#   Send these for any later retake or e037 shot of the channel instead of -jing / -tian2 / -xi2.
J2="$O/set-shanjiao-qu-jing2-l1.png"
python3 -I "$(dirname "$0")/shanjiao_qu_clean2.py" "$J" "$J2"
c "$J2" set-shanjiao-qu-tian3-l1 560:315:752:330
ffmpeg -v error -y -i "$J2" -vf "format=rgb24,geq=r='min(255,r(X,Y)+80*max(0,1-Y/(H*0.48)))':g='min(255,g(X,Y)+22*max(0,1-Y/(H*0.48)))':b='max(0,b(X,Y)-30*max(0,1-Y/(H*0.48)))',eq=brightness=-0.07:saturation=1.1:contrast=1.05:gamma=0.9,colorbalance=rs=0.14:gs=0.00:bs=-0.18:rm=0.16:gm=0.00:bm=-0.24:rh=0.22:gh=0.00:bh=-0.36,vignette=PI/6" -frames:v 1 -flags +bitexact -fflags +bitexact "$O/set-shanjiao-qu-xi3-l1.png"
