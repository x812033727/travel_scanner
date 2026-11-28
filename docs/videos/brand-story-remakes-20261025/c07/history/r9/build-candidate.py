#!/usr/bin/env python3
"""C07 R9 opening two-event same-image plan from immutable unreviewed R8; no source self-review."""
from pathlib import Path
import copy,datetime,hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
BASE=OUT/'history/r8'
ROOT=Path('/workspace/work/brand-story-20261025/c07-submission-root')
SLUG='story-everyday-dr-martens-c07-remake-20261025'
file_sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def binding(p):
    p=Path(p);return {'path':str(p),'bytes':p.stat().st_size,'sha256':file_sha(p)}
def readj(p):return json.loads(Path(p).read_text())
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

expected={'video.json':'037f7a673481337e6d0bf0c591e7b37b8443b0b1e82216722f9ee5c528b84262','script.md':'b9df40b98cd53582674445f2490d363cfbab73125251c9eaef658ff0b834a5b3','narration-only.json':'e6717dd0018a4d7cc9c5dadf0736190d14b3440da4647cea5f01d459020ce148','claims.json':'5d66f2ce62d61dade5e9ecdbaa90170671eef5fcab74f94a74111c6ba2583b90'}
for f,h in expected.items():assert file_sha(BASE/f)==h,('Frozen R8 changed',f)
assert not (OUT/'verify-1.md').exists()
assert readj(BASE/'review-state.json')['source_and_written_visual_review_for_this_exact_revision'] is False
PROTECTED=readj(BASE/'author-notes.json')['protected_input_sha256']
PROTECTED.update({str(f):file_sha(f) for f in (OUT/'history').rglob('*') if f.is_file()})
PROTECTED.update({str(f):file_sha(f) for f in (OUT/'research-expansion').rglob('*') if f.is_file()})
for f in ['author-data-r4.json','author-data-r5.json','author-data-r6.json','author-data-r7.json','author-data-r8.json']:PROTECTED[str(OUT/f)]=file_sha(OUT/f)
for f,h in PROTECTED.items():assert file_sha(f)==h,f
D=readj(OUT/'author-data-r9.json');prior=readj(BASE/'video.json');priorclaims=readj(BASE/'claims.json')
priorlines={l['id']:l['text'] for s in prior['scenes'] for l in s['lines']}
rows={r['id']:r for c in D['chapters'] for r in c['rows']}
first='c7r20104';second='c7h04b1';source_first='c7r20301';source_second='c7r20607'
oldscene=next(s for s in prior['scenes'] if s['lines'][0]['id']==first)
first_payoff=next(s for s in prior['scenes'] if s['lines'][0]['id']==source_first)
second_payoff=next(s for s in prior['scenes'] if s['lines'][0]['id']==source_second)
prompt_a=rows[first]['prompt'];prompt_b=rows[second]['prompt']
new_scene_id='c07r9-01-04b'
doc=copy.deepcopy(prior);scenes=[]
for s in doc['scenes']:
    key=s['lines'][0]['id']
    if key==first:
        s['lines'][0]['text']=rows[first]['text'];s['data']['prompt']=prompt_a;s['data']['camera']=first_payoff['data']['camera'];scenes.append(s)
        added=copy.deepcopy(oldscene);added['id']=new_scene_id;added['lines'][0]['id']=second;added['lines'][0]['text']=rows[second]['text'];added['data']['prompt']=prompt_b;added['data']['camera']=second_payoff['data']['camera'];scenes.append(added)
    else:
        if key==source_first:s['data']['prompt']=prompt_a
        if key==source_second:s['data']['prompt']=prompt_b
        scenes.append(s)
doc['scenes']=scenes;doc['loops']=copy.deepcopy(D['loops'])
assert len(scenes)==len(prior['scenes'])+1 and doc['characters']==[]
for s in scenes:
    if s['id']==new_scene_id:continue
    before=next(q for q in prior['scenes'] if q['id']==s['id'])
    if s['id'] not in [oldscene['id'],first_payoff['id'],second_payoff['id']]:assert s==before
    else:
        assert {k:v for k,v in s.items() if k not in ['data','lines']}=={k:v for k,v in before.items() if k not in ['data','lines']}
        assert {k:v for k,v in s['data'].items() if k not in ['prompt','camera']}=={k:v for k,v in before['data'].items() if k not in ['prompt','camera']}
        if s['id']!=oldscene['id']:assert s['lines']==before['lines']
