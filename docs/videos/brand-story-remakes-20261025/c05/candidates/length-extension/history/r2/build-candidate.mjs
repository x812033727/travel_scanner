import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {spokenUnits} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {eachLine, validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {lintVideo} from '/workspace/work/brand-remakes-source/tools/video/core/lint.mjs';

const OUT=path.dirname(fileURLToPath(import.meta.url));
const BASE='/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c05';
const CANON='/workspace/work/brand-story-20261025/submission-root/docs/videos/story-everyday-kincho-c05-remake-20261025';
const R1=path.join(OUT,'history/r1');
const EXPECTED='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a';
const R1_SHA='1bde566aa141080d3eafdfaf68a611034380a3f2f5bb47282f701cb53667a157';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const fileSha=p=>sha(fs.readFileSync(p));
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const writeJson=(name,x)=>fs.writeFileSync(path.join(OUT,name),JSON.stringify(x,null,2)+'\n');
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(x=>x.isDirectory()?walk(path.join(dir,x.name)):[path.join(dir,x.name)]);}
const protectedPaths=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(x=>x.isFile()).map(x=>path.join(BASE,x.name)),...walk(CANON),...walk(R1),...walk(path.join(OUT,'reviews'))];
const protectedBefore=Object.fromEntries(protectedPaths.map(p=>[p,fileSha(p)]));
assert.equal(fileSha(path.join(BASE,'video.json')),EXPECTED);
assert.equal(fileSha(path.join(CANON,'video.json')),EXPECTED);
assert.equal(fileSha(path.join(R1,'video.json')),R1_SHA);
const base=read(path.join(BASE,'video.json'));
const prior=read(path.join(R1,'video.json'));
const priorClaims=new Map(read(path.join(R1,'claims.json')).rows.map(r=>[r.id,r]));
const doc=structuredClone(prior);

