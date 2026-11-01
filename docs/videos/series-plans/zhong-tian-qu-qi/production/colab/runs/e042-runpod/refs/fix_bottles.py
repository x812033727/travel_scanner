"""Replace the row of bottles on the inn counter with a copy of one of the set's own sealed jars; the rest of the room is untouched."""
import os
from PIL import Image, ImageDraw, ImageFilter
A = os.path.dirname(os.path.abspath(__file__))
base = Image.open(f"{A}/set-zhou-kezhan-fixed.png").convert("RGB")
orig = Image.open(f"{A}/refs-dh/set-zhou-kezhan-t1.png").convert("RGB")
jar = orig.crop((1188, 350, 1284, 468)).resize((96, 118), Image.LANCZOS)
mask = Image.new("L", (96, 118), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((5, 18, 91, 116), fill=255)
draw.polygon([(16, 30), (30, 3), (68, 3), (82, 30)], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(1.5))
base.paste(jar, (850, 338), mask)
base.save(f"{A}/set-zhou-kezhan-fixed2.png")
both = Image.new("RGB", (1200, 400))
both.paste(orig.crop((760, 300, 1060, 500)).resize((600, 400)), (0, 0))
both.paste(base.crop((760, 300, 1060, 500)).resize((600, 400)), (600, 0))
both.save(f"{A}/p6.jpg", quality=90)
