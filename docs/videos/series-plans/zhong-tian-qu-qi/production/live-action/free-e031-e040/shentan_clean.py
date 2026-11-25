"""shentan_clean.py SRC DST KIND : the deep-pond masters with the things that must not be drawn painted out (arc 4, 2026-11-19,
e033 r2 independent review 必改 5 and 建議 10). KIND is "wheel" (set-shentan-l2 -> set-shentan-l3) or "gongdi"
(set-shentan-gongdi-l1 -> set-shentan-gongdi-l2); both pictures share the camera, so the boxes are the same.
(a) KIND wheel only (the half-built site's rope hangs elsewhere, with a ladder of lashings, and nobody pulls a rope there).
    The rope of the low left frame in set-shentan-l2 (the edit moved the frame a little left of set-shentan-l1's): from the
    lashing on the left post (x 220, y 292) down across the bank to the left edge (x 0, y 462), its shadow under the lower
    half, and the short sagging piece across to the frame (x 145-204, y 397). In the
    close shots of the sluice (e033 s29, s31-s33, s36, s37) Carpenter Shi pulls the sluice rope right there, and a second rope
    in the first frame joins his (e032 fix2: two long things drawn as one).
(b) The small electricity pylon with its wires on the far left horizon (x 0-63, y 290-310: it stands further left in the half-built site): Song dynasty (rule 13).
(c) The thin upright poles on the horizon right of the wheel (x 830-1312, y 312-328, above the far land, every pixel darker than the median of its
    row by 12 or more; the frame posts, dark above the band too, excluded): they could be redrawn as telegraph poles (e031 pick notes; rule 13).
Each mask is filled by harmonic (Laplace) diffusion from its border (clean_shangyou_box.py's way); the rope's mask then gets
the bank's grain back from outside it (the steep part from the left, the level part from above: a sideways copy along the
level part put the rope back)."""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, dst, kind = sys.argv[1], sys.argv[2], sys.argv[3]
assert kind in ("wheel", "gongdi"), kind
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = a.shape
assert (W, H) == (1312, 736), (W, H)


def poly_mask(lines):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    for pts, w in lines:
        d.line(pts, fill=255, width=w, joint="curve")
        for x, y in (pts[0], pts[-1]):
            d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=255)
    return np.asarray(im) > 0


def fill(img, m, grain_dx=0, iters=2500):
    ys, xs = np.where(m)
    y0, y1, x0, x1 = max(ys.min() - 3, 0), min(ys.max() + 4, H), max(xs.min() - 3, 0), min(xs.max() + 4, W)
    sub, mm = img[y0:y1, x0:x1].copy(), m[y0:y1, x0:x1]
    # start from the mean of the border so the diffusion converges fast
    border = ndi.binary_dilation(mm, iterations=2) & ~mm
    sub[mm] = sub[border].mean(0)
    for _ in range(iters):
        avg = (np.roll(sub, 1, 0) + np.roll(sub, -1, 0) + np.roll(sub, 1, 1) + np.roll(sub, -1, 1)) / 4
        sub[mm] = avg[mm]
    if grain_dx:
        hp = img - ndi.gaussian_filter(img, (2, 2, 0))
        sh = np.roll(hp, grain_dx, 1)[y0:y1, x0:x1]
        sub[mm] += 0.5 * sh[mm]
    out = img.copy()
    out[y0:y1, x0:x1] = sub
    return out


out = a.copy()


def clean_rope(out):
    """(a) the rope, its lower shadow, the sagging piece (polyline points from the picture; widths cover the rope and its edge)."""
    rope = poly_mask([
        ([(220, 292), (200, 320), (180, 348), (160, 376), (145, 397), (130, 415), (117, 430), (100, 441), (75, 450), (40, 456),
          (0, 462)], 11),
        ([(120, 433), (100, 445), (75, 455), (40, 461), (0, 467)], 9),      # its shadow on the bank under the lower half
        ([(145, 397), (180, 397), (204, 397)], 9),                          # the short piece across to the frame
    ])
    # keep the post itself and the lashing on it (x 203-222 is the post)
    post = np.zeros((H, W), bool)
    post[280:470, 203:223] = True
    rope &= ~post
    # inside that corridor only the rope itself: paler than the bank around it (a 25 px median), grown 3 px for its soft edge
    Lr = out @ np.array([0.299, 0.587, 0.114])
    corr = ndi.binary_dilation(rope, iterations=6) & ~post
    med = ndi.median_filter(Lr, size=25)
    rope = (corr & (Lr > med + 8)) | rope
    rope = ndi.binary_dilation(rope, iterations=3) & ~post
    filled = fill(out, rope)
    # the bank's grain back at full strength from outside the mask: the upper, steep part of the rope takes it from 22 px to its
    # left (the furrows run level, so they line up), the lower, nearly level part from 18 px above (a sideways copy along it
    # would copy the rope); where that spot is masked too, twice or three times as far
    hp = out - ndi.gaussian_filter(out, (3, 3, 0))
    ys, xs = np.where(rope)
    for y, x in zip(ys, xs):
        dy, dx = (0, -22) if y < 425 else (-18, 0)
        for k in (1, 2, 3):
            sy, sx = y + k * dy, x + k * dx
            if 0 <= sy < H and 0 <= sx < W and not rope[sy, sx]:
                filled[y, x] += hp[sy, sx]
                break
    return filled, rope


rope = np.zeros((H, W), bool)
if kind == "wheel":
    out, rope = clean_rope(out)
# (b) the pylon on the far left horizon
pyl = np.zeros((H, W), bool)
pyl[290:311, 0:64] = True
out = fill(out, pyl)
# (c) the thin poles on the horizon right of the wheel: darker than the sky just above them, frame posts left alone
L = out @ np.array([0.299, 0.587, 0.114])
band = np.zeros((H, W), bool)
band[312:329, 830:W] = True
sky = np.median(L[296:310, :], axis=0)[None, :]
rowsky = np.median(L[:, 830:], axis=1)[:, None]  # the haze darkens the sky toward the horizon: compare along each row
poles = band & (L < rowsky - 12)
# the tall right frame's posts (they stand where the edit put them): every column dark already above the band, 3 px each side
post_cols = ndi.binary_dilation(L[298:308, :].mean(0) < sky[0] - 20, iterations=3)
poles[:, post_cols] = False
# only the thin uprights, not the far land along the horizon: a pole pixel needs one above it too
poles &= np.roll(poles, 1, 0) | np.roll(poles, -1, 0)
poles = ndi.binary_dilation(poles, structure=np.ones((3, 3), bool)) & band
poles[:, post_cols] = False
if poles.any():
    lab, n = ndi.label(poles)
    for k in range(1, n + 1):
        ys, xs = np.where(lab == k)
        if xs.max() - xs.min() > 5:   # a thin upright only; a wider dark patch is the far land, left as it is
            poles[lab == k] = False
            continue
        out = fill(out, lab == k, iters=600)
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst)
print(kind, "rope px", int(rope.sum()), "pylon px", int(pyl.sum()), "pole px", int(poles.sum()))
