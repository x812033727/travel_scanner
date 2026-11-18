"""citang_huang.py SRC DST : set-citang-huang-l1 (arc 4, 2026-11-18, e032 r2) from the round-1 winner set-citang-l1 (seed 37038).
e032's third scene is the ancestral hall at DUSK (script: 門外天邊橘紅, 堂內燭光); the winner's doorway shows a daylit inner
porch, which a d1 draft would read as midday. Two free changes, both outside the candle-lit altar:
(a) the doorway zone (the same zone as citang_ye.py: x < 525 feathered over 40 px, weight smoothstep(45, 130) on the 5 px
    max-filtered luminance, at least 0.85 in the opening x 230-372, y 40-640) is pulled toward a dim warm dusk tone
    L * 0.62 * (1.30, 0.80, 0.48): the light through the lattice and the porch beyond read as the last orange evening light;
(b) the dark main beam along the top of the back wall (lower edge y = 160 - 0.42 (x - 700), about 80 px thick, x 560-1312)
    carries thin black crack strokes that could grow into writing (rule 33; the main beam is the subject of e032 s32). Each
    column is sheared so the beam runs level, a 9 x 31 median (across x along the beam) gives its plain wood, and the pixels darker
    than that by 6 or more (the wood is L about 20, the strokes 4-12; only where that plain wood is darker than 34, so the
    lit wall under the beam's lower edge is never pulled in) (dilated 2 px, feathered 1.2 px) inside the beam band are replaced by it."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = a.shape
xs = np.arange(W)[None, :].repeat(H, 0)
ys = np.arange(H)[:, None].repeat(W, 1)

# (b) the beam's crack strokes
SLOPE, X0, Y0, THICK = 0.42, 700, 160, 80
shift = np.round(SLOPE * (np.arange(W) - X0)).astype(int)          # y_low(x) = Y0 - shift
PAD = 320
sheared = np.zeros((H + 2 * PAD, W, 3))
for x in range(W):
    s = PAD + shift[x]
    sheared[s:s + H, x] = a[:, x]
bg = np.stack([ndi.median_filter(sheared[..., c], size=(9, 31), mode="nearest") for c in range(3)], -1)
bg_back = np.zeros_like(a)
for x in range(W):
    s = PAD + shift[x]
    bg_back[:, x] = bg[s:s + H, x]
ylow = Y0 - SLOPE * (xs - X0)
band = (ys >= ylow - THICK - 4) & (ys <= ylow + 2) & (xs >= 560)
Lw = a @ np.array([0.299, 0.587, 0.114])
Lb = bg_back @ np.array([0.299, 0.587, 0.114])
wood = band & (Lb < 34)                        # the beam's own dark wood, not the lit wall along its lower edge
crack = wood & (Lb - Lw >= 6)
crack = ndi.binary_dilation(crack, iterations=2) & wood
m = np.clip(ndi.gaussian_filter(crack.astype(np.float64), 1.2) * 1.6, 0, 1)
a = a * (1 - m[..., None]) + bg_back * m[..., None]

# (a) the doorway at dusk
L = a @ np.array([0.299, 0.587, 0.114])
Ld = ndi.gaussian_filter(ndi.maximum_filter(L, size=5), 1.0)
t = np.clip((Ld - 45) / (130 - 45), 0, 1)
w = t * t * (3 - 2 * t)
zone = np.clip((565 - xs) / 40.0, 0, 1)
opening = (xs >= 230) & (xs < 372) & (ys >= 40) & (ys < 640)
w = np.where(opening, np.maximum(w, 0.85), w) * zone
dusk = L[..., None] * 0.62 * np.array([1.30, 0.80, 0.48])
out = a * (1 - w[..., None]) + dusk * w[..., None]
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst)
print("crack pixels", int(crack.sum()))
