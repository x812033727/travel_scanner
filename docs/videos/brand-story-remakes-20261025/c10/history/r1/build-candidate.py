from pathlib import Path
import json,hashlib,copy,subprocess,re,shutil
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];AUDIT=Path('/workspace/work/brand-story-20261025/c10-audit')
ROOT=AUDIT/'initialized-author-root';MEDIA=AUDIT/'initialized-author-media';SLUG='story-everyday-oxo-c10-remake-20261025'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(HERE/'research-original.md')=='103534b03aa83d10d2d9c2b4c61ac8d0a45bad27384fff79418b44ea5eab4dc7'
assert sha(HERE/'research-original.claims.json')=='972924aa2bef4e3283130c8f4abaaf4446814a0c850699c774538e7113978c5e'
packet=json.loads((HERE/'research-original.claims.json').read_text());facts={x['id']:x for x in packet['new_material_claims']};records={x['id']:x for x in packet['source_records']}
def new_ev(source,locator,excerpt):
 s=records[source];assert s['usable_original_bytes']
 if locator.startswith('PDF '):
  page=int(re.match(r'PDF (\d+)',locator).group(1));file=Path(s['readable_cache_path']).with_name(source+'.page-'+str(page)+'.txt')
  if not file.exists():file.write_text(Path(s['readable_cache_path']).read_text().split('\f')[page-1])
  text=file.read_text()
 else:
  file=Path(s['readable_cache_path']);text=next(x.split('\t',1)[1] for x in file.read_text().splitlines() if x.startswith(locator.split(':')[0]+'\t'))
 assert re.sub(r'\s','',excerpt).lower() in re.sub(r'\s','',text).lower()
 return {'source':source,'url':s.get('final_url') or s['requested_url'],'source_bytes_sha256':s['sha256'],'locator':locator,'readable_cache_path':str(file),'readable_cache_sha256':sha(file),'short_excerpt':excerpt}
extra={
'A01':{'research_claim':'Stowell在2026回憶Sam堅持為一般家庭而做，並以小眾市場不足支撐生意解釋其方向。','evidence':[new_ev('I4','166','economic reality')],'limits_and_forbidden_inferences':'當事人對Sam想法的多年後回憶／經濟觀點，不是所有小眾產品不能營運的定律或OXO財務底帳。'},
'A02':{'research_claim':'2017品牌回顧說TPR當時多用於工業場景，包含汽車與產品內部密封墊。','evidence':[new_ev('S4','017','internal gaskets')],'limits_and_forbidden_inferences':'品牌後出材料選擇回顧；不擴成供應商身分、實際首批工廠製程或配方。'},
'A03':{'research_claim':'1995 MoMA圖錄的Santoprene材料通論說顆粒原料可以射出成形。','evidence':[new_ev('C3','PDF 85: printed80 / material description','granular raw material')],'limits_and_forbidden_inferences':'一般材料說明與OXO條目分開；不用同頁／鄰頁其他作品的雙次射出、鋼模步驟套到OXO。'},
'A04':{'research_claim':'1990原握柄專利在目標中列可相對低成本大量製造。','evidence':[new_ev('P0','PDF 4: printed2 / Summary of Invention','mass produced')],'limits_and_forbidden_inferences':'專利目標，不是實際成本／產量／量產線紀錄。'},
'A05':{'research_claim':'品牌2017回顧將小鰭片另解釋為邀請消費者觸摸的視覺線索。','evidence':[new_ev('S4','018','invite people')],'limits_and_forbidden_inferences':'品牌的後出行銷／造型說明，不推定每個顧客心理或抹去設計者對物理作用的回顧。'},
'A06':{'research_claim':'Stowell2026回憶收到使用者來信，自述多年來再度享受下廚，並有人購買送朋友。','evidence':[new_ev('I4','169','letters')],'limits_and_forbidden_inferences':'Stowell轉述來信，不是本包已取得信件原件或臨床病例；不推所有顧客、療效或可核銷售。'},
'A08':{'research_claim':'原專利兩側凹處外緣為橢圓，以大致配合拇指與食指指端，claim3另定其長軸平行握柄長軸。','evidence':[new_ev('P0','PDF 5: printed3 / concave depressions18A18B','elliptical'),new_ev('P0','PDF 6: claim3','long axis')],'limits_and_forbidden_inferences':'只說明文件披露的形狀與意圖，非每雙手都精確吻合或實際零售商品的尺寸證明。'},
'A07':{'research_claim':'Bruce Hannah在PBS後出評論說OXO削皮器比標準產品貴。','evidence':[new_ev('I3','006','more expensive')],'limits_and_forbidden_inferences':'Bruce Hannah的後代評論，不是Sam在LA Times2000的原採訪，不指確切1990價格／店家／日期或全市場。'}
}
facts.update(extra)
chapters={};rows=[];current=None
for raw in (HERE/'narration-r1.tsv').read_text().splitlines():
 if not raw:continue
 if raw.startswith('# '):current,title=raw[2:].split('|',1);chapters[current]=title;continue
 ident,kind,refs,text=raw.split('|',3);assert ident.startswith(current)
 refs=[x for x in refs.split(',') if x];assert all(x in facts for x in refs)
 rows.append({'short_id':ident,'id':'c10'+ident,'scene_id':'c10r1-'+ident,'chapter_key':current,'kind':kind,'refs':refs,'text':text})
