// C05 author R13: split the existing two-clause teaser and plan two genuinely shared stills.
// Local authoring only. This file never writes the parent, runtime, workdir, or an approval.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine,spokenText,validateVideo} from '../../../../../../tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS} from '../../../../../../tools/video/core/timeline.mjs';
import {loadProject,lintProject} from '../../../../../../tools/video/core/state.mjs';
import {videoLexicon} from '../../../../../../tools/video/core/lexicon-store.mjs';
import {screenplay,narrativeHash} from '../../../../../../tools/video/core/screenplay.mjs';
import {narrativeReviewMatches} from '../../../../../../tools/video/core/narrative.mjs';
import {resolveLook,shotCast,shotAppearancePrompt} from '../../../../../../tools/video/core/drama.mjs';
import {composeShotPrompt} from '../../../../../../tools/video/media/prompt-budget.mjs';
import {Stage} from '../../../../../../tools/video/media/stages.mjs';

const OUT=path.dirname(fileURLToPath(import.meta.url)),PARENT=path.resolve(OUT,'../..'),BASE=path.join(OUT,'history/r12');
const REPO=path.resolve(OUT,'../../../../../..'),AUDIT='/workspace/work/brand-story-20261025/c05-audit/teaser-image-plan';
const ROOT='/workspace/work/brand-story-20261025/submission-root',MEDIA='/workspace/work/brand-story-20261025/media';
const SLUG='story-everyday-kincho-c05-remake-20261025',AUTHOR='/root/c05_teaser_candidate';
const INITIAL=JSON.parse(fs.readFileSync(path.join(AUDIT,'protected-initial.json'),'utf8'));
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8')),write=(name,x)=>fs.writeFileSync(path.join(OUT,name),JSON.stringify(x,null,2)+'\n');
for(const [f,h]of Object.entries(INITIAL))assert.equal(fileSha(f),h,'Protected input changed: '+f);
const manifest=read(path.join(BASE,'baseline-manifest.json'));
for(const [f,h]of Object.entries(manifest.files_sha256))assert.equal(fileSha(path.join(BASE,f)),h,'R12 snapshot changed: '+f);
const old=read(path.join(BASE,'video.json')),oldRows=read(path.join(BASE,'narration-only.json')),oldClaims=read(path.join(BASE,'claims.json'));
assert.equal(fileSha(path.join(BASE,'video.json')),'1204dfb81743ed9dc7e041bc030ee7391ff92512951e0fa2cf470ccdc4f1ad87');
assert(!fs.existsSync(path.join(OUT,'verify-1.md')),'Never inherit a source PASS at the candidate root.');
assert.equal(oldRows.length,108);

