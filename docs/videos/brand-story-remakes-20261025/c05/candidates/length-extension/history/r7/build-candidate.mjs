import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine,spokenText,validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {loadProject,lintProject} from '/workspace/work/brand-remakes-source/tools/video/core/state.mjs';
const OUT=path.dirname(fileURLToPath(import.meta.url)),BASE=path.resolve(OUT,'../..'),PRIOR=path.join(OUT,'history/r6-skeleton'),RESEARCH=path.join(BASE,'research-expansion');
const ROOT='/workspace/work/brand-story-20261025/submission-root',SLUG='story-everyday-kincho-c05-remake-20261025';
const BASE_SHA='7fbc22336a476a32f684b463154b420a07ba5fa6377e7454b3d4b1e8edbf720a',R6_SHA='155dc0ac8a8949fd0adea91a28e6afd8c3571cb9bce6597533152c1e617eabb6';
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=f=>sha(fs.readFileSync(f)),read=f=>JSON.parse(fs.readFileSync(f,'utf8')),write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(p,e.name)):[path.join(p,e.name)]);
const protectedFiles=[...fs.readdirSync(BASE,{withFileTypes:true}).filter(e=>e.isFile()).map(e=>path.join(BASE,e.name)),...walk(path.join(BASE,'i18n')),...walk(path.join(ROOT,'docs/videos',SLUG)),...walk(path.join(OUT,'history')),...walk(path.join(OUT,'reviews')),...walk(RESEARCH)];
const protectedBefore=Object.fromEntries(protectedFiles.map(f=>[f,fileSha(f)]));
assert.equal(fileSha(path.join(PRIOR,'video.json')),R6_SHA);assert.equal(fileSha(path.join(BASE,'video.json')),BASE_SHA);
assert.equal(fileSha(path.join(RESEARCH,'research.md')),'0241eb279172af302351ffa72f43264313a521d30fe2ffa86429bad22f371ff0');
assert.equal(fileSha(path.join(RESEARCH,'claims.json')),'2219f8d5e97ac0647d2947319567695dea5bb90387edd6f5ae86e7dd1f656bc4');
const prior=read(path.join(PRIOR,'video.json')),priorRows=read(path.join(PRIOR,'narration-only.json')),priorClaims=read(path.join(PRIOR,'claims.json')),research=read(path.join(RESEARCH,'claims.json'));
const oldRows=new Map(priorRows.map(r=>[r.id,r])),oldClaims=new Map(priorClaims.rows.map(r=>[r.id,r])),oldScenes=new Map(prior.scenes.flatMap(s=>(s.lines??[]).map(l=>[l.id,s])));
const sourceMap=new Map(priorClaims.rows.flatMap(r=>r.sources??[]).map(s=>[s.id,s]));for(const [id,s]of Object.entries(research.sources))sourceMap.set(id,{id,...s});
for(const s of sourceMap.values())if(s.raw_cache)assert.equal(fileSha(s.raw_cache),s.raw_sha256);
for(const s of Object.values(research.sources)){if(s.retrieval)assert.equal(fileSha(s.retrieval.path),s.retrieval.sha256);for(const p of s.page_texts??[])assert.equal(fileSha(p.text.path),p.text.sha256);for(const p of Object.values(s.image_receipts??{}))assert.equal(fileSha(p.path),p.sha256);}
research.anchors.N26_DRY={source:'NDL1897',printed_page:26,canvas:17,page_side:'right',short_excerpt:'晴天四五日間',read_mode:'R7 author manually read actual scan; historical guidance only.',image_sha256:research.sources.NDL1897.image_receipts['17'].sha256};
research.anchors.N26_WET={source:'NDL1897',printed_page:26,canvas:17,page_side:'right lower columns',short_excerpt:'製粉の後變色す',read_mode:'R7 author manually read actual scan; historical guidance only.',image_sha256:research.sources.NDL1897.image_receipts['17'].sha256};
const scenes=[],rows=[],claims=[];let chapter='';
function ch(s){chapter=s;}
function add(id,text,prompt,refs=[],locator='',kind='FACT_OR_FORWARD_QUESTION'){
 const old=oldClaims.get(id),oldScene=oldScenes.get(id),scene=oldScene?structuredClone(oldScene):{id,template:'shot',data:{camera:'push in',visual:'still'},lines:[{id,emotion:'對一個朋友說書，自然起伏；意見用自己的反應，數字清楚'}]};
 scene.id=id;if(scene.template==='shot')scene.data.camera=['push in','pan left','pull out','pan right','drift','tilt up','tilt down'][scenes.length%7];delete scene.chapter;scene.lines=scene.lines.filter(l=>l.id===id);scene.lines[0].text=text;delete scene.lines[0].say;delete scene.lines[0].say_for;delete scene.lines[0].pause_after_ms;if(prompt)scene.data.prompt=prompt;if(!scenes.length||rows.at(-1)?.chapter!==chapter)scene.chapter=chapter;scenes.push(scene);rows.push({chapter,id,text});
 const anchors=refs.filter(r=>research.anchors[r]).map(r=>({id:r,...research.anchors[r]})),ids=[...new Set([...refs.filter(r=>sourceMap.has(r)),...anchors.map(a=>a.source)])],useIds=ids.length?ids:(old?.source_ids??['EDITORIAL']);
 claims.push({id,chapter,claim:text,status:'PENDING_INDEPENDENT_REVIEW',change:old?(old.claim===text?'R6_TEXT_RETAINED':'REWRITTEN_IN_R7'):'NEW_IN_R7',claim_kind:kind,source_ids:useIds,sources:useIds.filter(i=>sourceMap.has(i)).map(i=>sourceMap.get(i)),locator:locator||old?.locator||'作者問題／明示想像／意見，不主張新歷史事件。',source_anchors:anchors.length?anchors:(old?.source_anchors??[]),r6_claim_sha256:old?sha(old.claim):null});
}
function keep(id){const r=oldRows.get(id);assert(r,id);add(id,r.text);}
ch('一根香燒完，夜還很長');
keep('c05r001');keep('c05r002');
add('c07o03','我原以為，蚊香難在盤成那個圓；可材料還沒變成香，就已經有一道關卡。','Medium close-up of an anonymous adult looking curiously at a bowl of dried daisy flowers beside an unlit plain coil, warm desk light.',['EDITORIAL'],'作者原先想法與向前問題，尚未揭露乾花處理結果。','AUTHOR_REACTION');
add('c07o04','採下的花遇上連雨怎麼辦，點火後成分又從哪裡離開？','Wide shot of a shallow basket of freshly picked daisy flowers beside a rain-streaked window, soft daylight.',['N27_RAIN','K_F'],'兩個未揭結果預告，在c07d08及c05le013兌現。','TWO_UNRESOLVED_PREVIEWS');
add('c07o05','金鳥這一卷香，我們沿著百餘年的材料選擇，追到你點火的那一端。','Medium shot of an anonymous adult holding a plain unlit coil above a small table, gentle evening light.',['EDITORIAL'],'單一材料旅程承諾，非同一包材料穿越年代。','SINGLE_PROMISE');
add('c07o06','一把會散的乾花粉末，憑什麼變成能陪你過夜的商品？','Close-up of dried flower powder slipping between anonymous fingers above a plain bowl, side light.',['EDITORIAL'],'全片中心問題；乾花磨粉不是pollen。','CENTRAL_QUESTION');
ch('花採下來，先跟天氣搶時間');
add('c07d01','先得有能用的粉。公司年表記，一八八六年，上山英一郎收到的美國種子裡，有了除蟲菊。','Medium shot of an anonymous adult opening a plain seed packet on a simple wooden table, morning light.',['K_M'],'1886年種子抵達條目；不是1888舶來粉配方。');
keep('c05r013');keep('c05le001');keep('c05le002');
add('c07d02','我讀到上山英一郎出版的《除虫菊栽培書》，才發現花採下來以後，還有一場趕工。','Medium shot of an anonymous reader studying an old open book beside a shallow basket of flowers, soft window light.',['NDL1897'],'NDL1897書目出版者上山英一郎；作者欄空白，不增造著者。','ATTRIBUTED_HISTORICAL_GUIDANCE');
add('c07d03','一八九七年的第五版，寫的是把鮮花充分乾燥，再做成殺蟲粉；碰到天氣不配合呢？','Close-up of freshly picked daisy flowers spread thinly on a plain drying tray under clouded daylight.',['N25_FAST','N27_RAIN'],'p25殺虫劑製法；天氣條件問題，非某次工廠現場。');
add('c07d19','它給的日曬尺度，是晴天曬上四五天，讓花盡量攤薄；要等到什麼樣子，才收進去？','Close-up of an anonymous worker examining the center of a dried daisy flower above a broad mat, soft sunlight.',['N26_DRY'],'p26右頁乾燥段：花置莚/板、可成薄く、晴天四五日間；收起條件下句揭。');
add('c07d20','書中要求等到花心乾，再收起來；它擔心的是，乾得不充分，磨粉後會變色。','Close-up of an anonymous hand holding a daisy flower with a visibly thick center above a shallow tray, neutral daylight.',['N26_WET','N26_DRY'],'p26乾燥不充分製粉後變色、花心乾則立即收；歷史書中主張，不推現代效力機制。');
add('c07d04','你不妨想像，一小盤花還排得開，盛採時一批接一批，怎麼處理得完？','Wide shot of an anonymous worker carrying a flower basket toward several drying trays, diffuse daylight.',['N27_SCALE'],'明示想像，對應p27多量花與手續負荷，不造實際產量。','EXPLICIT_ILLUSTRATIVE_SCENE');
add('c07d05','書裡說，有人主張陰乾，但花量一多，這套手續難以負荷，所以改求日曬的方便。','Medium shot of an anonymous worker spreading flowers across a broad outdoor mat, mild sunlight.',['N27_SCALE'],'p27左頁下部：菊花陰干、多量花難以應付、日干便。');
add('c07d06','種得多，乾燥的位置和天氣卻得跟得上；我覺得這比有沒有種活，更像一道生產難題。','Wide shot of full flower baskets waiting beside occupied drying mats under a cloudy sky.',['N27_SCALE'],'作者解讀採後處理負荷，不增造產能、成本或藥效結論。','AUTHOR_INTERPRETATION');
add('c07d07','如果雨連著下，花已經在手裡，總不能只等天空放晴；手冊準備了什麼替代辦法？','Medium shot of an anonymous worker looking from a flower basket toward a rain-streaked doorway, cool light.',['N27_RAIN'],'p27霖雨備案，非某日降雨事件。');
add('c07d08','它寫，做一張寬大的竹簾，把花排在上面，再從下方供熱，讓溫暖的室內接手乾燥。','Wide shot of flowers spread on a raised bamboo drying mat in a simple warm drying room, an enclosed heat source below.',['N27_RAIN'],'p27廣き竹簾、其上に菊花、下に火、温室；歷史指導，非現代操作建議。');
add('c07d09','雨天的材料有了去處，趕時間時還能把花切細；書裡說，這樣約兩三小時就能乾。','Close-up of an anonymous worker finely cutting daisy flowers on a wooden board beside a shallow tray, soft side light.',['N25_FAST'],'p25細かく切り、二三時間にて乾燥す；未造實際工廠採行。');
add('c07d10','但快乾不是白拿的好處；出版者緊接著括註，切細後，功能多少會變得稀薄。','Medium close-up of an anonymous reader pausing over a page beside finely cut flowers, calm window light.',['N25_COST'],'p25括註功能多少稀薄となる；當時書中主張，不是現代控制實驗。');
add('c07d11','換成你，整批花等著乾，會先搶處理速度，還是照顧書中在意的功能？','Wide shot of an anonymous worker considering baskets of fresh flowers beside available drying trays, cloudy daylight.',['N25_FAST','N25_COST','N27_SCALE'],'觀眾選擇題依書中取捨提出，不給新機理。','VIEWER_TRADEOFF');
add('c07d12','真正要出售時，書裡的動作換成搗碎和過篩，讓乾花成為細粉。','Close-up of anonymous hands pounding dried flowers in a plain mortar beside a fine sieve, side light.',['N25_SIEVE'],'p25搗粉、篩ひ細粉。');
add('c07d13','篩下來的粉，再裝進袋子或瓶子，花才從田裡的收成，變成可以交到買家手上的貨。','Medium shot of an anonymous worker pouring fine plant powder through a funnel into an unmarked bottle, soft daylight.',['N25_SIEVE'],'p25適宜袋入又は罎入として賣却；後半交付動作解讀。');
add('c07d14','可是一年裡用不完的粉，該怎麼等到下次使用？隨手擱著，也算完成了嗎？','Close-up of an open powder jar and its plain lid resting on a wooden shelf, subdued daylight.',['N25_STORAGE'],'p25使用年內餘分，設保存問題。');
add('c07d15','手冊的答案，是收進瓶或壺裡，密閉存放；做成粉後，保存又接了一棒。','Close-up of an anonymous hand closing the lid of a plain ceramic jar on a shelf, gentle side light.',['N25_STORAGE'],'p25末欄罎又は壺に收め密閉し置く；不接重新焙火恢復功能。');
add('c07d16','這本書也在推銷自家的新鮮粉，抱怨舶來貨有放了兩三年，或混進莖葉粉的情況。','Medium shot of an anonymous seller presenting a small unmarked powder bag beside an old plain sack, daylight.',['N32_OLD'],'p32帶商業立場的自薦/抱怨，不認證整個進口市場。','ATTRIBUTED_SELLER_CLAIM');
add('c07d17','我會把它當成賣家當時在爭的一件事：買到的是什麼粉，又經過怎樣的處理？','Close-up of an anonymous buyer examining a pinch of powder above a plain bowl, soft daylight.',['N32_OLD'],'作者解讀賣家競爭焦點，不認證競品指控。','AUTHOR_INTERPRETATION');
add('c07d18','袋子能裝住粉，卻不能替你安排一整晚的燃燒；要讓粉持續工作，還缺什麼形狀？','Medium shot of a plain powder bag beside an empty incense holder on a small evening table.',['EDITORIAL'],'向前形狀問題，不預揭後段方法。','FORWARD_QUESTION');
ch('粉成了長條，還得盤得出來');
add('c07s01','上山借上了線香的手藝。年表記，一八八八年，他在東京和一位線香商人同宿。','Medium shot of two anonymous adults working with a bamboo tube at a simple bench, warm workshop light.',['K_M'],'1888條目；較早試作，不宣稱1897手冊是1888配方。');
keep('c05r019');keep('c05r020');keep('c05r021');keep('c05r023');keep('c05r024');keep('c05r025');keep('c05r026');
add('c07s02','一八九五年，依金鳥後來的記述，上山的妻子提出了螺旋構想。','Medium shot of an anonymous woman curling a long flexible strand across a small table, soft daylight.',['K_M','NM'],'1895年表與試作木模登錄；匿名概念插圖，不摹真人。');
keep('c05r030');keep('c05r031');keep('c05r032');
add('c07s03','留下的木模，被國立科學博物館登錄為試作品；把原料填進槽裡，就打算推出螺旋。','Close-up of an anonymous hand filling a plain wooden spiral mold on a workshop bench, diffuse light.',['NM','K_T'],'NM910191180001種類試作品、原料填入押出成型；非量產程序。');
keep('c05r036');
add('c07s04','公司年表把專利申請記在一九〇〇年；市售則落在一九〇二年，構想到上市隔了七年。','Medium shot of an anonymous shopkeeper placing plain joined spiral coils on a simple counter, morning light.',['K_M','NM'],'K_M1900出願、1902発売；NM7年後。不假稱已得原申請。');
keep('c05r049');keep('c05r050');
add('c07s05','原廠作者的一篇回顧說，這台設備原先高約兩公尺半，今天保存時，已經橫放下來。','Wide shot of a tall plain antique extrusion machine beside an anonymous adult for scale in a simple workshop, soft window light.',['C591_MACHINE'],'2017p591圖6及正文；示意原立放尺度，不把橫放保存畫成使用姿態。');
keep('c05le004');keep('c05le005');keep('c05r051');keep('c05r052');keep('c05r054');keep('c05r055');keep('c05r058');keep('c05r059');keep('c05r061');
add('c07s06','我看這些留下的商品，最有感的是，長夜終於有了不同的時間刻度；你要等多久，選擇開始不一樣。','Medium shot of an anonymous adult examining two plain historical spiral coils on a small table at dusk.',['K_S'],'作者反應；不同款時數各講一次，不推最早上市時數或效力倍率。','AUTHOR_REACTION');
keep('c05r067');
ch('機器在換，花裡的成分也被拆開');
keep('c05r068');keep('c05r069');keep('c05r071');keep('c05r073');keep('c05r074');keep('c05r076');
add('c07a01','你可能會想，從花裡取出有效成分，跟把整朵乾花磨成粉，到底差在哪裡？','Close-up of a bowl of dried flower powder beside a plain small glass vial, neutral side light.',['M27_EXTRACT'],'乾花原料與抽出製品的角色差異，非當前成品濃度。');
add('c07a02','國立科學博物館的技術報告，列乾花含約百分之一到一點五的除蟲菊素。','Close-up of dried daisy flowers in a plain shallow dish under soft laboratory light.',['M27_EXTRACT'],'p27乾燥花約1–1.5%；不重報1.3%，不當當前配方。');
add('c07a03','同一段寫，用溶劑抽出後，得到的製品可含約百分之二十；被處理的材料，已經不只是乾花。','Medium shot of an anonymous researcher holding a plain glass vial beside a covered dish of dried flowers, gentle light.',['M27_EXTRACT'],'p27石油系溶劑抽出製品約20%；無效力倍率或操作處方。');
add('c07a04','我覺得更容易想錯的，是把那個有效成分，當成一個早就看清楚的單一東西。','Medium close-up of an anonymous researcher studying several small abstract molecular models on a bench, soft light.',['M27_EXTRACT','C592_MIX'],'作者反應，引出天然成分實為混合物。','AUTHOR_REACTION');
add('c07a05','二〇一七年，原廠作者在《化學與工業》回顧，天然除蟲菊素其實是六種成分的混合物。','Close-up of six small differently shaped abstract molecular models arranged together in a plain dish, soft studio light.',['C592_MIX'],'2017化学と工業p592六種酯混合物；不列名稱或當前商品配方。');
add('c07a11','知道有哪幾種，身分就算說清楚了嗎？','Close-up of an anonymous hand examining an asymmetric molecular model under soft laboratory light.',['C592_IDENTITY'],'p592平面與立體身分解明促進後續合成研究；向前問題。');
add('c07a06','研究者已經弄清平面連接方式，卻還有一部分在空間裡怎麼擺，沒有定下來；那一部分要怎麼認？','Close-up of an anonymous hand rotating a simple asymmetric molecular model above a plain paper sheet, laboratory light.',['C592_IDENTITY'],'平面構造與醇部分絕對配置未定的白話說明；不造鏡像效力。');
add('c07a07','一九五八年，勝田純郎等人，讓材料經過化學轉換，接到身分已知的化合物。','Medium shot of an anonymous researcher moving a plain sample vial beside a simple molecular model on a laboratory bench, side light.',['C592_IDENTITY'],'1958醇部分絕對配置，直接導向配置既知物；不是1955導入原因。');
add('c07a08','要追的立體特徵，在轉換中保留下來；沿著這條關係，才判定原來那一部分的立體身分。','Close-up of two simple asymmetric molecular models connected by an anonymous hand holding a small neutral bead, soft light.',['C592_IDENTITY'],'E.Fischer法保持光學活性後轉換，無反應配方或效力結果。');
add('c07a09','文章還刊出保存的實驗筆記照片，圖說標成約那個年代使用；一碗花的功效，背後有這樣細的辨認。','Medium shot of an anonymous researcher writing in an unmarked laboratory notebook beside small plain vials, warm desk light.',['C592_NOTEBOOK'],'圖8再現筆記及1958前後圖說；不假稱翻原全筆記。後半作者感受。');
add('c07a10','這些身分研究，讓後來合成成分的開發往前走；但換了有效成分，植物粉料就可以拿掉了嗎？','Medium shot of an anonymous researcher placing a plain vial beside a large bowl of plant powder on a workbench, soft daylight.',['C592_IDENTITY','K_F'],'p592身分解明後合成研究加速；問現行原料，不稱1958造成1955。');
ch('粉要揉得起來，圓還不能馬上出貨');
keep('c05r091');keep('c05rx005');keep('c05rx007');
add('c07m01','你手上的香體，有負責成形的材料，也有負責殺蟲的成分；我覺得它像一個分工很細的載具。','Medium close-up of an anonymous worker studying a plain green coil beside bowls of plant powder and a small vial, soft workshop light.',['K_F'],'現行組成段的作者解讀；非1897粉袋同批料。','AUTHOR_INTERPRETATION');
keep('c05r092');keep('c5r5a01');keep('c5r5a02');keep('c5r5a03');keep('c5r5a04');keep('c5r5a05');keep('c05le010');keep('c05le023');keep('c5r5a06');keep('c5r5a07');keep('c5r5a08');keep('c5r5a09');
add('c07m02','裝箱讓材料離開工廠，等你拆封時，最後一道交接，卻還在自己的手指上。','Close-up of an anonymous adult opening a plain unmarked box containing joined spiral coils, gentle evening light.',['K_PROCESS_R5','K_Q'],'製程段11–12出貨，向前引入拆卷。','FORWARD_TURN');
add('c07m03','那兩個相連的圓，要怎麼分開，才不會在點火以前就弄壞？','Close-up of anonymous hands hovering over a plain joined pair of green spiral coils on a table, warm side light.',['K_Q'],'現行拆卷QA設問，下一章執行。');
ch('火走向前，成分先離開');
keep('c05r080');keep('c05r081');keep('c05r082');
add('c07u01','我還會留意罐裝附的香盤，那片白墊。你如果以為只是防撞包材，順手抽掉，會怎麼樣？','Close-up of an anonymous hand lifting the edge of a white fibrous mat inside a plain metal incense tray, soft evening light.',['K_Q'],'白墊非緩衝材問答及移除與立消問答。');
add('c07u02','原廠問答說，它是玻璃纖維做的不燃墊，點燃的香就放在上面，是使用時要留下的東西。','Close-up of a plain green incense coil resting on a white fibrous mat inside a shallow metal tray, one glowing tip, side light.',['K_Q'],'白墊問答：玻璃纖維不燃墊、火點線香置上、不要去除。');
add('c07u03','香端如果直接碰到金屬部分，金屬會把熱帶走，就可能讓火熄掉；香體的落腳處，也參與了燃燒。','Close-up conceptual view of a plain coil tip touching the bare rim of a shallow metal tray, a tiny fading ember, neutral side light.',['K_Q'],'上蓋金屬接觸奪熱立消；後半作者解讀。');
add('c07u06','罐裝的蓋子要翻過來，讓白墊朝上，才接住點燃的香；原廠還提醒，要把附的罩子蓋好。','Medium shot of anonymous hands placing the plain protective cover over a coil resting on the white mat in an inverted tin lid, evening light.',['K_Q'],'罐入蓋使用步驟①蓋罩拆下翻轉②白墊側置香③罩蓋上；不是品牌包裝復刻。');
keep('c05r084');keep('c05r085');keep('c05rx004');keep('c05r088');keep('c05r089');keep('c05rx009');keep('c05rx010');keep('c05le012');
add('c07u04','原廠把發紅的燃燒端，標在約攝氏七百度到八百度；成分卻從它前方的香體揮散。','Macro conceptual view of the glowing tip of a plain green incense coil and the intact section ahead, warm glow against a neutral backdrop.',['K_F'],'燃燒端700–800℃、成分由前方揮散；溫度分句給。');
add('c05le013','那個位置離前端約六到八毫米，溫度約攝氏二百五十度，還沒有變成你眼前的灰。','Macro conceptual view of a short intact section just ahead of the glowing tip of a plain incense coil, soft neutral light.',['K_F'],'先端6–8mm、約250℃揮散，後半位置解讀。');
keep('c05le014');keep('c05le015');
add('c07u05','我會把最後一段路留給空氣。你點著以後，位置隨便放，成分就會自己走到每個角落嗎？','Medium close-up of an anonymous adult considering where to place a plain incense tray beside an open window, evening light.',['K_Q'],'以原廠風上放置QA提出位置問題，未預揭結果。','AUTHOR_REACTION_AND_FORWARD_QUESTION');
add('c07u07','原廠問答用煙的擴散範圍，作為有效範圍的線索；把香擺在風的上游，有利成分隨氣流散開。','Wide shot of a plain coil on a lined tray near an open window, faint wisps drifting into a simple room, mild evening light.',['K_Q'],'どれくらいの範囲に効果：煙擴散範圍為目安，風上放置有效行きわたる；不說煙量即藥量。');
add('c07u08','對室內使用，問答也直接要求開窗、保持通風；香體走到房間裡，還得配合實際的使用環境。','Medium shot of an anonymous adult opening a window beside a plain lined incense tray, soft evening light.',['K_Q'],'室內息苦しいQA：必須開窗風通し良い風上；後半使用條件解讀。');
add('c05r101','一把乾花粉末要成為過夜的商品，靠的是讓材料在該留的時候留住，到了使用時，再有節奏地離開。',null,['EDITORIAL','K_F','NDL1897'],'中心答案的作者綜合結論，不重列事件或數字。','SYNTHESIS_ANSWER');
keep('c05r102');keep('c05r103');
const outroScene=scenes.find(s=>s.id==='c05r101');outroScene.lines=rows.filter(r=>['c05r101','c05r102','c05r103'].includes(r.id)).map(r=>({id:r.id,text:r.text,emotion:'親近乾脆，自然說話'}));for(const id of ['c05r102','c05r103'])scenes.splice(scenes.findIndex(s=>s.id===id),1);
const doc=structuredClone(prior);doc.scenes=scenes;
doc.youtube.title='金鳥蚊香憑什麼撐過長夜？一卷香的百年材料難關｜品牌故事';
doc.youtube.description='一把會散的乾花粉末，怎麼變成能陪你過夜的蚊香？沿著金鳥百餘年的材料選擇，從1897年手冊的採後乾燥、細切取捨與存粉，到留下的木模、手卷設備與工廠製程，再走到你拆卷、安放和點火的那一端。不同年代的材料與工法依各自來源說明；歷史場景為原創概念插畫。\n\n參考資料\n'+prior.sources.map(s=>s.title+'\n'+s.url).join('\n')+'\n金鳥工廠製程\nhttps://www.kincho.co.jp/factory/process/process_m.html\n1897年第五版《除虫菊栽培書》\nhttps://dl.ndl.go.jp/pid/1084941\n國立科學博物館《農薬産業技術の系統化調査》\nhttps://sts.kahaku.go.jp/albums/abm.php?d=5029&f=abm00010785.pdf&n=077.pdf\n上山直英〈日本における殺虫剤産業の発祥と発展〉2017\nhttps://www.kincho.co.jp/new/tech/chemical-industry.pdf';
doc.thumbnail.data={...doc.thumbnail.data,headline:'一卷香\n撐整夜',sub:'從乾花到火端',brand:'金鳥',shot:'c05r001'};
doc.sources=[...prior.sources,{title:'金鳥工廠製程',url:'https://www.kincho.co.jp/factory/process/process_m.html',checked_on:'2026-10-25'},...Object.values(research.sources).map(s=>({title:s.title,url:s.url??s.retrieval.url,checked_on:'2026-10-25'}))];
doc.loops=[
['c05r001','c05r059','短時直條的利害，後年螺旋商品給出長夜時間刻度'],['c07o04','c07d08','連雨鮮花的竹簾供熱備案'],['c07o04','c05le013','點火後成分離開的位置'],['c07o06','c05r101','保存成形交付釋放的中心答案'],['c05le001','c05le002','為何用花而非葉莖'],['c07d03','c07d08','天氣不配合的備案'],['c07d19','c07d20','等花心乾才收起，避免書中磨粉後變色問題'],['c07d07','c07d08','連雨用竹簾熱源'],['c07d09','c07d10','切細快乾的書中代價'],['c07d14','c07d15','餘粉密閉保存'],['c07d18','c05r020','粉料獲得燃燒形狀'],['c05r021','c05r025','直條送達前易折'],['c05r026','c05r031','長路徑收進小平面'],['c05r032','c05r036','木模未採量產'],['c05r049','c05r051','押出長條'],['c05le004','c05le005','加水成黏土狀'],['c05r051','c05r052','木片作芯兩條手盤'],['c05r054','c05r055','雙卷運送理由'],['c05r058','c05r059','歷史商品燃燒規格'],['c05r067','c05r069','手卷較晚仍使用'],['c05r071','c05r074','合成成分進展'],['c07a01','c07a03','乾花與抽出製品的材料差異'],['c07a04','c07a05','天然有效成分是混合物'],['c07a11','c07a08','轉成已知物判立體身分'],['c07a10','c05rx005','植物粉料仍負責香體'],['c5r5a01','c5r5a02','少水用重滾筒揉壓'],['c5r5a03','c5r5a04','指痕作柔軟尺度'],['c05le010','c05le023','刀模打出雙螺旋'],['c5r5a07','c5r5a08','成形後等兩天乾燥'],['c07m03','c05r080','按中心拆卷'],['c05r081','c05r082','外緣硬拉易折'],['c07u01','c07u03','保留白墊及金屬奪熱熄火'],['c05r084','c05r085','空隙少氧氣難入而慢燃'],['c05rx004','c05r088','現行一般卷規格'],['c05rx009','c05rx010','微粒進入空氣'],['c05le012','c05le013','前方六至八毫米揮散'],['c05le014','c05le015','燃燒中持續釋放'],['c07u05','c07u07','隨空氣送達的放置條件']
].map(([setup,payoff,what])=>({setup,payoff,what}));
assert.deepEqual(validateVideo(doc),[]);assert.deepEqual(doc.look,{preset:'cute-mystery'});assert.deepEqual(doc.voice,prior.voice);assert.equal(doc.subtitles.burn_in,true);
const idx=new Map(rows.map((r,i)=>[r.id,i]));for(const l of doc.loops)assert(idx.get(l.setup)<idx.get(l.payoff));
const chapterRows=new Map();for(const r of rows)chapterRows.set(r.chapter,[...(chapterRows.get(r.chapter)??[]),r]);assert.equal(chapterRows.size,6);for(const rr of chapterRows.values())assert(rr.some(r=>r.text.includes('你'))&&rr.some(r=>r.text.includes('我')));
const units=rr=>rr.reduce((n,r)=>n+spokenUnits(r.text),0),total=units(rows),opening=units([...chapterRows.values()][0]),outro=units(rows.filter(r=>['c05r101','c05r102','c05r103'].includes(r.id))),body=total-opening-outro;
const changed=rows.filter(r=>oldRows.has(r.id)&&r.text!==oldRows.get(r.id).text),added=rows.filter(r=>!oldRows.has(r.id)),deleted=priorRows.filter(r=>!idx.has(r.id));
const priorTotal=units(priorRows),addedUnits=units(added),deletedUnits=units(deleted),changedDelta=changed.reduce((n,r)=>n+spokenUnits(r.text)-spokenUnits(oldRows.get(r.id).text),0);assert.equal(total,priorTotal+addedUnits-deletedUnits+changedDelta);
const series={...read(path.join(PRIOR,'series.json')),status:'hold_r7_material_journey_pending_independent_source_and_two_fresh_readers',candidate_revision:'length-r7',parent_candidate_video_sha256:R6_SHA,independent_source_review_required:true,two_isolated_narrative_readers_required:true,target_minutes:13};series.names=[...new Set([...series.names,'勝田純郎','上山直英'])];
const brief=['# C05 R7｜一卷香的百年材料旅程','','狀態：HOLD。作者revision R7，下一次真正native讀者panel為round6；R6骨架未送panel。來源、兩名fresh reader、實聲與媒體均未核准。','','### 選項 A：把材料交到長夜裡','','乾花粉末／有效成分→成形→交付→使用，一條材料旅程。主角是材料的工作，不是跨百年同一包粉。1897手冊、歷史工具、2017研究回顧與未標日期的原廠製程各有歸屬。乾花粉末不是花粉pollen。','','## 問題','','一把會散的乾花粉末，憑什麼變成能陪你過夜的商品？','','## 一句答案','','讓材料在該留的時候留住，到了使用時，再有節奏地離開。','','## 站主觀點','','用動作帶出材料取捨：採後乾燥能力、細切快乾的書中代價、篩粉和存粉、手盤與打型，再讓使用者拆卷和安放完成交接。天然成分身分只作為從乾花走向已知成分的一關，不列化學名或商品型錄；1958研究不倒寫成1955導入的原因。','','## 長度與執行規格','', 'native總量'+total+' units；開場'+opening+'；有聲片尾'+outro+'；扣開場與有聲片尾的有效正文'+body+'。4–5units/s算術範圍'+(body/5).toFixed(1)+'–'+(body/4).toFixed(1)+'秒；4.5units/s約'+(body/4.5).toFixed(1)+'秒。不是實聲量測，實聲正文720–840秒仍HOLD，不能慢播或加停頓解除。','','原slug、Sulafat台灣自然語速與技術設定保留。look只有{preset:cute-mystery}、image-01、英文匿名概念插圖，無人名品牌logo或可讀字，不複用史料圖。至少70%插圖、連卡最多3、stillmotion、native每景≤12秒；繁中燒錄及CC。5秒片頭、21秒正式v4片尾僅待執行規格，未造媒體。縮圖layout d，金鳥品牌、黃字黑框主標、白短副標。','','## 未解除的關卡','','需另一位來源QA及兩位fresh readers；不寫verify，不繼承舊SOURCE／敘事PASS。1900原申請、1940導入日誌未取得，不造心理、利潤或逐年試作；界線留claims，不唸查核警語。BASE、canonical、八語、history、reviews與凍結研究不動，付費/provider/後台/git皆零。',''].join('\n');

