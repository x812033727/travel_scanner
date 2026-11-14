"""Two recap deletions and one true callback; exact r8 inputs remain retained."""
from pathlib import Path
import json,hashlib,re,csv
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'history-r8/video.json')=='3b2a99aa06ec8bf08e191ccb4952d7a6c12ec3162d15f8df82907f0b45f26fd3'
v=json.loads((P/'history-r8/video.json').read_text());delete={'c09r081','c09r101'}
for lid in delete:
 found=[s for s in v['scenes']if any(l['id']==lid for l in s['lines'])]
 assert len(found)==1 and len(found[0]['lines'])==1
v['scenes']=[s for s in v['scenes']if not any(l['id']in delete for l in s['lines'])]
new='我只把剛才那次攀登，當成那一條路線的答案；不拿它替每一面岩壁作保。'
for s in v['scenes']:
 for l in s['lines']:
  if l['id']=='c09r082':l['text']=new
# The one removed question no longer sets up a loop. No other link changes.
removed_loops=[l for l in v['loops']if l['setup']=='c09r081']
assert len(removed_loops)==1 and removed_loops[0]['payoff']=='c09r082'
v['loops']=[l for l in v['loops']if l['setup']!='c09r081']
assert not any(lid in[l['setup'],l['payoff']]for l in v['loops']for lid in delete)
(P/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
claims=[c for c in json.loads((P/'history-r8/claims.json').read_text())if c['id']not in delete]
for c in claims:
 if c['id']=='c09r082':c['text']=new
(P/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
projection=[];chapter=None
for s in v['scenes']:
 if s.get('chapter'):chapter=s['chapter']
 for l in s['lines']:projection.append({'chapter':chapter,'id':l['id'],'text':l['text']})
(P/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
old_text=next(l['text']for s in json.loads((P/'history-r8/video.json').read_text())['scenes']for l in s['lines']if l['id']=='c09r082')
for name in ['script.md','claims.md']:
 text=(P/'history-r8'/name).read_text()
 text=''.join(line for line in text.splitlines(keepends=True)if not any(line.startswith('| '+lid+' |')for lid in delete))
 assert text.count(old_text)==1;text=text.replace(old_text,new)
 (P/name).write_text(text)
with(P/'narration.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['id','chapter','source','anchor','text'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:r[k]for k in w.fieldnames}for r in claims)
notes=json.loads((P/'history-r8/author-notes.json').read_text())
notes.update(revision=9,status='r9_candidate_unapproved',previous_version='history-r8',video_sha256=sha(P/'video.json'),script_sha256=sha(P/'script.md'),narration_projection_sha256=sha(P/'narration-only.json'),lines=len(claims),scenes=len(v['scenes']),illustrations=sum(s['template']=='shot'for s in v['scenes']),spoken_character_count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in claims),retained_source_pass='history-r8/source-r8-delta.json',source_delta_status='awaiting_independent_r9_closure',loop_line_pairs=v['loops'])
notes['estimated_seconds_at_4_5_chars']=round(notes['spoken_character_count']/4.5,2)
(P/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
report={'type':'author_bounded_recap_delta','independent':False,'revision':'r9','old_video_sha256':sha(P/'history-r8/video.json'),'new_video_sha256':sha(P/'video.json'),'deleted_lines':sorted(delete),'changed_line':'c09r082','before':old_text,'after':new,'removed_loops':removed_loops,'other_video_values_unchanged':True,'facts_added':False,'retained_readers':['history-r8/reader-a.json','history-r8/reader-b.json'],'retained_source_pass':'history-r8/source-r8-delta.json','note':'Only the two recap scenes are removed and r082 explicitly calls back to the single climb without generalizing safety. No replacement transition added.'}
(P/'reviews/narrative-r9-author-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:notes[k]for k in ['lines','scenes','illustrations','video_sha256']},ensure_ascii=False))
