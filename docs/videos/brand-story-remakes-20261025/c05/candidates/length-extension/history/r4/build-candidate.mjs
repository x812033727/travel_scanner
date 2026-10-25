import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine,spokenText,validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {loadProject,lintProject} from '/workspace/work/brand-remakes-source/tools/video/core/state.mjs';
const OUT=path.dirname(fileURLToPath(import.meta.url)),BASE=path.resolve(OUT,'../..'),PRIOR=path.join(OUT,'history/r3');
const ROOT='/workspace/work/brand-story-20261025/submission-root',SLUG='story-everyday-kincho-c05-remake-20261025';
const BASE_SHA='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a',PRIOR_SHA='dbd1677d7c04ae4bc62634b910b37e06ea96c5dcef591a02fa3909b1eee0d05c';
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=f=>sha(fs.readFileSync(f)),read=f=>JSON.parse(fs.readFileSync(f,'utf8'));
const write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(p,e.name)):[path.join(p,e.name)]);
const CANON=path.join(ROOT,'docs/videos',SLUG);
const protectedPaths=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(e=>e.isFile()).map(e=>path.join(BASE,e.name)),...walk(path.join(BASE,'i18n')),...walk(CANON),...walk(path.join(OUT,'history')),...walk(path.join(OUT,'reviews'))];
const protectedBefore=Object.fromEntries(protectedPaths.map(f=>[f,fileSha(f)]));
assert.equal(fileSha(path.join(BASE,'video.json')),BASE_SHA);assert.equal(fileSha(path.join(CANON,'video.json')),BASE_SHA);assert.equal(fileSha(path.join(PRIOR,'video.json')),PRIOR_SHA);
const prior=read(path.join(PRIOR,'video.json')),priorRows=read(path.join(PRIOR,'narration-only.json')),priorNotes=read(path.join(PRIOR,'author-notes.json'));
const priorMap=new Map(priorRows.map(r=>[r.id,r])),priorClaims=new Map(read(path.join(PRIOR,'claims.json')).rows.map(r=>[r.id,r]));
const doc=structuredClone(prior);
const deleted={
 c05le022:'刪同種花含量的花期支線提問，從材料選擇直接回到成形。',
 c05le003:'刪盛開程度與含量的旁支；不影響種苗、收成、磨粉與製造主線。',
 c05r015:'刪遠古草木燻煙支線，避免從眼前粉料退回另一種驅蚊方法。',
 c05r016:'刪草木增煙與屋內煙霧支線，不用另一個問題撐長。',
 c05r062:'刪燃燒時數能否換算殺蚊本領的查核問答，較晚商品直接推向製造工序換代。',
 c05r063:'刪時數相除不等於殺蚊倍數的重述；稿中本來沒有作這項換算。',
 c05r064:'刪燃燒時間不等於效果強度的再次說明；來源界線留作者claims。'
};
const replacement={id:'c05rx009',text:'燃燒往前走時，有效成分怎麼離開香體，交到空氣裡？',reason:'刪「燒得慢只說明時間」回看句，直接推進原廠釋出機制的新問題；未加入新事實。'};
doc.scenes=doc.scenes.filter(s=>!(s.lines??[]).some(l=>Object.hasOwn(deleted,l.id)));
const changedScene=doc.scenes.find(s=>(s.lines??[]).some(l=>l.id===replacement.id));assert(changedScene);changedScene.lines.find(l=>l.id===replacement.id).text=replacement.text;
doc.loops=doc.loops.filter(l=>!Object.hasOwn(deleted,l.setup)&&!Object.hasOwn(deleted,l.payoff));
assert.deepEqual(validateVideo(doc),[]);for(const k of Object.keys(prior).filter(k=>!['scenes','loops'].includes(k)))assert.deepEqual(doc[k],prior[k]);
assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.deepEqual(doc.voice,prior.voice);assert.equal(doc.subtitles.burn_in,true);
const rows=[];let chapter='';for(const {scene,line} of eachLine(doc)){if(scene.chapter)chapter=scene.chapter;rows.push({chapter,id:line.id,text:line.text});}
const rowMap=new Map(rows.map(r=>[r.id,r])),flat=[...eachLine(doc)],sum=scenes=>scenes.flatMap(s=>s.lines??[]).reduce((n,l)=>n+spokenUnits(spokenText(l)),0);
const total=sum(doc.scenes),opening=sum(doc.scenes.slice(0,doc.scenes.findIndex((s,i)=>i>0&&s.chapter))),closing=sum(doc.scenes.filter(s=>s.template==='outro'));
const deletedRows=priorRows.filter(r=>!rowMap.has(r.id));assert.deepEqual(new Set(deletedRows.map(r=>r.id)),new Set(Object.keys(deleted)));
for(const r of rows)if(r.id!==replacement.id)assert.deepEqual(r,priorMap.get(r.id));
const oldSceneMap=new Map(prior.scenes.map(s=>[s.id,s])),changedScenes=doc.scenes.filter(s=>JSON.stringify(s)!==JSON.stringify(oldSceneMap.get(s.id))).map(s=>s.id);
assert.deepEqual(changedScenes,[changedScene.id]);assert.deepEqual(changedScene.data,oldSceneMap.get(changedScene.id).data);
const lineIndex=new Map(rows.map((r,i)=>[r.id,i]));for(const l of doc.loops)assert(lineIndex.get(l.setup)<lineIndex.get(l.payoff));
const payoffs=priorNotes.loop_audit.concrete_pairs_for_fresh_blind_review.filter(l=>lineIndex.has(l.setup)&&lineIndex.has(l.payoff)).map(l=>({...l,status:'AUTHOR_INTENT_PENDING_NEW_INDEPENDENT_READERS'}));assert(payoffs.length>=8);
const claims=rows.map(r=>{const old=priorClaims.get(r.id);assert(old);const modified=r.id===replacement.id;return {...structuredClone(old),chapter:r.chapter,claim:r.text,status:'PENDING_INDEPENDENT_REVIEW',change:modified?'SHORTENED_IN_R4':'UNCHANGED_FROM_R3',r3_claim_sha256:sha(old.claim),r4_change_reason:modified?replacement.reason:null,...(modified?{locator:'K_F：燃燒時有效成分進入空氣；本句引向既有原廠釋出說明，未加入新事實。',new_information:'直接問有效成分如何進入空氣，不再重述燃燒時間與效力的區分。'}:{})};});
const brief=[
 '# C05 長度候選 r4｜單一 A','',
 '狀態：未核准候選。r1–r3與所有原收據完整保留於history；本次只回應r3兩位讀者共同判否的重述及離題。','',
 '### 選項 A：把一條香做成能交付的工作','',
 '主角是一條香：花種與磨粉進入成形，長條盤入圓，工具交給雙手，再由機械接走手盤；同一件商品還得完整送達、分開使用，才輪到慢燃與成分釋出的工作。','',
 '## 問題','','為什麼把香盤成螺旋，還不夠讓它久燃、完整地走上貨架？','',
 '## 一句答案','','螺旋把長路徑收進平面；材料與製程把圓做出來，雙卷讓它較完整地送達，而香體密度與燃燒時的釋出，才接上它如何持續工作。','',
 '## 站主觀點','','我覺得這件日用品有意思的，是形狀留下來，做出形狀的動作卻改變。沿同一條香的交接講清楚每次新難題，把遠古驅蚊方法、花期含量與反覆提醒拿掉，不用資料清單撐長。','',
 '## 本次精修','','刪遠古草木煙燻與花期含量支線，刪燃燒時間不等於殺蚊效力的三句查核問答；有效成分釋出段直接問下一個機制，沒有回看「燒得慢只說明時間」。開場、製造事件、原廠歸屬、所有存續分鏡prompt及metadata逐字不動。','',
 '## 長度與待查','',`native總量${total} units；正文排除開場${total-opening}，再排除有聲片尾${total-opening-closing}。刪去弱支線後照實縮短，不補警語、停頓或慢播。實際TTS是否達12–14分鐘仍未量測，必須依真實聲音處理；本次不作篇幅或時長PASS。`,'',
 '維持原slug、voice、look、burn_in=true。原生估秒只是機械檢查；實際插圖、占時、音色、字幕、片頭片尾均未驗證。新稿仍待獨立來源差分與兩位新讀者，作者不寫verify/PASS，不重用舊核准。BASE、canonical、譯文、history、reviews不動；無provider、付費、後台或git。',''
].join('\n');
const series=read(path.join(PRIOR,'series.json'));Object.assign(series,{status:'length_extension_r4_candidate_unapproved',candidate_revision:'length-r4',parent_candidate_video_sha256:PRIOR_SHA,independent_source_review_required:true,two_isolated_narrative_readers_required:true});
write('video.json',doc);write('narration-only.json',rows);write('series.json',series);fs.writeFileSync(path.join(OUT,'brief.md'),brief);
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_REVIEW',candidate_revision:'length-r4',parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:PRIOR_SHA,rows:claims});
const script=['# '+doc.youtube.title,'','未核准長度候選r4；ID、章名與來源供審閱，不讀入旁白。r1–r3及其真實審查收據封存於history，新版差分待另查。',''];let last='';for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+last,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 長度候選 r4 逐句主張','','全部PENDING_INDEPENDENT_REVIEW；r3來源PASS未自動延伸為本版判定。','','| ID | r4狀態 | 旁白 | 來源索引 | 定位／變更 |','| --- | --- | --- | --- | --- |'];for(const r of claims)cm.push('| '+r.id+' | '+r.change+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+(r.r4_change_reason?'；'+r.r4_change_reason:'')+' |');
cm.push('','## r4刪除與改句','');for(const r of deletedRows)cm.push('- '+r.id+'：'+deleted[r.id]);
cm.push('- '+replacement.id+'：'+replacement.reason,'','## 來源界線保留於作者檔','','燃燒時間不直接表示殺蚊效力，稿中不作倍數換算。刪除旁白中的警語不會產生這項新主張，也不新增本集效力或安全實驗。','木片作芯僅是製法記錄，不是木芯現物留存。原件未說押出設備同時／每次出幾條，不補單條或雙條機構。NM_COIL不用西元括號錯配的日期、產能或首創主張。','乾花磨粉不是pollen；手卷加水成塊限於NM_MACHINE登錄。現代製程、溫度與釋出位置保留原廠歸屬及攝氏單位，不能倒寫早年相同配方或作法。','');
for(const s of [...new Map(claims.flatMap(c=>c.sources??[]).map(s=>[s.id,s])).values()])cm.push('- '+s.id+'：'+s.url+'；原件SHA '+s.raw_sha256+'；快取 '+s.raw_cache);cm.push('');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const project=loadProject({root:ROOT,slug:SLUG}),context={canonical_root:ROOT,canonical_video_sha256:fileSha(project.file),initialized_lexicon_sha256:sha(JSON.stringify(project.lexicon)),shelf_lexicon_sha256:sha(JSON.stringify(project.shelfLexicon)),in_memory_substitution_only:['doc','brief','series'],canonical_files_written:false,old_translation_staleness_warnings_preserved:true};
project.doc=doc;project.brief=brief;project.series=series;const lint=lintProject(project);assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));
const timeline=estimateTimeline(doc),estimates=timeline.scenes.filter(s=>doc.scenes.find(t=>t.id===s.id)?.template==='shot').map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS}));assert(estimates.every(s=>s.seconds<=12));
const priorTotal=sum(prior.scenes),removedUnits=deletedRows.reduce((n,r)=>n+spokenUnits(r.text),0),changedUnits=spokenUnits(replacement.text)-spokenUnits(priorMap.get(replacement.id).text);assert.equal(total,priorTotal-removedUnits+changedUnits);
const reviewInputs={source:path.join(PRIOR,'reviews/source-r3-independent.json'),native_panel:path.join(PRIOR,'reviews/narrative-r3.json')},files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs'];
const protectedAfter=Object.fromEntries(protectedPaths.map(f=>{assert.equal(fileSha(f),protectedBefore[f]);return[f,true];}));
const notes={status:'UNAPPROVED_LENGTH_EXTENSION_CANDIDATE',candidate_revision:'length-r4',author:'/root/c05_r4_author',parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:PRIOR_SHA,history_directory:PRIOR,
 review_inputs:Object.fromEntries(Object.entries(reviewInputs).map(([k,f])=>[k,{path:f,sha256:fileSha(f)}])),
 response_to_required_feedback:[{id:'no_recap',action:'刪時數/效力的三句警語，釋出問題直接向前，不先重述慢燃意義。',author_claim:'作者修訂意圖，待新讀者判定。'},{id:'no_detour',action:'移除花期含量與遠古草木燻煙支線；乾花材料選擇僅留與磨粉相接的一次說明。',author_claim:'作者修訂意圖，待新讀者判定。'}],single_reader_one_line_not_pursued:true,
 delta_from_r3:{added_lines:[],changed_lines:[{id:replacement.id,before:priorMap.get(replacement.id).text,after:replacement.text,reason:replacement.reason}],deleted_lines:deletedRows.map(r=>({id:r.id,text:r.text,spoken_units:spokenUnits(r.text),reason:deleted[r.id]})),deleted_spoken_units:removedUnits,changed_spoken_unit_delta:changedUnits,net_spoken_unit_delta:total-priorTotal,changed_scene_object_ids:changedScenes,unchanged_scene_objects_exact:doc.scenes.length-changedScenes.length,all_retained_prompt_data_exact:true,all_non_scene_and_loop_video_fields_exact:true,loops_removed:prior.loops.filter(l=>Object.hasOwn(deleted,l.setup)||Object.hasOwn(deleted,l.payoff)),metadata_changes:[],opening_lines_exact:true},
 author_self_check:{draft:'刪兩條支線與一段查核問答，縮短釋出機制的橋句。',critique:'花期及草木煙燻沒有繼續推進同一條香的製造；三句時數/效力警語又在末章被提起。',final:'材料進工具、工具交人手、人手換刀型、商品再進使用與燃燒；沒有新補事實或湊字。'},
 native_units:{counter:'spokenUnits(spokenText(line))',r3_total:priorTotal,candidate_total:total,candidate_opening:opening,candidate_body_excluding_opening:total-opening,candidate_outro:closing,candidate_body_excluding_opening_and_outro:total-opening-closing,target_actual_body_seconds:[720,840],actual_tts_seconds:null,actual_duration_verified:false,may_require_adjustment_after_actual_voice:true,planning_length_decision:'優先刪重述與支線，rough3500非硬湊字；真實聲音時長未驗收。'},
 planned_visuals:{scenes:doc.scenes.length,lines:rows.length,chapters:new Set(rows.map(r=>r.chapter)).size,illustration_scenes:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,planned_illustration_unit_share:flat.filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(spokenText(x.line)),0)/total,planning_basis:'spoken-unit share only, actual screen time unavailable',look_exact:true,voice_exact:true,burn_in:true,all_retained_prompt_data_exact:true,all_shots_static_stills:doc.scenes.filter(s=>s.template==='shot').every(s=>s.data.visual==='still'),actual_generated_media_reviewed:false},
 loop_audit:{total_declared_loops:doc.loops.length,concrete_pairs_for_fresh_blind_review:payoffs,opening_previews:2,actual_30_to_45_second_cadence_verified:false},
 native_initialized_context_lint:{scope:'read-only candidate mechanical lint, not independent verification',context,result:lint,maximum_estimated_shot_seconds:Math.max(...estimates.map(s=>s.seconds)),actual_audio_measured:false},
 independent_source_delta_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_ISOLATED_READERS',verify_file_written:false,owner_approval:false,
 file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))])),protected_parent_history_review_i18n_and_canonical_files_unchanged:protectedAfter,paid_calls:0,backend_writes:0,git_commands:0,canonical_written:false};
write('author-notes.json',notes);
console.log(JSON.stringify({revision:'length-r4',out:OUT,lines:rows.length,scenes:doc.scenes.length,native_units:notes.native_units,lint_errors:lint.errors.length,lint_warnings:lint.warnings.length,maximum_estimated_shot_seconds:Math.max(...estimates.map(s=>s.seconds)),file_sha256:notes.file_sha256},null,2));
