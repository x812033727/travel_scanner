"""shentan_l5.py SRC DST : set-shentan-l3 -> set-shentan-l5, the nine o'clock paddle made pale fresh-cut wood (arc 4,
2026-11-19, e033 live fix2 s34). Free: PIL and numpy only, no generation. Same method as shentan_l4.py, other paddle.

Why: fix1 put the pale paddle at the top of the wheel (set-shentan-l4) and asked for half a turn. Measured with
scratchpad rot6.py, the two fix1 takes turned about 38 and 66 degrees (this H3 route turns 40-70 degrees in 6-8 s), so the
pale paddle stopped at ten and nine o'clock, plainly short of the bottom; the marker made the short turn easier to see.
fix2 moves the marker next to where the wheel can actually get to: the paddle on the left side of the rim, level with the
hub (nine o'clock). A quarter turn down the left side brings it to the bottom, into the water, and the shot reads as
"the pale paddle turned down into the water and the wheel stopped dead". The water comes from the left and pushes the
lower rim to the right, so the top goes left and the left side goes down.

What: the horizontal paddle left of the rim (x 377-445, y 327-374 in the 1312x736 master; it sits about 15 px above the
hub at about (601,365); the rim and its iron bracket start at x 446 and are left alone). Unlike l4 the paddle is in front
of sand, not sky, and sand is also redder than blue, so the mask is the rectangle AND darker than luma 150 (paddle 40-140,
sand and haze 160-220). l4's pale blond (236,214,172) is the colour of the sand right behind and below this paddle
(measured 234,209,172) and the first try vanished into it, so here the board goes near-white planed pine (250,240,212),
keeps its grain with a narrower luminance ratio (0.75-1.1, so the shadowed right half stays a little darker), and keeps a
2 px dark rim (the mask eroded by a 5x5 min filter, then a 1.5 px feather) so it reads as a framed board against the sand. The other eleven paddles do not change.
l3 has no wooden flume on the left (only the stone steps and a plank landing), so the fix2 prompt carries the water by text.
Run: python3 -I shentan_l5.py assets/refs-live/set-shentan-l3.png assets/refs-live/set-shentan-l5.png   (deterministic)."""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
assert im.size == (1312, 736), im.size
a = np.asarray(im).astype(np.float64)
quad = [(377, 327), (445, 327), (445, 374), (377, 374)]
m = Image.new("L", im.size, 0)
ImageDraw.Draw(m).polygon(quad, fill=255)
lum = a @ np.array([0.299, 0.587, 0.114])
mask = (np.asarray(m) > 0) & (lum < 150)
inner = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 0  # keep a 2 px dark rim
mi = Image.fromarray((inner * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
w = np.asarray(mi).astype(np.float64)[..., None] / 255.0
ref = lum[mask].mean()
pale = np.array([250.0, 240.0, 212.0])  # near-white planed pine: l4's blond is the colour of the sand behind this paddle
grain = np.clip(lum / ref, 0.75, 1.1)[..., None]
target = np.clip(pale * grain, 0, 255)
out = a * (1 - w) + (0.15 * a + 0.85 * target) * w
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, optimize=False)
print(dst, "paddle pixels:", int(mask.sum()), "recoloured:", int(inner.sum()), "mean luma before %.0f after %.0f" % (
    ref, (np.clip(out, 0, 255) @ np.array([0.299, 0.587, 0.114]))[inner].mean()))
