#!/usr/bin/env python3
"""Build C07 R4 author artifacts from frozen R3; no provider/backend/verify."""
from pathlib import Path
import copy, datetime, hashlib, json, re, subprocess
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
R3=OUT/'history/r3'
ROOT=Path('/workspace/work/brand-story-20261025/c07-submission-root')
SLUG='story-everyday-dr-martens-c07-remake-20261025'
D=json.loads((OUT/'author-data-r4.json').read_text())
sha=lambda x:hashlib.sha256(x).hexdigest()
def file_sha(p):return sha(Path(p).read_bytes())
def binding(p):
 p=Path(p);return {'path':str(p),'bytes':p.stat().st_size,'sha256':file_sha(p)}
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
expected={'video.json':'5b610a91b3a6d37a1a2f388be16035270c70ed43bf4fe3821987ef2da1a4d907','script.md':'4be3167ad1af4deed03280ab6806d80e31dbb39fe574ee32ceb78d44c2a7b7c9','narration-only.json':'195731d668c75ce6d2cf27cc8bb954b340c87e9faaee20c1ba548fbd8d436f37','claims.json':'9ca2ab7682cb5a929eee11ddccdfbfa07705802a696bbea8f8831c6a54aa3aa9'}
for f,h in expected.items():assert file_sha(R3/f)==h,('Frozen R3 changed',f)
assert file_sha(R3/'reviews/source-r3-independent.json')=='e8078c1b3f7d26d955f583498a28b7b9c83c30e83b0ff7248fea5d212d61a6f1'
assert file_sha(R3/'verify-1.md')=='737ea94433d5f21b6d315928be769cf728d2348dffb00bba97336cf54c2f461f'
assert not (OUT/'verify-1.md').exists(),'Current verify would misstate author role; parent must archive before authoring'
protected={str(p):file_sha(p) for p in sorted((OUT/'history').rglob('*')) if p.is_file()}
for f in ['research-original.md','research-original.claims.json']:protected[str(OUT/f)]=file_sha(OUT/f)
prior=json.loads((R3/'video.json').read_text());priorclaims=json.loads((R3/'claims.json').read_text())
for x in priorclaims['original_inputs']:
 assert file_sha(x['path'])==x['sha256'];protected[x['path']]=x['sha256']
for x in priorclaims['source_inventory']:
 for k in ['raw_binding','text_cache','extracted_source']:
  z=x.get(k)
  if z:
   assert file_sha(z['path'])==z['sha256'] and Path(z['path']).stat().st_size==z['bytes'];protected[z['path']]=z['sha256']
for x in priorclaims['source_anchors'].values():
 for k in ['raw_binding','text_cache']:
  z=x.get(k)
  if z:
   assert file_sha(z['path'])==z['sha256'] and Path(z['path']).stat().st_size==z['bytes'];protected[z['path']]=z['sha256']
