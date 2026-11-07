"""Build a new unapproved C09 source package; never touches the approved C09 project."""
import csv, hashlib, json, re
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=ROOT/'docs/videos/story-everyday-patagonia-c09'
rows=list(csv.DictReader((HERE/'narration.tsv').open(),delimiter='\t'))
chapters={
 'hook':'一枚釘子帶走了，岩縫留下什麼？',
 'origin':'鐵砧旁的釘子，走進器材袋',
 'idea':'越用越順手，岩縫卻越來越寬',
 'engine':'商品型錄裡，多了一篇勸告',
 'turn':'不帶岩釘，真能爬上去嗎？',
 'now':'記者走進工廠，壓床還在動',
}
actions={
'hand-piton':('Close-up','a workbench','an anonymous adult examining a plain steel piton in one hand'),
'reader-catalog':('Medium shot','a modest equipment shop','an anonymous adult opening a blank product booklet'),
'climber-crack':('Close-up','the base of a simple rock wall','an anonymous adult looking at a worn crack beside a plain piton'),
'reader-surprise':('Close-up','a simple shop counter','an anonymous adult with a surprised expression looking down at a blank booklet'),
'factory-curious':('Medium shot','a plain metal workshop','an anonymous adult watching a working enclosed press with a curious expression'),
'smith-piton':('Close-up','a small forge','an anonymous adult holding a plain piton above a simple anvil'),
'reader-question':('Medium shot','an equipment desk','an anonymous adult with a puzzled expression looking between a plain hammer and a blank booklet'),
'climber-bag':('Medium shot','a rock wall base','an anonymous adult lifting a plain equipment bag'),
'climber-heavy':('Medium shot','a rocky path','an anonymous adult leaning under the weight of a plain equipment bag'),
'smith-early':('Medium shot','a small forge','an anonymous adult shaping a plain metal spike with a hammer'),
'shop-empty':('Medium shot','a modest equipment shop','an anonymous adult looking into an empty plain storage tray'),
'smith-book':('Close-up','a plain forge bench','an anonymous adult studying a blank open book beside a small anvil'),
'smith-road':('Wide shot','a simple coastal roadside','an anonymous adult unloading a small anvil from a plain car'),
'smith-slow':('Close-up','a small forge','an anonymous adult concentrating on one plain steel piton at an anvil'),
'climber-selling':('Medium shot','a rock wall base','an anonymous adult offering a plain piton across a small folding table'),
'reader-price':('Close-up','a plain shop counter','an anonymous adult with a doubtful expression inspecting a plain metal piton'),
'buyer-piton':('Close-up','an equipment counter','an anonymous adult balancing a plain piton in one open palm'),
'smith-stock':('Medium shot','a small workshop','an anonymous adult arranging plain finished pitons in a storage tray'),
'reader-single':('Close-up','a plain desk','an anonymous adult holding a single completely blank sheet of paper'),
'reader-smile':('Medium shot','a simple desk by a window','an anonymous adult smiling at a blank single-page order sheet'),
'factory-mould':('Medium shot','a modest metal workshop','an anonymous adult operating a simple enclosed press'),
'engineer-mould':('Close-up','a plain workshop desk','an anonymous adult examining a plain metal mould beside a blank drawing sheet'),
'factory-rail':('Wide shot','a modest workshop beside railway tracks','an anonymous adult standing at a plain workshop doorway'),
'climber-wonder':('Medium shot','a rock wall base','an anonymous adult looking thoughtfully from a plain piton to a rock crack'),
'reader-article':('Medium shot','a plain equipment bench','an anonymous adult reading a blank journal beside a plain piton'),
'climber-count':('Close-up','a rock wall base','an anonymous adult sorting a small row of plain metal pitons on a cloth'),
'climber-sort':('Close-up','a plain equipment bench','an anonymous adult separating plain pitons into different sizes'),
'climber-skilled':('Medium shot','a simple rock wall base','an anonymous adult returning a plain piton to an equipment bag'),
'climber-next':('Medium shot','the base of a worn rock wall','an anonymous adult pausing before an old scarred crack'),
'climber-scars':('Close-up','a simple rock wall','an anonymous adult pointing toward a row of small scars beside a crack'),
'climber-stone':('Close-up','the base of a simple rock wall','an anonymous adult examining a loose plain stone flake in one hand'),
'reader-concern':('Close-up','a plain equipment bench','an anonymous adult with a concerned expression looking at a plain piton'),
'climber-large':('Close-up','a simple rock wall base','an anonymous adult comparing a small plain piton with a widened crack'),
'climber-arrive':('Wide shot','a rocky path approaching a simple wall','an anonymous adult arriving with a plain equipment bag'),
'climber-pause':('Medium shot','a simple rock wall base','an anonymous adult holding a plain hammer motionless beside an equipment bag'),
'climber-chock':('Medium shot','a simple equipment bench','an anonymous adult holding a plain metal wedge with a small cord loop'),
'climber-chock-close':('Close-up','a simple equipment bench','an anonymous adult examining the shape of a plain metal wedge'),
'climber-assess':('Medium shot','a simple rock wall base','an anonymous adult standing back to study the shape of a crack'),
'reader-old-tool':('Close-up','a plain equipment desk','an anonymous adult turning a small plain metal wedge in one hand'),
'reader-letter':('Close-up','a plain desk','an anonymous adult reading a completely blank sheet beside a plain metal wedge'),
'climber-realize':('Close-up','a simple rock wall base','an anonymous adult with a troubled expression examining a widened crack'),
'reader-new-order':('Medium shot','a plain equipment counter','an anonymous adult moving a plain metal wedge in front of a plain piton'),
'reader-window':('Medium shot','a quiet room beside a window','an anonymous adult lowering a blank booklet while looking toward distant hills'),
'climber-hammer':('Close-up','a simple rock wall base','an anonymous adult lowering a plain hammer toward an open equipment bag'),
'climber-question':('Medium shot','a simple rock wall base','an anonymous adult with a puzzled expression looking into an equipment bag'),
'reader-open':('Close-up','a plain equipment desk','an anonymous adult opening a blank instruction booklet beside a plain metal wedge'),
'climber-options':('Close-up','a plain equipment cloth at a rock wall base','an anonymous adult reaching toward a plain metal wedge beside a plain piton'),
'climber-fixed':('Medium shot','a simple rock wall base','an anonymous adult looking at one plain fixed piton in a crack from a distance'),
'reader-guide':('Close-up','a plain wooden desk','an anonymous adult opening a completely blank local guidebook'),
'reader-consider':('Medium shot','a plain equipment desk','an anonymous adult with a thoughtful expression pausing over a blank booklet'),
'writer-pages':('Medium shot','a plain writing desk','an anonymous adult arranging several completely blank manuscript pages'),
'reader-thick':('Close-up','a plain desk','an anonymous adult holding a thick blank booklet beside a single blank sheet'),
'reader-surprise-pages':('Close-up','a plain equipment counter','an anonymous adult raising an eyebrow while turning a blank booklet page'),
'climber-foothold':('Medium shot','a simple rock wall base','an anonymous adult looking down at a smooth worn foothold'),
'climber-look':('Close-up','a simple rock wall base','an anonymous adult examining a natural crack beside a smooth foothold'),
'reader-price-doubt':('Medium shot','a plain equipment counter','an anonymous adult looking skeptically between a blank booklet and a plain piton tray'),
'reader-skeptical':('Close-up','a plain shop counter','an anonymous adult with a skeptical expression holding a blank product booklet'),
'reader-review':('Medium shot','a quiet room','an anonymous adult reading a blank journal with a doubtful expression'),
'reader-doubt':('Close-up','a plain desk','an anonymous adult frowning at a blank booklet beside a plain hammer'),
'climber-defiant':('Medium shot','a simple rock wall base','an anonymous adult holding a plain equipment bag with a determined expression'),
'climber-wall':('Wide shot','the base of a tall simple rock wall','an anonymous adult looking upward while holding a plain metal wedge'),
'climber-nohammer':('Medium shot','a simple rock wall base','an anonymous adult putting a plain hammer aside on a cloth'),
'reader-respond':('Medium shot','a plain desk','an anonymous adult comparing a blank product booklet with a blank journal'),
'climber-ready':('Medium shot','a simple rock wall base','an anonymous adult securing a plain equipment bag before a climb'),
'climber-start':('Wide shot','the base of a tall simple rock wall','an anonymous adult with a rope coiled beside them inspecting a plain metal wedge'),
'climber-high':('Wide shot','a simple tall rock wall','an anonymous adult climber with a clearly visible safety rope resting on a broad ledge'),
'reader-result':('Close-up','a plain desk','an anonymous adult lowering a blank journal with a relieved expression'),
'climber-other':('Medium shot','a different simple rock wall base','an anonymous adult pausing in front of an unfamiliar crack'),
'factory-door':('Medium shot','a modest metal workshop entrance','an anonymous adult reaching for a plain workshop door'),
'factory-piton':('Close-up','a modest metal workshop','an anonymous adult inspecting a newly pressed plain piton beside an enclosed press'),
'visitor-old':('Close-up','a simple equipment shop','an anonymous adult viewing old plain metal pitons in a small display case'),
'clerk-cabinet':('Medium shot','a simple equipment shop','an anonymous adult opening a plain display cabinet containing ordinary pitons and wedges'),
'worker-press':('Medium shot','a modest metal workshop','an anonymous adult working beside an enclosed press with a small idle portable forge behind'),
'clerk-board':('Medium shot','a simple equipment shop','an anonymous adult inspecting a plain wooden demonstration board holding ordinary wedges with cord loops'),
'reader-factory':('Close-up','a modest workshop doorway','an anonymous adult with a thoughtful expression watching an enclosed press'),
'worker-jacket':('Medium shot','a plain clothing rack inside an equipment shop','an anonymous adult holding the sleeve of an unbranded outdoor jacket'),
'clerk-jacket':('Medium shot','a simple equipment shop','an anonymous adult arranging an unbranded jacket on a plain rack'),
'worker-mould':('Close-up','a modest metal workshop','an anonymous adult inspecting a plain heavy metal mould'),
'reader-ledger':('Close-up','a plain office desk','an anonymous adult pausing over a completely blank notebook beside a plain mould'),
'climber-choice':('Medium shot','a simple rock wall base','an anonymous adult placing a plain metal wedge beside an open equipment bag'),
'reader-answer':('Medium shot','a plain equipment counter','an anonymous adult closing a blank booklet beside a plain hammer and wedge'),
'viewer-comment':('Close-up','a plain equipment desk','an anonymous adult looking thoughtfully at a plain piton'),
'viewer-close':('Medium shot','a plain desk','an anonymous adult closing a completely blank story booklet'),
}
lighting=['soft overcast light from the left','mild window light from the right','soft neutral daylight','soft lamp light from the left']
cameras=['push in','slow pan','pull back','hold']
scene_rows=[]
# Split only the twenty longest lines with an existing punctuation break. No words change.
choices=[]
for i,row in enumerate(rows[:-3]):
 candidates=[m.end() for m in re.finditer('[，；：。]',row['text'])if 16<=m.end()<=len(row['text'])-14]
 if len(row['text'])>42 and candidates:choices.append((len(row['text']),i,min(candidates,key=lambda j:abs(j-len(row['text'])/2))))
