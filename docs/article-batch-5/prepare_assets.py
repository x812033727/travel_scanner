"""Optimize the original generated images without changing their visual content."""
from pathlib import Path
import hashlib
import json
import argparse
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
rows = json.loads((HERE / 'image-sources.json').read_text(encoding='utf-8'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir', type=Path, required=True, help='Directory containing the original ImageGen PNG files')
args=parser.parse_args()
provenance = []
for row in rows:
    source = args.source_dir / row['original_file']
    output = ROOT / 'apps/web/public/guides' / row['slug'] / 'hero.jpg'
    with Image.open(source) as original:
        photo = ImageOps.fit(original.convert('RGB'), (1600, 900), method=Image.Resampling.LANCZOS)
        for quality in range(88, 19, -3):
            photo.save(output, quality=quality, optimize=True, progressive=True)
            if output.stat().st_size <= 200_000:
                break
    assert output.stat().st_size <= 200_000
    provenance.append({'slug': row['slug'], 'origin': 'OpenAI built-in ImageGen, generated for this batch',
        'original_file': source.name, 'original_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'asset': str(output.relative_to(ROOT)).replace('\\', '/'),
        'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'bytes': output.stat().st_size,
        'width':1600, 'height':900, 'usage_note':'Original AI-generated editorial illustration; not a documentary photograph. No third-party stock image used.'})
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
for name, group in [('travel', rows[:15]), ('life', rows[15:])]:
    sheet = Image.new('RGB', (1600, 690), '#f4f0e5')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(group):
        x, y = (i % 5) * 320, (i // 5) * 230
        with Image.open(ROOT / 'apps/web/public/guides' / row['slug'] / 'hero.jpg') as photo:
            sheet.paste(photo.resize((312, 175)), (x+4, y+4))
        words = row['slug'].split('-')
        lines = ['']
        for word in words:
            if len(lines[-1])+len(word)>33: lines.append('')
            lines[-1] += ('-' if lines[-1] else '') + word
        draw.text((x+5, y+184), '\n'.join(lines), fill='#154e50', font=font)
    sheet.save(HERE / f'{name}-contact-sheet.jpg', quality=90)
(HERE / 'image-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Prepared {len(rows)} unique web images, largest {max(p["bytes"] for p in provenance):,} bytes')
