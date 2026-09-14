"""Compile authored Markdown into structured article packs; never imports or publishes.

Only this series uses this authoring format. Code fences require a language and an input
location. article: links become publication-checked references, not arbitrary HTML.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import _body_length  # noqa: E402

MANIFEST = ROOT / 'apps/api/app/guides/series_data/claude-code.json'
AUTHORED = ROOT / 'docs/claude-code-series/lessons'
CONTENT = ROOT / 'apps/api/app/guides/content'
ASSETS = ROOT / 'apps/web/public/guides'
INLINE = re.compile(r'`([^`]+)`|\[([^\]]+)\]\(([^\s)]+)\)')


def inlines(text):
    nodes = []
    offset = 0
    for match in INLINE.finditer(text):
        if match.start() > offset:
            nodes.append({'type': 'text', 'text': text[offset:match.start()]})
        if match.group(1) is not None:
            nodes.append({'type': 'code', 'text': match.group(1)})
        elif match.group(3).startswith('article:'):
            nodes.append({'type': 'article', 'kind': 'life', 'slug': match.group(3)[8:], 'text': match.group(2)})
        else:
            nodes.append({'type': 'link', 'url': match.group(3), 'text': match.group(2)})
        offset = match.end()
    if offset < len(text):
        nodes.append({'type': 'text', 'text': text[offset:]})
    return nodes


def parse(text):
    lines = text.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('```'):
            fence = re.match(r'^`{3,}', line).group(0)
            parts = line[len(fence):].split(' ', 1)
            if len(parts) != 2:
                raise ValueError('Every code fence needs a language and input-location label')
            code = []
            i += 1
            while i < len(lines) and lines[i].strip() != fence:
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError('Unclosed code fence')
            blocks.append({'type': 'code', 'language': parts[0], 'label': parts[1], 'code': '\n'.join(code) + '\n'})
        elif line.startswith('## '):
            blocks.append({'type': 'heading', 'level': 2, 'text': line[3:]})
        elif line.startswith('### '):
            blocks.append({'type': 'heading', 'level': 3, 'text': line[4:]})
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [cell.strip() for cell in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in row):
                    rows.append(row)
                i += 1
            blocks.append({'type': 'table', 'header': rows[0], 'rows': rows[1:]})
            continue
        elif line.startswith('> '):
            blocks.append({'type': 'callout', 'tone': 'tip', 'title': '操作提醒', 'text': line[2:]})
        elif line.startswith('- ') or re.match(r'^\d+\. ', line):
            ordered = not line.startswith('- ')
            items = []
            pattern = r'^\d+\. ' if ordered else r'^- '
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append(re.sub(pattern, '', lines[i].strip()))
                i += 1
            blocks.append({'type': 'list', 'ordered': ordered, 'items': items})
            continue
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#{2,3} |```|\||> |- |\d+\. )', lines[i]):
                paragraph.append(lines[i].strip())
                i += 1
            value = '\n'.join(paragraph)
            nodes = inlines(value)
            blocks.append({'type': 'rich_paragraph', 'inlines': nodes} if INLINE.search(value) else {'type': 'paragraph', 'text': value})
            continue
        i += 1
    return blocks


def svg_document(title, inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="'Noto Sans TC','Microsoft JhengHei',system-ui,sans-serif">
<title id="title">{html.escape(title)} / Claude Code tutorial</title><desc id="desc">{html.escape(title)}，以流程和文件圖形呈現教學重點。</desc>
<rect width="1600" height="900" fill="#F7F1E8"/>{inner}<text x="1540" y="865" text-anchor="end" font-size="20" fill="#5C6B6B">© Mokaair</text></svg>'''


def assets(slug, title, steps, index):
    directory = ASSETS / slug
    directory.mkdir(parents=True, exist_ok=True)
    color = ['#0D6B68', '#2F6F9F', '#D97A2B'][index % 3]
    diagram = f'<text x="90" y="110" font-size="46" font-weight="bold" fill="#102A2B">{html.escape(title[:27])}</text>'
    diagram += '<text x="90" y="173" font-size="24" fill="#5C6B6B">跟著這條流程，完成本篇練習</text>'
    for i, label in enumerate(steps[:3]):
        x = 80 + i * 520
        diagram += f'<rect x="{x}" y="325" width="400" height="230" rx="24" fill="#FFFFFF" stroke="{color}" stroke-width="4"/>'
        for j, chunk in enumerate([label[:10], label[10:20]]):
            if chunk:
                diagram += f'<text x="{x+200}" y="{428+j*55}" text-anchor="middle" font-size="34" fill="#102A2B">{html.escape(chunk)}</text>'
        if i < 2:
            diagram += f'<path d="M{x+426} 440 h50 m-15 -15 15 15 -15 15" stroke="{color}" stroke-width="7" fill="none"/>'
    (directory / 'diagram-1.svg').write_text(svg_document(title, diagram), encoding='utf-8')
    # Ten arrangements share the site's simple geometric illustration vocabulary.
    offset = index % 10 * 12
    hero = f'''<text x="80" y="95" font-size="44" font-weight="bold" fill="#102A2B">{html.escape(title)}</text>
<text x="80" y="148" font-size="24" fill="{color}">CLAUDE CODE · {index:02}</text>
<circle cx="{1190-offset}" cy="250" r="160" fill="#E3F0EF"/>
<circle cx="{350+offset}" cy="650" r="130" fill="#E6F0F7"/>
<rect x="440" y="175" width="690" height="465" rx="36" fill="#FFFFFF" stroke="{color}" stroke-width="12"/>
<path d="M650 640 l-35 95 h340 l-35 -95" fill="#E3F0EF" stroke="{color}" stroke-width="10"/>
<rect x="{555+offset}" y="270" width="220" height="275" rx="18" fill="#F7F1E8" stroke="#102A2B" stroke-width="7"/>
<path d="M{590+offset} 340 h145 M{590+offset} 395 h110 M{590+offset} 450 h130" stroke="{color}" stroke-width="13" stroke-linecap="round"/>
<circle cx="1040" cy="540" r="110" fill="{color}"/>
<path d="M990 540 l35 35 65 -75" stroke="#FFFFFF" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'''
    (directory / 'hero.svg').write_text(svg_document(title, hero), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='*', type=int)
    args = parser.parse_args()
    catalogue = json.loads(MANIFEST.read_text(encoding='utf-8'))
    checks = {entry['url']: entry for entry in json.loads((ROOT / 'docs/claude-code-series/source-checks.json').read_text(encoding='utf-8'))}
    report = []
    hub = {'number': 0, 'slug': catalogue['hub'], 'title': 'Claude Code 完整教學目錄：從入門到自動化',
           'outcome': '依平台、程度與功能找到需要的教學，從 60 篇文章與共用練習專案逐步完成操作。',
           'sources': ['https://code.claude.com/docs/en/overview', 'https://code.claude.com/docs/en/platforms', 'https://code.claude.com/docs/en/commands'],
           'related': []}
    for entry in [hub, *catalogue['entries']]:
        number = entry['number']
        if args.only and number not in args.only:
            continue
        authored = AUTHORED / f'{number:02}.md'
        if not authored.exists():
            continue
        blocks = parse(authored.read_text(encoding='utf-8'))
        if not any(block['type'] == 'callout' and block['title'] == '驗證範圍' for block in blocks):
            blocks.insert(2, {'type': 'callout', 'tone': 'info', 'title': '驗證範圍',
                'text': '本文依官方文件核對功能與步驟，來源日期列於文末。Claude 帳號登入、外部服務與裝置操作需在你的環境實際驗證；本文不將文件查證視為已替讀者完成操作。'})
        headings = [b['text'] for b in blocks if b['type'] == 'heading' and b['level'] == 2]
        diagram_steps = headings[:3]
        assets(entry['slug'], entry['title'], diagram_steps, number)
        blocks.insert(min(4, len(blocks)), {'type': 'image', 'src': f'/guides/{entry["slug"]}/diagram-1.svg', 'alt': ' → '.join(diagram_steps), 'width': 1600, 'height': 900, 'caption': ' → '.join(diagram_steps), 'credit': {'author': 'Mokaair', 'license': '© Mokaair'}})
        if number:
            blocks.append({'type': 'rich_paragraph', 'inlines': [{'type': 'article', 'kind': 'life', 'slug': catalogue['hub'], 'text': '回 Claude Code 教學總目錄'}]})
        # Prerequisites and the single related-reading list are rendered from live series
        # navigation. Do not duplicate them in authored blocks or expose draft targets.
        lead = next((b.get('text', '') for b in blocks if b['type'] == 'paragraph'), '')
        description = (entry['outcome'] + lead)[:190]
        pack = {'slug': entry['slug'], 'kind': 'life', 'destination_id': None, 'topics': ['ai', 'tutorial'], 'featured': False, 'display_order': 100 + number,
                'locales': {'zh-TW': {'title': 'Claude Code｜' + entry['title'] if not entry['title'].startswith('Claude') else entry['title'], 'description': description,
                'hero': {'src': f'/guides/{entry["slug"]}/hero.jpg', 'alt': entry['title'] + '：文件、螢幕與完成記號的幾何插圖', 'width': 1600, 'height': 900, 'credit': {'author': 'Mokaair', 'license': '© Mokaair'}},
                'blocks': blocks, 'sources': [{'title': checks[url]['title'], 'url': url, 'checked_on': checks[url]['checked_on']} for url in entry['sources']]}}}
        parsed = ArticlePack.model_validate(pack)
        length = _body_length(parsed.locales['zh-TW'])
        (CONTENT / (entry['slug'] + '.json')).write_text(json.dumps(pack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        report.append({'number': number, 'slug': entry['slug'], 'body_characters': length, 'blocks': len(blocks)})
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
