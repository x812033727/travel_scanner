#!/usr/bin/env python3
"""Build C07 R5 author artifacts from frozen R4; no provider/backend/verify."""
from pathlib import Path
import copy, datetime, hashlib, json, re, subprocess
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
R4=OUT/'history/r4'
ROOT=Path('/workspace/work/brand-story-20261025/c07-submission-root')
SLUG='story-everyday-dr-martens-c07-remake-20261025'
D=json.loads((OUT/'author-data-r5.json').read_text())
sha=lambda x:hashlib.sha256(x).hexdigest()
def file_sha(p):return sha(Path(p).read_bytes())
def binding(p):
 p=Path(p);return {'path':str(p),'bytes':p.stat().st_size,'sha256':file_sha(p)}
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
expected={'video.json':'6c54f169c32f41e85931367d7b94b2257bc2c3afbb5a951e685e46005ae8e74f','script.md':'fccf5cf07db47621ff70ffd83d0bf84586fad854f9e2acd854db84109a9025c7','narration-only.json':'b5922c7d0fb66dfe47821c4802d555ab2be0a8375927ac0c7ab4aef4e6a0e1a7','claims.json':'23d362f2fbea5cd9615ceba68464bb16feaee5f8fe6cc45a0d0060e0f6f1b39b'}
for f,h in expected.items():assert file_sha(R4/f)==h,('Frozen R4 changed',f)
assert file_sha(R4/'reviews/source-r4-independent.json')=='cc5f61b926931a67c35787b967c882f2f2c21aac0cbe75db8a75c646b95cfce5'
assert file_sha(R4/'verify-1.md')=='c51653095967062b227f6493e06ddb7e3ea44126099f677479af898ba1c67cb3'
assert not (OUT/'verify-1.md').exists(),'Current verify would misstate author role; parent must archive before authoring'
protected={str(p):file_sha(p) for p in sorted((OUT/'history').rglob('*')) if p.is_file()}
for f in ['research-original.md','research-original.claims.json']:protected[str(OUT/f)]=file_sha(OUT/f)
for folder in [OUT/'reviews',OUT/'research-expansion',REPO/'docs/videos/story-everyday-dr-martens-c07']:
 for p in sorted(folder.rglob('*')):
  if p.is_file():protected[str(p)]=file_sha(p)
protected[str(OUT/'author-data-r4.json')]=file_sha(OUT/'author-data-r4.json')
old_snapshot=Path('/workspace/work/brand-story-20261025/story-everyday-dr-martens-c07.json')
if old_snapshot.exists():protected[str(old_snapshot)]=file_sha(old_snapshot)

