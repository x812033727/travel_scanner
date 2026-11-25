"""Paint out the same three tiny dark verticals on set-hantian-yang-l1's far field line (2026-11-20, e035 r2 d1 prep).

set-hantian-yang-l1 (screen test round 2, 37039) is set-hantian-l1 with the paddy in front of the ridge flooded and planted, so
it carries set-hantian-l1's thin pole by the right-hand houses, the thin goal-post-like frame and the small figure-like post on
the field edge, a few pixels to the right of where hantian_clean.py paints them on set-hantian-l1 (rules 13, 33, 34). The method
is hantian_clean.py's, unchanged (each thin box filled by interpolating straight across it from the two pixels just outside it,
across each row for an upright, down each column for the frame's faint curved top; feathered over two pixels; numpy and Pillow,
no random numbers: the same bytes on every run); only the boxes differ, looked at 8x on set-hantian-yang-l1.
Boxes (mode, x0, y0, x1, y1; x1, y1 exclusive): the pole by the houses; the frame's right post, its faint left post, its top;
the figure-like post.
Usage: python3 -I hantian_yang_clean.py refs-live/set-hantian-yang-l1.png OUT.png
"""
import sys

import numpy as np
from PIL import Image

BOXES = [("h", 594, 354, 604, 377), ("h", 749, 363, 757, 387), ("h", 733, 365, 740, 383), ("v", 733, 362, 756, 371), ("h", 837, 378, 846, 395)]
FEATHER = 2

img = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=np.float64).copy()
for mode, x0, y0, x1, y1 in BOXES:
    src = img.copy()
    ya, yb, xa, xb = y0 - FEATHER, y1 + FEATHER, x0 - FEATHER, x1 + FEATHER
    yy, xx = np.mgrid[ya:yb, xa:xb]
    if mode == "h":
        a = src[ya:yb, x0 - 2:x0].mean(axis=1)
        b = src[ya:yb, x1:x1 + 2].mean(axis=1)
        t = np.clip((xx - x0 + 0.5) / (x1 - x0), 0, 1)[..., None]
        fill = (1 - t) * a[:, None, :] + t * b[:, None, :]
    else:
        a = src[y0 - 2:y0, xa:xb].mean(axis=0)
        b = src[y1:y1 + 2, xa:xb].mean(axis=0)
        t = np.clip((yy - y0 + 0.5) / (y1 - y0), 0, 1)[..., None]
        fill = (1 - t) * a[None, :, :] + t * b[None, :, :]
    dx = np.maximum(np.maximum(x0 - xx, xx - (x1 - 1)), 0)
    dy = np.maximum(np.maximum(y0 - yy, yy - (y1 - 1)), 0)
    m = np.clip(1.0 - np.maximum(dx, dy) / (FEATHER + 1), 0, 1)[..., None]
    img[ya:yb, xa:xb] = m * fill + (1 - m) * src[ya:yb, xa:xb]
Image.fromarray(np.clip(np.rint(img), 0, 255).astype(np.uint8)).save(sys.argv[2], optimize=False)
