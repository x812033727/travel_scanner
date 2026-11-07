import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {validateVideo} from '/workspace/work/brand-remakes-source/tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS} from '/workspace/work/brand-remakes-source/tools/video/core/timeline.mjs';
import {loadProject,lintProject} from '/workspace/work/brand-remakes-source/tools/video/core/state.mjs';

const OUT=path.dirname(fileURLToPath(import.meta.url));
const REPO='/workspace/work/brand-remakes-source';
const SLUG='story-everyday-frixion-c15-remake-20261025';
const RUNTIME='/workspace/work/brand-story-20261025/c15-submission-root';
const sha=x=>createHash('sha256').update(x).digest('hex');
const fileSha=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8'));
const put=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const RESEARCH_SHA={
 'research-original.md':'275f3c5cf2b105abc26c606bc5a9cd609c4735409939f236a47372fbdbc5b6b7',
 'research-original.claims.json':'84da190bb348d86ac83ef86ad2430d80a035af4386e04bcc4d014a58a9d5b52f',
 'original-preservation.json':'031d38bcb119734c6f32e00ce4e5308805236c16b339df29198e27d3657ec316'
};
for(const[f,h]of Object.entries(RESEARCH_SHA))assert.equal(fileSha(path.join(OUT,f)),h,f);
const research=read(path.join(OUT,'research-original.claims.json'));
const preservation=read(path.join(OUT,'original-preservation.json'));
const protectedFiles=preservation.files.flatMap(f=>[{path:f.path,sha256:f.sha256},{path:f.snapshot,sha256:f.snapshot_sha256}]);
for(const f of protectedFiles)assert.equal(fileSha(f.path),f.sha256,f.path);
const sources=new Map(research.sources.map(s=>[s.id,s]));
const anchors=new Map(research.evidence_anchors.map(a=>[a.id,a]));
const facts=new Map(research.claims.map(c=>[c.id,c]));
const voiceFile=path.join(REPO,'docs/videos/brand-story-remakes-20261025/c06/video.json');
const voice=structuredClone(read(voiceFile).voice),voiceSHA=fileSha(voiceFile);
const scenes=[],rows=[],claims=[];let chapter='';
const cameras=['push in','pan left','pull out','pan right','tilt down','tilt up','drift'];
function ch(t){chapter=t;}
function add(id,text,prompt,refs=[],kind='SOURCED_FACT',context=''){
 const scene={id,template:'shot',data:{prompt,visual:'still',camera:cameras[scenes.length%cameras.length]},lines:[{id,text,emotion:'對一位觀眾說書，自然起伏，關鍵數字和來源歸屬讀清楚'}]};
 if(!rows.length||rows.at(-1).chapter!==chapter)scene.chapter=chapter;
 scenes.push(scene);rows.push({chapter,id,text});
 const ff=refs.map(x=>{assert(facts.has(x),x);return facts.get(x);});
 const aa=[...new Set(ff.flatMap(f=>f.evidence_anchor_ids))];
 claims.push({id,chapter,claim:text,claim_kind:kind,status:'PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW',research_claim_ids:refs,anchor_ids:aa,source_ids:[...new Set(aa.map(a=>{assert(anchors.has(a),a);return anchors.get(a).source_id;}))],limits:[...new Set(ff.map(f=>f.does_not_support))],author_context:context,visual_prompt:prompt,visual_kind:'ORIGINAL_ANONYMOUS_CONCEPT_ILLUSTRATION_NOT_ARCHIVAL_REENACTMENT'});
}

ch('顧客把筆翻過來');
add('c15r1h01','你剛改好的一頁筆記，若紙張到了六十度，還能留下哪一版？','Close-up at a plain writing desk, an anonymous adult holding a corrected draft sheet with a few abstract nonlinguistic marks, soft side light.',['F05','F31'],'VIEWER_CONDITIONAL_STAKE_WITH_SOURCED_TEMPERATURE','六十度為現行廠方消色條件；未說本片實測、任意桌面已達該溫或先揭回色結果。');
add('c15r1h02','PILOT的營業人員後來回憶，日本一家文具專門店試賣時，顧客親手寫，接著拿膠擦去擦。','Medium shot inside a small stationery shop, an anonymous customer rubbing an abstract ink stroke on a sample sheet with the plain eraser end of a pen, mild window light.',['F27'],'ATTRIBUTED_RETAIL_ACTION_SCENE','只使用後來受訪者所述日本文具專門店試賣，不補店名、試賣日、顧客原話或特定長相。');
add('c15r1h03','我覺得，這個動作比廣告更難交代：筆尖剛留下的東西，怎麼交給另一端處理？','Close-up of an anonymous customer turning a plain pen between its writing tip and eraser end above one sample sheet, soft interior light.',['F01','F27'],'AUTHOR_REACTION');
add('c15r1h04','它的背後，還有等著離開小燒杯的一批膠囊；而寫完的那張紙，溫度也有機會再插手。','Medium shot of an anonymous laboratory worker holding a small plain beaker beside an unmarked container, diffuse light.',['F24','F25','F32'],'TWO_OUTCOME_FREE_TEASERS','預告量產與後續低溫介入，均不給結果。');
add('c15r1h05','跟著FriXion的一筆修改，追過三十多年的變色研究，看它怎麼走到你手裡。','Medium shot at a writing desk, an anonymous adult holding one plain capped pen above a draft sheet, gentle desk lamp light.',['F10','F25','F26'],'SINGLE_NAMED_PROMISE','研究三十多年為原廠開發回顧的規模，非精確起訖年差或同一配方跨期不變。');
add('c15r1h06','同一支筆寫、消、再寫，究竟把什麼留在紙上，又把什麼交給了溫度？','Close-up at a plain desk, an anonymous hand poised with a pen above overlapping abstract curved marks on one sheet, soft light.',['F01','F07','F09','F33'],'CENTRAL_QUESTION');

