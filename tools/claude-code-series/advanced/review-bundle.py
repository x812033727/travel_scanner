"""Package review materials; does not import, deploy or publish them."""
import hashlib
import json
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[3]
DOC=ROOT/'docs/claude-code-series/advanced'
manifest=json.loads((ROOT/'apps/api/app/guides/series_data/claude-code.json').read_text(encoding='utf-8'))
owned={0,20,38,41,43,47,51,*range(61,97)}
slugs={e['number']:e['slug'] for e in manifest['entries']};slugs[0]=manifest['hub']
paths={ROOT/'apps/api/app/guides/series_data/claude-code.json',ROOT/'docs/claude-code-series/source-checks.json'}
paths.add(ROOT/'.github/workflows/claude-tutorial-validation.yml')
if (DOC/'evidence/live/capstone-result.zip').exists():paths.add(DOC/'evidence/live/capstone-result.zip')
for number in owned:
    paths.add(ROOT/f'apps/api/app/guides/content/{slugs[number]}.json')
    paths.add(ROOT/f'docs/claude-code-series/lessons/{number:02d}.md')
    paths.update((ROOT/f'apps/web/public/guides/{slugs[number]}').glob('*'))
paths.update((ROOT/'apps/web/public/tutorials/claude-code/advanced').glob('*.zip'))
paths.update(DOC.glob('*.md'));paths.update(DOC.glob('*.json'))
paths.update(p for p in (DOC/'evidence').glob('*') if p.is_file() and p.suffix in {'.json','.txt','.png'})
# Keep supplementary integration receipts and their reproduction scripts with
# the review; all files here are local tests, never account credentials.
paths.update(p for p in (DOC/'evidence/live').glob('*') if p.is_file() and p.suffix in {'.json','.md','.py','.mjs','.xml','.log','.txt'} and not p.name.endswith('-runtime.txt'))
paths.discard(DOC/'review-bundle-receipt.json')
target=DOC/'review-bundle.zip'
receipt=[]
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    archive.writestr('REVIEW.md','''# Claude Code phase 2 review materials

This bundle targets the existing Travel Scanner repository, not a standalone website.
It contains 43 new/updated native packs (hub, six earlier lessons, 36 new lessons),
the 96-entry catalogue, owned art, author drafts, 36 independent lesson ZIPs,
six group ZIPs and local verification receipts. The other 54 existing lessons stay in the repository.
Start at docs/claude-code-series/advanced/README.md in the repository for all relative links.
Keep publication, import and deployment as separate authorized operations.
See the latest live/real-operations-summary.json for actual CLI, browser and SDK checks.
Earlier OAuth failures are retained as history; remaining device and service checks are listed separately.
Archive hashes in bundle-files.json identify exactly which files were included.
''')
    for path in sorted(paths):
        if not path.is_file():raise ValueError(f'Missing review file: {path}')
        name=path.relative_to(ROOT).as_posix();data=path.read_bytes();archive.writestr(name,data)
        receipt.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    archive.writestr('bundle-files.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(target) as archive:assert archive.testzip() is None
result={'file':str(target),'files':len(receipt)+2,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
(DOC/'review-bundle-receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
