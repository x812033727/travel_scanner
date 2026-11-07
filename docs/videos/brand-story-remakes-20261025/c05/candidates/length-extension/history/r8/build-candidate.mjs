import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine, spokenText, validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {spokenUnits, estimateTimeline, FPS} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {loadProject, lintProject} from '/workspace/work/brand-remakes-source/tools/video/core/state.mjs';

// R8 applies only the shared one_line correction and the required V07_01 prompt scope.
const OUT=path.dirname(fileURLToPath(import.meta.url));
const BASE=path.resolve(OUT,'../..'), PRIOR=path.join(OUT,'history/r7'), RESEARCH=path.join(BASE,'research-expansion');
const ROOT='/workspace/work/brand-story-20261025/submission-root', SLUG='story-everyday-kincho-c05-remake-20261025';
const BASE_SHA='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a';
const R7_SHA='9597897739202d8df37b82158ae6abbbefe30553db1f104848eed45a135be80f';
const R7_CORE={
 'video.json':R7_SHA,
 'brief.md':'df76e71fff006af93a32094ec06fc0ba198f935eb2b24ee983f0bfb86c608b4e',
 'series.json':'32d759ddc47baf84a0f5424e15f890c5045e1adc13459a3bccb859c61b78402b',
 'claims.json':'ee8e34d2ffc1c47ccce3941b2b71e98d743ea4eeb97d8c14ed5746b06d68ac23'
};
const sha=x=>createHash('sha256').update(x).digest('hex'), fileSha=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8')), write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(p,e.name)):[path.join(p,e.name)]);
const protectedFiles=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(e=>e.isFile()).map(e=>path.join(BASE,e.name)),...walk(path.join(BASE,'i18n')),...walk(path.join(ROOT,'docs/videos',SLUG)),...walk(path.join(OUT,'history')),...walk(path.join(OUT,'reviews')),...walk(RESEARCH)];
const protectedBefore=Object.fromEntries(protectedFiles.map(f=>[f,fileSha(f)]));
for(const [f,digest]of Object.entries(R7_CORE))assert.equal(fileSha(path.join(PRIOR,f)),digest,f);
assert.equal(fileSha(path.join(BASE,'video.json')),BASE_SHA);
assert.equal(fileSha(path.join(RESEARCH,'research.md')),'0241eb279172af302351ffa72f43264313a521d30fe2ffa86429bad22f371ff0');
assert.equal(fileSha(path.join(RESEARCH,'claims.json')),'2219f8d5e97ac0647d2947319567695dea5bb90387edd6f5ae86e7dd1f656bc4');
const sourceReviewFile=path.join(OUT,'reviews/source-r7-independent.json');
const sourceReview=read(sourceReviewFile);
assert.equal(sourceReview.source_video_sha256,R7_SHA);
assert.equal(sourceReview.source_verdict,'PASS');
const visualFinding=sourceReview.findings.find(f=>f.id==='V07_01');
assert(visualFinding?.required);assert.equal(visualFinding.line_id,'c07u03');assert.equal(visualFinding.requires_narration_change,false);
const prior=read(path.join(PRIOR,'video.json')), priorRows=read(path.join(PRIOR,'narration-only.json'));
const priorClaims=read(path.join(PRIOR,'claims.json')), priorSeries=read(path.join(PRIOR,'series.json'));
const priorNotes=read(path.join(PRIOR,'author-notes.json'));
const oldRows=new Map(priorRows.map(r=>[r.id,r])),oldScenes=new Map(prior.scenes.map(s=>[s.id,s]));
const doc=structuredClone(prior);
const removedId='c07s01',changedId='c05r019';
const newText='公司年表記，一八八八年的蚊香試作，用的是舶來除蚤粉和竹筒。';
const removedScene=doc.scenes.find(s=>s.id===removedId);
assert(removedScene?.chapter);assert.equal(removedScene.lines.length,1);
doc.scenes=doc.scenes.filter(s=>s.id!==removedId);
const materialScene=doc.scenes.find(s=>s.id===changedId);
materialScene.chapter=removedScene.chapter;
assert.equal(materialScene.lines.length,1);materialScene.lines[0].text=newText;
const visualScene=doc.scenes.find(s=>s.id==='c07u03');
assert.equal(visualScene.data.prompt,visualFinding.current);
visualScene.data.prompt=visualFinding.proposed_prompt_only;
assert.equal(visualScene.data.prompt,'Close-up conceptual view of the glowing section of a plain coil directly touching the upper metal cover of an unmarked canned-incense holder, a dimming ember, neutral side light.');
// Exact invariants: every other retained scene and every non-scene field remain R7.
for(const key of Object.keys(prior).filter(k=>k!=='scenes'))assert.deepEqual(doc[key],prior[key],key);
for(const s of doc.scenes)if(![changedId,'c07u03'].includes(s.id))assert.deepEqual(s,oldScenes.get(s.id),s.id);
const materialBefore=structuredClone(oldScenes.get(changedId));materialBefore.chapter=removedScene.chapter;materialBefore.lines[0].text=newText;assert.deepEqual(materialScene,materialBefore);
const visualBefore=structuredClone(oldScenes.get('c07u03'));visualBefore.data.prompt=visualFinding.proposed_prompt_only;assert.deepEqual(visualScene,visualBefore);
assert.deepEqual(validateVideo(doc),[]);assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.deepEqual(doc.voice,prior.voice);assert.equal(doc.subtitles.burn_in,true);
const rows=[];let chapter='';for(const {scene,line}of eachLine(doc)){if(scene.chapter)chapter=scene.chapter;rows.push({chapter,id:line.id,text:line.text});}
const index=new Map(rows.map((r,i)=>[r.id,i]));assert(!index.has(removedId));
for(const r of rows)if(r.id!==changedId)assert.deepEqual(r,oldRows.get(r.id),r.id);
for(const l of doc.loops){assert(index.has(l.setup)&&index.has(l.payoff));assert(index.get(l.setup)<index.get(l.payoff));}
const chapterRows=new Map();for(const r of rows)chapterRows.set(r.chapter,[...(chapterRows.get(r.chapter)??[]),r]);
assert.equal(chapterRows.size,6);for(const rr of chapterRows.values())assert(rr.some(r=>r.text.includes('你'))&&rr.some(r=>r.text.includes('我')));
const units=rr=>rr.reduce((n,r)=>n+spokenUnits(r.text),0),total=units(rows),opening=units([...chapterRows.values()][0]);
const closing=rows.filter(r=>['c05r101','c05r102','c05r103'].includes(r.id)),outro=units(closing),body=total-opening-outro;
const deletedRows=priorRows.filter(r=>!index.has(r.id)),changedRows=rows.filter(r=>r.text!==oldRows.get(r.id)?.text);
const deletedUnits=units(deletedRows),changedDelta=changedRows.reduce((n,r)=>n+spokenUnits(r.text)-spokenUnits(oldRows.get(r.id).text),0);
assert.equal(total,units(priorRows)-deletedUnits+changedDelta);assert.deepEqual(deletedRows.map(r=>r.id),[removedId]);assert.deepEqual(changedRows.map(r=>r.id),[changedId]);