// Exact text anchors supplement the manually read NDL images and PDF page anchors.
// Text rows refer to cached original bytes; no research source or prior review is rewritten.
const textAnchorSpecs={
 c05r001:[['K_F','1本では40分程度']],
 c07d01:[['K_M','1886年',1]],c05r013:[['K_M','1887年',1]],
 c05le001:[['K_F','殺虫成分（ピレトリン']],c05le002:[['K_F','殺虫成分（ピレトリン']],
 c07s01:[['K_M','1888年',1]],c05r019:[['K_M','舶来のみとり粉']],
 c05r020:[['K_T','仏壇線香の製造法']],c05r021:[['K_M','1890年',3]],
 c05r023:[['K_T','長さ20cm']],c05r024:[['K_T','数本を同時']],c05r025:[['K_F','輸送の途中で折れやすい']],
 c07s02:[['K_M','1895年',1]],c07s03:[['NM','これは試作段階の道具']],c05r036:[['K_T','大量生産に不向き']],
 c07s04:[['K_M','1900年',1],['K_M','1902年',1],['NM','7年後']],
 c05r050:[['K_T','1910年頃']],c05le004:[['NM_MACHINE','粘土状にした塊']],c05le005:[['NM_MACHINE','粘土状にした塊']],
 c05r051:[['NM_MACHINE','粘土状にした塊'],['NM_COIL','一定の長さで']],c05r052:[['NM_COIL','木片の芯']],
 c05r054:[['K_T','ダブルコイル方式']],c05r055:[['K_T','ダブルコイル方式']],
 c05r058:[['K_S','大正8年頃',3]],c05r059:[['K_S','大正8年頃',3]],c05r061:[['K_S','大正11年頃',3]],
 c05r067:[['K_40','1940年',1],['K_T','1957（昭和32）年頃まで使用']],c05r068:[['K_40','1940年',1]],c05r069:[['K_T','1957（昭和32）年頃まで使用']],
 c05r073:[['K_F','食糧増産']],c05r074:[['K_F','1955年頃']],c05r076:[['K_57','1957年',1]],
 c05r091:[['K_F','蚊取線香は、粕粉']],c05rx005:[['K_F','蚊取線香は、粕粉']],c05rx007:[['K_F','蚊取線香は、粕粉']],c07m01:[['K_F','蚊取線香は、粕粉']],
 c05le010:[['NM_MACHINE','クッキーの形抜き']],
 c07m02:[['K_Q','2巻がくっついて']],c07m03:[['K_Q','中心を軽く上下に押']],
 c05r080:[['K_Q','中心を軽く上下に押',1]],c05r081:[['K_Q','端からはずすと折れる']],c05r082:[['K_Q','端からはずすと折れる']],
 c07u01:[['K_Q','緩衝材ではありません'],['K_Q','白いマットを取り除いて']],
 c07u02:[['K_Q','緩衝材ではありません']],c07u03:[['K_Q','熱を奪われて立消え']],
 c07u06:[['K_Q','缶のフタを裏返して',4]],c05r084:[['K_F','線香の断面は']],c05r085:[['K_F','線香の断面は']],
 c05rx004:[['K_Q','レギュラーサイズで約75cm']],c05r088:[['K_Q','レギュラーサイズで約75cm']],c05r089:[['K_Q','燃焼時間は使用環境']],
 c05rx009:[['K_F','極細微粒子として']],c05rx010:[['K_F','極細微粒子として']],c05le012:[['K_F','燃焼部分の温度']],c07u04:[['K_F','燃焼部分の温度']],c05le013:[['K_F','燃焼部分の温度']],
 c05le014:[['K_F','燃焼時間中絶えず']],c05le015:[['K_F','燃焼時間中絶えず']],
 c07u05:[['K_Q','煙の拡がっているところ']],c07u07:[['K_Q','煙の拡がっているところ',2]],c07u08:[['K_Q','必ず窓を開け']]
};
for(const r of claims){
 const specs=textAnchorSpecs[r.id]??[];
 for(const [id,token,after=0]of specs){const src=sourceMap.get(id);assert(src?.text_cache,id);const all=fs.readFileSync(src.text_cache,'utf8'),ls=all.split(/\r?\n/),at=ls.findIndex(l=>l.includes(token));assert(at>=0,id+':'+token);const excerpt=ls.slice(at,at+after+1).join('\n');r.source_anchors.push({source_id:id,text_cache:src.text_cache,text_cache_sha256:sha(all),line_start:at+1,line_end:at+after+1,exact_excerpt:excerpt,excerpt_sha256:sha(excerpt)});}
 if(specs.length&&(!r.locator||r.locator.startsWith('既有r6映射')))r.locator='本句source_anchors所列原文快取精確行號與excerpt SHA；舊審查不繼承。';
}

