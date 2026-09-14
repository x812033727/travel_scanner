"""Ingest only this series' complete staged articles after source-matched rendering.

No production connections. Article API schema, image dimensions/credits, SVG and
editorial checks are enforced by the existing content-pack pipeline.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.guides.pack_ingest import commons_client, ingest

catalogue = json.loads((HERE / 'catalogue.json').read_text(encoding='utf-8'))
renders = json.loads((HERE / 'renders/manifest.json').read_text(encoding='utf-8'))
selected = set(sys.argv[1:])
slugs = [t['slug'] for t in catalogue['terms']] + ['ai-terms-index']
log = []
with commons_client() as client:
    for slug in slugs:
        if selected and slug not in selected:
            continue
        folder = HERE / 'staging' / slug
        if not (folder / 'research.json').is_file():
            continue
        research = json.loads((folder / 'research.json').read_text(encoding='utf-8'))
        if research.get('status') != 'verified':
            continue
        def renderer(src, dest):
            key = f'{slug}-{src.stem}'
            expected = renders[key]
            assert hashlib.sha256(src.read_bytes()).hexdigest() == expected['sha256'], f'Rerender changed {key}'
            shutil.copyfile(HERE / 'renders' / expected['png'], dest)
        report = ingest(HERE / 'staging', slug,
                        content_dir=ROOT / 'apps/api/app/guides/content',
                        public_dir=ROOT / 'apps/web/public', client=client, renderer=renderer)
        assert report.ok, (slug, report.problems)
        log.append({'slug': slug, 'files': [str(p.relative_to(ROOT)) for p in report.written],
                    'warnings': [str(p) for p in report.problems]})
        print(f'Ingested {slug}', flush=True)
(HERE / 'ingest-log.json').write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
