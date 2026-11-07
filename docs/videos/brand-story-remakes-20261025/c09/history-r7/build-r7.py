"""Rebuild r7's bounded structural revision from the retained exact r6 inputs."""
from pathlib import Path
import json,hashlib,copy,re,csv
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'history-r6/video.json')=='54842c50b8da3636847fe52593967e4905f78a1f64b832cd059c372ef1b37bf0'
v=json.loads((P/'history-r6/video.json').read_text())
old=copy.deepcopy(v)
claims={r['id']:r for r in json.loads((P/'history-r6/claims.json').read_text())}
texts={
 'c09r001':'器材文章舉過一個例子：一組結繩熟手，一天能放入、取回多達一百枚岩釘。',
 'c09r002':'如果你是下一個爬同一道裂縫的人，他們帶走釘子以後，會把什麼留給你？',
 'c09r003':'想像你翻開一九七二年的器材型錄，桌旁是一枚剛從岩縫拔出的鋼釘。',
 'c09r040':'英國攀岩者早就用上金屬楔塊；這件不是修納德發明的工具，跟岩釘有什麼不同？',
 'c09r043':'記者寫，修納德在一九五九、一九六〇年，就已經用過楔塊。',
 'c09r033':'一九七二年的型錄前言說，在優勝美地的熱門路線，反覆敲拔已讓裂縫出現一排排釘孔。',
 'c09r042':'不過，不同裂縫有不同條件；換一件工具，也不能當成安全保證。',
 'c09r044':'報導轉引攀岩書裡一封一九七〇年的回信：他說楔塊有用，',
 'c09r045':'平常卻不會取代岩釘。',
 'c09r039':'還記得前面那枚楔塊嗎？兩種工具都能取回；現在，岩壁的代價讓這個差別變得更具體。',
 'c09r093':'同一年，戶外服裝開始使用巴塔哥尼亞標籤；開場提到的品牌名字，這時才出現。',
 'c09r092':'你還記得剛才出現的服裝標籤嗎？我覺得更有意思的是：服裝跟這座器材工廠，究竟有什麼關聯？',
 'c09r095':'修納德說，服裝收入補貼攀岩器材；一座壓岩釘的模具，又要多少錢？',
}
# The quantitative opening remains the source's example of a rope-party of skilled climbers;
# it is neither an individual count nor a measured population average.
claims['c09r001'].update(source='S1',anchor='1967 文章的一組結繩熟手單日多達100枚例示；非個人、非平均')
claims['c09r002'].update(source='S2',anchor='後來攀登者承受岩縫損傷的觀眾假設問句')
claims['c09r003'].update(source='S2',anchor='1972 型錄的明示假想閱讀場景，不重建史實現場')
claims['c09r043']['anchor']='1959／1960 已使用楔塊；不再將1970回信當作當時看法'
claims['c09r093']['anchor']='S7 的1973服裝標籤；放在同年段落，非1977才首次使用'
# No one of these deleted scenes carries a unique source fact.
deleted={'c09r028','c09r066','c09r067','c09r094'}
for s in v['scenes']:
 for l in s['lines']:
  if l['id']in texts:
   l['text']=texts[l['id']]
   l.pop('say',None);l.pop('say_for',None)
   claims[l['id']]['text']=l['text']
 # These two shots follow the new explicitly imagined opening, without naming a real person.
 if s['id']=='c09r-shot-002':
  s['data']['prompt']='Wide shot at the base of a simple rock wall, an anonymous adult arriving with a plain equipment bag and looking toward a worn crack, soft overcast light.'
 if s['id']=='c09r-shot-003':
  s['data']['prompt']='Medium shot at a plain equipment desk, an anonymous adult opening a completely blank product booklet beside a plain steel piton, soft neutral window light.'
# Retain every scene/line ID, but place dated facts in the actual body chronology.
base=[s for s in v['scenes']if not any(l['id']in deleted for l in s['lines'])]
line_scene={l['id']:s for s in base for l in s['lines']}
moved_ids=['c09r040','c09r041','c09r043','c09r044','c09r045','c09r093']
moved_scenes={line_scene[x]['id'] for x in moved_ids}
ordered=[s for s in base if s['id']not in moved_scenes]
def insert_before(line_id,ids):
 at=next(i for i,s in enumerate(ordered)if any(l['id']==line_id for l in s['lines']))
 ordered[at:at]=[line_scene[x]for x in ids]
def insert_after(line_id,ids):
 at=next(i for i,s in enumerate(ordered)if any(l['id']==line_id for l in s['lines']))+1
 ordered[at:at]=[line_scene[x]for x in ids]
