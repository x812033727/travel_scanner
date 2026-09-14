"""Validate authored batches, apply explicit related links, and record evidence.

This does not write article prose, certify visual review, or publish anything.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DOCS = Path(__file__).resolve().parent
API = ROOT / 'apps/api'
WORK = ROOT / '.codex/two-site-life/work'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def run(command, cwd=ROOT):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    print(result.stdout, end='', flush=True)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument('batch', type=int)
    p.add_argument('--links', action='store_true')
    p.add_argument('--ingest', action='store_true')
    p.add_argument('--audit', action='store_true')
    args = p.parse_args()
    catalogue = read(DOCS / 'catalogue.json')['articles']
    articles = catalogue[(args.batch - 1) * 20:args.batch * 20]
    assert articles
    titles = {a['slug']: a['title'] for a in catalogue}
    links = read(DOCS / 'related-articles.json')
    log = []
    for a in articles:
        slug = a['slug']
        if args.links:
            draft_path = WORK / slug / 'draft.json'
            draft = read(draft_path)
            assert len(links[slug]) >= 2
            for dest in links[slug]:
                assert dest != slug
                target = API / 'app/guides/content' / (dest + '.json')
                assert target.exists(), target
                assert read(target)['kind'] == 'life'
            draft['links'] = [{'text': titles[s], 'url': f'https://mokaair.com/zh-TW/life/{s}'} for s in links[slug]]
            # Correct two editorial typos found by the Traditional Chinese review.
            serialized = json.dumps(draft, ensure_ascii=False, indent=2).replace('網站名称', '網站名稱').replace('問題与支援', '問題與支援')
            draft_path.write_text(serialized + '\n', encoding='utf-8')
            log.append(run([sys.executable, str(DOCS / 'prepare_article.py'), slug]))
        if args.ingest:
            log.append(run([sys.executable, '-m', 'app.guides.pack_cli', 'ingest', '--from', str(WORK), '--slug', slug], API))
    if log:
        (DOCS / f'batch-{args.batch:02d}-ingest.log').write_text(''.join(log), encoding='utf-8')
    if not args.audit:
        return
    existing = list((API / 'app/guides/content').glob('*.json'))
    paragraphs = defaultdict(set)
    for path in existing:
        pack = read(path)
        for b in pack['locales'].get('zh-TW', {}).get('blocks', []):
            if b['type'] == 'paragraph' and len(b['text']) >= 50:
                paragraphs[re.sub(r'\s+', '', b['text'])].add(pack['slug'])
    selected = {a['slug'] for a in articles}
    duplicates = [{'slugs': sorted(s), 'text': t} for t, s in paragraphs.items() if len(s) > 1 and s & selected]
    report = {'batch': args.batch, 'checked_on': '2026-09-14', 'count': len(articles), 'total_local_packs': len(existing),
              'publication': 'not imported or published; related links require the referenced packs to be published together or already present',
              'duplicate_paragraphs_50plus': duplicates, 'articles': []}
    for a in articles:
        slug = a['slug']
        pack_path = API / 'app/guides/content' / (slug + '.json')
        pack = read(pack_path)
        doc = pack['locales']['zh-TW']
        assert pack['kind'] == 'life' and pack['destination_id'] is None
        body = ''.join(b['text'] if b['type'] in ('paragraph', 'callout') else ''.join(b['items']) if b['type'] == 'list' else '' for b in doc['blocks'])
        chars = len(re.sub(r'\s+', '', body))
        assert 1800 <= chars <= 3000
        related = [b['url'] for b in doc['blocks'] if b['type'] == 'link' and '/zh-TW/life/' in b['url']]
        assert len(related) >= 2
        for url in related:
            assert (API / 'app/guides/content' / (url.rsplit('/', 1)[1] + '.json')).exists()
        assert all(s['checked_on'] for s in doc['sources'])
        files = [pack_path, DOCS / 'notes' / (slug + '.md')]
        files += [ROOT / 'apps/web/public/guides' / slug / n for n in ['hero.jpg', 'hero.svg', 'diagram-1.svg']]
        files += [ROOT / '.codex/two-site-life/qa' / (slug + '-' + n + '.png') for n in ['hero', 'diagram-1']]
        evidence = [{'path': str(f.relative_to(ROOT)).replace('\\', '/'), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]
        report['articles'].append({'slug': slug, 'body_characters': chars, 'related': related, 'evidence': evidence})
    assert not duplicates, duplicates
    (DOCS / f'batch-{args.batch:02d}-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"batch {args.batch:02d}: {len(articles)} complete packs, zero repeated paragraphs >=50 characters")


if __name__ == '__main__':
    main()
