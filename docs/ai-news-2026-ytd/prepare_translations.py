"""Extract all prose and illustration labels for exact-field translation."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=HERE/'renders/translation-inputs';OUT.mkdir(parents=True,exist_ok=True)
SKIP={'url','src','author','license','source_url','checked_on','type','tone'}
def strings(node,prefix=''):
    if isinstance(node,dict):return [v for k,n in node.items() if k not in SKIP for v in strings(n,prefix+'/'+k)]
    if isinstance(node,list):return [v for i,n in enumerate(node) for v in strings(n,prefix+'/'+str(i))]
    return [{'id':prefix,'text':node}] if isinstance(node,str) and node else []
for file in (HERE/'research').glob('*.json'):
    research=json.loads(file.read_text(encoding='utf8'));pack=json.loads((ROOT/'apps/api/app/guides/content'/file.name).read_text(encoding='utf8'))
    items=strings(pack['locales']['zh-TW'],'/document')+strings(research['diagram'],'/diagram')+[{'id':'/hero_label','text':research['hero_label']}]
    for locale in ['en','ja','ko','zh-CN']:(OUT/(research['slug']+'.'+locale+'.json')).write_text(json.dumps({'slug':research['slug'],'target_locale':locale,'items':items},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Prepared 88 translation inputs')
