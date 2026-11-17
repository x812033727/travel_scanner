"""clean_shangyou_box.py SRC DST : set-shangyou-ba-l1 (arc 4, 2026-11-17) from screen-test round-3 seed 37042.
Far up the valley, just above the far field ridge, stands one small dark upright box (x 509-524, y 310-327): a shed or a
stone block with a blank face, the kind of plain board that grows writing (rule 33). The box x 507-526, y 308-329 is
filled by harmonic (Laplace) diffusion from the pixels around it (so the sloping bank behind and the green field below
run on smoothly; a straight copy from 22 px to the left left a step in the bank), then a little of the neighbours'
grain is put back: the fill gets the high-pass detail of the same rows 22 px to the left, at half strength."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
x0, x1, y0, y1, dx = 507, 527, 308, 330, 22
m = np.zeros(a.shape[:2], bool)
m[y0:y1, x0:x1] = True
out = a.copy()
out[m] = 0
for _ in range(3000):
    avg = (np.roll(out, 1, 0) + np.roll(out, -1, 0) + np.roll(out, 1, 1) + np.roll(out, -1, 1)) / 4
    out[m] = avg[m]
hp = a - ndi.gaussian_filter(a, (2, 2, 0))
out[y0:y1, x0:x1] += 0.5 * hp[y0:y1, x0 - dx:x1 - dx]
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst)
