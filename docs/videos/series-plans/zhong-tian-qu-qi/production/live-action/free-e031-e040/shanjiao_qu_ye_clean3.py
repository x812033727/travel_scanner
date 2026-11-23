"""e037 independent review 必改 6 (2026-11-23): shanjiao_qu_ye_clean.py again, with step 1 done another way. Its rail step
replaced each column of the 13 px band by the slope 13 px below it, and on the night picture that slope is the bright step of the
terraced bank: it left one flat bright strip (about x 310-500, y 337-348) cut off square at x = 500, which the crops -zhuo,
-kong, -cao and the dawn grade put behind people (it reads as a kerb or a rail and would grow back). Here each column of the band
(widened by 2 px above and below) is a straight blend from the pixel 2 px above the band to the pixel 2 px below it, the work runs
to x 520 and fades into the original over x 480-520. Steps 2-4 (the board, the skyline bumps, the moon) are shanjiao_qu_ye_clean.py's,
unchanged. New ids from it (shanjiao_qu_ye_e937.sh): -ye3 and its crops; -ye2 stays as it was, never sent again.
Usage: python3 -I shanjiao_qu_ye_clean3.py set-shanjiao-qu-ye-l1.png OUT.png
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


# 1. the rail: a straight blend down each column from just above the band to just below it, faded out over x 480-520
for x in range(0, 520):
    top = int(round(325 + x * 0.024)) - 2
    bot = top + 17
    up, down = a[top - 2, x], a[bot + 2, x]
    tt = (np.arange(bot - top) + 0.5) / (bot - top)
    fill = up[None, :] * (1 - tt[:, None]) + down[None, :] * tt[:, None]
    fw = 1.0 if x < 480 else (520 - x) / 40
    out[top:bot, x] = fill * fw + a[top:bot, x] * (1 - fw)
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
