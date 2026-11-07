import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine, spokenText, validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {spokenUnits, estimateTimeline, FPS} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {loadProject, lintProject} from '/workspace/work/brand-remakes-source/tools/video/core/state.mjs';

// Author R11. R10 is immutable; only current author files are regenerated.
// loadProject supplies initialized native context; candidate substitutions stay in memory.
const OUT=path.dirname(fileURLToPath(import.meta.url)),BASE=path.resolve(OUT,'../..'),PRIOR=path.join(OUT,'history/r10');
const ROOT='/workspace/work/brand-story-20261025/submission-root',SLUG='story-everyday-kincho-c05-remake-20261025';
const BASE_SHA='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a';
const R10_CORE={'video.json':'3cf768c449dc875e8fefbc04001879e0f6eacd3ad746de9a2146b4c844c6044c','brief.md':'0694de8fa1a910344934b8c5084e53d3db219dcfa8453111f015d4c9309e30f6','series.json':'a50d508be0af86d51636b5fd8437cd0eb0cf9dd4b085a92ff1e914f3266f9de7','claims.json':'99325f782ccb4fc55901b009c1215805a231b2a5cc8bb44afc7325a21e1a2ee9'};
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8')),write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(p,e.name)):[path.join(p,e.name)]);
const protectedFiles=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(e=>e.isFile()).map(e=>path.join(BASE,e.name)),...walk(path.join(BASE,'i18n')),...walk(path.join(ROOT,'docs/videos',SLUG)),...walk(path.join(OUT,'history')),...walk(path.join(OUT,'reviews')),...walk(path.join(BASE,'research-expansion'))];
const protectedBefore=Object.fromEntries(protectedFiles.map(f=>[f,fileSha(f)]));
for(const [f,digest]of Object.entries(R10_CORE))assert.equal(fileSha(path.join(PRIOR,f)),digest,f);
assert.equal(fileSha(path.join(BASE,'video.json')),BASE_SHA);
assert(!fs.readdirSync(OUT,{withFileTypes:true}).some(e=>e.isFile()&&/verify/i.test(e.name)),'Root must remove current verify before author editing.');
const prior=read(path.join(PRIOR,'video.json')),priorRows=read(path.join(PRIOR,'narration-only.json')),priorClaims=read(path.join(PRIOR,'claims.json')),priorNotes=read(path.join(PRIOR,'author-notes.json'));
const oldRows=new Map(priorRows.map(r=>[r.id,r])),oldClaims=new Map(priorClaims.rows.map(r=>[r.id,r]));
const sourceReviewFile=path.join(OUT,'reviews/source-r10-independent.json'),sourceReview=read(sourceReviewFile);
assert.equal(sourceReview.source_video_sha256,R10_CORE['video.json']);assert.equal(sourceReview.source_verdict,'PASS');
const replacements={
  c05r002:'一八九〇年，上山英一郎推出棒狀蚊香，把除蟲菊粉做成了能點燃的細條。',
  c05r020:'開場那種細條，借用的是佛壇線香的製法。',
  c05r021:'可這種細香，能不能完整地送到你手上？',
  c05r023:'原廠留存的一款直條商品，約二十公分長；資料還說，使用時會同時用上數根。',
  c05r092:'我沒想到，原廠的製程解說還把混合與捏和分開：粉料先在混合機裡，混約三十分鐘。',
  c05le010:'原廠製程裡，料片沿輸送帶進入打型機，像餅乾模那樣，切出相連的雙卷。',
  c05rx010:'原廠說，燃燒期間，有效成分會持續以極細微粒子的形式進入空氣。',
};
const deletionReasons={
  c07d06:'刪除對乾燥位置、天氣與產量的抽象小結，讓陰乾負荷直接走向連雨備案。',
  c07s06:'刪除對剛說過六小時、十二小時商品選擇的總結，不再重講長夜有不同刻度。',
  c05le004:'刪除乾粉會散、再問如何成塊的重啟；直接給加水成黏土狀的新工序。',
  c07m01:'刪除剛列過的成形材料／有效成分分工小結；第一人稱反應併入有三十分鐘工序事實的r092。',
  c05le023:'將輸送帶、打型、相連雙卷合併進le010，只講一次現行打型動作。',
  c07m02:'刪除剛裝箱又說材料離廠的過門，直接讓雙卷分開問題接到使用章。',
  c05le014:'將持續釋放的時間尺度併入rx010，不在位置揭露後重啟一次釋放問答。',
  c05le015:'持續釋放事實已完整併入rx010，本句刪除。',
};
const promptReplacements={
  c05r002:'Medium shot of one anonymous adult presenting a plain bundle of thin straight incense sticks against a simple neutral background, soft diffused light.',
  c05le010:'Close-up of an unmarked interlocking spiral die cutting a soft sheet carried by a plain conveyor, diffuse factory light.',
};
const doc=structuredClone(prior);doc.scenes=doc.scenes.filter(s=>!deletionReasons[s.id]);
for(const s of doc.scenes){for(const l of s.lines??[])if(replacements[l.id])l.text=replacements[l.id];if(promptReplacements[s.id])s.data.prompt=promptReplacements[s.id];}
doc.loops=doc.loops.filter(l=>!deletionReasons[l.setup]&&!deletionReasons[l.payoff]&&!(l.setup==='c05le010'&&l.payoff==='c05le023'));
assert.deepEqual(validateVideo(doc),[]);assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.deepEqual(doc.voice,prior.voice);assert.equal(doc.subtitles.burn_in,true);
for(const key of Object.keys(prior).filter(k=>!['scenes','loops'].includes(k)))assert.deepEqual(doc[key],prior[key],key);
for(const s of doc.scenes){const expected=structuredClone(prior.scenes.find(t=>t.id===s.id));for(const l of expected.lines??[])if(replacements[l.id])l.text=replacements[l.id];if(promptReplacements[s.id])expected.data.prompt=promptReplacements[s.id];assert.deepEqual(s,expected,s.id);}
const rows=[];let chapter='';for(const {scene,line}of eachLine(doc)){assert.equal(spokenText(line),line.text);if(scene.chapter)chapter=scene.chapter;rows.push({chapter,id:line.id,text:line.text});}
const index=new Map(rows.map((r,i)=>[r.id,i]));for(const l of doc.loops){assert(index.has(l.setup)&&index.has(l.payoff));assert(index.get(l.setup)<index.get(l.payoff));}
const chapterRows=new Map();for(const r of rows)chapterRows.set(r.chapter,[...(chapterRows.get(r.chapter)??[]),r]);assert.equal(chapterRows.size,6);for(const rr of chapterRows.values())assert(rr.some(r=>r.text.includes('你'))&&rr.some(r=>r.text.includes('我')));
const units=rr=>rr.reduce((n,r)=>n+spokenUnits(r.text),0),total=units(rows),opening=units([...chapterRows.values()][0]),outro=units(rows.filter(r=>['c05r101','c05r102','c05r103'].includes(r.id))),body=total-opening-outro;
const deletedUnits=Object.keys(deletionReasons).reduce((n,id)=>n+spokenUnits(oldRows.get(id).text),0),changedUnitDelta=Object.entries(replacements).reduce((n,[id,text])=>n+spokenUnits(text)-spokenUnits(oldRows.get(id).text),0),unitDelta=changedUnitDelta-deletedUnits;
assert.equal(total,units(priorRows)+unitDelta);
const sourceById=new Map(priorClaims.rows.flatMap(r=>r.sources).map(s=>[s.id,s]));
const anchor=(sourceId,start,end=start)=>{const s=sourceById.get(sourceId),content=fs.readFileSync(s.text_cache,'utf8'),excerpt=content.split(/\r?\n/).slice(start-1,end).join('\n');assert.equal(fileSha(s.raw_cache),s.raw_sha256);return{source_id:sourceId,text_cache:s.text_cache,text_cache_sha256:sha(content),line_start:start,line_end:end,exact_excerpt:excerpt,excerpt_sha256:sha(excerpt)};};
const claims=structuredClone(priorClaims);claims.candidate_revision='length-r11';claims.author='/root/c05_r11_author';claims.status='PENDING_INDEPENDENT_REVIEW_HOLD';claims.parent_candidate_video_sha256=R10_CORE['video.json'];
claims.historical_r9_independent_review=structuredClone(claims.prior_independent_review);
claims.prior_independent_review={path:sourceReviewFile,sha256:fileSha(sourceReviewFile),source_video_sha256:R10_CORE['video.json'],reported_r10_source_verdict:sourceReview.source_verdict,reported_r10_written_visual_verdict:sourceReview.written_visual_verdict,scope:'R10 only. R11 narration/prompt/claims delta requires another reviewer.'};
claims.rows=rows.map(r=>{const c=structuredClone(oldClaims.get(r.id));c.r10_claim_sha256=sha(oldRows.get(r.id).text);c.claim=r.text;c.chapter=r.chapter;c.change=replacements[r.id]?'REWRITTEN_IN_R11':'R10_TEXT_RETAINED';c.status='PENDING_INDEPENDENT_REVIEW';return c;});
const cm=new Map(claims.rows.map(r=>[r.id,r]));
Object.assign(cm.get('c05r002'),{claim_kind:'ATTRIBUTED_HISTORICAL_EVENT',source_ids:['K_M','K_F'],sources:['K_M','K_F'].map(id=>sourceById.get(id)),locator:'K_M 37–39：1890棒狀蚊香發明／上市；K_F 49：創辦人上山英一郎歸屬，62：粉料固成棒狀。只講推出商品，不編當日工作臺、手勢、對白或特定買家；未把K_T的1911–1914留存實物尺寸指定為1890規格。',source_anchors:[anchor('K_M',37,39),anchor('K_F',49),anchor('K_F',62)]});
Object.assign(cm.get('c05r020'),{locator:'精確回呼開場的細條，新增佛壇線香製法；K_T 33與K_F 62。未重報1890上市。',source_anchors:[anchor('K_T',33),anchor('K_F',62)]});
Object.assign(cm.get('c05r021'),{source_ids:['K_F','EDITORIAL'],sources:[sourceById.get('K_F')],locator:'向前運送問題，下一個新事實為細條運送中容易折；刪除重報1890上市。',source_anchors:[anchor('K_F',62)]});
Object.assign(cm.get('c05r023'),{locator:'K_T 33–34：此為原廠留存商品條目，製作年1911–1914；20cm／數根並用不硬合成1890上市時實物規格。',source_anchors:[anchor('K_T',33,34)]});
Object.assign(cm.get('c05r092'),{locator:'K_PROCESS_R5 2、4段：先混約三十分鐘，再移至捏和機；用具體工序承接第一人稱反應，刪原m01分工小結。',claim_kind:'FACT_WITH_AUTHOR_REACTION'});
Object.assign(cm.get('c05le010'),{source_ids:['K_PROCESS_R5','NM_MACHINE'],sources:['K_PROCESS_R5','NM_MACHINE'].map(id=>sourceById.get(id)),locator:'K_PROCESS_R5第7段：輸送帶送片、打出相連雙卷；NM_MACHINE 399：餅乾模類比。兩句原打型描述合併成一次現行動作，非1940或1957同批機器現場。',source_anchors:[...oldClaims.get('c05le023').source_anchors,...oldClaims.get('c05le010').source_anchors]});
Object.assign(cm.get('c05rx010'),{locator:'K_F 79：極細微粒子進入空氣；80末：燃燒期間持續釋放。合併空間形式與時間尺度，不在le014/le015另啟同題。',source_anchors:[anchor('K_F',79),anchor('K_F',80)]});
claims.chronology_scope_r11={opening_event:{year:1890,person:'上山英一郎',action:'推出棒狀蚊香',sources:['K_M','K_F'],imagined_contemporaneous_event:false},surviving_straight_product:{source:'K_T',catalogue_manufacture_years:[1911,1914],length_cm:20,same_1890_artifact_claimed:false},handbook:structuredClone(priorNotes.chronology_scope.handbook),r10_omitted_1888_trial_not_restored:true,same_batch_across_sources_claimed:false,modern_stamping_assigned_to_1940_machine:false,status:'AUTHOR_SCOPE_PENDING_INDEPENDENT_REVIEW'};
assert.deepEqual(claims.rows.map(r=>r.claim),rows.map(r=>r.text));
const series={...read(path.join(PRIOR,'series.json')),status:'hold_r11_material_journey_pending_independent_delta_and_fresh_readers',candidate_revision:'length-r11',parent_candidate_video_sha256:R10_CORE['video.json']};
const roleDelta={scope:'R10 shared scene_first/no_recap: replace the imagined opening with a sourced event and remove recap throughout; keep the passed R10 chronology correction.',narration_changed:Object.entries(replacements).map(([id,text])=>({id,before:oldRows.get(id).text,after:text,spoken_unit_delta:spokenUnits(text)-spokenUnits(oldRows.get(id).text)})),narration_deleted:Object.entries(deletionReasons).map(([id,reason])=>({id,text:oldRows.get(id).text,spoken_units:spokenUnits(oldRows.get(id).text),reason})),prompts_changed:Object.entries(promptReplacements).map(([id,after])=>({id,before:prior.scenes.find(s=>s.id===id).data.prompt,after})),loops_deleted:prior.loops.filter(l=>!doc.loops.some(t=>JSON.stringify(t)===JSON.stringify(l))),all_other_narration_exact:true,all_other_retained_scene_objects_exact:true,all_non_scene_video_fields_except_loops_exact:true,added_narration_lines:[],deleted_narration_lines:Object.keys(deletionReasons),net_total_unit_delta:unitDelta,net_effective_body_unit_delta:body-priorNotes.native_units.effective_body_excluding_opening_and_outro,new_historical_experiment_or_psychology_claim:false,padding_added:false};
const brief=[
  '# C05 R11｜一卷香的百年材料旅程','',
  '狀態：HOLD。作者revision R11，下一次實際native讀者panel為round10。R10來源及配鏡PASS只對R10雜湊有效；R11待另一位來源差分查核與兩位fresh readers。實聲、長度與媒體未核准。','',
  '### 選項 A：把材料交到長夜裡','',
  '乾花粉末／有效成分→成形→交付→使用，一條材料旅程。主角是材料的工作，不是跨百年同一包粉。1897手冊、歷史工具、2017研究回顧與未標日期的原廠製程各有歸屬。乾花粉末不是花粉pollen；粉劑本來可以出售或撒用，本集追的是它如何成為可燃燒、可交付的一卷香。','',
  '## 問題','','一把會散的乾花粉末，憑什麼變成能陪你過夜的商品？','',
  '## 一句答案','','讓材料在該留的時候留住，到了使用時，再有節奏地離開。','',
  '## 站主觀點','','用動作帶出材料取捨：採後乾燥能力、細切快乾的書中代價、篩粉和存粉、手盤與打型，再讓使用者拆卷和安放完成交接。天然成分身分只作為從乾花走向已知成分的一關，不列化學名或商品型錄；1958研究不倒寫成1955導入的原因。','',
  '## R11精確修改','',
  'r002以K_M與K_F支持的1890上山英一郎推出棒狀蚊香，取代虛擬夜景。r001保留早期四十分鐘利害；不把留存的1911–1914年二十公分實物硬接成1890規格。r020精確回呼開場細條，給佛壇線香製法新事實；r021不再報一次上市；r023標明原廠留存的一款商品。','',
  '刪除le004乾粉散落的重啟、d06乾燥負荷小結、s06長夜時間選擇小結、m01成形與殺蟲分工小結、m02裝箱離廠過門。m01的第一人稱反應併入r092三十分鐘混合的新工序。le010與le023只留一次輸送帶／刀模打型；rx010合併微粒與燃燒期間持續釋放，刪le014/le015重啟問答。八句刪除、七句改寫、兩個提示詞改動；不以同義詞藏重述，不另加材料支線填長。','',
  'R10刪除的1888試作不恢復；1897書仍是旁白讀後來出版手冊的工序說明，非1880年代同批工廠紀錄。1940完成、約1957舊設備使用期和現行製程各有歸屬。其餘敘事、章名、標題、片尾三句與技術設定保留。','',
  '## 長度與執行規格','',
  `native總量${total} units；開場${opening}；排開場正文${total-opening}；有聲片尾${outro}；再扣有聲片尾的有效正文${body}。相較R10有效正文3055，淨變化${body-3055}。4–5units/s算術範圍${(body/5).toFixed(1)}–${(body/4).toFixed(1)}秒；4.5units/s約${(body/4.5).toFixed(1)}秒。不是實聲量測；實聲正文720–840秒仍HOLD，不慢播、停頓或灌字補足。`,'',
  '原slug、Sulafat台灣自然語速與技術設定保留。look只有{preset:cute-mystery}、image-01、英文匿名概念插圖，無人名品牌logo或可讀字，不複用史料圖。至少70%插圖、連卡最多3、stillmotion、native每景≤12秒；繁中燒錄及CC。5秒片頭、21秒正式v4片尾僅待執行規格，未造媒體。縮圖layout d，金鳥品牌、黃字黑框主標、白短副標。','',
  '## 未解除的關卡','','需另一位來源QA及兩位fresh readers，不寫verify或作者SOURCE／敘事PASS。1900原申請、1940導入日誌未取得，不造心理、利潤或逐年試作；界線留claims，不唸查核警語。BASE、canonical、八語、history、reviews與凍結研究不動；付費/provider/後台/git皆零。','',
].join('\n');
write('video.json',doc);write('narration-only.json',rows);write('claims.json',claims);write('series.json',series);fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const script=['# '+doc.youtube.title,'','作者R11材料旅程；HOLD，待獨立差分查核及兩位fresh readers。下一次實際native panel為round10；實聲未量。ID不讀入旁白。',''];let last='';for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+r.chapter,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const markdown=['# C05 R11逐句主張與來源錨點','','全部PENDING_INDEPENDENT_REVIEW；R10收據不自動成為R11判定，無作者SOURCE／敘事PASS。','','| ID | 類型 | 旁白 | 來源 | 定位 |','| --- | --- | --- | --- | --- |'];for(const r of claims.rows)markdown.push('| '+r.id+' | '+r.claim_kind+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+' |');for(const r of claims.rows.filter(r=>r.source_anchors.length)){markdown.push('','## '+r.id,'');for(const a of r.source_anchors)markdown.push('- '+JSON.stringify(a));}
markdown.push('','## R11時間與回呼範圍','',JSON.stringify(claims.chronology_scope_r11,null,2),'','乾花粉末不是pollen；歷史粉劑本來可以販售和撒用。1897手冊是歷史指導與帶商業立場的主張，非現代控制藥效實驗或1888/1902工廠逐批記錄。乾花1–1.5%與抽出製品20%不是當前香體配方或效力倍率。1958不是1955的原因。現代粉料與工法不回填早期。1900原申請、1940導入日誌仍缺；不造產量利潤心理或全產業交棒日。2017筆記照片不等於已讀原全筆記，不複用史料圖。','');fs.writeFileSync(path.join(OUT,'claims.md'),markdown.join('\n'));
write('revision-edits.json',{revision:11,author_revision_label:'R11',next_actual_native_panel_round:10,prior_video_sha256:R10_CORE['video.json'],prior_core_four_sha256:R10_CORE,role_delta:roleDelta,loops:doc.loops});
const loaded=loadProject({root:ROOT,slug:SLUG}),context={canonical_root:ROOT,canonical_video_sha256:fileSha(loaded.file),initialized_lexicon_sha256:sha(JSON.stringify(loaded.lexicon)),shelf_lexicon_sha256:sha(JSON.stringify(loaded.shelfLexicon)),in_memory_substitution_only:['doc','brief','series'],canonical_files_written:false};assert.equal(context.canonical_video_sha256,BASE_SHA);
const lint=lintProject({...loaded,doc:structuredClone(doc),brief,series:structuredClone(series)}),timeline=estimateTimeline(doc),shots=timeline.scenes.filter(s=>doc.scenes.find(t=>t.id===s.id)?.template==='shot').map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS}));
const maxShot=Math.max(...shots.map(s=>s.seconds)),cadence=lint.warnings.filter(w=>/no open loop|open loops? planted|condensation plants/.test(w.message));assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));assert.equal(cadence.length,0,JSON.stringify(cadence));assert(maxShot<=12);
for(const f of protectedFiles)assert.equal(fileSha(f),protectedBefore[f],f);
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs','revision-edits.json'];
const notes={status:'HOLD_PENDING_INDEPENDENT_DELTA_AND_TWO_FRESH_READERS',candidate_revision:'length-r11',author:'/root/c05_r11_author',next_actual_native_panel_round:10,parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:R10_CORE['video.json'],prior_core_four_sha256:R10_CORE,prior_source_receipt:{path:sourceReviewFile,sha256:fileSha(sourceReviewFile),source_video_sha256:R10_CORE['video.json'],reported_source_verdict:sourceReview.source_verdict,reported_written_visual_verdict:sourceReview.written_visual_verdict,applies_to_r11:false},independent_source_delta_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_READERS',verify_written:false,source_pass_claimed:false,narrative_pass_claimed:false,role_delta:roleDelta,chronology_scope:claims.chronology_scope_r11,native_units:{counter:'spokenUnits(spokenText(line))',r10_total:units(priorRows),r10_body_excluding_opening:priorNotes.native_units.body_excluding_opening,r10_effective_body_excluding_opening_and_outro:priorNotes.native_units.effective_body_excluding_opening_and_outro,r11_total:total,opening,outro,body_excluding_opening:total-opening,effective_body_excluding_opening_and_outro:body,added_units:0,deleted_units:deletedUnits,changed_unit_delta:changedUnitDelta,net_total_delta:unitDelta,net_effective_body_delta_from_r10:body-priorNotes.native_units.effective_body_excluding_opening_and_outro,target_actual_body_seconds:[720,840],normal_4_to_5_units_per_second_body_seconds_range:[body/5,body/4],at_4_5_units_per_second:body/4.5,actual_tts_seconds:null,actual_duration_verified:false,length_hold:true,range_is_arithmetic_not_measured_tts:true},counts:{lines:rows.length,scenes:doc.scenes.length,chapters:chapterRows.size,illustrations:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,loops:doc.loops.length,added_lines:0,changed_lines:Object.keys(replacements).length,deleted_lines:Object.keys(deletionReasons).length,prompts_changed:Object.keys(promptReplacements).length},native_initialized_context_lint:{context,scope:'author mechanical validation only; not independent source/narrative/runtime approval',result:lint,errors:lint.errors.length,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,all_estimated_shots_at_most_12_seconds:maxShot<=12},visual_spec:{...structuredClone(priorNotes.visual_spec),illustration_unit_share:[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(spokenText(x.line)),0)/total,actual_generated_media_reviewed:false},opening_native_units:opening,opening_arithmetic_seconds_at_4_to_5:[opening/5,opening/4],at_least_eight_concrete_action_payoffs_for_fresh_review:priorNotes.at_least_eight_concrete_action_payoffs_for_fresh_review.filter(l=>index.has(l.setup)&&index.has(l.payoff)),metadata_changed_from_r10:[],protected_files_unchanged:true,paid_calls:0,provider_calls:0,backend_writes:0,git_commands:0,canonical_written:false,author_ready_for_independent_review:true,frozen_at_utc:new Date().toISOString(),file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))]))};
notes.core_four_sha256=Object.fromEntries(['video.json','brief.md','series.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));notes.submission_four_sha256=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));write('author-notes.json',notes);
console.log(JSON.stringify({revision:'length-r11',status:notes.status,next_actual_native_panel_round:10,counts:notes.counts,native_units:notes.native_units,lint_errors:lint.errors,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,submission_four_sha256:notes.submission_four_sha256,core_four_sha256:notes.core_four_sha256,role_delta:roleDelta},null,2));