ch('同一個位置重新落筆');
add('c15r1a01','想像你正在改一份草稿，先用這支筆劃下一道線；真正要擦之前，手得先停一下。','Medium shot at a home desk, an anonymous writer lifting a plain pen after drawing one abstract curved stroke, mild window light.',['F01'],'EXPLICIT_VIEWER_ILLUSTRATION','現行用法的明示假設示意，不編2006首批顧客的實測。');
add('c15r1a02','現行說明要求，等筆跡乾了，再讓附屬的專用膠擦接觸紙面。','Close-up at a writing desk, an anonymous hand holding the plain eraser end just above a dry abstract ink stroke, soft side light.',['F01']);
add('c15a02b1','接觸紙面的那塊材料，又是怎麼選出來的？','Close-up at a product workbench, an anonymous worker examining the plain eraser end of a pen between two fingers, soft light.',['F08'],'FORWARD_MATERIAL_QUESTION');
add('c15a02c1','千賀談到選材時，說要有彈性，還要耐磨；膠擦本身也得承受一次次使用。','Medium shot at a product workbench, an anonymous worker gently pressing a plain pen eraser with a fingertip, diffuse light.',['F08'],'ATTRIBUTED_DEVELOPER_SELECTION_GOAL','彈性與耐磨為選材意圖，非本片耐久試驗或所有紙張絕無損傷保證。');
add('c15r1a03','如果你只看見擦這個動作，很容易把它當成另一種橡皮；它到底移走了什麼？','Medium close-up at a desk, an anonymous adult examining a plain pen eraser beside an ordinary eraser, diffuse light.',['F05','F06'],'AUTHOR_INTERPRETATION');
add('c15r1a04','專用膠擦來回摩擦，熱傳進筆跡，墨水便朝無色的狀態改變。','Close-up at a plain desk, an anonymous hand rubbing a dry abstract ink arc with a plain pen eraser, soft light.',['F05','F06']);
add('c15r1a05','開場問的那個溫度，正是現行墨水說明所列的消色門檻。','Medium close-up at a writing desk, an anonymous adult examining the rubbed area of a sheet under a desk lamp, neutral light.',['F05'],'ATTRIBUTED_CURRENT_PRODUCT_CONDITION','只讀現行原頁條件；無紙面到溫秒數或每代精確值，不與2017約65度平均。');
add('c15r1a06','紙面沒有跟著掉下一堆消字屑；熱能傳到紙纖維裡的筆跡，也能讓那裡變得無色。','Close-up at a writing desk, an anonymous fingertip pointing toward a clean rubbed area on a sheet with a few abstract marks nearby, gentle light.',['F06'],'ATTRIBUTED_MANUFACTURER_MECHANISM','無消字屑與紙纖維消色為原廠說明；不擴成所有紙張絕無損傷。');
add('c15r1a07','所以，剛才那個位置接下來能做什麼？','Close-up of an anonymous hand moving a plain writing tip toward the rubbed area of a draft sheet, mild light.',['F07'],'FORWARD_ACTION_QUESTION');
add('c15r1a08','你把筆轉回來，在消色處重新落筆，同一個位置就能寫上新的內容。','Medium shot at a desk, an anonymous writer drawing a new abstract stroke in a rubbed patch of paper, soft window light.',['F07'],'EXPLICIT_VIEWER_ILLUSTRATION','示意原廠所述原位重寫，不承諾紙張無限次耐擦。');
add('c15r1a09','我喜歡這裡的省事：修改不必搬到紙張的旁邊，也不用另外拉一條線，替新內容找位置。','Medium shot of an anonymous writer looking at a small corrected area within a plain draft sheet, gentle light.',['F07'],'AUTHOR_REACTION','由原位重寫的使用意義作作者解讀，不宣稱所有人的偏好。');
add('c15r1a10','但如果只是把顏色藏起來，為什麼你放開手之後，舊線沒有立刻再冒出來？','Close-up of an anonymous hand resting beside a rubbed patch and a fresh abstract ink curve on the same sheet, soft side light.',['F09'],'FORWARD_STATE_QUESTION');
add('c15r1a11','這個問題，得縮到筆跡裡去看。擔任色材的，是一顆顆微膠囊。','Medium close-up at a laboratory desk, an anonymous researcher examining a simple enlarged capsule model beside a plain pen, diffuse light.',['F02'],'CONCEPTUAL_MODEL','放大模型非真實比例顯微照片，不作零售剖面重建。');
add('c15r1a12','每個膠囊裡，裝著決定顏色的成分、使它顯色的成分，還有調整變色溫度的材料。','Close-up at a laboratory bench, an anonymous researcher holding a simple intact capsule model containing three different abstract shapes, soft light.',['F02']);
add('c15r1a13','這三種工作，被放在同一個小空間裡；光有決定黑、紅等顏色的染料，就能顯色嗎？','Medium shot at a laboratory bench, an anonymous worker pointing to a pale abstract component within an intact capsule model, mild light.',['F02','F03'],'CONCEPTUAL_MODEL','三類功能不等於恰好三種化學物；模型形狀非分子結構。');
add('c15r1a14','開發者千賀邦行解釋，那種染料與顯色劑結合，才會顯出黑、紅等顏色。','Close-up at a laboratory desk, an anonymous researcher bringing two small abstract pieces together within a simple intact capsule model, diffuse light.',['F03'],'ATTRIBUTED_DEVELOPER_EXPLANATION');
add('c15r1a15','而調整劑會介入這個組合，決定溫度變到哪裡時，顏色跟著換一個狀態。','Medium close-up at a bench, an anonymous researcher adjusting a third abstract component beside two joined pieces in an intact capsule model, soft light.',['F02','F04'],'ATTRIBUTED_CONCEPTUAL_MECHANISM','不補酸鹼/氧化還原/零售分子式；不以膠囊破裂表達消色。');
add('c15r1a16','你剛才用膠擦提供的熱，就是改變這種組合的入口；可它並不會替你一直加熱。','Medium shot at a writing desk, an anonymous hand setting a plain pen beside a corrected draft, soft side light.',['F04','F09'],'CAUSAL_LINK_TO_VIEWER_ACTION');
add('c15r1a17','要讓手停下來後的修改留下，材料還需要一種特性：回到室溫，仍維持剛變過的樣子。','Close-up at a desk, an anonymous adult observing the same corrected sheet with both hands resting away from it, gentle window light.',['F09'],'NEW_STATE_REQUIREMENT');
add('c15r1a18','這種能把狀態留下的材料，是怎麼從只會變色，走到能供人修改？','Medium shot at a laboratory desk, an anonymous researcher looking between a plain cup and a simple pen, diffuse light.',['F09','F12','F14'],'FORWARD_MATERIAL_HISTORY_QUESTION');