assert {k:v for k,v in doc.items() if k not in ['scenes','loops']}=={k:v for k,v in prior.items() if k not in ['scenes','loops']}
ids=[l['id'] for s in scenes for l in s['lines']]
for lp in doc['loops']:assert ids.index(lp['setup'])<ids.index(lp['payoff'])
series=readj(BASE/'series.json');dump('video.json',doc);dump('series.json',series);(OUT/'brief.md').write_text(D['brief'])
claims=copy.deepcopy(priorclaims);oldclaims={r['id']:r for r in priorclaims['narration_claims']}
claims.update(episode='C07 Dr. Martens remake R9',status='AUTHOR_CANDIDATE_PENDING_NEW_INDEPENDENT_SOURCE_AND_VISUAL_QA',r8_binding={f:binding(BASE/f) for f in expected},r8_review_state=binding(BASE/'review-state.json'),historical_pass_not_inherited=True,source_pass_issued=False,written_visual_pass_issued=False,owner_approval_issued=False,author_role_disclosure='R9 author and local request-key plan only; unreviewed R8 is archived. Source/visual and fresh narrative verdicts must come from other agents.')
claimrows=[]
for r in claims['narration_claims']:
    if r['id']==first:
        r['text']=rows[first]['text'];r['source_ids']=['T7_repairs_resole','R2_REPAIR_VIDEO'];r['evidence']=copy.deepcopy(oldclaims[source_first]['evidence']);r['written_visual']['prompt']=prompt_a
        r['narrative_mode']=['viewer teaser question; different authorised demonstration context, not proof of the public commenter physical boot']
        claimrows.append(r)
        z=copy.deepcopy(oldclaims[first]);z['id']=second;z['scene']=new_scene_id;z['text']=rows[second]['text'];z['source_ids']=['R2_CUSTOMER_6870'];z['evidence']=copy.deepcopy(oldclaims[source_second]['evidence']);z['written_visual']['scene']=new_scene_id;z['written_visual']['prompt']=prompt_b;z['narrative_mode']=['viewer teaser question; unverified July public account; neutral closed parcel with surprise contents withheld; no invented unboxing sequence'];claimrows.append(z)
    else:
        if r['id']==source_first:r['written_visual']['prompt']=prompt_a
        if r['id']==source_second:r['written_visual']['prompt']=prompt_b
        claimrows.append(r)
claims['narration_claims']=claimrows
pairs=[(first,source_first,'knife-before-cut-shared-still'),(second,source_second,'return-parcel-shared-still')]
for a,b,asset in pairs:
    sa=next(s for s in scenes if s['lines'][0]['id']==a);sb=next(s for s in scenes if s['lines'][0]['id']==b)
    for row in claimrows:
        if row['id'] in [a,b]:row['planned_same_image']={'plan':'image-reuse-plan.json','asset_plan_id':asset,'source_scene_id':sb['id'],'reuse_scene_id':sa['id'],'actual_file_sha256':None,'status':'PLAN_ONLY'}
for key in ['source_inventory','source_anchors','original_inputs','public_review_scope','source_video_scope']:assert claims[key]==priorclaims[key]
dump('claims.json',claims)
chapters=[{'title':c['title'],'line_ids':[r['id'] for r in c['rows']]} for c in D['chapters']];lines=[{'id':r['id'],'text':r['text']} for c in D['chapters'] for r in c['rows']]
assert lines==[{'id':l['id'],'text':l['text']} for s in scenes for l in s['lines']]
dump('narration-only.json',{'slug':SLUG,'scope':'R9 author narration only, two teasers split in payoff order; no verdict','chapters':chapters,'lines':lines})
script=['# '+D['title'],'','R9作者附來源稿；待新查核與隔離讀者。R8未受來源／敘事審查。兩項預告各與回收章規劃同一中性圖，sidecar見image-reuse-plan.json；實檔未生成／驗證，不是owner核准或canonical劇本。','']
for ch in D['chapters']:
    script+=['## '+ch['title'],'']
    for row in claimrows:
        if row['chapter']==ch['title']:script+=['['+row['id']+'] '+row['text'],'來源：'+(', '.join(row['source_ids']) or '觀眾問題／訂閱邀請'),'']
