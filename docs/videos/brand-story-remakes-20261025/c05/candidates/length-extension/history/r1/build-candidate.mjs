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
const CACHE='/workspace/work/brand-story-20261025/c05-audit/source-check';
const EXPECTED='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const fileSha=p=>sha(fs.readFileSync(p));
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const writeJson=(name,x)=>fs.writeFileSync(path.join(OUT,name),JSON.stringify(x,null,2)+'\n');
const ADDITIONS=[
  {
    "after": "c05r013",
    "id": "c05le001",
    "text": "可是你想一想，同樣一株除蟲菊，為什麼收下來磨的偏偏是花，不是整把葉子？",
    "sources": [
      "K_F"
    ],
    "locator": "除蟲菊について：乾花中的成分、葉及莖幾乎沒有",
    "new_fact": "花與葉、莖的有效成分分布不同，為材料選擇增加具體原因。",
    "prompt": "Medium shot of one anonymous grower comparing a shallow basket of small white flowers with a separate bundle of leaves on a workbench, soft morning window light.",
    "camera": "push in"
  },
  {
    "after": "c05r013",
    "id": "c05le002",
    "text": "原廠後來說，有效成分主要在乾花中，葉和莖幾乎沒有。",
    "sources": [
      "K_F"
    ],
    "locator": "除蟲菊について：殺蟲成分存在於乾花，葉／莖幾乎沒有",
    "new_fact": "原廠對乾花、葉及莖的具體區分；不推斷當年已做此分析。",
    "prompt": "Close-up of one anonymous worker sorting dried flower heads into a plain bowl while setting stems aside, neutral workshop light.",
    "camera": "pan left"
  },
  {
    "after": "c05r013",
    "id": "c05le022",
    "text": "可是，收下同一種花，含量就都一樣嗎？",
    "sources": [
      "K_F"
    ],
    "locator": "除蟲菊について：殺蟲成分存在於乾花，葉／莖幾乎沒有",
    "new_fact": "以含量是否相同的具體問題銜接開花程度的原廠說明。",
    "prompt": "Medium shot of one anonymous grower comparing unopened buds with a fully opened small white flower, soft daylight.",
    "camera": "push in"
  },
  {
    "after": "c05r013",
    "id": "c05le003",
    "text": "花朵展開的程度也會影響含量，盛開時最多。你手上那碗粉，前面先有了採什麼、何時採的差別。",
    "sources": [
      "K_F"
    ],
    "locator": "除蟲菊について：隨花蕾膨大增加、盛開時最大",
    "new_fact": "開花程度影響含量，把採花選擇接到粉料；不加新的採收年代或比例。",
    "prompt": "Close-up of one anonymous grower examining a fully opened small white flower beside unopened buds, mild daylight.",
    "camera": "pull out"
  },
  {
    "after": "c05r050",
    "id": "c05le004",
    "text": "你若站在這台機器前，送進去的不是一把乾粉。粉一倒就散，怎麼變成能被擠出去的那一塊？",
    "sources": [
      "NM_MACHINE"
    ],
    "locator": "910191180004 特徵：粉／糊粉加水成黏土狀塊料",
    "new_fact": "用尚未解答的入口材料狀態引出押出前工序，不加設備內部構造。",
    "prompt": "Medium shot of one anonymous worker holding a soft lump beside a plain extrusion inlet and a separate bowl of loose powder, soft workshop light.",
    "camera": "push in"
  },
  {
    "after": "c05r050",
    "id": "c05le005",
    "text": "科博館對這台押出機的記錄說，除蟲菊粉和糊粉等原料，先加水混合，成為像黏土的塊料。",
    "sources": [
      "NM_MACHINE"
    ],
    "locator": "910191180004 特徵：原料粉／糊粉加水混合為黏土狀",
    "new_fact": "新增水、糊粉與黏土狀塊料的製造動作，限於該手卷押出設備記錄。",
    "prompt": "Close-up of one anonymous worker mixing plain powder and water into a soft lump in a shallow basin, warm overhead workshop light.",
    "camera": "tilt down"
  },
  {
    "after": "c05r050",
    "id": "c05le006",
    "text": "先讓散粉聚成塊，才輪到機器往外擠；可接著盤成圓，還是同一台機器的工作嗎？",
    "sources": [
      "NM_MACHINE",
      "EDITORIAL"
    ],
    "locator": "910191180004 塊料→長條；旁白對成形分工的反應",
    "new_fact": "將塊料的入口需求與押出作用接起；末句明示旁白反應。",
    "prompt": "Close-up of one anonymous worker moving a soft lump toward a simple unmarked extrusion inlet, low window light.",
    "camera": "pan right"
  },
  {
    "after": "c05r052",
    "id": "c05le007",
    "text": "另一筆商品登錄還留下中心那塊小木片。兩根合在一起之後，手又該先往哪裡繞？",
    "sources": [
      "NM_COIL"
    ],
    "locator": "910191180006 製法段：以木片作芯、兩根手卷；不採其括號日期",
    "new_fact": "新增作芯木片，讓手卷的中心動作有具體物件。",
    "prompt": "Close-up of one anonymous worker positioning two plain soft strands beside a small plain wooden core on a round work board, soft side light.",
    "camera": "push in"
  },
  {
    "after": "c05r052",
    "id": "c05le008",
    "text": "長條先切成一定長度，再以木片作芯，兩根一起盤。你可以想像，手上每放好一圈，整個圓才慢慢長出來。",
    "sources": [
      "NM_COIL",
      "NM_MACHINE",
      "EDITORIAL"
    ],
    "locator": "910191180006 製法段：定長切條、木片作芯、兩根手卷",
    "new_fact": "新增定長切條與作芯盤卷，不使用產能數字或內部矛盾日期。",
    "prompt": "Close-up of one anonymous worker curling two plain soft strands around a small wooden core on a work board, gentle workshop light.",
    "camera": "pan left"
  },
  {
    "after": "c05r052",
    "id": "c05le009",
    "text": "盤好後，還要把整卷放到金網上乾燥。剛才繞好的形狀，現在得從工人的雙手，交給網面承放。",
    "sources": [
      "NM_COIL"
    ],
    "locator": "910191180006 製法段：金網上乾燥",
    "new_fact": "新增歷史手卷後的金網乾燥／承放工序，不加乾燥時間或溫度。",
    "prompt": "Medium shot of one anonymous worker placing a plain joined coil flat on a simple wire mesh drying tray, diffuse workshop light.",
    "camera": "pull out"
  },
  {
    "after": "c05r092",
    "id": "c05le010",
    "text": "你可以把那把刀想成餅乾模，科博館也是這樣比喻。刀型已備好輪廓，可送到刀下的，為何是一片料？",
    "sources": [
      "NM_MACHINE"
    ],
    "locator": "910191180004 特徵：如餅乾打型，以巴形渦卷刃型打抜",
    "new_fact": "新增刀型輪廓如何取代逐圈盤卷的具體製造類比。",
    "prompt": "Close-up of a plain interlocking spiral cutting die above a flat sheet of soft material, neutral factory light.",
    "camera": "tilt down"
  },
  {
    "after": "c05r092",
    "id": "c05le011",
    "text": "原廠先用混和機揉合，再擠成板狀，讓刀型從平面取出螺旋。",
    "sources": [
      "K_F",
      "NM_MACHINE",
      "EDITORIAL"
    ],
    "locator": "K_F 家庭用殺蟲劑略歷：混和機練料、押出板狀、打型；004為長條押出",
    "new_fact": "新增混和機揉合動作，區分同名押出步驟的不同出料形態與後續角色。",
    "prompt": "Medium shot of one anonymous technician inspecting a plain flat sheet emerging beside a simple mixing vat, clean overhead factory light.",
    "camera": "pan right"
  },
  {
    "after": "c05r092",
    "id": "c05le023",
    "text": "讓我意外的是，同名押出機，前面交長條，這裡卻交片材。",
    "sources": [
      "K_F",
      "NM_MACHINE",
      "EDITORIAL"
    ],
    "locator": "K_F 家庭用殺蟲劑略歷：混和機練料、押出板狀、打型；004為長條押出",
    "new_fact": "明示作者對前後押出形態分工的反應，不主張兩台相同型號設備。",
    "prompt": "Medium shot of one anonymous technician comparing a soft strand on one tray with a plain flat sheet on another, diffuse workshop light.",
    "camera": "pull out"
  },
  {
    "after": "c05rx010",
    "id": "c05le012",
    "text": "原廠的說明把兩個位置分開。你看到香端發紅，有效成分就一定要等到那一點才離開嗎？",
    "sources": [
      "K_F"
    ],
    "locator": "なぜ蚊取線香で蚊が死ぬ：燃燒端與前端前方揮散位置",
    "new_fact": "把成分進入空氣的問題進一步定位到燃燒端前方，而不是添加效力保證。",
    "prompt": "Close-up of a plain smoldering spiral coil resting on a shallow dish, a tiny glowing tip visible in dim evening light.",
    "camera": "push in"
  },
  {
    "after": "c05rx010",
    "id": "c05le013",
    "text": "燃燒端大約七百度到八百度；香體上離前端六到八毫米的位置，約二百五十度，有效成分在那裡揮散。",
    "sources": [
      "K_F"
    ],
    "locator": "なぜ蚊取線香で蚊が死ぬ：700–800℃；前端6–8mm／約250℃揮散",
    "new_fact": "新增原廠的兩位置、距離與溫度，限於原廠所述作用機制。",
    "prompt": "Close-up of a plain incense coil with a small glowing end and an intact section immediately ahead, resting motionless on an unmarked holder, soft low light.",
    "camera": "pan left"
  },
  {
    "after": "c05rx010",
    "id": "c05le014",
    "text": "照這個說法，還沒變成灰的那一小段，已在把成分交給空氣。可釋出的工作，怎麼跟著火一路走完？",
    "sources": [
      "K_F"
    ],
    "locator": "同段：前方約250℃位置揮散；依原廠位置敘述的白話解讀",
    "new_fact": "說明位置差異的觀眾意義，不主張本集量過溫度或微粒。",
    "prompt": "Close-up of a plain coil showing an intact section beside a short ash segment, with faint wisps above the dish, quiet evening light.",
    "camera": "pull out"
  },
  {
    "after": "c05rx010",
    "id": "c05le015",
    "text": "那份說明還把工作寫成燃燒中連續釋放；一卷慢慢走完，也在把有效成分一段接一段送進空氣。",
    "sources": [
      "K_F"
    ],
    "locator": "末段：燃燒時間中不斷連續釋放有效成分",
    "new_fact": "新增持續釋放與慢燃進程的分工；不引用安全性、濃度或效力保證。",
    "prompt": "Medium shot of one anonymous adult watching a plain coil smolder steadily in a shallow dish beside an open blank notebook, soft evening window light.",
    "camera": "pan right"
  },
  {
    "after": "c05r093",
    "id": "c05le016",
    "text": "說到灰，還記得開場桌邊那一截嗎？香燒過一段，灰為什麼也常斷成一段，沒有一直連著還沒燒完的香？",
    "sources": [
      "K_F",
      "EDITORIAL"
    ],
    "locator": "なぜ蚊取線香の灰が切れてしまう：灰斷開；回扣c05r002實際出現的灰",
    "new_fact": "以開場已出現的灰提出新受力問題，不補歷史事故。",
    "prompt": "Close-up of one anonymous adult studying a short separated ash segment beside the remaining plain coil on a shallow dish, low warm light.",
    "camera": "push in"
  },
  {
    "after": "c05r093",
    "id": "c05le017",
    "text": "原廠以香皿的墊面解釋：一股力讓灰和香體相連，另一股摩擦力，卻要把灰留在墊面原來的位置。",
    "sources": [
      "K_F"
    ],
    "locator": "灰為何斷：香體相連力與白墊摩擦力",
    "new_fact": "新增香皿支撐下的兩股力，限於原廠指定容器情境。",
    "prompt": "Close-up of a plain coil and its attached ash resting on a simple light-colored mat inside a shallow dish, soft side light.",
    "camera": "pan left"
  },
  {
    "after": "c05r093",
    "id": "c05le018",
    "text": "灰累積到一定長度，摩擦力超過相連的力，灰就斷開；接著再燃燒、再累積，這個過程反覆發生。",
    "sources": [
      "K_F"
    ],
    "locator": "灰為何斷：一定長度後摩擦力大、斷開並反覆",
    "new_fact": "新增斷灰的條件與循環，不虛構固定斷灰長度。",
    "prompt": "Close-up of several short ash segments aligned behind a plain smoldering coil on a shallow dish, diffuse low light.",
    "camera": "pull out"
  },
  {
    "after": "c05r093",
    "id": "c05le024",
    "text": "如果改由線香立支撐，原廠又用哪一股力，解釋灰為什麼往下落？",
    "sources": [
      "K_F"
    ],
    "locator": "灰為何斷：線香立情境改以灰的重量解釋",
    "new_fact": "以不同支撐方式提出具體力學問題，下一句給出重力條件。",
    "prompt": "Medium shot of one anonymous adult leaning toward a small plain incense stand over a ceramic tray, thoughtful face, evening lamp light.",
    "camera": "push in"
  },
  {
    "after": "c05r093",
    "id": "c05le019",
    "text": "原廠把另一邊換成灰的重量：重力超過相連的力，灰便往下落，依然是一段段交接。",
    "sources": [
      "K_F"
    ],
    "locator": "灰為何斷：線香立情境為相連力對灰重量／向下落力",
    "new_fact": "新增另一種支撐方式下的力學對照；不是操作或安全建議。",
    "prompt": "Close-up of a plain incense coil supported by a simple unmarked stand above a tray, with a small ash fragment below, soft window light.",
    "camera": "tilt down"
  },
  {
    "after": "c05r093",
    "id": "c05le020",
    "text": "原廠在罐裝香皿的問答裡說，燃著的部分若直接碰到上蓋金屬，就會被帶走熱，可能中途熄掉。",
    "sources": [
      "K_Q"
    ],
    "locator": "缶入上蓋金屬部分直接接觸火種會奪熱立消；其他立消原因列金屬接觸",
    "new_fact": "新增原廠罐裝香皿所述上蓋金屬接觸火種、熱流失及立消風險，未泛稱所有金屬皆如此。",
    "prompt": "Close-up of a plain incense tip beside a simple unmarked metal dish edge, with a darkened ember and a short ash segment, quiet low light.",
    "camera": "push in"
  },
  {
    "after": "c05r093",
    "id": "c05le021",
    "text": "原來承放也有取捨：要接住香和灰，又可能從接觸處帶走熱。我覺得這讓能燒多久，從香體一路連到它放在哪裡。",
    "sources": [
      "K_Q",
      "K_F",
      "EDITORIAL"
    ],
    "locator": "K_Q 金屬接觸奪熱立消；K_F 香皿支撐／摩擦；旁白對支撐與熱接觸的解讀",
    "new_fact": "把灰的支撐與熱接觸造成的中斷連為具體取捨，明示作者反應。",
    "prompt": "Medium shot of one anonymous adult studying a plain coil and its ash resting in a shallow dish, thoughtful expression, soft evening window light.",
    "camera": "pull out"
  }
];
const base=read(path.join(BASE,'video.json'));
assert.equal(fileSha(path.join(BASE,'video.json')),EXPECTED);
assert.equal(fileSha(path.join(CANON,'video.json')),EXPECTED);
const protectedPaths=['video.json','script.md','claims.md','narration-only.json','brief.md','series.json'].map(n=>path.join(BASE,n));
protectedPaths.push(path.join(CANON,'video.json'),path.join(CANON,'script.md'));
const protectedBefore=Object.fromEntries(protectedPaths.map(p=>[p,fileSha(p)]));
const doc=structuredClone(base);
const grouped=new Map();
for(const row of ADDITIONS){if(!grouped.has(row.after))grouped.set(row.after,[]);grouped.get(row.after).push(row);}
const inserted=[];
doc.scenes=[];
for(const scene of base.scenes){
  doc.scenes.push(structuredClone(scene));
  const key=scene.lines.at(-1)?.id;
  for(const row of grouped.get(key)||[]){
    const added={id:row.id,template:'shot',data:{prompt:row.prompt,camera:row.camera,visual:'still'},lines:[{id:row.id,text:row.text,emotion:'對一位觀眾自然說書；工序清楚，問句上揚，反應保留第一人稱'}]};
    doc.scenes.push(added);inserted.push(row.id);
  }
}
assert.equal(inserted.length,ADDITIONS.length);
const newLoops=[
 ['c05le001','c05le002','為何磨花而不是整把葉子'],
 ['c05le022','c05le003','同一種花的開花程度如何影響含量'],
 ['c05le004','c05le005','散粉怎麼成為押出機的入口塊料'],
 ['c05le006','c05r051','押出以後是否還由同台機器盤成圓'],
 ['c05le007','c05le008','手卷的中心如何靠木芯形成'],
 ['c05le010','c05le011','刀型為何等一片料而非兩條長條'],
 ['c05le012','c05le013','成分在燃燒端前方哪裡揮散'],
 ['c05le014','c05le015','釋出如何跟著燃燒持續往前'],
 ['c05le016','c05le018','開場截灰後來如何以受力解釋'],
 ['c05le024','c05le019','改由線香立支撐後是哪股力拉下灰']
].map(([setup,payoff,what])=>({setup,payoff,what}));
doc.loops.push(...newLoops);
const newSources=[
 {title:'國立科學博物館手卷押出機登錄',url:'https://sts.kahaku.go.jp/sts/detail.php?no=910191180004',checked_on:'2026-10-25'},
 {title:'國立科學博物館渦卷商品登錄（製法段）',url:'https://sts.kahaku.go.jp/sts/detail.php?no=910191180006',checked_on:'2026-10-25'}
];
doc.sources.push(...newSources);
doc.youtube.description += '\n'+newSources.map(s=>s.title+'\n'+s.url).join('\n');
const preservedKeys=Object.keys(base).filter(k=>!['scenes','loops','sources','youtube'].includes(k));
for(const k of preservedKeys)assert.deepEqual(doc[k],base[k]);
for(const k of Object.keys(base.youtube).filter(k=>k!=='description'))assert.deepEqual(doc.youtube[k],base.youtube[k]);
const oldById=new Map(base.scenes.map(s=>[s.id,s]));
for(const scene of doc.scenes)if(oldById.has(scene.id))assert.deepEqual(scene,oldById.get(scene.id));
assert.deepEqual(validateVideo(doc),[]);
const flat=[];let chapter='',chapterIndex=-1,body=0,total=0,outro=0,hook=0;
for(const {scene,line}of eachLine(doc)){
 if(scene.chapter){chapter=scene.chapter;chapterIndex++;}
 const units=spokenUnits(line.text);total+=units;
 if(chapterIndex===0)hook+=units;else body+=units;
 if(scene.template==='outro')outro+=units;
 flat.push({chapter,id:line.id,text:line.text});
}
const originalTotal=[...eachLine(base)].reduce((n,x)=>n+spokenUnits(x.line.text),0);
const added=ADDITIONS.reduce((n,x)=>n+spokenUnits(x.text),0);
assert.equal(total,originalTotal+added);
assert(body>=3300 && body<=3550);
assert(body-outro>=3300 && body-outro<=3550);
const originalRows=read(path.join(BASE,'narration-only.json'));
const retained=flat.filter(r=>!inserted.includes(r.id));
assert.deepEqual(retained,originalRows);
const sourceReceipt=read('/workspace/work/brand-story-20261025/c05-audit/readiness-review.json');
const sourceMap=Object.fromEntries(sourceReceipt.sources_reopened.map(s=>[s.id,s]));
const priorEvidence=Object.fromEntries(read(path.join(BASE,'reviews/source-r6-delta.json')).line_results.map(r=>[r.line_id,r.source_evidence]));
const claims=flat.map(row=>{
 const add=ADDITIONS.find(a=>a.id===row.id);
 const ids=add?add.sources:priorEvidence[row.id]||[];
 return {id:row.id,chapter:row.chapter,claim:row.text,status:'PENDING_INDEPENDENT_REVIEW',change:add?'ADDED':'UNCHANGED_FROM_R6',source_ids:ids,
 sources:ids.filter(id=>sourceMap[id]).map(id=>({id,url:sourceMap[id].url,raw_cache:path.join(CACHE,id+'.html'),raw_sha256:sourceMap[id].raw_sha256,text_cache:path.join(CACHE,id+'.txt')})),
 locator:add?.locator||'既有r6映射；原句未改，舊來源報告只對舊SHA有效。',
 new_information:add?.new_fact||null};
});
const brief=[
'# C05 長度增補候選｜單一 A','',
'狀態：未核准候選。保留r6全部97句與舊檔，本目錄不含verify檔或任何新稿PASS。','',
'## 選項 A：把一條香做成能交付的工作','',
'沿同一卷香，從乾花／粉料、加水成塊、押出與盤卷，到打型、燃燒、支撐及灰的交接，回答外形為何只完成一部分工作。不是另一個故事版本。','',
'## 問題','',
'為什麼把香盤成螺旋，還不夠讓它久燃、完整地走上貨架？','',
'## 一句答案','',
'螺旋收進長路徑；原料須先能被加工，盤卷或刀型把形狀做出來，雙卷承擔運輸，香體結構、熱與支撐再共同影響它如何持續燃燒。','',
'## 站主觀點','',
'我覺得這個日用品最有意思的，是每到下一雙手或下一個位置，都要換一種具體工作：粉要聚成料、料要被押出、圓要能離手與運送、燃燒還要把成分交進空氣。對一位觀眾把這條因果說清楚；公司回顧、館藏與現行規格不混為同一年代，不補專利核准、逐年試作或全廠換線。','',
'## 目標與待查','',
'正文目標3300–3550 native spokenUnits。本候選同時列出排除開場，以及再排除有聲片尾的口徑；皆為文字量，實際TTS時長、音色、配鏡及節奏仍未知。維持原slug、voice、look、burn_in=true及原標題／縮圖／tags；僅因新增來源，說明欄附加兩條官方登錄。','',
'保留原97句逐字；新增句與新來源映射均待另一位來源讀者及兩位隔離敘事讀者，作者不給新稿PASS。新鏡頭為匿名英文概念插圖、靜態運鏡；不重建真實人物或歷史實驗。原件快取留work，不進repo。未呼叫provider／後台／付費，未搬入canonical。',''
].join('\n');
fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const series=read(path.join(BASE,'series.json'));
series.status='length_extension_candidate_unapproved';
series.parent_source_video_sha256=EXPECTED;
series.independent_source_review_required=true;
series.two_isolated_narrative_readers_required=true;
writeJson('video.json',doc);writeJson('narration-only.json',flat);writeJson('series.json',series);
writeJson('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_REVIEW',parent_source_video_sha256:EXPECTED,rows:claims});
const script=['# '+doc.youtube.title,'','未核准長度候選；ID與來源只供審閱，不讀入旁白。正文97句保留，新增句須獨立重查。',''];
let last='';
for(const row of flat){
 if(row.chapter!==last){last=row.chapter;script.push('## '+last,'');}
 script.push('### '+row.id,'',row.text,'');
}
fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 長度候選逐句主張','', '全部PENDING_INDEPENDENT_REVIEW；作者沒有將舊source PASS轉移為新稿PASS。','', '| ID | 狀態 | 旁白 | 來源索引 | 新增資訊／定位 |','| --- | --- | --- | --- | --- |'];
for(const row of claims)cm.push('| '+row.id+' | '+row.status+' | '+row.claim+' | '+row.source_ids.join(', ')+' | '+(row.new_information||'原r6逐字保留')+'；'+row.locator+' |');
cm.push('','## 原件與使用範圍','');
for(const id of [...new Set(ADDITIONS.flatMap(x=>x.sources))].filter(id=>sourceMap[id])){
 const s=sourceMap[id];cm.push('- '+id+'：'+s.url+'；HTTP '+s.status+'，讀取日2026-10-25；raw SHA '+s.raw_sha256+'；快取 '+path.join(CACHE,id+'.html'));
}
cm.push('','NM_COIL只用製法段的定長切條、木芯、手卷與網上乾燥。該頁西元括號與紀年換算有衝突，不用它補任何日期、產能或首創主張；原稿年代仍按原來源。所有廠方機制均保留歸屬，不加入安全／效力保證或本集實驗。','');
fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const lexicon=read('/workspace/work/brand-remakes-source/docs/videos/lexicon.json');
const lint=lintVideo(doc,{brief,lexicon,series,translations:{}});
const lineIndex=new Map(flat.map((r,i)=>[r.id,i]));
const eight=[['c05r003','c05r036'],['c05r005','c05r052'],['c05r025','c05r055'],['c05r043','c05r045'],['c05r067','c05r069'],['c05r084','c05r085'],['c05r089','c05r090'],['c05le001','c05le002'],['c05le004','c05le005'],['c05le007','c05le008'],['c05le010','c05le011'],['c05le012','c05le013'],['c05le016','c05le018']];
const payoffs=eight.map(([setup,payoff])=>{assert(lineIndex.get(setup)<lineIndex.get(payoff));return {setup,payoff,status:'AUTHOR_INTENT_PENDING_BLIND_REVIEW'};});
const unitBefore=new Map();let cumulative=0;
for(const row of flat){unitBefore.set(row.id,cumulative);cumulative+=spokenUnits(row.text);}
const hookIds=[...new Set(doc.loops.map(x=>x.setup))].sort((a,b)=>lineIndex.get(a)-lineIndex.get(b));
const gaps=hookIds.slice(1).map((id,i)=>({from:hookIds[i],to:id,spoken_units:unitBefore.get(id)-unitBefore.get(hookIds[i]),seconds_at_4_5_units:Math.round((unitBefore.get(id)-unitBefore.get(hookIds[i]))/4.5*100)/100}));
const shotUnits=[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(x.line.text),0);
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json'];
const notes={
status:'UNAPPROVED_LENGTH_EXTENSION_CANDIDATE',author:'/root/c03_review_pt_id',source_review_for_parent_only:'/workspace/work/brand-story-20261025/c05-audit/readiness-review.json',
parent_source_video_sha256:EXPECTED,parent_canonical_script_sha256:fileSha(path.join(CANON,'script.md')),parent_repo_script_sha256:fileSha(path.join(BASE,'script.md')),
source_review_of_new_candidate:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_ISOLATED_READERS',native_verify_file_written:false,
delta:{retained_original_line_count:retained.length,retained_original_texts_exact:true,retained_original_scene_objects_exact:true,changed_original_lines:[],deleted_original_lines:[],added_line_count:ADDITIONS.length,added_spoken_units:added,new_lines:ADDITIONS.map(r=>({id:r.id,insert_after:r.after,text:r.text,spoken_units:spokenUnits(r.text),source_ids:r.sources,source_locator:r.locator,new_information:r.new_fact})),
metadata_changes:[{target:'youtube.description',change:'Append only two required official-source entries; body, original source list, title, tags and thumbnail unchanged.'}],new_source_entries:newSources,new_loops:newLoops},
native_units:{counter:'tools/video/core/timeline.mjs spokenUnits + core/schema.mjs eachLine',original_total:originalTotal,original_hook:hook,original_body_excluding_hook:originalTotal-hook,original_body_excluding_hook_and_outro:originalTotal-hook-outro,candidate_total:total,candidate_hook:hook,candidate_body_excluding_hook:body,candidate_body_excluding_hook_and_outro:body-outro,candidate_outro:outro,target_body_range:[3300,3550],actual_tts_seconds:null,actual_duration_verified:false},
planned_visuals:{scenes:doc.scenes.length,lines:flat.length,illustration_scenes:doc.scenes.filter(s=>s.template==='shot').length,cards:doc.scenes.filter(s=>s.template!=='shot').length,planned_illustration_unit_share:shotUnits/total,planning_basis:'spoken-unit share only; not measured screen time',new_scenes_all_still:true,new_prompts_anonymous_english:true,actual_generated_media_reviewed:false},
loop_audit:{total_declared_loops:doc.loops.length,concrete_pairs_for_blind_review:payoffs,max_setup_gap_by_units:gaps.sort((a,b)=>b.spoken_units-a.spoken_units)[0],gaps_at_4_5_units_are_estimates_only:true},
source_caveats:['NM_COIL Gregorian parentheses disagree with era conversion; use only its fabrication actions, not dates or output figures.','Dry flower powder is not pollen. New botanical content is a later manufacturer explanation, not an 1887 assay.','Historical hand-roll inlet water and clay-like material are confined to NM_MACHINE; no invented moisture ratio or drying setting.','Temperatures, release position, ash forces and metal-contact extinction are manufacturer explanations; no independent test, medical claim or safety guarantee.','Ash and support detail may be a narrative detour; leave relevance and pacing to the two isolated readers rather than author PASS.'],
lint:{errors:lint.errors,warnings:lint.warnings,summary:lint.summary,scope:'local text/structure only; estimates are not measured TTS or media acceptance'},
file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))])),
protected_parent_inputs_unchanged:Object.fromEntries(protectedPaths.map(p=>{assert.equal(fileSha(p),protectedBefore[p]);return[p,true];})),paid_calls:0,backend_writes:0,git_commands:0,canonical_written:false
};
writeJson('author-notes.json',notes);
console.log(JSON.stringify({out:OUT,lines:flat.length,scenes:doc.scenes.length,added_units:added,native_units:notes.native_units,lint_errors:lint.errors,lint_warnings:lint.warnings,largest_hook_gap:notes.loop_audit.max_setup_gap_by_units},null,2));
