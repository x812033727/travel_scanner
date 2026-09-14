"""Create a portable review/content-import bundle; never import or publish."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / 'apps/api/app/guides/series_data/claude-code.json').read_text(encoding='utf-8'))
files = {}
for slug in [manifest['hub'], *[entry['slug'] for entry in manifest['entries']]]:
    files[f'content/{slug}.json'] = ROOT / f'apps/api/app/guides/content/{slug}.json'
    for image in (ROOT / f'apps/web/public/guides/{slug}').iterdir():
        if image.is_file(): files[f'web-public/guides/{slug}/{image.name}'] = image
for download in (ROOT / 'apps/web/public/tutorials/claude-code').glob('*.zip'):
    files[f'web-public/tutorials/claude-code/{download.name}'] = download
for document in (ROOT / 'docs/claude-code-series/lessons').glob('*.md'):
    files[f'lessons/{document.name}'] = document
for name in ['README.md', 'source-checks.json']:
    files[name] = ROOT / 'docs/claude-code-series' / name
for evidence in (ROOT / 'docs/claude-code-series/evidence').iterdir():
    if evidence.is_file() and evidence.suffix in {'.json', '.md', '.png', '.log'}:
        files[f'evidence/{evidence.name}'] = evidence
files['series/claude-code.json'] = ROOT / 'apps/api/app/guides/series_data/claude-code.json'
target = ROOT / 'docs/claude-code-series/review-bundle.zip'
with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    for name, source in sorted(files.items()):
        if not source.is_file(): raise FileNotFoundError(source)
        archive.write(source, name)
    archive.writestr('checksums.json', json.dumps({name: hashlib.sha256(source.read_bytes()).hexdigest() for name, source in sorted(files.items())}, indent=2))
print(json.dumps({'bundle': str(target), 'files': len(files) + 1, 'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))