ch('冷水改了杯子，墨水得記住改變');
add('c15r1b01','PILOT在二〇二四年的回顧裡，把變色研究的靈感，放在一九七〇年的秋天。','Medium shot at a modest laboratory desk, an anonymous researcher observing a leaf beside a small glass test tube, overcast window light.',['F10'],'ATTRIBUTED_LATER_COMPANY_HISTORY','不補研究員姓名、逐字台詞、地點或精確發現日；不聲稱全球首創。');
add('c15r1b02','研究者看見紅葉，想把那種顏色變化做進試管，於是著手尋找能變色的墨水。','Medium close-up at a laboratory bench, an anonymous researcher holding a plain test tube beside a leaf, mild side light.',['F10'],'ATTRIBUTED_LATER_COMPANY_HISTORY','Metamo名稱在J1回顧原文；不將紅葉自然機理當墨水機理。');
add('c15r1b03','一九七六年，公司推出加冷水就會變色的紙杯，讓人把水倒進去，看杯子的外觀改變。','Medium shot at a table, an anonymous adult pouring cold water from a plain jug into a paper cup with a simple abstract patch, soft light.',['F12'],'ATTRIBUTED_PRODUCT_ACTION','匿名示意，不仿當年特定圖案、不推定顯退色方向或與筆用配方相同。');
add('c15r1b04','你若拿著這種杯子，變化就是它要交給你的效果；寫在草稿上的字，要求卻不一樣。','Medium close-up at a table, an anonymous adult looking from a plain paper cup toward a draft sheet with abstract marks, mild light.',['F12','F09'],'AUTHOR_INTERPRETATION');
add('c15r1b05','我覺得難處正在這裡：能表演變化以後，研究得先把哪個分界改清楚？','Medium shot at a desk, an anonymous writer watching a corrected patch on a draft sheet, gentle desk lamp light.',['F09','F13'],'AUTHOR_REACTION');
add('c15r1b06','早期材料升溫時慢慢變色，放著又會回色，連改變的分界也不夠清楚。','Close-up at a laboratory bench, an anonymous researcher comparing two plain sample swatches with faint and darker abstract patches, diffuse light.',['F13'],'ATTRIBUTED_LATER_COMPANY_HISTORY');
add('c15r1b07','於是，團隊先把調整劑改得更敏感：到某個溫度，顏色迅速改變。','Medium shot at a laboratory bench, an anonymous researcher lifting a small sample strip beside an unmarked warm container, soft light.',['F14']);
add('c15r1b08','這一型降到接近那個溫度以下，也很快回色；變得俐落了，卻還留不住一次改動。','Close-up of an anonymous researcher comparing a cooled plain sample strip with a warm sample strip on a bench, neutral light.',['F14'],'CAUSAL_INTERPRETATION_OF_HISTORICAL_MATERIAL');
add('c15r1b09','如果要讓你停手後的修改不馬上翻回去，變色與回色，能不能分開發生？','Medium close-up at a laboratory desk, an anonymous researcher moving two plain sample trays farther apart, diffuse light.',['F09','F14'],'FORWARD_MATERIAL_QUESTION');
add('c15r1b10','開發接著轉向記憶型：加熱變過色，必須再冷到另一個更低的設定溫度，才會回色。','Medium shot at a bench, an anonymous researcher transferring an intact plain sample vial from a warm tray toward a cool tray, soft light.',['F09','F14']);
add('c15r1b11','同樣回到室溫，原本有色的可以有色，已經變成無色的，也能保持無色。','Close-up at a laboratory desk, an anonymous researcher placing a colored sample and a clear sample side by side at rest, mild light.',['F09']);
add('c15r1b12','剛才那道舊線沒有立刻回來的疑問，到早期記憶型裡，兩端曾被隔開多遠？','Close-up at a writing desk, an anonymous adult examining a rubbed patch beside a fresh abstract mark without touching the paper, soft light.',['F09'],'NAMED_CALLBACK_WITH_NEW_CAUSAL_ANSWER');
add('c15r1b13','公司記錄一九八八年能在約二十度的溫差間保持色態；再拉開，該怎麼找調整劑？','Medium shot at a laboratory bench, an anonymous researcher arranging two plain sample vials beside a simple unnumbered temperature instrument, diffuse light.',['F14'],'ATTRIBUTED_HISTORICAL_TEMPERATURE_SPAN','二十度是該歷史階段變色/回色的差，不是現售筆門檻或室溫。');
add('c15r1b14','那個差距，來自調整劑的選擇；千賀回憶，起步時用的是已經存在的物質。','Medium close-up at a laboratory desk, an anonymous researcher selecting one small plain vial from a modest rack, gentle light.',['F15'],'ATTRIBUTED_DEVELOPER_RECOLLECTION');
add('c15r1b15','後來，團隊自己製作超過一千種原創化合物，尋找想要的變色溫度調整劑。','Medium shot at a laboratory bench, an anonymous researcher placing a newly prepared plain vial into a rack of unmarked samples, mild light.',['F15'],'ATTRIBUTED_DEVELOPER_RECOLLECTION','一千種為化合物種類，不是試驗次數、研究員數或一次同時出現的瓶數。');
add('c15r1b16','但要把這些材料交到你寫字的那一端，光把溫度範圍拉開，還過不了筆尖。','Close-up at a laboratory desk, an anonymous hand holding an enlarged plain pen-tip model beside intact capsule models, diffuse light.',['F16','F19'],'FORWARD_PHYSICAL_CONSTRAINT');
add('c15r1b17','那些負責變色的小膠囊，當時大到什麼程度？','Medium close-up at a workbench, an anonymous researcher comparing differently sized intact capsule models beside a plain pen tip, soft light.',['F16'],'FORWARD_SIZE_QUESTION');

