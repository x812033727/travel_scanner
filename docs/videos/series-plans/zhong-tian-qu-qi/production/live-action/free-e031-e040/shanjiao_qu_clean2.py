"""e936 cut review 2 中等 1 (2026-11-21, REVIEW 3): the far skyline of set-shanjiao-qu-jing-l1 has a small square bump above the
tree line on the right (x 1058-1128, y 316-335), one thin spike (x 1252-1272) and a row of faint blocky shapes in the haze at the
vanishing point (x 852-1004, y 332-347); the model grew them into a cluster of modern tower blocks in e936 s21 and s29. Each
region is repainted row by row as a straight blend from the pixel just left of it to the pixel just right of it (sky over the
bump and the spike, so the tree line runs on at its neighbours' height; haze over the faint shapes), 1 px feathered. Free and
deterministic; new ids from it (shanjiao_qu.sh): -jing2, -tian3, -xi3, -xi3-zhuo.
Usage: python3 -I shanjiao_qu_clean2.py set-shanjiao-qu-jing-l1.png OUT.png
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
out = a.copy()
for x0, x1, y0, y1 in ((1058, 1128, 316, 336), (1252, 1272, 314, 336), (852, 1004, 332, 347)):
    L = a[y0:y1, x0 - 3:x0].mean(axis=1)
    R = a[y0:y1, x1:x1 + 3].mean(axis=1)
    t = (np.arange(x1 - x0) + 0.5) / (x1 - x0)
    out[y0:y1, x0:x1] = L[:, None, :] * (1 - t[None, :, None]) + R[:, None, :] * t[None, :, None]
    # 1 px feather against the original on the rectangle's edge
    for yy in (y0, y1 - 1):
        out[yy, x0:x1] = (out[yy, x0:x1] + a[yy, x0:x1]) / 2
Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8)).save(dst, optimize=False)
