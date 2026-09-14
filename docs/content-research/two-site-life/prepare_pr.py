"""One-time integration of the completed delivery with the reviewed main inventory.

Preserves original batch manifests and records reversible byte transformations.
Never imports, publishes, or deploys articles.
"""
import hashlib
import json
from pathlib import Path
import subprocess

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[2]
SUPERSEDED = {
    'small-language-models': ('ai-term-small-language-model', '同為小型語言模型的適用工作、限制與是否採用的入門判斷。'),
    'rag-retrieval-explained': ('ai-term-retrieval-augmented-generation', '同為 RAG 檢索、引用與資料更新限制的入門解說。'),
    'generative-ai-basics': ('ai-term-generative-ai', '同為生成式 AI 的生成方式、用途與輸出查核入門。'),
    'claude-code-plugin-management': ('claude-code-plugins-guide', '同為 Claude Code 外掛的來源、安裝、更新與移除操作。'),
}
LINK_FROM = b'https://mokaair.com/zh-TW/life/generative-ai-basics'
LINK_TO = b'https://mokaair.com/zh-TW/life/ai-term-generative-ai'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    assert not (DOCS / 'pr-evidence.json').exists(), 'Integration already recorded; use final_audit.py to verify.'
    catalogue = read(DOCS / 'catalogue.json')['articles']
    selected = {a['slug'] for a in catalogue}
    upstream = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', upstream, 'apps/api/app/guides/content'], cwd=ROOT, text=True).splitlines()
    inventory = []
    for path in paths:
        if not path.endswith('.json'):
            continue
        pack = json.loads(subprocess.check_output(['git', 'show', f'{upstream}:{path}'], cwd=ROOT))
        inventory.append({'slug': pack['slug'], 'title': pack['locales'].get('zh-TW', {}).get('title'), 'path': path})
    assert len(inventory) == 398
    assert not selected.intersection(p['slug'] for p in inventory)
    assert all(target in {p['slug'] for p in inventory} for target, _ in SUPERSEDED.values())
    evidence = []
    for batch in range(1, 13):
        for article in read(DOCS / f'batch-{batch:02d}-audit.json')['articles']:
            for item in article['evidence']:
                path = ROOT / item['path']
                data = path.read_bytes()
                assert hashlib.sha256(data).hexdigest() == item['sha256'], path
                normalized = data.replace(b'\r\n', b'\n') if path.suffix in ('.json', '.md', '.svg') else data
                evidence.append({
                    'slug': article['slug'], 'original_path': item['path'],
                    'original_sha256': item['sha256'], 'path': item['path'],
                    'original_crlf': data != normalized,
                    'normalized_sha256': hashlib.sha256(normalized).hexdigest(),
                    'related_link_redirect': article['slug'] == 'claude-cowork-evaluation' and path.suffix == '.json',
                })
    # Archive and verify each file before removing its original importable copy.
    for slug in SUPERSEDED:
        archive = DOCS / 'superseded' / slug
        archive.mkdir(parents=True, exist_ok=True)
        originals = [ROOT / f'apps/api/app/guides/content/{slug}.json']
        originals += [ROOT / f'apps/web/public/guides/{slug}/{name}' for name in ('hero.jpg', 'hero.svg', 'diagram-1.svg')]
        for original in originals:
            assert original.resolve().is_relative_to(ROOT.resolve())
            destination = archive / original.name
            destination.write_bytes(original.read_bytes())
            assert destination.read_bytes() == original.read_bytes()
            for item in evidence:
                if item['original_path'] == original.relative_to(ROOT).as_posix():
                    item['path'] = destination.relative_to(ROOT).as_posix()
            original.unlink()
    for item in evidence:
        path = ROOT / item['path']
        data = path.read_bytes()
        if path.suffix in ('.json', '.md', '.svg'):
            data = data.replace(b'\r\n', b'\n')
        if item['related_link_redirect']:
            assert data.count(LINK_FROM) == 1
            data = data.replace(LINK_FROM, LINK_TO)
        path.write_bytes(data)
        item['sha256'] = hashlib.sha256(data).hexdigest()
    for name in ('draft.json', 'pack.json'):
        path = ROOT / '.codex/two-site-life/work/claude-cowork-evaluation' / name
        data = path.read_bytes().replace(b'\r\n', b'\n')
        assert data.count(LINK_FROM) == 1
        path.write_bytes(data.replace(LINK_FROM, LINK_TO))
    write(DOCS / 'pr-evidence.json', {'original_hashes_verified_before_integration': len(evidence), 'evidence': evidence})
    write(DOCS / 'pr-integration.json', {
        'checked_on': '2026-09-14', 'base_sha': upstream,
        'original_authored_count': 232, 'active_new_article_count': 228,
        'upstream_pack_count': len(inventory), 'upstream_articles': inventory,
        'semantic_review': '與新增主分支文章依主題、讀者問題、操作目的重查。四組同需求改為既有涵蓋；其餘仍以選題表指定的操作任務區分。',
        'superseded': [{'slug': slug, 'replacement_slug': target, 'reason': reason,
                        'archive': f'docs/content-research/two-site-life/superseded/{slug}',
                        'source_keys': next(a['source_keys'] for a in catalogue if a['slug'] == slug)}
                       for slug, (target, reason) in SUPERSEDED.items()],
        'related_link_redirects': [{'slug': 'claude-cowork-evaluation', 'from': LINK_FROM.decode(), 'to': LINK_TO.decode()}],
        'evidence_note': '原始批次 SHA 保留不改寫；pr-evidence.json 保存可逆的 LF 正規化、封存路徑與單一站內連結替換。',
    })
    print(f'Integrated: {len(evidence)} original hashes verified; 228 active packs; four drafts archived.')


if __name__ == '__main__':
    main()
