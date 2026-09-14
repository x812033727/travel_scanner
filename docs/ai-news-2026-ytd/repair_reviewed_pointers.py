"""Correct inspected field identifiers; never infer missing prose or accept partial documents."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE/'renders'
FIXES={
 'ai-news-chatgpt-work-20260709.ja':{'/document/blocks/11/rows/1/0':'/document/blocks/10/rows/1/0'},
 'ai-news-claude-interactive-visuals-20260312.ja':{'/document/blocks/3/0':'/document/blocks/10/rows/3/0'},
 'ai-news-claude-interactive-visuals-20260312.ko':{'/document/blocks/2/1':'/document/blocks/10/rows/2/1','/document/blocks/2/2':'/document/blocks/10/rows/2/2'},
 'ai-news-gpt-56-sol-preview-20260626.ja':{'/document/blocks/3/1':'/document/blocks/10/rows/3/1','/document/blocks/3/2':'/document/blocks/10/rows/3/2'},
 'ai-news-lyria-3-pro-20260325.ja':{'/document/blocks/3/0':'/document/blocks/8/rows/3/0'},
 'ai-news-nvidia-rubin-20260105.ko':{f'/document/blocks/{r}/{c}':f'/document/blocks/10/rows/{r}/{c}' for r in [2,3] for c in range(3)},
}
records=[]
for key,mapping in FIXES.items():
    r=json.loads((ROOT/'outputs'/f'{key}.partial.json').read_text(encoding='utf8'))
    source=json.loads((ROOT/'translation-inputs'/f'{key}.json').read_text(encoding='utf8'))
    for item in r['items']:
        if item['id'] in mapping:
            records.append({'file':key,'old_id':item['id'],'id':mapping[item['id']],'text':item['text'],'method':'Editor verified table position and translated meaning against source'})
            item['id']=mapping[item['id']]
    assert len(r['items'])==len(source['items']) and {i['id'] for i in r['items']}=={i['id'] for i in source['items']}
    (ROOT/'outputs'/f'{key}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
key='ai-news-claude-sonnet-5-20260630.ko'
r=json.loads((ROOT/'outputs'/f'{key}.partial.json').read_text(encoding='utf8'))
source=json.loads((ROOT/'translation-inputs'/f'{key}.json').read_text(encoding='utf8'))
extra=next(i for i in r['items'] if i['id']=='/document/blocks/2/2')
canonical=next(i for i in r['items'] if i['id']=='/document/blocks/10/rows/2/2')
assert extra['text']==canonical['text']
r['items']=[i for i in r['items'] if i['id']!=extra['id']]
assert len(r['items'])==len(source['items']) and {i['id'] for i in r['items']}=={i['id'] for i in source['items']}
(ROOT/'outputs'/f'{key}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
records.append({'file':key,'old_id':extra['id'],'id':canonical['id'],'method':'Removed exact duplicate of an already-present table cell after comparing both texts'})
(HERE/'translation-pointer-repairs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Repaired',len(FIXES),'inspected translation documents')
