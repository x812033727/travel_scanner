# Run: python3 -I clean_di.py refs-live/set-xujia-yuan-dong-di-l1.png refs-live/set-xujia-yuan-dong-di2-l1.png
# e930 fix1 s32: set-xujia-yuan-dong-di2-l1 = set-xujia-yuan-dong-di-l1 with the two pale leaf-shaped chips painted out
# (the big one bottom-left, the small one upper-left): in d1 both takes of s32 turned the torn halves into one small
# leaf-shaped scrap after ~1.3-1.5 s, the shape this picture already holds. Each box is covered by plain earth DX px to
# its side on the same rows, scaled per channel to the mean of a ring round the box; mask Gaussian-blurred.
import sys
import numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
out = a.copy(); mask = np.zeros(a.shape[:2])
BOXES = [((310, 590, 520, 640), -270), ((272, 445, 260, 350), 170)]  # (x0, x1, y0, y1), dx of the source patch
RING = 8
for (x0, x1, y0, y1), dx in BOXES:
    patch = a[y0:y1, x0 + dx:x1 + dx]
    ring = np.concatenate([a[y0 - RING:y0, x0:x1].reshape(-1, 3), a[y1:y1 + RING, x0:x1].reshape(-1, 3),
                           a[y0:y1, x0 - RING:x0].reshape(-1, 3), a[y0:y1, x1:x1 + RING].reshape(-1, 3)]).mean(axis=0)
    out[y0:y1, x0:x1] = patch * (ring / np.maximum(patch.reshape(-1, 3).mean(axis=0), 1))
    mask[y0 + 14:y1 - 14, x0 + 14:x1 - 14] = 1
m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float64)[..., None] / 255
Image.fromarray(np.clip(a * (1 - m) + out * m, 0, 255).astype(np.uint8)).save(dst)
