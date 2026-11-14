from pathlib import Path
import json,copy,hashlib,re,subprocess
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=HERE/'history/r4'
AUDIT=Path('/workspace/work/brand-story-20261025/c10-audit')
ROOT=Path('/workspace/work/brand-story-20261025/c10-submission-root')
MEDIA=AUDIT/'r5-prepared-media'
SLUG='story-everyday-oxo-c10-remake-20261025'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
readj=lambda p:json.loads(Path(p).read_text())
def writej(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
protection=readj(AUDIT/'r5-protected-before.json')
for p,h in protection['protected_files'].items():assert sha(p)==h,p
old=readj(BASE/'video.json'); oldclaims=readj(BASE/'claims.json'); oldn=readj(BASE/'narration-only.json')
assert {n:sha(BASE/n) for n in protection['r4_input_sha256']}==protection['r4_input_sha256']
oldlines={l['id']:l for s in old['scenes'] for l in s['lines']}
oldscenes={l['id']:s for s in old['scenes'] for l in s['lines']}
oldrows={r['line_id']:r for r in oldclaims['claims']}
expand=readj(HERE/'research-expansion/claims.json')
receipts=readj(HERE/'research-expansion/source-receipts.json')
xs={s['id']:s for s in receipts['sources']}
xc={c['id']:c for c in expand['claims']}
scenes=[];rows=[]; newids=[]; change_reasons={}; chapters={}

def keep(lid):
 s=copy.deepcopy(oldscenes[lid]); assert len(s['lines'])==1
 scenes.append(s); rows.append(copy.deepcopy(oldrows[lid]))

def ev(sid,loc,excerpt,page=None):
 r=xs[sid]
 p=(AUDIT/'length-research/X05.page-11.txt' if sid=='X05_TEACHER_PACKET' else Path(r['raw_path']).with_suffix('.paragraphs.txt')) if page is None else AUDIT/'length-research'/f'X20.page-{page}.flow.txt'
 assert p.is_file(),p
 assert re.sub(r'\s+',' ',excerpt).strip() in re.sub(r'\s+',' ',p.read_text()).strip(),(sid,excerpt)
 return {'source':sid,'url':r['requested_url'],'source_bytes_sha256':r['sha256'],'locator':loc,'readable_cache_path':str(p),'readable_cache_sha256':sha(p),'short_excerpt':excerpt}

def add(code,text,prompt,refs=(),evidence=(),kind='attributed_fact',limits=(),chapter=None):
 lid='c10v5'+code;sceneid='c10r5-'+code
 assert lid not in oldlines
 
 if not re.search(r'close-up|medium shot|wide shot|overhead|low angle|from behind',prompt,re.I):
  size='Close-up' if code[0] in 'bp' or code in ['f06','f07','s03','s04','s06','s07','u04','u05','u08','u10','u11','u12','u13','u14'] else 'Medium shot'
  prompt=size+': '+prompt
 moves=['pan right','slow pull out','tilt up','pan left','tilt down','drift right']
 s={'id':sceneid,'template':'shot','data':{'prompt':prompt,'visual':'still','camera':moves[len(newids)%len(moves)]},'lines':[{'id':lid,'text':text,'emotion':'自然接話，對一位觀眾說，不拉長停頓'}]}
 if chapter:s['chapter']=chapter
 scenes.append(s)
 boundaries=list(limits)
 for ref in refs:
  if ref in xc:boundaries+=xc[ref]['boundaries']
 if kind!='attributed_fact':boundaries+=['作者反應／觀眾假想／接續問題，不冒稱原事件或實測結果。']
 rows.append({'line_id':lid,'scene_id':sceneid,'text':text,'kind':kind,'material_refs':list(refs),'evidence':list(evidence),'limits':list(dict.fromkeys(boundaries)),'written_visual':{'conceptual':True,'not_historical_reconstruction':True,'prompt':prompt,'narration_binding':lid},'independent_verdict':'NOT_REVIEWED'})
 newids.append(lid)
 return lid

# Lock all nine already merged opening scenes, byte-value identical.
for s in old['scenes'][:9]:
 scenes.append(copy.deepcopy(s)); rows.extend(copy.deepcopy(oldrows[l['id']]) for l in s['lines'])
origin=[x['id'] for x in oldn if x['id'].startswith('c10o')]
for lid in origin:
 keep(lid)
 if lid=='c10o20':
  add('o01','館方另記下，不同版本的原型，也交給廚師、一般使用者和紐約的關節炎群體試用。','An anonymous adult user holding a prototype peeler over a kitchen preparation board while a second adult observes the hand movement.',('C10X15',),(ev('X05_TEACHER_PACKET','PDF p.11 / printed p.9, prototype user testing','Several different iterations of the peeler were developed and tested with the public'),),limits=['教育資料只述公眾試原型，沒有臨床流程、參與者人數或量化成果。'])
  # Replace the automatic HTML default with the actual per-page PDF text extraction.
  a=rows[-1]['evidence'][0];a['readable_cache_path']=str(AUDIT/'length-research/X05.page-11.txt');a['readable_cache_sha256']=sha(a['readable_cache_path'])
# User-motion grouping from a newly acquired, named 2001 article; no product list.
# Insert before the paragraph that introduces the prototype materials.
insert_at=next(i for i,s in enumerate(scenes) if s['lines'][0]['id']=='c10o19')
saved_s,saved_r=scenes[insert_at:],rows[insert_at:]
scenes=scenes[:insert_at];rows=rows[:insert_at]
add('o02','介紹早期設計的訪談記下，團隊按手和手腕的動作，替廚具分組。削皮器分到哪一組？','An anonymous designer grouping a few unbranded handle studies by simple hand motions on a worktable, no diagrams or written labels.',('A10',),(ev('X02_HANDLES','paragraph 021','groups based on the corresponding types of wrist and hand motions'),),limits=['2001文章回述設計方法，不是把該刊期當分組發生年。'])
add('o03','削皮器對應的動作，是推和拉。你可以拿起它，試著把手帶向前，再帶回來。','Close-up of an anonymous hand holding a peeler above a vegetable with a gentle push-pull gesture implied by the hand position.',('A10',),(ev('X02_HANDLES','paragraph 021','push/pull (peelers, graters)'),),kind='fact_and_explicit_viewer_hypothesis',limits=['只有推／拉分組是來源事實；你可以試的動作是觀眾示意，不當歷史測試紀錄。'])
scenes+=saved_s;rows+=saved_r
for x in oldn:
 lid=x['id']
 if not lid.startswith('c10r'):continue
 if lid=='c10r18':
  add('b01','斯托威爾談過另一種早期方案：光滑的握柄表面下，藏著可以變形的泡狀結構。','Cutaway concept illustration of a smooth rounded hand-tool handle with deformable rounded structures beneath the outer surface, no liquid or air filling shown.',('C10X01',),(ev('X02_HANDLES','paragraph 022','malleable bubbles beneath a smooth-surfaced handle'),))
  add('b02','他的想法是，手有時要捏緊再拉，有時只輕輕拉；握柄得能隨著握法變。','An anonymous hand gently pressing a smooth handle study on a neutral worktable, with a second grip study beside it.',('A11',),(ev('X02_HANDLES','paragraph 022','sometimes you need to clench and pull, and sometimes you need to pull gently'),),limits=['Stowell回述設計理論；不是已完成的力學／醫療測試或泡狀原型實效。'])
  add('b03','可是，那些初步設計最後被捨棄。斯托威爾說，它們沒有讓人直覺看出能做什麼。','An anonymous designer moving a smooth handle study aside on the worktable while leaving another grip study available to inspect.',('C10X02',),(ev('X02_HANDLES','paragraph 022','were rejected because they weren’t intuitive enough'),ev('X02_HANDLES','paragraph 022','they didn’t really communicate what they did')))
  add('b05','我會想，你第一次碰到這個光滑表面，要怎麼知道哪裡可以捏？','Close-up of a fingertip approaching an unmarked smooth handle surface without yet pressing it.',(),(),kind='editorial_viewer_question')
 keep(lid)
for x in oldn:
 if x['id'].startswith('c10m'):keep(x['id'])
for x in oldn:
 if x['id'].startswith('c10a') and x['id'] not in ['c10a20a','c10a20b','c10a20c']:keep(x['id'])
# Same assembly chapter, but make its title describe the next actual action/result.
assembly=next(s for s in scenes if s['lines'][0]['id']=='c10a01');assembly['chapter']='接上刀片，交出樣品'
add('p01','另一件館藏削皮器原型，把問題帶到刀片：它靠哪裡接住？','Concept illustration of a black-handled peeler prototype resting on a neutral worktable, clearly showing its blade support without manufacturing machinery.',('C10X03',),(ev('X16_BLADE_PROTOTYPE','paragraph 088 object description','Black handled peeler'),),limits=['「另一件」是不同館藏原型，不能與專利示意、展前樣品或首款商品混為同一實物。'])
add('p02','刀片是能轉動的金屬片，支架的上端和下端，各有一個孔。','Close-up concept view of a peeler blade support with one upper attachment hole and one lower attachment hole, no exploded assembly sequence.',('C10X03',),(ev('X16_BLADE_PROTOTYPE','paragraph 088 object description','Blade is metal that swivels'),ev('X16_BLADE_PROTOTYPE','paragraph 088 object description','upper and lower holes of blade support')))
add('p03','它靠兩個接點，分別落在這兩個孔裡。','Close-up concept view of an assembled swivelling metal peeler blade held at two attachment points within its support.',('C10X03',),(ev('X16_BLADE_PROTOTYPE','paragraph 088 object description','attached by two points that fit into upper and lower holes of blade support'),))
add('f01','要把這件工具交出去，能找到願意做的工廠嗎？','An anonymous designer bringing a finished handle study toward a plain factory meeting table, no real factory identity or industrial process shown.',('C10X04',),(),kind='source_based_transition')
add('f02','斯托威爾在後來的PBS訪談裡回憶，離預定亮相的展會只剩兩個月，製造商還沒選定。','An anonymous designer looking at a peeler study beside an unmarked closed calendar on an office table, no readable dates or invented schedule shown.',('C10X04',),(ev('X09_PBS_TRANSCRIPT','paragraph 032, Davin Stowell speech','We hadn\'t selected a manufacturer yet'),ev('X09_PBS_TRANSCRIPT','paragraph 032, Davin Stowell speech','two months before the gourmet show')))
add('f03','山姆想起以前做廚具時，合作過的一家日本製造商。','Anonymous adults discussing a plain hand-tool sample across a meeting table, with no map, company signs, heritage objects or location-specific architecture.',('C10X04',),(ev('X09_PBS_TRANSCRIPT','paragraph 032, Davin Stowell speech','he had worked with a Japanese manufacturer'),),limits=['原廠未具名；不採刀劍祖業支線或推廠址／製程。'])
add('f04','他們去了工廠，得到的答覆是：願意製作。','Anonymous adults meeting across a plain factory office table with a peeler study between them, no machinery, handshake or contract implied.',('C10X05',),(ev('X09_PBS_TRANSCRIPT','paragraph 036, Davin Stowell speech','We went to the factory and they said they would make it.'),))
add('f05','我聽到這裡，會先盯著展會開門的時間。換你等樣品，還能等到哪一天？','An anonymous adult beside an unmarked exhibition entrance, looking toward a plain empty sample table, conceptual setting only.',(),(),kind='editorial_viewer_question')
add('f06','展會開門前兩天，一個箱子到了。','A plain closed shipping box resting on a worktable near an anonymous adult, no shipping labels, carrier route or delivery actor shown.',('C10X06',),(ev('X09_PBS_TRANSCRIPT','paragraph 036, Davin Stowell speech','Two days before the gourmet show opened, a box arrived'),))
add('f07','他說，箱裡裝著樣品；他用「完美」形容它們。','Concept illustration of several unbranded peeler samples visible in a plain open box, no exact historical sample count or inspection procedure implied.',('C10X06',),(ev('X09_PBS_TRANSCRIPT','paragraph 036, Davin Stowell speech','it had the samples in it, and they were perfect'),),limits=['畫面少量示意不是原箱實際件數；完美是當事人的主觀回憶，非QC記錄。'])
add('f08','他記得，展會是在一九九〇年五月開門的。','Anonymous visitors at a modest housewares exhibition table holding unbranded peelers, no real venue identity, banners or readable dates.',('C10X07',),(ev('X09_PBS_TRANSCRIPT','paragraph 038, Davin Stowell speech','The show opened up in May of 1990'),))
add('f09','如果你是店家，把這些工具買回去，客人會直接伸手嗎？','An anonymous shopkeeper placing an unbranded peeler on a simple store display while an anonymous shopper approaches.',(),(),kind='editorial_viewer_question')
add('s01','斯托威爾點名，家用品店萊克特斯買下整條產品線。','An anonymous housewares shopkeeper inspecting a small group of unbranded kitchen tools at a counter, no store logo, order quantities or invoices shown.',('C10X07',),(ev('X09_PBS_TRANSCRIPT','paragraph 038, Davin Stowell speech','Lechters, a housewares store, purchased the full line'),),chapter='拿去試，再交到下一雙手')
add('s02','可是他記得，貨賣得沒有店家期待的快。','An anonymous shopkeeper standing beside a plain peeler display with a few items still present, no empty-store claim or numerical sales chart.',('C10X07',),(ev('X09_PBS_TRANSCRIPT','paragraph 038, Davin Stowell speech','it wasn\'t selling as quickly as they expected it to'),))
add('s03','山姆的主意，是先擺出一碗胡蘿蔔。','A bowl of whole carrots on a modest housewares store demonstration table, no people performing an unsupported action.',('C10X08',),(ev('X09_PBS_TRANSCRIPT','paragraph 038, Davin Stowell speech','a bowl full of carrots'),))
add('s04','削皮器用鏈條拴在碗上，讓走進店裡的人直接試。','An unbranded black-handled peeler attached by a visible short chain to a bowl of carrots on a store demonstration table; an anonymous hand reaches toward the peeler.',('C10X08',),(ev('X09_PBS_TRANSCRIPT','paragraph 038, Davin Stowell speech','a peeler chained to the bowl so people could try the peeler right in the store'),))
# Retain the two explicit imagined use actions once, within the single retail event.
for lid in ['c10l06','c10l07']:keep(lid)
add('s05','沒想到，照他的回憶，開放試削後，貨就賣得很快。','An anonymous shopper testing a tethered peeler at the carrot bowl while a shopkeeper observes, no checkout transaction, crowd or measured uplift implied.',('C10X08',),(ev('X09_PBS_TRANSCRIPT','paragraph 038, Davin Stowell speech','And once they did that, they flew off the shelves.'),))
add('s06','後來介紹這套設計的文章，還記下包裝讓握柄露在外面的做法。','A plain minimal retail sleeve around the head of an unbranded peeler, leaving its handle exposed and accessible, no logo, writing or exact launch-package reconstruction.',('C10X09',),(ev('X02_HANDLES','paragraph 028','minimal packaging exposes the handles'),))
add('s07','顧客買之前，就能伸手摸一摸，再捏一捏。','An anonymous shopper squeezing the exposed handle of an unbranded peeler still held within a minimal retail sleeve.',('C10X09',),(ev('X02_HANDLES','paragraph 028','touch and squeeze the merchandise before purchasing'),))
add('u01','設計作者艾爾本在一九九七年刊出的文章裡，寫下親手用它的經驗。她先拿來做什麼？','An anonymous adult author holding an unbranded peeler at a kitchen preparation board, no journal pages or invented readable text.',('C10X10',),(ev('X20_INTERACTION_ESSAY','PDF p.1 authorship','by Lauralee Alben',1),ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17, journal footer publication date','SUMMER 1997',9),ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17, first-person account','I bought one of the peelers.',9)),limits=['作者全名Lauralee Alben；原刊Summer1997見PDFp.1及p.9頁腳。1997只標文章刊出，不定購買／試用事件年。'])
add('u02','她買了一支，拿來削胡蘿蔔。她說，自己用得很愉快。','An anonymous adult using an unbranded peeler on a carrot over a kitchen board, no connection to a shop demonstration or medical trial.',('C10X10',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','I pared a carrot with it. I actually enjoyed using it.',9),))
add('u03','她又把削皮器帶到丈夫父母那裡，讓吉姆和寶拉試。','An anonymous adult passing an unbranded peeler toward two other anonymous adults at a kitchen table, neutral ages and no medical or family-photo likeness cues.',('C10X11',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','my husband’s parents, Jim and Paula, to try out.',9),))
add('u04','她記下他們一開始的反應：很舒服，大黑柄容易握，不用捏得那麼用力。','Close-up of anonymous hands loosely wrapping around a broad black peeler handle, no grip-force scale or medical before-and-after framing.',('C10X11','C10X12'),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17, reported personal reaction','This big black handle is easy to hold.',9),ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17, reported personal reaction','You don’t have to squeeze it so hard.',9)))
add('u06','如果換你，會只把它握著，還是真的拿一顆馬鈴薯來？','A whole potato on a preparation board beside an anonymous hand holding a peeler, an uncompleted next action.',(),(),kind='editorial_viewer_question')
add('u07','艾爾本寫道，他們輪流拿削皮器削馬鈴薯。','Two anonymous adults taking turns at a preparation board, with only one adult currently holding a peeler above a potato; no precise test count or patient status.',('C10X12',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','They took turns peeling a potato.',9),))
add('u08','她記下他們還說，刀很利，朝自己或往外削，都能用。','Close-up of an unbranded peeler beside a partly peeled potato on a board, showing no two-direction test protocol or unsafe cutting demonstration.',('C10X12',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17, quoted comments not controlled testing','It’s very sharp. Works if you peel toward yourself or away.',9),))
add('u09','我讀到這裡，反而等著看，他們會怎麼把它收起來。','An anonymous adult holding a peeler above a clean work surface beside a simple kitchen hook, before a storage action occurs.',(),(),kind='editorial_reaction')
add('u10','文章裡，他們又說：試試把它掛起來吧。','An anonymous hand bringing an unbranded peeler hanging hole toward a simple kitchen hook, conceptual storage action without exact historical hook dimensions.',('C10X13',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','Let’s try hanging it up.',9),))
add('u11','接著的回答是：行，這樣也可以。','An unbranded peeler hanging securely from a simple kitchen hook, anonymous hand nearby, no quantified tolerance or repeated test implied.',('C10X13',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','Yep, that works too.',9),))
add('u12','然後，兩人拿出原本那支金屬削皮器。','An anonymous hand bringing an old slim metal peeler beside the newer broad-handled peeler at a kitchen table, no drawer or specific storage location shown.',('C10X14',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','They pulled out their old metal peeler',9),))
add('u13','他們把新舊兩支，並排拿著。','Anonymous hands holding one slim metal peeler and one broad black-handled peeler side by side above a kitchen table.',('C10X14',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','held the two side by side',9),))
add('u14','最後，把舊的那支丟進垃圾桶。','An anonymous hand lowering a slim old metal peeler into an ordinary bin while the broad-handled peeler remains on the nearby table; no invented emotional expression.',('C10X14',),(ev('X20_INTERACTION_ESSAY','PDF p.9 / printed p.17','then threw the old one in the trash.',9),))
# Preserve the already stated answer and the two voiced CTA lines, no additional recap.
outro=copy.deepcopy(old['scenes'][-1]);scenes.append(outro)
rows += [copy.deepcopy(oldrows[l['id']]) for l in outro['lines']]

doc=copy.deepcopy(old);doc['scenes']=scenes
loops=[l for l in old['loops'] if all(any(r['line_id']==l[k] for r in rows) for k in ['setup','payoff']) and l['setup'] not in ['c10h07']]
loops += [
 {'setup':'c10v5o02','payoff':'c10v5o03','what':'按手部動作分組時削皮器歸到哪一類'},
 {'setup':'c10h07','payoff':'c10v5s04','what':'陌生黑柄如何交到店內顧客手裡'},
 {'setup':'c10v5b01','payoff':'c10v5b03','what':'泡狀結構的早期方案是否被採用'},
 {'setup':'c10v5b05','payoff':'c10r19','what':'表面如何讓人看出能捏的地方'},
 {'setup':'c10v5p01','payoff':'c10v5p03','what':'館藏原型的刀片靠什麼留在支架'},
 {'setup':'c10v5f01','payoff':'c10v5f04','what':'未選廠時如何找到願意製作的人'},
 {'setup':'c10v5f05','payoff':'c10v5f07','what':'展會開門前樣品是否抵達'},
 {'setup':'c10v5f09','payoff':'c10v5s04','what':'店家購進後如何讓顧客伸手試'},
 {'setup':'c10v5s02','payoff':'c10v5s05','what':'慢銷之後店家做了什麼、當事人記得什麼結果'},
 {'setup':'c10v5s06','payoff':'c10v5s07','what':'包裝露出握柄讓買前多出什麼動作'},
 {'setup':'c10v5u01','payoff':'c10v5u02','what':'具名作者自己使用後留下什麼感受'},
 {'setup':'c10v5u06','payoff':'c10v5u07','what':'另一雙手是否真的拿食材試削'},
 {'setup':'c10v5u09','payoff':'c10v5u11','what':'試用後能不能把工具掛回去'},
 {'setup':'c10v5u12','payoff':'c10v5u14','what':'拿出舊工具並排後發生什麼動作'}
]
doc['loops']=loops
# Newly used original URLs accompany the unchanged core references.
newtitles={'X02_HANDLES':'Handles with care — Pilar Guzman / ONE Magazine, Jan 2001','X09_PBS_TRANSCRIPT':'Curb Cut Effect: Kitchen Utensils — PBS accessible descriptive transcript','X16_BLADE_PROTOTYPE':'Good Grips prototype 2011-50-20 — Smithsonian / Cooper Hewitt','X20_INTERACTION_ESSAY':'At the Heart of Interaction Design — Lauralee Alben, Summer 1997','X05_TEACHER_PACKET':'Teacher Resource Packet — Cooper Hewitt'}
for sid,title in newtitles.items():
 if not any(s['url']==xs[sid]['requested_url'] for s in doc['sources']):doc['sources'].append({'title':title,'url':xs[sid]['requested_url'],'checked_on':'2026-10-25'})
# Keep publish title / layout-d thumbnail fixed. Rewrite synopsis around final scope.
doc['youtube']['description']='一支削皮器從握不住，到真的交給另一雙手，握柄得改掉什麼？\n\n跟著OXO的黏土與原型、被放棄的光滑泡狀方案、材料與連接設計，走到展前樣品、店內試削，以及具名作者記下的一次家庭使用。\n\n起因與早期過程依品牌、具名設計者及館方回顧。專利是方案，館藏原型不是首款量產BOM；店家反應是當事人回憶，家庭試用是Lauralee Alben文章的個人記述，不推普遍療效。1997是文章刊出年，非已確定的試用年。匿名畫面為概念插圖。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(s['title']+'\n'+s['url'] for s in doc['sources'])
series=readj(BASE/'series.json')
series['logline']='一個握柄經過實際原型取捨與部件連接，走向展前樣品、店內試削，再交給具名家庭使用者。'
series['names']+=['Lechters','Lauralee Alben','Lauralee','Alben','Jim','Paula']
for beat in series['beats']:
 if beat['chapter']=='a':beat.update(title='接上刀片，交出樣品',point='專利連接方案與館藏刀片分開，接到具名回述的找廠、樣品到達。')
 if beat['chapter']=='l':beat.update(title='拿去試，再交到下一雙手',point='Lechters一次店內試削，接到Alben文章裡Jim和Paula的試削、試掛及舊具取捨。')
writej('video.json',doc);writej('series.json',series)
# Sourced author projection, distinct from the runtime's official screenplay.
narration=[];chapter=None
for scene in scenes:
 chapter=scene.get('chapter',chapter)
 for line in scene['lines']:narration.append({'id':line['id'],'scene':scene['id'],'chapter':chapter,'text':line['text']})
assert len(rows)==len(narration)
for row,n in zip(rows,narration):
 assert row['line_id']==n['id'];row['scene_id']=n['scene'];row['text']=n['text']
writej('narration-only.json',narration)
script=['# C10 OXO｜R5 作者附來源稿','','作者候選；非canonical核准劇本。只有旁白欄進聲音，ID／章名／來源與註解不讀。',''];last=None
for row,n in zip(rows,narration):
 if n['chapter']!=last:script+=['','## '+n['chapter'],'','| ID | 旁白 | 來源材料／性質 |','|---|---|---|'];last=n['chapter']
 script.append('| '+n['id']+' | '+n['text']+' | '+(', '.join(row['material_refs']) or '作者互動／CTA')+'；'+row['kind']+' |')
(HERE/'script.md').write_text('\n'.join(script)+'\n')
claims=copy.deepcopy(oldclaims)
claims.update(revision='r5',scope='R5 author source anchors only; independent source/written-visual/native panel round-4-r5 pending',input_sha256={n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json']},r4_input_sha256=protection['r4_input_sha256'],claims=rows,source_qa=False,visual_qa=False,actual_audio_measured=False)
claims['research_expansion_sha256']={n:sha(HERE/'research-expansion'/n) for n in ['research.md','claims.json','source-receipts.json']}
claims['research_expansion_claims']={k:{'research_proposition':v['research_proposition'],'date_scope':v['event_date_scope'],'r4_relation':v['r4_relation'],'boundaries':v['boundaries']} for k,v in xc.items() if any(k in r['material_refs'] for r in rows)}
claims['additional_author_materials']['A10']={'source':'X02_HANDLES','locator':'paragraph 021','proposition':'Team grouped household tools by corresponding wrist/hand motions; peeler in push/pull group.','limits':['Do not list other products or infer a clinical test/quantified result.','2001 is article publication, not this method event year.']}
claims['additional_author_materials']['A11']={'source':'X02_HANDLES','locator':'paragraph 022','proposition':'Stowell described a handle that changes with gripping demands, sometimes clench/pull and sometimes gentle pull.','limits':['Design theory, not proof the smooth-bubble concept passed mechanical/user trials.']}
for sid in newtitles:
 r=xs[sid]
 claims['source_records'].append({'id':sid,'requested_url':r['requested_url'],'final_url':r.get('final_url'),'status':r.get('http_status'),'content_type':r.get('content_type'),'last_modified':r.get('last_modified'),'bytes':r['bytes'],'sha256':r['sha256'],'path':r['raw_path'],'fetched_at':r['retrieved_at_utc'],'kind':r['source_scope'],'date_scope':r['date_nature'],'usable_original_bytes':True,'limits':r['source_scope']+' '+r['date_nature']})
writej('claims.json',claims)
md=['# C10 OXO｜R5 作者逐句來源錨點','','逐句事實綁實際原件bytes／SHA、段頁、短摘錄與不支持界線，完整欄位見claims.json；C10Xxx綁三份凍結research-expansion。這不是獨立查核。','','| ID | 種類 | 原件材料 | 不支持界線 |','|---|---|---|---|']
for r in rows:md.append('| '+r['line_id']+' | '+r['kind']+' | '+(', '.join(r['material_refs']) or '作者互動／CTA')+' | '+('；'.join(dict.fromkeys(r['limits'])) if r['limits'] else '不作史實')+' |')
(HERE/'claims.md').write_text('\n'.join(md)+'\n')
brief='''# C10 OXO｜R5 修訂作者候選

## 本次建議

### 選項 A：一個握柄，怎麼交給另一雙手？

保留R4已合併開場九句及去重核心。用被捨棄的光滑泡狀柄、館藏原型刀片兩點支承、找廠與展前樣品，接到一次Lechters店內試削，再交到Alben文章中的Jim和Paula手裡。只推薦這個方向，未執行正式成片或八語媒體。

## 問題

換了拿它的手，握柄究竟得改掉什麼？

## 一句答案

要交給另一雙手，握柄得先替人讓出能自己控制工具的位置。

## 站主觀點

建議的旁白觀點是，工具還得容納真正拿起它、移動它與收回它的手；把新舊工具並排後願意留哪一支，比一句抽象通用設計宣言更具體。這是作者建議，尚未取得站主核准。

## 敘事與來源

開場先說你握不住就難做菜的利害，以MoMA館藏單件17.8公分全長交代掌中尺度，第三句進假想廚房；最多黏土、等待伸手的黑柄兩個預告，接單一承諾與主問句。六章沿物件需求推進，沒有公司年表或全產品清單。

R5新增真實動作／結果：公眾試原型、手部動作分組、被捨棄的泡狀柄、刀片兩點支承的館藏原型、未選廠到訪廠／同意製作、展前兩天箱中樣品、明說1990年五月展會、Lechters買進後慢銷與拴碗試用、買前露柄可摸、Alben自行購用到Jim／Paula試削／試掛／並排與丟舊具。舊2017胡蘿蔔泛述及PBS晚近回憶合為同一次零售敘述；舊後期產品去鰭片、轉述信件、Elsa館藏使用／挖芽眼與價格旁支讓位，不再增加人物結果線。

泡狀柄、木／泡棉模型沒有硬排測試先後。原1990專利保留為方案，非首款商品工廠流程；館藏原型兩點支承只述該件物，與首款量產BOM分開。MoMA材料圖錄只用OXO欄，旁邊滑雪杖雙射出／鋼模不用。找廠與Lechters故事是Stowell晚近回述，不補廠名、刀劍祖業、QC／訂單／銷售數或精確日。

Alben文章刊出於1997；購買與家庭試用日期未明，不替Jim／Paula加年齡、病況或臨床效果。舒適與不用那麼用力是文中個人反應。2001文章描述露柄包裝，但不當1990首批包裝配置。沒有把could force-gauge、未定1.2mm、未聽MP3或未取得信件補成事實。研究3+3、歷史與原舊集保護。

## 製作規格與狀態

目標13分鐘，自然4–5spokenUnits/s；實聲正文目標720–840秒待真TTS。官方duration body是整份未加頻道bookends的旁白，包含冷開場與有聲CTA；after-opening／strict只作分項。rough3500只是作者規劃，不用停頓、慢播、總結或旁支填長。

Gemini Sulafat與exact原生STORY_VOICE_STYLE；MiniMax image-01，look僅{"preset":"cute-mystery"}。匿名英文概念插圖不含人名、品牌、logo或文字；still與簡單運鏡。每景原生估時≤12秒、插圖規劃≥70%／最多連3卡，真媒體時間仍未驗。繁中燒錄＋CC；濃縮開場後5秒正式片頭、21秒正式v4片尾僅規格，未冒素材身分。縮圖layout d，品牌OXO、黃黑框主標、白短副標。

本版HOLD待新的獨立來源／書面配鏡、actual native panel4（round-4-r5）、念法及站主關卡。R4只有prepared-only輸入，沒有R4來源批准或actualpanel4；最後actualpanel3與source3保留history/r3，不延用來批准R5。沒有verify、SOURCE／敘事／visual PASS或owner批准。無provider、backend、Git、付費、音訊、圖片、影片與翻譯。
'''
(HERE/'brief.md').write_text(brief)
# Validate all byte/quote anchors now, without making a source-QA verdict.
records={r['id']:r for r in claims['source_records']}
checks=set()
for r in rows:
 for e in r['evidence']:
  assert sha(e['readable_cache_path'])==e['readable_cache_sha256']
  assert sha(records[e['source']]['path'])==e['source_bytes_sha256']
  normal=lambda s:re.sub(r'\s','',s).lower()
  assert normal(e['short_excerpt']) in normal(Path(e['readable_cache_path']).read_text()),(r['line_id'],e['short_excerpt'])
  checks.add((e['source_bytes_sha256'],e['readable_cache_sha256']))
assert doc['scenes'][:9]==old['scenes'][:9]
assert not (HERE/'verify-1.md').exists()
# R4's old runtime verify is not applicable to the new candidate. Preserve bytes, then remove only that stale runtime copy.
target=ROOT/'docs/videos'/SLUG
archive=AUDIT/'r5-runtime-before';archive.mkdir(exist_ok=True)
runtime_snapshot=AUDIT/'r5-runtime-before.json'
if runtime_snapshot.exists():
 runtime_before=readj(runtime_snapshot)
 for original,h in runtime_before.items():assert sha(archive/Path(original).relative_to(target))==h
else:
 runtime_before={}
 for p in target.rglob('*'):
  if p.is_file():
   runtime_before[str(p)]=sha(p)
   dest=archive/p.relative_to(target);dest.parent.mkdir(parents=True,exist_ok=True)
   assert not dest.exists()
   dest.write_bytes(p.read_bytes())
 runtime_snapshot.write_text(json.dumps(runtime_before,indent=2)+'\n')
oldverify=target/'verify-1.md'
if oldverify.exists():
 assert (archive/'verify-1.md').read_bytes()==oldverify.read_bytes()
 oldverify.unlink()
# Ordinary offline runtime preparation, c10 only, preserves the pinned immutable dictionary.
prep=subprocess.run(['node',str(HERE.parent/'prepare-runtime.mjs'),str(ROOT),str(MEDIA),'c10'],cwd=REPO,capture_output=True,text=True)
if prep.returncode:raise RuntimeError(prep.stderr)
(AUDIT/'r5-prepare-runtime.txt').write_text(prep.stdout+prep.stderr)
code=r'''
import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
import {loadProject,lintProject} from './tools/video/core/state.mjs';
import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs';
import {spokenUnits,estimateTimeline,FPS} from './tools/video/core/timeline.mjs';
import {eachLine,spokenText} from './tools/video/core/schema.mjs';
const [source,root]=process.argv.slice(1),read=f=>fs.readFileSync(f,'utf8'),hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex'),d=JSON.parse(read(source+'/video.json')),slug=d.slug,p=loadProject({root,slug});
assert.deepEqual(p.doc,d);assert.equal(p.brief,read(source+'/brief.md'));assert.deepEqual(p.series,JSON.parse(read(source+'/series.json')));
const context={root,canonical_video_sha256:hash(p.file),initialized_dictionary_terms:Object.keys(p.lexicon.terms).length,initialized_dictionary_value_sha256:createHash('sha256').update(JSON.stringify(p.lexicon)).digest('hex'),shelf_dictionary_value_sha256:createHash('sha256').update(JSON.stringify(p.shelfLexicon)).digest('hex')};assert(context.initialized_dictionary_terms>0);
const lint=lintProject(p),timeline=estimateTimeline(d),flat=[...eachLine(d)],sum=xs=>xs.reduce((n,l)=>n+spokenUnits(spokenText(l)),0),total=sum(flat.map(x=>x.line)),first=d.scenes.findIndex((x,i)=>i>0&&x.chapter),opening=sum(d.scenes.slice(0,first).flatMap(x=>x.lines??[])),outro=sum(d.scenes.filter(x=>x.template==='outro').flatMap(x=>x.lines??[])),shots=d.scenes.filter(x=>x.template==='shot');
const shotTimes=timeline.scenes.filter(x=>shots.some(s=>s.id===x.id)).map(x=>({id:x.id,seconds:(x.end_frame-x.start_frame)/FPS}));
const cadence=lint.warnings.filter(x=>/no open loop between/.test(x.message));
assert.equal(d.voice.style,STORY_VOICE_STYLE);assert(!d.series);assert.equal(d.category,'story');
const chapters=[];let current;for(const sc of d.scenes){if(sc.chapter){current={title:sc.chapter,text:''};chapters.push(current);}current.text+=(sc.lines??[]).map(l=>l.text).join('');}
const counts=chapters.map(x=>({chapter:x.title,you:(x.text.match(/你/g)??[]).length,i:(x.text.match(/我/g)??[]).length}));
const positions=new Map();let units=0;for(const {line}of flat){positions.set(line.id,units);units+=spokenUnits(spokenText(line));}
const events=[...new Set(d.loops.flatMap(l=>[positions.get(l.setup),positions.get(l.payoff)]))].sort((a,b)=>a-b),points=[0,...events,units],maxGap=Math.max(...points.slice(1).map((x,i)=>x-points[i]));
console.log(JSON.stringify({scope:'R5 author native mechanical preflight only; no independent source, narrative, visual, audio, media or owner verdict',context,source_video_sha256:hash(source+'/video.json'),brief_sha256:hash(source+'/brief.md'),series_sha256:hash(source+'/series.json'),runtime_script_sha256:hash(p.dir+'/script.md'),lint,cadence_warning_count:cadence.length,native_units:{total,duration_body_including_cold_open_and_voiced_cta:total,opening,body_after_opening:total-opening,outro_narration:outro,body_without_opening_and_outro:total-opening-outro},lines:flat.length,scenes:d.scenes.length,illustration_scenes:shots.length,maximum_estimated_shot_seconds:Math.max(...shotTimes.map(x=>x.seconds)),estimated_total_seconds:timeline.total_frames/FPS,shot_times:shotTimes,chapter_viewer_counts:counts,author_loop_plan:{entries:d.loops.length,distinct_payoffs:new Set(d.loops.map(x=>x.payoff)).size,maximum_gap_units:maxGap,maximum_gap_seconds_at_4_5_units:maxGap/4.5,independent_narrative_verdict:false},exact_native_story_voice:true,actual_timing_verified:false,provider_calls:0,backend_writes:0}));
'''
run=subprocess.run(['node','--input-type=module','-e',code,str(HERE),str(ROOT)],cwd=REPO,capture_output=True,text=True)
if run.returncode:raise RuntimeError(run.stderr)
result=json.loads(run.stdout)
writej('native-author-lint-r5.json',result)
assert not result['lint']['errors'],result['lint']['errors']
assert result['cadence_warning_count']==0,result['lint']['warnings']
assert result['maximum_estimated_shot_seconds']<=12
assert all(c['you'] and c['i'] for c in result['chapter_viewer_counts'])
newtext={n['id']:n['text'] for n in narration}
deleted=[{'id':lid,'text':l['text'],'reason':'由R5具名實際使用／製造回憶深化主線取代；不保留價格、後期產品去鰭片、信件及另一館藏顧客旁支，也不重講同一胡蘿蔔示範。'} for lid,l in oldlines.items() if lid not in newtext]
changed=[{'id':lid,'before':oldlines[lid]['text'],'after':t} for lid,t in newtext.items() if lid in oldlines and oldlines[lid]['text']!=t]
newrow_byid={r['line_id']:r for r in rows}
added=[{'id':lid,'text':newtext[lid],'material_refs':newrow_byid[lid]['material_refs'],'kind':newrow_byid[lid]['kind']} for lid in newids]
for p,h in protection['protected_files'].items():assert sha(p)==h,p
# Dictionaries and events must remain exactly as before ordinary preparation.
for p,h in runtime_before.items():
 if '/story-lexicon/' in p:assert sha(p)==h,p
notes={'status':'HOLD_PENDING_NEW_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_ACTUAL_NATIVE_PANEL4','revision':'r5','author':'/root/c06_translate_en_ja','scope':'C10 current author files and c10-only offline runtime preparation; source research/history/old28 preserved','input_sha256':{n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json','claims.json']},'r4_input_sha256':protection['r4_input_sha256'],'research_expansion_sha256':claims['research_expansion_sha256'],'delta_from_r4':{'added_narration':added,'deleted_narration':deleted,'changed_narration':changed,'opening_nine_scenes_unchanged':True,'retained_narration_count':sum(lid in oldlines for lid in newtext),'retail_carrot_telling_count':1,'r4_deleted_35_summary_lines_restored':[],'changed_chapter_titles':{'把軟的地方留在工具上':'接上刀片，交出樣品','店家擺出胡蘿蔔，讓顧客試削':'拿去試，再交到下一雙手'}},'narration_plan':result['native_units'],'duration_body_definition':'Whole unbranded actual narration timeline including cold open and voiced CTA; excludes added 5s intro / 21s formal outro. after-opening/strict are planning breakdowns only.','actual_narration_seconds':None,'actual_required_extra_units':None,'planning_note':'Aimrough3500有效units只作規劃；按來源實寫，不用純summary/慢播/停頓填長。實聲720–840尚未知，原生估時不能當實聲不足或時長PASS。','native_mechanical':{k:v for k,v in result.items() if k!='shot_times'},'native_lint_receipt_sha256':sha(HERE/'native-author-lint-r5.json'),'protected_files':{'count':len(protection['protected_files']),'all_unchanged':True,'manifest_path':str(AUDIT/'r5-protected-before.json'),'manifest_sha256':sha(AUDIT/'r5-protected-before.json')},'evidence_cache_pairs_rehashed':len(checks),'runtime':{'prepare_command':['node',str(HERE.parent/'prepare-runtime.mjs'),str(ROOT),str(MEDIA),'c10'],'source_equals_runtime':True,'dictionary_changed':False,'stale_runtime_verify_archived_removed':str(archive/'verify-1.md'),'no_current_verify':not (target/'verify-1.md').exists(),'approvals_created':0},'independent_source_pass':False,'independent_visual_pass':False,'native_narrative_pass':False,'verify_written':False,'owner_approval':False,'actual_panel_round_next':4,'actual_panel_audit_name':'round-4-r5','r4_prepared_only_not_actual_panel':True,'last_actual_panel_and_source':'history/r3','translations_created':False,'provider_calls':0,'backend_writes':0,'generated_media':0,'git_actions':0}
reasons={
 'c10a20a':'刪Bruce Hannah後出價格評論，接合章改接真原型與找廠／樣品事件；沒有改寫成1990首價。',
 'c10a20b':'隨價格旁支刪去假想貨架差價選擇，直接沿樣品走到具名店家。',
 'c10a20c':'舊買前試握問題由新f09／Lechters試削及露柄包裝接替，不重複開同一問題。',
 'c10l02':'舊陌生黑柄商店提問由樣品交給店家後的新f09接續，不再另開一次商店。',
 'c10l03a':'鰭片邀請觸摸已在泡狀方案取捨／可見表面處深化一次，刪零售章同義再說。',
 'c10l05':'2017品牌的胡蘿蔔泛述改由PBS具名Lechters／拴碗細節深化同一事件，不並列第二次試削。',
 'c10l08':'刪展示是否擴及其他店的通路問題，以同一使用動作直接走向家庭交手。',
 'c10l09':'品牌泛述展示反應改由Stowell具名店家慢銷到試用的回憶接替。',
 'c10l11':'刪展示擴及許多店的分布總述，不另開通路擴張線。',
 'c10l11a':'轉述來信享受做菜改由Alben具名第一人稱使用感受接替；沒有冒取信件原件。',
 'c10l11b':'轉述買給朋友改由Alben實際交給Jim／Paula試用接替，不再加另一個未具名交手。',
 'c10l11d':'刪後期鰭片是否保留的產品世代問題，保持同一支削皮器使用旅程。',
 'c10l11e':'刪2017許多新工具沒有鰭片的旁支，不做全產品演進。',
 'c10l11f':'刪鰭片在經典／新工具間保留範圍，主線改往具名使用結果。',
 'c10l12':'刪另一件長年使用物件去處的分支提問，以Alben家庭試用直接收尾。',
 'c10l13':'刪Elsa另一顧客與博物館捐贈線，避免在Jim／Paula之外再換人物結果。',
 'c10l14':'隨另一顧客線刪其關節炎及多年使用敘述，原史實仍封存在R4，不移植給Jim／Paula。',
 'c10l15':'刪另一館藏工具工作端提問；工作端的新兩點支承由獨立1990原型目錄窄述。',
 'c10l16':'刪Elsa實物的隨曲面轉動描述；新p02只用另一原型的可轉刀片，不移植同一實物身分。',
 'c10l17':'刪挖芽眼的末段功能旁路，用具名家庭比較與丟舊具接全片結尾。',
 'c10l17a':'隨挖芽眼功能刪假想凹點處理，不加另一個工作流程。'
}
for item in notes['delta_from_r4']['deleted_narration']:item['reason']=reasons[item['id']]
assert len(reasons)==len(deleted)
r4_removed={x['id'] for x in readj(BASE/'author-notes.json')['delta_from_r3']['deleted_narration']}
assert not r4_removed.intersection(newtext)
notes['delta_from_r4']['r4_deleted_35_summary_ids_not_restored']=sorted(r4_removed)
notes['delta_from_r4']['new_narration_spoken_units_planning']=839
notes['delta_from_r4']['removed_narration_spoken_units_planning']=547
notes['delta_from_r4']['net_spoken_units_planning']=292
notes['remaining_native_warnings_scope']='Only handle / peeler lexical picture-repetition advisories remain; same-object journey retained, no unrelated objects added to silence the warnings. Independent written-visual verdict pending.'
notes['actual_media_or_audio_eligibility']=False
writej('author-notes.json',notes)
print(json.dumps({'status':notes['status'],'four_sha256':notes['input_sha256'],'units':result['native_units'],'lines':result['lines'],'scenes':result['scenes'],'added':len(added),'deleted':len(deleted),'changed':len(changed),'errors':result['lint']['errors'],'warnings':result['lint']['warnings'],'cadence_warnings':result['cadence_warning_count'],'max_shot_seconds':result['maximum_estimated_shot_seconds'],'protected_unchanged':len(protection['protected_files'])},ensure_ascii=False,indent=2))
