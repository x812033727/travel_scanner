"""Assemble actual public-browser screenshots for visual review; never changes site assets."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ITEMS = json.loads((HERE / 'manifest.json').read_text(encoding='utf8'))
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
created = []
for viewport in ['desktop', 'mobile']:
    for locale in ['zh-TW', 'en', 'ja', 'ko', 'zh-CN']:
        files = [HERE / 'browser' / f'{viewport}-{locale}-{item["slug"]}-top.png' for item in ITEMS]
        if not all(p.exists() for p in files):
            continue
        width = 330 if viewport == 'desktop' else 300
        height = 360 if viewport == 'desktop' else 650
        sheet = Image.new('RGB', (5 * (width + 12) + 12, 2 * (height + 42) + 12), '#e6e6e6')
        draw = ImageDraw.Draw(sheet)
        for i, p in enumerate(files):
            frame = Image.open(p).convert('RGB')
            if viewport == 'desktop':
                frame = frame.crop((280, 88, 1085, 900))
            frame.thumbnail((width, height), Image.Resampling.LANCZOS)
            x, y = 12 + (i % 5) * (width + 12), 12 + (i // 5) * (height + 42)
            draw.text((x, y), f'{i + 1:02d} | {locale} | {ITEMS[i]["event_date"]}', fill='#222', font=FONT)
            sheet.paste(frame, (x, y + 28))
        target = HERE / f'public-layout-{viewport}-{locale}.jpg'
        sheet.save(target, quality=90, optimize=True)
        created.append(target.name)

for locale in ['zh-TW', 'en', 'ja', 'ko', 'zh-CN']:
    for group in range(2):
        items = ITEMS[group * 5:(group + 1) * 5]
        files = [HERE / 'browser' / f'mobile-{locale}-{item["slug"]}-table-clean.png' for item in items]
        if not all(p.exists() for p in files):
            continue
        frames = []
        for p in files:
            frame = Image.open(p).convert('RGB')
            frame.thumbnail((320, 1800), Image.Resampling.LANCZOS)
            frames.append(frame)
        sheet = Image.new('RGB', (1672, max(f.height for f in frames) + 54), '#e6e6e6')
        draw = ImageDraw.Draw(sheet)
        for i, frame in enumerate(frames):
            x = 12 + i * 332
            draw.text((x, 10), f'{group * 5 + i + 1:02d} | {locale} | table', fill='#222', font=FONT)
            sheet.paste(frame, (x, 38))
        target = HERE / f'public-tables-mobile-{locale}-{group + 1}.jpg'
        sheet.save(target, quality=92, optimize=True)
        created.append(target.name)
print(json.dumps(created))
