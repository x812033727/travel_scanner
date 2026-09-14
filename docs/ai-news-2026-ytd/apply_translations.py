"""Preserve original structure, sources and identity when applying reviewed translations."""
import copy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
LOCALES=['zh-TW','en','ja','ko','zh-CN']
corrections=json.loads((HERE/'translation-corrections.json').read_text(encoding='utf8'))
def put(node,pointer,value):
    keys=pointer.strip('/').split('/');cursor=node
    for k in keys[:-1]:cursor=cursor[int(k)] if isinstance(cursor,list) else cursor[k]
    if isinstance(cursor,list):cursor[int(keys[-1])]=value
    else:cursor[keys[-1]]=value
packs={};usage=[]
for file in (HERE/'research').glob('*.json'):
    research=json.loads(file.read_text(encoding='utf8'));slug=research['slug']
    pack=json.loads((ROOT/'apps/api/app/guides/content'/file.name).read_text(encoding='utf8'))
    research['translations']={}
    for locale in LOCALES[1:]:
        result=json.loads((HERE/'renders/translation-outputs'/f'{slug}.{locale}.json').read_text(encoding='utf8'))
        inputs=json.loads((HERE/'renders/translation-inputs'/f'{slug}.{locale}.json').read_text(encoding='utf8'))
        assert len(result['items'])==len(inputs['items']) and {i['id'] for i in result['items']}=={i['id'] for i in inputs['items']}
        container={'document':copy.deepcopy(pack['locales']['zh-TW']),'diagram':copy.deepcopy(research['diagram']),'hero_label':''}
        for entry in result['items']:
            value=entry['text']
            for c in corrections:
                if c['slug']==slug and c['locale']==locale and c['id']==entry['id']:value=c['text']
            put(container,entry['id'],value)
        doc=container['document'];doc['hero']['src']=f'/guides/{slug}/hero-{locale.lower()}.jpg'
        for block in doc['blocks']:
            if block['type']=='image':block['src']=f'/guides/{slug}/diagram-1-{locale.lower()}.svg'
        pack['locales'][locale]=doc
        research['translations'][locale]={'diagram':container['diagram'],'hero_label':container['hero_label']}
        usage.append({'slug':slug,'locale':locale,'model':result['model'],'fields':len(result['items']),**result['usage']})
    file.write_text(json.dumps(research,ensure_ascii=False,indent=2)+'\n',encoding='utf8');packs[slug]=pack
for slug,pack in packs.items():
    for locale,doc in pack['locales'].items():
        for block in doc['blocks']:
            if block['type']!='link':continue
            target=block['url'].rsplit('/',1)[-1]
            other=packs.get(target) or json.loads((ROOT/'apps/api/app/guides/content'/f'{target}.json').read_text(encoding='utf8'))
            assert locale in other['locales']
            block['text']=other['locales'][locale]['title'];block['url']=f'https://mokaair.com/{locale}/life/{target}'
    (ROOT/'apps/api/app/guides/content'/f'{slug}.json').write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'translation-report.json').write_text(json.dumps({'method':'Existing configured Gemini provider; exact-field translations of reviewed originals, separately checked for fidelity','translations':usage},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Assembled 110 locale documents with matching-language links')