fixed_split_rows=[25, 33, 41, 43, 45, 48, 51, 52, 53, 56, 57, 61, 70, 74, 75, 78, 79, 80]
splits={}
for i in fixed_split_rows:
 candidates=[m.end()for m in re.finditer('[，；：。]',rows[i]['text'])if 12<=m.end()<=len(rows[i]['text'])-12]
 if not candidates:raise ValueError(f'fixed split row {i+1} needs a phrase boundary')
 anchor={25:'文章，',48:'；'}.get(i)
 splits[i]=rows[i]['text'].index(anchor)+len(anchor) if anchor else min(candidates,key=lambda j:abs(j-len(rows[i]['text'])/2))
for i,row in enumerate(rows):
 if i>=len(rows)-3:continue
 parts=[row['text']]
 if i in splits:
  j=splits[i];parts=[row['text'][:j],row['text'][j:]]
 for part_n,part in enumerate(parts):
  scene_rows.append({**row,'text':part,'parent_row':i+1,'part':part_n})

scenes=[]
records=[]
chapter_counts=Counter()
first_by_chapter={}
by_parent={}
for n,row in enumerate(scene_rows,1):
 chapter=row['chapter'];chapter_counts[chapter]+=1
 lid=f'c09r{n:03d}';sid=f'c09r-shot-{n:03d}'
 view,place,action=actions[row['visual']]
 if row['part']:
  view='Close-up' if view!='Close-up' else 'Medium shot'
 prompt=f'{view} at {place}, {action}, {lighting[n%len(lighting)]}.'
 scene={'id':sid,'template':'shot','data':{'prompt':prompt,'camera':cameras[(n-1)%len(cameras)],'visual':'still'},'lines':[{'id':lid,'text':row['text']}]}
 if chapter not in first_by_chapter:
  first_by_chapter[chapter]=lid;scene['chapter']=chapters[chapter]
 # Use explicit per-line speech only for the approved source brand's written Latin name.
 if 'Patagonia' in row['text']:
  scene['lines'][0]['say']=row['text'].replace('Patagonia','巴塔哥尼亞')
  scene['lines'][0]['say_for']=hashlib.sha256(row['text'].encode()).hexdigest()[:12]
 scenes.append(scene)
 records.append({'id':lid,'chapter':chapter,'text':row['text'],'source':row['source'],'anchor':row['anchor'],'status':'PENDING_INDEPENDENT_REVIEW','parent_row':row['parent_row']})
 by_parent.setdefault(row['parent_row'],[]).append(lid)
