#!/usr/bin/env python3
"""C07 R10 minimal two-line deduplication from immutable R9; no source self-review."""
from pathlib import Path
import copy,datetime,hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
BASE=OUT/'history/r9'
ROOT=Path('/workspace/work/brand-story-20261025/c07-submission-root')
SLUG='story-everyday-dr-martens-c07-remake-20261025'
file_sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def binding(p):
    p=Path(p);return {'path':str(p),'bytes':p.stat().st_size,'sha256':file_sha(p)}
def readj(p):return json.loads(Path(p).read_text())
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


expected={'video.json':'474bde4e16ee3d575e70af2d21d5ac3f98ea43aee0b1c25749be2178f90ae4ab','script.md':'0a322b76db44c978aae51f72957bb6320b9375f7e35374f1d94a4d197d89e297','narration-only.json':'ff25e34df88cfb0005fd4437ef51931232a25597f26e4c8cec329d9a1d190646','claims.json':'419c47a40e00cf36dc3ccb99ee6216b2b8940d9060c9beb70b7ff60ec1cd2704'}
for f,h in expected.items():assert file_sha(BASE/f)==h,('Frozen R9 changed',f)
assert file_sha(BASE/'reviews/source-r9-independent.json')=='9ef1905a5ea2d6239171851113e233038ec113448b5ebbf77ce1f7cdeef3c74e'
assert file_sha(BASE/'verify-1.md')=='a7d04302b1a363a9bc447c9f55e05e417681c02185cebdbd31877dd160a6d3d9'
assert not (OUT/'verify-1.md').exists()
PROTECTED=readj(BASE/'author-notes.json')['protected_input_sha256']
PROTECTED.update({str(f):file_sha(f) for f in (OUT/'history').rglob('*') if f.is_file()})
PROTECTED.update({str(f):file_sha(f) for f in (OUT/'research-expansion').rglob('*') if f.is_file()})
PROTECTED[str(OUT/'author-data-r9.json')]=file_sha(OUT/'author-data-r9.json')
for f,h in PROTECTED.items():assert file_sha(f)==h,f
D=readj(OUT/'author-data-r10.json');prior=readj(BASE/'video.json');priorclaims=readj(BASE/'claims.json')
priorlines={l['id']:l['text'] for s in prior['scenes'] for l in s['lines']}
CHANGE={'c7r20310':'新外底要直接縫到鞋面上嗎？'};DELETED=['c7r20309']
doc=copy.deepcopy(prior);scenes=[]
for s in doc['scenes']:
    s['lines']=[l for l in s['lines'] if l['id'] not in DELETED]
    if not s['lines']:
        assert 'chapter' not in s
        continue
    for l in s['lines']:
        if l['id'] in CHANGE:l['text']=CHANGE[l['id']]
    scenes.append(s)
doc['scenes']=scenes
assert doc['loops']==D['loops']==prior['loops']
assert doc['scenes'][:7]==prior['scenes'][:7]
for s in scenes:
    before=next(q for q in prior['scenes'] if q['id']==s['id']);assert s['data']==before['data']
    if not any(l['id'] in CHANGE for l in s['lines']):assert s==before
assert {k:v for k,v in doc.items() if k!='scenes'}=={k:v for k,v in prior.items() if k!='scenes'}
ids=[l['id'] for s in scenes for l in s['lines']]
for lp in doc['loops']:assert ids.index(lp['setup'])<ids.index(lp['payoff'])
series=readj(BASE/'series.json');dump('video.json',doc);dump('series.json',series);(OUT/'brief.md').write_text(D['brief'])
claims=copy.deepcopy(priorclaims)
claims.update(episode='C07 Dr. Martens remake R10',status='AUTHOR_CANDIDATE_PENDING_NEW_INDEPENDENT_SOURCE_AND_VISUAL_QA',r9_binding={f:binding(BASE/f) for f in expected},r9_historical_source_review=binding(BASE/'reviews/source-r9-independent.json'),r9_historical_verify=binding(BASE/'verify-1.md'),r9_historical_native8=binding(BASE/'reviews/narrative-r8.json'),historical_pass_not_inherited=True,source_pass_issued=False,written_visual_pass_issued=False,owner_approval_issued=False,author_role_disclosure='R10 minimal author edit only; no independent source/visual/native self-review or owner approval. R9 source PASS and native8 HOLD bind the old bytes only.')
claims['narration_claims']=[r for r in claims['narration_claims'] if r['id'] not in DELETED]
for row in claims['narration_claims']:
    if row['id'] in CHANGE:row['text']=CHANGE[row['id']]