assert len({x['id'] for x in rows})==len(rows)==139
prompts=dict(s.split('|',1) for s in (HERE/'prompts-r1.tsv').read_text().splitlines() if s)
assert set(prompts)=={r['short_id'] for r in rows if not (r['kind'].endswith('cta') or r['kind']=='final_answer')}
voice={'provider': 'gemini', 'name': 'Sulafat', 'style': '標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。語速像平常聊天，一秒四到五個字，句與句之間不拖。絕不平、絕不像在念稿。', 'performance': '對一個人說材料怎麼換工作；企業與館方回顧自然保留歸屬。假設動作不演成歷史現場。'}
voice['performance']='對一位觀眾講握柄怎麼接到不同的手；來源回顧自然保留歸屬，假想動作不演成歷史現場。'
names=['OXO','Good Grips','Sam Farber','Betsey Farber','Sam','Betsey','Farber','Smart Design','Davin Stowell','Michael Callahan','Dan Formosa','Daniel Formosa','Bruce Hannah','Elsa Edwards','Santoprene','PBS','MoMA','Cooper Hewitt']
series={'kind':'story','slug':'brand-stories-everyday-reversals','episode':10,'chapter':1,'target_minutes':13,'title':'OXO：1990年，削皮器為什麼先改握柄？','logline':'一個握柄從黏土與不同手的試作，走向形狀、材料及連接方案，再交給貨架前的人親手試。','names':names,'characters':[],'visual_tier':'stills','compilation':False,'beats':[{'chapter':k,'title':title,'point':{'h':'手先卡住，單一物件的承諾。','o':'黏土先接到一雙手，設計範圍接到更多人。','r':'尺寸兩端與橢圓方向，指腹接觸區繼續推進。','m':'可彎小鰭片需要合適材料，也得能做成部件。','a':'專利文件內腔、固定及孔口方案，接到使用與收回。','l':'零售可摸的機會、後代回饋及實際使用物件。'}[k]} for k,title in chapters.items()], 'production_requirements':{'image_model':'MiniMax image-01','look':{'preset':'cute-mystery'},'illustration_actual_body_time_minimum':0.70,'max_consecutive_cards':3,'motion':'still pictures with camera movement','voice_style_contract':'exact native STORY_VOICE_STYLE; natural4–5 spoken units per second; no padding pauses','measured_narration_body_seconds':[720,840],'burned_zhTW_and_cc':True,'intro':{'seconds':5,'after_line_id':'c10h09','formal_asset_selected':False},'outro':{'seconds':21,'version':'v4','formal_asset_selected':False},'additional_languages_default':['en','ja','ko','es','pt','id','vi','th'],'backend_language_choice_written':False,'all_media_unexecuted':True}}
source_ids=sorted({ev['source'] for r in rows for ref in r['refs'] for ev in facts[ref]['evidence']})
sources=[{'title':records[k]['research_title'],'url':records[k].get('final_url') or records[k]['requested_url'],'checked_on':'2026-10-25'} for k in source_ids]
title='OXO：1990年，削皮器為什麼先改握柄？｜品牌故事'
desc='一支削皮器，握柄怎麼從卡住一雙手，走到交給別人試？沿著黏土原型、尺寸與方向、可彎小鰭片、材料和內部連接，以及店裡一碗胡蘿蔔，追同一個握柄怎麼替人留下控制工具的位置。\n\n起因與早期過程依品牌、設計者及館方後代回顧。1989設計年、1990推出、專利申請／核發與館藏日期各守範圍；專利方案不是首款商品的製程紀錄，使用者來信是設計者轉述，不推醫療效果或銷售因果。畫面是匿名概念插圖。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(s['title']+'\n'+s['url'] for s in sources)
doc={'schema_version':1,'slug':SLUG,'format':'drama','category':'story','narration_locale':'zh-TW','target_minutes':[12,14],'voice':voice,'subtitles':{'burn_in':True},'look':{'preset':'cute-mystery'},'characters':[],'music':{'prompt':'light, curious, a little mysterious, no vocals','gain_db':-20,'duck_db':-10},'loops':[],'youtube':{'category_id':27,'made_for_kids':False,'default_language':'zh-TW','title':title,'description':desc,'tags':['OXO','Good Grips','削皮器','握柄','設計故事','品牌故事','日用品的意外轉身'],'video_id':None},'thumbnail':{'template':'thumb','data':{'layout':'d','brand':'OXO','headline':'握不住怎麼削','sub':'1990先改握柄','tag':'品牌故事','shot':'c10r1-h01'}},'sources':sources,'assets':[],'scenes':[]}
assert 'series' not in doc
cameras=['push in','pan left','pull back','pan right'];seen=set();outro_lines=[]
for i,r in enumerate(rows):
 emotion='自然接話，對一位觀眾說' if r['kind'] not in ['attributed_fact','attributed_opinion'] else '自然說書，來源歸屬清楚但不拖慢'
 if '？' in r['text']:emotion='好奇上揚，不拉長停頓'
 if r['kind']=='opinion':emotion='像跟朋友分享自己的反應'
 line={'id':r['id'],'text':r['text'],'emotion':emotion}
 if (r['kind'].endswith('cta') or r['kind']=='final_answer'):outro_lines.append(line);continue
 scene={'id':r['scene_id'],'template':'shot','data':{'prompt':prompts[r['short_id']],'visual':'still','camera':cameras[i%len(cameras)]},'lines':[line]}
 if r['chapter_key'] not in seen:scene['chapter']=chapters[r['chapter_key']];seen.add(r['chapter_key'])
 doc['scenes'].append(scene)