# End with exactly three outro lines; the answer is not repeated in an earlier final-card scene.
outro_lines=[]
for outro_n,row in enumerate(rows[-3:]):
 lid=f'c09r{len(records)+1:03d}'
 outro_lines.append({'id':lid,'text':row['text']})
 records.append({'id':lid,'chapter':'now','text':row['text'],'source':row['source'],'anchor':row['anchor'],'status':'PENDING_INDEPENDENT_REVIEW','parent_row':len(rows)-2+outro_n})
 by_parent[len(rows)-2+outro_n]=[lid]
scenes.append({'id':'c09r-outro','template':'outro','data':{'title':'工具仍賣，建議變了','cta':'留言說說你會不會相信'},'lines':outro_lines})

def lid(parent,last=False):return by_parent[parent][-1 if last else 0]
loop_pairs=[
(1,82,'帶走器材，留給下一個人的代價'),
(22,23,'手工趕不上需求後如何交貨'),
(31,32,'岩縫反覆被敲後留下什麼'),
(43,44,'新的想法寫到哪裡'),
(45,46,'型錄用什麼衡量攀登成功'),
(50,51,'固定岩釘的資訊如何留給後人'),
(55,56,'作者用什麼例子說明器材選擇有差別'),
(66,67,'一次大岩壁攀登的器材袋裡有什麼'),
(79,80,'一座壓岩釘的模具成本多少'),
(5,68,'不帶岩釘能否完成一次大岩壁路線'),
(5,75,'工廠那部機器後來做什麼'),
(7,84,'為何賣岩釘的人勸少敲，商品後來怎麼了'),
(11,12,'想買可重用硬鋼釘時供應發生什麼'),
(14,15,'一個人手工一小時做幾枚'),
(16,17,'手工岩釘開什麼價格'),
(19,20,'價目表要先提醒顧客什麼'),
(25,32,'順手耐用的工具怎麼長出另一個問題'),
(29,32,'人的熟練動作給岩石留下什麼'),
(34,35,'裂縫變寬後原來的小釘子能不能用'),
(37,39,'是否有少用錘子的替代工具'),
(41,42,'早用過楔塊的人當時怎麼看它'),
(47,53,'只讀勸告的顧客下一步怎麼選'),
(52,53,'換工具是否只靠前言'),
(59,65,'顧客是否相信賣器材者的勸告'),
(63,68,'不用岩釘是否能完成長路線'),
(69,70,'一次路線走通能否普遍保證'),
(71,75,'工廠裡那部機器在做什麼'),
(74,75,'陳列櫃岩釘是否只是舊存貨'),
(77,79,'器材店裡的外套如何與器材相關'),
(81,84,'勸少用而商品仍在，改變的是什麼'),
]
# The parent-row references are checked and human-readable in author-notes.json.
old=json.loads((OLD/'video.json').read_text())
style='標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，關鍵數字放慢。語速像平常聊天，一秒四到五個字，句與句之間不拖。絕不平、絕不像在念稿。'
video={**old,'slug':'story-everyday-patagonia-c09-remake-20261025','target_minutes':[12,14],'voice':{'provider':'gemini','name':'Sulafat','style':style},'subtitles':{'burn_in':True},'look':{'preset':'cute-mystery'},'characters':[],'loops':[{'setup':lid(s),'payoff':lid(p,True),'what':what}for s,p,what in loop_pairs],'scenes':scenes}
video.pop('series',None)
video['youtube']={**old['youtube'],'title':'Patagonia憑什麼勸你少用？1972年的岩釘難題｜品牌故事','description':'1972 年的器材型錄，為什麼勸顧客少用自家岩釘？從當事人回憶的手工鍛造，經過岩縫傷痕、型錄爭論與一次大岩壁攀登，走進後來報導記錄的工廠。\n\n1977 僅為採訪文章刊出年，非已確認的到訪日期。插畫由 AI 生成，均為匿名概念示意，不重建真人或真實路線。\n\n參考資料\n'+'\n'.join(x['url'] for x in old['sources']),'video_id':None}
video['thumbnail']={'template':'thumb','data':{'headline':'少用\n自家貨？','sub':'1972年岩釘的難題','brand':'PATAGONIA','tag':'品牌故事','shot':scenes[3]['id']}}
(HERE/'video.json').write_text(json.dumps(video,ensure_ascii=False,indent=2)+'\n')
series=json.loads((OLD/'series.json').read_text())
series['target_minutes']=13
series['video_slug']=video['slug']
series['production_status']='candidate_unapproved'
(HERE/'source-series-context.json').write_text(json.dumps(json.loads((OLD/'series.json').read_text()),ensure_ascii=False,indent=2)+'\n')
(HERE/'series.json').write_text(json.dumps(series,ensure_ascii=False,indent=2)+'\n')
# Plain projected input for new independent readers: no source verdicts or previous outcomes.
projection=[{'chapter':s.get('chapter'), 'id':l['id'],'text':l['text']}for s in scenes for l in s['lines']]
(HERE/'narration-only.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
(HERE/'claims.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
script=['# C09 Patagonia｜10-25 新規則重製候選','', '狀態：未核准作者候選；舊 C09 稿、核准與素材保持原狀。目標13分鐘，尚未量測TTS。只有下表旁白進配音，來源及章名不念。','']
for chapter in chapters:
 script += ['## '+chapters[chapter],'','| ID | 旁白 | 原件／段落 |','| --- | --- | --- |']
 for r in records:
  if r['chapter']==chapter:script.append(f"| {r['id']} | {r['text']} | {r['source']}：{r['anchor']} |")
 script.append('')
script+=['## 原件','']
for source in old['sources']:script.append(f"- {source['title']}：{source['url']}（沿用來源身份，本文新增說法待獨立重核）")
(HERE/'script.md').write_text('\n'.join(script)+'\n')
claims=['# C09 重製候選逐行來源索引','', '全部仍為 PENDING_INDEPENDENT_REVIEW。這是作者對照表，不是正式查核收據，也不繼承舊稿的 PASS。','', '| 行 | 主張／句子 | 來源 | 原件定位／界線 | 狀態 |','| --- | --- | --- | --- | --- |']
for r in records:claims.append(f"| {r['id']} | {r['text']} | {r['source']} | {r['anchor']} | PENDING |")
(HERE/'claims.md').write_text('\n'.join(claims)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
count=sum(len(re.sub(r'[^\w\u3400-\u9fff]','',r['text']))for r in records)
notes={'status':'candidate_unapproved','basis_commit':'2b20c30d359fe5d93a4ea66f013a52fa20a35c05','reference_pr':1844,'source_project':'story-everyday-patagonia-c09','new_slug':video['slug'],'old_script_sha256':sha(OLD/'script.md'),'old_video_sha256':sha(OLD/'video.json'),'video_sha256':sha(HERE/'video.json'),'script_sha256':sha(HERE/'script.md'),'narration_projection_sha256':sha(HERE/'narration-only.json'),'lines':len(records),'scenes':len(scenes),'illustrations':sum(s['template']=='shot'for s in scenes),'spoken_character_count':count,'estimated_seconds_at_4_5_chars':round(count/4.5,2),'measured_tts_seconds':None,'duration_gate_passed':False,'series_kind':'story','approved':False,'independent_reviews':[],'paid_operations':0,'backend_writes':0,'budget_status':'HOLD: a new everyday slug needs an attributable account and approved whole-film quote before paid work','source_delta':['S4: summer direct sales and winter stock, participant recollection','S4: Europe about 30 cents versus own 1.50 dollars, participant recollection; no margin claim','S4: 1964 order-sheet May–September delivery warning and journalist explanation'],'facts_not_added':['no 1972 complete withdrawal','no sales percentage or causation from apparel','no interview date inferred from 1977 publication'],'loop_parent_row_pairs':[{'setup_parent':s,'setup_text':rows[s-1]['text'],'payoff_parent':p,'payoff_text':rows[p-1]['text'],'what':w}for s,p,w in loop_pairs],'note':'At 4.5 characters/s the estimate excludes real pacing. No duration acceptance or media approval is claimed.'}
(HERE/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:notes[k]for k in ['lines','scenes','illustrations','spoken_character_count','estimated_seconds_at_4_5_chars','video_sha256']},ensure_ascii=False))
