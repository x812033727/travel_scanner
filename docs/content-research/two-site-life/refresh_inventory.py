"""Record the current local article and task inventory before a batch is closed."""
import argparse
import datetime
import json
from pathlib import Path
import re

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('batch', type=int)
    args = parser.parse_args()
    baseline = json.loads((DOCS / 'existing-snapshot.json').read_text(encoding='utf-8'))
    catalogue = json.loads((DOCS / 'catalogue.json').read_text(encoding='utf-8'))['articles']
    planned = []
    for line in (ROOT / 'docs/life-ai-series.md').read_text(encoding='utf-8').splitlines():
        cells = [cell.strip() for cell in line.split('|')]
        if len(cells) > 4 and re.fullmatch(r'\d+', cells[1]) and re.fullmatch(r'`[a-z0-9-]+`', cells[2]):
            planned.append({'slug': cells[2].strip('`'), 'title': cells[3]})
    known = {a['slug'] for a in baseline['existing'] + catalogue + planned}
    local = []
    for path in sorted((ROOT / 'apps/api/app/guides/content').glob('*.json')):
        pack = json.loads(path.read_text(encoding='utf-8'))
        local.append({'slug': pack['slug'], 'kind': pack['kind'], 'title': pack['locales'].get('zh-TW', {}).get('title', '')})
    tasks = []
    for directory in ['open', 'done']:
        for path in sorted((ROOT / 'tasks' / directory).glob('*.md')):
            text = path.read_text(encoding='utf-8')
            slugs = sorted(set(re.findall(r'apps/api/app/guides/content/([a-z0-9-]+)\.json', text)))
            if not slugs and not re.search(r'apps/api/app/guides|apps/web/public/guides|docs/life-ai-series|^title:.*(?:文章|生活分享|content pack)', text, re.M):
                continue
            fields = {}
            for field in ['id', 'title', 'status', 'owner']:
                match = re.search(r'^' + field + r':(.*)$', text, re.M)
                fields[field] = match[1].strip() if match else ''
            tasks.append({'path': path.relative_to(ROOT).as_posix(), **fields, 'slugs': slugs})
    report = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'batch': args.batch,
              'local_pack_count': len(local), 'local_packs': local, 'planned_ai_count': len(planned),
              'planned_ai': planned, 'content_tasks_checked': tasks,
              'new_unmapped_packs': [a for a in local if a['slug'] not in known],
              'new_unmapped_task_slugs': sorted({s for t in tasks for s in t['slugs']} - known)}
    (DOCS / f'batch-{args.batch:02d}-live-inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{len(local)} local packs; {len(planned)} planned AI titles; {len(tasks)} content tasks")
    print(f"Unmapped packs: {report['new_unmapped_packs']}; unmapped task slugs: {report['new_unmapped_task_slugs']}")


if __name__ == '__main__':
    main()