doc['scenes'].append({'id':'c10r1-outro','template':'outro','data':{'title':'把工具交給另一雙手','cta':'你想替哪件工具換掉握的地方？'},'lines':outro_lines})
loops=[('h06','o06','黏土怎麼接到舊金屬柄'),('h07','l05','陌生黑柄怎麼交給人試'),('h09','l19','換一雙手，握柄究竟改什麼'),('o11','o14','一雙手以外還要了解哪些人'),('o22','r05','柄的大小如何卡住收回的手指'),('r08','r11','輪廓如何接到手裡的方向'),('r16','m03','表面如何接到指腹'),('r21','m03','兩根手指可以壓在哪'),('m06','m08','可彎小片要由什麼材料做出'),('m13','m14','濕手還得面對什麼材料條件'),('m19','a02','軟的外柄如何接上工作端'),('a07','a08','往回拉時握柄如何留在工具上'),('a10','a12','不靠黏結時形狀如何抵抗抽出'),('a15','a18a','尾端開口如何接到不同的動作'),('a20c','l05','付錢前怎麼有機會親手試'),('l11d','l11e','早期招呼試握的小片還得一直留下嗎'),('l12','l13','一件用過的工具留下什麼去處')]
doc['loops']=[{'setup':'c10'+a,'payoff':'c10'+b,'what':why} for a,b,why in loops]
for filename,value in [('video.json',doc),('series.json',series),('narration-only.json',[{'id':r['id'],'scene':r['scene_id'] if not (r['kind'].endswith('cta') or r['kind']=='final_answer') else 'c10r1-outro','chapter':chapters[r['chapter_key']],'text':r['text']} for r in rows])]:
 (HERE/filename).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
