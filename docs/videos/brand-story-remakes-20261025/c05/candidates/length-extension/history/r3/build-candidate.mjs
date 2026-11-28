import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {spokenUnits} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {eachLine,validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {lintVideo} from '/workspace/work/brand-remakes-source/tools/video/core/lint.mjs';

const OUT=path.dirname(fileURLToPath(import.meta.url));
const BASE='/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c05';
const CANON='/workspace/work/brand-story-20261025/submission-root/docs/videos/story-everyday-kincho-c05-remake-20261025';
const PRIOR=path.join(OUT,'history/r2');
const EXPECTED='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a';
const PRIOR_SHA='efbe5021a8dac732a71376f307903a5cf8220409a405130f59f742ddc96a57de';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const fileSha=p=>sha(fs.readFileSync(p));
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const writeJson=(name,value)=>fs.writeFileSync(path.join(OUT,name),JSON.stringify(value,null,2)+'\n');
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(x=>x.isDirectory()?walk(path.join(dir,x.name)):[path.join(dir,x.name)]);}
const protectedPaths=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(x=>x.isFile()).map(x=>path.join(BASE,x.name)),...walk(CANON),...walk(path.join(OUT,'history')),...walk(path.join(OUT,'reviews'))];
const protectedBefore=Object.fromEntries(protectedPaths.map(p=>[p,fileSha(p)]));
assert.equal(fileSha(path.join(BASE,'video.json')),EXPECTED);
assert.equal(fileSha(path.join(CANON,'video.json')),EXPECTED);
assert.equal(fileSha(path.join(PRIOR,'video.json')),PRIOR_SHA);
const prior=read(path.join(PRIOR,'video.json'));
const base=read(path.join(BASE,'video.json'));
const priorRows=read(path.join(PRIOR,'narration-only.json'));
const priorMap=new Map(priorRows.map(r=>[r.id,r]));
const priorClaims=new Map(read(path.join(PRIOR,'claims.json')).rows.map(r=>[r.id,r]));
const priorNotes=read(path.join(PRIOR,'author-notes.json'));
const doc=structuredClone(prior);

const deleted={
 c05le007:'木片作芯的來源歸屬及做法併入r052；刪重開手卷中心動作的提問，不在前後兩句各講一次兩根合卷。',
 c05le008:'定長切條、木片作芯及兩根手卷合入r052，成為一次連續製造動作；刪第二遍盤卷描述與想像句。',
 c05r053:'刪旁白中的查核邊界與第二次兩根合卷說明；機器是否同時擠出兩條未知，保留在claims及作者備註，不反向斷言只出一條。'
};
const replacement={
 id:'c05r052',
 text:'另一筆商品登錄記下：長條切成定長，兩根合在一起，以小木片作芯，用手盤成螺旋。',
 source_ids:['K_T','NM_MACHINE','NM_COIL'],
 locator:'K_T：押出的兩根合在一起手卷。NM_MACHINE 910191180004：麵條狀材料兩根手卷。NM_COIL 910191180006製法段：定長切條、木片作芯、兩根手卷；不用錯配年份及產能。',
 reason:'針對r2雙讀者共同no_recap，將r052、le007、le008及r053涉及的手卷雙根事實合成一次推進：切長→合兩根→以木片作芯→手盤螺旋。只稱登錄記下製法，不稱木芯現物留存；不說機器同時或每次只出幾條。',
 prompt:'Close-up of one anonymous worker curling two plain soft strands around a small wooden core on a plain work board, with cut ends visible, gentle workshop light.'
};
doc.scenes=doc.scenes.filter(s=>!s.lines.some(l=>Object.hasOwn(deleted,l.id)));
const mergedScene=doc.scenes.find(s=>s.lines.some(l=>l.id===replacement.id));
assert(mergedScene);
mergedScene.lines.find(l=>l.id===replacement.id).text=replacement.text;
mergedScene.data.prompt=replacement.prompt;
doc.loops=doc.loops.filter(x=>!Object.hasOwn(deleted,x.setup)&&!Object.hasOwn(deleted,x.payoff));
for(const loop of doc.loops)if(loop.setup==='c05r005')loop.what='預告的兩根長條，在單一製法段落完成切長、合卷與木片作芯手盤';
assert.deepEqual(validateVideo(doc),[]);
for(const key of Object.keys(prior).filter(k=>!['scenes','loops'].includes(k)))assert.deepEqual(doc[key],prior[key]);
assert.deepEqual(doc.voice,base.voice);assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.equal(doc.subtitles.burn_in,true);

