"""Existing damage callback, a single teaching question, and exact source bindings."""
from pathlib import Path
import json,hashlib,re,csv
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'history-r11/video.json')=='fadf5da0d73e5f4d3f6b0faaa2f9a668cfb4ec0ca75bd2b48f78cbe3633c269b'
v=json.loads((P/'history-r11/video.json').read_text())
texts={'c09r034':'還記得開場那道岩縫嗎？合金鋼比花崗岩硬，薄石片還可能在敲拔時鬆動、剝落。','c09r058':'我覺得難處還在你翻完冊子以後：換一件工具，只讀前言就夠嗎？'}
old={}
for s in v['scenes']:
 for l in s['lines']:
  if l['id']in texts:old[l['id']]=l['text'];l['text']=texts[l['id']]
assert len(old)==2
found=[s for s in v['scenes']if any(l['id']=='c09r059'for l in s['lines'])];assert len(found)==1 and len(found[0]['lines'])==1
v['scenes']=[s for s in v['scenes']if s['id']!=found[0]['id']]
assert not any('c09r059'in[l['setup'],l['payoff']]for l in v['loops'])
(P/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
claims=[c for c in json.loads((P/'history-r11/claims.json').read_text())if c['id']!='c09r059']
claim_delta=[]
for c in claims:
 if c['id']in texts:c['text']=texts[c['id']]
 if c['id']=='c09r002':
  claim_delta.append({'id':c['id'],'old_source':c['source'],'old_anchor':c['anchor']})
  c['source']='S2、S4'
  c['anchor']='S2 1972前言原文：熱門路線裂縫變成成排釘孔、反覆敲拔使岩片鬆落；S4:D small cracks now needed large pitons，窄裂縫擴大需較大釘子；保留如果/可能的觀眾假設，非同孔100次'
 if c['id']=='c09r034':c['anchor']='明示回呼002的岩縫；S2合金鋼相對花崗岩硬度及敲拔使薄片鬆動/剝落，未重述擴寬結果'
 if c['id']=='c09r058':
  c['source']='S2、S3'
  c['anchor']='旁白明示意見與換工具是否只讀前言的問句；054–057完整保留路線/例外規則，060–061以型錄教學長文回答'
(P/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
projection=[];chapter=None
for s in v['scenes']:
 if s.get('chapter'):chapter=s['chapter']
 for l in s['lines']:projection.append({'chapter':chapter,'id':l['id'],'text':l['text']})
(P/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
for name in ['script.md','claims.md']:
 text=(P/'history-r11'/name).read_text();text=''.join(line for line in text.splitlines(keepends=True)if not line.startswith('| c09r059 |'))
 # Re-emit only the changed source table rows; all other rows keep their exact bytes.
 out=[]
 for line in text.splitlines(keepends=True):
  if line.startswith('| c09r002 |')or line.startswith('| c09r034 |')or line.startswith('| c09r058 |'):
   lid=line.split('|')[1].strip();c=next(c for c in claims if c['id']==lid)
   line=(f"| {lid} | {c['text']} | {c['source']}：{c['anchor']} |\n"if name=='script.md'else f"| {lid} | {c['text']} | {c['source']} | {c['anchor']} | PENDING |\n")
  out.append(line)
 (P/name).write_text(''.join(out))
with(P/'narration.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['id','chapter','source','anchor','text'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:r[k]for k in w.fieldnames}for r in claims)
notes=json.loads((P/'history-r11/author-notes.json').read_text());notes.update(revision=12,status='r12_candidate_unapproved',previous_version='history-r11',video_sha256=sha(P/'video.json'),script_sha256=sha(P/'script.md'),narration_projection_sha256=sha(P/'narration-only.json'),lines=len(claims),scenes=len(v['scenes']),illustrations=sum(s['template']=='shot'for s in v['scenes']),spoken_character_count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in claims),retained_source_hold='history-r11/source-r11-delta.json',source_delta_status='awaiting_independent_r12_closure')
notes['estimated_seconds_at_4_5_chars']=round(notes['spoken_character_count']/4.5,2)
(P/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
rep={'type':'author_bounded_recap_and_source_binding_delta','independent':False,'revision':'r12','old_video_sha256':sha(P/'history-r11/video.json'),'new_video_sha256':sha(P/'video.json'),'spoken_changes':[{'id':lid,'before':old[lid],'after':new}for lid,new in texts.items()],'deleted_line':'c09r059','deleted_scene':found[0]['id'],'claim_changes':{'c09r002':'S2 piton holes/repeated damage + S4:D widening that required larger pitons; narration unchanged','c09r034':'True callback to opening crack; retain the distinct hardness and flaking mechanism','c09r058':'Delete rule recap; consolidate the existing teaching question with explicit narrator reaction; S2/S3'},'route_support_retained':['c09r054','c09r055','c09r056','c09r057'],'loops_unchanged':True,'visuals_unchanged':True,'other_video_values_unchanged':True,'facts_added':False,'reader_handling':'Copied reader files into history-r11 only; this revision did not inspect or edit reader outputs','retained_source_hold':'history-r11/source-r11-delta.json'}
(P/'reviews/narrative-r12-author-delta.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:notes[k]for k in ['lines','scenes','illustrations','video_sha256']},ensure_ascii=False))
