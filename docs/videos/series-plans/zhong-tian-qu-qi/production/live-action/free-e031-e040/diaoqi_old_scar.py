"""diaoqi_old_scar.py SRC DST : diaoqi-portrait-l1 (arc 4, 2026-11-17) from screen-test round-3 seed 37041.
The seed has the right face and clothes, but its scar on his left cheekbone (the right of the picture) is a short fresh
red cut. 1) The cut is found inside x 485-530, y 268-330: pixels whose R - G is 10 or more above its 11 px median and
whose luminance is 10 or more below its 11 px median (the flushed cheek is red but not darker), closed 2 px, plus any
pixel within 4 px of that with R - G > 68 (the wide middle of the cut), grown 2 px. 2) That area is filled with the
surrounding skin (a normalised Gaussian of the unmasked pixels, sigma 4, plus 0.7 of the skin grain of the same rows 45 px
to the left, the plain cheek). 3) An old healed scar is drawn back along the cut's own axis (a line fitted to the cut's
pixels, extended 25 % past each end): a thin line about 2 px wide, 12 brighter than the skin under it and a little
less saturated, with a soft edge."""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = a.shape
box = np.zeros((H, W), bool)
box[268:330, 485:530] = True
rg = a[..., 0] - a[..., 1]
lum = a @ np.array([0.299, 0.587, 0.114])
m = (rg - ndi.median_filter(rg, 11) > 10) & (ndi.median_filter(lum, 11) - lum > 10) & box
m = ndi.binary_closing(m, iterations=2)
m |= (rg > 68) & ndi.binary_dilation(m, iterations=4) & box
ys, xs = np.nonzero(m)
m = ndi.binary_dilation(m, iterations=2)
w = (~m).astype(np.float64)
num = np.stack([ndi.gaussian_filter(a[..., c] * w, 4) for c in range(3)], -1)
skin = num / np.maximum(ndi.gaussian_filter(w, 4)[..., None], 1e-6)
grain = a - ndi.gaussian_filter(a, (2, 2, 0))
skin = skin + 0.7 * np.roll(grain, 45, axis=1)   # grain of the plain cheek 45 px to the left
alpha = ndi.gaussian_filter(m.astype(np.float64), 1)[..., None]
alpha[m] = 1.0
out = a * (1 - alpha) + skin * alpha
# the cut's axis
cx, cy = xs.mean(), ys.mean()
u, s_, vt = np.linalg.svd(np.stack([xs - cx, ys - cy], 1), full_matrices=False)
d = vt[0]
t = (np.stack([xs - cx, ys - cy], 1) @ d)
t0, t1 = t.min() * 1.25, t.max() * 1.25
p0, p1 = (cx + d[0] * t0, cy + d[1] * t0), (cx + d[0] * t1, cy + d[1] * t1)
line = Image.new("L", (W, H), 0)
ImageDraw.Draw(line).line([p0, p1], fill=255, width=2)
la = ndi.gaussian_filter(np.asarray(line).astype(np.float64) / 255, 0.7)[..., None]
g = out.mean(-1, keepdims=True)
pale = g + (out - g) * 0.75 + 12
out = out * (1 - la) + pale * la
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst)
print("cut pixels", len(xs), "axis", [round(v) for v in (*p0, *p1)])
