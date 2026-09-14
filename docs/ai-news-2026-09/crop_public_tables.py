"""Locate table pixels in normal full-page captures, preserving unobscured evidence."""
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
items = json.loads((HERE / "manifest.json").read_text(encoding="utf8"))
results = []
for locale in ["zh-TW", "en", "ja", "ko", "zh-CN"]:
    for item in items:
        stem = f'mobile-{locale}-{item["slug"]}'
        full = Image.open(HERE / "browser" / f"{stem}.png").convert("RGB")
        table = Image.open(HERE / "browser" / f"{stem}-table.png").convert("RGB")
        raw, stride = full.tobytes(), full.width * 3
        samples = []
        for y in range(table.height // 5, table.height * 4 // 5, 17):
            row = table.crop((0, y, table.width, y + 1)).tobytes()
            colors = len(set(row[i:i + 3] for i in range(0, len(row), 3)))
            if colors > 25:
                samples.append((colors, y, row))
        samples.sort(reverse=True)
        match = None
        for _, y, row in samples[:20]:
            pos = raw.find(row)
            if pos < 0:
                continue
            x, top = (pos % stride) // 3, pos // stride - y
            if x < 0 or top < 0 or x + table.width > full.width or top + table.height > full.height:
                continue
            score = sum(
                raw[(top + sy) * stride + x * 3:(top + sy) * stride + (x + table.width) * 3] == sr
                for _, sy, sr in samples
            ) / len(samples)
            if score >= 0.65:
                match = (x, top, score)
                break
        if match is None:
            raise RuntimeError(f"Cannot confidently locate table: {stem}")
        x, top, score = match
        rect = (x, top, x + table.width, top + table.height)
        full.crop(rect).save(HERE / "browser" / f"{stem}-table-clean.png")
        results.append({"source": f"browser/{stem}.png", "rectangle": rect,
                        "matching_text_scanlines": score, "output": f"browser/{stem}-table-clean.png"})
(HERE / "table-crop-verification.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf8")
print(f"Cropped {len(results)} tables from unmodified public full-page screenshots")
