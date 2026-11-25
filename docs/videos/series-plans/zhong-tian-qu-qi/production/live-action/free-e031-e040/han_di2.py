"""han_di2.py SRC DST : set-xujia-yuan-han-di2-l1 (arc 4, 2026-11-17, e031 review; coordinator's decision) for the e031 s21
insert (the red clay bowl held over the earth). set-xujia-yuan-han-di-l1 has the same pale leaf-shaped stone chip as -dong-di-l1
(bottom left, about x 295-530, y 590-670) and a smaller chip upper left (x 255-385, y 320-365): in e930 d1 s32 both takes turned
the falling paper into a leaf of that shape. colab/runs/e930-live/fix1/clean_di.py's way: each box covered by plain earth DX px
to its side on the same rows, scaled per channel to the mean of an 8 px ring round the box; the mask shrunk 12 px and
Gaussian-blurred 9 px.
Run: python3 -I han_di2.py refs-live/set-xujia-yuan-han-di-l1.png OUT/set-xujia-yuan-han-di2-l1.png"""
import sys
import numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
out = a.copy(); mask = np.zeros(a.shape[:2])
BOXES = [((262, 568, 560, 706), -258), ((222, 420, 292, 398), 200)]  # (x0, x1, y0, y1), dx of the source patch
RING = 8
for (x0, x1, y0, y1), dx in BOXES:
    patch = a[y0:y1, x0 + dx:x1 + dx]
    ring = np.concatenate([a[y0 - RING:y0, x0:x1].reshape(-1, 3), a[y1:y1 + RING, x0:x1].reshape(-1, 3),
                           a[y0:y1, x0 - RING:x0].reshape(-1, 3), a[y0:y1, x1:x1 + RING].reshape(-1, 3)]).mean(axis=0)
    out[y0:y1, x0:x1] = patch * (ring / np.maximum(patch.reshape(-1, 3).mean(axis=0), 1))
    mask[y0 + 12:y1 - 12, x0 + 12:x1 - 12] = 1
m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float64)[..., None] / 255
Image.fromarray(np.clip(a * (1 - m) + out * m, 0, 255).astype(np.uint8)).save(dst)
