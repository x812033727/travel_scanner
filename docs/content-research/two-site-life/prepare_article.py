"""Package individually authored draft.json files and original vector artwork.

This tool provides layout/serialization only. It never expands or pads prose.
The existing guides.pack_cli ingest remains the only route into shipped packs.
"""
import argparse
import html
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESEARCH = Path(__file__).resolve().parent
WORK = ROOT / '.codex/two-site-life/work'


def svg_start(title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="'Noto Sans TC','Microsoft JhengHei',sans-serif">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>
<rect width="1600" height="900" fill="#F7F1E8"/>
'''


def label(x, y, text, size=36, color='#102A2B', anchor='start', weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(text)}</text>\n'


def rect(x, y, w, h, fill='#FFFFFF', stroke='#0D6B68', radius=24):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>\n'


def diagram(draft):
    spec = draft['diagram']
    out = svg_start(spec['title'], spec['description'])
    out += label(80, 94, spec['title'], 52, weight='bold')
    out += label(80, 151, spec['subtitle'], 28, '#5C6B6B')
    nodes = spec['nodes']
    assert 3 <= len(nodes) <= 6
    if len(nodes) <= 4:
        w = (1440 - (len(nodes) - 1) * 36) / len(nodes)
        positions = [(80 + i * (w + 36), 256, w, 400) for i in range(len(nodes))]
    else:
        positions = [(80 + (i % 3) * 490, 224 + (i // 3) * 260, 458, 218) for i in range(len(nodes))]
    for i, (node, (x, y, w, h)) in enumerate(zip(nodes, positions, strict=True)):
        out += rect(x, y, w, h, '#E3F0EF' if i % 2 == 0 else '#E6F0F7')
        out += label(x + 28, y + 58, node['label'], 38, weight='bold')
        for j, line in enumerate(node['lines']):
            assert len(line) <= 16, line
            out += label(x + 28, y + 115 + j * 52, line, 32)
    out += label(80, 803, spec['takeaway'], 32)
    out += label(1520, 862, 'Mokaair 原創製圖', 24, '#5C6B6B', 'end')
    return out + '</svg>\n'


def hero(draft):
    spec = draft['hero_art']
    out = svg_start(spec['label'], spec['alt'])
    # Original geometric illustrations; semantic symbols and arrangement are authored per article.
    out += '<circle cx="1280" cy="210" r="130" fill="#E3F0EF"/><circle cx="230" cy="700" r="110" fill="#E6F0F7"/>\n'
    color = spec.get('color', '#0D6B68')
    for i, icon in enumerate(spec['icons']):
        x = 110 + i * 500
        out += rect(x, 230, 380, 370, '#FFFFFF', color, 32)
        if icon == 'document':
            out += rect(x + 75, 280, 230, 265, '#E3F0EF', color, 12)
            for j, width in enumerate([150, 170, 120, 155]):
                out += f'<path d="M{x+108} {335+j*46}h{width}" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
        elif icon == 'server':
            for j in range(3):
                out += rect(x + 50, 283 + j * 89, 280, 64, '#E6F0F7', color, 12)
                out += f'<circle cx="{x+91}" cy="{315+j*89}" r="10" fill="#D97A2B"/>'
        elif icon == 'screen':
            out += rect(x + 40, 286, 300, 205, '#E6F0F7', color, 12)
            out += f'<path d="M{x+190} 493v52m-65 0h130" stroke="{color}" stroke-width="14" stroke-linecap="round"/>'
            out += rect(x + 65, 315, 90, 150, '#E3F0EF', color, 6)
            out += rect(x + 182, 315, 130, 50, '#FFFFFF', color, 6)
        elif icon == 'shield':
            out += f'<path d="M{x+190} 275L{x+310} 325v85q0 94-120 144q-120-50-120-144v-85Z" fill="#E3F0EF" stroke="{color}" stroke-width="8"/><path d="M{x+130} 410l43 43l82-90" fill="none" stroke="{color}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
        elif icon == 'budget':
            out += rect(x + 83, 272, 214, 284, '#E3F0EF', color, 18)
            out += rect(x + 105, 295, 170, 53, '#FFFFFF', color, 5)
            for r in range(3):
                for c in range(3):
                    out += rect(x + 108 + c * 59, 377 + r * 52, 36, 32, '#D97A2B' if c == 2 else '#FFFFFF', color, 5)
        elif icon == 'folder':
            out += f'<path d="M{x+45} 333v-43h110l35 43h145v206h-290Z" fill="#E3F0EF" stroke="{color}" stroke-width="8"/>'
            out += rect(x + 90, 368, 200, 120, '#FFFFFF', color, 8)
        else:
            raise ValueError(f'Unknown authored icon: {icon}')
        if i < len(spec['icons']) - 1:
            out += f'<path d="M{x+407} 418h60m-18-17l18 17l-18 17" fill="none" stroke="#D97A2B" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    out += label(800, 746, spec['label'], 64, color, 'middle', 'bold')
    return out + '</svg>\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slug')
    args = parser.parse_args()
    target = WORK / args.slug
    draft = json.loads((target / 'draft.json').read_text(encoding='utf-8'))
    assignments = json.loads((RESEARCH / 'catalogue.json').read_text(encoding='utf-8'))['articles']
    assignment = next(a for a in assignments if a['slug'] == args.slug)
    blocks = [{'type': 'paragraph', 'text': p} for p in draft['intro']]
    for section in draft['sections']:
        blocks.append({'type': 'heading', 'level': 2, 'text': section['title']})
        blocks.extend({'type': 'paragraph', 'text': p} for p in section['paragraphs'])
        if section.get('steps'):
            blocks.append({'type': 'list', 'ordered': True, 'items': section['steps']})
    blocks += [{'type': 'image', 'src': f'/guides/{args.slug}/diagram-1.svg', 'alt': draft['diagram']['description'],
                'width': 1600, 'height': 900, 'caption': draft['diagram']['takeaway']},
               {'type': 'table', **draft['table']}, {'type': 'callout', 'tone': 'tip', **draft['callout']}]
    for link in draft.get('links', [{'text': '閱讀更多生活分享', 'url': 'https://mokaair.com/zh-TW/life'}]):
        blocks.append({'type': 'link', **link})
    text = ''.join(b['text'] if b['type'] in ('paragraph', 'callout') else ''.join(b['items']) if b['type'] == 'list' else '' for b in blocks)
    length = len(re.sub(r'\s+', '', text))
    if not 1800 <= length <= 3000:
        raise ValueError(f'{args.slug}: authored body is {length} characters, expected 1800–3000 (no automatic padding)')
    assert 120 <= len(draft['description']) <= 200, len(draft['description'])
    assert all(s.get('checked_on') for s in draft['sources'])
    doc = {'title': assignment['title'], 'description': draft['description'],
           'hero': {'src': f'/guides/{args.slug}/hero.jpg', 'alt': draft['hero_art']['alt'], 'width': 1600, 'height': 900},
           'blocks': blocks, 'sources': draft['sources']}
    pack = {'slug': args.slug, 'kind': 'life', 'destination_id': None, 'topics': assignment['topics'],
            'featured': False, 'display_order': 100, 'locales': {'zh-TW': doc}}
    (target / 'pack.json').write_text(json.dumps(pack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (target / 'diagram-1.svg').write_text(diagram(draft), encoding='utf-8')
    (target / 'hero.svg').write_text(hero(draft), encoding='utf-8')
    notes = ['# ' + assignment['title'] + '：查證與編輯紀錄', '', f'正文非空白字數（排除標題、表格）：{length}', '',
             '來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。', '',
             '## 主張與來源', '', *draft['notes'], '', '## 配圖', '', '封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。', '']
    (target / 'notes.md').write_text('\n'.join(notes), encoding='utf-8')
    research_notes = RESEARCH / 'notes'
    research_notes.mkdir(exist_ok=True)
    (research_notes / f'{args.slug}.md').write_text('\n'.join(notes), encoding='utf-8')
    print(f'{args.slug}: {length} authored characters; pack and two original SVGs prepared')


if __name__ == '__main__':
    main()
