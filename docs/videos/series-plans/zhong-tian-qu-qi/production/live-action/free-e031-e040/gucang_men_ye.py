"""gucang_men_ye.py SRC DST : set-gucang-men-ye-l1 (arc 4, 2026-11-17) from the round-3 pick set-gucang-wai-l1 (seed 37042).
1) Crop the granary and the dry ground in front of its door: crop 560x315 at (752, 190), lanczos up to 1312x736
   (2.34x, soft). 2) Relight to a clear moonlit night: every pixel becomes its luminance L' = L^1.15 scaled to 0.30,
   tinted (0.62, 0.78, 1.25) (cold blue-grey), plus 18 % of its own colour so the wood and earth keep a trace of their
   hue; the sky (the top band above the roof line, blue > red + 40) is pulled further down to a deep blue (0.5x, through
   an 8 px soft mask so the hill line has no hard step); inside the open doorway (x 625-885, y 390-690 of the output)
   every pixel is capped at the doorway's 30th-percentile colour, so the small lit window at the back reads as dark. A torch on the door post is written
   in each shot (bible rule 33), not painted here."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB").crop((752, 190, 752 + 560, 190 + 315)).resize((1312, 736), Image.LANCZOS)
a = np.asarray(im).astype(np.float64)
L = a @ np.array([0.299, 0.587, 0.114])
Ln = 255 * (L / 255) ** 1.15 * 0.30
night = Ln[..., None] * np.array([0.62, 0.78, 1.25]) + 0.18 * a * 0.30
sky = ndi.gaussian_filter((a[..., 2] > a[..., 0] + 40).astype(np.float64), 8)[..., None]
night *= 1 - 0.5 * sky
door = (slice(390, 690), slice(625, 885))     # the open doorway; its small lit back window would read as a lamp
night[door] = np.minimum(night[door], np.percentile(night[door], 30, axis=(0, 1)))
Image.fromarray(np.clip(night + 0.5, 0, 255).astype(np.uint8)).save(dst)
