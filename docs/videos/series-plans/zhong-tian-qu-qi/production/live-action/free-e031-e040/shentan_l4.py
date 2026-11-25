"""shentan_l4.py SRC DST : set-shentan-l3 -> set-shentan-l4, one paddle made pale fresh-cut wood (arc 4, 2026-11-19, e033 live
fix1 s34). Free: PIL and numpy only, no generation.

Why: in d1 both takes of s34 ("the wheel turns half a turn, slows and stops") turned one to three paddles' worth (A: about
40-50 and 20 degrees) and the twelve paddles all look alike, so nobody can see how far it went (both pickers, RETAKE; review B
asked for a marker). s39's line is 「就轉半圈」. With one paddle lighter than the other eleven the turn has a unit: the pale
paddle starts at the top of the wheel in the first frame and ends at the bottom when the wheel has turned half a turn.

What: the paddle standing straight up at the top of the rim (corners about (575,79), (628,71), (636,152), (583,160) in the
1312x736 master; the rim below it is left alone). Only the paddle's wood inside that quadrilateral changes (pixels redder than
they are blue by 25 or more, so the sky around it stays); the wood is pulled toward a pale blond new-cut colour while keeping
its own grain (the luminance pattern is kept, the colour is a blend), with a 1.5 px feather on the mask edge.
Run: python3 -I shentan_l4.py refs-live/set-shentan-l3.png refs-live/set-shentan-l4.png   (deterministic, byte for byte)."""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
assert im.size == (1312, 736), im.size
a = np.asarray(im).astype(np.float64)
quad = [(574, 78), (629, 70), (637, 152), (582, 161)]
m = Image.new("L", im.size, 0)
ImageDraw.Draw(m).polygon(quad, fill=255)
wood = (a[..., 0] - a[..., 2]) >= 25
mask = np.asarray(m) > 0
mask &= wood
mi = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
w = np.asarray(mi).astype(np.float64)[..., None] / 255.0
lum = a @ np.array([0.299, 0.587, 0.114])
ref = lum[mask].mean()
pale = np.array([236.0, 214.0, 172.0])  # pale blond new-cut pine
grain = np.clip(lum / ref, 0.6, 1.3)[..., None]
target = np.clip(pale * grain, 0, 255)
out = a * (1 - w) + (0.15 * a + 0.85 * target) * w
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, optimize=False)
print(dst, "paddle pixels:", int(mask.sum()), "mean luma before %.0f after %.0f" % (
    ref, (np.clip(out, 0, 255) @ np.array([0.299, 0.587, 0.114]))[mask].mean()))
