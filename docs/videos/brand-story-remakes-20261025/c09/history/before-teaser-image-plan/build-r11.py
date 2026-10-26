"""Direct the existing stakes and real payoff; remove one already-answered question."""
from pathlib import Path
import json,hashlib,re,csv
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'history-r10/video.json')=='98fb3119aa800e7c8dcce06075601cedcfa108f3a3a42b880ebb80b23317a818'
v=json.loads((P/'history-r10/video.json').read_text())
texts={'c09r002':'如果下一個爬同一道裂縫的人是你，他們帶走釘子，卻可能把越敲越寬的釘孔留給你。','c09r079':'開場那次不帶岩釘的攀登，說的就是這裡：同年，修納德和夥伴帶著楔塊，去爬酋長岩一條著名長路線。','c09r098':'這是他的估算，還不是一份獨立財報。'}
old={}
for s in v['scenes']:
 for l in s['lines']:
  if l['id']in texts:old[l['id']]=l['text'];l['text']=texts[l['id']]
assert len(old)==3
found=[s for s in v['scenes']if any(l['id']=='c09r099'for l in s['lines'])];assert len(found)==1 and len(found[0]['lines'])==1
v['scenes']=[s for s in v['scenes']if s['id']!=found[0]['id']]
removed_loops=[l for l in v['loops']if l['setup']=='c09r098'];assert len(removed_loops)==1 and removed_loops[0]['payoff']=='c09r102'
v['loops']=[l for l in v['loops']if l['setup']!='c09r098']
assert not any('c09r099'in[l['setup'],l['payoff']]for l in v['loops'])
(P/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
claims=[c for c in json.loads((P/'history-r10/claims.json').read_text())if c['id']!='c09r099']
for c in claims:
 if c['id']in texts:c['text']=texts[c['id']]
(P/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
projection=[];chapter=None
for s in v['scenes']:
 if s.get('chapter'):chapter=s['chapter']
 for l in s['lines']:projection.append({'chapter':chapter,'id':l['id'],'text':l['text']})
(P/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
for name in ['script.md','claims.md']:
 text=(P/'history-r10'/name).read_text();text=''.join(line for line in text.splitlines(keepends=True)if not line.startswith('| c09r099 |'))
 for lid,new in texts.items():assert text.count(old[lid])==1;text=text.replace(old[lid],new)
 (P/name).write_text(text)
with(P/'narration.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['id','chapter','source','anchor','text'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:r[k]for k in w.fieldnames}for r in claims)
notes=json.loads((P/'history-r10/author-notes.json').read_text());notes.update(revision=11,status='r11_candidate_unapproved',previous_version='history-r10',video_sha256=sha(P/'video.json'),script_sha256=sha(P/'script.md'),narration_projection_sha256=sha(P/'narration-only.json'),lines=len(claims),scenes=len(v['scenes']),illustrations=sum(s['template']=='shot'for s in v['scenes']),spoken_character_count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in claims),retained_source_pass='history-r10/source-r10-delta.json',source_delta_status='awaiting_independent_r11_closure',loop_line_pairs=v['loops'])
notes['estimated_seconds_at_4_5_chars']=round(notes['spoken_character_count']/4.5,2)
(P/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
report={'type':'author_stakes_and_payoff_delta','independent':False,'revision':'r11','old_video_sha256':sha(P/'history-r10/video.json'),'new_video_sha256':sha(P/'video.json'),'changes':[{'id':lid,'before':old[lid],'after':new}for lid,new in texts.items()],'deleted_line':'c09r099','deleted_scene':found[0]['id'],'removed_loops':removed_loops,'other_video_values_unchanged':True,'visuals_unchanged':True,'source_labels_unchanged':True,'facts_added':False,'opening_limit':'S1 one rope-party daily up to100 remains unchanged; S2 possible crack damage is not a claim that100 actions occurred at one crack or caused an accident','payoff_limit':'r079 identifies the opening preview, r080 still gives the success result; the event remains the1973 route in the same-year body context','boundary_repair':'Root explicitly approved removing the dangling phrase 你再看看工廠， from r098 with deletion of r099; the independent-financial-statement limit is preserved','retained_readers':['history-r10/reader-a.json','history-r10/reader-b.json'],'retained_source_pass':'history-r10/source-r10-delta.json'}
(P/'reviews/narrative-r11-author-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:notes[k]for k in ['lines','scenes','illustrations','video_sha256']},ensure_ascii=False))
