"""Make numbered visual-review sheets from local rendered assets."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
catalogue = json.loads((HERE / 'catalogue.json').read_text(encoding='utf-8'))
items = catalogue['terms'] + [{'id': 82, 'slug': 'ai-terms-index'}]
out = HERE / 'qa'
out.mkdir(exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
report = {}
for kind in ['hero', 'diagram-1']:
    available = [(t, HERE / 'renders' / f"{t['slug']}-{kind}.png") for t in items]
    available = [(t, p) for t, p in available if p.is_file()]
    pages = []
    for start in range(0, len(available), 4):
        canvas = Image.new('RGB', (1600, 972), '#FFFFFF')
        draw = ImageDraw.Draw(canvas)
        names = []
        for n, (term, file) in enumerate(available[start:start+4]):
            x, y = (n % 2) * 800, (n // 2) * 486
            with Image.open(file) as picture:
                canvas.paste(picture.convert('RGB').resize((800, 450), Image.Resampling.LANCZOS), (x, y + 32))
            draw.text((x + 12, y + 8), f"{term['id']:02d} {term['slug']} / {kind}", font=font, fill='#102A2B')
            names.append(term['slug'])
        page = f'{kind}-{start//4+1:02d}.jpg'
        canvas.save(out / page, quality=90, optimize=True)
        pages.append({'file': page, 'slugs': names})
    report[kind] = pages
(out / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({kind: len(pages) for kind, pages in report.items()}))