(OUT/'script.md').write_text('\n'.join(script)+'\n')
md=['# C07 R9｜逐句來源與書面概念配鏡索引','','作者映射，待不同來源reviewer及兩位新讀者；R8沒有來源或敘事PASS可繼承。','','## 原件來源','']
for source in claims['source_inventory']:md+=['- '+source['id']+'：['+source['title']+']('+source['url']+')；'+source['evidence_level']+'；raw SHA '+source['raw_binding']['sha256']+'。']
md+=['','## 逐句錨點','','| ID | 旁白 | 來源 | 定位 |','|---|---|---|---|']
for row in claimrows:md+=['| '+row['id']+' | '+row['text'].replace('|','／')+' | '+', '.join(row['source_ids'])+' | '+(row['evidence'][0]['locator'] if row['evidence'] else '觀眾邀請')+' |']
md+=['','## 開場共圖計畫','','20104→20301用刀尚未切下的中性工坊示意；20104b→20607用內容不可見的閉合包裹示意，依正文順序。image-reuse-plan.json逐對列完整參數及純local原生compose/imageKey相等證明。payoff先--takes 1通過；teaser命令前重算live key並讀cache entry與實檔SHA，一項缺漏即停，不讓cache miss另購第二張；兩端各judge，retake停pair，最終核含trim的相同file/SHA。actual_same_asset_verified=false。','','兩則not-verified評論、倫敦店與授權示範是不同人／鞋／事件；共用匿名概念圖不證明同一實物，不捏造拆箱順序。材料、範圍及原廠現行工法歸因仍按逐句來源，未從圖像辨認PVC或量工具溫度。本作者不給來源或配鏡PASS。']
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
console.log(JSON.stringify({scope:'R9 author native lint in existing normally initialized canonical context; candidate substituted in memory only; not verify or independent approval',input_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','author-data-r9.json'].map(f=>[f,sha(path.join(dir,f))])),context_binding:context,immutable_dictionary_unchanged:immutableFiles.every(f=>dictionaryBefore[f]===sha(path.join(p.dir,f))),canonical_bytes_unchanged:sha(p.file)===context.canonical_sha256,voice_exact_native_story_style:d.voice.style===STORY_VOICE_STYLE,native_units:{total,official_narration_body_planning_units:total,opening,body_after_opening:total-opening,closing_card:closing,body_excluding_opening_and_closing:total-opening-closing,chapters:chapters.map(c=>({name:c.name,lines:c.lines.length,spoken_units:sum(c.lines)}))},line_spoken_units:Object.fromEntries(flat.map(l=>[l.id,spokenUnits(spokenText(l))])),native_estimate:{default_cpm:DEFAULT_CPM,minutes:t.total_frames/FPS/60,not_actual_audio:true},scene_estimates:t.scenes.map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS})),result,paid_calls:0,provider_calls:0,backend_actions:0,actual_duration_measured:false}));
"""
run=subprocess.run(['node','--input-type=module','-e',native_code,str(OUT),str(ROOT)],cwd=REPO,capture_output=True,text=True,check=True)
native=json.loads(run.stdout)
cadence=[w for w in native['result']['warnings'] if re.search(r'no open loop|open loops? planted|condensation plants',w.get('message',''))]
native['cadence_warning_count']=len(cadence)
shotids={s['id'] for s in scenes if s['template']=='shot'}
native['max_shot_estimated_seconds']=max(x['seconds'] for x in native['scene_estimates'] if x['id'] in shotids)
dump('native-initialized-lint.json',native)
assert not native['result']['errors'],native['result']['errors']
assert not cadence,cadence
assert native['max_shot_estimated_seconds']<=12
assert native['voice_exact_native_story_style'] and native['immutable_dictionary_unchanged'] and native['canonical_bytes_unchanged']
assert native['context_binding']['initialized_terms']>0


ends={};acc=0
for line in lines:acc+=native['line_spoken_units'][line['id']];ends[line['id']]=acc
hooks=[];prev=0
for hook in D['hooks']:
    end=ends[hook['id']];hooks.append({**hook,'end_native_spoken_units':end,'gap_units':end-prev,'planned_gap_seconds_at_4_5':round((end-prev)/4.5,2)});prev=end
assert max(x['planned_gap_seconds_at_4_5'] for x in hooks)<=45
for ch in D['chapters']:
    text=''.join(r['text'] for r in ch['rows']);assert '你' in text and '我' in text
current={r['id']:r['text'] for r in lines};changed=[k for k in priorlines if current[k]!=priorlines[k]];added=[k for k in current if k not in priorlines]
assert changed==[first] and added==[second]
assert len(lines)==85 and len(scenes)==83
subprocess.run(['node',str(OUT/'build-image-reuse-plan.mjs')],cwd=REPO,check=True,capture_output=True,text=True)
for f,h in PROTECTED.items():assert file_sha(f)==h,f
u=native['native_units'];files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','build-image-reuse-plan.mjs','image-reuse-plan.json','author-data-r9.json','native-initialized-lint.json']
notes={'schema_version':1,'revision':'C07 R9','author':'/root/c07_r7_author','status':'AUTHOR_HOLD_PENDING_DIFFERENT_SOURCE_VISUAL_QA_FRESH_NATIVE8_AND_ACTUAL_PRODUCTION','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'r8_core_bindings':{f:binding(BASE/f) for f in expected},'r8_source_and_native_reviewed':False,'r8_review_state_binding':binding(BASE/'review-state.json'),'r8_to_r9_delta':{'changed_narration_ids':changed,'added_narration_ids':added,'deleted_narration_ids':[],'all_other_83_narration_texts_unchanged':True,'added_scene_id':new_scene_id,'changed_existing_prompt_scene_ids':[oldscene['id'],first_payoff['id'],second_payoff['id']],'changed_existing_camera_scene_ids':[oldscene['id']],'all_other_existing_complete_scenes_unchanged':True,'two_teasers_in_payoff_order':True,'no_new_event_teaser_or_revealed_result':True,'loop_change':'Only the return-parcel teaser setup changes from 20104 to 20104b; all setup/payoff facts and other 17 loops stay unchanged.','prompts_mean_concept_reuse_not_same_physical_boot':True},'counts':{'narration_lines':len(lines),'scenes':len(scenes),'chapters':len(chapters),'illustration_shots':len(shotids),'cards':1,'loops':len(doc['loops'])},'native_units':u,'planning_length':{'whole_narration_spoken_units':u['total'],'actual_duration_seconds':None,'target_actual_body_seconds':[720,840],'known_duration_failure_claimed':False,'duration_pass_claimed':False,'no_padding_added':True},'substantive_existing_hook_plan':hooks,'native_initialized_context_lint':{'path':str(OUT/'native-initialized-lint.json'),'sha256':file_sha(OUT/'native-initialized-lint.json'),'errors':len(native['result']['errors']),'warnings':len(native['result']['warnings']),'cadence_warning_count':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'immutable_dictionary_unchanged':True,'canonical_unchanged':True,'not_independent_verdict':True},'image_reuse_plan':{'path':'image-reuse-plan.json','sha256':file_sha(OUT/'image-reuse-plan.json'),'pairs':2,'actual_same_asset_verified':False,'live_cache_sha_precheck_before_second_command_required':True},'protected_input_sha256':PROTECTED,'protected_inputs_all_unchanged':True,'author_validation_history':[{'issue':'Initial proposed new line id exceeded native eight-character limit; mechanical lint only, no external call','failed_receipt':'/workspace/work/brand-story-20261025/c07-audit/round-9-author/failed-author-lint-long-id.json','corrected_new_id':'c7h04b1','corrected_native_errors':0}],'source_pass_issued':False,'written_visual_pass_issued':False,'native_narrative_pass_issued':False,'verify_written':False,'owner_approval_issued':False,'paid_calls':0,'provider_calls':0,'backend_actions':0,'git_actions':0,'source_files_sha256':{f:file_sha(OUT/f) for f in files},'core_four_sha256':{f:file_sha(OUT/f) for f in expected}}
dump('author-notes.json',notes)
print(json.dumps({'revision':'C07 R9','counts':notes['counts'],'native_units':u,'native_errors':len(native['result']['errors']),'native_warning_count':len(native['result']['warnings']),'cadence_warnings':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'four_sha256':notes['core_four_sha256'],'image_reuse_plan_sha256':notes['image_reuse_plan']['sha256']},ensure_ascii=False))