const bookClaim=claims.find(r=>r.id==='c07d02');bookClaim.source_anchors.push({id:'NDL1897_BIB',source:'NDL1897',record_path:research.sources.NDL1897.record.path,record_sha256:research.sources.NDL1897.record.sha256,title:research.sources.NDL1897.title,publisher:research.sources.NDL1897.publisher,publication_year:research.sources.NDL1897.publication_year,scope:'NDL metadata; publisher credit only, no invented author credit.'});
const editorialKinds={c05r002:'EXPLICIT_IMAGINED_SCENE',c05r026:'FORWARD_QUESTION',c05r030:'GEOMETRIC_ILLUSTRATION',c05r031:'GEOMETRIC_ILLUSTRATION',c05r032:'AUTHOR_REACTION_AND_QUESTION',c05r049:'AUTHOR_FORWARD_QUESTION',c05r071:'AUTHOR_FORWARD_QUESTION',c05r102:'VIEWER_COMMENT_QUESTION',c05r103:'CHANNEL_INVITATION'};
for(const r of claims)if(editorialKinds[r.id]){r.claim_kind=editorialKinds[r.id];if(!r.source_anchors.length)r.locator='明示想像、幾何示意、作者反應或向前問題；不主張新增歷史事實。';}
write('video.json',doc);write('narration-only.json',rows);write('series.json',series);fs.writeFileSync(path.join(OUT,'brief.md'),brief);
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_REVIEW_HOLD',candidate_revision:'length-r7',author:'/root/c05_material_author',parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:R6_SHA,frozen_expansion_research:{markdown_sha256:fileSha(path.join(RESEARCH,'research.md')),claims_sha256:fileSha(path.join(RESEARCH,'claims.json')),receipts_sha256:fileSha(path.join(RESEARCH,'source-receipts.json'))},source_caveats:priorClaims.source_caveats_moved_out_of_narration,rows:claims});
const script=['# '+doc.youtube.title,'','作者R7材料旅程；HOLD，待獨立來源QA及兩fresh readers。下一次native panel為round6；實聲未量。ID不讀入旁白。',''];let last='';for(const r of rows){if(r.chapter!==last){last=r.chapter;script.push('## '+r.chapter,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C05 R7逐句主張與來源錨點','','全部PENDING_INDEPENDENT_REVIEW；無作者SOURCE或敘事PASS。','','| ID | 類型 | 旁白 | 來源 | 定位 |','| --- | --- | --- | --- | --- |'];for(const r of claims)cm.push('| '+r.id+' | '+r.claim_kind+' | '+r.claim+' | '+r.source_ids.join(', ')+' | '+r.locator+' |');for(const r of claims.filter(r=>r.source_anchors.length)){cm.push('','## '+r.id,'');for(const a of r.source_anchors)cm.push('- '+JSON.stringify(a));}cm.push('','## 範圍界線','','乾花粉末不是pollen。1897手冊是歷史指導與帶商業立場的主張，非現代控制藥效實驗或1888/1902工廠逐批記錄。乾花1–1.5%與抽出製品20%不是當前香體配方或效力倍率。1958不是1955的原因。現代粉料與工法不回填早期。1900原申請、1940導入日誌仍缺；不造產量利潤心理或全產業交棒日。2017筆記照片不等於已讀原全筆記，不複用史料圖。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
write('revision-edits.json',{revision:7,author_revision_label:'R7',next_actual_native_panel_round:6,r6_was_not_panelled:true,prior_video_sha256:R6_SHA,single_promise:rows.find(r=>r.id==='c07o05').text,added:added.map(r=>({...r,spoken_units:spokenUnits(r.text)})),changed:changed.map(r=>({id:r.id,before:oldRows.get(r.id).text,after:r.text,spoken_unit_delta:spokenUnits(r.text)-spokenUnits(oldRows.get(r.id).text)})),deleted:deleted.map(r=>({...r,spoken_units:spokenUnits(r.text)})),loops:doc.loops});
const project=loadProject({root:ROOT,slug:SLUG}),context={canonical_root:ROOT,canonical_video_sha256:fileSha(project.file),initialized_lexicon_sha256:sha(JSON.stringify(project.lexicon)),shelf_lexicon_sha256:sha(JSON.stringify(project.shelfLexicon)),in_memory_substitution_only:['doc','brief','series'],canonical_files_written:false};project.doc=doc;project.brief=brief;project.series=series;
const lint=lintProject(project),timeline=estimateTimeline(doc),shotEstimates=timeline.scenes.filter(s=>doc.scenes.find(t=>t.id===s.id)?.template==='shot').map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS})),maxShot=Math.max(...shotEstimates.map(s=>s.seconds)),cadence=lint.warnings.filter(w=>/no open loop|open loops? planted|condensation plants/.test(w.message));
const files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs','revision-edits.json'];for(const f of protectedFiles)assert.equal(fileSha(f),protectedBefore[f],f);
const notes={status:'HOLD_PENDING_INDEPENDENT_SOURCE_AND_TWO_FRESH_READERS',candidate_revision:'length-r7',author:'/root/c05_material_author',next_actual_native_panel_round:6,r6_skeleton_was_not_panelled:true,parent_source_video_sha256:BASE_SHA,parent_candidate_video_sha256:R6_SHA,independent_source_review:'PENDING_OTHER_REVIEWER',narrative_review:'PENDING_TWO_FRESH_READERS',verify_written:false,source_pass_claimed:false,narrative_pass_claimed:false,native_units:{counter:'spokenUnits(spokenText(line))',r6_total:priorTotal,r6_opening:183,r6_body_excluding_opening:1985,r6_effective_body_excluding_opening_and_outro:1895,r7_total:total,opening,outro,body_excluding_opening:total-opening,effective_body_excluding_opening_and_outro:body,net_effective_body_delta_from_r6:body-1895,added_units:addedUnits,deleted_units:deletedUnits,changed_unit_delta:changedDelta,net_total_delta:total-priorTotal,target_actual_body_seconds:[720,840],normal_4_to_5_units_per_second_body_seconds_range:[body/5,body/4],at_4_5_units_per_second:body/4.5,actual_tts_seconds:null,actual_duration_verified:false,length_hold:true,range_is_arithmetic_not_measured_tts:true},counts:{lines:rows.length,scenes:scenes.length,chapters:chapterRows.size,illustrations:scenes.filter(s=>s.template==='shot').length,cards:scenes.filter(s=>s.template!=='shot').length,loops:doc.loops.length,added_lines:added.length,changed_lines:changed.length,deleted_lines:deleted.length},delta_from_r6:{added:added.map(r=>r.id),changed:changed.map(r=>r.id),deleted:deleted.map(r=>r.id)},native_initialized_context_lint:{context,scope:'author mechanical validation, not independent source/narrative/runtime approval',result:lint,errors:lint.errors.length,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot,all_estimated_shots_at_most_12_seconds:maxShot<=12},visual_spec:{image_model:'image-01',look_exact:true,voice_exact:true,stillmotion:true,illustration_unit_share:[...eachLine(doc)].filter(x=>x.scene.template==='shot').reduce((n,x)=>n+spokenUnits(spokenText(x.line)),0)/total,planned_branding:{intro_seconds:5,outro_seconds:21,outro_version:'formal-v4',executed:false},thumbnail:{layout:'d',brand:'金鳥',headline_style:'yellow with black outline',subtitle_style:'short white'},burn_in_zh_tw:true,cc_zh_tw:true,actual_generated_media_reviewed:false},file_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(OUT,f))])),protected_files_unchanged:true,paid_calls:0,provider_calls:0,backend_writes:0,git_commands:0,canonical_written:false};
notes.frozen_at_utc=new Date().toISOString();notes.core_four_sha256=Object.fromEntries(['video.json','brief.md','series.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));notes.author_ready_for_independent_review=true;notes.opening_native_units=opening;notes.opening_arithmetic_seconds_at_4_to_5=[opening/5,opening/4];notes.metadata_changed=['youtube.title','youtube.description','thumbnail.data.headline','thumbnail.data.sub','sources','series.names','chapter titles'];notes.at_least_eight_concrete_action_payoffs_for_fresh_review=doc.loops.filter(l=>['c07d07','c07d19','c07d09','c07d14','c05r032','c05le004','c05r051','c05r054','c5r5a01','c5r5a03','c5r5a07','c07m03','c07u01','c05le012'].includes(l.setup)).map(l=>({...l,status:'AUTHOR_INTENT_PENDING_INDEPENDENT_JUDGMENT'}));
write('author-notes.json',notes);
console.log(JSON.stringify({revision:'length-r7',status:notes.status,counts:notes.counts,native_units:notes.native_units,lint_errors:lint.errors,cadence_warnings:cadence,lint_warning_count:lint.warnings.length,maximum_estimated_shot_seconds:maxShot,file_sha256:notes.file_sha256},null,2));
assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));assert.equal(cadence.length,0,JSON.stringify(cadence));assert(maxShot<=12,JSON.stringify(shotEstimates.filter(s=>s.seconds>12)));