const doc=structuredClone(old),newId='c05h04b1';
const first=doc.scenes.find(s=>s.id==='c07o04'),drying=doc.scenes.find(s=>s.id==='c07d08'),burning=doc.scenes.find(s=>s.id==='c07u04');
assert(first&&drying&&burning);
assert.equal(first.lines[0].text,'採下的花遇上連雨怎麼辦，點火後成分又從哪裡離開？');
first.lines[0].text='採下的花遇上連雨怎麼辦？';
const flowerPrompt='Wide shot in a simple room, an anonymous worker holding a shallow basket of picked flowers beside an empty raised bamboo mat, rain outside a small window, soft daylight.';
const coilPrompt='Macro view at a plain worktable, the glowing tip and adjacent intact portion of an unmarked incense coil resting on a simple holder, soft neutral light.';
first.data={...first.data,prompt:flowerPrompt,camera:drying.data.camera};
drying.data={...drying.data,prompt:flowerPrompt};
const second=structuredClone(first);second.id=newId;second.lines=[{...structuredClone(first.lines[0]),id:newId,text:'點火後成分又從哪裡離開？'}];
second.data={...second.data,prompt:coilPrompt,camera:burning.data.camera};
burning.data={...burning.data,prompt:coilPrompt};
doc.scenes.splice(doc.scenes.findIndex(s=>s.id==='c07o04')+1,0,second);
let changedLoops=0;
for(const loop of doc.loops)if(loop.setup==='c07o04'&&loop.payoff==='c05le013'){
  loop.setup=newId;loop.payoff='c07u04';changedLoops++;
}
assert.equal(changedLoops,1);
assert.deepEqual(validateVideo(doc),[]);
const rows=[];let chapter='';
for(const {scene,line}of eachLine(doc)){if(scene.chapter)chapter=scene.chapter;assert.equal(spokenText(line),line.text);rows.push({chapter,id:line.id,text:line.text});}
assert.equal(rows.length,109);
const lineById=new Map([...eachLine(doc)].map(x=>[x.line.id,x.line])),oldLineById=new Map([...eachLine(old)].map(x=>[x.line.id,x.line]));
for(const [id,line]of oldLineById)if(id!=='c07o04')assert.deepEqual(lineById.get(id),line,id);
assert.deepEqual(rows.filter(x=>x.id!=='c07o04'&&x.id!==newId),oldRows.filter(x=>x.id!=='c07o04'));
const oldSceneIds=old.scenes.map(s=>s.id),sceneIds=doc.scenes.filter(s=>s.id!==newId).map(s=>s.id);assert.deepEqual(sceneIds,oldSceneIds);
const changedSceneIds=new Set(['c07o04','c07d08','c07u04']);
for(const scene of old.scenes)if(!changedSceneIds.has(scene.id))assert.deepEqual(doc.scenes.find(x=>x.id===scene.id),scene,scene.id);
for(const k of Object.keys(old).filter(k=>!['scenes','loops'].includes(k)))assert.deepEqual(doc[k],old[k],k);
const index=new Map(rows.map((r,i)=>[r.id,i]));for(const loop of doc.loops)assert(index.get(loop.setup)<index.get(loop.payoff),JSON.stringify(loop));
assert(index.get('c05r076')<index.get('c05r069')&&index.get('c05r069')<index.get('c07a01'),'R12 chronology must stay fixed.');
const chapters=new Map();for(const r of rows)chapters.set(r.chapter,[...(chapters.get(r.chapter)??[]),r]);
assert.equal(chapters.size,6);for(const rr of chapters.values())assert(rr.some(r=>r.text.includes('你'))&&rr.some(r=>r.text.includes('我')));
const units=rr=>rr.reduce((n,r)=>n+spokenUnits(r.text),0),total=units(rows),opening=units([...chapters.values()][0]);
assert.equal(total,3041);assert.equal(total,units(oldRows));