const rows=[];let chapter='',chapterIndex=-1,total=0,hook=0,outro=0;
for(const {scene,line}of eachLine(doc)){
 if(scene.chapter){chapter=scene.chapter;chapterIndex++;}
 const units=spokenUnits(line.text);total+=units;
 if(chapterIndex===0)hook+=units;
 if(scene.template==='outro')outro+=units;
 rows.push({chapter,id:line.id,text:line.text});
}
const body=total-hook;
const rowMap=new Map(rows.map(r=>[r.id,r]));
for(const r of rows)if(r.id!==replacement.id)assert.deepEqual(r,priorMap.get(r.id));
const deletedRows=priorRows.filter(r=>!rowMap.has(r.id));
assert.deepEqual(new Set(deletedRows.map(r=>r.id)),new Set(Object.keys(deleted)));
const sourceMap=Object.fromEntries(read('/workspace/work/brand-story-20261025/c05-audit/readiness-review.json').sources_reopened.map(s=>[s.id,s]));
const CACHE='/workspace/work/brand-story-20261025/c05-audit/source-check';
const claims=rows.map(row=>{
 const old=priorClaims.get(row.id);assert(old);
 const modified=row.id===replacement.id;
 const ids=modified?replacement.source_ids:old.source_ids;
 return {...structuredClone(old),chapter:row.chapter,claim:row.text,status:'PENDING_INDEPENDENT_REVIEW',change:modified?'MERGED_IN_R3':'UNCHANGED_FROM_R2',
 source_ids:ids,sources:ids.filter(id=>sourceMap[id]).map(id=>({id,url:sourceMap[id].url,raw_cache:path.join(CACHE,id+'.html'),raw_sha256:sourceMap[id].raw_sha256,text_cache:path.join(CACHE,id+'.txt')})),
 locator:modified?replacement.locator:old.locator,new_information:modified?replacement.reason:old.new_information,
 r2_claim_sha256:sha(old.claim),r3_change_reason:modified?replacement.reason:null,
 ...(modified?{source_limits:['來源記下兩根合在一起手卷，未交代機器是否同時擠出兩條；也不能反向聲稱機器每次只擠出一條。','木片作芯是製法記錄，不是木芯現物留存的證明。','NM_COIL只用製法，不用錯配日期、產能或首創主張。']}:{} )};
});
const brief=[
'# C05 長度候選 r3｜單一 A','',
'狀態：未核准候選。r1、r2及其原審查收據保留於history；本次只修r2兩位讀者共同指出的手卷雙根重述。','',
'## 選項 A：把一條香做成能交付的工作','',
'沿同一條香，從乾花成粉、糊粉加水成塊、押出與雙條手卷，走到雙卷運送、機械打型、使用前分離，再解開香體密度與釋出位置。','',
'## 問題','',
'為什麼把香盤成螺旋，還不夠讓它久燃、完整地走上貨架？','',
'## 一句答案','',
'螺旋把長路徑收進平面；材料與製程把圓做出來，雙卷讓它較完整地送達，而香體密度與燃燒時的釋出，才接上它如何持續工作。','',
'## 站主觀點','',
'我覺得這件日用品有意思的，是形狀留下來，做出形狀的動作卻改變：木模沒有進產線，手卷把兩條合在一起，刀型又接過手盤工作。對一位觀眾把每次交接的原因說清楚，不把年代排成發明清單。','',
'## 本次精修','',
'在r052一次講清定長切條、合兩根、木片作芯及手盤螺旋；刪le007、le008、r053，下一景直接進金網乾燥，再問雙卷的運送理由。未改其餘旁白與場序。機器一次擠出幾條未明的來源界線只留claims，不在旁白反覆唸查核過程，也不反向斷言只出一條。','',
'## 長度與待查','',
`native總量${total} units；正文排除開場${body}，再排除有聲片尾${body-outro}。字數照實報告，不為回到r2的3279補弱句或停頓。實際TTS是否達12–14分鐘仍未量測，可能須依真實聲音調整；不作篇幅或時長PASS。`,'',
'維持原slug、STORY voice、look、burn_in=true、所有metadata。修改鏡頭為匿名英文概念插圖，靜態運鏡；實際畫面、占時、音色與字幕尚未驗證。新稿來源差分及兩位新讀者的判定仍待完成，作者不標PASS、verify或送審完成。base、canonical、譯文、history與舊reviews不動，未呼叫provider、付費、後台或git。',''
].join('\n');
fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const series=read(path.join(PRIOR,'series.json'));
Object.assign(series,{status:'length_extension_r3_candidate_unapproved',candidate_revision:'length-r3',parent_candidate_video_sha256:PRIOR_SHA,independent_source_review_required:true,two_isolated_narrative_readers_required:true});
writeJson('video.json',doc);writeJson('narration-only.json',rows);writeJson('series.json',series);
writeJson('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_REVIEW',candidate_revision:'length-r3',parent_source_video_sha256:EXPECTED,parent_candidate_video_sha256:PRIOR_SHA,rows:claims});
const script=['# '+doc.youtube.title,'','未核准長度候選r3；ID與來源只供審閱，不讀入旁白。r1、r2與原收據保留於history，新差分須另查。',''];
let last='';for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+last,'');}script.push('### '+r.id,'',r.text,'');}
fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 長度候選 r3 逐句主張','','全部PENDING_INDEPENDENT_REVIEW；r2審查結論只綁r2，未延伸為r3判定。','','| ID | r3狀態 | 旁白 | 來源索引 | 定位／變更 |','| --- | --- | --- | --- | --- |'];
for(const r of claims)cm.push('| '+r.id+' | '+r.change+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+(r.r3_change_reason?'；'+r.r3_change_reason:'')+' |');
cm.push('','## r3刪除差分','');for(const r of deletedRows)cm.push('- '+r.id+'（'+spokenUnits(r.text)+' units）：'+deleted[r.id]);
cm.push('','## 手卷段的來源界線','',
'r052合併K_T、NM_MACHINE與NM_COIL的既有製法資訊。先由機器押出長條，再由人合兩根並盤卷；資料沒有交代機器是否同時擠出兩條，不能聲稱機器同時出雙條，也不能反向聲稱每次只出一條。木片作芯僅是登錄記下的做法，不是木芯現物留存。NM_COIL只用定長切條、木片作芯、手卷與金網乾燥段；其西元括號與紀年換算衝突，不引用日期、產能或首創主張。','',
'乾花磨粉不是pollen。手卷加水成塊限於NM_MACHINE登錄；現代製程與溫度、釋出位置保留原廠歸屬及攝氏單位，不補殺蚊／安全效果或本集實驗。原件快取只留work。','');
for(const id of [...new Set(claims.flatMap(x=>x.source_ids))].filter(id=>sourceMap[id])){const s=sourceMap[id];cm.push('- '+id+'：'+s.url+'；raw SHA '+s.raw_sha256+'；快取 '+path.join(CACHE,id+'.html'));}
cm.push('');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));

