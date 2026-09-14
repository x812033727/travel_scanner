"""Assemble reviewed originals and deterministic metadata; no publication."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
INDEX='ai-news-2026-january-september-index'
LOCALES=['zh-TW','en','ja','ko','zh-CN']
credit={'author':'Mokaair','license':'© Mokaair','source_url':None}
items=sorted([json.loads(f.read_text(encoding='utf8')) for f in (HERE/'research').glob('*.json')],key=lambda x:(x['event_date'],x['slug']))
old=json.loads((HERE.parent/'ai-news-2026-09/manifest.json').read_text(encoding='utf8'))
news=sorted([i for i in items if i['slug']!=INDEX]+old,key=lambda x:(x['event_date'],x['slug']))
assert len(items)==22 and len(news)==31
for order,item in enumerate(items):
    slug=item['slug'];result=json.loads((HERE/'renders/drafts'/f'{slug}.json').read_text(encoding='utf8'))
    d=result['document'];blocks=[]
    for text in d['introduction']:blocks.append({'type':'paragraph','text':text})
    for i,section in enumerate(d['sections']):
        blocks.append({'type':'heading','level':2,'text':section['heading']})
        blocks.extend({'type':'paragraph','text':p} for p in section['paragraphs'])
        if i==1:blocks.append({'type':'table','header':d['table_header'],'rows':d['table_rows'],'caption':d['table_caption']})
        if i==2:blocks.append({'type':'image','src':f'/guides/{slug}/diagram-1.svg','alt':item['hero_label']+'：四項閱讀與使用重點','width':1600,'height':900,'caption':'、'.join(h+'：'+v for h,v in item['diagram_nodes'])+'。','credit':credit})
    blocks.append({'type':'callout','tone':'info','title':d['callout_title'],'text':d['callout_text']})
    if slug==INDEX:
        for month in range(1,10):
            blocks.append({'type':'heading','level':2,'text':f'2026 年 {month} 月新聞解析'})
            for n in news:
                if int(n['event_date'][5:7])==month:blocks.append({'type':'link','text':n['title'],'url':f"https://mokaair.com/zh-TW/life/{n['slug']}"})
    else:
        ix=next(i for i,n in enumerate(news) if n['slug']==slug)
        related=news[min(ix+1,len(news)-1)]
        blocks.extend([{'type':'link','text':next(i['title'] for i in items if i['slug']==INDEX),'url':f'https://mokaair.com/zh-TW/life/{INDEX}'},
            {'type':'link','text':related['title'],'url':f"https://mokaair.com/zh-TW/life/{related['slug']}"}])
    doc={'title':item['title'],'description':d['description'],'hero':{'src':f'/guides/{slug}/hero.jpg','alt':item['hero_label']+'的原創概念插圖，呈現本篇事件的使用脈絡','width':1600,'height':900,'credit':credit},'blocks':blocks,'sources':item['sources']}
    pack={'slug':slug,'kind':'life','destination_id':None,'topics':['ai','software'],'valid_until':None,'featured':False,'display_order':120+order,'locales':{'zh-TW':doc}}
    (ROOT/'apps/api/app/guides/content'/f'{slug}.json').write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    item['diagram']={'title':item['hero_label'],'caption':'、'.join(h+'：'+v for h,v in item['diagram_nodes'])+'。','nodes':item['diagram_nodes']}
    (HERE/'research'/f'{slug}.json').write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Assembled 22 originals, including chronological index')
