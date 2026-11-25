"""e037 independent review 建議 1 (coordinator 2026-11-23: do it): a night copy of the owner's hair reference
refs-live/tangxiaotang-back-shuangji-e929-w3.png (two round buns from behind, blue daytime sky and two tiled houses behind her),
so the night back shots of Tang Xiaotang do not pull daylight or the houses into a night alley or yard. The original stays
untouched (the owner chose it, 2026-11-22). Free and deterministic:
1. the blue sky (blue more than 40 above red) becomes a dark night blue, feathered over the mask edge (a 3 px box blur of the mask);
2. in the two lower corners only, where the houses are, everything brighter than the dark hair (luminance > 70) is blurred
   (a 9 px box) and pressed down, so only the dark shape of a roof line is left;
3. the whole picture is graded to cool moonlight: x 0.62 brightness, a blue lift, a little less saturation; the black hair
   and the pink ribbons keep their shapes and their colour (darker).
Usage: python3 -I tangxiaotang_back_ye.py tangxiaotang-back-shuangji-e929-w3.png OUT.png
"""
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter

a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float64)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = a.mean(axis=2)
sky = ((b - r) > 40).astype(np.float64)
sky = uniform_filter(sky, size=3)
night = np.array([18.0, 26.0, 58.0])
out = a * (1 - sky[..., None]) + night * sky[..., None]
# the houses and trees (not the hair, not the ribbons: the ribbons are pink, r well above b)
h, w = lum.shape
yy, xx = np.mgrid[0:h, 0:w]
corner = (yy > 0.55 * h) & ((xx < 0.24 * w) | (xx > 0.80 * w))  # the two houses sit in the lower corners
bg = ((lum > 70) & ~((r - b) > 40) & corner).astype(np.float64)
bg = uniform_filter(bg, size=5) * (1 - sky)
blur = np.stack([uniform_filter(out[..., c], size=9) for c in range(3)], axis=2)
out = out * (1 - bg[..., None]) + (blur * 0.45) * bg[..., None]
# cool moonlight grade
grey = out.mean(axis=2, keepdims=True)
out = grey + (out - grey) * 0.85
out = out * 0.62 + np.array([0.0, 4.0, 14.0])
Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8)).save(sys.argv[2], optimize=False)