ch('膠囊縮小，筆跡卻還有顏色');
add('c15r1c01','依原廠回顧，初期膠囊直徑約十到十五微米；到了記憶型階段，縮到五到十微米。','Close-up at a laboratory desk, an anonymous researcher placing larger and smaller intact capsule models into two plain trays, soft side light.',['F16'],'ATTRIBUTED_HISTORICAL_SIZES','歷史研發尺寸，不是現售全色規格；放大圖無比例。');
add('c15r1c02','可是，墨水要從原子筆尖細小的間隙順暢出去，那時的膠囊仍然太大。','Medium close-up at a workbench, an anonymous technician holding an enlarged simple pen-tip model beside a large intact capsule model, neutral light.',['F16']);
add('c15r1c03','你在紙上只想劃一條細線，裡面的色材，卻必須連自己的外殼一起通過。','Close-up at a writing desk, an anonymous hand guiding a plain pen above a single fine abstract curve, mild window light.',['F02','F16'],'VIEWER_CAUSAL_INTERPRETATION');
add('c15r1c04','我沒想到，膠囊縮小，膜卻變薄、更容易破裂；除了薄，墨水還會帶來什麼？','Medium shot at a laboratory bench, an anonymous researcher carefully holding a small intact capsule model beside a larger model, soft light.',['F17'],'AUTHOR_REACTION_WITH_SOURCED_FAILURE_CONSTRAINT');
add('c15r1c05','研究得同時處理尺寸和膜材，不能讓色材到了能過筆尖的大小，就失去實用的強度。','Medium close-up at a laboratory desk, an anonymous researcher examining an intact tiny capsule model through a simple magnifier, diffuse light.',['F17']);
add('c15r1c06','而膠囊進入墨水，還會碰到溶劑與添加物；千賀說，其中許多與膠囊相容性不好。','Medium shot at a laboratory bench, an anonymous researcher adding an unmarked liquid toward a plain sample beaker with a dropper, soft light.',['F18'],'ATTRIBUTED_DEVELOPER_RECOLLECTION','不指定液體名稱、濃度或真實零售配方，不演示自行配墨。');
add('c15r1c07','所以膜不只要夠強，還得耐受這些成分；團隊連包覆的方法與條件，也一起研究。','Close-up at a laboratory desk, an anonymous researcher lifting a plain sample vial beside an intact capsule model, mild light.',['F18']);
add('c15r1c08','二〇〇〇年代初，膠囊縮到約二到三微米，能用於筆具墨水；先走出哪支筆？','Medium shot at a laboratory bench, an anonymous researcher moving a much smaller intact capsule model toward an enlarged plain pen-tip model, diffuse light.',['F19'],'ATTRIBUTED_DATE_RANGE','J1記2001、D2記2002；採兩來源共同年代範圍，不掩掉差異，不說所有工廠已量產。');
add('c15r1c09','筆尖這一關跨過後，二〇〇二年出現了一支名叫ILLUSION的裝飾筆。','Medium shot at a stationery counter, an anonymous adult lifting a plain capped pen beside a sheet with an abstract dark stroke, soft interior light.',['F20']);
add('c15r1c10','它寫下黑色的筆跡，再用筆帽上的專用膠擦摩擦，黑色會變成另一種顏色。','Close-up at a desk, an anonymous hand rubbing a dark abstract ink arc with the eraser on a plain pen cap, a contrasting colored arc nearby, soft light.',['F20'],'HISTORICAL_SPECIFIC_PRODUCT_ACTION','當年膠擦在筆帽；變另一色不是變透明，不說與現行筆同配方或同一實體。');
add('c15r1c11','可是，如果你想改掉一個錯字，換一種顏色，還是把舊筆跡留在原來的位置。','Medium close-up at a desk, an anonymous writer examining a colored abstract stroke in the middle of a draft sheet, mild light.',['F20','F21'],'VIEWER_USE_CASE_INTERPRETATION');
add('c15r1c12','歐洲子公司的行銷人員看見這支筆後，向開發負責人提出：能不能從有色，變成透明？','Medium shot in a plain product room, one anonymous product worker examining a capped pen beside a sample sheet, diffuse light.',['F21'],'ATTRIBUTED_LATER_COMPANY_ACCOUNT','間接轉述，不造精確對話日、地點或當事人長相，不把2002產品年硬當談話年。');
add('c15r1c13','這個要求，把變色從紙上的裝飾，推向了同一頁的修改。','Close-up at a writing desk, an anonymous adult holding a plain pen above a small empty patch within abstract draft marks, gentle light.',['F21','F22'],'AUTHOR_INTERPRETATION');
add('c15r1c14','公司以法國的用筆情境解釋：某些墨水可用消字液處理，原筆還能接著寫嗎？','Medium shot at a desk, an anonymous adult placing a plain ink pen beside an unmarked ink-removal applicator, soft light.',['F22'],'ATTRIBUTED_SPECIFIC_USE_CONTEXT','限定公司敘述的特定消字液情境，不泛指所有修正帶/液、所有歐洲人或現行法規。');
add('c15r1c15','但消字液浸過的地方，不能再由原來那支筆重寫，得另拿一支專用筆。','Close-up at a writing desk, an anonymous hand reaching for a second plain writing tool beside a treated patch on a sheet, mild light.',['F22'],'ATTRIBUTED_SPECIFIC_USE_CONTEXT');
add('c15r1c16','假設你只是想改同一行，桌上卻要接連交棒：寫、消，再換工具補上去。','Medium close-up at a desk, an anonymous adult arranging three plain writing and erasing tools beside one draft sheet, gentle light.',['F22'],'EXPLICIT_VIEWER_ILLUSTRATION','限定上述原廠情境，非普遍三支筆需求。');
add('c15r1c17','FriXion要接下原位重寫，但有色轉無色要站得住，還得經得起哪段日常溫差？','Medium shot at a laboratory desk, an anonymous researcher holding a plain pen beside sample sheets and unmarked sample containers, diffuse light.',['F21','F22','F23'],'FORWARD_STABILITY_REQUIREMENT');
add('c15r1c18','研究回顧記下，當時那段溫域曾擴到零至四十度；若環境跨出去，色態就可能跟著變。','Close-up at a laboratory bench, an anonymous worker inspecting a plain sample strip beside an unnumbered temperature instrument, soft light.',['F23'],'ATTRIBUTED_HISTORICAL_RANGE','歷史研發溫域非現售校正曲線，不說任何季節一定到墨水門檻。');
add('c15r1c19','後來的新調整劑，把這個歷史研發範圍，拉到零下二十至六十五度，相隔八十五度。','Medium close-up at a laboratory desk, an anonymous researcher separating two plain sample trays with a small vial between them, diffuse light.',['F23'],'ATTRIBUTED_HISTORICAL_RANGE','保留J2研發跨度，不與現行FAQ60度等同，非專利ΔH定義或全色零售保證。');
add('c15r1c20','調整的目標，是讓一般使用環境裡的色態穩定；接下來，得把實驗室這一小份，真的做成商品。','Medium shot in a laboratory doorway, an anonymous worker carrying a small plain sample beaker toward a work area, mild light.',['F23','F24'],'FORWARD_SCALE_TRANSITION');

