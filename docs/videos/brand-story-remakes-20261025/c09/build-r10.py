"""Two actual-object callbacks only, from the exact retained r9 input."""
from pathlib import Path
import json,hashlib,re,csv
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'history-r9/video.json')=='edfebcb001483e53bb312d0369d2f5e4fd5a6357ca36130819c08b5957b80999'
v=json.loads((P/'history-r9/video.json').read_text())
texts={'c09r047':'回到開場那本型錄，他們給的建議是：在合適路線上，','c09r102':'回到剛才那部壓床，這段紀錄的答案是：建議的次序改了，商品卻仍在；賣工具的人，也開始追問你該不該用它。'}
old={}
for s in v['scenes']:
 for l in s['lines']:
  if l['id']in texts:old[l['id']]=l['text'];l['text']=texts[l['id']]
assert len(old)==2
(P/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
claims=json.loads((P/'history-r9/claims.json').read_text())
for c in claims:
 if c['id']in texts:c['text']=texts[c['id']]
(P/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
projection=[];chapter=None
for s in v['scenes']:
 if s.get('chapter'):chapter=s['chapter']
 for l in s['lines']:projection.append({'chapter':chapter,'id':l['id'],'text':l['text']})
(P/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
for name in ['script.md','claims.md']:
 text=(P/'history-r9'/name).read_text()
 for lid,new in texts.items():assert text.count(old[lid])==1;text=text.replace(old[lid],new)
 (P/name).write_text(text)
with(P/'narration.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['id','chapter','source','anchor','text'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:r[k]for k in w.fieldnames}for r in claims)
notes=json.loads((P/'history-r9/author-notes.json').read_text())
notes.update(revision=10,status='r10_candidate_unapproved',previous_version='history-r9',video_sha256=sha(P/'video.json'),script_sha256=sha(P/'script.md'),narration_projection_sha256=sha(P/'narration-only.json'),spoken_character_count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in claims),retained_source_pass='history-r9/source-r9-delta.json',source_delta_status='awaiting_independent_r10_callback_closure')
notes['estimated_seconds_at_4_5_chars']=round(notes['spoken_character_count']/4.5,2)
(P/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
report={'type':'author_object_callback_delta','independent':False,'revision':'r10','old_video_sha256':sha(P/'history-r9/video.json'),'new_video_sha256':sha(P/'video.json'),'changes':[{'id':lid,'before':old[lid],'after':new}for lid,new in texts.items()],'callback_targets':{'c09r047':'opening product catalogue at c09r004; c09r048 keeps its new chock-priority information','c09r102':'the operating press actually making new pitons at c09r089'},'other_video_values_unchanged':True,'loops_unchanged':True,'visuals_unchanged':True,'source_labels_unchanged':True,'facts_added':False,'retained_readers':['history-r9/reader-a.json','history-r9/reader-b.json'],'retained_source_pass':'history-r9/source-r9-delta.json','note':'No overnight withdrawal story, continuous supply assertion or financial cause is added.'}
(P/'reviews/narrative-r10-author-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('rebuilt r10: 2 callback strings only')