prior=json.loads((R4/'video.json').read_text());priorclaims=json.loads((R4/'claims.json').read_text())
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
anchors={s+'-r5':copy.deepcopy(priorclaims['source_anchors'][s+'-r4']) for s in used}
# The repair-machinery passage remains relevant; annual totals/loyalty are no longer spoken.
anchors['AR26-r5']['short_exact_anchors']=[x for x in anchors['AR26-r5']['short_exact_anchors'] if x['short_quote']=='require dedicated machinery and expertise']
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
  claims.append({'id':i,'scene':sc['id'],'chapter':chapter['title'],'text':r['text'],'source_ids':r['sources'],'evidence':[{'source_id':s,'anchor_id':s+'-r5','locator':r['locator'],'url':sources[s]['url'],'raw_sha256':sources[s]['raw_binding']['sha256'],'evidence_level':sources[s]['evidence_level']} for s in r['sources']],'narrative_mode':mode or ['source_bound_current_account; independent review pending'],'status':'PENDING_NEW_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW','written_visual':{'scene':sc['id'],'prompt':sc['data']['prompt'],'mode':'anonymous concept, not real customer or historical reconstruction','review_state':'NOT_REVIEWED'}})
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
# The three R4 source hard fixes must remain exact. This is an author regression check, not a new verdict.
current={x['id']:x['text'] for x in lines}
for i in ['c7r20217','c7r20218','c7r20219','c7r20319','c7r20320','c7r20520','c7r20606','c7r20607']:assert current[i]==pl[i]['text']
for i in ['c7r20319','c7r20320']:assert next(s for s in scenes if any(l['id']==i for l in s['lines']))['data']==ps[i]['data']
series=copy.deepcopy(json.loads((R4/'series.json').read_text()));series['logline']=D['logline']
claimdoc={'schema_version':1,'episode':'C07 Dr. Martens remake R5','status':'AUTHOR_CANDIDATE_HOLD_PENDING_DIFFERENT_SOURCE_REVIEWER_AND_TWO_FRESH_READERS','research_original_sha256':priorclaims['research_original_sha256'],'r4_binding':{f:binding(R4/f) for f in expected},'r4_historical_source_review':binding(R4/'reviews/source-r4-independent.json'),'r4_historical_verify':binding(R4/'verify-1.md'),'historical_pass_not_inherited':True,'author_role_disclosure':'New R5 author did not write the earlier candidate. This is an author change, not independent source or visual review; another source reviewer and two fresh readers are required.','original_inputs':priorclaims['original_inputs'],'source_inventory':[sources[s] for s in used],'source_anchors':anchors,'narration_claims':claims,'public_review_scope':priorclaims['public_review_scope'],'source_video_scope':priorclaims['source_video_scope'],'new_external_source_claims_added':False,'paid_calls':0,'provider_calls':0,'backend_actions':0,'actual_runtime_verified':False,'source_pass_issued':False,'written_visual_pass_issued':False,'owner_approval_issued':False}
dump('video.json',doc);dump('series.json',series);dump('claims.json',claimdoc);dump('narration-only.json',{'slug':SLUG,'scope':'R5 narration only; author candidate, no verdict','chapters':chapters,'lines':lines});(OUT/'brief.md').write_text(D['brief'])
script=['# '+D['title'],'','R5作者附來源稿；HOLD未核准。R4來源PASS不適用本稿；canonical screenplay由根代理另用原生工具產生。','']
for chapter in D['chapters']:
 script+=['## '+chapter['title'],'']
 for r in claims:
  if r['chapter']==chapter['title']:script+=['['+r['id']+'] '+r['text'],'來源：'+(', '.join(r['source_ids']) or '觀眾問題／訂閱邀請'),'']
