"""e037 independent review 必改 7 (2026-11-23): the stars out of the dawn grade. Only in the sky above the tree line (y < 330 at
1312 x 736): every pixel whose brightness is more than 15 above the median of its 9 x 9 neighbourhood is replaced by that median,
the mask grown by 1 px. Free and deterministic. Usage: python3 -I destar_e937.py IN.png OUT.png"""
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import median_filter, binary_dilation

a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float64)
lum = a.mean(axis=2)
med = np.stack([median_filter(a[..., c], size=9, mode="nearest") for c in range(3)], axis=2)
mask = (lum - med.mean(axis=2)) > 15
mask[330:] = False
mask = binary_dilation(mask, iterations=1)
mask[330:] = False
out = np.where(mask[..., None], med, a)
Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8)).save(sys.argv[2], optimize=False)