for key in ['source_inventory','source_anchors','original_inputs','public_review_scope','source_video_scope']:assert claims[key]==priorclaims[key]
dump('claims.json',claims)
chapters=[{'title':c['title'],'line_ids':[r['id'] for r in c['rows']]} for c in D['chapters']];lines=[{'id':r['id'],'text':r['text']} for c in D['chapters'] for r in c['rows']]
assert lines==[{'id':l['id'],'text':l['text']} for s in scenes for l in s['lines']]
dump('narration-only.json',{'slug':SLUG,'scope':'R10 author narration only, minimal two-line edit; no verdict','chapters':chapters,'lines':lines})
script=['# '+D['title'],'','R10作者附來源稿；待新來源查核與actualnative9。R9來源／配鏡PASS及native8 HOLD封存，不適用新稿；兩對同圖參數保持原值，只更新image-reuse-plan.json來源SHA，實圖尚未生成／驗證。不是owner核准或canonical劇本。','']
for ch in D['chapters']:
    script+=['## '+ch['title'],'']
    for row in claims['narration_claims']:
        if row['chapter']==ch['title']:script+=['['+row['id']+'] '+row['text'],'來源：'+(', '.join(row['source_ids']) or '觀眾問題／訂閱邀請'),'']
(OUT/'script.md').write_text('\n'.join(script)+'\n')
md=['# C07 R10｜逐句來源與書面概念配鏡索引','','作者映射，待不同來源reviewer及兩位新讀者；不繼承R9來源PASS與native8判定。','','## 原件來源','']
for source in claims['source_inventory']:md+=['- '+source['id']+'：['+source['title']+']('+source['url']+')；'+source['evidence_level']+'；raw SHA '+source['raw_binding']['sha256']+'。']
md+=['','## 逐句錨點','','| ID | 旁白 | 來源 | 定位 |','|---|---|---|---|']
for row in claims['narration_claims']:md+=['| '+row['id']+' | '+row['text'].replace('|','／')+' | '+', '.join(row['source_ids'])+' | '+(row['evidence'][0]['locator'] if row['evidence'] else '觀眾邀請')+' |']
md+=['','## 最小修訂與共圖保全','','只刪20309狀態橋句，20310直接問新外底是否縫鞋面；20313先接新沿條、後章熱刀接底的既有答案不改。所有存留prompt/camera/cast及兩對原生imageKey保持R9，image-reuse-plan.json只更新版本與本稿SHA。第二命令前必核live cache實檔SHA；miss即停、不買相似第二圖。最終manifest及含trim衍生檔同一實檔SHA待驗，actual_same_asset_verified=false。','','兩則not-verified評論、倫敦店與授權示範是不同人／鞋／事件；共用匿名概念圖不證明同一實物、不捏造拆箱順序。材料、範圍及現行工法歸因按原逐句來源，不由圖像辨識PVC或量溫。本作者不給來源或配鏡PASS。']
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
console.log(JSON.stringify({scope:'R10 author native lint in existing normally initialized canonical context; candidate substituted in memory only; not verify or independent approval',input_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','author-data-r10.json'].map(f=>[f,sha(path.join(dir,f))])),context_binding:context,immutable_dictionary_unchanged:immutableFiles.every(f=>dictionaryBefore[f]===sha(path.join(p.dir,f))),canonical_bytes_unchanged:sha(p.file)===context.canonical_sha256,voice_exact_native_story_style:d.voice.style===STORY_VOICE_STYLE,native_units:{total,official_narration_body_planning_units:total,opening,body_after_opening:total-opening,closing_card:closing,body_excluding_opening_and_closing:total-opening-closing,chapters:chapters.map(c=>({name:c.name,lines:c.lines.length,spoken_units:sum(c.lines)}))},line_spoken_units:Object.fromEntries(flat.map(l=>[l.id,spokenUnits(spokenText(l))])),native_estimate:{default_cpm:DEFAULT_CPM,minutes:t.total_frames/FPS/60,not_actual_audio:true},scene_estimates:t.scenes.map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS})),result,paid_calls:0,provider_calls:0,backend_actions:0,actual_duration_measured:false}));
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
current={r['id']:r['text'] for r in lines};changed=[k for k in current if current[k]!=priorlines[k]];deleted=[k for k in priorlines if k not in current]
assert changed==list(CHANGE) and deleted==DELETED
assert len(lines)==84 and len(scenes)==82
oldclaims={r['id']:r for r in priorclaims['narration_claims']}
for row in claims['narration_claims']:
    if row['id'] not in CHANGE:assert row==oldclaims[row['id']]
subprocess.run(['node',str(OUT/'build-image-reuse-plan.mjs')],cwd=REPO,check=True,capture_output=True,text=True)
oldplan=readj(BASE/'image-reuse-plan.json');newplan=readj(OUT/'image-reuse-plan.json')
assert newplan['pairs']==oldplan['pairs']
assert newplan['production_handoff']==oldplan['production_handoff']
for f,h in PROTECTED.items():assert file_sha(f)==h,f
u=native['native_units'];files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py','build-image-reuse-plan.mjs','image-reuse-plan.json','author-data-r10.json','native-initialized-lint.json']
notes={'schema_version':1,'revision':'C07 R10','author':'/root/c07_r7_author','status':'AUTHOR_HOLD_PENDING_NEW_SOURCE_VISUAL_QA_FRESH_NATIVE9_AND_ACTUAL_PRODUCTION','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'r9_core_bindings':{f:binding(BASE/f) for f in expected},'r9_source_receipt_binding':binding(BASE/'reviews/source-r9-independent.json'),'r9_verify_binding':binding(BASE/'verify-1.md'),'r9_native8_binding':binding(BASE/'reviews/narrative-r8.json'),'r9_to_r10_delta':{'changed_narration_ids':changed,'deleted_narration_ids':deleted,'added_narration_ids':[],'all_other_83_narration_texts_unchanged':True,'all_retained_prompts_cameras_cast_emotions_unchanged':True,'opening_seven_complete_scenes_unchanged':True,'all_18_loop_values_and_hook_content_unchanged':True,'two_image_reuse_pairs_and_full_native_request_keys_unchanged':True,'image_reuse_plan_only_new_revision_and_source_sha_binding':True,'different_physical_boot_and_public_comment_scope_preserved':True,'lone_one_line_not_pursued':True,'change_reason':'Delete retained-upper/pre-needle state recap at 20309; remove already-told old-sole premise from 20310 while preserving a direct mechanism question and the actual 20313/heat-weld answers.'},'counts':{'narration_lines':len(lines),'scenes':len(scenes),'chapters':len(chapters),'illustration_shots':len(shotids),'cards':1,'loops':len(doc['loops'])},'native_units':u,'planning_length':{'whole_narration_spoken_units':u['total'],'actual_duration_seconds':None,'target_actual_body_seconds':[720,840],'known_duration_failure_claimed':False,'duration_pass_claimed':False,'no_padding_added':True},'substantive_existing_hook_plan':hooks,'native_initialized_context_lint':{'path':str(OUT/'native-initialized-lint.json'),'sha256':file_sha(OUT/'native-initialized-lint.json'),'errors':len(native['result']['errors']),'warnings':len(native['result']['warnings']),'cadence_warning_count':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'immutable_dictionary_unchanged':True,'canonical_unchanged':True,'not_independent_verdict':True},'image_reuse_plan':{'path':'image-reuse-plan.json','sha256':file_sha(OUT/'image-reuse-plan.json'),'pairs':2,'actual_same_asset_verified':False,'live_cache_sha_precheck_before_second_command_required':True},'protected_input_sha256':PROTECTED,'protected_inputs_all_unchanged':True,'source_pass_issued':False,'written_visual_pass_issued':False,'native_narrative_pass_issued':False,'verify_written':False,'owner_approval_issued':False,'paid_calls':0,'provider_calls':0,'backend_actions':0,'git_actions':0,'source_files_sha256':{f:file_sha(OUT/f) for f in files},'core_four_sha256':{f:file_sha(OUT/f) for f in expected}}
dump('author-notes.json',notes)
print(json.dumps({'revision':'C07 R10','counts':notes['counts'],'native_units':u,'native_errors':len(native['result']['errors']),'native_warning_count':len(native['result']['warnings']),'cadence_warnings':len(cadence),'max_shot_estimated_seconds':native['max_shot_estimated_seconds'],'four_sha256':notes['core_four_sha256'],'image_reuse_plan_sha256':notes['image_reuse_plan']['sha256']},ensure_ascii=False))
