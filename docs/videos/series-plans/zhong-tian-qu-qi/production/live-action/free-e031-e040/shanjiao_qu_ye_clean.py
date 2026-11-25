"""e037 r2 d1 prep (2026-11-23): the e036 cleaning done again on the paid night picture set-shanjiao-qu-ye-l1 (screen test round 5,
37046: set-shanjiao-qu-l1 relit as a clear cold blue night with a thin crescent moon), free and deterministic, so the night
channel of e037 scene 2 (and the dawn grade made from it, shanjiao_qu_ye_e937.sh) carries none of what the e036 reviews took out
of the day picture:
1. the white modern guard rail along the terraced bank at the far left (x 0-500, a 13 px band from y 325 + 0.024 x): each column
   of the band is replaced by the slope 13 px below it (shanjiao_qu_clean.py's step 1, the same geometry);
2. the flat upright board under the plank (x 724-816, y 374-510 here: the night edit drew it a little wider and taller than in
   the day picture, with a cap on top, so shanjiao_qu_clean.py's rectangle leaves a ghost of it): above the plank each row is a
   straight blend from the pixel left of it to the pixel right of it; the plank band is the same blend (the plank runs on
   across); below the plank the rows are copied from 92 px to the right (the cracked bed), one 8 px strip of the board's own wood
   kept as a thin post holding the plank; 2 px feathered;
3. the small blocky bumps on the far tree line at the right (x 1080-1128, y 318-336; e936 cut review 2: the model grows them into
   tower blocks): each row blended across from its left to its right neighbour (shanjiao_qu_clean2.py's way);
4. the crescent moon and its glow (centre about x 418, y 100): inside a 78 px radius the sky is replaced by a quadratic surface
   fitted to the sky in the ring 80-110 px from the centre, feathered over the outer 20 px. e036's yard showed a full moon (e936
   s36, s38) and e037's back gate picture a full moon; a crescent here would break the night, so the channel shows the moonlight
   and no moon. The one small star just right of it stays.
Usage: python3 -I shanjiao_qu_ye_clean.py set-shanjiao-qu-ye-l1.png OUT.png
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
h, w, _ = a.shape
out = a.copy()


def blend_rows(img, ref, x0, x1, y0, y1):
    L = ref[y0:y1, x0 - 3:x0].mean(axis=1)
    R = ref[y0:y1, x1:x1 + 3].mean(axis=1)
    t = (np.arange(x1 - x0) + 0.5) / (x1 - x0)
    img[y0:y1, x0:x1] = L[:, None, :] * (1 - t[None, :, None]) + R[:, None, :] * t[None, :, None]


def feather(img, ref, x0, x1, y0, y1, k=2):
    ring = np.zeros((h, w))
    ring[y0 - k:y1 + k, x0 - k:x1 + k] = 1
    ring[y0 + k:y1 - k, x0 + k:x1 - k] = 0
    blur = img.copy()
    blur[1:-1, 1:-1] = (img[1:-1, 1:-1] * 4 + img[:-2, 1:-1] + img[2:, 1:-1] + img[1:-1, :-2] + img[1:-1, 2:]) / 8
    return np.where(ring[..., None] > 0, blur, img)


# 1. the rail
for x in range(0, 500):
    top = int(round(325 + x * 0.024))
    out[top:top + 13, x] = a[top + 13:top + 26, x]
# 2. the board
x0, x1, y0, y1, dx = 724, 816, 374, 510, 92
plank0, plank1 = 426, 451
blend_rows(out, a, x0, x1, y0, plank1)
out[plank1:y1, x0:x1] = a[plank1:y1, x0 + dx:x1 + dx]
out[plank1:y1, 766:774] = a[plank1:y1, 766:774]
out = feather(out, a, x0, x1, y0, y1)
# 3. the skyline bumps
blend_rows(out, a, 1080, 1128, 318, 336)
# 4. the moon
cx, cy, r_in, r_fit = 418, 100, 78, 110
yy, xx = np.mgrid[0:h, 0:w]
d = np.hypot(xx - cx, yy - cy)
fit = (d >= 80) & (d <= r_fit)
X = np.stack([np.ones(fit.sum()), xx[fit] - cx, yy[fit] - cy, (xx[fit] - cx) ** 2, (yy[fit] - cy) ** 2, (xx[fit] - cx) * (yy[fit] - cy)], 1)
inside = d < r_in + 20
Xi = np.stack([np.ones(inside.sum()), xx[inside] - cx, yy[inside] - cy, (xx[inside] - cx) ** 2, (yy[inside] - cy) ** 2, (xx[inside] - cx) * (yy[inside] - cy)], 1)
wgt = np.clip((r_in + 20 - d[inside]) / 20, 0, 1)
for ch in range(3):
    coef, *_ = np.linalg.lstsq(X, a[..., ch][fit], rcond=None)
    sky = Xi @ coef
    col = out[..., ch]
    col[inside] = col[inside] * (1 - wgt) + sky * wgt
    out[..., ch] = col
Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8)).save(dst, optimize=False)
