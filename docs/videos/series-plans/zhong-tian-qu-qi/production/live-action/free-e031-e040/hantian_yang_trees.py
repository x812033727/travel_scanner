"""Drain the colour from the far tree line of the cleaned set-hantian-yang-l1 before its dawn grade (2026-11-20, e035 independent
review 建議 2). The misty dawn grade (-chen) washed the far red tree to salmon pink and the yellow ones to milky white: at 960x544
they read as an orchard in blossom, the very thing 原版必修 e035 removes. Here a feathered band over the far tree line (y 320-400,
12 px feather, left of x 1000 so the big willow at the right stays as it is) pulls the coloured pixels (saturation over 40,
ramped to full at 80) 75% toward a dull olive brown of the same lightness. Pure numpy and Pillow, no random numbers.
Usage: python3 -I hantian_yang_trees.py CLEANED.png OUT.png
"""
import sys

import numpy as np
from PIL import Image

img = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=np.float64)
h, w, _ = img.shape
y = np.arange(h)[:, None]
x = np.arange(w)[None, :]
band = np.clip(np.minimum(y - 320, 400 - y) / 12.0, 0, 1) * (x < 1000)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b
sat = np.maximum(r, np.maximum(g, b)) - np.minimum(r, np.minimum(g, b))
m = band * np.clip((sat - 40) / 40, 0, 1)
k = 0.75
tgt = np.stack([lum * 0.92, lum * 0.88, lum * 0.74], -1)
out = img * (1 - m[..., None] * k) + tgt * (m[..., None] * k)
Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8)).save(sys.argv[2], optimize=False)
