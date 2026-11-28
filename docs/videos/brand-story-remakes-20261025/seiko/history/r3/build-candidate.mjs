import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spokenUnits} from '../../../../tools/video/core/timeline.mjs';
import {validateVideo} from '../../../../tools/video/core/schema.mjs';
import {resolveLook,keyframeKey} from '../../../../tools/video/core/drama.mjs';
import {shotPrompt} from '../../../../tools/video/media/keyframes.mjs';
import {Stage,imageSelectionVersion} from '../../../../tools/video/media/stages.mjs';
const OUT=path.dirname(fileURLToPath(import.meta.url)),REPO=path.resolve(OUT,'../../../..');
const SLUG='story-adapt-seiko-quartz-astron-remake-20261025',RUNTIME='/workspace/work/brand-story-20261025/seiko-submission-root',MEDIA='/workspace/work/brand-story-20261025/media';
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=p=>sha(fs.readFileSync(p)),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const PROTECTED={'research-original.md':'a41609ac4465275a629db67fd3ffa225907753d7f7681d50cd2dd4741d4eaacc','research-original.claims.json':'4195ab5af88173c59ca4a3eff3b40386764a70c0e65420bec4446ac943095231','original-preservation.json':'de1800877f4406ac0ef01c9c3558ebb2965779bb7b3f1c63d29fd82bcba909bc'};
for(const[f,h]of Object.entries(PROTECTED))assert.equal(fileSha(path.join(OUT,f)),h,f);
const historyPath=path.join(OUT,'history/r1/preservation-receipt.json');assert.equal(fileSha(historyPath),'43b7a79545760899a37f1f01d40046949315a61f0c345389ff90024e06fa42de');const r1history=read(historyPath);for(const f of r1history.files)assert.equal(fileSha(path.resolve(REPO,f.snapshot)),f.sha256);for(const f of r1history.source_cache_protection)assert.equal(fileSha(f.path),f.sha256);
const historyR2Path=path.join(OUT,'history/r2/preservation-receipt.json');assert.equal(fileSha(historyR2Path),'a70673164e7ad6aefc1555d217590d37463d838fe037a13b6c6e0f18e5de3911');const r2history=read(historyR2Path);for(const f of r2history.files)assert.equal(fileSha(path.resolve(REPO,f.snapshot)),f.sha256);for(const f of r2history.source_cache_protection)assert.equal(fileSha(f.path),f.sha256);
const research=read(path.join(OUT,'research-original.claims.json')),pres=read(path.join(OUT,'original-preservation.json')),added=read(path.join(OUT,'author-source-additions.json'));
const oldChecks=pres.related_files.map(f=>{const original=path.join(REPO,f.path);assert.equal(fileSha(original),f.working_tree_sha256);assert.equal(fileSha(f.readonly_snapshot_path),f.working_tree_sha256);return{path:f.path,sha256:f.working_tree_sha256,snapshot:f.readonly_snapshot_path,unchanged:true};});
const registry=Object.fromEntries(research.claims.filter(c=>c.evidence_class!=='unsupported').map(c=>[c.id,c]));
for(const a of added.anchors)registry[a.id]=a;
for(const a of Object.values(registry)){assert.equal(fileSha(a.raw_path),a.raw_sha256);assert.equal(fileSha(a.text_path),a.text_sha256);assert(fs.readFileSync(a.text_path,'utf8').includes(a.short_quote));assert.equal(sha(a.short_quote),a.quote_sha256);}
const rows=read(path.join(OUT,'author-rows.json'));assert.equal(new Set(rows.map(r=>r.id)).size,rows.length);assert(rows.every(r=>spokenUnits(r.text)<=40));assert(rows.every(r=>r.research_claim_ids.every(id=>registry[id])));
const whole=rows.reduce((n,r)=>n+spokenUnits(r.text),0);assert(whole>=3350&&whole<=3650,'Planning length changed: '+whole);
const voicePath=path.join(REPO,'docs/videos/brand-story-remakes-20261025/c06/video.json'),voice=structuredClone(read(voicePath).voice);
const motifs={
goldwatch:['a small shop counter','an anonymous adult holding a plain gold-colored wristwatch with an unmarked dial'],
solder:['an electronics workbench','an anonymous assembler using a fine soldering iron beside a ceramic circuit board'],
boardfit:['a watch workshop','an anonymous technician examining a small ceramic circuit board beside gears and a battery'],
viewerwatch:['a plain room near a window','an anonymous adult examining a plain wristwatch in one hand'],
crystal:['a component bench','an anonymous technician holding a small sealed crystal element with fine tweezers'],
fork:['a crystal workshop','an anonymous technician examining a small two-pronged crystal element under a magnifier'],
divide:['an electronics bench','an anonymous technician studying a simple chain of abstract connected shapes on a wordless diagram'],
suspend:['a component workbench','an anonymous technician holding a small sealed capsule beside a simplified spring suspension model'],
parts:['an assembly bench','an anonymous assembler examining a tray of tiny electronic parts beside a ceramic board'],
motor:['a watch workbench','an anonymous technician holding a small magnetic rotor above a simple mechanical fixture'],
coil:['a winding workbench','an anonymous technician holding a small fine-wire coil above a shallow component tray'],
magnets:['a laboratory table','an anonymous experimenter arranging three small magnet pieces around a simple circular guide'],
distributed:['a watch workbench','an anonymous technician placing a coil beside separated rotor and stator pieces inside a plain movement frame'],
watchface:['a small shop counter','an anonymous adult examining a plain wristwatch face with simple unmarked hands'],
battery:['a repair workbench','an anonymous repairer holding a small battery beside an opened plain battery cover'],
packing:['a workshop dispatch table','an anonymous worker closing a small unmarked parcel beside plain watch boxes'],
adjust:['a watch adjustment bench','an anonymous technician using fine tweezers beside a plain watch movement'],
pricepaper:['a shop preparation counter','an anonymous worker holding a small unmarked price card beside a plain gold-colored wristwatch'],
carpaper:['an archive reading desk','an anonymous reader examining an unmarked folded brochure beside a generic small car silhouette model'],
printing:['a print preparation table','an anonymous worker sorting unmarked paper sheets beside a small stack of price cards'],
counter:['a shop counter','an anonymous clerk placing a plain gold-colored wristwatch beside a small unmarked display stand'],
returned:['a service workbench','an anonymous repairer examining a plain wristwatch beside several closed unmarked service boxes'],
crystaltest:['a component testing bench','an anonymous technician examining a sealed crystal element beside a simple meter with a featureless face'],
grind:['a crystal shaping workbench','an anonymous technician examining a small two-pronged crystal piece beside a grinding tool'],
inspect:['a component inspection bench','an anonymous inspector looking through a magnifier at a small crystal piece'],
tuning:['a crystal adjustment table','an anonymous technician holding a fine tool beside a small crystal element'],
aging:['a component testing shelf','an anonymous technician checking a row of small sealed crystal units linked to a simple test fixture'],
sorting:['a component sorting table','an anonymous worker placing one sealed crystal unit into a shallow plain tray'],
oven:['a factory heating station','an anonymous worker standing beside a closed vacuum furnace with unmarked controls'],
ovencheck:['a factory heating station','an anonymous supervisor examining an unmarked control knob beside a closed vacuum furnace and a closed plain folder'],
record:['a factory recording desk','an anonymous supervisor examining a plain unmarked notebook beside a small control fixture'],
procedure:['a factory worktable','an anonymous supervisor placing an unmarked instruction sheet beside a simple work fixture'],
chip:['a laboratory bench','an anonymous engineer holding a tiny semiconductor chip with fine tweezers'],
lab:['an electronics laboratory','an anonymous engineer examining a small circuit test fixture on a clear table'],
delivery:['an electronics receiving bench','an anonymous worker opening an unmarked component parcel beside a shallow chip tray'],
sortingchip:['a component testing table','an anonymous technician moving a tiny chip between two plain shallow trays'],
classroom:['a training classroom','an anonymous trainee studying an abstract wordless circuit diagram beside a notebook'],
presentboard:['a research office table','an anonymous engineer presenting a bulky handmade circuit board beside a plain wristwatch'],
largeboard:['a laboratory table','an anonymous engineer examining a bulky handmade circuit board beside a small empty watch case'],
cleanroom:['an electronics cleanroom','an anonymous worker wearing a plain clean suit while examining a small wafer holder'],
equipment:['a laboratory equipment room','an anonymous engineer inspecting a closed processing cabinet with unmarked controls'],
chiptest:['a laboratory testing bench','an anonymous engineer checking a tiny chip connected to a simple featureless test fixture'],
boardchip:['an electronics bench','an anonymous engineer holding a tiny chip beside a ceramic board with several separate component groups'],
assembly:['a watch assembly table','an anonymous assembler examining a plain movement beside a tray of small circuit components'],
laterwatch:['a watch design table','an anonymous designer examining a plain thinner watch frame beside a small battery'],
batterychoice:['a watch design bench','an anonymous engineer comparing two plain batteries beside an unmarked watch frame'],
repairbench:['a neighborhood watch repair counter','an anonymous repairer using fine tweezers beside a plain watch circuit module'],
paper:['a quiet reading desk','an anonymous reader examining an open unmarked technical journal beside a plain watch movement'],
module:['a watch repair bench','an anonymous technician holding a small plain circuit module above a shallow parts tray'],
connector:['a precision assembly bench','an anonymous technician examining a bent metal contact beside a small circuit module'],
replacepart:['a watch repair workbench','an anonymous repairer lifting a small circuit component with fine tweezers'],
assemblymachine:['a production workshop','an anonymous worker inspecting a simple circular circuit assembly fixture with unmarked controls'],
moduletray:['an assembly workshop table','an anonymous worker examining a shallow tray of small plain circuit modules'],
inspectionbench:['a watch inspection bench','an anonymous inspector examining a plain watch beside a featureless timing fixture'],
componenttest:['a component testing workbench','an anonymous technician placing a tiny electronic component into a simple test socket'],
temperaturetest:['an electronics testing room','an anonymous technician examining a plain watch beside a closed test chamber with unmarked controls']
};
const framings=['Medium shot','Close-up','Wide shot','Medium close-up'],lights=['soft light from a side window','mild overhead light','muted diffuse light','soft interior lamp light','gentle light from the left'],cameras=['push in','pan left','pull out','pan right'];
rows.forEach((r,i)=>{const m=motifs[r.visual];assert(m,r.visual);r.prompt=framings[i%4]+' at '+m[0]+', '+m[1]+', '+lights[Math.floor(i/4)%5]+'.';r.camera=cameras[i%4];});
const promptOverrides={
skr1e21a:'Medium shot at a small rotor fixture, an anonymous technician watching a stationary magnetic wheel beside a simple contact lever, mild desk light.',
skr1e28a:'Close-up in a plain room, an anonymous owner turning an unmarked wristwatch over to inspect the back cover, gentle indoor light.',
skr1p06:'Medium close-up at a dispatch table, an anonymous worker placing a finished plain wristwatch inside a small open box, mild overhead light.',
skr1r06:'Medium shot at a crystal shaping station, an anonymous worker holding a two-pronged crystal blank beside a small grinding wheel, soft side light.',
skr1r18:'Wide shot at a training table, an anonymous trainee studying a wordless component flow diagram beside sealed crystal units, diffuse light.',
skr1c10:'Medium close-up at a watch workshop desk, an anonymous technician opening an unmarked training notebook beside a disassembled plain movement, soft overhead light.',
skr1c11c:'Wide shot in a research office, an anonymous engineer studying a small empty watch case on an otherwise clear table, gentle side light.',
skr1d03:'Medium shot at a repair counter, an anonymous repairer looking at a few tiny separate components laid out beside a plain movement, diffuse light.',

skr1e10:'Close-up in a component lab, an anonymous engineer pointing at a simple spring suspension model beside a sealed capsule, soft overhead light.',
skr1e12:'Wide shot at an electronics demonstration desk, an anonymous technician arranging paired abstract blocks into a simple signal chain, gentle indoor light.',
skr1e14:'Medium close-up at an assembly table, an anonymous assembler positioning tiny electronic components onto a ceramic board with tweezers, soft side light.',
skr1e20:'Medium shot in a laboratory, an anonymous experimenter touching a simple contact beside a magnetic rotor fixture, mild ceiling light.',
skr1e22:'Close-up at a watch bench, an anonymous technician pointing toward two small magnetic pieces resting in a plain movement frame, diffuse light.',
skr1e28b:'Medium close-up at a repair table, an anonymous repairer lifting a plain battery cover from an unmarked watch case, mild desk lamp light.',
skr1p03:'Wide shot at a workshop doorway, an anonymous dispatch worker carrying a small unmarked parcel toward an open door, soft interior light.',
skr1p08:'Close-up at a shop preparation table, an anonymous worker replacing a small unmarked label on a plain display stand, mild lamp light.',
skr1p09:'Medium shot at a planning desk, an anonymous shop worker considering a plain gold-colored watch beside a generic compact car model, soft overhead light.',
skr1p11:'Medium close-up in an archive room, an anonymous reader holding an open unmarked vehicle price brochure, gentle side light.',
skr1p12:'Wide shot at an archive table, an anonymous reader placing a larger generic car model beside an unmarked folded brochure, soft indoor light.',
skr1p16:'Medium shot in a preparation room, an anonymous worker carrying a stack of unmarked paper sheets beside display stands, diffuse light.',
skr1p17:'Medium close-up in a preparation office, an anonymous coordinator looking toward a plain wall clock while holding unmarked sheets, mild overhead light.',
skr1r08:'Medium shot at an inspection table, an anonymous worker turning a small sealed capsule under a simple lens, gentle side light.',
skr1r12:'Wide shot at a component test bench, an anonymous technician separating two small sealed units into different plain trays, soft overhead light.',
skr1r15:'Close-up at a testing shelf, an anonymous technician connecting one sealed crystal unit to a simple electrical fixture, mild indoor light.',
skr1f04:'Medium close-up beside a closed furnace, an anonymous supervisor studying an unmarked folder while facing the controls, soft ceiling light.',
skr1c01:'Medium shot at an electronics research bench, an anonymous engineer holding a small experimental circuit beside a plain test fixture, diffuse light.',
skr1c07:'Close-up at a receiving bench, an anonymous technician opening a plain packet of small chips beside an unmarked test socket, mild lamp light.',
skr1c11a:'Wide shot in a training room, an anonymous instructor pointing at an abstract wordless circuit diagram, soft overhead light.',
skr1c22:'Medium close-up at a repair desk, an anonymous engineer tilting a plain watch movement to inspect its separate circuit areas, gentle side light.',
skr1c23:'Close-up at an electronics desk, an anonymous engineer placing a tiny chip beside a cluster of separate components on a simple circuit board, mild indoor light.',
skr1c26b:'Medium shot at a design bench, an anonymous technician placing a plain battery inside an unmarked later watch frame, soft overhead light.',
skr1d08:'Wide shot in a production planning room, an anonymous planner holding one small circuit module beside a simple circular assembly table, diffuse light.'
};
for(const r of rows)if(promptOverrides[r.id])r.prompt=promptOverrides[r.id];
const pairDefs=[['skr1h05','skr1p14','price-card-before-relabel'],['skr1h06','skr1f08','furnace-setting-inspection']];
for(const[a,b]of pairDefs){const setup=rows.find(r=>r.id===a),payoff=rows.find(r=>r.id===b);if(b==='skr1f08'){const m=motifs.ovencheck;payoff.prompt='Medium shot at '+m[0]+', '+m[1]+', mild overhead light.';payoff.camera='pan right';}setup.prompt=payoff.prompt;setup.camera=payoff.camera;}
const loopsData=[
['h04','d09','手工工作台後的製造方法發展到後期回路組裝機'],
['h05','p14','服部要求改回標價引發重貼價牌與印刷準備'],
['h06','f08','現場查出爐溫低設且原設定沒有留資料'],
['h08','d18','穩定製造和可維修接法一起接住使用者'],
['e04','e06','縮小振子牽動頻率分頻級數與耗電'],
['e10','e11','振子節拍需分頻後才能給出秒驅動訊號'],
['e13','e14','最初用手工零件構成hybrid回路'],
['e18','e20','以短暫通電和步進動作降低馬達耗電'],
['e21a','e22','停電時磁吸作用留住轉子位置'],
['e24','e25','功能件分散配置利用機芯空隙'],
['e28a','e28b','電池蓋使交換較容易'],
['e29','p03','企業史的12月24日已送十支'],
['p07','p08','臨時價格不同而不是價牌已準備好'],
['p10','p11','汽車比較需限定1966東京Standard'],
['p15','p16','變動落到重貼價牌與重排印刷物'],
['p21','r03','售出的腕錶仍可能回來再調整'],
['r04','r11','通電後裂紋狀態與頻率可能改變'],
['r08','r09','蝕去表面也不能目視判定剩餘裂紋'],
['r14','r15','數日通電老化讓變動先出現'],
['r19','f01','回頭檢視去除氣體的真空烘烤製程'],
['f03','f05','實際加熱設定比應有值低五十度'],
['f07','f08','設定沒有被作為數據記錄'],
['f13','c02','手焊hybrid的生產性與耗電仍有瓶頸'],
['c03','c04','電路設計之外尚需建立製造能力'],
['c10','c11a','學者授課與研究單位訓練'],
['c07','c08','供應晶片仍需篩選品質性能'],
['c11c','c12','山村以試作品向研究者說明困難'],
['c17','c18','設備到了並不帶來已成熟的製造經驗'],
['c22','c23','外購Intersil在35SQ只替換分頻，其餘回路仍hybrid'],
['c26a','c26c','省下耗電可用在續航或更小電池的設計取捨'],
['c27','d02','1977設計要求讓零售商可用簡單治具修理'],
['d03','d04','後期回路裝配預先考慮售後維護'],
['d08','d09','後期回路用rotary自動裝配'],
['d12','d13','品質保證先要求各電子部件可靠性']
];
const loops=loopsData.map(([a,b,what])=>({setup:'skr1'+a,payoff:'skr1'+b,what}));
for(const l of loops){assert(rows.find(r=>r.id===l.setup));assert(rows.find(r=>r.id===l.payoff));assert(rows.findIndex(r=>r.id===l.setup)<rows.findIndex(r=>r.id===l.payoff));}
const title='Seiko45萬的錶，為何還得回廠調整？｜品牌故事';
const usedIds=[...new Set(rows.flatMap(r=>r.research_claim_ids).map(id=>registry[id].source_id))];
const sources=research.sources.filter(s=>usedIds.includes(s.id));assert(sources.every(s=>s.http_status===200));
const description='一支新石英錶能走得準，為什麼仍可能回廠調整？從1960年代末顯微鏡下的手焊基板，沿著振子與馬達的小型化、1969年出貨改價、老化與爐溫現場檢查，走到後期分頻晶片，以及1977技術文裡的可維修接法。\n\n上市與製程事件依精工／Epson回顧、2004企業史摘錄、2017青木茂技術史及1977安川英昭論文，各守時期與歸屬。沒有把多件回廠錶拼成一支可追蹤序號案例；兩成是振子初期良率，一成是特定階段IC挑選比例，並非退貨率。精度保留常溫條件；汽車價只比較1966東京卡羅拉Standard。初代hybrid、35SQ外購Intersil分頻晶片、自研A型與1971年12月38系，以及1977實裝，各守機種與時期。舊題瑞士產業單因果與全球免費專利說法不採。圖為匿名概念插畫。\n\n原件來源（查閱2026-10-26）\n'+sources.map(s=>(s.title||s.id)+'\n'+s.final_url).join('\n');
const outroIds=new Set(['skr1d18','skr1d19','skr1d20']);const scenes=[];let current='';
for(const r of rows){if(outroIds.has(r.id))continue;const s={id:r.id,template:'shot',data:{prompt:r.prompt,visual:'still',camera:r.camera},lines:[{id:r.id,text:r.text,emotion:'對一位觀眾自然說書，條件和來源歸屬清楚，問句帶好奇，句間不拖'}]};if(current!==r.chapter){current=r.chapter;s.chapter=current;}scenes.push(s);}
scenes.push({id:'skr1outro',template:'outro',data:{title:'準確，還得交到下一雙手',cta:'你最想少操心的是什麼？'},lines:rows.slice(-3).map(r=>({id:r.id,text:r.text,emotion:'溫暖收束，對一位觀眾自然邀請'}))});
const doc={schema_version:1,slug:SLUG,format:'drama',category:'story',narration_locale:'zh-TW',target_minutes:[12,14],voice,subtitles:{burn_in:true},look:{preset:'cute-mystery'},characters:[],music:{prompt:'light, curious, a little mysterious, no vocals',gain_db:-20,duck_db:-10},loops,youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',title,description,tags:['Seiko','精工','Astron','石英錶','腕錶','品牌故事','製造','維修'],video_id:null},thumbnail:{template:'thumb',data:{layout:'d',brand:'SEIKO',tag:'品牌故事',headline:'賣出又回廠',sub:'45萬日圓的考驗',shot:'skr1h01'}},sources:sources.map(s=>({title:s.title||s.id,url:s.final_url,checked_on:'2026-10-26'})),assets:[],scenes};
const validation=validateVideo(doc);assert.equal(validation.errors?.length??0,0,JSON.stringify(validation.errors));write('video.json',doc);write('narration-only.json',rows.map(({id,chapter,text})=>({id,chapter,text})));
const sm=['# '+title,'','Seiko R3 作者稿。ID/章名不讀入旁白；'+whole+' native spokenUnits，目標13分鐘仍待實聲。SOURCE、書面配鏡、fresh native、owner、paid admission均待獨立真關卡。',''];current='';for(const r of rows){if(current!==r.chapter){current=r.chapter;sm.push('## '+current,'');}sm.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),sm.join('\n'));
const classMap={fact:'來源支持事實',attributed:'有歸屬敘述',hypothetical:'明示觀眾假設/條件',editorial_link:'編輯連接',question:'旁白疑問',reaction_question:'旁白反應與疑問',reaction:'旁白反應/結尾答案',cta:'對觀眾邀請'};
const claimRows=rows.map(r=>({id:r.id,scene_id:outroIds.has(r.id)?'skr1outro':r.id,claim:r.text,claim_class:classMap[r.kind],kind:r.kind,research_claim_ids:r.research_claim_ids,source_ids:[...new Set(r.research_claim_ids.map(id=>registry[id].source_id))],source_evidence:r.research_claim_ids.map(id=>({id,...registry[id]})),limits:[...new Set(r.research_claim_ids.map(id=>registry[id].limits))],visual_prompt:outroIds.has(r.id)?'Native outro typography only.':r.prompt,visual_scope:'Anonymous concept only. Not a source photograph, exact branded model, named likeness, readable original price card, actual serial-number watch or guaranteed factory workflow.',independent_source_review:'PENDING_OTHER_REVIEWER',independent_visual_review:'PENDING_OTHER_REVIEWER'}));
for(const[a,b,asset]of pairDefs)for(const id of[a,b])claimRows.find(r=>r.id===id).planned_same_image={asset_plan_id:asset,payoff_scene_id:b,teaser_scene_id:a,actual_file_sha256:null,actual_same_asset_verified:false};
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_QA',candidate_revision:'seiko-r3',author:'/root/c10_eight_text',video_slug:SLUG,frozen_research_sha256:PROTECTED,author_additions_sha256:fileSha(path.join(OUT,'author-source-additions.json')),source_registry:Object.fromEntries(sources.map(s=>[s.id,s])),rows:claimRows,source_pass_claimed:false,approvals_created:0});
const cm=['# Seiko R3 逐句來源與配鏡綁定','','作者的來源對位，不是獨立SOURCE PASS。研究57候選與新增A01–A10均保留原件SHA與定位；段落歸屬不抹平。','','| ID | 旁白 | 分類 | 原件錨點 |','| --- | --- | --- | --- |'];for(const r of claimRows)cm.push('| '+r.id+' | '+r.claim+' | '+r.claim_class+' | '+r.research_claim_ids.join('、')+' |');cm.push('','## 邊界','','S7是Epson2004企業史摘錄，不是同期逐日工單；S24是2017青木回顧，其1972才入社。S20是安川1977量產技術論文，後期48高階款/回路組裝機不得畫成1969首批。PDF1000頁雙欄pdftotext交錯已用實際像素核讀，短引只作定位；A04組裝機圖12與次頁能力十萬units/month合讀。35SQ的外購Intersil CMOS只換分頻，其餘仍hybrid；1971年4月自研A型含分頻及馬達驅動訊號輸出，接到同年12月38系。兩條線已在旁白分開，沒有給35SQ替換另編精確日期。低設50℃非爐溫50℃，20%振子與10%IC非退貨。沒有同一序號錶從上市到爐溫或後期晶片的追蹤案例。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const series={kind:'story',slug:'brand-story-remakes-20261025',episode:1,chapter:1,title,logline:'從1960年代末的手焊工作台、1969出貨改價、振子穩定與現場記錄，接到後期晶片與可維修回路。',original_backend_slug:'story-adapt-seiko-quartz-astron',original_backend_series_slug:'brand-stories-adapt',names:['Seiko','Astron','CMOS','Intersil','Toyota','Corolla','精工','阿斯特隆','諏訪精工舍','安川英昭','山村','垂井','豐田','卡羅拉'],characters:[],visual_tier:'stills',compilation:false,target_minutes:13,image_model:'image-01',look:{preset:'cute-mystery'},candidate_revision:'seiko-r3',status:'hold_pending_independent_source_and_fresh_readers'};write('series.json',series);
const opening=rows.filter(r=>r.chapter===rows[0].chapter).reduce((n,r)=>n+spokenUnits(r.text),0),cta=rows.slice(-2).reduce((n,r)=>n+spokenUnits(r.text),0);
const brief=['# Seiko R3｜手焊基板怎麼交到下一雙手','','新slug '+SLUG+'，沿原non-C story-adapt family。video.json無series欄，不重綁原後台。狀態HOLD_PENDING_INDEPENDENT_SOURCE_AND_FRESH_READERS。','','## 問題','','把準確塞進手腕以後，還差哪些事，才能交給下一個人？','','## 一句答案','','振子要穩定，製造流程要可掌握，後期回路還得讓人能維修。','','## 站主觀點','','從人手上的工作推進，不以Swiss崩潰單因果或企業神話代替製程證據。','','## 核心問題與單線','','把準確塞進手腕以後，還差哪些事，才能交給下一個人？第一句以1969花45萬日圓購錶仍可能送回調整的觀眾利害起手，第二句明歸屬精工企業史並落在顯微鏡下手焊電路。這是早期售後難題，不聲稱每支回廠、回廠當日或同一序號。前八句含兩個事件預告價牌/爐邊現查、點名精工產品與持續製造規模、末句核心問。','','正文從振子/回路/馬達的商品化工作往前走，到1969年12月兩批出貨與改價、上市後回廠再調整/老化、低爐溫與未記錄設定，再到35SQ外購Intersil分頻晶片、自研A型及1971年12月38系，最後到1977安川論文對零售修理、可換元件、回路自動組裝與出貨品質的具體要求。最後一段清楚屬1977後期實裝，不冒同一首批機種。沒有以一支serial錶串出完整維修劇情。','','## 規劃與實測','','全文'+whole+' native spokenUnits，coldopen '+opening+'，有聲CTA '+cta+'。規劃約3500/13分鐘；自然4–5units/s算術約'+(whole/5).toFixed(1)+'–'+(whole/4).toFixed(1)+'秒，並不是真聲PASS。官方實聲正文720–840秒，含coldopen/voicedCTA，排新增片頭片尾；actual_seconds=null。沒有加長停頓/拖慢語速。','','## 來源／書面畫面','','七章、'+rows.length+'句、'+(scenes.length-1)+' shot+1 native outro；所有正文shot，沒有連續字卡。每章有你與我，新問題接有源新答案；'+loops.length+'組書面loops仍待fresh native審讀。源圖只研究，插畫全anonymous conceptual，不畫真人/可辨品牌錶型/logo/可讀價牌或技術paper。唯一look{preset:cute-mystery}，image-01。','','開場h05/p14同價牌圖；h06/f08同爐邊檢查圖，完整Stage.imageKey純本地等值在image-reuse-plan.json。尚無實圖/真cache，實際same_asset保持false/null；只在正常製作入場後先payoff takes1，之後真cache+bytes SHA guard才容許teaser，兩端各judge，裁切後selected同檔SHA仍須讀真檔。','','## 保護與真正待辦','','三研究檔SHA凍結、三份舊B25與readonly snapshot不變；舊付費媒體不可得，舊checklist/approval不繼承。S7內部月份和功率疑誤不用；新增A01–10只綁既有原件，非獨立批准。','','八語為授權製作預設，實際各語設定/稿/配音/字幕/成片均未完成。exact新remake的US$25帳戶、protected admission與all-in quote仍未成立；禁止付費。正式PR1860片頭5秒在開場濃縮後，片尾21秒在末句後，使用../branding-pr1860/required-branding.json，缺素材/包版本不符即停。未建立本題production pin/timeline，未render。',''];fs.writeFileSync(path.join(OUT,'brief.md'),brief.join('\n'));
const coreFiles=['video.json','script.md','narration-only.json','claims.json'];const core=Object.fromEntries(coreFiles.map(f=>[f,fileSha(path.join(OUT,f))]));
const pairs=pairDefs.map(([setup,payoff,asset])=>{const a=scenes.find(s=>s.id===setup),b=scenes.find(s=>s.id===payoff);assert.equal(a.data.prompt,b.data.prompt);assert.equal(a.data.camera,b.data.camera);const prompt=shotPrompt(a,resolveLook(doc.look),[],1500);assert.equal(prompt,shotPrompt(b,resolveLook(doc.look),[],1500));const tuple={provider:'minimax',model:'image-01',prompt,negative:'',width:1920,height:1080,seed:1,references:[]},options={prompt,negative:'',references:[],seed:1,size:null},ctx={status:{image:{provider:'minimax',model:'image-01'}},format:null,imageVersion:imageSelectionVersion(series)},key=Stage.prototype.imageKey.call(ctx,options);assert.equal(key,Stage.prototype.imageKey.call(ctx,{...options,prompt:shotPrompt(b,resolveLook(doc.look),[],1500)}));return{asset_plan_id:asset,source_scene_id:payoff,reuse_scene_id:setup,narration_setup_text:a.lines[0].text,narration_payoff_text:b.lines[0].text,prompt_exact_match:true,camera_exact_match:true,source_prompt_sha256:sha(b.data.prompt),reuse_prompt_sha256:sha(a.data.prompt),camera:b.data.camera,composed_prompt_sha256:sha(prompt),no_result_drawn_in_teaser:'Anonymous neutral object before final placement/inspection; no readable price, measured furnace value, changed result or historical named likeness.',native_same_input_key_rehearsal:{pure_local_functions_only:true,input_tuple:tuple,requested_size:null,image_selection_version:imageSelectionVersion(series),seed_offset:0,takes:1,correction_list:[],prompt_budget_chars:1500,base_key:keyframeKey(tuple),native_stage_key:key,parameters_are_declared_plan_not_backend_readback:true,no_provider_call:true},actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,actual_same_asset_verified:false,actual_same_file_sha_verified:false};});
const codeFiles=['tools/video/media/keyframes.mjs','tools/video/media/stages.mjs','tools/video/media/cache.mjs','tools/video/media/prompt-budget.mjs','tools/video/core/drama.mjs','tools/video/media/trim.mjs'];
write('image-reuse-plan.json',{schema_version:1,revision:'seiko-r3',status:'WRITTEN_REUSE_PLAN_PENDING_REAL_ASSETS_AND_SHA',not_a_video_schema_extension:true,not_a_keyframes_manifest:true,no_assets_generated:true,actual_same_asset_verified:false,candidate_binding:{core_four_sha256:core,claims_md_sha256:fileSha(path.join(OUT,'claims.md')),brief_sha256:fileSha(path.join(OUT,'brief.md')),series_sha256:fileSha(path.join(OUT,'series.json'))},rule:{file:'.agents/skills/youtube-video/references/script-writing.md',sha256:fileSha(path.join(REPO,'.agents/skills/youtube-video/references/script-writing.md')),quote:'每一個預告句用回收它的那一章的畫面（同一張圖）'},code_readback:{files_sha256:Object.fromEntries(codeFiles.map(f=>[f,fileSha(path.join(REPO,f))])),still_alias_field_available:false,data_source_is_clip_only_not_still_alias:true,camera_is_part_of_composed_prompt:true,guard_is_read_only:'Use readCache(workdir), existsSync and hash actual bytes; never use cached() as a readonly guard because it can mutate/delete cache.'},pairs,production_handoff:{preconditions:['Current independent source/visual and fresh native reviews, exact owner gates, real new-project US$25 accounting and protected admission, and complete all-in quote are pending.','Before paid work, read actual provider/model/version/size/negative/refs/seed/fixes/prompt limit and recompute native keys; declared example values are not live backend/cache evidence.'],official_command_recipe_only:pairs.flatMap(p=>[{purpose:'PAYOFF FIRST only after normal production admission',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.source_scene_id,'--takes','1']},{purpose:'MANDATORY READONLY LIVE CACHE GUARD BEFORE SECOND COMMAND',checks:['Read official keyframes/manifest.json payoff selected item: judge passed, needs_review false, exact seed/take/fixes/live-key and selected file.','Hash actual selected file bytes and match selected.sha256.','Use readCache(workdir), require entries[live-key], matching provider/model/file existence and actual bytes SHA equal entry.sha256.','Cache miss, file missing, SHA mismatch, changed request, retake or selected crop mismatch: STOP pair. Do not run teaser to buy another image.']},{purpose:'TEASER only after real cache guard succeeds',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.reuse_scene_id,'--takes','1']}]),actual_verification_required:['Both scenes independently pass the ordinary judge.','Read actual official manifest selected file references and selected SHA for both, then hash the actual final bytes.','After any trim/crop require the same final selected derived file and SHA; original generated SHA alone is insufficient.','Assembly input must use the same actual selected image in teaser and payoff. Preserve normal cache/job/ledger receipts.'],on_failure:'Stop; no force/accept-best, lookalike paid reroll, fake alias, custom manifest or hand-edit cache.',executed:false},provider_calls:0,paid_calls:0});
write('protected-inputs-r3.json',{schema_version:1,role:'PRESERVATION_READBACK_NOT_APPROVAL',history_r1_receipt_sha256:fileSha(historyPath),history_files_checked:r1history.files.length,history_r2_receipt_sha256:fileSha(historyR2Path),history_r2_files_checked:r2history.files.length,all_existing_source_cache_files_checked:r2history.source_cache_protection.length,research_files_sha256:PROTECTED,related_old_files:oldChecks,legacy_paid_media_available:false,old_owner_approval_inherited:false,raw_and_text_sha_checked:true,author_source_additions_sha256:fileSha(path.join(OUT,'author-source-additions.json')),paid_calls:0});
write('author-notes.json',{schema_version:1,status:'HOLD_PENDING_INDEPENDENT_SOURCE_VISUAL_AND_FRESH_READERS',candidate_revision:'seiko-r3',author:'/root/c10_eight_text',counts:{lines:rows.length,scenes:scenes.length,shots:scenes.length-1,cards:0,outro:1,chapters:[...new Set(rows.map(r=>r.chapter))].length,loops:loops.length},native_units:{whole_narration_spoken_units:whole,coldopen:opening,voiced_CTA:cta,rough_planning_target:3500,actual_narration_seconds:null,actual_final_seconds:null,actual_duration_verified:false,planning_arithmetic_at_4_to_5_units_per_second:[whole/5,whole/4],planning_is_not_actual_time:true,official_duration_scope:'Whole unwrapped narration including coldopen and voiced CTA; excludes added5secondintro+21secondoutro.'},voice_source:{path:voicePath,file_sha256:fileSha(voicePath),voice_object_sha256:sha(JSON.stringify(voice)),exact_copy:true,other_episode_dictionary_copied:false},source_research_sha256:PROTECTED,additional_author_anchors:added.anchors.length,related_old_files_unchanged:true,source_pass_claimed:false,narrative_pass_claimed:false,owner_approval_created:false,actual_media_generated:false,actual_same_image_verified:false,provider_calls:0,paid_calls:0,backend_mutations:0,git_mutations:0,runtime_root:RUNTIME,media_base:MEDIA,image_reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json')),independent_source_review:'PENDING_OTHER_REVIEWER',independent_narrative_review:'ROUND_3_PENDING_FRESH_READERS',actual_native_round_count:2});
write('review-state.json',{schema_version:1,candidate_revision:'seiko-r3',current_source_sha256:fileSha(path.join(OUT,'video.json')),independent_source:'R3_PENDING_AFTER_R2_PASS',written_visual:'R3_PENDING_CURRENT_SOURCE',fresh_native:'ROUND_3_PENDING_FRESH_READERS',actual_native_round_count:2,previous_source_verdict:'PASS_R2',previous_native_verdict:'HOLD_shared_no_recap',previous_native_round:2,previous_evidence:'history/r2',pending_native_round:3,verify_1_created:false,owner_approvals_created:false,actual_media_available:false});
fs.writeFileSync(path.join(OUT,'producer.md'),'# Seiko R3 製作交接\n\n僅有source/recipe，paid/provider/backend/Git均0。新slug '+SLUG+'，不得借舊activated帳戶或改prefix規避保護。\n\nR1透過正常prepare-runtime.mjs seiko在全新 '+RUNTIME+' 已初始化一次普通immutable story lexicon；R3沿用同一字典與current pointer，不重建；media base '+MEDIA+'，不複製其他集字典/批准。只跑免費lint與projection核對，R2 SOURCE與書面配鏡PASS、native2共享no_recap HOLD，完整verify/raw/input/payload等保存在history/r2；actual native count=2，新SOURCE與native3待真審。R3僅p08移除重複45萬，其他句與所有配鏡不變。字典念法/來源/fresh narrative/owner/US$25 exact帳戶與全片報價都仍待處理。\n\n同圖recipe詳image-reuse-plan.json；正常admission後先payoff takes1，第二命令前用readCache+真manifest+bytes SHA guard。缺cache即停，兩端各judge且裁切後selected同路徑/同SHA仍須驗，不把規劃key當實際素材。\n\n正式片頭5秒在開場濃縮後，片尾21秒在末句後，政策../branding-pr1860/required-branding.json；fresh readonly preflight before assembly，缺包/disabled/版本錯/不可比對即停。未建production pin或timeline。\n\n正文實聲720–840秒含coldopen及有聲CTA，排26秒bookends；自然4–5units/s不拖慢。八語預設各語仍須真語意審/聲音/字幕/整片QA。所有生成storymedia0。研究三檔/原related3檔/readonly snapshot rawSHA不變，不繼承舊後台checklist。\n');
console.log(JSON.stringify({core_four_sha256:core,whole_units:whole,coldopen:opening,CTA:cta,lines:rows.length,scenes:scenes.length,shots:scenes.length-1,chapters:[...new Set(rows.map(r=>r.chapter))].length,loops:loops.length,unique_composed_shot_requests:new Set(scenes.filter(s=>s.template==='shot').map(s=>shotPrompt(s,resolveLook(doc.look),[],1500))).size,image_reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json')),paid_calls:0},null,2));