const claims=structuredClone(oldClaims);Object.assign(claims,{candidate_revision:'teaser-r13',author:AUTHOR,status:'PENDING_INDEPENDENT_SOURCE_AND_FRESH_NATIVE_PANEL12',parent_candidate_video_sha256:manifest.source_video_sha256});
const oldClaimById=new Map(oldClaims.rows.map(r=>[r.id,r])),firstClaim=structuredClone(oldClaimById.get('c07o04'));
Object.assign(firstClaim,{claim:first.lines[0].text,claim_kind:'UNRESOLVED_EVENT_PREVIEW',change:'R13_SPLIT_FIRST_EXISTING_PREVIEW_ONLY',source_ids:['NDL1897'],sources:firstClaim.sources.filter(s=>s.id==='NDL1897'),locator:'1897第五版p27連雨備案的未揭結果問題，於c07d08回答；中性花籃與空竹簾情境共圖，不在開場畫供熱結果。'});
const secondClaim=structuredClone(oldClaimById.get('c07u04'));
for(const key of Object.keys(secondClaim))if(/^r\d+_claim_sha256$/.test(key))delete secondClaim[key];
secondClaim.source_evidence_reused_from_r12_line='c07u04';
Object.assign(secondClaim,{id:newId,chapter:oldClaimById.get('c07o04').chapter,claim:second.lines[0].text,status:'PENDING_INDEPENDENT_REVIEW',claim_kind:'UNRESOLVED_EVENT_PREVIEW',change:'R13_SPLIT_SECOND_EXISTING_PREVIEW_ONLY',locator:'K_F原廠說明燃端與前方揮散位置；本句只問位置，c07u04先回答，c05le013接續6–8mm及約250°C細節。'});
claims.rows=rows.map(r=>r.id==='c07o04'?firstClaim:r.id===newId?secondClaim:structuredClone(oldClaimById.get(r.id)));
for(const row of claims.rows){assert.equal(row.claim,lineById.get(row.id).text);if(!['c07o04',newId].includes(row.id))assert.deepEqual(row,oldClaimById.get(row.id),row.id);}
claims.baseline_adopted_r12={source_video_sha256:manifest.source_video_sha256,source_receipt:'history/r12/reviews/source-length-r12-independent.json',source_receipt_sha256:fileSha(path.join(BASE,'reviews/source-length-r12-independent.json')),narrative_receipt:'history/r12/reviews/narrative-final.json',narrative_receipt_sha256:fileSha(path.join(BASE,'reviews/narrative-final.json')),applies_to_candidate:false};
claims.teaser_image_plan={file:'image-reuse-plan.json',actual_same_asset_verified:false,source_gate_required:true,pairs:[{setup:'c07o04',payoff:'c07d08'},{setup:newId,payoff:'c07u04'}],scope:'Written visual planning only; matching prompts/keys are not generated-image acceptance.'};
const series={...read(path.join(BASE,'series.json')),status:'hold_r13_teaser_image_plan_pending_source_and_fresh_native12',candidate_revision:'teaser-r13',parent_candidate_video_sha256:manifest.source_video_sha256};
let brief=fs.readFileSync(path.join(BASE,'brief.md'),'utf8').replace('# C05 R12','# C05 R13共圖候選');
brief=brief.replace(/狀態：[^\n]*/,'狀態：CANDIDATE／HOLD／未採用。R12 current與864句八語保持不變；本版待獨立來源及書面配鏡差分、兩位fresh readers（下一次實際native panel12）、新精確劇本送審。不得沿用R12待審或BASE批准。');
brief=brief.replace(/## R12精確修改[\s\S]*?(?=## 長度與執行規格)/,'## R13精確修改\n\n只把c07o04原有兩個未揭結果預告拆成c07o04與c05h04b1兩句／兩景。其他107句、原scene順序、所有史實與年代保留。兩個預告依正文順序分別與c07d08雨天處理、c07u04成分揮散首個答案共圖；前者用花籃與空竹簾的中性情境，不先畫供熱；後者只見燃端與鄰接未燃香體，不先畫揮散箭頭、熱區數字或成分流向。\n\n圖像計畫是獨立sidecar，不擴充video schema、不造manifest。必須先依正常帳戶與當前批准生成合格payoff、核live cache真檔SHA，再讓teaser從同一exact-request cache取用；cache缺失不可放任CLI派送另一張。兩端仍各經原生judge，裁切／重試造成差異須停止pair，最後檢驗manifest與真檔SHA；目前actual_same_asset_verified=false。\n\nR12已修的1940→約1955材料進展→1957改良機→約1957手卷設備使用期→1958研究順序原樣。未定年抽出與結構研究不補新日期；1958不倒寫成1955的原因。六到八毫米、約250°C與燃端700–800°C不混成同一位置。\n\n');
brief=brief.replace('與R11相同','與R12相同');
brief=brief.replace('需另一位來源QA及兩位fresh readers，不寫verify或作者SOURCE／敘事PASS。','需另一位來源QA及兩位fresh readers，不寫verify或作者SOURCE／敘事PASS。拆句後必須重新送精確canonical劇本；R12現行864句八語不自動成為候選109句的翻譯批准。');
write('video.json',doc);write('narration-only.json',rows);write('claims.json',claims);write('series.json',series);fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const script=['# '+doc.youtube.title,'','C05作者R13共圖候選；未採用、待獨立來源／書面差分及兩位fresh readers，下一次實際native panel12。ID不讀入旁白。',''];let last='';
for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+r.chapter,'');}script.push('### '+r.id,'',r.text,'');}
fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
let markdown=fs.readFileSync(path.join(BASE,'claims.md'),'utf8').replace('# C05 R12逐句主張與來源錨點','# C05 R13共圖候選逐句主張與來源錨點').replace('全部PENDING_INDEPENDENT_REVIEW；R11收據不自動成為R12判定，無作者SOURCE／敘事PASS。','候選未採用；全部待新的獨立差分。R12來源／敘事只對基底有效，無作者SOURCE／敘事PASS。');
const table=r=>'| '+r.id+' | '+r.claim_kind+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+' |';
const originalTable=markdown.split('\n').find(x=>x.startsWith('| c07o04 |'));assert(originalTable);
markdown=markdown.replace(originalTable,table(firstClaim)+'\n'+table(secondClaim));
markdown+='\n## R13拆句第二預告原件錨點\n\n'+secondClaim.source_anchors.map(a=>'- '+JSON.stringify(a)).join('\n')+'\n\n## R13共圖候選差分\n\nc07o04／c05h04b1只拆原兩個問題；其他107句不變。兩對setup/payoff的prompt、camera與完整native image key對照見image-reuse-plan.json。舊R12章節與來源段落保留為歷史基底資訊，不等於本候選已獨立通過；實圖、實聲及當前owner批准均不存在。\n';
fs.writeFileSync(path.join(OUT,'claims.md'),markdown);

