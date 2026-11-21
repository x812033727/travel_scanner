"""Pure deletion of the r7a recap line, rebuilt from exact retained inputs."""
from pathlib import Path
import json,hashlib,re,csv
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'history-r7a/video.json')=='511510eb9cb014c74012d1c4c7146e5304bee1b89d8c31bc5955bcd74f0af2fe'
v=json.loads((P/'history-r7a/video.json').read_text())
found=[s for s in v['scenes']if any(l['id']=='c09r083'for l in s['lines'])]
assert len(found)==1 and len(found[0]['lines'])==1
assert not any('c09r083'in[l['setup'],l['payoff']]for l in v['loops'])
v['scenes']=[s for s in v['scenes']if s['id']!=found[0]['id']]
(P/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
claims=[c for c in json.loads((P/'history-r7a/claims.json').read_text())if c['id']!='c09r083']
(P/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
projection=[];chapter=None
for s in v['scenes']:
 if s.get('chapter'):chapter=s['chapter']
 for l in s['lines']:projection.append({'chapter':chapter,'id':l['id'],'text':l['text']})
(P/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
for name in ['script.md','claims.md']:
 text=(P/'history-r7a'/name).read_text()
 (P/name).write_text(''.join(line for line in text.splitlines(keepends=True)if not line.startswith('| c09r083 |')))
with(P/'narration.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['id','chapter','source','anchor','text'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:r[k]for k in w.fieldnames}for r in claims)
notes=json.loads((P/'history-r7a/author-notes.json').read_text())
notes.update(revision=8,status='r8_candidate_unapproved',previous_version='history-r7a',video_sha256=sha(P/'video.json'),script_sha256=sha(P/'script.md'),narration_projection_sha256=sha(P/'narration-only.json'),lines=len(claims),scenes=len(v['scenes']),illustrations=sum(s['template']=='shot'for s in v['scenes']),spoken_character_count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in claims),retained_source_pass='history-r7a/source-r7a-delta.json',source_delta_status='awaiting_independent_pure_deletion_closure')
notes['estimated_seconds_at_4_5_chars']=round(notes['spoken_character_count']/4.5,2)
(P/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
report={'type':'author_pure_deletion','independent':False,'revision':'r8','old_video_sha256':sha(P/'history-r7a/video.json'),'new_video_sha256':sha(P/'video.json'),'deleted_line':'c09r083','deleted_scene':found[0]['id'],'deleted_text':found[0]['lines'][0]['text'],'other_video_values_unchanged':True,'loops_unchanged':True,'facts_added':False,'retained_readers':['history-r7a/reader-a.json','history-r7a/reader-b.json'],'retained_source_pass':'history-r7a/source-r7a-delta.json','note':'No replacement transition added. Root will collect fresh readers and independent source deletion closure.'}
(P/'reviews/narrative-r8-author-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:notes[k]for k in ['lines','scenes','illustrations','video_sha256']},ensure_ascii=False))
