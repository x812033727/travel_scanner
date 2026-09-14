"""Materialize the reviewed title-to-topic assignments; never fabricates article bodies."""
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]


def main():
    source = json.loads((OUT / "titles.json").read_text(encoding="utf-8"))
    baseline = json.loads((OUT / "existing-snapshot.json").read_text(encoding="utf-8"))
    reviewed = json.loads((OUT / "assignments.json").read_text(encoding="utf-8"))
    previous_path = OUT / 'catalogue.json'
    previous = {a['slug']: a for a in json.loads(previous_path.read_text(encoding='utf-8'))['articles']} if previous_path.exists() else {}
    by_key = {(('F' if row['source'] == 'frankknow' else 'N') + str(row['source_id'])): row for row in source['articles']}
    existing = {row['slug']: row for row in baseline['existing']}
    planned = {row['slug']: row for row in baseline['planned_ai']}
    integration_path = OUT / 'pr-integration.json'
    integration = json.loads(integration_path.read_text(encoding='utf-8')) if integration_path.exists() else {}
    superseded = {row['slug']: row for row in integration.get('superseded', [])}
    new, decisions = [], {}
    for index, assignment in enumerate(reviewed['new_articles']):
        item = dict(assignment)
        item['batch'] = index // 20 + 1
        item['coverage'] = item['coverage'].replace('条件', '條件').replace('预览', '預覽').replace('与', '與')
        assert item['slug'] not in existing and item['slug'] not in planned, item['slug']
        item['topics'] = ['tutorial', 'software'] if item['group'] != '行銷與經營' else ['tutorial', 'misc']
        if item['slug'].startswith(('ai-', 'claude-', 'rag-', 'generative-', 'small-language-')):
            item['topics'] = ['ai', 'tutorial']
        item['angle'] = item['title']
        item['must_cover'] = [s.strip() for s in item['coverage'].split('、')]
        item['hero'] = {'size': [1600, 900], 'format': 'original SVG plus hero.jpg',
                        'subject': item['title'], 'visual_focus': item['must_cover'],
                        'style': '原創幾何插圖；繁體中文；不用供應商介面截圖或商標圖檔'}
        item['diagram'] = {'size': [1600, 900], 'format': 'original SVG',
                           'subject': item['title'], 'required_concepts': item['must_cover'],
                           'purpose': '清楚區分本篇讀者任務的操作階段或比較項目，標示需驗證的結果'}
        item['internal_links'] = previous.get(item['slug'], {}).get('internal_links', [])
        item['status'] = previous.get(item['slug'], {}).get('status', 'assigned')
        draft_path = ROOT / '.codex/two-site-life/work' / item['slug'] / 'draft.json'
        if draft_path.exists():
            draft = json.loads(draft_path.read_text(encoding='utf-8'))
            item['hero']['authored_design'] = draft['hero_art']
            item['diagram']['authored_design'] = draft['diagram']
            item['internal_links'] = [link['url'] for link in draft.get('links', [])]
        replacement = superseded.get(item['slug'])
        if replacement:
            item['status'] = 'covered_upstream'
            item['replacement_slug'] = replacement['replacement_slug']
            item['archive'] = replacement['archive']
        new.append(item)
        for offset, key in enumerate(item['source_keys']):
            assert key in by_key and key not in decisions, key
            decisions[key] = {'decision': 'new' if offset == 0 else 'merged', 'target_slug': item['slug'],
                              'reason': '以相同讀者任務合併來源題目；正文另外查證並原創撰寫。' if offset else '獨立讀者任務；新增完整文章。'}
            if replacement:
                decisions[key] = {'decision': 'covered_existing', 'target_slug': replacement['replacement_slug'],
                                  'reason': 'PR 整合時主分支已有同需求文章；完整原創稿保留內部封存。' + replacement['reason']}
    for slug, keys in reviewed['covered']:
        assert slug in existing or slug in planned, slug
        for key in keys.split():
            assert key in by_key and key not in decisions, key
            decisions[key] = {'decision': 'covered_existing' if slug in existing else 'covered_planned',
                              'target_slug': slug, 'reason': '與既有／AI 系列已指定文章回答同一問題；避免再開相同入門題目。'}
    for row in reviewed['excluded']:
        key = row['key']
        assert key in by_key and key not in decisions, key
        decisions[key] = {'decision': 'excluded', 'target_slug': None, 'reason': row['reason']}
    assert set(decisions) == set(by_key), sorted(set(by_key) - set(decisions))
    assert len({a['slug'] for a in new}) == len(new)
    mapping = [{**row, 'short_key': key, **decisions[key]} for key, row in by_key.items()]
    active_count = len(new) - len(superseded)
    (OUT / 'mapping.json').write_text(json.dumps({'checked_at': source['checked_at'], 'source_count': len(mapping),
                                               'new_article_count': active_count, 'original_authored_count': len(new), 'mapping': mapping}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'catalogue.json').write_text(json.dumps({'active_new_article_count': active_count, 'original_authored_count': len(new), 'articles': new}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# 原創文章選題總表', '', f'{len(mapping)} 筆來源標題；完成 {len(new)} 篇原創稿，其中 {active_count} 篇新增內容包、{len(superseded)} 篇由主分支文章涵蓋並保留封存稿；每批最多 20 篇。', '',
             '本表是指派，不代表正文、圖片、匯入或發布完成。實際狀態見各批任務與內容包。', '',
             '| 批次 | slug | 原創標題 | 必寫重點 | 狀態 | 來源 ID |', '| --- | --- | --- | --- | --- | --- |']
    lines.extend(f"| {a['batch']:02d} | `{a['slug']}` | {a['title']} | {a['coverage']} | {a['status']} | {', '.join(a['source_keys'])} |" for a in new)
    lines += ['', '每篇固定的圖像主題、必要概念與尺寸見 catalogue.json 的 hero／diagram；已有正文者並保存實際配圖設計。圖像規劃不算已完成圖片。', '']
    if superseded:
        lines += ['## PR 整合去重', '', '| 封存原稿 | 主分支對應文章 | 原因 |', '| --- | --- | --- |']
        lines.extend(f"| {slug} | {row['replacement_slug']} | {row['reason']} |" for slug, row in superseded.items())
    lines += ['', '## 每筆來源處理結果', '', '| 來源 | 原標題 | 處理 | 對應 slug | 原因 |', '| --- | --- | --- | --- | --- |']
    lines.extend(f"| {row['short_key']} | [{row['title'].replace('|', '&#124;')}]({row['url']}) | {row['decision']} | {row['target_slug'] or '—'} | {row['reason']} |" for row in mapping)
    (OUT / 'catalogue.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{len(mapping)} source decisions; {active_count} active new articles; {len(superseded)} archived drafts; {(len(new) + 19) // 20} batches')


if __name__ == '__main__':
    main()
