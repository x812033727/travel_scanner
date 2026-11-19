"""citang_ye_clean.py SRC DST : set-citang-ye2-l1 (arc 4, 2026-11-19, e033 r2 d1 prep) from the free night hall set-citang-ye-l1
(citang_ye.py: only the doorway zone x < 565 turned to night). set-citang-ye-l1 was made from set-citang-l1 before e032 found the
thin black crack strokes on the main beam that could grow into writing (rule 33; citang_huang.py step (b) paints them out of the
dusk hall). e033 c05-c11 take the beam down by torchlight, so the night hall gets the same step (b), byte for byte the same code:
each column sheared so the beam runs level, a 9 x 31 median along the beam gives its plain wood, and the pixels darker than that
by 6 or more inside the beam band (only where the plain wood is darker than 34) are replaced by it (dilated 2 px, feathered
1.2 px). The doorway zone (citang_ye.py's change) lies left of x 565 and the beam band right of x 560, so the night doorway is
left as it was."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = a.shape
xs = np.arange(W)[None, :].repeat(H, 0)
ys = np.arange(H)[:, None].repeat(W, 1)
SLOPE, X0, Y0, THICK = 0.42, 700, 160, 80
shift = np.round(SLOPE * (np.arange(W) - X0)).astype(int)
PAD = 320
sheared = np.zeros((H + 2 * PAD, W, 3))
for x in range(W):
    s = PAD + shift[x]
    sheared[s:s + H, x] = a[:, x]
bg = np.stack([ndi.median_filter(sheared[..., c], size=(9, 31), mode="nearest") for c in range(3)], -1)
bg_back = np.zeros_like(a)
for x in range(W):
    s = PAD + shift[x]
    bg_back[:, x] = bg[s:s + H, x]
ylow = Y0 - SLOPE * (xs - X0)
band = (ys >= ylow - THICK - 4) & (ys <= ylow + 2) & (xs >= 560)
Lw = a @ np.array([0.299, 0.587, 0.114])
Lb = bg_back @ np.array([0.299, 0.587, 0.114])
wood = band & (Lb < 34)
crack = wood & (Lb - Lw >= 6)
crack = ndi.binary_dilation(crack, iterations=2) & wood
m = np.clip(ndi.gaussian_filter(crack.astype(np.float64), 1.2) * 1.6, 0, 1)
a = a * (1 - m[..., None]) + bg_back * m[..., None]
Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)).save(dst)
print("crack pixels", int(crack.sum()))
