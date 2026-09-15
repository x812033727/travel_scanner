"""Validate the review bundle without writing to a database or publishing content."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import _body_length, check_svg, lint_document  # noqa: E402
from app.guides.series import Catalogue  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--partial', action='store_true', help='Report missing lessons without passing final acceptance')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/claude-code-series/evidence/content-validation.json')
    args = parser.parse_args()
    catalogue = Catalogue.model_validate(json.loads((ROOT / 'apps/api/app/guides/series_data/claude-code.json').read_text(encoding='utf-8')))
    expected = {entry.slug for entry in catalogue.entries} | {catalogue.hub}
    checks = {entry['url']: entry for entry in json.loads((ROOT / 'docs/claude-code-series/source-checks.json').read_text(encoding='utf-8'))}
    report = {'expected_pages': len(expected), 'pages': [], 'missing': [], 'errors': [], 'warnings': [],
              'verification': {'source_documents': True, 'claude_product_operations': False, 'production_imported': False, 'production_published': False}}
    for slug in sorted(expected):
        path = ROOT / f'apps/api/app/guides/content/{slug}.json'
        if not path.exists():
            report['missing'].append(slug)
            continue
        pack = ArticlePack.model_validate(json.loads(path.read_text(encoding='utf-8')))
        if pack.slug != slug or pack.kind != 'life' or set(pack.locales) != {'zh-TW'} or set(pack.topics) != {'ai', 'tutorial'}:
            report['errors'].append(f'{slug}: incorrect identity, locales or topics')
        doc = pack.locales['zh-TW']
        for issue in lint_document(doc, 'life'):
            if slug in {catalogue.hub, 'claude-code-templates-cheatsheet'} and issue.code == 'text_length':
                continue
            report['errors' if issue.level == 'error' else 'warnings'].append(f'{slug}: {issue.code}: {issue.message}')
        for source in doc.sources:
            checked = checks.get(source.url)
            if not checked or checked['status'] != 200 or not checked['title'] or str(source.checked_on) != checked['checked_on']:
                report['errors'].append(f'{slug}: unverified source {source.url}')
        refs = set()
        code_count = 0
        for block in doc.blocks:
            if block.type == 'rich_paragraph':
                for node in block.inlines:
                    if node.type == 'article':
                        refs.add(node.slug)
                        if node.kind != 'life' or node.slug not in expected:
                            report['errors'].append(f'{slug}: unknown internal reference {node.slug}')
                    if node.type == 'link' and '/tutorials/claude-code/' in urlparse(node.url).path:
                        base = (ROOT / 'apps/web/public/tutorials/claude-code').resolve()
                        filename = unquote(urlparse(node.url).path.split('/tutorials/claude-code/', 1)[1])
                        target = (base / filename).resolve()
                        if not target.is_relative_to(base) or not target.is_file():
                            report['errors'].append(f'{slug}: missing or unsafe download {filename}')
            elif block.type == 'code':
                code_count += 1
                if not block.label or not block.code.endswith('\n'):
                    report['errors'].append(f'{slug}: code missing label or final newline')
        if slug != catalogue.hub and catalogue.hub not in refs:
            report['errors'].append(f'{slug}: no directory return reference')
        if slug != catalogue.hub and not code_count:
            report['errors'].append(f'{slug}: no complete example')
        assets = ROOT / 'apps/web/public/guides' / slug
        for filename in ['hero.jpg', 'hero.svg', 'diagram-1.svg']:
            asset = assets / filename
            if not asset.exists():
                report['errors'].append(f'{slug}: missing {filename}')
            elif filename.endswith('.svg'):
                for issue in check_svg(asset.read_text(encoding='utf-8')):
                    report['errors' if issue.level == 'error' else 'warnings'].append(f'{slug}/{filename}: {issue.message}')
        report['pages'].append({'slug': slug, 'body_characters': _body_length(doc), 'blocks': len(doc.blocks), 'code_examples': code_count, 'internal_targets': sorted(refs)})
    report['complete'] = not report['missing'] and not report['errors']
    target = args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'pages': len(report['pages']), 'missing': len(report['missing']), 'errors': report['errors'], 'warnings': report['warnings'], 'complete': report['complete']}, ensure_ascii=False, indent=2))
    return int(bool(report['errors']) or (bool(report['missing']) and not args.partial))


if __name__ == '__main__':
    sys.exit(main())