ps={l['id']:s for s in prior['scenes'] for l in s['lines']}
pl={l['id']:l for s in prior['scenes'] for l in s['lines']}
new_rows=[r for c in D['chapters'] for r in c['rows']]
used=list(dict.fromkeys(s for r in new_rows for s in r['sources']))
sources={x['id']:copy.deepcopy(x) for x in priorclaims['source_inventory'] if x['id'] in used}
assert set(sources)==set(used)
anchors={s+'-r4':copy.deepcopy(priorclaims['source_anchors'][s+'-r3']) for s in used}
# The repair-machinery passage remains relevant; annual totals/loyalty are no longer spoken.
anchors['AR26-r4']['short_exact_anchors']=[x for x in anchors['AR26-r4']['short_exact_anchors'] if x['short_quote']=='require dedicated machinery and expertise']
scenes=[];lines=[];claims=[];chapters=[]
for chapter in D['chapters']:
 chapter_ids=[]
 for idx,r in enumerate(chapter['rows']):
  i=r['id']
  if i in ps and ps[i]['template']=='shot':
   sc=copy.deepcopy(ps[i]);sc['lines']=[{**pl[i],'text':r['text']}]
  elif i=='c7r20107':
   sc={'id':'c07r4-01-07','template':'shot','data':{'prompt':r['prompt'],'visual':'still','camera':'push in'},'lines':[{'id':i,'text':r['text'],'emotion':'對一個人自然說書，問句輕微上揚，數字清楚，句尾收乾淨'}]}
  else:
   # The three closing lines are gathered into the unchanged native card below.
   sc={'id':'c07r4-close-'+i,'template':'shot','data':{'prompt':'Close-up at a simple parcel table, one anonymous adult holding a plain repaired boot, soft daylight from the left.','visual':'still','camera':'hold'},'lines':[{**pl[i],'text':r['text']}]}
  sc.pop('chapter',None)
  if idx==0:sc['chapter']=chapter['title']
  scenes.append(sc);lines.append({'id':i,'text':r['text']});chapter_ids.append(i)
  mode=[]
  if any(s.startswith('R2_CUSTOMER') for s in r['sources']):mode.append('attributed_customer_self_report_or_commentary; not independently verified')
  if 'R2_REPAIR_VIDEO' in r['sources']:mode.append('separate authorised demonstration observation; not reviewer documented pair')
  if i in ['c7r20104','c7r20105','c7r20106'] or r['text'].startswith(('我','如果是我','你')):mode.append('viewpoint_or_viewer_question; no firsthand repair or invented historical psychology')
  if not r['sources']:mode.append('viewer_or_subscription_invitation; not external factual claim')
  claims.append({'id':i,'scene':sc['id'],'chapter':chapter['title'],'text':r['text'],'source_ids':r['sources'],'evidence':[{'source_id':s,'anchor_id':s+'-r4','locator':r['locator'],'url':sources[s]['url'],'raw_sha256':sources[s]['raw_binding']['sha256'],'evidence_level':sources[s]['evidence_level']} for s in r['sources']],'narrative_mode':mode or ['source_bound_current_account; independent review pending'],'status':'PENDING_NEW_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW','written_visual':{'scene':sc['id'],'prompt':sc['data']['prompt'],'mode':'anonymous concept, not real customer or historical reconstruction','review_state':'NOT_REVIEWED'}})
 chapters.append({'title':chapter['title'],'line_ids':chapter_ids})
