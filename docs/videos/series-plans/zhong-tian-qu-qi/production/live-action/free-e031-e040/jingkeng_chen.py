"""jingkeng_chen.py SRC DST : the trunk-free base for set-jingkeng-chen-l1 (arc 4, 2026-11-18, e032 r2 review 必改 1 and 建議).
In the round-2 winner set-jingkeng-l1 (seed 37040) a thin crownless tree trunk stands alone in the far field (x 836-843,
y 378-391): small, it reads as a standing person (rule 34: the count). Each row of the box x 832-848, y 374-394 is replaced by a
straight blend between the field pixels just left (x 831) and right (x 849) of it, feathered 1 px. jingkeng_chen.sh then
grades this base to a grey dawn and crops it."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
x0, x1, y0, y1 = 832, 848, 374, 394
fill = a.copy()
for y in range(y0, y1 + 1):
    left, right = a[y, x0 - 1], a[y, x1 + 1]
    for x in range(x0, x1 + 1):
        t = (x - (x0 - 1)) / (x1 + 1 - (x0 - 1))
        fill[y, x] = left * (1 - t) + right * t
m = np.zeros(a.shape[:2])
m[y0:y1 + 1, x0:x1 + 1] = 1
m = np.clip(ndi.gaussian_filter(m, 1.0) * 1.3, 0, 1)
out = a * (1 - m[..., None]) + fill * m[..., None]
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst)
