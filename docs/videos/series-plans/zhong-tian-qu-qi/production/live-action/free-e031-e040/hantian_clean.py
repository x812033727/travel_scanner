"""Paint out the three tiny dark verticals on set-hantian-l1's far field line (2026-11-19, e034 independent review 建議 7).

The first pass (ffmpeg delogo) left soft grey boxes on the horizon that a model could grow into a pole, a figure or a patch of
mist (rule 33: a free paint-out continues the same material from beside it, soft-edged, never a box). Here each thin box is
filled by interpolating straight across it between the pixels just outside it: across each row for an upright pole ("h": the
horizon, the tree line and the furrows run across the picture and carry straight through), down each column for a thin flat
line ("v": the faint curved top of the goal-post-like frame). Each side's sample is the mean of the two pixels just outside the
box; the patch is feathered into the picture over two pixels. A wide box copying in a strip from beside it was tried first and
dragged neighbouring trees and the house wall into the sky, so the boxes are kept tight. Pure numpy and Pillow, no random
numbers: the same bytes on every run.
Boxes (mode, x0, y0, x1, y1; x1, y1 exclusive), looked at 8x: the thin pole by the right-hand houses; the right post of the thin
frame, the faint trace of its left post and its faint curved top; the small figure-like post on the field edge.
Usage: python3 -I hantian_clean.py refs-live/set-hantian-l1.png OUT.png
"""
import sys

import numpy as np
from PIL import Image

BOXES = [("h", 593, 354, 603, 376), ("h", 742, 366, 751, 387), ("h", 725, 361, 732, 377), ("v", 724, 363, 749, 372), ("h", 825, 376, 837, 395)]
FEATHER = 2

img = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=np.float64).copy()
for mode, x0, y0, x1, y1 in BOXES:
    src = img.copy()  # each box reads the picture as the earlier boxes left it
    ya, yb, xa, xb = y0 - FEATHER, y1 + FEATHER, x0 - FEATHER, x1 + FEATHER
    yy, xx = np.mgrid[ya:yb, xa:xb]
    if mode == "h":
        a = src[ya:yb, x0 - 2:x0].mean(axis=1)  # left, per row
        b = src[ya:yb, x1:x1 + 2].mean(axis=1)  # right, per row
        t = np.clip((xx - x0 + 0.5) / (x1 - x0), 0, 1)[..., None]
        fill = (1 - t) * a[:, None, :] + t * b[:, None, :]
    else:
        a = src[y0 - 2:y0, xa:xb].mean(axis=0)  # above, per column
        b = src[y1:y1 + 2, xa:xb].mean(axis=0)  # below, per column
        t = np.clip((yy - y0 + 0.5) / (y1 - y0), 0, 1)[..., None]
        fill = (1 - t) * a[None, :, :] + t * b[None, :, :]
    dx = np.maximum(np.maximum(x0 - xx, xx - (x1 - 1)), 0)
    dy = np.maximum(np.maximum(y0 - yy, yy - (y1 - 1)), 0)
    m = np.clip(1.0 - np.maximum(dx, dy) / (FEATHER + 1), 0, 1)[..., None]
    img[ya:yb, xa:xb] = m * fill + (1 - m) * src[ya:yb, xa:xb]
Image.fromarray(np.clip(np.rint(img), 0, 255).astype(np.uint8)).save(sys.argv[2], optimize=False)
