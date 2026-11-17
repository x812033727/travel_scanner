"""tangfang_chen.py SRC DST : free dawn grade trial of set-xujia-tangfang-l2 (arc 4, 2026-11-17; bible 〈盤點〉 -tangfang-chen).
(a) the candle flame and its halo (x 1142-1185, y 458-497) is filled by harmonic diffusion from the headboard and wall around it;
(b) the lit wax (x 1144-1187, y 497-552, pixels brighter than 20) is repainted as an unlit neutral grey-white
    cylinder (118 at the top to 78 at the foot, 45 darker at the sides), before (a) so the fill does not
    take the lit wax top as its edge;
(c) the warm candle glow on the right wall and the table is cooled: inside a soft circle around the flame, R/G are pulled
    toward B by the glow's strength;
(d) the two window panes (x 789-887 and 898-1002, y 172-329; pixels darker than 26 keep, the H-shaped bolt) become a pale dawn
    white (top 212,214,218 -> bottom 190,196,204), feathered 1.5 px;
(e) a soft cool fall-off of window light (radius 520 px) brightens the wall around the window, the bed and the table;
then ffmpeg eq=gamma=1.6:contrast=1.1 over the whole picture (the bible's grade)."""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = a.shape
yy, xx = np.mgrid[0:H, 0:W]
# (b) wax: every body pixel (brighter than 70 inside the candle box) to a neutral grey-white, keeping its shading
box = (slice(497, 552), slice(1144, 1187))
w = a[box]; lum = w.mean(-1, keepdims=True)
body = lum > 20
shade = 118 - np.linspace(0, 40, w.shape[0])[:, None, None] - np.abs(np.linspace(-1, 1, w.shape[1]))[None, :, None] ** 2 * 45
a[box] = np.where(body, shade * np.array([1.0, 1.0, 1.03]), w)
# (a) flame: harmonic fill from the headboard and wall around it
hole = np.zeros((H, W), bool); hole[458:497, 1142:1185] = True
k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]])
p = a[440:520, 1120:1210]; hp = hole[440:520, 1120:1210]
p[hp] = np.median(p[ndi.binary_dilation(hp, iterations=2) & ~hp], axis=0)
for _ in range(600):
    for c in range(3):
        p[..., c][hp] = ndi.convolve(p[..., c], k, mode="nearest")[hp]
# (c) cool the glow
d = np.hypot(xx - 1163, yy - 490); g = np.clip(1 - d / 260, 0, 1)[..., None] ** 1.5
lum = a.mean(-1, keepdims=True)
a = a * (1 - 0.8 * g) + lum * np.array([0.92, 0.98, 1.08]) * 0.8 * g
# (d) window
pane = np.zeros((H, W), bool); pane[172:330, 789:888] = True; pane[172:330, 898:1003] = True
pane &= a.mean(-1) > 26  # the H-shaped bolt stays
alpha = np.maximum(ndi.gaussian_filter(pane.astype(float), 1.5), pane)[..., None]
t = np.clip((yy - 166) / 168, 0, 1)[..., None]
sky = np.array([212, 214, 218]) * (1 - t) + np.array([190, 196, 204]) * t
a = a * (1 - alpha) + sky * alpha
# (e) window light fall-off
d = np.hypot(xx - 897, (yy - 250) * 1.3); f = np.clip(1 - d / 520, 0, 1)[..., None] ** 2
a = a + f * np.array([38, 40, 44]) * (1 - pane[..., None])
tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
Image.fromarray(np.clip(np.rint(a), 0, 255).astype(np.uint8)).save(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-vf", "eq=gamma=1.6:contrast=1.1", dst], check=True)
os.unlink(tmp)
