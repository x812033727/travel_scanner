"""ye_dong2.py SRC DST : set-xujia-yuan-ye-dong2-l1 (arc 4, 2026-11-17, e031 review 必改 3; coordinator's decision) for the e031
night wides s07, s08. set-xujia-yuan-ye-dong-l1 still has (a) the dark blank board on the house wall right of the doorway
(x 251-302, y 306-373: a hung board grows writing, rule 33) and (b) the lantern's light without a lantern round the right post of
the yard gate (the post lit about 2.7x the left post, the scalloped eave edge above it lit, and vertical warm streaks in the dark
gap between the post and the tree, x 678-750, y 296-348): a light with no body grows the lantern back.
(a) as e930's clean_yard.py (a), widened left to x 224 to take the board's cast shadow too: the stone wall 68 px below moved
up, each row scaled to the wall left (x 210-221) and right (x 304-315) of it.
(b) the dark gap: every row replaced by its own median over the gap (the streaks go, the row's tone stays), then x0.8; the post
and the eave edge: a smooth gain (Gaussian blob centred on the post top, sigma 34 x 70 px) pulling them down to the left post's
level (gain 0.42 at the centre). Masks Gaussian-blurred 1.5 px.
Run: python3 -I ye_dong2.py refs-live/set-xujia-yuan-ye-dong-l1.png OUT/set-xujia-yuan-ye-dong2-l1.png"""
import sys
import numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
out = a.copy()
H, W, _ = a.shape
mask = np.zeros((H, W))
# (a) the board
dy = 68
patch = a[306 + dy:374 + dy, 224:303].copy()
for i, y in enumerate(range(306, 374)):
    ref = np.concatenate([a[y, 210:222], a[y, 304:316]]).mean(axis=0)
    src_ref = np.concatenate([a[y + dy, 210:222], a[y + dy, 304:316]]).mean(axis=0)
    patch[i] *= ref / np.maximum(src_ref, 1)
out[306:374, 224:303] = patch
mask[306:374, 224:303] = 1
# (b1) the streaked dark gap right of the post
gx0, gx1, gy0, gy1 = 680, 748, 297, 346
for y in range(gy0, gy1):
    out[y, gx0:gx1] = np.median(a[y, gx0:gx1], axis=0) * 0.8
mask[gy0:gy1, gx0:gx1] = 1
m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
m = np.asarray(m).astype(np.float64)[..., None] / 255
res = a * (1 - m) + out * m
# (b2) the lit post and eave edge: a smooth gain
yy, xx = np.mgrid[0:H, 0:W]
blob = np.exp(-(((xx - 676) / 34.0) ** 2 + ((yy - 318) / 70.0) ** 2) / 2)
gain = 1 - 0.58 * blob
res = res * gain[..., None]
Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(dst)
