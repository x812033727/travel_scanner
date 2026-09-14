"""Render a self-contained editorial index from the same JSON shipped for import."""
from pathlib import Path
from html import escape as e
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
rows=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
slugs={r['slug'] for r in rows}
def asset(src): return '../../apps/web/public'+src
def photo(b):
    credit=b.get('credit',{})
    return f'<figure><img loading="lazy" src="{e(asset(b["src"]))}" width="{b["width"]}" height="{b["height"]}" alt="{e(b["alt"])}"><figcaption>{e(b.get("caption", ""))} {e(credit.get("author", ""))} · {e(credit.get("license", ""))}</figcaption></figure>'
def block(b):
    t=b['type']
    if t=='paragraph': return f'<p>{e(b["text"])}</p>'
    if t=='heading': return f'<h2>{e(b["text"])}</h2>'
    if t=='list':
        tag='ol' if b['ordered'] else 'ul'
        return f'<{tag}>'+''.join(f'<li>{e(s)}</li>' for s in b['items'])+f'</{tag}>'
    if t=='table':
        return '<div class="table-wrap"><table><caption>'+e(b.get('caption',''))+'</caption><thead><tr>'+''.join(f'<th>{e(s)}</th>' for s in b['header'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{e(c)}</td>' for c in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
    if t=='callout': return f'<aside><strong>{e(b["title"])}</strong><p>{e(b["text"])}</p></aside>'
    if t=='image': return photo(b)
    if t=='link':
        slug=b['url'].rstrip('/').split('/')[-1]
        url='#'+slug if slug in slugs else b['url']
        return f'<p class="related"><a href="{e(url)}">延伸閱讀：{e(b["text"])}</a></p>'
    if t=='offer': return '<aside class="offer">'+e(b['heading'])+'<p>合作活動區塊的位置預覽；實際選項依網站供應狀態顯示。</p></aside>'
    raise ValueError(t)
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f7f5ef;color:#243a39;font-family:"Microsoft JhengHei",system-ui,sans-serif;line-height:1.8}a{color:#176967;text-underline-offset:4px}header{background:#153e40;color:#fff;padding:64px max(24px,calc((100vw - 1160px)/2))}header h1{font-size:clamp(30px,4vw,52px);line-height:1.3;margin:10px 0 18px}header p{max-width:760px;color:#d3e2dd}main{max-width:1208px;padding:32px 24px;margin:auto}.tag{font-size:13px;letter-spacing:2px;color:#efce8a}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}.card{display:block;text-decoration:none;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 3px 15px #153e4010}.card img{width:100%;height:auto;display:block;aspect-ratio:16/9}.card div{padding:18px}.card h3{font-size:19px;line-height:1.6;margin:4px 0}.card span{font-size:13px;color:#8e533d}.section-title{margin:42px 0 20px;font-size:26px}article{max-width:860px;margin:70px auto;padding:36px;background:white;border-radius:20px;scroll-margin-top:20px}article h1{font-size:32px;line-height:1.55;margin:8px 0}article h2{font-size:23px;margin-top:34px;line-height:1.6}.dek{font-size:18px;color:#536f6b}figure{margin:28px 0}figure img{display:block;width:100%;height:auto;border-radius:12px}figcaption{font-size:12px;line-height:1.7;color:#697772;margin-top:8px}.table-wrap{overflow-x:auto;margin:20px 0}table{border-collapse:collapse;width:100%;font-size:15px;min-width:530px}th,td{border:1px solid #dfe5de;padding:12px;text-align:left;vertical-align:top}th{background:#edf2eb}caption{text-align:left;font-size:13px;margin-bottom:8px;color:#61746e}aside{padding:18px 22px;background:#eff4e9;border-left:4px solid #79945c;border-radius:6px;margin:24px 0}aside p{margin:8px 0 0}.offer{background:#faf1e6;border-color:#c08d52}.sources{font-size:14px;border-top:1px solid #dfe5de;margin-top:30px;padding-top:14px}.sources li{margin:10px 0}.back{font-size:14px}.related{padding-top:12px}footer{text-align:center;padding:40px;color:#60736c}@media(max-width:720px){header{padding:40px 20px}.grid{grid-template-columns:1fr}main{padding:20px 14px}article{padding:22px 18px;margin:40px auto}article h1{font-size:25px}article h2{font-size:21px}.dek{font-size:16px}p,li{overflow-wrap:anywhere}figure{margin:22px 0}}'''
parts=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>30 篇旅遊與生活分享｜Mokaair 第五批內容預覽</title><style>'+css+'</style><header id="top"><div class="tag">MOKAAIR · EDITORIAL COLLECTION 05</div><h1>把旅途安排好，也把日常過得更順</h1><p>15 篇旅遊實用攻略 × 15 篇生活分享。每篇配有原創 AI 示意插畫與編輯流程圖；參考資料查核日為 2026 年 9 月 14 日。</p><p>本頁為內容預覽，尚未發布至正式網站。</p></header><main>']
for kind,label in [('howto','旅遊情報與實用攻略'),('life','生活分享與整理方法')]:
    parts.append(f'<h2 class="section-title">{label} · 15 篇</h2><div class="grid">')
    for r in rows:
        if r['kind']!=kind: continue
        d=json.loads((ROOT/'apps/api/app/guides/content'/f'{r["slug"]}.json').read_text(encoding='utf-8'))['locales']['zh-TW']
        parts.append(f'<a class="card" href="#{r["slug"]}"><img loading="lazy" src="{asset(d["hero"]["src"])}" width="1600" height="900" alt="{e(d["hero"]["alt"])}"><div><span>{label}</span><h3>{e(d["title"])}</h3></div></a>')
    parts.append('</div>')
for r in rows:
    d=json.loads((ROOT/'apps/api/app/guides/content'/f'{r["slug"]}.json').read_text(encoding='utf-8'))['locales']['zh-TW']
    parts.append(f'<article id="{r["slug"]}"><a class="back" href="#top">↑ 回到文章目錄</a><h1>{e(d["title"])}</h1><p class="dek">{e(d["description"])}</p>'+photo(d['hero']))
    parts += [block(b) for b in d['blocks']]
    parts.append('<section class="sources"><h2>資料來源</h2><ul>'+''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])}</a> · 查核 {s["checked_on"]}</li>' for s in d['sources'])+'</ul></section></article>')
parts.append('</main><footer>Mokaair · 原創內容預覽 · 圖片為示意，並非實地攝影</footer></html>')
(HERE/'index.html').write_text(''.join(parts),encoding='utf-8')
diagrams=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>30 篇自製流程圖檢視</title><style>body{background:#eee;font-family:sans-serif}main{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}figure{margin:0;background:white}img{width:100%;display:block}figcaption{padding:8px}</style><main>']
for r in rows:
    diagrams.append(f'<figure><img src="{asset("/guides/"+r["slug"]+"/diagram-1.svg")}"><figcaption>{e(r["title"])}</figcaption></figure>')
diagrams.append('</main></html>')
(HERE/'diagrams.html').write_text(''.join(diagrams),encoding='utf-8')
print('Built full 30-article preview and diagram review sheet')
