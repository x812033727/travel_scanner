"""jingkeng_jingdi.py SRC DST : set-jingkeng-jingdi-l1 (arc 4, 2026-11-18, e032 d1 prep; coordinator's decision) for the e032 s16
insert (two hands and a pick at the bottom of a deep narrow shaft, looking straight down). set-jingkeng-di-l1 is bright orange
dry furrows (ridges, stalks, a brick-like crack pattern): sent to s16 it would grow a lit field. This keeps only the SOIL of
set-jingkeng-di-l1: its mean colour per channel, pulled to a damp dark yellow-brown, laid on a grain that is fixed seeded noise
at three scales (no ridges, no cracks, no pit mouth, no bricks, nobody), then a soft vignette and one narrow warm orange
gradient along the top edge (the evening light at the shaft's mouth, r2.py s16: "only a thin warm orange glow along the top
edge, the rest in shadow"). d1 sends it only as the colour and grain of the soil (e932-live/mkspec.py), never as the place.
Deterministic (numpy default_rng(932016), PIL lanczos, no timestamps): two runs are byte-identical.
Run: python3 -I jingkeng_jingdi.py refs-live/set-jingkeng-di-l1.png OUT/set-jingkeng-jingdi-l1.png"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
W, H = 1312, 736
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
mean = a.reshape(-1, 3).mean(axis=0)                       # the soil's own colour (orange-lit dry earth)
damp = mean / mean.max() * np.array([0.42, 0.36, 0.24]) * 255 / np.array([1.0, 0.86, 0.62])  # darker, yellower, less orange
damp = np.clip(damp, 0, 255)

rng = np.random.default_rng(932016)


def noise(scale):
    small = rng.standard_normal((H // scale + 2, W // scale + 2))
    im = Image.fromarray(((small - small.min()) / (small.max() - small.min()) * 255).astype(np.uint8))
    im = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(max(1, scale // 3)))
    return np.asarray(im).astype(np.float64) / 255 - 0.5


grain = 0.55 * noise(48) + 0.30 * noise(12) + 0.15 * noise(3)   # lumps, clods, fine grit
img = damp[None, None, :] * (1 + 0.55 * grain[..., None])
# moist sheen: a few darker wet patches
wet = noise(96)
img *= (1 - 0.18 * np.clip(wet * 2, 0, 1))[..., None]
# shadow toward the edges (the shaft walls close in)
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.58) / (H / 2)) ** 2)
img *= (1 - 0.45 * np.clip(r - 0.35, 0, 1))[..., None]
# one narrow warm orange gradient along the top edge
g = np.clip(1 - yy / (H * 0.16), 0, 1) ** 2
orange = np.array([235.0, 140.0, 60.0])
img = img * (1 - 0.55 * g[..., None]) + orange[None, None, :] * (0.55 * g[..., None])
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(dst, optimize=False)
