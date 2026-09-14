"""Rebuild only batch-five editorial packs; no database or network writes."""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'apps/api/app/guides/content'
ART = ROOT / 'apps/web/public/guides'
ENTRIES = []

def h(text): return {'type': 'heading', 'level': 2, 'text': text}
def p(text): return {'type': 'paragraph', 'text': text}
def li(*items): return {'type': 'list', 'ordered': False, 'items': list(items)}
def table(header, rows, caption=''): return {'type': 'table', 'header': header, 'rows': rows, 'caption': caption}
def tip(title, text): return {'type': 'callout', 'tone': 'tip', 'title': title, 'text': text}
def link(title, slug, kind='howto'):
    path = f'life/{slug}' if kind == 'life' else f'guides/{kind}/{slug}'
    return {'type': 'link', 'text': title, 'url': f'https://mokaair.com/zh-TW/{path}'}
def source(title, url): return {'title': title, 'url': url, 'checked_on': '2026-09-14'}

def write(slug, title, description, destination, topics, blocks, sources, steps, kind='howto', alt=''):
    from travel_scenarios import SCENARIOS
    if slug in SCENARIOS:
        heading, paragraphs = SCENARIOS[slug]
        at = next((i for i, block in enumerate(blocks) if block['type'] == 'callout'), len(blocks))
        blocks[at:at] = [h(heading), *[p(text) for text in paragraphs]]
    folder = ART / slug
    folder.mkdir(parents=True, exist_ok=True)
    # These diagrams express editorial decisions, not geographic routes or journey times.
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
           f'<title>{escape(title)}：判斷流程</title><desc>依序檢查：{escape("、".join(s[0] for s in steps))}。編輯整理，非地圖或實測時間。</desc>',
           '<rect width="1600" height="900" rx="36" fill="#f4f0e5"/>',
           '<g font-family="Noto Sans TC,Microsoft JhengHei,Arial,sans-serif">',
           '<text x="100" y="118" fill="#154e50" font-size="42" font-weight="700">先後順序 · A practical sequence</text>',
           '<text x="100" y="175" fill="#576968" font-size="25">依你的條件取捨，不必一次全部完成</text>']
    for i, (zh, en, detail) in enumerate(steps):
        x=75+i*370
        svg.extend([f'<rect x="{x}" y="280" width="340" height="380" rx="26" fill="{["#154e50", "#315f61", "#9b543d", "#69663d"][i]}"/>',
                    f'<text x="{x+28}" y="351" fill="#f4dc9d" font-size="34">{i+1:02d}</text>',
                    f'<text x="{x+28}" y="436" fill="white" font-size="33" font-weight="700">{escape(zh)}</text>',
                    f'<text x="{x+28}" y="497" fill="#f4f0e5" font-size="23">{escape(en)}</text>',
                    f'<text x="{x+28}" y="573" fill="#f4dc9d" font-size="26">{escape(detail)}</text>'])
    svg.append('<text x="100" y="780" fill="#576968" font-size="26">Mokaair · 編輯自製示意 / Editorial diagram</text></g></svg>')
    (folder/'diagram-1.svg').write_text(''.join(svg),encoding='utf-8')
    image={'type':'image','src':f'/guides/{slug}/diagram-1.svg','alt':'四步驟流程：'+ '、'.join(s[0] for s in steps),
           'width':1600,'height':900,'caption':'編輯建議的處理順序；示意圖不代表地理距離、服務保證或效果實測。',
           'credit':{'author':'Mokaair','license':'© Mokaair'}}
    # Put the diagram after the first substantive section, before the second heading.
    at=next((i for i,b in enumerate(blocks) if i>1 and b['type']=='heading'),len(blocks))
    blocks.insert(at,image)
    doc={'title':title,'description':description,
         'hero':{'src':f'/guides/{slug}/hero.jpg','width':1600,'height':900,
                 'alt':alt+'（AI 生成示意插畫，非實拍）',
                 'credit':{'author':'Mokaair · AI 生成示意圖','license':'AI 生成，非實拍'}},
         'blocks':blocks,'sources':sources}
    pack={'slug':slug,'kind':kind,'destination_id':destination,'topics':topics,'featured':False,'display_order':100,'locales':{'zh-TW':doc}}
    (OUT/f'{slug}.json').write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    ENTRIES.append({'slug':slug,'kind':kind,'title':title,'sources':sources})

if __name__=='__main__':
    import runpy
    for name in ['travel_a.py','travel_b.py','travel_c.py','life_a.py','life_b.py','life_c.py']:
        runpy.run_path(str(Path(__file__).with_name(name)),init_globals=globals())
    Path(__file__).with_name('manifest.json').write_text(json.dumps(ENTRIES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(ENTRIES)} batch-five articles')