assert [x['id'] for x in lines[-3:]]==['c7r20619','c7r20620','c7r20621']
outro=copy.deepcopy(prior['scenes'][-1]);outro['lines']=[l for s in scenes[-3:] for l in s['lines']]
scenes=scenes[:-3]+[outro]
for r in claims[-3:]:r['scene']=outro['id'];r['written_visual']={'scene':outro['id'],'template':'outro','data':outro['data'],'mode':'native closing card','review_state':'NOT_REVIEWED'}
doc=copy.deepcopy(prior);doc['scenes']=scenes;doc['loops']=D['loops'];doc['sources']=[{'title':sources[s]['title'],'url':sources[s]['url'],'checked_on':'2026-10-25'} for s in used]
doc['youtube']['description']='一位公開評論中的送修者，先選修理與配色，再把四年舊靴裝進鞋盒。收到收件通知後，用另一次授權維修示範與原廠現行說明，看拆底、車沿條、熱接和整理如何往前推進；最後接回那位送修者的完工消息、回程與新增鞋帶。公共評論保留未經獨立驗證的自述歸因；圖像是匿名概念插圖，示範與評論不是同一實鞋的證據。工序溫度只描述原廠現行接底操作。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(sources[s]['title']+'\n'+sources[s]['url'] for s in used)
assert doc['category']=='story' and doc['slug']==SLUG and doc['look']=={'preset':'cute-mystery'} and doc['subtitles']['burn_in'] is True and doc['voice']==prior['voice']
ids=[x['id'] for x in lines];assert len(ids)==len(set(ids))
for lp in doc['loops']:assert lp['setup'] in ids and lp['payoff'] in ids and ids.index(lp['setup'])<ids.index(lp['payoff'])
# The three R3 source hard fixes must remain exact. This is an author regression check, not a new verdict.
current={x['id']:x['text'] for x in lines}
for i in ['c7r20217','c7r20218','c7r20219','c7r20319','c7r20320','c7r20520','c7r20606','c7r20607']:assert current[i]==pl[i]['text']
for i in ['c7r20319','c7r20320']:assert next(s for s in scenes if any(l['id']==i for l in s['lines']))['data']==ps[i]['data']
series=copy.deepcopy(json.loads((R3/'series.json').read_text()));series['logline']=D['logline']
claimdoc={'schema_version':1,'episode':'C07 Dr. Martens remake R4','status':'AUTHOR_CANDIDATE_HOLD_PENDING_DIFFERENT_SOURCE_REVIEWER_AND_TWO_FRESH_READERS','research_original_sha256':priorclaims['research_original_sha256'],'r3_binding':{f:binding(R3/f) for f in expected},'r3_historical_source_review':binding(R3/'reviews/source-r3-independent.json'),'r3_historical_verify':binding(R3/'verify-1.md'),'historical_pass_not_inherited':True,'author_role_disclosure':'Same agent reviewed frozen R3 sources. Now authoring R4; cannot independently review or verify this candidate. Another source reviewer is required.','original_inputs':priorclaims['original_inputs'],'source_inventory':[sources[s] for s in used],'source_anchors':anchors,'narration_claims':claims,'public_review_scope':priorclaims['public_review_scope'],'source_video_scope':priorclaims['source_video_scope'],'new_external_source_claims_added':False,'paid_calls':0,'provider_calls':0,'backend_actions':0,'actual_runtime_verified':False,'source_pass_issued':False,'written_visual_pass_issued':False,'owner_approval_issued':False}
dump('video.json',doc);dump('series.json',series);dump('claims.json',claimdoc);dump('narration-only.json',{'slug':SLUG,'scope':'R4 narration only; author candidate, no verdict','chapters':chapters,'lines':lines});(OUT/'brief.md').write_text(D['brief'])
script=['# '+D['title'],'','R4作者附來源稿；HOLD未核准。R3來源PASS不適用本稿；canonical screenplay由根代理另用原生工具產生。','']
for chapter in D['chapters']:
 script+=['## '+chapter['title'],'']
 for r in claims:
  if r['chapter']==chapter['title']:script+=['['+r['id']+'] '+r['text'],'來源：'+(', '.join(r['source_ids']) or '觀眾問題／訂閱邀請'),'']
