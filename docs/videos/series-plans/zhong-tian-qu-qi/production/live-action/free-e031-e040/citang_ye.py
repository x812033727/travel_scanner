"""citang_ye.py SRC DST : set-citang-ye-l1 (arc 4, 2026-11-17) from the round-1 winner set-citang-l1 (seed 37038).
Bible: only the doorway on the left goes to night; the candle-lit hall is left alone. In the winner the left third is
the pair of lattice door leaves (x 0-230 and 370-515) with daylight shining through the lattice, and the opening
between them (x 230-370, y 40-640) looks through to a daylit inner court. Inside the door zone (x < 525, feathered
over 40 px to the right) every pixel is pulled toward a cold night tone: luminance L is weighted by
w = smoothstep(L', 45, 130) on L' = L max-filtered 5 px, blurred 1 px (so the dark wooden frames stay as they are and the daylight goes), and in the opening
itself w is at least 0.85. The night tone is L * 0.20 times (0.70, 0.85, 1.35) per channel (deep blue grey)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = a.shape
L = a @ np.array([0.299, 0.587, 0.114])
Ld = ndi.gaussian_filter(ndi.maximum_filter(L, size=5), 1.0)   # so the rims of each lattice hole go too
t = np.clip((Ld - 45) / (130 - 45), 0, 1)
w = t * t * (3 - 2 * t)
xs = np.arange(W)[None, :].repeat(H, 0)
ys = np.arange(H)[:, None].repeat(W, 1)
zone = np.clip((565 - xs) / 40.0, 0, 1)            # 1 for x <= 525, 0 for x >= 565
opening = (xs >= 230) & (xs < 372) & (ys >= 40) & (ys < 640)
w = np.where(opening, np.maximum(w, 0.85), w) * zone
night = L[..., None] * 0.20 * np.array([0.70, 0.85, 1.35])
out = a * (1 - w[..., None]) + night * w[..., None]
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst)
