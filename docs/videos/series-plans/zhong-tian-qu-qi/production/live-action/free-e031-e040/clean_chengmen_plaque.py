"""clean_chengmen_plaque.py SRC DST [DX] [SLOPE] : paint the blank-looking plaque with faint fake characters out of
screen-test seed 37038 of set-chengmen-ye-l1 (arc 4, 2026-11-17; rule 33: no hung signs, plaques grow writing).
The plaque is masked as the parallelogram at the top edge above the gate arch, x 246-406, its lower edge from y 26 at
x 246 to y 86 at x 406, following the brick courses (DX 132 was tried first: its source reaches the plaque's own
lower-right orange frame and leaves an L-shaped mark, so DX is 160). Each masked pixel (x, y) takes the wall pixel
(x + DX, y + SLOPE * DX), i.e. the same brick course further right, so the courses run on; the patch is scaled
per colour channel to the mean of a 6 px ring of wall around the mask, and the mask is feathered 4 px."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
DX = int(sys.argv[3]) if len(sys.argv) > 3 else 160
SLOPE = float(sys.argv[4]) if len(sys.argv) > 4 else 0.40
im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(np.float64)
H, W, _ = a.shape
poly = [(246, 0), (406, 0), (406, 86), (246, 26)]
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).polygon(poly, fill=255)
mask = np.asarray(m) > 0
ring_img = m.filter(ImageFilter.MaxFilter(13))
ring = (np.asarray(ring_img) > 0) & ~mask
ys, xs = np.nonzero(mask)
dy = int(round(SLOPE * DX))
patch = a.copy()
patch[ys, xs] = a[ys + dy, xs + DX]
# match colour to the surrounding wall
src_ring = a[np.nonzero(ring)[0] + 0, np.nonzero(ring)[1]]
ry, rx = np.nonzero(ring)
pr = a[np.clip(ry + dy, 0, H - 1), np.clip(rx + DX, 0, W - 1)]
gain = a[ry, rx].mean(0) / np.maximum(pr.mean(0), 1)
patch[ys, xs] *= gain
alpha = np.asarray(m.filter(ImageFilter.GaussianBlur(4))).astype(np.float64)[..., None] / 255.0
alpha[mask] = 1.0
out = a * (1 - alpha) + patch * alpha
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, pnginfo=None)
print("gain", gain.round(3), "pixels", mask.sum())
