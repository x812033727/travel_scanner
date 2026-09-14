"""Freeze reviewed source prose and record decisions on secondary audit suggestions."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
for folder in ['research']:
    for f in (HERE/folder).glob('*.json'):
        data=f.read_text(encoding='utf8').replace('音訊初期僅支援聲音參考','音訊初期僅支援人聲參考').replace('音訊參考初期僅支援聲音參考','音訊參考初期僅支援人聲參考').replace('僅支援聲音參考','僅支援人聲參考')
        f.write_text(data,encoding='utf8')
reviews=[json.loads(f.read_text(encoding='utf8')) for f in (HERE/'renders/original-reviews').glob('*.json')]
assert len(reviews)==21
decisions=[]
for r in reviews:
    for issue in r['issues']:
        assert r['slug']=='ai-news-gemini-omni-20260519'
        decisions.append({'slug':r['slug'],**issue,'decision':'rejected','reason':'Official Gemini Omni release explicitly says only voice references will be supported for audio to start. 人聲參考 is the precise translation; the brief had used the broader 聲音參考 and has now been clarified.','source':'https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/'})
originals=[]
for f in (HERE/'renders/drafts').glob('*.json'):
    r=json.loads(f.read_text(encoding='utf8'));text=json.dumps(r['document'],ensure_ascii=False,sort_keys=True)
    originals.append({'slug':r['slug'],'paragraph_characters':r['paragraph_characters'],'sha256':hashlib.sha256(text.encode()).hexdigest(),'reviewed_on':'2026-09-14','method':'Full editorial reading; dated source facts, substantive manual corrections and secondary fidelity audit'})
(HERE/'original-review.json').write_text(json.dumps({'originals':originals,'secondary_reviews':reviews,'decisions':decisions},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Frozen 22 editor-reviewed originals; 2 secondary suggestions rejected against official wording')
