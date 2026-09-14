"""Repair two inspected index field-mapping failures without accepting omitted content."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;root=HERE/'renders';slug='ai-news-2026-january-september-index'
repairs=[]
for locale in ['en','ja']:
    file=root/'outputs'/f'{slug}.{locale}.partial.json';result=json.loads(file.read_text(encoding='utf8'))
    source=json.loads((root/'translation-inputs'/f'{slug}.{locale}.json').read_text(encoding='utf8'))
    if locale=='en':
        for entry in result['items']:
            for i in range(3):
                if entry['id']==f'/document/blocks/2/{i}':
                    entry['id']=f'/document/blocks/9/rows/2/{i}'
                    repairs.append({'slug':slug,'locale':locale,'id':entry['id'],'method':'Corrected inspected March table row pointer; English content exactly matches source'})
    else:
        result['items']=[i for i in result['items'] if i['id']!='/document/blocks/66/text']
        result['items'].append({'id':'/document/blocks/25/text','text':'本特集の対象は2026-09-14までです。発表時のモデル、料金、提供対象は、現在のアカウントの状態と一致するとは限りません。本文のその後の更新情報と公式情報源も併せて確認してください。'})
        repairs.append({'slug':slug,'locale':locale,'id':'/document/blocks/25/text','method':'Removed extra duplicate article-link field; editor translated omitted reminder in full'})
    assert len(result['items'])==len(source['items']) and {i['id'] for i in result['items']}=={i['id'] for i in source['items']}
    (root/'outputs'/f'{slug}.{locale}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'translation-field-repairs.json').write_text(json.dumps(repairs,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Repaired and checked 2 index translation outputs')