const lint=lintVideo(doc,{brief,lexicon:read('/workspace/work/brand-remakes-source/docs/videos/lexicon.json'),series,translations:{}});
const index=new Map(rows.map((r,i)=>[r.id,i]));for(const loop of doc.loops)assert(index.get(loop.setup)<index.get(loop.payoff));
const payoffs=priorNotes.loop_audit.concrete_pairs_for_fresh_blind_review.filter(x=>index.has(x.setup)&&index.has(x.payoff)).map(x=>({...x,status:'AUTHOR_INTENT_PENDING_FRESH_BLIND_REVIEW'}));
assert(payoffs.length>=8);
const priorUnits=priorRows.reduce((n,r)=>n+spokenUnits(r.text),0);
const deletedUnits=deletedRows.reduce((n,r)=>n+spokenUnits(r.text),0);
const changeDelta=spokenUnits(replacement.text)-spokenUnits(priorMap.get(replacement.id).text);
assert.equal(total,priorUnits-deletedUnits+changeDelta);
const priorSceneMap=new Map(prior.scenes.map(s=>[s.id,s]));
const changedScenes=doc.scenes.filter(s=>JSON.stringify(s)!==JSON.stringify(priorSceneMap.get(s.id))).map(s=>s.id);
assert.deepEqual(changedScenes,[replacement.id]);
const originalRows=read(path.join(BASE,'narration-only.json'));
const originalMap=new Map(originalRows.map(r=>[r.id,r]));
const retainedOriginal=rows.filter(r=>originalMap.has(r.id));
const shotUnits=[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(x.line.text),0);
const reviewInputs={blind_a:path.join(PRIOR,'reviews/narrative-r2-a.raw.json'),blind_b:path.join(PRIOR,'reviews/narrative-r2-b.raw.json'),source:path.join(PRIOR,'reviews/source-r2-independent.json')};
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs'];
const notes={
 status:'UNAPPROVED_LENGTH_EXTENSION_CANDIDATE',candidate_revision:'length-r3',author:'/root/c03_review_pt_id',parent_source_video_sha256:EXPECTED,parent_candidate_video_sha256:PRIOR_SHA,history_directory:PRIOR,
 review_inputs:Object.fromEntries(Object.entries(reviewInputs).map(([k,p])=>[k,{path:p,sha256:fileSha(p)}])),
 response_to_required_feedback:[{id:'no_recap',reader_a_target:'c05le008',reader_b_target:'c05r053',action:'雙根手卷只在r052完整敘述一次，合入切長及木片作芯；刪le007、le008、r053。',author_claim:'已精修，是否解決由新pair判定。'}],
 author_self_check:{draft:'合併四句的獨立資訊，不添加新支線或填長句。',critique:'保留切長、雙根、木芯與手工盤卷；來源只記方法，機器每次出料條數仍未知；乾燥和運輸理由分別向前推進。',final:'僅r052旁白／prompt更改，三句刪除，其餘逐字保留；同步刪木芯重開問題的loop，保留開場兩根長條的既有回收。'},
 delta_from_r2:{added_lines:[],changed_lines:[{id:replacement.id,before:priorMap.get(replacement.id).text,after:replacement.text,old_spoken_units:spokenUnits(priorMap.get(replacement.id).text),new_spoken_units:spokenUnits(replacement.text),unit_delta:changeDelta,source_ids:replacement.source_ids,source_locator:replacement.locator,reason:replacement.reason}],deleted_lines:deletedRows.map(r=>({id:r.id,text:r.text,spoken_units:spokenUnits(r.text),reason:deleted[r.id]})),deleted_spoken_units:deletedUnits,changed_spoken_unit_delta:changeDelta,net_spoken_unit_delta:total-priorUnits,moved_scene_ids:[],changed_scene_object_ids:changedScenes,unchanged_scene_objects_exact:doc.scenes.length-changedScenes.length,metadata_changes:[],loops_removed:prior.loops.filter(l=>Object.hasOwn(deleted,l.setup)||Object.hasOwn(deleted,l.payoff)),loops_updated:doc.loops.filter(l=>l.setup==='c05r005')},
 delta_from_r6:{original_lines:originalRows.length,retained_original_ids:retainedOriginal.length,retained_original_texts_exact:retainedOriginal.filter(r=>r.text===originalMap.get(r.id).text).length,changed_original_ids:retainedOriginal.filter(r=>r.text!==originalMap.get(r.id).text).map(r=>r.id),deleted_original_ids:originalRows.filter(r=>!rowMap.has(r.id)).map(r=>r.id),r1_additions_retained:rows.filter(r=>!originalMap.has(r.id)).length},
 native_units:{counter:'tools/video/core/timeline.mjs spokenUnits + core/schema.mjs eachLine',r2_total:priorUnits,candidate_total:total,candidate_hook:hook,candidate_body_excluding_hook:body,candidate_body_excluding_hook_and_outro:body-outro,candidate_outro:outro,body_planning_range:[3300,3550],planning_range_met:body>=3300&&body<=3550,shortfall_to_3300:Math.max(0,3300-body),length_decision:'針對共同重述問題減字，不為回到3279或工作下限添加弱句、警語或停頓；不作篇幅或時長PASS。',actual_tts_seconds:null,target_tts_minutes:[12,14],actual_duration_verified:false,may_require_adjustment_after_actual_voice:true},
 planned_visuals:{scenes:doc.scenes.length,lines:rows.length,illustration_scenes:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,planned_illustration_unit_share:shotUnits/total,planning_basis:'spoken-unit share only; actual screen-time share unverified',look_exact:JSON.stringify(doc.look)===JSON.stringify(base.look),voice_exact:JSON.stringify(doc.voice)===JSON.stringify(base.voice),burn_in:true,changed_prompt_anonymous_english:true,all_shots_static_stills:doc.scenes.filter(s=>s.template==='shot').every(s=>s.data.visual==='still'),actual_generated_media_reviewed:false},
 loop_audit:{total_declared_loops:doc.loops.length,concrete_pairs_for_fresh_blind_review:payoffs,opening_previews:2,actual_30_to_45_second_cadence_verified:false},
 source_caveats:['只在手工盤卷處講一次兩根合在一起；押出設備同時／每次出幾條未知，不補成單條或雙條機構。','木芯是商品登錄記下的製法，不是留存現物。','NM_COIL不用錯配西元日期或產能；其餘來源限定沿r2保留。'],
 independent_source_delta_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_ISOLATED_READERS',native_verify_file_written:false,native_factchecked_marker_created:false,owner_approval:false,
 lint:{errors:lint.errors,warnings:lint.warnings,summary:lint.summary,scope:'local text/structure only; estimates are not actual TTS/media acceptance'},
 file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))])),
 protected_parent_history_and_review_files_unchanged:Object.fromEntries(protectedPaths.map(p=>{assert.equal(fileSha(p),protectedBefore[p]);return[p,true];})),paid_calls:0,backend_writes:0,git_commands:0,canonical_written:false
};
writeJson('author-notes.json',notes);
console.log(JSON.stringify({out:OUT,revision:'length-r3',lines:rows.length,scenes:doc.scenes.length,native_units:notes.native_units,lint_errors:lint.errors,lint_warnings:lint.warnings,file_sha256:notes.file_sha256},null,2));