(OUT/'script.md').write_text('\n'.join(script)+'\n')
md=['# C07 R4｜逐句來源與書面概念配鏡索引','','作者映射，待另一位獨立來源reviewer及兩位新讀者；不繼承R3 PASS。','','## 原件來源','']
for s in used:md+=['- '+s+'：['+sources[s]['title']+']('+sources[s]['url']+')；'+sources[s]['evidence_level']+'；raw SHA `'+sources[s]['raw_binding']['sha256']+'`。']
md+=['','## 逐句錨點','','| ID | 旁白 | 來源 | 定位 |','|---|---|---|---|']
for r in claims:md+=['| '+r['id']+' | '+r['text'].replace('|','／')+' | '+', '.join(r['source_ids'])+' | '+(r['evidence'][0]['locator'] if r['evidence'] else '觀眾邀請')+' |']
md+=['','評論是not-verified公共自述，來源示範是另一雙鞋的獨立工序展示，匿名prompt不冒充真實顧客或歷史原件。所有原件／cache SHA、短錨點、日期性質與逐句prompt在claims.json。']
(OUT/'claims.md').write_text('\n'.join(md)+'\n')
native_code=r"""
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {loadProject,lintProject} from './tools/video/core/state.mjs';
import {spokenText} from './tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS,DEFAULT_CPM} from './tools/video/core/timeline.mjs';
import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs';
import {readStoryLexicon} from './tools/video/core/story-lexicon.mjs';
const dir=process.argv[1],root=process.argv[2],slug='story-everyday-dr-martens-c07-remake-20261025';
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');const val=v=>crypto.createHash('sha256').update(JSON.stringify(v)).digest('hex');
const p=loadProject({root,slug});const snap=readStoryLexicon({slug,storyDir:p.dir});
const immutableFiles=['story-lexicon/current.json','story-lexicon/versions/'+snap.lexicon_sha256+'.json','story-lexicon/events/'+snap.head_event_sha256+'.json'];
const dictionaryBefore=Object.fromEntries(immutableFiles.map(f=>[f,sha(path.join(p.dir,f))]));
const context={root,slug,canonical_file:p.file,canonical_sha256:sha(p.file),initialized_terms:Object.keys(p.lexicon.terms??{}).length,lexicon_sha256:val(p.lexicon),shelf_lexicon_sha256:val(p.shelfLexicon),story_lexicon_mode:snap.mode,story_lexicon_raw_sha256:snap.lexicon_sha256,story_lexicon_event_sha256:snap.head_event_sha256,immutable_file_sha256:dictionaryBefore,preserved_fields:['lexicon','shelfLexicon','translations','others','pack','file','dir']};
p.doc=JSON.parse(fs.readFileSync(path.join(dir,'video.json'),'utf8'));p.brief=fs.readFileSync(path.join(dir,'brief.md'),'utf8');p.series=JSON.parse(fs.readFileSync(path.join(dir,'series.json'),'utf8'));
const d=p.doc,result=lintProject(p),flat=d.scenes.flatMap(s=>s.lines??[]),sum=a=>a.reduce((n,l)=>n+spokenUnits(spokenText(l)),0),chapters=[];
for(const s of d.scenes){if(s.chapter)chapters.push({name:s.chapter,lines:[]});chapters.at(-1).lines.push(...s.lines??[])}
const total=sum(flat),opening=sum(chapters[0].lines),closing=sum(d.scenes.at(-1).lines),t=estimateTimeline(d);
console.log(JSON.stringify({scope:'R4 author native lint in existing normally initialized canonical context; candidate substituted in memory only; not verify or independent approval',input_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','author-data-r4.json'].map(f=>[f,sha(path.join(dir,f))])),context_binding:context,immutable_dictionary_unchanged:immutableFiles.every(f=>dictionaryBefore[f]===sha(path.join(p.dir,f))),canonical_bytes_unchanged:sha(p.file)===context.canonical_sha256,voice_exact_native_story_style:d.voice.style===STORY_VOICE_STYLE,native_units:{total,opening,body_after_opening:total-opening,closing_card:closing,body_excluding_opening_and_closing:total-opening-closing,chapters:chapters.map(c=>({name:c.name,lines:c.lines.length,spoken_units:sum(c.lines)}))},native_estimate:{default_cpm:DEFAULT_CPM,minutes:t.total_frames/FPS/60,not_actual_audio:true},scene_estimates:t.scenes.map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS})),result,paid_calls:0,provider_calls:0,backend_actions:0,actual_duration_measured:false}));
"""
r=subprocess.run(['node','--input-type=module','-e',native_code,str(OUT),str(ROOT)],cwd=REPO,capture_output=True,text=True,check=True)
native=json.loads(r.stdout);cadence=[w for w in native['result']['warnings'] if 'no open loop between' in w.get('message','')];native['cadence_warning_count']=len(cadence)
shotids={s['id'] for s in scenes if s['template']=='shot'};native['max_shot_estimated_seconds']=max(s['seconds'] for s in native['scene_estimates'] if s['id'] in shotids);dump('native-initialized-lint.json',native)
assert not native['result']['errors'],native['result']['errors'];assert not cadence,cadence;assert native['max_shot_estimated_seconds']<=12
assert native['voice_exact_native_story_style'] and native['immutable_dictionary_unchanged'] and native['canonical_bytes_unchanged']
TOKEN=re.compile(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]");CJK=re.compile(r'[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]')
def units(t):return sum(1 if CJK.fullmatch(x) else 2 for x in TOKEN.findall(t))
ends={};acc=0
for l in lines:acc+=units(l['text']);ends[l['id']]=acc
hooks=[];prev=0
for h in D['hooks']:
 end=ends[h['id']];assert end>=prev;hooks.append({**h,'end_spoken_units':end,'gap_units':end-prev,'planned_gap_seconds_at_4_5':round((end-prev)/4.5,2)});prev=end
