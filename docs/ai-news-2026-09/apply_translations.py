"""Assemble checked translations while preserving all non-text fields and article identity."""
import copy
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LOCALES=['zh-TW','en','ja','ko','zh-CN']
PAIRS=[(5,7),(3,6),(9,8),(1,7),(6,7),(0,7),(4,1),(5,3),(9,2),(8,2)]
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
corrections=json.loads((HERE/'translation-corrections.json').read_text(encoding='utf-8'))
def put(container,pointer,value):
    parts=pointer.strip('/').split('/')
    cursor=container
    for key in parts[:-1]:cursor=cursor[int(key)] if isinstance(cursor,list) else cursor[key]
    if isinstance(cursor,list):cursor[int(parts[-1])]=value
    else:cursor[parts[-1]]=value
packs={}
usage=[]
for item in manifest:
    slug=item['slug']
    file=ROOT/'apps/api/app/guides/content'/f'{slug}.json'
    pack=json.loads(file.read_text(encoding='utf-8'))
    research_file=HERE/'research'/f'{slug}.json'
    research=json.loads(research_file.read_text(encoding='utf-8'))
    research['translations']={}
    for locale in LOCALES[1:]:
        result=json.loads((HERE/'renders/translation-outputs'/f'{slug}.{locale}.json').read_text(encoding='utf-8'))
        inputs=json.loads((HERE/'renders/translation-inputs'/f'{slug}.{locale}.json').read_text(encoding='utf-8'))
        assert len(result['items'])==len(inputs['items'])
        assert {i['id'] for i in result['items']}=={i['id'] for i in inputs['items']}
        container={'document':copy.deepcopy(pack['locales']['zh-TW']),'diagram':copy.deepcopy(research['diagram']),'hero_label':''}
        for entry in result['items']:
            value=entry['text']
            for correction in corrections:
                if correction['slug']==slug and correction['locale']==locale and correction['id']==entry['id']:
                    if 'text' in correction:value=correction['text']
                    else:
                        assert correction['find'] in value
                        value=value.replace(correction['find'],correction['replace'])
            put(container,entry['id'],value)
        doc=container['document']
        doc['hero']['src']=f'/guides/{slug}/hero-{locale.lower()}.jpg'
        for block in doc['blocks']:
            if block['type']=='image':block['src']=f'/guides/{slug}/diagram-1-{locale.lower()}.svg'
        pack['locales'][locale]=doc
        research['translations'][locale]={'diagram':container['diagram'],'hero_label':container['hero_label']}
        usage.append({'slug':slug,'locale':locale,'model':result['model'],'fields':len(result['items']),**result['usage']})
    assert set(pack['locales'])==set(LOCALES)
    packs[slug]=pack
    research_file.write_text(json.dumps(research,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for index,item in enumerate(manifest):
    pack=packs[item['slug']]
    for locale in LOCALES[1:]:
        links=[b for b in pack['locales'][locale]['blocks'] if b['type']=='link']
        assert len(links)==2
        for block,other_index in zip(links,PAIRS[index]):
            target=manifest[other_index]['slug']
            block['text']=packs[target]['locales'][locale]['title']
            block['url']=f'https://mokaair.com/{locale}/life/{target}'
    (ROOT/'apps/api/app/guides/content'/f"{item['slug']}.json").write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'translation-report.json').write_text(json.dumps({'method':'Existing configured Gemini translation provider; exact-field translation of reviewed source copy','translations':usage},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Assembled 10 articles in all 5 locales (50 documents)')
