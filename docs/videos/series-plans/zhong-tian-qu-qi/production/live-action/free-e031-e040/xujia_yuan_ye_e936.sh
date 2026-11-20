#!/bin/bash
# arc 4 (2026-11-20, e036 r2 d1 prep): free crops of set-xujia-yuan-ye-dong2-l1 (the night yard: e931's ye_dong2.py output, the
# blank board and the bodiless lantern glow painted out): the farmhouse at the LEFT with its dark doorway at the far left and a
# small lattice window, split firewood stacked against the house front under the window, the yard gate of planks under a small
# tiled roof in the MIDDLE of the back wall, the bare tree just right of the gate, the low earth-and-stone back wall running from
# the gate to the right edge, the round stone well with its windlass in the front RIGHT, a wooden bucket in the middle, dark
# fields and far hills beyond the wall under a deep blue night sky. Each a new id, lanczos to 1312x736 (rules 19, 35). e036
# scene 3 (half a month after the opening, the third watch) sends set-xujia-yuan-ye-dong2-l1 itself to the wide s31 and:
#   -chai:  the woodpile against the house front and the lattice window above it (s34: Xu Yan comes from the house door)
#   -qiang: the right stretch of the back wall, the dark fields beyond it, the well's windlass at the lower right (bible rule 42: the row of
#           straw mats lies along its foot; s32 the mats, s33 / s35 Qin Shuang on its top)
#   -shan:  the dark fields and the far hills beyond the right stretch of the wall, its warm-lit top along the bottom edge (s36:
#           the line of small flames down the hillside)
#   -wu:    the dark doorway at the far left of the house and the stacked firewood beside it (s37: A-ling at the door)
#   -zhong: the middle of the yard, the bucket, the tree and the gate behind (s38)
# After the e036 independent review (2026-11-20, 建議 8): -shan2, a true 16:9 crop of the wall top, the dark fields and the far
# hills right of the tree and the gate roof (-shan was 640x270 stretched 1.33x tall and had the tree trunk and the roof in it) (s36)
# Usage: bash xujia_yuan_ye_e936.sh refs-live/set-xujia-yuan-ye-dong2-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$S" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-xujia-yuan-ye-dong2-chai-l1  560:315:140:300
c set-xujia-yuan-ye-dong2-qiang-l1 560:315:752:250
c set-xujia-yuan-ye-dong2-shan-l1  640:270:672:140
c set-xujia-yuan-ye-dong2-wu-l1    480:270:0:290
c set-xujia-yuan-ye-dong2-zhong-l1 640:360:330:250
c set-xujia-yuan-ye-dong2-shan2-l1 520:292:792:120