const currentClaims=structuredClone(priorClaims);
currentClaims.candidate_revision='length-r8';currentClaims.status='PENDING_INDEPENDENT_REVIEW_HOLD';currentClaims.parent_candidate_video_sha256=R7_SHA;
currentClaims.author='/root/c05_material_author';
currentClaims.prior_independent_review={path:sourceReviewFile,sha256:fileSha(sourceReviewFile),source_video_sha256:R7_SHA,reported_r7_source_verdict:sourceReview.source_verdict,reported_r7_written_visual_verdict:sourceReview.written_visual_verdict,scope:'R7 receipt only; R8 source/visual delta remains pending another reviewer.'};
currentClaims.rows=currentClaims.rows.filter(r=>r.id!==removedId);
for(const r of currentClaims.rows){r.r7_claim_sha256=sha(oldRows.get(r.id).text);r.change=r.id===changedId?'REWRITTEN_IN_R8':'R7_TEXT_RETAINED';r.status='PENDING_INDEPENDENT_REVIEW';}
const materialClaim=currentClaims.rows.find(r=>r.id===changedId);materialClaim.claim=newText;materialClaim.claim_kind='SOURCED_MATERIAL_AND_TOOL_TRIAL';
materialClaim.locator='K_M原文1888年條目至舶來除蚤粉/竹筒試作行；旁白只保留粉料、工具、試作年份，不敘述人物相遇/東京同宿。';
const materialSource=materialClaim.sources.find(s=>s.id==='K_M');assert(materialSource?.text_cache);
assert.equal(fileSha(materialSource.raw_cache),materialSource.raw_sha256);
const materialSourceText=fs.readFileSync(materialSource.text_cache,'utf8'),sourceLines=materialSourceText.split(/\r?\n/);
const sourceAt=sourceLines.findIndex(l=>l.includes('1888年'));assert(sourceAt>=0);
const sourceEnd=sourceLines.findIndex((l,i)=>i>=sourceAt&&l.includes('舶来のみとり粉と竹筒で蚊取り線香を試作'));assert(sourceEnd>=sourceAt);
const excerpt=sourceLines.slice(sourceAt,sourceEnd+1).join('\n');
materialClaim.source_anchors=[{source_id:'K_M',text_cache:materialSource.text_cache,text_cache_sha256:sha(materialSourceText),line_start:sourceAt+1,line_end:sourceEnd+1,exact_excerpt:excerpt,excerpt_sha256:sha(excerpt),scope:'Year context plus powder/tube trial. The intervening encounter is source context only and is absent from narration.'}];
const visualClaim=currentClaims.rows.find(r=>r.id==='c07u03');assert.equal(visualClaim.claim,oldRows.get('c07u03').text);
visualClaim.written_visual_change={finding:'V07_01',before:visualFinding.current,after:visualFinding.proposed_prompt_only,narration_unchanged:true,source_quote:visualFinding.source_quote,source_original_raw_sha256:visualFinding.source_original_raw_sha256,status:'PENDING_INDEPENDENT_VISUAL_DELTA_REVIEW'};
assert.equal(currentClaims.rows.length,rows.length);
for(const r of currentClaims.rows){assert.equal(r.claim,rows.find(x=>x.id===r.id).text);for(const a of r.source_anchors??[])if(a.exact_excerpt){const full=fs.readFileSync(a.text_cache,'utf8');assert.equal(sha(full),a.text_cache_sha256);assert.equal(sha(a.exact_excerpt),a.excerpt_sha256);assert.equal(full.split(/\r?\n/).slice(a.line_start-1,a.line_end).join('\n'),a.exact_excerpt);}}
const series={...priorSeries,status:'hold_r8_material_journey_pending_independent_delta_and_fresh_readers',candidate_revision:'length-r8',parent_candidate_video_sha256:R7_SHA,independent_source_review_required:true,two_isolated_narrative_readers_required:true,target_minutes:13};
const brief=['# C05 R8｜一卷香的百年材料旅程','','狀態：HOLD。作者revision R8，下一次實際native讀者panel為round7。R7的來源及panel收據只對R7雜湊有效，本版待獨立差分查核與新讀者；實聲和媒體未核准。','','### 選項 A：把材料交到長夜裡','','乾花粉末／有效成分→成形→交付→使用，一條材料旅程。主角是材料的工作，不是跨百年同一包粉。1897手冊、歷史工具、2017研究回顧與未標日期的原廠製程各有歸屬。乾花粉末不是花粉pollen；粉劑本來可以出售或撒用，本集追的是它如何成為可燃燒、可交付的一卷香。','','## 問題','','一把會散的乾花粉末，憑什麼變成能陪你過夜的商品？','','## 一句答案','','讓材料在該留的時候留住，到了使用時，再有節奏地離開。','','## 站主觀點','','用動作帶出材料取捨：採後乾燥能力、細切快乾的書中代價、篩粉和存粉、手盤與打型，再讓使用者拆卷和安放完成交接。天然成分身分只作為從乾花走向已知成分的一關，不列化學名或商品型錄；1958研究不倒寫成1955導入的原因。','','## R8精確修改','','移除c07s01人物相遇、東京與同宿的旁白；第三章直接從1888試作的舶來除蚤粉和竹筒進入下一句的可燃香體形狀。沒有重寫配方或替歷史人物補心理。c07u03旁白不改，提示詞依V07_01窄成罐裝香器的上方金屬蓋與火種直接接觸。其餘旁白、提示詞、章名、承諾、loops、標題和技術設定維持R7。','','## 長度與執行規格','','native總量'+total+' units；開場'+opening+'；排開場正文'+(total-opening)+'；有聲片尾'+outro+'；再扣有聲片尾的有效正文'+body+'。相較R7有效正文3111，淨變化'+(body-3111)+'。4–5units/s算術範圍'+(body/5).toFixed(1)+'–'+(body/4).toFixed(1)+'秒；4.5units/s約'+(body/4.5).toFixed(1)+'秒。不是實聲量測；實聲正文720–840秒仍HOLD，不慢播、停頓或灌字補足。','','原slug、Sulafat台灣自然語速與技術設定保留。look只有{preset:cute-mystery}、image-01、英文匿名概念插圖，無人名品牌logo或可讀字，不複用史料圖。至少70%插圖、連卡最多3、stillmotion、native每景≤12秒；繁中燒錄及CC。5秒片頭、21秒正式v4片尾僅待執行規格，未造媒體。縮圖layout d，金鳥品牌、黃字黑框主標、白短副標。','','## 未解除的關卡','','需另一位來源QA及兩位fresh readers，不寫verify或作者SOURCE／敘事PASS。1900原申請、1940導入日誌未取得，不造心理、利潤或逐年試作；界線留claims，不唸查核警語。BASE、canonical、八語、history、reviews與凍結研究不動；付費/provider/後台/git皆零。',''].join('\n');
write('video.json',doc);write('narration-only.json',rows);write('claims.json',currentClaims);write('series.json',series);fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const script=['# '+doc.youtube.title,'','作者R8材料旅程；HOLD，待獨立差分查核及fresh readers。下一次實際native panel為round7；實聲未量。ID不讀入旁白。',''];let last='';for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+r.chapter,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 R8逐句主張與來源錨點','','全部PENDING_INDEPENDENT_REVIEW；R7 SOURCE收據不自動成為R8判定，無作者SOURCE／敘事PASS。','','| ID | 類型 | 旁白 | 來源 | 定位 |','| --- | --- | --- | --- | --- |'];for(const r of currentClaims.rows)cm.push('| '+r.id+' | '+r.claim_kind+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+' |');for(const r of currentClaims.rows.filter(r=>r.source_anchors.length)){cm.push('','## '+r.id,'');for(const a of r.source_anchors)cm.push('- '+JSON.stringify(a));}cm.push('','## R8書面配鏡差分','','c07u03：'+visualFinding.proposed_prompt_only,'','原件限定：'+visualFinding.source_quote,'','## 範圍界線','','乾花粉末不是pollen；歷史粉劑本來可以販售和撒用，本集不把粉末泛稱為尚非商品。1897手冊是歷史指導與帶商業立場的主張，非現代控制藥效實驗或1888/1902工廠逐批記錄。乾花1–1.5%與抽出製品20%不是當前香體配方或效力倍率。1958不是1955的原因。現代粉料與工法不回填早期。1900原申請、1940導入日誌仍缺；不造產量利潤心理或全產業交棒日。2017筆記照片不等於已讀原全筆記，不複用史料圖。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const roleDelta={scope:'Only jointly failed one_line plus required source-visual V07_01; single-reader scene_first/no_recap and texture advisory were not expanded into edits.',narration_deleted:deletedRows.map(r=>({...r,spoken_units:spokenUnits(r.text),reason:'移除不推進材料成形的相遇/東京/同宿傳記岔路；該句不再留於旁白。'})),narration_changed:changedRows.map(r=>({id:r.id,before:oldRows.get(r.id).text,after:r.text,spoken_unit_delta:spokenUnits(r.text)-spokenUnits(oldRows.get(r.id).text),reason:'章首直接接舶來除蚤粉與竹筒的試作動作；保留來源年份，不借人物相遇開傳記線。'})),prompt_changed:[{id:'c07u03',before:visualFinding.current,after:visualFinding.proposed_prompt_only,source_finding:'V07_01',narration_changed:false}],chapter_marker_transferred:{from:'c07s01',to:'c05r019',title:removedScene.chapter},all_other_retained_scene_objects_exact:true,all_non_scene_video_fields_exact:true,loops_exact:true,added_narration_lines:[],deleted_units:deletedUnits,changed_unit_delta:changedDelta,net_total_unit_delta:total-units(priorRows),net_effective_body_unit_delta:body-priorNotes.native_units.effective_body_excluding_opening_and_outro};
write('revision-edits.json',{revision:8,author_revision_label:'R8',next_actual_native_panel_round:7,prior_video_sha256:R7_SHA,prior_core_four_sha256:R7_CORE,role_delta:roleDelta,loops:doc.loops});
const project=loadProject({root:ROOT,slug:SLUG}),context={canonical_root:ROOT,canonical_video_sha256:fileSha(project.file),initialized_lexicon_sha256:sha(JSON.stringify(project.lexicon)),shelf_lexicon_sha256:sha(JSON.stringify(project.shelfLexicon)),in_memory_substitution_only:['doc','brief','series'],canonical_files_written:false};
project.doc=doc;project.brief=brief;project.series=series;
const lint=lintProject(project),timeline=estimateTimeline(doc),shotEstimates=timeline.scenes.filter(s=>doc.scenes.find(t=>t.id===s.id)?.template==='shot').map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS}));
const maxShot=Math.max(...shotEstimates.map(s=>s.seconds)),cadence=lint.warnings.filter(w=>/no open loop|open loops? planted|condensation plants/.test(w.message));
assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));assert.equal(cadence.length,0,JSON.stringify(cadence));assert(maxShot<=12);
for(const f of protectedFiles)assert.equal(fileSha(f),protectedBefore[f],f);
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs','revision-edits.json'];
const notes={status:'HOLD_PENDING_INDEPENDENT_DELTA_AND_TWO_FRESH_READERS',candidate_revision:'length-r8',author:'/root/c05_material_author',next_actual_native_panel_round:7,parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:R7_SHA,prior_core_four_sha256:R7_CORE,prior_source_receipt:{path:sourceReviewFile,sha256:fileSha(sourceReviewFile),source_video_sha256:R7_SHA,reported_verdict:sourceReview.source_verdict,applies_to_r8:false},independent_source_delta_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_READERS',verify_written:false,source_pass_claimed:false,narrative_pass_claimed:false,role_delta:roleDelta,native_units:{counter:'spokenUnits(spokenText(line))',r7_total:units(priorRows),r7_body_excluding_opening:priorNotes.native_units.body_excluding_opening,r7_effective_body_excluding_opening_and_outro:priorNotes.native_units.effective_body_excluding_opening_and_outro,r8_total:total,opening,outro,body_excluding_opening:total-opening,effective_body_excluding_opening_and_outro:body,added_units:0,deleted_units:deletedUnits,changed_unit_delta:changedDelta,net_total_delta:total-units(priorRows),net_effective_body_delta_from_r7:body-priorNotes.native_units.effective_body_excluding_opening_and_outro,target_actual_body_seconds:[720,840],normal_4_to_5_units_per_second_body_seconds_range:[body/5,body/4],at_4_5_units_per_second:body/4.5,actual_tts_seconds:null,actual_duration_verified:false,length_hold:true,range_is_arithmetic_not_measured_tts:true},counts:{lines:rows.length,scenes:doc.scenes.length,chapters:chapterRows.size,illustrations:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,loops:doc.loops.length,added_lines:0,changed_lines:changedRows.length,deleted_lines:deletedRows.length,prompts_changed:1},native_initialized_context_lint:{context,scope:'author mechanical validation, not independent source/narrative/runtime approval',result:lint,errors:lint.errors.length,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,all_estimated_shots_at_most_12_seconds:maxShot<=12},visual_spec:{...structuredClone(priorNotes.visual_spec),illustration_unit_share:[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(spokenText(x.line)),0)/total,actual_generated_media_reviewed:false},opening_native_units:opening,opening_arithmetic_seconds_at_4_to_5:[opening/5,opening/4],at_least_eight_concrete_action_payoffs_for_fresh_review:structuredClone(priorNotes.at_least_eight_concrete_action_payoffs_for_fresh_review),metadata_changed_from_r7:[],protected_files_unchanged:true,paid_calls:0,provider_calls:0,backend_writes:0,git_commands:0,canonical_written:false,author_ready_for_independent_review:true,frozen_at_utc:new Date().toISOString(),file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))]))};
notes.core_four_sha256=Object.fromEntries(['video.json','brief.md','series.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));
write('author-notes.json',notes);
console.log(JSON.stringify({revision:'length-r8',status:notes.status,next_actual_native_panel_round:7,counts:notes.counts,native_units:notes.native_units,lint_errors:lint.errors,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,core_four_sha256:notes.core_four_sha256,role_delta:roleDelta},null,2));
