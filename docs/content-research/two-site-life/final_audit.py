"""Audit the delivered title mapping and packs without importing or publishing."""
from collections import Counter, defaultdict
import datetime
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[2]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    titles = read(DOCS / 'titles.json')
    catalogue = read(DOCS / 'catalogue.json')['articles']
    mapping = read(DOCS / 'mapping.json')['mapping']
    baseline = read(DOCS / 'existing-snapshot.json')
    inventory = read(DOCS / 'batch-12-live-inventory.json')
    integration_path = DOCS / 'pr-integration.json'
    integration = read(integration_path) if integration_path.exists() else {}
    superseded = {row['slug']: row for row in integration.get('superseded', [])}
    pr_evidence = {row['original_path']: row for row in read(DOCS / 'pr-evidence.json')['evidence']} if integration else {}
    assert len(titles['articles']) == titles['count'] == len(mapping) == 474
    assert Counter(x['source'] for x in titles['articles']) == {'frankknow': 394, 'notesstartup': 80}
    assert len({x['url'] for x in titles['articles']}) == 474
    assert {x['key'] for x in mapping} == {x['key'] for x in titles['articles']}
    for row in titles['articles']:
        cleaned = re.sub(r'\s+', ' ', re.sub(r'[\x00-\x1f\x7f]', '', html.unescape(re.sub(r'<[^>]+>', '', row['original_title'])))).strip()
        assert row['title'] == cleaned and row['checked_on']
    selected = {a['slug'] for a in catalogue}
    existing = {a['slug'] for a in baseline['existing']}
    planned = {a['slug'] for a in inventory['planned_ai']}
    assert len(selected) == len(catalogue) == 232
    assert len(existing) == 110 and len(planned) == 220
    assert not selected & (existing | planned)
    assert not inventory['new_unmapped_packs'] and not inventory['new_unmapped_task_slugs']
    active = selected - superseded.keys()
    upstream = {row['slug'] for row in integration.get('upstream_articles', [])}
    assert not selected & upstream
    decisions = Counter(x['decision'] for x in mapping)
    assert decisions == {'new': len(active), 'merged': 224, 'covered_existing': 7 + len(superseded), 'covered_planned': 10, 'excluded': 1}
    for row in mapping:
        assert row['reason']
        if row['decision'] in ('new', 'merged'):
            assert row['target_slug'] in active
        elif row['decision'] == 'covered_existing':
            assert row['target_slug'] in existing | upstream
        elif row['decision'] == 'covered_planned':
            assert row['target_slug'] in planned
        else:
            assert row['target_slug'] is None
    records = []
    for batch in range(1, 13):
        audit = read(DOCS / f'batch-{batch:02d}-audit.json')
        assert audit['count'] == (20 if batch < 12 else 12)
        assert not audit['duplicate_paragraphs_50plus']
        assert (DOCS / f'batch-{batch:02d}-review.md').exists()
        assert f"{audit['count']} entries checked" in (DOCS / f'batch-{batch:02d}-lint.log').read_text(encoding='utf-8-sig')
        assert '9 passed, 5 skipped' in (DOCS / f'batch-{batch:02d}-tests.log').read_text(encoding='utf-8-sig')
        for article in audit['articles']:
            assert len(article['evidence']) == 7
            for evidence in article['evidence']:
                current = pr_evidence.get(evidence['path'], evidence)
                path = ROOT / current['path']
                assert path.is_file(), path
                data = path.read_bytes()
                assert hashlib.sha256(data).hexdigest() == current['sha256'], path
                if integration:
                    assert current['original_sha256'] == evidence['sha256']
                    if current['related_link_redirect']:
                        old = b'https://mokaair.com/zh-TW/life/generative-ai-basics'
                        new = b'https://mokaair.com/zh-TW/life/ai-term-generative-ai'
                        assert data.count(new) == 1 and old not in data
                        data = data.replace(new, old)
                    assert hashlib.sha256(data).hexdigest() == current['normalized_sha256'], path
                    if current['original_crlf']:
                        data = data.replace(b'\n', b'\r\n')
                    assert hashlib.sha256(data).hexdigest() == evidence['sha256'], path
            records.append(article)
    assert {r['slug'] for r in records} == selected and len(records) == 232
    if integration:
        assert len(pr_evidence) == 1624
    paragraphs = defaultdict(set)
    packs = list((ROOT / 'apps/api/app/guides/content').glob('*.json'))
    for path in packs:
        pack = read(path)
        for block in pack['locales'].get('zh-TW', {}).get('blocks', []):
            if block['type'] == 'paragraph' and len(block['text']) >= 50:
                paragraphs[re.sub(r'\s+', '', block['text'])].add(pack['slug'])
    duplicates = [{'slugs': sorted(s), 'text': p} for p, s in paragraphs.items() if len(s) > 1 and s & active]
    assert not duplicates
    manifest = []
    for article in catalogue:
        slug = article['slug']
        archived = slug in superseded
        assert article['status'] == ('covered_upstream' if archived else 'validated_local')
        canonical = ROOT / 'apps/api/app/guides/content' / f'{slug}.json'
        archive = ROOT / superseded[slug]['archive'] if archived else None
        path = archive / f'{slug}.json' if archived else canonical
        if archived:
            assert not canonical.exists()
            assert superseded[slug]['replacement_slug'] in upstream
        pack = read(path)
        doc = pack['locales']['zh-TW']
        assert pack['kind'] == 'life' and pack['destination_id'] is None
        assert doc['title'] == article['title']
        types = {b['type'] for b in doc['blocks']}
        assert {'paragraph', 'heading', 'list', 'table', 'callout', 'link', 'image'} <= types
        assert all(s['checked_on'] and s['url'].startswith('https://') for s in doc['sources'])
        body = ''.join(b['text'] if b['type'] in ('paragraph', 'callout') else ''.join(b['items']) if b['type'] == 'list' else '' for b in doc['blocks'])
        chars = len(re.sub(r'\s+', '', body))
        assert 1800 <= chars <= 3000
        links = [b['url'] for b in doc['blocks'] if b['type'] == 'link' and '/zh-TW/life/' in b['url']]
        assert len(links) >= 2
        for url in links:
            target = url.rsplit('/', 1)[1]
            if archived and target in superseded:
                target = superseded[target]['replacement_slug']
            dest = ROOT / 'apps/api/app/guides/content' / (target + '.json')
            assert dest.exists() and read(dest)['kind'] == 'life'
        art = archive if archived else ROOT / 'apps/web/public/guides' / slug
        for public in (path, art / 'hero.svg', art / 'diagram-1.svg'):
            assert not re.search(r'frankknow\.com|notesstartup\.com|犬哥|諾特斯', public.read_text(encoding='utf-8'), flags=re.I), public
        for name in ['hero.jpg', 'hero.svg', 'diagram-1.svg']:
            if name.endswith('.jpg'):
                with Image.open(art / name) as im:
                    assert im.size == (1600, 900)
            else:
                svg = ET.parse(art / name).getroot()
                assert svg.attrib['viewBox'] == '0 0 1600 900'
        for visual in [doc['hero'], *[b for b in doc['blocks'] if b['type'] == 'image']]:
            assert visual['credit']['author'] == 'Mokaair'
            assert visual['credit']['license'] == '© Mokaair'
            assert visual['credit'].get('source_url') is None
        manifest.append({'slug': slug, 'title': doc['title'], 'batch': article['batch'], 'body_characters': chars,
                         'status': article['status'], 'replacement_slug': superseded.get(slug, {}).get('replacement_slug'),
                         'pack': path.relative_to(ROOT).as_posix(), 'image_directory': art.relative_to(ROOT).as_posix(),
                         'research_note': f'docs/content-research/two-site-life/notes/{slug}.md',
                         'sources': len(doc['sources']), 'related': links})
    report = {'audited_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'result': 'passed',
              'publication_state': 'local reviewable packs only; no production import, publication, or deployment',
              'source_count': 474, 'sources_by_site': dict(Counter(x['source'] for x in titles['articles'])),
              'source_decisions': dict(decisions), 'original_authored_articles': len(manifest),
              'new_complete_articles': len(active), 'archived_superseded_articles': len(superseded),
              'existing_baseline_articles': 110, 'planned_ai_titles_checked': 220,
              'current_local_pack_count': len(packs), 'content_tasks_checked': len(inventory['content_tasks_checked']),
              'body_characters_min': min(x['body_characters'] for x in manifest),
              'body_characters_max': max(x['body_characters'] for x in manifest),
              'body_characters_total': sum(x['body_characters'] for x in manifest),
              'hero_jpg_count': len(active), 'original_svg_count': len(active) * 2, 'qa_png_count': 464,
              'archived_hero_jpg_count': len(superseded), 'archived_svg_count': len(superseded) * 2,
              'previous_evidence_hashes_verified': sum(len(r['evidence']) for r in records),
              'duplicate_paragraphs_50plus': duplicates, 'source_archive_verification': titles['verification'],
              'validation_limit': 'Five PostgreSQL integration tests skipped in each batch; local image review and schema/lint are not production import verification.',
              'articles': manifest}
    (DOCS / 'delivery-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"PASS: 474 source decisions; {len(active)} active packs; {len(superseded)} archived drafts; {report['previous_evidence_hashes_verified']} original evidence hashes reconstructed and verified")
    print(f"Body characters: {report['body_characters_min']}–{report['body_characters_max']}; total {report['body_characters_total']}")


if __name__ == '__main__':
    main()