const removed={
 c05rx006:'刪第二次「散粉靠什麼留住螺旋」提問；手卷入口的加水、糊粉及塊料已在le004–le005解答，不再重開同一問題。',
 c05rx008:'刪泛稱粉料成形的重述；現代原料後直接進唯一一次板材／打型工序。',
 c05le011:'刪第二次混和→板狀→刀型流程；將混和機、押出成板、打型、乾燥合入r092，只敘述一次。',
 c05le016:'刪斷灰支線的提問，結尾回到商品製造、運送與香體慢燃。',
 c05le017:'刪香皿摩擦支線，不以來源足夠當成保留理由。',
 c05le018:'刪灰累積與反覆斷開的支線機制。',
 c05le024:'刪線香立重力支線的提問。',
 c05le019:'刪線香立灰重力支線。',
 c05le020:'整場刪除上蓋金屬接觸支線；r1來源／配鏡V01所指物件與直接接觸缺口隨場景一併移除。',
 c05le021:'刪支撐與熱接觸的總結，避免把主線另轉到使用器皿。'
};
const changes={
 c05le007:{text:'另一筆商品登錄還記下以小木片作芯的做法。兩根合在一起之後，手又該先往哪裡繞？',reason:'精確採用S01建議，將製法記錄與留存木芯現物分開。',sources:['NM_COIL'],locator:'910191180006 特徵：木片の芯を中心に2本ずつ手作業で巻く；只用製法段，不用錯配日期。'},
 c05r090:{text:'原廠描述的現行產品，使用合成擬除蟲菊酯有效成分。你猜，換了成分，植物粉料是不是就可以一起退場？',reason:'隨現代材料段前移，明示現行產品範圍，將有效成分與植物材料是否同時更換的問題留給下一句；保留材料轉折的真問題。',sources:['K_F'],locator:'家庭用殺蟲劑略歷、なぜ緑色をしている：現行產品有效成分與植物粉／黏結材料。',prompt:'Medium shot of one anonymous technician comparing a small plain vial with separate bowls of plant powder and wood powder on a workbench, neutral factory light.'},
 c05r091:{text:'原料表裡仍有植物性粉末和木粉。換了有效成分，不等於把香體的植物材料也抽走。',reason:'回答r090有效成分與植物材料是否同時更換；刪提前重說黏結材料的部分，下一句再給取走成分後粉料的具體例子。',sources:['K_F'],locator:'なぜ緑色をしている：粕粉、木粉等植物性粉末；不是指所有現代香體或歷史初代配方。',prompt:'Close-up of one anonymous technician holding a bowl of plain plant powder beside a separate small mound of wood powder, soft factory window light.'},
 c05r092:{text:'原廠描述的工序，先用混和機揉合，再由押出機做成板狀，接著打出螺旋並乾燥。',reason:'把r1的r092與le011合成唯一一次完整製程，保留混和機／板狀／打型／乾燥動作與原廠歸屬。',sources:['K_F'],locator:'家庭用殺蟲劑略歷：混和機で練り、押出機にかけて板状、渦巻型に打抜き、乾燥。',prompt:'Medium shot of one anonymous technician inspecting a plain flat sheet emerging from a simple unmarked extrusion outlet beside a mixing vat, neutral overhead factory light.'},
 c05le010:{text:'科博館把現在的打型比作餅乾模。料片交到巴形的渦卷刃型下，這回還需要工人一圈圈盤嗎？',reason:'不再問已由板材製程回答的「為何是一片料」，改問盤卷工作是否仍由手完成；r093以工法交接回收。',sources:['NM_MACHINE'],locator:'910191180004 特徵：現在以クッキー形抜き類比，巴形渦巻刃型打抜；早期兩條手卷。'},
 c05r093:{text:'不用。你剛才看過的手盤動作，在這裡換成打型；圓留下來了，做出圓的動作卻變了。',reason:'前移至現代製程後，直接回答刀型取代手盤的問題，完成製造段後才把成品交到觀眾手上。',sources:['K_F','NM_MACHINE','EDITORIAL'],locator:'K_F 現行打型製程；NM_MACHINE兩條手卷與現行渦卷刃型對照；末句是旁白解讀。'},
 c05r080:{text:'這樣交到你手裡的雙卷，兩卷還相連著；使用前該從哪裡分開？',reason:'現代工序已在前文，刪第二次時間拉回的轉場，讓製造完成直接進入雙卷分離。',sources:['K_Q'],locator:'現行問答：兩卷相連，使用前拆成各自一卷。'},
 c05r089:{text:'原廠還列短時與長時尺寸，燃燒時數也會隨使用環境變動。',reason:'現代有效成分已移至製造段解答，刪原來再問花粉的逆向提問；保留各款與環境限定。',sources:['K_Q'],locator:'現行尺寸與時數問答：大型／一般／迷你；燃燒時間因使用環境而異。'},
 c05rx009:{text:'不過，燒得慢只說明時間。燃燒往前走時，有效成分怎麼離開香體，交到空氣裡？',reason:'不再從「把粉料黏成圓」開同一個問題，沿剛解答的慢燃直接問釋出位置。',sources:['K_F','EDITORIAL'],locator:'なぜ蚊取線香で蚊が死ぬ：燃燒釋出有效成分；首句為旁白對時數與釋出的區分。'},
 c05le013:{text:'原廠說，燃燒端約攝氏七百度到八百度；離前端六到八毫米的香體，約攝氏二百五十度，成分在那裡揮散。',reason:'落實r1來源A02的單位限定，明講攝氏與原廠歸屬；不改距離、兩處溫度或揮散位置。',sources:['K_F'],locator:'なぜ蚊取線香で蚊が死ぬ：燃燒部700–800℃；先端6–8mm部分約250℃揮散。'}
};
doc.scenes=doc.scenes.filter(s=>!s.lines.some(l=>Object.hasOwn(removed,l.id)));
for(const s of doc.scenes)for(const l of s.lines){const c=changes[l.id];if(c){l.text=c.text;if(c.prompt)s.data.prompt=c.prompt;}}
const moveIds=['c05r090','c05r091','c05rx005','c05rx007','c05le010','c05r092','c05le023','c05r093'];
const moved=moveIds.map(id=>{const s=doc.scenes.find(x=>x.id===id);assert(s);assert(!s.chapter);return s;});
doc.scenes=doc.scenes.filter(s=>!moveIds.includes(s.id));
doc.scenes.splice(doc.scenes.findIndex(s=>s.id==='c05r076')+1,0,...moved);
doc.loops=doc.loops.filter(x=>!Object.hasOwn(removed,x.setup)&&!Object.hasOwn(removed,x.payoff)&&!(x.setup==='c05r089'&&x.payoff==='c05r090'));
for(const loop of doc.loops)if(loop.setup==='c05le010')Object.assign(loop,{payoff:'c05r093',what:'刀型接手形狀，是否還要人逐圈盤卷'});
doc.loops.push({setup:'c05r090',payoff:'c05r091',what:'有效成分換代，植物粉料是否也一起退場'});
assert.deepEqual(validateVideo(doc),[]);
for(const k of Object.keys(prior).filter(k=>!['scenes','loops'].includes(k)))assert.deepEqual(doc[k],prior[k]);
assert.deepEqual(doc.voice,base.voice);assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.equal(doc.subtitles.burn_in,true);
const flat=[];let chapter='',chapterIndex=-1,total=0,hook=0,outro=0;
for(const {scene,line}of eachLine(doc)){if(scene.chapter){chapter=scene.chapter;chapterIndex++;}const u=spokenUnits(line.text);total+=u;if(chapterIndex===0)hook+=u;if(scene.template==='outro')outro+=u;flat.push({chapter,id:line.id,text:line.text});}
const body=total-hook;
const oldFlat=read(path.join(R1,'narration-only.json'));
const originalRows=read(path.join(BASE,'narration-only.json'));
const oldMap=new Map(oldFlat.map((r,i)=>[r.id,{...r,index:i}]));
const rowMap=new Map(flat.map((r,i)=>[r.id,{...r,index:i}]));
for(const r of flat)if(!changes[r.id])assert.equal(r.text,oldMap.get(r.id).text);
const deletedRows=oldFlat.filter(r=>!rowMap.has(r.id));
assert.deepEqual(new Set(deletedRows.map(r=>r.id)),new Set(Object.keys(removed)));
const sourceMap=Object.fromEntries(read('/workspace/work/brand-story-20261025/c05-audit/readiness-review.json').sources_reopened.map(s=>[s.id,s]));
const CACHE='/workspace/work/brand-story-20261025/c05-audit/source-check';
const claims=flat.map(row=>{const old=priorClaims.get(row.id),c=changes[row.id];assert(old);const ids=c?.sources||old.source_ids;return{...structuredClone(old),chapter:row.chapter,claim:row.text,status:'PENDING_INDEPENDENT_REVIEW',change:c?'MODIFIED_IN_R2':moveIds.includes(row.id)?'MOVED_IN_R2':'UNCHANGED_FROM_R1',source_ids:ids,sources:ids.filter(id=>sourceMap[id]).map(id=>({id,url:sourceMap[id].url,raw_cache:path.join(CACHE,id+'.html'),raw_sha256:sourceMap[id].raw_sha256,text_cache:path.join(CACHE,id+'.txt')})),locator:c?.locator||old.locator,new_information:c?c.reason:old.new_information,r1_claim_sha256:sha(old.claim),r2_change_reason:c?.reason||(moveIds.includes(row.id)?'移至機器／現代製造章，材料和打型一次講完，再把雙卷交給使用者。':null)};});
const brief=[
'# C05 長度候選 r2｜單一 A','','狀態：未核准候選。r1及其HOLD收據封存在history/r1；本次只修改current作者檔，不沿用r1的審查結論。','',
'## 選項 A：把一條香做成能交付的工作','','沿同一條香，從乾花成粉、糊粉加水成塊、押出與雙條手卷，走到雙卷運送、機械打型、使用前分離，再解開香體密度與釋出位置。灰、香皿和金屬上蓋支線整段刪除。','',
'## 問題','','為什麼把香盤成螺旋，還不夠讓它久燃、完整地走上貨架？','',
'## 一句答案','','螺旋把長路徑收進平面；材料與製程把圓做出來，雙卷讓它較完整地送達，而香體密度與燃燒時的釋出，才接上它如何持續工作。','',
'## 站主觀點','','我覺得這件日用品有意思的，是形狀留下來，做出形狀的動作卻改變：木模沒有進產線，後來的手卷把兩條合在一起，刀型又接過了手盤的工作。對一位觀眾把每次交接的原因說清楚，不能只把年代排成發明清單。','',
'## 本次修訂','','刪掉已回答的散粉提問及重複板材流程；把現代材料／打型集中在同一章，完成後才談雙卷分離、密度與氧氣。木芯只說登錄記下做法，不稱留存現物。保留公司回顧、館藏及現行產品範圍；不加專利核准、逐年試作、全廠換線或效力倍數。','',
'## 長度與待查','',`native總量${total} units；正文排除開場${body}，再排除有聲片尾${body-outro}。目標正文約3300–3550；刪除支線後的不足如實保留，不以重述、警語或慢播補足。這是文字量；實際TTS是否達到12–14分鐘仍未量測，可能須依真實聲音再調整，不作篇幅或時長PASS。`,'',
'維持原slug、STORY voice、look、burn_in=true、標題／縮圖／tags；來源說明欄維持r1。匿名英文概念插圖、靜態運鏡；實際畫面占比、生成畫面、音色與字幕尚未驗證。須由另一位來源讀者查差分及兩位全新隔離讀者評估；作者不標新稿PASS、verify或送審完成。未呼叫provider、付費、後台或git，未搬入canonical。',''].join('\n');
fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const series=read(path.join(R1,'series.json'));
Object.assign(series,{status:'length_extension_r2_candidate_unapproved',candidate_revision:'length-r2',parent_source_video_sha256:EXPECTED,parent_candidate_video_sha256:R1_SHA,independent_source_review_required:true,two_isolated_narrative_readers_required:true});
writeJson('video.json',doc);writeJson('narration-only.json',flat);writeJson('series.json',series);
writeJson('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_REVIEW',candidate_revision:'length-r2',parent_source_video_sha256:EXPECTED,parent_candidate_video_sha256:R1_SHA,rows:claims});
const script=['# '+doc.youtube.title,'','未核准長度候選r2；ID與來源只供審閱，不讀入旁白。r1舊稿與收據保留於history/r1，新差分須另查。',''];
let last='';for(const r of flat){if(r.chapter!==last){last=r.chapter;script.push('## '+last,'');}script.push('### '+r.id,'',r.text,'');}
fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 長度候選 r2 逐句主張','','全部PENDING_INDEPENDENT_REVIEW。r1 source／visual HOLD及兩讀者HOLD保留原貌；作者不把舊結論延伸到r2。','','| ID | r2狀態 | 旁白 | 來源索引 | 定位／變更 |','| --- | --- | --- | --- | --- |'];
for(const r of claims)cm.push('| '+r.id+' | '+r.change+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+(r.r2_change_reason?'；'+r.r2_change_reason:'')+' |');
cm.push('','## 刪除差分','');for(const r of deletedRows)cm.push('- '+r.id+'（'+spokenUnits(r.text)+' units）：'+removed[r.id]);
cm.push('','## 來源範圍','','花粉在這份中文敘事指乾花磨粉，不是pollen。NM_COIL只用定長切條、木片作芯、手卷與金網乾燥的製法段；其西元括號與紀年換算衝突，不引用它的日期、產能或首創主張。手卷加水成塊限於NM_MACHINE登錄；現代製程與溫度、釋出位置保留原廠歸屬及攝氏單位，不補殺蚊／安全效果或本集實驗。原件快取只留work。','');
for(const id of [...new Set(claims.flatMap(x=>x.source_ids))].filter(id=>sourceMap[id])){const s=sourceMap[id];cm.push('- '+id+'：'+s.url+'；raw SHA '+s.raw_sha256+'；快取 '+path.join(CACHE,id+'.html'));}cm.push('');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const lint=lintVideo(doc,{brief,lexicon:read('/workspace/work/brand-remakes-source/docs/videos/lexicon.json'),series,translations:{}});
const index=new Map(flat.map((r,i)=>[r.id,i]));for(const loop of doc.loops)assert(index.get(loop.setup)<index.get(loop.payoff),JSON.stringify(loop));
const payoffPairs=[['c05r003','c05r036'],['c05r005','c05r052'],['c05r025','c05r055'],['c05r043','c05r045'],['c05r067','c05r069'],['c05r080','c05r081'],['c05r084','c05r085'],['c05r090','c05r091'],['c05le001','c05le002'],['c05le004','c05le005'],['c05le007','c05le008'],['c05le010','c05r093'],['c05le012','c05le013']].map(([setup,payoff])=>{assert(index.get(setup)<index.get(payoff));return{setup,payoff,status:'AUTHOR_INTENT_PENDING_FRESH_BLIND_REVIEW'};});
const priorUnits=oldFlat.reduce((n,r)=>n+spokenUnits(r.text),0);
const deletedUnits=deletedRows.reduce((n,r)=>n+spokenUnits(r.text),0);
const changedRows=Object.entries(changes).map(([id,c])=>({id,before:oldMap.get(id).text,after:rowMap.get(id).text,old_spoken_units:spokenUnits(oldMap.get(id).text),new_spoken_units:spokenUnits(rowMap.get(id).text),unit_delta:spokenUnits(rowMap.get(id).text)-spokenUnits(oldMap.get(id).text),reason:c.reason,source_ids:c.sources,source_locator:c.locator}));
const changedUnits=changedRows.reduce((n,r)=>n+r.unit_delta,0);assert.equal(total,priorUnits-deletedUnits+changedUnits);
const baseById=new Map(originalRows.map(r=>[r.id,r]));
const retainedBase=flat.filter(r=>baseById.has(r.id));
const exactBase=retainedBase.filter(r=>r.text===baseById.get(r.id).text);
const sceneMap=new Map(prior.scenes.map(s=>[s.id,s]));
const changedScenes=doc.scenes.filter(s=>JSON.stringify(s)!==JSON.stringify(sceneMap.get(s.id))).map(s=>s.id);
const shotUnits=[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(x.line.text),0);
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs'];
const notes={status:'UNAPPROVED_LENGTH_EXTENSION_CANDIDATE',candidate_revision:'length-r2',author:'/root/c03_review_pt_id',parent_source_video_sha256:EXPECTED,parent_candidate_video_sha256:R1_SHA,history_directory:R1,
 review_inputs:{blind_a:'/workspace/work/brand-story-20261025/c05-audit/length-extension-r1/blind-a.raw.json',blind_b:'/workspace/work/brand-story-20261025/c05-audit/length-extension-r1/blind-b.raw.json',source:path.join(R1,'reviews/source-r1-independent.json')},
 response_to_required_feedback:[{id:'no_recap',action:'刪rx006、rx008、le011；現代材料與打型前移至第五章，一次完成製程。',author_claim:'已改稿，是否解決留給兩位全新隔離讀者。'},{id:'no_detour',action:'整刪le016–le021及le024，包含灰、香皿摩擦、重力與金屬上蓋。',author_claim:'支線已移除，是否保持單線留給兩位全新隔離讀者。'},{id:'S01',action:'le007精確採用來源審查replacement；只說商品登錄記下木片作芯的做法。',author_claim:'待另一位來源讀者核差分。'},{id:'V01',action:'le020整場刪除，旁白與不完整接觸配鏡皆不在r2。',author_claim:'刪除差分待來源／書面配鏡重查。'}],
 delta_from_r1:{added_lines:[],changed_lines:changedRows,deleted_lines:deletedRows.map(r=>({id:r.id,text:r.text,spoken_units:spokenUnits(r.text),reason:removed[r.id]})),deleted_spoken_units:deletedUnits,changed_spoken_unit_delta:changedUnits,net_spoken_unit_delta:total-priorUnits,moved_scene_ids:moveIds,move_after_scene:'c05r076',move_reason:'現代原料及打型一次說完，再由出貨雙卷接到使用前分離。',changed_scene_object_ids:changedScenes,unchanged_scene_objects_exact:doc.scenes.filter(s=>!changedScenes.includes(s.id)).length,metadata_changes:[]},
 delta_from_r6:{original_lines:originalRows.length,retained_original_ids:retainedBase.length,retained_original_texts_exact:exactBase.length,changed_original_ids:retainedBase.filter(r=>r.text!==baseById.get(r.id).text).map(r=>r.id),deleted_original_ids:originalRows.filter(r=>!rowMap.has(r.id)).map(r=>r.id),r1_additions_retained:flat.filter(r=>!baseById.has(r.id)).length},
 native_units:{counter:'tools/video/core/timeline.mjs spokenUnits + core/schema.mjs eachLine',r1_total:priorUnits,candidate_total:total,candidate_hook:hook,candidate_body_excluding_hook:body,candidate_body_excluding_hook_and_outro:body-outro,candidate_outro:outro,body_target:[3300,3550],body_target_met:body>=3300&&body<=3550,shortfall_to_3300:Math.max(0,3300-body),length_decision:'刪支線與重述後如實報較低正文，不為目標灌入來源警語、清單或同義重講；可作約3500規劃的未核准候選，不作篇幅或時長PASS。',actual_tts_seconds:null,target_tts_minutes:[12,14],actual_duration_verified:false,may_require_adjustment_after_actual_voice:true},
 planned_visuals:{scenes:doc.scenes.length,lines:flat.length,illustration_scenes:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,planned_illustration_unit_share:shotUnits/total,planning_basis:'spoken-unit share only; actual screen-time share unverified',look_exact:JSON.stringify(doc.look)===JSON.stringify(base.look),voice_exact:JSON.stringify(doc.voice)===JSON.stringify(base.voice),burn_in:true,all_changed_prompts_anonymous_english:true,all_shots_static_stills:doc.scenes.filter(s=>s.template==='shot').every(s=>s.data.visual==='still'),actual_generated_media_reviewed:false},
 loop_audit:{total_declared_loops:doc.loops.length,concrete_pairs_for_fresh_blind_review:payoffPairs,opening_previews:2,actual_30_to_45_second_cadence_verified:false},
 source_caveats:['NM_COIL只用製法，不用錯配西元日期或產能。','木片作芯是記錄的製法，非本集核實的留存木芯現物。','乾花磨粉不等於pollen；植物成分與現代配方各保留原廠歸屬。','溫度與釋出位置是原廠說明，明說攝氏；不是本集實測、殺蚊能力倍數或安全保證。'],
 independent_source_delta_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_ISOLATED_READERS',native_verify_file_written:false,native_factchecked_marker_created:false,owner_approval:false,
 lint:{errors:lint.errors,warnings:lint.warnings,summary:lint.summary,scope:'local text/structure only; estimates are not actual TTS/media acceptance'},
 file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))])),protected_parent_history_and_review_files_unchanged:Object.fromEntries(protectedPaths.map(p=>{assert.equal(fileSha(p),protectedBefore[p]);return[p,true];})),paid_calls:0,backend_writes:0,git_commands:0,canonical_written:false};
writeJson('author-notes.json',notes);
console.log(JSON.stringify({out:OUT,revision:'length-r2',lines:flat.length,scenes:doc.scenes.length,native_units:notes.native_units,lint_errors:lint.errors,lint_warnings:lint.warnings,file_sha256:notes.file_sha256},null,2));
