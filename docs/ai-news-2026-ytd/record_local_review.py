"""Record the completed editorial and rendered-art review before opening the PR."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
slugs = json.loads((HERE / 'slugs.json').read_text(encoding='utf-8'))
assets = []
for slug in slugs:
    for asset in sorted((ROOT / 'apps/web/public/guides' / slug).iterdir()):
        if asset.name.startswith('hero') and asset.suffix == '.svg':
            continue
        assets.append({'path': asset.relative_to(ROOT).as_posix(),
                       'bytes': asset.stat().st_size,
                       'sha256': hashlib.sha256(asset.read_bytes()).hexdigest()})
assert len(assets) == 220 and max(a['bytes'] for a in assets) < 300_000
sheets = sorted(p.name for p in HERE.glob('*sheet-*.jpg'))
assert len(sheets) == 60
receipt = {'checked_on': '2026-09-14', 'status': 'reviewed',
           'public_assets': 220, 'rendered_dimensions': [1600, 900],
           'method': 'All 60 final contact sheets visually inspected; Chromium rendered every localized hero and diagram with fonts loaded. Labels, spacing, dates, credits, contrast and clipping checked.',
           'fixes': ['Chronological index hero corrected to nine numbered month cards before final review.'],
           'limitations': 'Local artwork review only; public page verification follows deployment.',
           'sheets': sheets, 'assets': assets}
(HERE / 'visual-verification.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
