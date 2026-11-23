#!/usr/bin/env python3
"""第 8 集 c26、c28 的門縫遮罩（script.md〈剪接〉）：兩邊是近黑的深紅褐門板，中間一道直縫，寬 22%、中心在 47%（實拍的小滿在 47%，不是分鏡寫的 62%），邊緣羽化，
門板上很淡的直木紋與暗角。輸出 RGBA PNG，用 ffmpeg overlay 疊在片段上。  python3 door_mask.py out.png [W H [center]]"""
import sys
import numpy as np
from PIL import Image

out = sys.argv[1]
W, H = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1312, 736)
rng = np.random.default_rng(8)
x = np.arange(W)[None, :].repeat(H, 0).astype(float)
c = float(sys.argv[4]) * W if len(sys.argv) > 4 else 0.47 * W
half, feather = 0.11 * W, 40 * W / 1920
d = np.abs(x - c) - half                      # <0 inside the gap
alpha = np.clip(d / feather + 0.5, 0, 1)      # soft edge
grain = rng.normal(0, 1, W).cumsum(); grain = (grain - grain.mean()) / (grain.std() + 1e-6)
wood = 1 + 0.06 * np.tanh(grain)[None, :] + 0.03 * rng.normal(0, 1, (H, W))
yy = np.linspace(-1, 1, H)[:, None]
shade = (1 - 0.35 * yy ** 2) * (1 - 0.25 * np.clip(-d / W * 0 + np.abs(x - c) / W, 0, 1))
base = np.array([34, 16, 12], float)          # near-black dark red-brown
rgb = np.clip(base[None, None, :] * (wood * shade)[..., None], 0, 255)
img = np.dstack([rgb, alpha[..., None] * 255]).astype(np.uint8)
Image.fromarray(img, "RGBA").save(out)
print(out, W, H)
