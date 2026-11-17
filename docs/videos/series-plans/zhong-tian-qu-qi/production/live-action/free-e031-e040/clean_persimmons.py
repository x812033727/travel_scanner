"""clean_persimmons.py SRC DST : paint every orange persimmon out of set-xujia-yuan-ye-nolantern-l1 (arc 4, 2026-11-17).
Find: orange dots by local contrast of (R-B) against its 21 px median (so the warm-lit walls, the gate eave and the
trunk's warm rim are left alone) inside the sky and tree crown (y < 0.36 H, less the lit gate eave x 520-745 y 205-300),
the thatch (x < 530, y 60-262) and the gate-roof ridge; inside the trunk's lit rim band (x 738-775, y 118-200) only
pixels with R > 85 count (the rim is R <= 75, a fruit's core 110-156); long thin blobs (h > 18 and h > 3 w) are skipped.
Fill: each found pixel grown 5 px, filled by harmonic (Laplace) diffusion from the unmasked pixels around it (so a sky
gradient or a crossing twig runs on smoothly instead of leaving flat patches), mask feathered 1.2 px.
Pass 1 threshold 22, pass 2 on the result threshold 14, pass 3 the dim dark-red fruit rims left in the crown
(R - G > 18 and R > 28, y < 240, x > 560, outside the trunk band)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
img = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = img.shape
region = np.zeros((H, W), bool)
region[: int(0.36 * H), :] = True
region[205:300, 520:745] = False
region[60:262, 0:530] = True
region[190:222, 600:645] = True     # the dot on the gate-roof ridge
band = np.zeros((H, W), bool)
band[118:200, 738:775] = True


def find(a, thr):
    r, b = a[..., 0], a[..., 2]
    d = r - b
    med = ndi.median_filter(d, size=21)
    m = (d - med > thr) & (r > 40) & (d > 12) & region
    core = m & band & (r > 85)
    m = (m & ~band) | ndi.binary_dilation(core, iterations=2) & m
    lab, n = ndi.label(m)
    keep = np.zeros_like(m)
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if h > 18 and h > 3 * w:
            continue
        keep[sl] |= lab[sl] == i
    return keep


GROW = 5
reg3 = np.zeros((H, W), bool)
reg3[:240, 560:] = True
reg3[190:300, 520:745] = False
reg3[190:222, 600:645] = True
reg3 &= ~band


def find_dark(a):
    r, g = a[..., 0], a[..., 1]
    return (r - g > 18) & (r > 28) & reg3


def fill(a, m):
    m = ndi.binary_dilation(m, iterations=GROW)
    out = a.copy()
    lab, n = ndi.label(m)
    ring_all = ndi.binary_dilation(m, iterations=2) & ~m
    for i, sl in enumerate(ndi.find_objects(lab), 1):  # start each hole at the median of its own ring
        y0, y1 = max(sl[0].start - 2, 0), min(sl[0].stop + 2, H)
        x0, x1 = max(sl[1].start - 2, 0), min(sl[1].stop + 2, W)
        hole = lab[y0:y1, x0:x1] == i
        ring = ndi.binary_dilation(hole, iterations=2) & ring_all[y0:y1, x0:x1]
        out[y0:y1, x0:x1][hole] = np.median(out[y0:y1, x0:x1][ring], axis=0)
    k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]])
    ys, xs = np.nonzero(ndi.binary_dilation(m, iterations=1))
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    patch, hole = out[y0:y1, x0:x1], m[y0:y1, x0:x1]
    for _ in range(400):  # harmonic fill of all holes at once, the unmasked pixels fixed
        for c in range(3):
            sm = ndi.convolve(patch[..., c], k, mode="nearest")
            patch[..., c][hole] = sm[hole]
    alpha = ndi.gaussian_filter(m.astype(np.float64), 1.2)
    alpha = np.maximum(alpha, m * 1.0)[..., None]
    return a * (1 - alpha) + out * alpha, m


a = img
total = np.zeros((H, W), bool)
for thr in (22, 14, None):
    m = find(a, thr) if thr else find_dark(a)
    print(f"pass thr={thr}: {ndi.label(m)[1]} blobs, {m.sum()} px")
    a, grown = fill(a, m)
    total |= grown
Image.fromarray(np.clip(np.rint(a), 0, 255).astype(np.uint8)).save(dst)