brief=f'''# C10 OXO｜r1 新規則作者候選

## 本次建議

### 選項 A：一個握柄，怎麼交給另一雙手？

只追一支削皮器的握柄：黏土包住舊金屬柄，不同手的研究接到尺寸與橢圓方向，指腹鰭片需要材料，軟外柄要接上工作端，最後讓貨架前的人自己試。正式成片及八語媒體未執行。

## 問題

換了拿它的手，握柄究竟得改掉什麼？

## 一句答案

要交給另一雙手，握柄得先替人讓出能自己控制工具的位置。正文以具體物件與動作推進；不以普遍療效、銷量成長或所有手都適用作答案。

## 站主觀點

建議的旁白觀點是：日用品不只把一個完成的形狀交給人，還得容納實際拿它的手。以「我」標出編輯反應，以「你／想像」限定示意動作；這是作者建議，尚未取得站主核准。

## 敘事與來源

開場先給觀眾握不住工具的利害及1989設計年，四句內進普羅旺斯廚房的假想握持；只預告黏土與等待人伸手的黑柄，點名OXO和一支削皮器的尺度，最後落主問句。正文六章依握柄的狀態向前：黏土／不同手、尺寸與方向、指腹與材料、內部連接、試握與使用物件。每個研究事實由claims綁回實際已讀原件；作者推理及假想動作另標kind，不寫成史實。

三份research-original／preservation檔案完全保護。原1990專利的結構方案以文件身分出場，不當作首款商品的實際工廠流程。MoMA1995圖錄的OXO條目只用左欄，右欄滑雪杖的雙次射出未採。關節炎起因、早期回顧、品牌材料說法與設計者轉述來信均窄歸因；LA Times／Fast Company未重開的Sam價格或數百泡棉說法不使用。價格比較另窄歸因PBS收錄的Bruce Hannah後出評論，未稱為Sam2000採訪或確切1990價格。

## 製作規格

目標13分鐘，正文自然4–5spokenUnits/s，實測720–840秒待執行。Gemini Sulafat使用exact原生STORY_VOICE_STYLE；MiniMax image-01、look只{{"preset":"cute-mystery"}}。英文匿名概念圖、still與簡單運鏡，實際插圖時間至少70%／最多連3卡待真實時間軸驗證。繁中燒錄＋CC；濃縮開場後5秒正式片頭、末尾21秒正式v4片尾，未假造正式素材身分。縮圖layout d，OXO品牌字、黃黑框主標、白短副標；後製排字，不交圖片模型畫logo或文字。

## 狀態

作者r1，HOLD待獨立來源／書面配鏡、兩位全新讀者、念法及站主關卡；沒有SOURCE／敘事／visual PASS、verify或核准。全新slug不綁原episode；沒有改原集、其他集、canonical、後台或provider，沒有八語翻譯、音訊、影片、費用或Git動作。
'''
(HERE/'brief.md').write_text(brief)
script=['# C10 OXO｜r1 作者附來源稿','','作者候選，非canonical核准劇本。ID／章名／來源／註解不進旁白。','']
last=None
for r in rows:
 if r['chapter_key']!=last:
  script += ['', '## '+chapters[r['chapter_key']],'','| ID | 旁白 | 來源材料／性質 |','|---|---|---|'];last=r['chapter_key']
 script.append('| '+r['id']+' | '+r['text']+' | '+(', '.join(r['refs']) or '觀眾互動／CTA')+'；'+r['kind']+' |')
 script.append('') if r is rows[-1] else None
