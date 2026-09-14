"""Extract every translatable field without passing filenames or runtime secrets to the model."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'renders/translation-inputs'
OUT.mkdir(exist_ok=True)
LABELS=['工作交接','用量與帳單','清楚標示來源','回答之前先想清楚','用語音整理一天','能力與存取資格','模型到日常工具','交付電腦工作','把想法變成音樂','保留重點再修改']
SKIP={'url','src','author','license','source_url','checked_on','type','tone'}
def strings(node,prefix=''):
    result=[]
    if isinstance(node,dict):
        for k,v in node.items():
            if k not in SKIP: result+=strings(v,prefix+'/'+k)
    elif isinstance(node,list):
        for i,v in enumerate(node):result+=strings(v,prefix+'/'+str(i))
    elif isinstance(node,str) and node:result.append({'id':prefix,'text':node})
    return result
for file in (HERE/'research').glob('*.json'):
    research=json.loads(file.read_text(encoding='utf-8'))
    pack=json.loads((ROOT/'apps/api/app/guides/content'/file.name).read_text(encoding='utf-8'))
    items=strings(pack['locales']['zh-TW'],'/document')+strings(research['diagram'],'/diagram')
    items.append({'id':'/hero_label','text':LABELS[research['hero_style']]})
    for locale in ['en','ja','ko','zh-CN']:
        (OUT/(research['slug']+'.'+locale+'.json')).write_text(json.dumps({'slug':research['slug'],'target_locale':locale,'items':items},ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared 40 exact-field translation inputs')