const project=loadProject({root:ROOT,slug:SLUG});assert.equal(fileSha(project.file),manifest.source_video_sha256);
const lexicon=videoLexicon({root:ROOT,slug:SLUG,dir:project.dir,workdir:path.join(MEDIA,SLUG),requireSnapshot:true});assert.equal(lexicon.mode,'snapshot');
const lint=lintProject({...project,doc:structuredClone(doc),brief,series:structuredClone(series)});
assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));
const cadence=lint.warnings.filter(w=>/no open loop|open loops? planted|condensation plants/.test(w.message));assert.equal(cadence.length,0,JSON.stringify(cadence));
const timeline=estimateTimeline(doc),maxShot=Math.max(...timeline.scenes.filter(s=>doc.scenes.find(t=>t.id===s.id)?.template==='shot').map(s=>(s.end_frame-s.start_frame)/FPS));
assert(maxShot<=12);
const look=resolveLook(doc.look),stage=new Stage({slug:SLUG,workdir:path.join(MEDIA,SLUG),options:{},status:{image:{provider:'minimax',model:'image-01'}},stage:'author-plan-key-proof-only',format:doc.format,imageVersion:0});
const compose=s=>composeShotPrompt({prompt:s.data.prompt,look,camera:s.data.camera,cast:shotAppearancePrompt(shotCast(doc,s)),fixes:[],limit:1500});
const pairs=[{id:'rain-flower-context',setup:'c07o04',payoff:'c07d08'},{id:'burning-coil-context',setup:newId,payoff:'c07u04'}].map(x=>{
  const setup=doc.scenes.find(s=>s.id===x.setup),payoff=doc.scenes.find(s=>s.id===x.payoff),a=compose(setup),b=compose(payoff);assert.deepEqual(a,b);assert.equal(a.cutChars,0);assert.equal(a.droppedFixes,0);
  assert.equal(setup.data.prompt,payoff.data.prompt);assert.equal(setup.data.camera,payoff.data.camera);
  const bySize={};for(const size of ['1K','2K']){const args={prompt:a.prompt,negative:look.negative??'',references:[],seed:1,size};const firstKey=stage.imageKey(args),secondKey=stage.imageKey({...args,prompt:b.prompt});assert.equal(firstKey,secondKey);bySize[size]={source_key:firstKey,reuse_key:secondKey,equal:true};}
  return {asset_plan_id:x.id,source_scene_id:x.payoff,source_line_id:payoff.lines[0].id,reuse_scene_id:x.setup,reuse_line_id:setup.lines[0].id,source_prompt:payoff.data.prompt,reuse_prompt:setup.data.prompt,prompt_sha256:sha(payoff.data.prompt),camera:payoff.data.camera,composed_prompt:a.prompt,composed_prompt_sha256:sha(a.prompt),pure_local_native_key_rehearsal:{provider:'minimax',model:'image-01',seed:1,seed_offset:0,fixes:[],references:[],image_selection_version:0,by_size:bySize,example_parameters_not_backend_status:true,no_provider_call:true},actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,actual_same_asset_verified:false};
});
const codeFiles=['tools/video/media/keyframes.mjs','tools/video/media/stages.mjs','tools/video/media/cache.mjs','tools/video/media/trim.mjs','tools/video/media/prompt-budget.mjs','tools/video/core/drama.mjs'];
const plan={schema_version:1,revision:'c05-teaser-r13',status:'WRITTEN_REUSE_PLAN_PENDING_INDEPENDENT_REVIEW_AND_REAL_ASSET_VERIFICATION',candidate_not_adopted:true,not_a_video_schema_extension:true,not_a_keyframes_manifest:true,rule:{file:'.agents/skills/youtube-video/references/script-writing.md',quote:'每一個預告句用回收它的那一章的畫面（同一張圖）',sha256:fileSha(path.join(REPO,'.agents/skills/youtube-video/references/script-writing.md'))},source_files_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json'].map(f=>[f,fileSha(path.join(OUT,f))])),code_files_sha256:Object.fromEntries(codeFiles.map(f=>[f,fileSha(path.join(REPO,f))])),pairs,production_handoff:{preconditions:['Candidate must first pass new exact source/written-visual and fresh native12 reviews, controlled adoption, exact owner narrative/outline approval and legitimate production admission. The current R12 project must never be overwritten or used as if this candidate were approved.','Use the same workdir, model/selection version, look, cast/reference hashes, composed prompt, negative, size, seed=1/offset=0 and empty corrections at both ends.','Generate and pass each payoff once, then read the live native cache index and independently hash its selected real file before invoking the teaser command. A missing, stale or different cached file stops the pair: do not let a cache miss dispatch another image.'],official_recipe_only:pairs.flatMap(p=>[{purpose:'admitted payoff first, exact take 1 only',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',ROOT,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.source_scene_id,'--takes','1']},{purpose:'only after the live-cache/file-SHA precondition has been positively checked; must reuse that actual file',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',ROOT,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.reuse_scene_id,'--takes','1']}]),on_failure:'Stop the pair. Each endpoint still receives its own native scene judge. No force, accept-best, independent retake/correction, look-alike purchase, invented still alias or edited manifest can establish reuse. Correct both ends together, repeat exact source/visual binding and stay inside the ordinary account/take caps.',actual_verification_required:['Read both real keyframes manifest entries, require both native judges to pass and require the same selected actual file path and SHA256; independently hash the bytes.','After trim/crop, compare the final referenced derived files and their actual SHA256, not just the original generated-file hash. If they differ, stop and resolve through the ordinary workflow.','Retain real cache/job/ledger and scene-judge receipts. The CLI does not enforce this pair and may dispatch on a cache miss; the caller must perform the stated pre-command stop check.'],actual_same_asset_verified:false,executed:false},paid_requests:0,media_files_generated:0,backend_writes:0,approvals_created:0};
write('image-reuse-plan.json',plan);write('native-author-lint-r13.json',{scope:'Author mechanical check in memory against the genuine current immutable C05 dictionary; no runtime or media writes.',canonical_source_video_sha256:fileSha(project.file),candidate_video_sha256:fileSha(path.join(OUT,'video.json')),lexicon_mode:lexicon.mode,initialized_speech_lexicon_sha256:sha(JSON.stringify(project.lexicon)),initialized_shelf_lexicon_sha256:sha(JSON.stringify(project.shelfLexicon)),result:lint,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,translations:'Existing parent R12 translations stay untouched; stale/missing candidate lines remain visible as warnings and do not become candidate translation approval.'});
const delta={revision:'teaser-r13',baseline:'adopted-r12',baseline_source_video_sha256:manifest.source_video_sha256,candidate_source_video_sha256:fileSha(path.join(OUT,'video.json')),narration_changed:['c07o04'],narration_added:[newId],narration_deleted:[],remaining_107_complete_line_objects_identical:true,remaining_107_narration_rows_same_order:true,old_scene_order_preserved:true,existing_complete_scenes_unchanged:old.scenes.length-3,prompt_changed:['c07o04','c07d08','c07u04'],camera_changed:['c07o04'],new_scenes:[newId],loop_change:{old:{setup:'c07o04',payoff:'c05le013'},current:{setup:newId,payoff:'c07u04'},reason:'The first true location answer is c07u04; c05le013 supplies the following 6–8mm/~250°C detail.'},all_other_video_fields_identical:true,all_other_claim_rows_identical:107,source_anchors_for_existing_payoff_rows_unchanged:true,r12_chronology_preserved:true,no_new_source_fact:true,canonical_script_sha256:{baseline:sha(screenplay(old)),candidate:sha(screenplay(doc)),same:false},narrative_hash:{baseline:narrativeHash(old),candidate:narrativeHash(doc)},old_native_review_applies:false,next_actual_native_panel_round:12,adopted:false,actual_duration_measured:false};
assert.notEqual(delta.canonical_script_sha256.baseline,delta.canonical_script_sha256.candidate);
assert.equal(narrativeReviewMatches(read(path.join(BASE,'reviews/narrative-final.json')),doc),false);
write('revision-edits.json',delta);
const protectedAfter={};for(const [f,h]of Object.entries(INITIAL)){protectedAfter[f]=fileSha(f);assert.equal(protectedAfter[f],h,'Protected file was modified: '+f);}
fs.writeFileSync(path.join(AUDIT,'protected-after.json'),JSON.stringify(protectedAfter,null,2)+'\n');
const freezeFiles=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','image-reuse-plan.json','build-candidate.mjs','revision-edits.json','native-author-lint-r13.json'];
const notes={schema_version:1,status:'CANDIDATE_NOT_ADOPTED_PENDING_NEW_SOURCE_WRITTEN_VISUAL_AND_FRESH_NATIVE12',candidate_revision:'teaser-r13',author:AUTHOR,baseline_adopted_r12:manifest.source_video_sha256,source_pass_claimed:false,narrative_pass_claimed:false,verify_written:false,owner_approval_claimed:false,old_r12_pending_review_or_base_approval_reused:false,next_actual_native_panel_round:12,counts:{lines:rows.length,scenes:doc.scenes.length,chapters:chapters.size,illustrations:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,loops:doc.loops.length},whole_narration_spoken_units:total,cold_open_spoken_units:opening,actual_tts_seconds:null,duration_pass:false,planning_target_minutes:13,padding_added:false,native_initialized_context_lint:{errors:lint.errors.length,warnings:lint.warnings.length,i18n_warnings:lint.warnings.filter(w=>/i18n\//.test(w.path)).length,cadence_warnings:cadence.length,maximum_estimated_shot_seconds:maxShot},protected_files:{count:Object.keys(INITIAL).length,all_exact:true,before_manifest:AUDIT+'/protected-initial.json',before_manifest_sha256:fileSha(path.join(AUDIT,'protected-initial.json')),after_manifest:AUDIT+'/protected-after.json',after_manifest_sha256:fileSha(path.join(AUDIT,'protected-after.json'))},parent_current_i18n_entries:864,parent_i18n_untouched:true,candidate_i18n_approved:false,candidate_lines_requiring_new_translation_binding:['c07o04',newId],media_generated:0,paid_requests:0,backend_writes:0,approvals_created:0,files_sha256:Object.fromEntries(freezeFiles.map(f=>[f,fileSha(path.join(OUT,f))])),delta};
write('author-notes.json',notes);
const freeze={schema_version:1,revision:'teaser-r13',status:notes.status,frozen_at_utc:new Date().toISOString(),next_actual_native_panel_round:12,core_four_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(f=>[f,fileSha(path.join(OUT,f))])),plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json')),author_notes_sha256:fileSha(path.join(OUT,'author-notes.json')),protected_files_unchanged:true,paid_requests:0,backend_writes:0,adopted:false};
write('author-freeze-r13.json',freeze);
console.log(JSON.stringify({status:notes.status,counts:notes.counts,whole_narration_spoken_units:total,lint_errors:lint.errors.length,lint_warnings:lint.warnings.length,i18n_warnings:notes.native_initialized_context_lint.i18n_warnings,cadence_warnings:cadence.length,maximum_estimated_shot_seconds:maxShot,core_four_sha256:freeze.core_four_sha256,plan_sha256:freeze.plan_sha256,protected_files:Object.keys(INITIAL).length},null,2));