ch('小燒杯得接上五百公斤');
add('c15r1d01','二〇〇四年，公司決定商品化，專案正式啟動；研究室與工廠開始追同一個品質。','Wide shot at a simple production workbench, an anonymous technician examining a small plain sample jar beside a large unmarked vessel, diffuse light.',['F24'],'ATTRIBUTED_LATER_COMPANY_ACCOUNT');
add('c15r1d02','你能在燒杯裡做出一次變色，換到大量生產時，還能得到同樣的墨水嗎？','Medium close-up at a workbench, an anonymous technician comparing a small plain beaker with a large unmarked vessel, soft light.',['F24','F25'],'VIEWER_CAUSAL_INTERPRETATION');
add('c15r1d03','開場那批等著離開燒杯的膠囊，到了千賀的量產回憶裡，數量是五百公斤。','Medium shot in a plain production room, an anonymous technician standing beside a large unmarked capsule-material container and a small sample jar, mild light.',['F25'],'NAMED_CALLBACK_WITH_NEW_SCALE','五百公斤為訪談所述需穩定生產的膠囊量，非每日、年產能、單支含量或本片實秤。');
add('c15r1d04','這一關得建立穩定生產膠囊的技術；放大以後，還多出了哪些小燒杯沒有的問題？','Medium shot at a production bench, an anonymous technician taking a small sample from an unmarked container, soft overhead light.',['F25'],'ATTRIBUTED_DEVELOPER_RECOLLECTION');
add('c15r1d05','其中一項，是膠囊做成墨水後，會出現分離或劣化；不是膠囊能做出來，事情就結束。','Close-up at a laboratory workbench, an anonymous technician examining a plain vial with distinct liquid layers beside another sample, diffuse light.',['F25'],'ATTRIBUTED_DEVELOPMENT_PROBLEM','示意原文分離問題，不指定層位成分、等待時間、失效率或零售產品瑕疵。');
add('c15r1d06','墨水開發人員得與產品設計、生產設備及企畫合作，把這些問題一起處理。','Medium shot at a workbench, one anonymous technician comparing a plain sample jar with a simple pen-body model and a small equipment part, neutral light.',['F25']);
add('c15r1d07','我覺得，這比單獨找到會消色的材料更吃力；別人手上沒有成功的燒杯，要怎麼買到它？','Medium close-up at a stationery shelf, an anonymous adult holding one plain packaged pen beside a small sample jar, soft light.',['F24','F25'],'AUTHOR_REACTION');
add('c15r1d08','原廠把這段跨部門合作，記為越過量產難關的過程；二〇〇六年，FriXion先在歐洲上市。','Medium shot inside a simple stationery shop, an anonymous worker placing plain capped pens on a display tray, mild interior light.',['F25','F26'],'ATTRIBUTED_RESULT_WITH_RELEASE_YEAR','不補未公開配方、設備改善手段、批次或原廠客觀成功率。');
add('c15r1d09','產品走到日本以前，營業團隊先讓文具店顧客拿筆；那隻手試過以後呢？','Medium shot inside a small stationery shop, an anonymous customer reaching for a plain demonstration pen beside a sample sheet, soft window light.',['F27'],'ATTRIBUTED_LATER_SALES_ACCOUNT');
add('c15r1d10','開場那次寫與擦的試賣，重點正是親手體驗；營業的鈴木直之回憶，顧客看見消色，接著有人購買。','Close-up at a stationery counter, an anonymous customer looking at a rubbed patch on a sample sheet while holding a plain pen, soft light.',['F27'],'NAMED_CALLBACK_WITH_NEW_OBSERVED_RESULT','不創造個別顧客引言、不當獨立效果試驗或所有人購買動機；只轉述受訪者。');
add('c15r1d11','這樣，材料的改變才從研究桌，落到一個原本沒參與開發的人手裡。','Medium shot at a stationery counter, an anonymous customer setting a plain pen beside a corrected sample sheet, mild light.',['F27'],'AUTHOR_INTERPRETATION_OF_SALES_ACTION');
add('c15r1d12','二〇〇七年三月，這支筆在日本上市；紙上的修改，開始有了可直接買到的工具。','Medium shot in a simple stationery shop, an anonymous shop worker arranging plain capped pens in a small tray, diffuse light.',['F26'],'ATTRIBUTED_RELEASE_DATE','2007年3月是日本上市，不當全球首售日；不拿D2的2005產品化改成2005歐洲首售。');
add('c15r1d13','但你拿回家的紙，離開店面以後，並不會一直待在同一種溫度裡。','Medium shot at a home desk, an anonymous adult placing a corrected draft sheet beside a plain closed notebook, soft side light.',['F31','F32'],'FORWARD_NEW_USE_CONDITION');
add('c15r1d14','當初為了讓修改留下而拉開的溫差，碰到另一端的冷或熱，還會怎麼改動這一頁？','Close-up at a desk, an anonymous adult examining a corrected sheet while a warm cup rests at a distance, gentle light.',['F31','F32'],'FORWARD_TEMPERATURE_RESULT_QUESTION','杯子只是FAQ列的可能熱源示意，不說此杯已使紙面到溫。');

