import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine, spokenText, validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {spokenUnits, estimateTimeline, FPS} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {loadProject, lintProject} from '/workspace/work/brand-remakes-source/tools/video/core/state.mjs';

// Author R10: local deletion of the 1888 trial, with later handbook attribution preserved.
// Root has frozen R9 and removed current verify. No canonical/runtime files are written.
const OUT=path.dirname(fileURLToPath(import.meta.url)),BASE=path.resolve(OUT,'../..'),PRIOR=path.join(OUT,'history/r9');
const ROOT='/workspace/work/brand-story-20261025/submission-root',SLUG='story-everyday-kincho-c05-remake-20261025';
const BASE_SHA='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a';
const R9_SHA='627eb73b3756529308800a1091ca0a8dfc3a5b3374aeb13084df30291b280e51';
const R9_CORE={'video.json':R9_SHA,'brief.md':'a1a05dc37b9b5fc7fff5d5442e83b0bf68c3420e835d012640501b0b6b82117a','series.json':'3b11cbb951850d3d1ce8b51497c2758604ff4e1c15898217231b118d2e7c8b9e','claims.json':'fbcc96591a68724c17517738c9f44d4e865fe825fa14951fbb5597af771d47c4'};
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8')),write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(p,e.name)):[path.join(p,e.name)]);
const protectedFiles=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(e=>e.isFile()).map(e=>path.join(BASE,e.name)),...walk(path.join(BASE,'i18n')),...walk(path.join(ROOT,'docs/videos',SLUG)),...walk(path.join(OUT,'history')),...walk(path.join(OUT,'reviews')),...walk(path.join(BASE,'research-expansion'))];
const protectedBefore=Object.fromEntries(protectedFiles.map(f=>[f,fileSha(f)]));
for(const [f,digest]of Object.entries(R9_CORE))assert.equal(fileSha(path.join(PRIOR,f)),digest,f);
assert.equal(fileSha(path.join(BASE,'video.json')),BASE_SHA);
assert(!fs.readdirSync(OUT,{withFileTypes:true}).some(e=>e.isFile()&&/verify/i.test(e.name)),'Root must remove current verify before R10.');
const prior=read(path.join(PRIOR,'video.json')),priorRows=read(path.join(PRIOR,'narration-only.json')),priorClaims=read(path.join(PRIOR,'claims.json')),priorNotes=read(path.join(PRIOR,'author-notes.json'));
const oldRows=new Map(priorRows.map(r=>[r.id,r])),oldScenes=new Map(prior.scenes.map(s=>[s.id,s]));
const sourceReviewFile=path.join(OUT,'reviews/source-r9-independent.json'),sourceReview=read(sourceReviewFile);
assert.equal(sourceReview.source_video_sha256,R9_SHA);assert.equal(sourceReview.source_verdict,'PASS');
const deletedId='c05r019',chapterMovedTo='c05r020',deletedScene=oldScenes.get(deletedId);
const replacements={
  c07d02:'我讀到上山英一郎後來出版的《除虫菊栽培書》，才發現花採下來以後，還有一場趕工。',
  c07d03:'這本書的第五版，寫的是把鮮花充分乾燥，再做成殺蟲粉；碰到天氣不配合呢？',
};
const doc=structuredClone(prior);assert.equal(deletedScene.lines.length,1);assert.equal(deletedScene.lines[0].id,deletedId);
assert(!doc.loops.some(l=>l.setup===deletedId||l.payoff===deletedId));
doc.scenes=doc.scenes.filter(s=>s.id!==deletedId);doc.scenes.find(s=>s.id===chapterMovedTo).chapter=deletedScene.chapter;
for(const [id,text]of Object.entries(replacements)){const scene=doc.scenes.find(s=>s.id===id);assert.equal(scene.lines.length,1);scene.lines[0].text=text;}
for(const key of Object.keys(prior).filter(k=>k!=='scenes'))assert.deepEqual(doc[key],prior[key],key);
for(const s of doc.scenes){const expected=structuredClone(oldScenes.get(s.id));if(replacements[s.id])expected.lines[0].text=replacements[s.id];if(s.id===chapterMovedTo)expected.chapter=deletedScene.chapter;assert.deepEqual(s,expected,s.id);}
assert.deepEqual(validateVideo(doc),[]);assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.deepEqual(doc.voice,prior.voice);assert.equal(doc.subtitles.burn_in,true);
const rows=[];let chapter='';for(const {scene,line}of eachLine(doc)){if(scene.chapter)chapter=scene.chapter;rows.push({chapter,id:line.id,text:line.text});}
for(const r of rows)if(!replacements[r.id])assert.deepEqual(r,oldRows.get(r.id),r.id);
assert.equal(rows.length,priorRows.length-1);assert(!rows.some(r=>r.id===deletedId));
const index=new Map(rows.map((r,i)=>[r.id,i]));for(const l of doc.loops){assert(index.has(l.setup)&&index.has(l.payoff));assert(index.get(l.setup)<index.get(l.payoff));}assert.equal(index.get(chapterMovedTo),index.get('c07d18')+1);
const chapterRows=new Map();for(const r of rows)chapterRows.set(r.chapter,[...(chapterRows.get(r.chapter)??[]),r]);assert.equal(chapterRows.size,6);for(const rr of chapterRows.values())assert(rr.some(r=>r.text.includes('你'))&&rr.some(r=>r.text.includes('我')));
const units=rr=>rr.reduce((n,r)=>n+spokenUnits(r.text),0),total=units(rows),opening=units([...chapterRows.values()][0]),outro=units(rows.filter(r=>['c05r101','c05r102','c05r103'].includes(r.id))),body=total-opening-outro;
const deletedUnits=spokenUnits(oldRows.get(deletedId).text),changedUnitDelta=Object.entries(replacements).reduce((n,[id,text])=>n+spokenUnits(text)-spokenUnits(oldRows.get(id).text),0),unitDelta=changedUnitDelta-deletedUnits;assert.equal(total,units(priorRows)+unitDelta);
const chronologyScope={
  omitted_trial:{id:deletedId,year:1888,source_id:'K_M',reason:'Unnecessary return to an earlier trial after material preparation; retained only in immutable R9 history.'},
  handbook:{source_id:'NDL1897',title:'除虫菊栽培書 5版',publication_year:1897,spoken_attribution:['c07d02','c07d03'],scope:'The narrator consults a later-published handbook to explain its stated material procedures. These are not an 1886/1887 factory batch or proof that the 1890 product used every step.'},
  material_sequence:'花的收成→書中記載的乾燥、製粉與保存→香體形狀→成形與交付→使用',same_batch_across_sources_claimed:false,handbook_causes_1890_product_claimed:false,historical_causality_added:false,status:'AUTHOR_SCOPE_PENDING_INDEPENDENT_REVIEW',
};
const claims=structuredClone(priorClaims);claims.candidate_revision='length-r10';claims.author='/root/c05_r10_author';claims.status='PENDING_INDEPENDENT_REVIEW_HOLD';claims.parent_candidate_video_sha256=R9_SHA;
claims.historical_r8_independent_review=structuredClone(claims.prior_independent_review);
claims.prior_independent_review={path:sourceReviewFile,sha256:fileSha(sourceReviewFile),source_video_sha256:R9_SHA,reported_r9_source_verdict:sourceReview.source_verdict,reported_r9_written_visual_verdict:sourceReview.written_visual_verdict,scope:'R9 receipt only; R10 deletion and attribution wording remain pending another reviewer.'};
claims.rows=claims.rows.filter(r=>r.id!==deletedId);claims.chronology_scope_r10=chronologyScope;
for(const r of claims.rows){r.r9_claim_sha256=sha(oldRows.get(r.id).text);r.change=replacements[r.id]?'REWRITTEN_IN_R10':'R9_TEXT_RETAINED';r.status='PENDING_INDEPENDENT_REVIEW';if(replacements[r.id]){r.claim=replacements[r.id];r.chronological_attribution_scope={publication_year:1897,source_id:'NDL1897',retrospective_handbook_reading:true,actual_1880s_factory_or_same_batch_claim:false};}const old=priorClaims.rows.find(x=>x.id===r.id);assert.deepEqual(r.source_ids,old.source_ids);assert.deepEqual(r.sources,old.sources);assert.deepEqual(r.source_anchors,old.source_anchors);assert.equal(r.claim,rows.find(x=>x.id===r.id).text);}assert.equal(claims.rows.length,rows.length);
const series={...read(path.join(PRIOR,'series.json')),status:'hold_r10_material_journey_pending_independent_delta_and_fresh_readers',candidate_revision:'length-r10',parent_candidate_video_sha256:R9_SHA,independent_source_review_required:true,two_isolated_narrative_readers_required:true,target_minutes:13};
const deltaDescription='刪除c05r019整句與整景的1888舶來除蚤粉／竹筒試作，使c07d18的形狀問題直接由c05r020的細條承接；章標記移到c05r020，章名不變。c07d02只加「後來」，明確是旁白讀後來出版的手冊；c07d03將「一八九七年的第五版」改成「這本書的第五版」，保留整段的書中記載歸屬。出版年1897完整留在逐句來源與作者註。不是把1897手冊移到1880年代，也不聲稱這些做法是1887收成或1890商品的同一工廠批次，更不造手冊造成直條上市的歷史因果。其餘114句旁白、所有保留提示詞、39組loops、章名、承諾、標題和技術設定不改。';
const brief=[
  '# C05 R10｜一卷香的百年材料旅程','',
  '狀態：HOLD。作者revision R10，下一次實際native讀者panel為round9。R9的來源、配鏡與panel收據只對R9雜湊有效，本版待獨立差分查核與新讀者；實聲和媒體未核准。','',
  '### 選項 A：把材料交到長夜裡','',
  '乾花粉末／有效成分→成形→交付→使用，一條材料旅程。主角是材料的工作，不是跨百年同一包粉。1897手冊、歷史工具、2017研究回顧與未標日期的原廠製程各有歸屬。乾花粉末不是花粉pollen；粉劑本來可以出售或撒用，本集追的是它如何成為可燃燒、可交付的一卷香。','',
  '## 問題','','一把會散的乾花粉末，憑什麼變成能陪你過夜的商品？','',
  '## 一句答案','','讓材料在該留的時候留住，到了使用時，再有節奏地離開。','',
  '## 站主觀點','','用動作帶出材料取捨：採後乾燥能力、細切快乾的書中代價、篩粉和存粉、手盤與打型，再讓使用者拆卷和安放完成交接。天然成分身分只作為從乾花走向已知成分的一關，不列化學名或商品型錄；1958研究不倒寫成1955導入的原因。','',
  '## R10精確修改','',deltaDescription,'',
  '## 長度與執行規格','',
  'native總量'+total+' units；開場'+opening+'；排開場正文'+(total-opening)+'；有聲片尾'+outro+'；再扣有聲片尾的有效正文'+body+'。相較R9有效正文3081，淨變化'+unitDelta+'（刪句-'+deletedUnits+'，兩句改字淨'+changedUnitDelta+'）。4–5units/s算術範圍'+(body/5).toFixed(1)+'–'+(body/4).toFixed(1)+'秒；4.5units/s約'+(body/4.5).toFixed(1)+'秒。不是實聲量測；實聲正文720–840秒仍HOLD，不慢播、停頓或灌字補足。','',
  '原slug、Sulafat台灣自然語速與技術設定保留。look只有{preset:cute-mystery}、image-01、英文匿名概念插圖，無人名品牌logo或可讀字，不複用史料圖。至少70%插圖、連卡最多3、stillmotion、native每景≤12秒；繁中燒錄及CC。5秒片頭、21秒正式v4片尾僅待執行規格，未造媒體。縮圖layout d，金鳥品牌、黃字黑框主標、白短副標。','',
  '## 未解除的關卡','','需另一位來源QA及兩位fresh readers，不寫verify或作者SOURCE／敘事PASS。1900原申請、1940導入日誌未取得，不造心理、利潤或逐年試作；界線留claims，不唸查核警語。BASE、canonical、八語、history、reviews與凍結研究不動；付費/provider/後台/git皆零。','',
].join('\n');
write('video.json',doc);write('narration-only.json',rows);write('claims.json',claims);write('series.json',series);fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const script=['# '+doc.youtube.title,'','作者R10材料旅程；HOLD，待獨立差分查核及fresh readers。下一次實際native panel為round9；實聲未量。ID不讀入旁白。',''];let last='';for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+r.chapter,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 R10逐句主張與來源錨點','','全部PENDING_INDEPENDENT_REVIEW；R9收據不自動成為R10判定，無作者SOURCE／敘事PASS。','','| ID | 類型 | 旁白 | 來源 | 定位 |','| --- | --- | --- | --- | --- |'];for(const r of claims.rows)cm.push('| '+r.id+' | '+r.claim_kind+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+' |');for(const r of claims.rows.filter(r=>r.source_anchors.length)){cm.push('','## '+r.id,'');for(const a of r.source_anchors)cm.push('- '+JSON.stringify(a));}
cm.push('','## R10局部時間線修正','',deltaDescription,'','《除虫菊栽培書》第五版出版年仍為1897，NDL原書目與原掃來源不變。上述是旁白讀後來出版手冊的材料工序說明；不是1886/1887實際收成批次、不是1880年代金鳥按第五版製程生產的記錄，也不是1890商品實際採用每一步或由這本手冊促成的證據。原1888舶來除蚤粉配方未知，刪除後不與手冊粉料接成同一批。','','## 保留的具體結果','','c07d11：'+rows.find(r=>r.id==='c07d11').text,'','c07d12：'+rows.find(r=>r.id==='c07d12').text,'','來源：NDL1897第五版p25／畫幅16左頁，N25_SIEVE；只問搗碎/過篩的下一個材料動作，不替歷史人物或觀眾選擇乾燥取捨。','','## 範圍界線','','乾花粉末不是pollen；歷史粉劑本來可以販售和撒用，本集不把粉末泛稱為尚非商品。1897手冊是歷史指導與帶商業立場的主張，非現代控制藥效實驗或1888/1902工廠逐批記錄。乾花1–1.5%與抽出製品20%不是當前香體配方或效力倍率。1958不是1955的原因。現代粉料與工法不回填早期。1900原申請、1940導入日誌仍缺；不造產量利潤心理或全產業交棒日。2017筆記照片不等於已讀原全筆記，不複用史料圖。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const roleDelta={scope:'Only the jointly failed one_line timeline break at c05r019 and necessary handbook attribution; single-reader no_recap/no_detour were not pursued.',narration_changed:Object.entries(replacements).map(([id,text])=>({id,before:oldRows.get(id).text,after:text,spoken_unit_delta:spokenUnits(text)-spokenUnits(oldRows.get(id).text),reason:id==='c07d02'?'明確為旁白讀後來出版手冊，保留跨來源／跨批次界線。':'保留第五版和書中歸屬；來源出版年1897完整留claims，避免當作工序發生時間。'})),narration_deleted:[{id:deletedId,text:oldRows.get(deletedId).text,spoken_units:deletedUnits,reason:'移除不必要的1888試作回頭，讓粉料形狀問題直接交到直條。'}],scene_deleted:deletedId,chapter_marker_moved:{from:deletedId,to:chapterMovedTo,title:deletedScene.chapter},prompt_changed:[],all_retained_prompts_exact:true,all_other_scene_objects_exact_except_chapter_transfer:true,all_other_narration_exact:true,all_non_scene_video_fields_exact:true,all_prior_39_loops_exact:true,added_narration_lines:[],deleted_narration_lines:[deletedId],new_historical_choice_or_experiment_claim:false,handbook_publication_year_retained_in_claims:1897,handbook_same_1880s_factory_batch_claimed:false,net_total_unit_delta:unitDelta,net_effective_body_unit_delta:unitDelta};
write('revision-edits.json',{revision:10,author_revision_label:'R10',next_actual_native_panel_round:9,prior_video_sha256:R9_SHA,prior_core_four_sha256:R9_CORE,role_delta:roleDelta,loops:doc.loops});
const loaded=loadProject({root:ROOT,slug:SLUG}),context={canonical_root:ROOT,canonical_video_sha256:fileSha(loaded.file),initialized_lexicon_sha256:sha(JSON.stringify(loaded.lexicon)),shelf_lexicon_sha256:sha(JSON.stringify(loaded.shelfLexicon)),in_memory_substitution_only:['doc','brief','series'],canonical_files_written:false};assert.equal(context.canonical_video_sha256,BASE_SHA);
const project={...loaded,doc:structuredClone(doc),brief,series:structuredClone(series)},lint=lintProject(project),timeline=estimateTimeline(doc),shots=timeline.scenes.filter(s=>doc.scenes.find(t=>t.id===s.id)?.template==='shot').map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS}));
const maxShot=Math.max(...shots.map(s=>s.seconds)),cadence=lint.warnings.filter(w=>/no open loop|open loops? planted|condensation plants/.test(w.message));assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));assert.equal(cadence.length,0,JSON.stringify(cadence));assert(maxShot<=12);
for(const f of protectedFiles)assert.equal(fileSha(f),protectedBefore[f],f);
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs','revision-edits.json'];
const notes={status:'HOLD_PENDING_INDEPENDENT_DELTA_AND_TWO_FRESH_READERS',candidate_revision:'length-r10',author:'/root/c05_r10_author',next_actual_native_panel_round:9,parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:R9_SHA,prior_core_four_sha256:R9_CORE,prior_source_receipt:{path:sourceReviewFile,sha256:fileSha(sourceReviewFile),source_video_sha256:R9_SHA,reported_source_verdict:sourceReview.source_verdict,reported_written_visual_verdict:sourceReview.written_visual_verdict,applies_to_r10:false},independent_source_delta_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_READERS',verify_written:false,source_pass_claimed:false,narrative_pass_claimed:false,role_delta:roleDelta,chronology_scope:chronologyScope,native_units:{counter:'spokenUnits(spokenText(line))',r9_total:units(priorRows),r9_body_excluding_opening:priorNotes.native_units.body_excluding_opening,r9_effective_body_excluding_opening_and_outro:priorNotes.native_units.effective_body_excluding_opening_and_outro,r10_total:total,opening,outro,body_excluding_opening:total-opening,effective_body_excluding_opening_and_outro:body,added_units:0,deleted_units:deletedUnits,changed_unit_delta:changedUnitDelta,net_total_delta:unitDelta,net_effective_body_delta_from_r9:unitDelta,target_actual_body_seconds:[720,840],normal_4_to_5_units_per_second_body_seconds_range:[body/5,body/4],at_4_5_units_per_second:body/4.5,actual_tts_seconds:null,actual_duration_verified:false,length_hold:true,range_is_arithmetic_not_measured_tts:true},counts:{lines:rows.length,scenes:doc.scenes.length,chapters:chapterRows.size,illustrations:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,loops:doc.loops.length,added_lines:0,changed_lines:2,deleted_lines:1,prompts_changed:0},native_initialized_context_lint:{context,scope:'author mechanical validation, not independent source/narrative/runtime approval',result:lint,errors:lint.errors.length,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,all_estimated_shots_at_most_12_seconds:maxShot<=12},visual_spec:{...structuredClone(priorNotes.visual_spec),illustration_unit_share:[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(spokenText(x.line)),0)/total,actual_generated_media_reviewed:false},opening_native_units:opening,opening_arithmetic_seconds_at_4_to_5:[opening/5,opening/4],at_least_eight_concrete_action_payoffs_for_fresh_review:structuredClone(priorNotes.at_least_eight_concrete_action_payoffs_for_fresh_review),metadata_changed_from_r9:[],protected_files_unchanged:true,paid_calls:0,provider_calls:0,backend_writes:0,git_commands:0,canonical_written:false,author_ready_for_independent_review:true,frozen_at_utc:new Date().toISOString(),file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))]))};
notes.core_four_sha256=Object.fromEntries(['video.json','brief.md','series.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));notes.submission_four_sha256=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));write('author-notes.json',notes);
console.log(JSON.stringify({revision:'length-r10',status:notes.status,next_actual_native_panel_round:9,counts:notes.counts,native_units:notes.native_units,lint_errors:lint.errors,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,submission_four_sha256:notes.submission_four_sha256,role_delta:roleDelta},null,2));
