"""Contact sheet: each slug's hero.jpg and rendered diagram-1.svg side by side, for review.

Usage (from apps/api): .venv/bin/python ../../docs/ai-terms-series/batch-02/sheet.py OUT.png SLUG...
"""

import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from app.guides.pack_ingest import render_svg

PUBLIC = Path("../web/public/guides")
W, H = 800, 450

out, slugs = Path(sys.argv[1]), sys.argv[2:]
sheet = Image.new("RGB", (W * 2 + 30, (H + 40) * len(slugs) + 10), "white")
draw = ImageDraw.Draw(sheet)
with tempfile.TemporaryDirectory() as tmp:
    for row, slug in enumerate(slugs):
        y = row * (H + 40) + 10
        draw.text((10, y), slug, fill="black")
        hero = Image.open(PUBLIC / slug / "hero.jpg").convert("RGB").resize((W, H))
        png = Path(tmp) / f"{slug}.png"
        render_svg(PUBLIC / slug / "diagram-1.svg", png)
        diagram = Image.open(png).convert("RGB").resize((W, H))
        sheet.paste(hero, (10, y + 20))
        sheet.paste(diagram, (W + 20, y + 20))
sheet.save(out)
