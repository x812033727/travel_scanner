"""e036 independent review 必改 7 and 建議 6 (2026-11-20): two things out of set-shanjiao-qu-l1 before it is cropped and graded
(shanjiao_qu.sh), free, deterministic:
1. the white modern guard rail (a row of low white posts and a rail) along the terraced bank in the middle distance at the left
   (x 0-500, a 13 px band from y 325 + 0.024 x, sloping down to the right): each column of the band is replaced by the earth slope
   13 px below it, so the bank reads as one terraced slope of earth;
2. the flat upright board standing in the middle of the channel under the plank (x 725-807, y 379-505; a flat board grows writing,
   e935 fix1 s30): below and across the plank the rectangle is copied from the same rows 85 px to the right (the cracked bed, the
   plank running on), above it each row is blended across with fine texture; one narrow strip below the plank stays as a thin
   wooden post holding the plank; 2 px feathered edges.
Usage: python3 -I shanjiao_qu_clean.py set-shanjiao-qu-l1.png OUT.png
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
h, w, _ = a.shape
out = a.copy()
# 1. the rail: each column's band is replaced by the earth slope just below it (the same column 13 px lower)
for x in range(0, 500):
    top = int(round(325 + x * 0.024))
    out[top:top + 13, x] = a[top + 13:top + 26, x]
# 2. the board -> a thin post. Below the plank (y 452-506) the rectangle is copied from 85 px to the right (the cracked bed);
# the plank band (y 432-452) likewise (the plank runs on across); above the plank (y 379-432), where the far channel and the
# mound's edge meet in perspective and no shifted copy lines up, each row is blended across from its left neighbour to its
# right neighbour with the shifted copy's fine texture on top; one narrow strip (x 761-771) below the plank stays the board's own wood as a thin post.
x0, x1, y0, y1, dx = 725, 808, 379, 506, 85
post0, post1, plank = 761, 771, 432
low = out.copy()
low[plank:y1, x0:x1] = a[plank:y1, x0 + dx:x1 + dx]
low[plank + 20:y1, post0:post1] = a[plank + 20:y1, post0:post1]
out[plank:y1, x0:x1] = low[plank:y1, x0:x1]
# above the plank: each row interpolated across from the pixel left of the rectangle to the pixel right of it, plus the fine
# texture (minus its 7 px box blur) of the same rows 85 px to the right, so it reads as dry earth, not a smudge
src_rows = a[y0:plank, x0 + dx:x1 + dx]
k = 7
pad = np.pad(src_rows, ((k, k), (k, k), (0, 0)), mode="edge")
cs = pad.cumsum(0).cumsum(1)
box = (cs[2 * k:, 2 * k:] - cs[:-2 * k, 2 * k:] - cs[2 * k:, :-2 * k] + cs[:-2 * k, :-2 * k]) / (2 * k) ** 2
detail = src_rows - box[:src_rows.shape[0], :src_rows.shape[1]]
L = out[y0:plank, x0 - 2:x0].mean(axis=1)
R = out[y0:plank, x1:x1 + 2].mean(axis=1)
t = (np.arange(x1 - x0) + 0.5) / (x1 - x0)
out[y0:plank, x0:x1] = L[:, None, :] * (1 - t[None, :, None]) + R[:, None, :] * t[None, :, None] + detail * 0.8
# feather the rectangle's edge 2 px against the original surroundings
ring = np.zeros((h, w)); ring[y0 - 2:y1 + 2, x0 - 2:x1 + 2] = 1; ring[y0 + 1:y1 - 1, x0 + 1:x1 - 1] = 0
blur = out.copy()
blur[1:-1, 1:-1] = (out[1:-1, 1:-1] * 4 + out[:-2, 1:-1] + out[2:, 1:-1] + out[1:-1, :-2] + out[1:-1, 2:]) / 8
out = np.where(ring[..., None] > 0, blur, out)
Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8)).save(dst, optimize=False)