insert_before('c09r019',['c09r040','c09r041','c09r043'])
insert_after('c09r030',['c09r044','c09r045'])
insert_after('c09r082',['c09r093'])
v['scenes']=ordered
for i in ['c09r040','c09r041','c09r043']:claims[i]['chapter']='origin'
claims['c09r093']['chapter']='turn'
# Answered material is no longer hung as a fresh mystery after its answer.
loops=[]
for l in v['loops']:
 if l['setup']in {'c09r039','c09r043'}:continue
 if l['setup']=='c09r001':l['setup']='c09r002'
 if l['setup']=='c09r094':l['setup']='c09r095'
 if l['setup']=='c09r083':l['setup']='c09r084'
 if l['setup']=='c09r092':l['what']='服裝與器材工廠的財務關聯，歸於當事人說法'
 loops.append(l)
loops.append({'setup':'c09r040','payoff':'c09r041','what':'英國楔塊與岩釘在使用方式上有什麼不同'})
v['loops']=loops
pos={l['id']:i for i,s in enumerate(ordered)for l in s['lines']}
for l in loops:
 assert l['setup']in pos and l['payoff']in pos
 assert pos[l['setup']]<pos[l['payoff']],l
# Generated source files remain author candidates: no old approval is promoted.
(P/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
records=[claims[l['id']]for s in ordered for l in s['lines']]
projection=[]
current=None
for s in ordered:
 if s.get('chapter'):current=s['chapter']
 for l in s['lines']:projection.append({'chapter':current,'id':l['id'],'text':l['text']})
(P/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
(P/'claims.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
script=['# C09 Patagonia｜r7 結構修訂候選','', '狀態：未核准作者候選，尚未量測實際音訊；r6與兩位讀者原判定保留在history-r6。只有旁白進配音，章名與來源不念。','']
for s in ordered:
 if s.get('chapter'):script+=['## '+s['chapter'],'','| ID | 旁白 | 原件／段落 |','| --- | --- | --- |']
 for l in s['lines']:
  c=claims[l['id']];script.append(f"| {l['id']} | {l['text']} | {c['source']}：{c['anchor']} |")
script+=['','## 原件','']
for x in v['sources']:script.append(f"- {x['title']}：{x['url']}")
(P/'script.md').write_text('\n'.join(script)+'\n')
cs=['# C09 r7 作者逐行來源對照','', '全部仍待綁定本次結構修訂的獨立覆核；不承接舊稿的正式核准。','', '| 行 | 主張／句子 | 來源 | 原件定位／界線 | 狀態 |','| --- | --- | --- | --- | --- |']
for r in records:cs.append(f"| {r['id']} | {r['text']} | {r['source']} | {r['anchor']} | PENDING |")
(P/'claims.md').write_text('\n'.join(cs)+'\n')
with(P/'narration-r7.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['id','chapter','source','anchor','text'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:r[k]for k in w.fieldnames}for r in records)
(P/'narration.tsv').write_bytes((P/'narration-r7.tsv').read_bytes())
changed=[{'id':l['id'],'before':next(q['text']for s in old['scenes']for q in s['lines']if q['id']==l['id']),'after':l['text'],'source':claims[l['id']]['source']}for s in ordered for l in s['lines']if l['id']in texts]
rep={'type':'author_structural_delta','independent':False,'old_video_sha256':sha(P/'history-r6/video.json'),'new_video_sha256':sha(P/'video.json'),'changes':changed,'deleted_line_ids':sorted(deleted),'moved_line_ids':moved_ids,'source_chronology':['1946 prior smith','1957 Chouinard forge','prior British chock use; Chouinard 1959/1960 use','1964 mail order','1966 workshop','1967 article','1970 letter','1972 foreword','1973 review/climb/apparel label','1977 article publication; visit day unknown'],'opening_limit':'1967 example: one rope-party of skilled climbers, up to100 placements/removals in a day; not a person or average','source_facts_added':False,'note':'Figures/clauses move but no new dated fact or financial cause is asserted. Fresh source/structural review and two blind readers still required.'}
(P/'reviews/structural-r7-author-delta.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
notes=json.loads((P/'history-r6/author-notes.json').read_text());notes.update(revision=7,video_sha256=sha(P/'video.json'),script_sha256=sha(P/'script.md'),narration_projection_sha256=sha(P/'narration-only.json'),lines=len(records),scenes=len(ordered),illustrations=sum(s['template']=='shot'for s in ordered),spoken_character_count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in records),independent_reviews=[],previous_version='history-r6',status='r7_structural_candidate_unapproved')
notes.pop('loop_parent_row_pairs',None)
notes['loop_line_pairs']=v['loops']
notes['estimated_seconds_at_4_5_chars']=round(notes['spoken_character_count']/4.5,2)
(P/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:notes[k]for k in ['lines','scenes','illustrations','spoken_character_count','estimated_seconds_at_4_5_chars','video_sha256']},ensure_ascii=False))