ch('低溫把重寫的字也帶回來');
add('c15r1e01','先把草稿放回日常環境。現行說明列出，陽光直射、發熱機材或熱水杯附近，都可能讓筆跡變淡或無色。','Medium shot at a home desk, an anonymous adult moving a corrected sheet away from a plain warm cup, soft window light.',['F31'],'ATTRIBUTED_CONDITIONAL_CURRENT_FAQ','只說可能，不保證任意一杯熱飲、任意日照都到紙面門檻。');
add('c15r1e02','開場擔心的那一頁，若真的受熱消色，原廠另有一條回答：冷卻能讓顏色開始回來。','Close-up at a desk, an anonymous adult looking at a sheet with faint abstract marks beside a closed plain folder, mild light.',['F32'],'NAMED_CALLBACK_WITH_NEW_LOW_TEMPERATURE_RESULT','高溫消色後低溫回復FAQ，不暗示本片已熱測或確實復原。');
add('c15r1e03','說明先把限制擺明：不能保證顏色確實恢復；那它把開始回色，放在哪裡？','Medium close-up at a writing desk, an anonymous adult carefully holding a faintly marked draft sheet, soft light.',['F32']);
add('c15r1e04','它把開始回色，寫在零下十度以下；到了零下二十度前後，則有完整回色的特性。','Close-up at a plain workbench, an anonymous adult looking at an enclosed draft sheet beside an unnumbered cooling instrument, diffuse light.',['F32'],'ATTRIBUTED_CURRENT_FAQ_TEMPERATURE_ENDPOINTS','零下十開始與零下二十前後特性分清；非每張字都保證全回或環境溫度等於已量墨溫。');
add('c15r1e05','這兩個位置不一樣：開始看見回色，不等於每一筆都已經回到原樣。','Medium close-up at a desk, an anonymous adult comparing two abstract strokes with different faintness on a plain sheet, mild light.',['F32'],'INTERPRETATION_OF_DISTINCT_FAQ_ENDPOINTS');
add('c15r1e06','我更想知道，重寫過的那個位置，低溫會替你挑出最新的一版嗎？','Close-up at a desk, an anonymous writer pointing toward overlapping abstract curves on the same small paper area, gentle side light.',['F33'],'AUTHOR_REACTION');
add('c15r1e07','原廠明示，重疊寫過的內容，會一起回色；先前擦掉的舊筆跡，也可能夾在新內容裡。','Medium shot at a writing desk, an anonymous adult examining overlapping abstract ink arcs within a corrected patch, diffuse light.',['F33'],'ATTRIBUTED_CURRENT_FAQ_RESULT');
add('c15r1e08','而用摩擦擦過的筆跡，說明直接寫不能完整回色；把紙冷下來，不能當成復原鍵。','Close-up at a desk, an anonymous adult holding a sheet with partly faded overlapping abstract marks, soft light.',['F33'],'ATTRIBUTED_CURRENT_FAQ_LIMIT','保留不能完整，不弱化為只是未必；不假造本片冷卻實驗。');
add('c15r1e09','若極端高溫或強紫外線直射，已把墨水成分破壞，原廠也說顏色無法恢復。','Medium close-up at a home desk, an anonymous adult putting a faintly marked sheet inside a plain folder away from a window, mild light.',['F34'],'ATTRIBUTED_CURRENT_FAQ_LIMIT','不補破壞溫度、照射量或壽命。');
add('c15r1e10','那是不是所有這種筆跡，都註定很快看不見？','Medium shot at a desk, an anonymous adult looking at a closed plain notebook and a capped pen, soft light.',['F35'],'FORWARD_STORAGE_QUESTION');
add('c15r1e11','原廠的長期保存回答沒有這樣說：避開前面那段高溫，可達到其他染料型凝膠墨水同程度的保存。','Medium close-up at a home desk, an anonymous adult placing a plain notebook in a cool shaded drawer, diffuse light.',['F35'],'ATTRIBUTED_QUALIFIED_COMPARISON','無年份/獨立檔案認證，不作所有現售型號全條件保證。');
add('c15r1e12','它也保留紫外線會使筆跡逐漸褪色的條件，沒有替每一張紙訂下保證年限。','Close-up at a desk, an anonymous hand closing a plain folder around a draft sheet, gentle light.',['F35'],'ATTRIBUTED_QUALIFIED_COMPARISON','無保證年限是原件未提供，不添加定量年數。');
add('c15r1e13','所以，你要交出去的如果是不能消字的證書或地址，就得把筆換掉；這些用途在原廠的禁用範圍。','Medium shot at a desk, an anonymous adult setting a plain erasable pen aside before picking another plain writing tool beside a blank envelope, soft light.',['F36'],'SOURCE_GROUNDED_USE_CHOICE','只列直接相關用途，不演作弊/偽造或他人損失，也不保證另一種墨水永不褪。');
add('c15e13b1','即使留作草稿，你手裡的紙面，也適合這樣來回摩擦嗎？','Medium close-up at a home writing table, an anonymous adult comparing a smooth draft sheet and a rough paper sheet beside a plain pen, soft light.',['F37'],'FORWARD_PAPER_CHOICE_QUESTION');
add('c15e13c1','原廠列出，粗糙紙或和紙的表面，可能在摩擦時受損；紙面有塗層，也可能比較難寫。','Close-up at a writing table, an anonymous adult examining the edge of a rough sheet beside a plain pen, gentle light.',['F37'],'ATTRIBUTED_CURRENT_PAPER_CONDITIONS','各自為可能，非所有紙皆受損、非現場已測或把紙材限制倒灌歷史研發。');
add('c15r1e14','而還在推敲的草稿，你可以選擇讓這一處繼續修改，同時知道紙上材料沒有因為看不見就全數離開。','Medium close-up at a writing desk, an anonymous adult holding a plain pen above an unfinished draft with abstract marks, mild light.',['F06','F07','F33'],'SOURCE_GROUNDED_USE_CHOICE','由原位重寫及重疊回色解讀材料仍在；非法證復原或紙面定量。');
add('c15r1e15','開頭那個問題，我的答案是：這支筆把顏色的狀態交給溫度，留給你的，是能修改、也得選用途的一頁。','Medium shot at a desk, an anonymous adult separating a draft sheet from a blank envelope while holding a plain capped pen, gentle light.',['F05','F07','F33','F36'],'CENTRAL_QUESTION_ANSWER_WITH_USE_DECISION');
const answerScene=scenes.pop();assert.equal(answerScene.id,'c15r1e15');const answer=answerScene.lines[0];const answerClaim=claims.at(-1);answerClaim.visual_prompt=null;answerClaim.visual_kind='OUTRO_CARD_NOT_GENERATED';
const outro={id:'c15r1outro',template:'outro',data:{title:'能修改，也要選用途',cta:'分享你最常改的一頁'},lines:[answer,
 {id:'c15r1ct1',text:'留言分享，你最常拿這種筆改哪一頁，是行程、草稿，還是自己的筆記。',emotion:'溫暖收束，像對一位觀眾說話'},
 {id:'c15r1ct2',text:'想看熟悉的物品，怎麼把材料的取捨交到你手裡，歡迎訂閱品牌故事。',emotion:'溫暖收束，像對一位觀眾說話'}]};
scenes.push(outro);for(const l of outro.lines.slice(1)){rows.push({chapter,id:l.id,text:l.text});claims.push({id:l.id,chapter,claim:l.text,claim_kind:'VIEWER_INVITATION_NOT_STORY_PROMISE',status:'PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW',research_claim_ids:[],anchor_ids:[],source_ids:[],limits:[],author_context:'觀眾留言與訂閱邀請，不宣稱史實，不預告下一集。',visual_prompt:null,visual_kind:'OUTRO_CARD_NOT_GENERATED'});}

