#!/bin/bash
# grab.sh SHOT SEEDSUFFIX t1 t2 t3 ... -> tile 2 columns at 640 width
S=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/e906/x
C=/root/mokaair-work/videos/zhong-tian-qu-qi-e906-dh/runpod/a/v1/out
sh=$1; sd=$2; shift 2
files=()
for t in "$@"; do f=$S/$sh-$sd-$t.jpg; ffmpeg -v error -y -ss $t -i $C/$sh-906010$sd.mp4 -frames:v 1 -vf scale=640:-1 $f; files+=($f); done
python3 - "$S/$sh-$sd-grid.jpg" "${files[@]}" <<'PY'
import sys
from PIL import Image, ImageDraw
out=sys.argv[1]; fs=sys.argv[2:]
ims=[Image.open(f) for f in fs]; w,h=ims[0].size; cols=2; rows=(len(ims)+1)//2
g=Image.new('RGB',(w*cols,h*rows))
for i,im in enumerate(ims):
  d=ImageDraw.Draw(im); d.text((5,5),fs[i].split('/')[-1],fill='yellow'); g.paste(im,((i%cols)*w,(i//cols)*h))
g.save(out)
PY
echo $S/$sh-$sd-grid.jpg