chapteryou=[]
for chapter in D['chapters']:
 text=''.join(r['text'] for r in chapter['rows']);assert '你' in text and '我' in text
 chapteryou.append({'title':chapter['title'],'you':text.count('你'),'i':text.count('我')})
priororder=list(pl);currentorder=list(current);changed=[i for i in current if i in pl and current[i]!=pl[i]['text']];deleted=[i for i in pl if i not in current];added=[i for i in current if i not in pl]
changedprompts=[s['id'] for s in scenes if s['template']=='shot' and s['id'] in {z['id'] for z in prior['scenes']} and s['data']!=next(z['data'] for z in prior['scenes'] if z['id']==s['id'])]
reasons={'c7r20201':'Website-choice fact relocated into new opening c7r20107; no return to before posting.','c7r20202':'Colour-choice enjoyment condensed into new opening c7r20107, stated only once.','c7r20212':'Pure preview/summary of old-versus-new components, no new action or result.','c7r20214':'Repeated opening four-year/upper-good/sole-worn facts, no new result.','c7r20315':'Repeated inverted-boot/supporting-hand posture already shown.','c7r20321':'Repeated welt-attached/sole-separate state immediately before joining.','c7r20604':'Closing flashback through Thursday packing/collection/receipt, already narrated in order.','c7r20616':'Annual corporate loyalty branch does not move the specific returned pair forward.','c7r20617':'Question for removed annual count branch.','c7r20618':'Annual UK volume detour, outside the specific repair journey.'}
for p,h in protected.items():assert file_sha(p)==h,('Protected file changed',p)
shots=sum(units(l['text']) for s in scenes if s['template']=='shot' for l in s['lines']);u=native['native_units']
notes={'schema_version':1,'revision':'C07 R4','status':'HOLD_PENDING_DIFFERENT_INDEPENDENT_SOURCE_WRITTEN_VISUAL_REVIEW_TWO_FRESH_READERS_AND_LENGTH_RISK','author':'/root/c06_translate_en_ja','role':'R4 author; previously R3 source reviewer, therefore prohibited from independent R4 source/visual verdict or verify','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'r3_core_bindings':{f:binding(R3/f) for f in ['video.json','script.md','narration-only.json','claims.json','brief.md','series.json','author-notes.json','build-candidate.py','native-initialized-lint.json']},'r3_feedback_bindings':[binding(R3/'reviews'/f) for f in ['source-r3-independent.json','narrative-r3-a.raw.json','narrative-r3-b.raw.json','narrative-r3.json','narrative-r3-binding.json']]+[binding(R3/'verify-1.md')],'r3_to_r4_delta':{'changed_line_ids':changed,'deleted_line_ids':deleted,'added_line_ids':added,'line_changes':[{'id':i,'before':pl[i]['text'],'after':current[i]} for i in changed],'deletions':[{'id':i,'text':pl[i]['text'],'reason':reasons[i]} for i in deleted],'added_lines':[{'id':i,'text':current[i]} for i in added],'moved_lines':[{'id':'c7r20103','text_unchanged':True,'from_chapter':'刀伸進了舊靴的鞋邊','to_chapter':'選好的靴子裝進了鞋盒','new_position':'after c7r20220, before c7r20230','reason':'Packing and next-day pickup now occur once, after repair/colour choice, before receipt notice.'}],'opening_promise':'One named brand, one pair, retained-upper stake; no numbered components or staged table of contents.','shared_failed_items_addressed':['one_line','no_toc','no_recap','no_detour'],'hard_source_fix_text_and_both_tool_prompts_preserved':True,'changed_retained_prompt_ids':changedprompts,'new_prompt_scene_ids':['c07r4-01-07'],'retained_scene_data_cameras_preserved':not changedprompts,'new_external_source_facts_added':False,'no_r4_approval_inherited':True},'counts':{'narration_lines':len(lines),'scenes':len(scenes),'chapters':len(chapters),'illustration_shots':len(shotids),'cards':1,'loops':len(doc['loops']),'unique_loop_payoffs':len({x['payoff'] for x in doc['loops']})},'native_units':u,'length_risk':{'status':'HOLD_UNMEASURED_AND_TEXT_CAPACITY_BELOW_TARGET','rough_body_target_units':3000,'r3_body_units':2752,'r4_body_units':u['body_after_opening'],'body_unit_delta_from_r3':u['body_after_opening']-2752,'delta_from_rough_target':u['body_after_opening']-3000,'target_actual_body_minutes':[12,14],'actual_audio_duration':None,'paper_body_minutes_at_4_to_5_units_per_second':[round(u['body_after_opening']/5/60,2),round(u['body_after_opening']/4/60,2)],'paper_rate_range_is_not_audio_measurement':True,'natural_4_to_5_delivery_cannot_be_declared_12_to_14_fit':True,'no_padding_slowing_pause_or_recap_added':True,'material_action':'No new research or invented operations added merely to hit length. Keep capacity risk explicit for parent decision; actual production must not be reported duration PASS.'},'chapter_you_i':chapteryou,'substantive_hook_plan':hooks,'max_planned_hook_gap_seconds_at_4_5':max(x['planned_gap_seconds_at_4_5'] for x in hooks),'opening':{'lines':6,'scene_by_line':3,'forward_previews':[{'setup':'c7r20104','topic':'拆開範圍'},{'setup':'c7r20104','topic':'回程新增物'}],'promise_scale':'Dr. Martens, one pair, keeping the familiar upper; no three-component itinerary'},'loop_plan':doc['loops'],'visual_plan':{'look':doc['look'],'image_model':'image-01','all_shots_still':all(s['data']['visual']=='still' for s in scenes if s['template']=='shot'),'illustrated_spoken_units':shots,'total_spoken_units':u['total'],'planned_illustration_share':round(shots/u['total'],4),'actual_timing_verified':False,'new_media_created':False,'prompts':'Anonymous English concepts only; no real customer, brand logo, readable document, historic likeness or shared-pair inference.'},'branding_plan':{'intro_seconds':5,'after_opening':True,'outro_version':'formal v4','outro_seconds':21,'selected_assets':None,'not_executed':True},'subtitles_plan':{'burn_in_zh_TW':True,'CC_zh_TW':True,'timed_srt_created':False},'native_initialized_context_lint':{'path':str(OUT/'native-initialized-lint.json'),'sha256':file_sha(OUT/'native-initialized-lint.json'),'errors':len(native['result']['errors']),'warnings':len(native['result']['warnings']),'cadence_warning_count':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'proper_existing_initialized_context':True,'immutable_dictionary_unchanged':True,'canonical_unchanged':True,'not_independent_verdict':True},'protected_input_sha256':protected,'protected_input_count':len(protected),'protected_inputs_all_unchanged':True,'research_original_sha256':priorclaims['research_original_sha256'],'source_pass_issued':False,'written_visual_pass_issued':False,'native_narrative_pass_issued':False,'verify_written':False,'owner_approval_issued':False,'different_source_reviewer_required':True,'fresh_isolated_readers_required':2,'actual_audio_measured':False,'candidate_media_reviewed':False,'translations_written':False,'verification_pipeline_run':False,'paid_calls':0,'provider_calls':0,'backend_actions':0,'git_actions':0,'source_files_sha256':{f:file_sha(OUT/f) for f in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','author-data-r4.json','native-initialized-lint.json']}}
dump('author-notes.json',notes)
print(json.dumps({'revision':'C07 R4','counts':notes['counts'],'native_units':u,'native_errors':len(native['result']['errors']),'native_warnings':len(native['result']['warnings']),'cadence_warnings':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'changed_line_ids':changed,'deleted_line_ids':deleted,'added_line_ids':added,'protected_inputs':len(protected),'length_risk':notes['length_risk'],'four_sha256':{f:file_sha(OUT/f) for f in expected}},ensure_ascii=False))
