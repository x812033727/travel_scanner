"""Free prop picture: one sheet of handmade white paper backlit by the noon sun, a slender willow-leaf watermark in the middle.
python3 -I liuye_w2.py OUT.png   (deterministic, seed 2929)"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 1312, 736
rng = np.random.default_rng(2929)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
# base warm paper colour with the sun glowing through from behind, brightest a little above and right of the middle
d = np.sqrt(((xx - 760) / W) ** 2 + ((yy - 250) / H) ** 2)
glow = np.clip(1.0 - d * 1.15, 0, 1) ** 1.6
base = np.stack([226 + 22 * glow, 218 + 26 * glow, 196 + 32 * glow], -1)
# low-frequency cloudiness of the pulp (+-5%)
def lowfreq(scale, amp):
    small = rng.normal(0, 1, (H // scale + 2, W // scale + 2)).astype(np.float32)
    im = Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-6) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    a = np.asarray(im, np.float32) / 255 - 0.5
    return a * amp
cloud = lowfreq(48, 0.07) + lowfreq(16, 0.03)
img = base * (1 + cloud[..., None])
# fine fibres: many short thin slightly curved strands, a little darker or lighter
fib = Image.new("L", (W, H), 128)
dr = ImageDraw.Draw(fib)
for _ in range(700):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    ang = rng.uniform(0, math.pi); ln = rng.uniform(8, 38); bend = rng.uniform(-0.012, 0.012)
    pts = []
    for t in np.linspace(0, 1, 6):
        a = ang + bend * t * ln
        pts.append((x + math.cos(a) * ln * t, y + math.sin(a) * ln * t))
    dr.line(pts, fill=int(128 + rng.choice([-1, 1]) * rng.uniform(6, 14)), width=1)
fib = np.asarray(fib.filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 128 - 1
img = img * (1 + fib[..., None] * 0.35)
# the willow leaf: long, narrow, pointed at both ends, about six times longer than wide, a gentle curve, short stalk
cx, cy, L, Wd, tilt = 656, 372, 540, 84, math.radians(-14)
def leaf_pt(t, side):
    # t in [0,1] along the leaf; half-width profile pointed at both ends, widest a little below the middle
    w = Wd / 2 * (math.sin(math.pi * t) ** 1.15)
    s = (t - 0.5) * L
    curve = 9 * math.sin(math.pi * t)
    px, py = s, curve + side * w
    return (cx + px * math.cos(tilt) - py * math.sin(tilt), cy + px * math.sin(tilt) + py * math.cos(tilt))
N = 160
poly = [leaf_pt(i / N, -1) for i in range(N + 1)] + [leaf_pt(1 - i / N, 1) for i in range(N + 1)]
mask = Image.new("L", (W, H), 0); md = ImageDraw.Draw(mask)
md.polygon(poly, fill=255)
mid = [leaf_pt(i / N, 0) for i in range(N + 1)]
stalk_end = (mid[0][0] - 30 * math.cos(tilt), mid[0][1] - 30 * math.sin(tilt) + 6)
lines = Image.new("L", (W, H), 0); ld = ImageDraw.Draw(lines)
ld.line(mid, fill=200, width=3)
ld.line([mid[0], stalk_end], fill=200, width=3)
for k in range(1, 15):
    t = k / 15
    for side in (-1, 1):
        a = leaf_pt(t, 0); b = leaf_pt(min(1, t + 0.06), side * 0.85)
        ld.line([a, b], fill=110, width=1)
mask = np.asarray(mask.filter(ImageFilter.GaussianBlur(2.2)), np.float32) / 255
edge = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
lines = np.asarray(lines.filter(ImageFilter.GaussianBlur(0.9)), np.float32) / 255 * mask
lift = mask * 0.42 + lines * 0.20 + np.clip(edge * 0.9, 0, 0.10)
ring = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)), np.float32) / 255 - mask
img = img * (1 - np.clip(ring, 0, 1)[..., None] * 0.22)  # the thicker pulp piled along the rim of the leaf reads a little darker
img = img + (255 - img) * np.clip(lift, 0, 0.6)[..., None]
img = np.clip(img, 0, 255).astype(np.uint8)
Image.fromarray(img).filter(ImageFilter.GaussianBlur(0.4)).save(sys.argv[1])