(HERE/'script.md').write_text('\n'.join(script)+'\n')
claims_rows=[]
for r in rows:
 evs=[];limits=[]
 for key in r['refs']:
  evs.extend(copy.deepcopy(facts[key]['evidence']));limits.append(facts[key]['limits_and_forbidden_inferences'])
 claims_rows.append({'line_id':r['id'],'scene_id':r['scene_id'] if not (r['kind'].endswith('cta') or r['kind']=='final_answer') else 'c10r1-outro','text':r['text'],'kind':r['kind'],'material_refs':r['refs'],'evidence':evs,'limits':limits,'written_visual':{'conceptual':True,'not_historical_reconstruction':True,'prompt':prompts.get(r['short_id']),'narration_binding':r['id']},'independent_verdict':'NOT_REVIEWED'})
claims={'schema_version':1,'revision':'r1','slug':SLUG,'scope':'author source anchors only; not independent SOURCE or visual PASS','input_sha256':{f:sha(HERE/f) for f in ['video.json','script.md','narration-only.json']},'protected_research_sha256':{f:sha(HERE/f) for f in ['research-original.md','research-original.claims.json','original-preservation.json']},'source_records':packet['source_records'],'additional_author_materials':extra,'claims':claims_rows,'source_qa':False,'visual_qa':False,'actual_audio_measured':False,'paid_requests':0,'backend_writes':0}
(HERE/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
md=['# C10 OXO｜r1 作者逐句來源錨點','','研究材料索引Nxx見research-original.claims.json；Axx為本作者從同一已取得原件補用的窄段。完整短摘錄、locator與cacheSHA在claims.json。這不是獨立查核。','','| ID | 種類 | 原件材料 | 界線 |','|---|---|---|---|']
for r in claims_rows:md.append('| '+r['line_id']+' | '+r['kind']+' | '+(', '.join(r['material_refs']) or 'CTA')+' | '+('；'.join(dict.fromkeys(r['limits'])) if r['limits'] else '不作史實')+' |')
(HERE/'claims.md').write_text('\n'.join(md)+'\n')
# Proper offline immutable dictionary initialization. It precedes the first project video copy.
code=r'''
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
import {initializeStoryLexicon} from './tools/video/core/lexicon-store.mjs';import {loadProject,lintProject} from './tools/video/core/state.mjs';import {writeScreenplay} from './tools/video/core/screenplay.mjs';import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs';import {spokenUnits,estimateTimeline,FPS} from './tools/video/core/timeline.mjs';import {eachLine,spokenText} from './tools/video/core/schema.mjs';
const [source,root,media]=process.argv.slice(1),d=JSON.parse(fs.readFileSync(source+'/video.json')),s=JSON.parse(fs.readFileSync(source+'/series.json')),slug=d.slug,shelf=root+'/docs/videos',target=shelf+'/'+slug,workdir=media+'/'+slug;
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
fs.mkdirSync(shelf,{recursive:true});const shared=fs.readFileSync('./docs/videos/lexicon.json');if(fs.existsSync(shelf+'/lexicon.json'))assert(fs.readFileSync(shelf+'/lexicon.json').equals(shared));else fs.writeFileSync(shelf+'/lexicon.json',shared);
assert.equal(d.voice.style,STORY_VOICE_STYLE);assert(!d.series);assert.equal(d.category,'story');
for(const f of ['auto.json','approvals.json','timeline.json','narration.wav','final.mp4'])assert(!fs.existsSync(workdir+'/'+f));
fs.mkdirSync(target,{recursive:true});const lexicon=initializeStoryLexicon({root,slug,workdir,names:s.names});for(const f of ['video.json','brief.md','series.json','claims.md'])fs.copyFileSync(source+'/'+f,target+'/'+f);
writeScreenplay(target,d);const p=loadProject({root,slug}),lint=lintProject(p),timeline=estimateTimeline(d),flat=[...eachLine(d)],sum=xs=>xs.reduce((n,l)=>n+spokenUnits(spokenText(l)),0),total=sum(flat.map(x=>x.line)),first=d.scenes.findIndex((x,i)=>i>0&&x.chapter),opening=sum(d.scenes.slice(0,first).flatMap(x=>x.lines??[])),outro=sum(d.scenes.filter(x=>x.template==='outro').flatMap(x=>x.lines??[])),shots=d.scenes.filter(x=>x.template==='shot');
const shotTimes=timeline.scenes.filter(x=>shots.some(s=>s.id===x.id)).map(x=>({id:x.id,seconds:(x.end_frame-x.start_frame)/FPS}));
console.log(JSON.stringify({scope:'author native mechanical preflight only; no independent verdict',context_root:root,context_media:media,source_video_sha256:hash(source+'/video.json'),canonical_script_sha256:hash(target+'/script.md'),lexicon_sha256:lexicon.lexicon_sha256,lint,native_units:{total,opening,body_after_opening:total-opening,outro_narration:outro,body_without_opening_and_outro:total-opening-outro},lines:flat.length,scenes:d.scenes.length,illustration_scenes:shots.length,maximum_estimated_shot_seconds:Math.max(...shotTimes.map(x=>x.seconds)),estimated_total_seconds:timeline.total_frames/FPS,shot_times:shotTimes,actual_timing_verified:false,provider_calls:0,backend_writes:0}));
'''
run=subprocess.run(['node','--input-type=module','-e',code,str(HERE),str(ROOT),str(MEDIA)],cwd=REPO,capture_output=True,text=True)
if run.returncode:raise RuntimeError(run.stderr)
result=json.loads(run.stdout);(AUDIT/'native-author-lint-r1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(HERE/'native-author-lint-r1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
assert not result['lint']['errors'],result['lint']['errors']
notes={'status':'HOLD_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_FRESH_READERS','revision':'r1','author':'/root/c06_translate_en_ja','source_research_authorship_disclosed':True,'protected_research_sha256':claims['protected_research_sha256'],'input_sha256':{f:sha(HERE/f) for f in ['video.json','script.md','narration-only.json','claims.json']},'narration_plan':result['native_units'],'planning_body_target_approx_units':[3300,3500],'planning_note':'正文實算3261 units（含結尾旁白），略低於約3300–3500規劃，不另加無來源或重述湊數。未實際量音；若正文不足720秒須有效改寫，不能慢播／停頓補長。','native_mechanical':{k:v for k,v in result.items() if k!='shot_times'},'delta_from_original':'New narration and images under a new slug; no old content approvals or media reused. Original80 lines retained only in frozen research inventory.','independent_source_pass':False,'independent_visual_pass':False,'native_narrative_pass':False,'verify_written':False,'owner_approval':False,'actual_narration_seconds':None,'translations_created':False,'provider_calls':0,'backend_writes':0,'generated_media':0}
(HERE/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
for name,digest in claims['protected_research_sha256'].items():assert sha(HERE/name)==digest
for name,digest in packet['original_preservation']['all_original_files_sha256'].items():assert sha(REPO/name)==digest
print(json.dumps({'input_sha256':notes['input_sha256'],'units':result['native_units'],'lines':result['lines'],'scenes':result['scenes'],'illustration_scenes':result['illustration_scenes'],'lint_errors':result['lint']['errors'],'warnings':result['lint']['warnings'],'maximum_estimated_shot_seconds':result['maximum_estimated_shot_seconds'],'status':notes['status']},ensure_ascii=False))
