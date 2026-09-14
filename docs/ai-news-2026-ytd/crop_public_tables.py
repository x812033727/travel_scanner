"""Locate table pixels in normal full-page captures, preserving unobscured evidence."""
import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
items = json.loads((HERE / "manifest.json").read_text(encoding="utf8"))
results = []
refresh_scrolled = '--refresh-scrolled' in sys.argv
previous = json.loads((HERE / 'table-crop-verification.json').read_text(encoding='utf8')) if refresh_scrolled else []
for locale in ["zh-TW", "en", "ja", "ko", "zh-CN"]:
    for item in items:
        stem = f'mobile-{locale}-{item["slug"]}'
        if '--partial' in sys.argv and not all((HERE / 'browser' / f'{stem}{suffix}.png').exists() for suffix in ['', '-table']):
            continue
        scroll_receipt = HERE / 'browser' / f'{stem}-scroll.json'
        if refresh_scrolled and not scroll_receipt.exists():
            # Preserve the already verified, unchanged normal-page crops.
            results.append(next(r for r in previous if r['output'] == f'browser/{stem}-table-clean.png'))
            continue
        full = Image.open(HERE / "browser" / f"{stem}.png").convert("RGB")
        table = Image.open(HERE / "browser" / f"{stem}-table.png").convert("RGB")
        if scroll_receipt.exists():
            evidence = json.loads(scroll_receipt.read_text(encoding='utf8'))
            assert evidence['native_horizontal_scroll_verified'] is True
            left, right = evidence['captures']
            dpr = left['dpr']
            width, height = round(left['width'] * dpr), round(left['height'] * dpr)
            clean = Image.new('RGB', (width, height), (247, 241, 230))
            for capture in [left, right]:
                source = Image.open(HERE / capture['source']).convert('RGB')
                x, y = round(capture['left'] * dpr), round(capture['top'] * dpr)
                visible = round(capture['visibleWidth'] * dpr)
                offset = round(capture['scrollLeft'] * dpr)
                clean.paste(source.crop((x, y, x + visible, y + height)), (offset, 0))
            clean.save(HERE / 'browser' / f'{stem}-table-clean.png')
            results.append({'source': [c['source'] for c in evidence['captures']],
                            'method': 'Two normal full-page captures at the native left and right scroll positions, stitched at the measured scroll offset. No style or content changes.',
                            'native_horizontal_scroll_verified': True,
                            'captures': evidence['captures'],
                            'scroll_receipt': f'browser/{stem}-scroll.json',
                            'output': f'browser/{stem}-table-clean.png'})
            continue
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
            matching_rows = [sy for _, sy, sr in samples
                             if raw[(top + sy) * stride + x * 3:(top + sy) * stride + (x + table.width) * 3] == sr]
            score = len(matching_rows) / len(samples)
            span = max(matching_rows) - min(matching_rows) if matching_rows else 0
            # Locator captures can include sticky navigation over part of a tall
            # table. Six distinct exact text scanlines spanning 300 pixels still
            # identify its position in the unobscured full-page source.
            if score >= 0.65 or (len(matching_rows) >= 6 and span >= 300):
                match = (x, top, score, len(matching_rows), span)
                break
        if match is None:
            raise RuntimeError(f"Cannot confidently locate table: {stem}")
        x, top, score, count, span = match
        rect = (x, top, x + table.width, top + table.height)
        full.crop(rect).save(HERE / "browser" / f"{stem}-table-clean.png")
        results.append({"source": f"browser/{stem}.png", "rectangle": rect,
                        "matching_text_scanlines": score, "exact_matching_text_rows": count,
                        "matching_text_span_pixels": span, "output": f"browser/{stem}-table-clean.png"})
if '--partial' not in sys.argv:
    assert len(results) == 110
receipt = HERE / ('renders/table-crop-progress.json' if '--partial' in sys.argv else 'table-crop-verification.json')
receipt.write_text(json.dumps(results, indent=2) + "\n", encoding="utf8")
print(f"Cropped {len(results)} tables from unmodified public full-page screenshots")