(OUT/'script.md').write_text('\n'.join(script)+'\n')
md=['# C07 R5｜逐句來源與書面概念配鏡索引','','作者映射，待另一位獨立來源reviewer及兩位新讀者；不繼承R4 PASS。','','## 原件來源','']
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
console.log(JSON.stringify({scope:'R5 author native lint in existing normally initialized canonical context; candidate substituted in memory only; not verify or independent approval',input_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','author-data-r5.json'].map(f=>[f,sha(path.join(dir,f))])),context_binding:context,immutable_dictionary_unchanged:immutableFiles.every(f=>dictionaryBefore[f]===sha(path.join(p.dir,f))),canonical_bytes_unchanged:sha(p.file)===context.canonical_sha256,voice_exact_native_story_style:d.voice.style===STORY_VOICE_STYLE,native_units:{total,opening,body_after_opening:total-opening,closing_card:closing,body_excluding_opening_and_closing:total-opening-closing,chapters:chapters.map(c=>({name:c.name,lines:c.lines.length,spoken_units:sum(c.lines)}))},native_estimate:{default_cpm:DEFAULT_CPM,minutes:t.total_frames/FPS/60,not_actual_audio:true},scene_estimates:t.scenes.map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS})),result,paid_calls:0,provider_calls:0,backend_actions:0,actual_duration_measured:false}));
"""
r=subprocess.run(['node','--input-type=module','-e',native_code,str(OUT),str(ROOT)],cwd=REPO,capture_output=True,text=True,check=True)
native=json.loads(r.stdout);cadence=[w for w in native['result']['warnings'] if re.search(r'no open loop|open loops? planted|condensation plants',w.get('message',''))];native['cadence_warning_count']=len(cadence)
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
assert max(x['planned_gap_seconds_at_4_5'] for x in hooks)<=45,'A real existing hook must be identified within the paper cadence limit; do not pad narration.'
chapteryou=[]
for chapter in D['chapters']:
 text=''.join(r['text'] for r in chapter['rows']);assert '你' in text and '我' in text
 chapteryou.append({'title':chapter['title'],'you':text.count('你'),'i':text.count('我')})
priororder=list(pl);currentorder=list(current);changed=[i for i in current if i in pl and current[i]!=pl[i]['text']];deleted=[i for i in pl if i not in current];added=[i for i in current if i not in pl]
changedprompts=[s['id'] for s in scenes if s['template']=='shot' and s['id'] in {z['id'] for z in prior['scenes']} and s['data']!=next(z['data'] for z in prior['scenes'] if z['id']==s['id'])]
reasons={
 'c7r20215':'Remove question that starts an unnecessary 2023 management-example branch inside the 2025 repair journey.',
 'c7r20216':'Remove the different twenty-year customer example; do not relabel it as either 2025 public reviewer or the filmed demonstration pair.',
 'c7r20304':'The service-page component scope is merged into the real first-cut action at c7r20301; delete the after-cut summary.',
 'c7r20312':'Delete summary repeating the welt-to-upper attachment and not-yet-attached outsole; keep actual stitching at c7r20311 and c7r20313.',
 'c7r20510':'Remove return to the separate 2023 management demonstration pair during the current workshop sequence.',
 'c7r20511':'Remove the separate management-display shoe and its polishing description with that branch.',
 'c7r20512':'Remove the separate Glastonbury-shoe history with that branch; no shared-pair inference.',
 'c7r20513':'Remove summary of new outsole versus retained upper at the end of the deleted management branch.'}
assert changed==['c7r20301'],changed
assert deleted==list(reasons),deleted
assert not added,added
assert not changedprompts,changedprompts
for s in scenes:
 if s['id']!=ps['c7r20301']['id']:
  assert s==next(z for z in prior['scenes'] if z['id']==s['id']),('Unexpected surviving scene change',s['id'])
for p,h in protected.items():assert file_sha(p)==h,('Protected file changed',p)
shots=sum(units(l['text']) for s in scenes if s['template']=='shot' for l in s['lines']);u=native['native_units']
prior_notes=json.loads((R4/'author-notes.json').read_text())
prior_total=prior_notes['native_units']['total']
notes={
 'schema_version':1,'revision':'C07 R5','status':'HOLD_PENDING_DIFFERENT_INDEPENDENT_SOURCE_WRITTEN_VISUAL_REVIEW_TWO_FRESH_READERS_AND_UNMEASURED_LENGTH',
 'author':'/root/c05_material_author','role':'R5 author; no independent source/visual verdict, narrative vote or verification authored for this candidate',
 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'next_actual_native_reader_round':5,
 'r4_core_bindings':{f:binding(R4/f) for f in ['video.json','script.md','narration-only.json','claims.json','brief.md','series.json','author-notes.json','build-candidate.py','author-data-r4.json','native-initialized-lint.json']},
 'r4_feedback_bindings':[binding(R4/'reviews'/f) for f in ['source-r4-independent.json','narrative-r4-a.raw.json','narrative-r4-b.raw.json','narrative-r4.json','narrative-r4-binding.json']]+[binding(R4/'verify-1.md')],
 'r4_to_r5_delta':{
  'changed_line_ids':changed,'deleted_line_ids':deleted,'added_line_ids':added,
  'line_changes':[{'id':i,'before':pl[i]['text'],'after':current[i]} for i in changed],
  'deletions':[{'id':i,'text':pl[i]['text'],'reason':reasons[i]} for i in deleted],
  'unchanged_surviving_narration_lines':len(lines)-len(changed),
  'moved_surviving_line_ids':['c7r20515'],'moved_question':{'id':'c7r20515','text_unchanged':True,'from':'after c7r20514','to':'before c7r20514','reason':'Ask what repair requires before the component and machinery answers; shortens the 46-second gap left by deleting the 2023 branch without adding text.'},
  'source_binding_change':{'id':'c7r20301','sources':['T7_repairs_resole','R2_REPAIR_VIDEO'],'scope':'Move the page-attributed old sole/welt/stitching removal scope into the first visible cut action; do not claim every component is separately visually identifiable, do not attach demo to the reviewer physical pair.'},
  'loops':{'before':len(prior['loops']),'after':len(doc['loops']),'deleted_setup_payoff':['c7r20215','c7r20216'],'main_question_and_teardown_preview_payoff':'c7r20301','real_new_action':'page-attributed teardown scope with demonstrator inverted boot and knife along upper outsole edge'},
  'shared_failed_items_addressed':['one_line','no_recap'],
  'lone_feedback_not_expanded':['no_toc c7r20104','no_detour c7r20404'],
  'hard_source_fix_text_and_both_tool_prompts_preserved':True,
  'changed_retained_prompt_ids':changedprompts,'new_prompt_scene_ids':[],
  'retained_scene_data_cameras_preserved':True,
  'hook_plan_existing_questions_added':['c7r20305','c7r20518'],'hook_plan_note':'These questions and their visible following actions were already spoken in R4; recording them changes no narration or source fact.','new_external_source_facts_added':False,'research_expansion_micro_actions_used':False,'Australian_other_shoe_or_process_used':False,
  'no_r5_approval_inherited':True},
 'counts':{'narration_lines':len(lines),'scenes':len(scenes),'chapters':len(chapters),'illustration_shots':len(shotids),'cards':1,'loops':len(doc['loops']),'unique_loop_payoffs':len({x['payoff'] for x in doc['loops']})},
 'native_units':{**u,'official_narration_body_planning_units':u['total'],'official_duration_scope':'all actual narration including coldopen and voiced CTA; only separately added 5s intro and 21s outro excluded'},
 'length_risk':{'status':'HOLD_ACTUAL_TTS_UNMEASURED_PLANNING_UNITS_BELOW_ROUGH_TARGET','rough_whole_target_units':3500,'r4_whole_planning_units':prior_total,'r5_whole_planning_units':u['total'],'whole_unit_delta_from_r4':u['total']-prior_total,'delta_from_rough_target':u['total']-3500,'target_actual_narration_seconds':[720,840],'actual_audio_duration':None,'paper_whole_seconds_at_4_to_5_units_per_second':[round(u['total']/5,2),round(u['total']/4,2)],'paper_rate_range_is_not_audio_measurement':True,'known_duration_failure_claimed':False,'duration_pass_claimed':False,'no_padding_slowing_pause_or_recap_added':True},
 'chapter_you_i':chapteryou,'substantive_hook_plan':hooks,'max_planned_hook_gap_seconds_at_4_5':max(x['planned_gap_seconds_at_4_5'] for x in hooks),
 'opening':{'lines':6,'scene_by_line':3,'forward_previews':[{'setup':'c7r20104','topic':'拆開範圍'},{'setup':'c7r20104','topic':'回程新增物'}],'promise_scale':'Dr. Martens, one pair, keeping the familiar upper; unchanged R4 opening'},
 'loop_plan':doc['loops'],
 'visual_plan':{'look':doc['look'],'image_model':'image-01','all_shots_still':all(s['data']['visual']=='still' for s in scenes if s['template']=='shot'),'illustrated_spoken_units':shots,'total_spoken_units':u['total'],'planned_illustration_share':round(shots/u['total'],4),'actual_timing_verified':False,'new_media_created':False,'prompts':'All surviving R4 prompts and cameras unchanged; anonymous concepts, not historical customer or same-pair proof.'},
 'branding_plan':{'intro_seconds':5,'after_opening':True,'outro_version':'formal v4','outro_seconds':21,'selected_assets':None,'not_executed':True},
 'subtitles_plan':{'burn_in_zh_TW':True,'CC_zh_TW':True,'timed_srt_created':False},
 'native_initialized_context_lint':{'path':str(OUT/'native-initialized-lint.json'),'sha256':file_sha(OUT/'native-initialized-lint.json'),'errors':len(native['result']['errors']),'warnings':len(native['result']['warnings']),'cadence_warning_count':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'proper_existing_initialized_context':True,'immutable_dictionary_unchanged':True,'canonical_unchanged':True,'not_independent_verdict':True},
 'protected_input_sha256':protected,'protected_input_count':len(protected),'protected_inputs_all_unchanged':True,
 'research_original_sha256':priorclaims['research_original_sha256'],
 'source_pass_issued':False,'written_visual_pass_issued':False,'native_narrative_pass_issued':False,'verify_written':False,'owner_approval_issued':False,
 'different_source_reviewer_required':True,'fresh_isolated_readers_required':2,'actual_audio_measured':False,'candidate_media_reviewed':False,'translations_written':False,'verification_pipeline_run':False,
 'paid_calls':0,'provider_calls':0,'backend_actions':0,'git_actions':0,'subagents_spawned':0,
 'source_files_sha256':{f:file_sha(OUT/f) for f in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','author-data-r5.json','native-initialized-lint.json']}}
notes['core_four_sha256']={f:file_sha(OUT/f) for f in expected}
dump('author-notes.json',notes)
print(json.dumps({'revision':'C07 R5','counts':notes['counts'],'native_units':u,'native_errors':len(native['result']['errors']),'native_warnings':len(native['result']['warnings']),'cadence_warnings':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'changed_line_ids':changed,'deleted_line_ids':deleted,'added_line_ids':added,'protected_inputs':len(protected),'length_risk':notes['length_risk'],'four_sha256':notes['core_four_sha256']},ensure_ascii=False))
