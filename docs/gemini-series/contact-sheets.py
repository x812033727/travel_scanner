"""Create a labelled visual QA contact sheet for every cover and teaching diagram."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
series = json.loads((ROOT / "apps/web/lib/guide-series.json").read_text(encoding="utf8"))
entries = [(0, series["hubSlug"])] + [(a["number"], a["slug"]) for a in series["articles"]]
font = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 22)
destination = HERE / "visual-review"
destination.mkdir(exist_ok=True)
for start in range(0, len(entries), 6):
    sheet = Image.new("RGB", (1200, 2130), "#FFFFFF")
    draw = ImageDraw.Draw(sheet)
    for index, (number, slug) in enumerate(entries[start:start+6]):
        x, y = (index % 2) * 600, (index // 2) * 710
        draw.text((x + 12, y + 5), f"{number:02} · {slug[:42]}", fill="#123D38", font=font)
        for image_index, name in enumerate(("hero", "diagram-1")):
            with Image.open(HERE / "renders" / slug / f"{name}.png") as picture:
                sheet.paste(picture.resize((600, 337), Image.Resampling.LANCZOS), (x, y + 35 + image_index * 337))
    sheet.save(destination / f"contact-{start//6+1:02}.jpg", quality=94)
print(f"{(len(entries)+5)//6} contact sheets; {len(entries)*2} images")