const loops=[
 ['c15r1h01','c15r1e07','開場那頁受溫度影響後不能只選最新一版'],
 ['c15r1h02','c15r1d10','試賣寫擦之後有顧客購買的回憶'],
 ['c15r1h03','c15r1a04','筆另一端以摩擦熱改色而不是搬走整片材料'],
 ['c15r1h04','c15r1d03','小燒杯外的量產膠囊為五百公斤'],
 ['c15r1h04','c15r1e04','寫後低溫介入的開始與回色端點'],
 ['c15r1h06','c15r1e15','材料的色態與用途決定回答核心問題'],
 ['c15r1a01','c15r1a02','先停手的原因是要等筆跡乾'],
 ['c15a02b1','c15a02c1','膠擦選材重彈性與耐磨'],
 ['c15r1a03','c15r1a06','消色不以消字屑帶走筆跡'],
 ['c15r1a07','c15r1a08','消色原位重新落筆'],
 ['c15r1a10','c15r1b10','舊線沒有馬上回來因記憶型還需更低溫'],
 ['c15r1a18','c15r1b10','變色到修改靠記憶型分離回色溫度'],
 ['c15r1b09','c15r1b10','記憶型用另一個更低設定才回色'],
 ['c15r1b12','c15r1b13','早期記憶型回顧所列約二十度間隔'],
 ['c15r1c08','c15r1c09','小型化後2002裝飾筆出現'],
 ['c15r1e03','c15r1e04','高溫消色後低溫回色的不同端點'],
 ['c15r1b16','c15r1c08','能過筆尖所需的膠囊小型化'],
 ['c15r1b17','c15r1c01','初期與記憶型的實際尺寸'],
 ['c15r1c04','c15r1c07','變薄與相容問題需膜材及包覆方法研究'],
 ['c15r1c11','c15r1c12','仍留色的問題引出變透明的提案'],
 ['c15r1c17','c15r1c19','穩定溫域向兩端擴大'],
 ['c15r1c20','c15r1d08','小份實驗接上量產合作及歐洲上市'],
 ['c15r1d02','c15r1d05','放大後新增墨水分離或劣化問題'],
 ['c15r1d09','c15r1d10','試賣的親手動作接上受訪者所述購買'],
 ['c15r1d14','c15r1e07','冷熱介入重寫紙時舊新內容會一同回色'],
 ['c15r1e10','c15r1e11','條件保存並非必定很快消失'],
 ['c15e13b1','c15e13c1','粗糙紙摩擦與塗層紙書寫各有條件']
].map(([setup,payoff,what])=>({setup,payoff,what}));
const usedAnchorIds=[...new Set(claims.flatMap(c=>c.anchor_ids))];
const usedSourceIds=[...new Set(claims.flatMap(c=>c.source_ids))];
for(const k of usedSourceIds){const s=sources.get(k);assert.equal(fileSha(s.raw_path),s.sha256,k);if(s.text_path)assert.equal(fileSha(s.text_path),s.text_sha256,k);}
for(const k of usedAnchorIds){const a=anchors.get(k);if(a.text_file)assert.equal(fileSha(a.text_file),a.text_file_sha256,k);}
const title='FriXion改過的字，六十度後還留哪一版？｜品牌故事';
const doc={schema_version:1,slug:SLUG,format:'drama',category:'story',narration_locale:'zh-TW',target_minutes:[12,14],voice,subtitles:{burn_in:true},look:{preset:'cute-mystery'},characters:[],music:{prompt:'light, curious, a little mysterious, no vocals',gain_db:-20,duck_db:-10},loops,youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',title,description:'一支能寫、消、再寫的筆，到底把什麼留在紙上？跟著FriXion的一筆修改，看記憶型變色材料、微膠囊小型化與量產，如何接到現代使用者的草稿。低溫回色與不能完整復原的界線，決定這張紙應該選哪種筆。歷史依原廠及開發者回顧歸屬，匿名概念插圖不作同期現場或零售配方剖面。\n\n原件來源\n'+usedSourceIds.map(k=>sources.get(k).final_url).join('\n'),tags:['FriXion','PILOT','擦擦筆','品牌故事','日用品的意外轉身','微膠囊','墨水'],video_id:null},thumbnail:{template:'thumb',data:{layout:'d',headline:'擦掉\n還會回來',sub:'你要留哪一版',brand:'FRIXION',tag:'品牌故事',shot:'c15r1e07'}},sources:usedSourceIds.map(k=>({title:sources.get(k).title,url:sources.get(k).final_url,checked_on:'2026-10-25'})),assets:[],scenes};
assert.deepEqual(validateVideo(doc),[]);
assert(!doc.series);assert.deepEqual(doc.voice,read(voiceFile).voice);
const pos=new Map(rows.map((r,i)=>[r.id,i]));for(const l of loops)assert(pos.get(l.setup)<pos.get(l.payoff),JSON.stringify(l));
const chapterGroups=new Map();for(const r of rows)chapterGroups.set(r.chapter,[...(chapterGroups.get(r.chapter)??[]),r]);
for(const [c,rr]of chapterGroups)assert(rr.some(r=>r.text.includes('你'))&&rr.some(r=>r.text.includes('我')),c);
const total=rows.reduce((n,r)=>n+spokenUnits(r.text),0),coldopen=chapterGroups.values().next().value.reduce((n,r)=>n+spokenUnits(r.text),0),cta=outro.lines.reduce((n,r)=>n+spokenUnits(r.text),0);
const series={kind:'story',slug:'brand-story-remakes-20261025',episode:15,chapter:1,title,logline:'一筆草稿的寫消再寫，穿過變色材料、膠囊與量產，再回到冷熱下的用途選擇。',names:['FriXion','FRIXION','PILOT','Metamo Color','ILLUSION','千賀邦行','鈴木直之'],characters:[],visual_tier:'stills',compilation:false,target_minutes:13,image_model:'image-01',look:{preset:'cute-mystery'},candidate_revision:'c15-r1',status:'HOLD_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_FRESH_NARRATIVE'};
put('video.json',doc);put('series.json',series);put('narration-only.json',rows);
put('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW',candidate_revision:'c15-r1',author:'/root/c15_r1_author',author_is_original_researcher:false,video_slug:SLUG,frozen_research_sha256:RESEARCH_SHA,source_registry:Object.fromEntries(usedSourceIds.map(k=>[k,sources.get(k)])),anchor_registry:Object.fromEntries(usedAnchorIds.map(k=>[k,anchors.get(k)])),rows:claims});
const script=['# '+title,'','C15 R1全新稿，HOLD待獨立來源／書面配鏡與新讀者。ID與章名不讀入旁白。未生成TTS、圖片、音樂或影片。',''];let last='';for(const r of rows){if(last!==r.chapter){last=r.chapter;script.push('## '+last,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C15 R1逐句來源及書面配鏡綁定','','作者只提交可審稿，不給SOURCE、敘事、媒體或owner批准。原始bytes留倉庫外source-cache；完整來源、raw SHA、文本SHA、段落錨點、原文節錄與逐句限制在claims.json。所有人物、膠囊與紙面均為匿名概念插圖，不仿歷史人物或提供零售分子結構。','','| ID | 旁白 | 類型 | 研究主張／原件錨點 | 限制與作者語境 |','| --- | --- | --- | --- | --- |'];for(const c of claims)cm.push('| '+c.id+' | '+c.claim+' | '+c.claim_kind+' | '+c.research_claim_ids.join(', ')+' / '+c.anchor_ids.join(', ')+' | '+[...c.limits,c.author_context].filter(Boolean).join('；')+' |');cm.push('','## 原件錨點','');for(const a of usedAnchorIds)cm.push('### '+a,'',JSON.stringify(anchors.get(a)),'');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const brief=['# C15 R1｜一筆修改留下了什麼','','狀態：HOLD。全新remake slug、category story、video不帶series，不沿用原集核准。新稿須另一位逐句來源／書面配鏡查核及兩位新讀者。','','### 選項 A：一筆草稿的寫、消、再寫','','主線：用同一筆修改作觀眾線索，由等待乾、消色與原位重寫，進入能保留色態的記憶型材料，再看膠囊小型化、透明化與量產，最後回到這一頁在冷熱下的結果及選筆。歷史材料、不同產品與觀眾假設不是同一實體或同一配方；不依產品目錄拼接。','','## 問題','','同一支筆寫、消、再寫，究竟把什麼留在紙上，又把什麼交給了溫度？','','## 一句答案','','它改變紙上材料的顏色狀態，原位可重寫；新舊內容在低溫回色條件下可能一同出現且摩擦擦過者不能完整復原，因此修改方便與不能消字的用途要分開選。','','## 站主觀點','','每次往前都有真動作或結果：等乾再擦、原位重寫、記憶型維持色態、膜變薄與溶劑相容、變透明提案、五百公斤量產與墨水分離、顧客親手體驗、低溫新舊回色。沒有玩具／產品型號／銷量清單、文件災難或犯罪戲，也不拿警語撐長。每章保留觀眾位置與作者反應。','','## 原件界線','','歷史皆按原廠／受訪者回顧歸屬，不宣稱全球首創；2001／2002微粒化差異用2000年代初；1975專利原案未識別故不入稿。現行60度與歷史研發−20至65度跨度分開，不說2017約65與現行60是相同全型號實測。零下十開始、零下二十前後回色特性仍不保證；重寫內容一同回色，摩擦擦過者不能完整恢復。圖像膠囊不破裂、不仿零售剖面，紙面抽象筆畫無可讀字。','','## 長度與語言','','whole narration '+total+' native spokenUnits，含coldopen '+coldopen+'及有聲CTA '+cta+'。目標13分鐘、真正unwrapped narration720–840秒，只能實際TTS量測；規劃units與估時不作時長PASS／FAIL，不慢播、不插空白、不重述填長。八語預設en/ja/ko/es/pt/id/vi/th，尚未翻譯或套後台選項。','','## 聲畫執行待辦','','voice逐字複製C06的Sulafat STORY設定；正常初始化本集immutable字典，不抄他集字典。image-01、唯一look cute-mystery，英文匿名prompt，stillmotion；正文至少70%插圖、最多連3卡。繁中燒錄及CC，冷開場後5秒片頭，最後21秒正式v4片尾，layout d黃字黑邊主標與白副標。尚未取得／生成任何新媒體或確認正式v4身份。','','## 待查','','逐句來源和書面圖像語意、新盲讀、讀音、實TTS、媒體QA與owner審核均待辦。0付費、0provider、0後台mutation、0新增批准。',''].join('\n');fs.writeFileSync(path.join(OUT,'brief.md'),brief);
const tl=estimateTimeline(doc),maxShot=Math.max(...tl.scenes.filter(s=>s.id!==outro.id).map(s=>(s.end_frame-s.start_frame)/FPS));
const notes={schema_version:1,status:'HOLD_PENDING_NATIVE_INITIALIZATION_AND_INDEPENDENT_SOURCE_NATIVE_READERS',candidate_revision:'c15-r1',author:'/root/c15_r1_author',counts:{lines:rows.length,scenes:scenes.length,shots:scenes.length-1,cards:1,chapters:chapterGroups.size,loops:loops.length},native_units:{whole_narration_spoken_units:total,coldopen,voiced_CTA:cta,actual_narration_seconds:null,actual_duration_verified:false,official_duration_scope:'whole actual unwrapped narration timeline including coldopen and voiced CTA, excluding separately added channel bookends',rough_planning_target:3500,delta_to_rough_target:total-3500,planning_arithmetic_at_4_to_5_units_per_second:[total/5,total/4],planning_arithmetic_not_actual_audio:true},maximum_estimated_shot_seconds:maxShot,source_research_sha256:RESEARCH_SHA,source_raw_receipts_checked:usedSourceIds.length,protected_original25_and_snapshots_unchanged:true,voice_source:{path:voiceFile,file_sha256:voiceSHA,voice_object_sha256:sha(JSON.stringify(voice)),exact_copy:true},independent_source_review:'PENDING_OTHER_REVIEWER',independent_narrative_review:'PENDING_FRESH_READERS',source_pass_claimed:false,narrative_pass_claimed:false,owner_approval_created:false,provider_calls:0,paid_calls:0,backend_mutations:0,actual_media_generated:false,runtime_root:RUNTIME,author_notes:['Material history supports the one-ink-stroke use chain; not one physical stroke traveling through past laboratories.','2001/2002 original mismatch retained in research and narrowed to early 2000s in narration.','1975 precise patent identity, unverified photocopying claim, product catalogue and sales totals excluded.','Every visual is an anonymous original concept; no readable text, logo or named likeness in prompts.'],recipe_only:{image_model:'image-01',look:{preset:'cute-mystery'},stillmotion:true,burn_in_zh_tw:true,cc_zh_tw:true,intro_seconds:5,intro_after_coldopen:true,outro_seconds:21,outro_version:'formal-v4-not-yet-identified',minimum_illustration_share:0.70,maximum_consecutive_cards:3},frozen_at_utc:new Date().toISOString()};
if(!process.argv.includes('--draft')){
 const project=loadProject({root:RUNTIME,slug:SLUG});
 assert.equal(fileSha(project.file),fileSha(path.join(OUT,'video.json')));
 const lexBefore=sha(JSON.stringify(project.shelfLexicon));const lint=lintProject(project);
 assert.equal(lexBefore,sha(JSON.stringify(project.shelfLexicon)));
 notes.native_initialized_lint=lint;notes.native_lint_errors=lint.errors.length;notes.immutable_dictionary_sha256=lexBefore;
 notes.status='HOLD_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_FRESH_READERS';
 put('native-author-lint-r1.json',lint);assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));
}
for(const f of protectedFiles)assert.equal(fileSha(f.path),f.sha256,f.path);for(const[f,h]of Object.entries(RESEARCH_SHA))assert.equal(fileSha(path.join(OUT,f)),h,f);assert.equal(fileSha(voiceFile),voiceSHA);
notes.file_sha256=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.mjs'].map(f=>[f,fileSha(path.join(OUT,f))]));
notes.core_four_sha256=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(f=>[f,notes.file_sha256[f]]));
put('author-notes.json',notes);
console.log(JSON.stringify({status:notes.status,counts:notes.counts,native_units:notes.native_units,maxShot,native_lint_errors:notes.native_lint_errors,core_four_sha256:notes.core_four_sha256},null,2));
