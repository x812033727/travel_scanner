import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {eachLine,spokenText,validateVideo} from '../../../../tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS} from '../../../../tools/video/core/timeline.mjs';
import {loadProject,lintProject} from '../../../../tools/video/core/state.mjs';

const OUT=path.dirname(fileURLToPath(import.meta.url));
const REPO=path.resolve(OUT,'../../../..');
const SLUG='story-everyday-camelbak-c14-remake-20261025';
const RUNTIME='/workspace/work/brand-story-20261025/c14-submission-root';
const sha=x=>createHash('sha256').update(x).digest('hex');
const fileSha=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8'));
const write=(f,x)=>fs.writeFileSync(path.join(OUT,f),JSON.stringify(x,null,2)+'\n');
const RESEARCH_SHA={
 'research-original.md':'e8d6ec0f77680c32c3f7de08723d2f44a5e8960b2f86024ac4bc742180acda65',
 'research-original.claims.json':'2303aa7b73dd2a9dbba94f6b09793b77bb183620125f971a553d08aa31d52609',
 'original-preservation.json':'2e0f4c93c05f455d732880b2591f771b1bcaccf21d0c741228798e70a588e009'
};
for(const[f,d]of Object.entries(RESEARCH_SHA))assert.equal(fileSha(path.join(OUT,f)),d,f);
const research=read(path.join(OUT,'research-original.claims.json'));
const preservation=read(path.join(OUT,'original-preservation.json'));
const protectedFiles=[...preservation.snapshots.flatMap(f=>[{path:f.path,sha256:f.sha256},{path:f.snapshot_path,sha256:f.snapshot_sha256}]),...Object.entries(RESEARCH_SHA).map(([f,sha256])=>({path:path.join(OUT,f),sha256})),{path:preservation.snapshot_manifest_path,sha256:preservation.snapshot_manifest_sha256}];
for(const f of protectedFiles)assert.equal(fileSha(f.path),f.sha256,f.path);
const voiceSource=path.join(REPO,'docs/videos/brand-story-remakes-20261025/c06/video.json');
const voiceSourceSha=fileSha(voiceSource),voice=structuredClone(read(voiceSource).voice);
const sourceRegistry=Object.fromEntries(research.source_catalog.map(s=>[s.id,structuredClone(s)]));
const anchorRegistry=Object.fromEntries(research.anchors.map(a=>[a.id,structuredClone(a)]));
const textOf=s=>fs.readFileSync(s.text_path,'utf8');
const context=(s,n,pdf)=>pdf?textOf(s).split('\f')[n-1]:textOf(s).split('\n').find(x=>x.startsWith(String(n).padStart(4,'0')+': '))?.slice(6);
const normal=x=>String(x).normalize('NFKC').replace(/\s/g,'').toLowerCase();
function extra(id,sid,n,pdf,quote,claim,limits){
 const s=sourceRegistry[sid],c=context(s,n,pdf);assert(c&&normal(c).includes(normal(quote)),id);
 anchorRegistry[id]={id,source_id:sid,claim,limits,locator:(pdf?'PDF page ':'HTML normalized text paragraph ')+n,paragraph:pdf?null:n,pdf_page:pdf?n:null,short_quote:quote,quote_sha256:sha(quote),context_sha256:sha(c),raw_path:s.raw_path,raw_sha256:s.sha256,text_path:s.text_path,text_sha256:s.text_sha256,status:'AUTHOR_LOCATOR_IN_FROZEN_ORIGINAL_PENDING_INDEPENDENT_REVIEW'};
}
extra('A_MOUTH_P7','PAT_MOUTH_PDF',7,true,'the mouthpiece can be slipped on and off the hose for','口器與管的可拆清潔接點；狹縫兩唇在靜止時相貼。','僅US6070767圖1–10所述設計，非每款量產SKU；不是初代衣夾同零件。');
extra('A_MOUTH_P8','PAT_MOUTH_PDF',8,true,'35 ml/sec and approximately 45 ml/sec','圖1–10口器申請人稱35–45mL/s；正常條件定義為口含、壓至出水狀態、吸吮如吸管；撤力回閉。','專利申請人自行報告，無獨立測試、樣本數、精確吸力或耐久條件；不是自然灌水、每SKU或醫療結果。不口播倍數、效率、供氧或速度表現承諾。');
extra('A_SW_CONTEXT','SW_PDF',3,true,'The more testing we can do with real people to obtain feedback','具名工程師談以可用樣件取得真人回饋。','©2016供應商回顧；未給此咬閥真人測試條件/結果/具體事件日期；兩個月為likely估計，不口播。');
extra('A_CARE_CONTEXT','CARE',75,false,'If the ring is twisted or pulled out of shape','蓋內密封圈變形可能不能正確密合。','現行故障可能原因，非全故障表或初代歷史事件。');
extra('A_CARE_GRIT','CARE',74,false,'keep it from sealing completely','砂粒可能使蓋口不能完整密封。','現行故障可能原因；不主張本片實測。');
extra('A_CLEAN_CONTEXT','CLEAN',92,false,'Remove the drinking tube, bite valve and other detachable components','原廠清潔範圍包括可拆管與咬口。','現行指引；不是早年研發動機或已完成清潔實驗。不可拆部件不作可拆示意。');
extra('A_CLEAN_RINSE','CLEAN',110,false,'Run clean water through the drinking tube and bite valve','清水沖洗包括管與咬口的完整水路。','現行支援內容，非清洗配方、消毒或微生物結果。');
extra('A_CLEAN_TUBE','CLEAN',128,false,'Avoid leaving it tightly coiled','管子垂掛兩端開放，避免盤緊造成低處積水。','現行乾燥指引，非本片實測、感染或醫療結果。');
// Resolve the exact 3L product title node from the immutable original text, never from a search snippet.
const crux=sourceRegistry.SWISS_CRUX,cruxLines=textOf(crux).split('\n');
const capacityLine=cruxLines.find(x=>/Crux.*3L.*Reservoir/i.test(x));assert(capacityLine);
const capacityPara=Number(capacityLine.slice(0,4));
extra('A_CRUX_3L','SWISS_CRUX',capacityPara,false,capacityLine.slice(6),'現行Crux3L原頁標題容量。','開場三公升是具名現行容量的觀眾假設，不是原型容量，也未聲稱本片真的測得漏水。');
const materials=read(path.join(OUT,'author-materials.json'));
const rows=[],scenes=[],claims=[];
const rowNotes={
 c14r1h02:'1988/1989均屬八〇年代末。主辦同段自相矛盾，不擇一；NZ回顧非同期現場。COURT的1988Texas只作年代/地點交叉界線，不把Michael Edson拼字或FasTrak成立與品牌回顧合成已證單一事件。艾德森為Michael Eidson的口播譯名。',
 c14r1h01:'假設句；現行Crux3L容量，不是初代水袋規格、實測滴漏、危急脫水或醫療操作。',
 c14r1o02:'只敘後來品牌回顧中的器材與位置；不教點滴袋改裝飲用、不演醫療程序。',
 c14r1v02:'1998-07-17申請、2000-06-06授權為文件日期；不是首發明或首款採用日期。',
 c14r1v15:'申請人報圖1–10口器35–45mL/s，正常操作包括嘴含、壓開與吸吮；沒有樣本數/精確吸力/獨立複現。不等倍增銷量或全產品流量。',
 c14r1b06:'2006-10-12公開，不作實驗事件年；本案2005-12-20送件，與展場實物的專利/SKU對應未證。',
 c14r1b08:'防漏為報導歸給公司的說法，不是記者或本片獨立測試；相鄰專利可選構造不當展場SKU精確剖面。',
 c14r1t01:'2014會計年度母公司年報，2015申報；只口播當年產品組合。',
 c14r1t05:'2015-05-06報導的現場觀測；不是測試歷史首次或所有型號。',
 c14r1t06:'原文a dozen=12，圖示應12件；反覆咬壓無精確循環數/樣本通過率，不把thousands of times a day變成壽命結果。',
 c14r1m01:'麥克里迪為Aaron McCready；©2016供應商個案的具名回述，非確認2016實驗日期、初代首次或2015實驗室同一SKU。',
 c14r1m04:'可測樣件的取得，不聲稱真人實測已執行或通過。',
 c14r1m05:'兩天只屬工程師回述的實體矽膠測試件取得，不等兩天耐久測試通過；likely兩個月及10–20倍宣傳比較未口播。',
 c14r1r09:'第三人稱歸屬現行指引的檢查動作，不當本片親測、初代故障或醫療/戶外安全保證。',
 c14r1d10:'只示意原廠允許拆卸的部件，不強拆固定接點。'
};
function bind(id,chapter,text,prompt,refs,kind){
 const aa=[...new Set(refs.split(',').filter(Boolean))];
 if(id==='c14r1h01')aa.push('A_CRUX_3L');
 if(id==='c14r1r06')aa.push('A_CARE_GRIT');
 if(id==='c14r1d04')aa.push('A_CLEAN_RINSE');
 for(const a of aa)assert(anchorRegistry[a],a);
 const evidence=aa.map(a=>{const x=anchorRegistry[a],s=sourceRegistry[x.source_id];return {anchor_id:a,source_id:x.source_id,url:s.url,http_status:s.http_status,retrieved_at_utc:s.retrieved_at_utc,raw_path:x.raw_path,raw_bytes:s.bytes,raw_sha256:x.raw_sha256,text_path:x.text_path,text_sha256:x.text_sha256,locator:x.locator,short_quote:x.short_quote,quote_sha256:x.quote_sha256,context_sha256:x.context_sha256,scope:x.claim,not_supported:x.limits};});
 rows.push({chapter,id,text});
 claims.push({id,chapter,claim:text,claim_kind:kind,status:'PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW',anchor_ids:aa,source_ids:[...new Set(aa.map(a=>anchorRegistry[a].source_id))],evidence,limits:[...new Set(aa.map(a=>anchorRegistry[a].limits))],author_context:rowNotes[id]??'物件/功能相連不代表同一袋水、同一部件、型號、批次或已證歷史研發因果。',visual_prompt:prompt,visual_kind:prompt?'ORIGINAL_ANONYMOUS_CONCEPT_ILLUSTRATION_NOT_ARCHIVAL_REENACTMENT':'OUTRO_CARD'});
}
for(const chapter of materials.chapters){
 chapter.rows.forEach(([text,refs,prompt,kind],i)=>{
  const id='c14r1'+chapter.key+String(i+1).padStart(2,'0');
  const scene={id,template:'shot',data:{prompt,visual:'still',camera:['push in','pan left','pull out','pan right','drift','tilt up','tilt down'][scenes.length%7]},lines:[{id,text,emotion:'對一位觀眾說書，自然起伏；假設、原文歸屬與數字讀清楚'}]};
  if(i===0&&rows.at(-1)?.chapter!==chapter.title)scene.chapter=chapter.title;
  scenes.push(scene);bind(id,chapter.title,text,prompt,refs,kind);
 });
}
const outroLines=materials.outro.map(([text,refs,kind],i)=>{const id='c14r1ct'+(i+1);bind(id,materials.chapters.at(-1).title,text,null,refs,kind);return{id,text,emotion:'溫暖乾脆，對一位觀眾說話'};});
scenes.push({id:'c14r1outro',template:'outro',data:{title:'方便，也要留給下一次',cta:'你把水帶去哪裡？'},lines:outroLines});
const loops=[
 ['h01','r05','容量並不替代補水蓋密封：砂粒與扭曲密封圈'],
 ['h04','t06','開場的金屬牙齒：十二咬閥被反覆夾壓'],
 ['h04','m05','開場的模具：兩天拿到實體矽膠測試件'],
 ['h06','o01','原型出口先由衣夾手動夾閉'],
 ['h06','ct1','一條可開關並可重新使用的水路'],
 ['o04','o05','出口到嘴邊仍需手動控制'],
 ['o07','v06','放開嘴後彈性狹縫回到閉合狀態'],
 ['v04','v06','平常閉合的兩唇靠彈性回閉'],
 ['v08','v09','材料須能回復，文件舉矽膠例'],
 ['v10','v11','可拆口器從管端滑下再裝回以供清潔'],
 ['v13','v15','吸吮條件下申請人報35–45mL/s流量'],
 ['v18','b02','翻起咬口與瓶內短吸管形成手握水路'],
 ['b05','b07','水瓶文件沿用受壓開、撤力閉的設計構想'],
 ['b08','b09','展場防漏屬公司主張，非記者自測'],
 ['b11','t06','袋體壓扭與咬口夾壓分別觀測'],
 ['t04','t06','測試動作對應袋體與嘴部不同受力'],
 ['t09','t10','報導未交出循環數與通過率，不擴為保證'],
 ['t11','m04','列印模製出可測的真矽膠件'],
 ['m03','m05','軟件取得讓形狀與材料可受測'],
 ['m07','m08','工程師重視真人回饋，但未給此樣件測試結果'],
 ['m09','r05','補水口另外由蓋口與密封圈密合'],
 ['r04','r05','蓋邊漏水可能是砂粒或密封圈變形'],
 ['r08','r09','裝水後轉動與壓袋觀察密封'],
 ['r12','d06','收存前把內壁撐開讓殘水排出'],
 ['d05','d06','乾燥架分開內壁提供空氣通路'],
 ['d08','d09','管子排水垂掛兩端開放以免低處積水'],
 ['d11','d12','收存前逐處觀察水滴與凝結']
].map(([setup,payoff,what])=>({setup:'c14r1'+setup,payoff:'c14r1'+payoff,what}));
const usedAnchors=[...new Set(claims.flatMap(c=>c.anchor_ids))];
const usedSources=[...new Set(usedAnchors.map(a=>anchorRegistry[a].source_id))];
for(const sid of Object.keys(sourceRegistry)){const s=sourceRegistry[sid];assert.equal(s.http_status,200);assert.equal(fs.statSync(s.raw_path).size,s.bytes);assert.equal(fileSha(s.raw_path),s.sha256);assert.equal(fileSha(s.text_path),s.text_sha256);}
for(const id of [...usedAnchors,'A01']){const a=anchorRegistry[id],s=sourceRegistry[a.source_id],c=context(s,a.pdf_page??a.paragraph,!!a.pdf_page);assert.equal(sha(c),a.context_sha256,id);assert.equal(sha(a.short_quote),a.quote_sha256,id);assert(normal(c).includes(normal(a.short_quote)),id);}
const doc={schema_version:1,slug:SLUG,format:'drama',category:'story',narration_locale:'zh-TW',target_minutes:[12,14],voice,subtitles:{burn_in:true},look:{preset:'cute-mystery'},characters:[],music:{prompt:'light, curious, a little mysterious, no vocals',gain_db:-20,duck_db:-10},loops,youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',title:'CamelBak水背上身，為何出口還得受咬？｜品牌故事',description:'一袋水背上身以後，怎麼讓它在要喝時出來，其他時候留在該在的地方？從品牌回顧的襪子與衣夾，循著口器原件、2006展場水瓶、2015實驗室觀測、2016工程師回述，再走到現行補水密封與乾燥。原型賽事1988/1989原主辦回顧同段矛盾，不擇一；公司成立1989另屬事件。專利方案、商品觀測與各期樣件不混成同一SKU、批次或歷史首次；測試動作不等耐久結果。畫面為原創匿名概念插圖，尚未生成媒體。\n\n參考原件（查閱2026-10-25）\n'+usedSources.map(k=>sourceRegistry[k].title+'\n'+sourceRegistry[k].url).join('\n'),tags:['CamelBak','水袋','咬閥','品牌故事','日用品的意外轉身','單車','材料','設計'],video_id:null},thumbnail:{template:'thumb',data:{layout:'d',headline:'出口\n得自己關',sub:'一袋水怎麼重用',brand:'CAMELBAK',tag:'品牌故事',shot:'c14r1h03'}},sources:usedSources.map(k=>({title:sourceRegistry[k].title,url:sourceRegistry[k].url,checked_on:'2026-10-25'})),assets:[],scenes};
assert(!doc.series);assert.deepEqual(validateVideo(doc),[]);assert.deepEqual(doc.voice,voice);
const order=new Map(rows.map((r,i)=>[r.id,i]));for(const l of loops)assert(order.get(l.setup)<order.get(l.payoff),JSON.stringify(l));
for(const c of materials.chapters)assert(c.rows.some(r=>r[0].includes('你'))&&c.rows.some(r=>r[0].includes('我')),c.title);
const total=[...eachLine(doc)].reduce((n,{line})=>n+spokenUnits(spokenText(line)),0);
const coldopen=rows.filter(r=>r.chapter===materials.chapters[0].title).reduce((n,r)=>n+spokenUnits(r.text),0);
const CTA=outroLines.reduce((n,r)=>n+spokenUnits(r.text),0);
write('video.json',doc);write('narration-only.json',rows);
write('series.json',{kind:'story',slug:'brand-story-remakes-20261025',episode:14,chapter:1,title:doc.youtube.title,logline:'一袋水與出口，從背上身走到開關、補水、清乾再重用。',names:['CamelBak','Michael Eidson','艾德森','Aaron McCready','麥克里迪','Crux'],characters:[],visual_tier:'stills',compilation:false,target_minutes:13,image_model:'image-01',look:{preset:'cute-mystery'},candidate_revision:'c14-r2',status:'hold_pending_independent_source_and_fresh_readers'});
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW',candidate_revision:'c14-r2',author:'/root/c05_r10_author',author_is_original_researcher:true,video_slug:SLUG,frozen_research_sha256:RESEARCH_SHA,source_registry:Object.fromEntries(usedSources.map(k=>[k,sourceRegistry[k]])),anchor_registry:Object.fromEntries(usedAnchors.map(k=>[k,anchorRegistry[k]])),background_source_registry:{C_HISTORY:sourceRegistry.C_HISTORY},author_added_locators_in_existing_frozen_originals_only:usedAnchors.filter(a=>a.startsWith('A_')),separate_omitted_background:{company_founded:{year:1989,anchor:anchorRegistry.A01,event_distinct_from_prototype:true,not_spoken:true},prototype_date_conflict:{anchors:['A05','A06','A07'],not_resolved:true},omitted_claims:['全場嘲笑','整體市場反對','倍增銷量','危急脫水後果','醫療操作教學','兩月外製實測','終身不漏/測試通過率']},rows:claims});
const script=['# '+doc.youtube.title,'','C14 R2作者新稿，HOLD。章名及ID僅供審稿；官方body含coldopen及有聲CTA，實聲未測。',''];let previous='';
for(const r of rows){if(previous!==r.chapter){previous=r.chapter;script.push('## '+r.chapter,'');}script.push('### '+r.id,'',r.text,'');}
fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const cm=['# C14 R2逐句原件與書面配鏡綁定','','作者同時是原研究員，不能簽來源PASS。每句綁raw實bytes/SHA、取回狀態、原頁/段、quote/context SHA；新增定位只在凍結原件中，三研究不改。概念圖不是同期實物重建、原專利精密剖面或已生成媒體。','','| ID | 口播 | 類型 | 原件錨點 | 額外界線 |','| --- | --- | --- | --- | --- |'];
for(const c of claims)cm.push('| '+c.id+' | '+c.claim+' | '+c.claim_kind+' | '+c.anchor_ids.join(', ')+' | '+c.author_context+' |');
cm.push('','## 精確原件定位','');for(const a of usedAnchors)cm.push('### '+a,'',JSON.stringify(anchorRegistry[a]),'');
fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const brief=['# C14 R2｜一袋水與出口','','HOLD：作者/原研究員交第一稿；沒有獨立來源、敘事、實聲圖像或owner核准。新slug '+SLUG+'，category story / format drama；video無series欄位，不rebind舊集。父task已涵蓋，未另開task。','','## 問題','','把水背上身之後，怎麼讓它在你要喝時出來，其他時候留在該在的地方？','','## 一句答案','','方便要把開關、密封與再使用接成完整水路；把容量背走，還只是開始。','','## 站主觀點','','用每個部件實際承擔的動作講方便：管與夾先移動並守住出口，彈性狹縫控制出水，模具做出可測件，補水蓋與乾燥再承擔各自的問題；不把公司成功當物件結果。','','## 一條線','','一袋水如何從背上身，沿管到嘴邊，控制開關，再完成補水、密封、清乾與下一次重用。主角是水路與出口的工作，不是同一袋液體、零件、SKU或工廠批次跨年。每階段有上一個安排留下的新問題與可見動作；不做企業百科、商業成功史或清潔教學清單。','','## 年代與物件','','原型賽事：主辦同段1988/1989矛盾，口播只用八〇年代末並歸品牌回顧。官方公司成立1989是另事件，留claims背景不口播，未合成原型年。IV袋/襪/管/夾只描述後代回顧，不提供醫材改裝步驟或危急脫水故事。1998申請/2000授權為特定口器文件；2006展場750mL瓶與同年公開申請不當同一SKU證據。2014年報袋/管/口器材料只屬該年。2015記者看壓扭與12咬閥金屬夾壓，無耐久成績表。2016供應商個案具名工程師稱兩天取得實體矽膠測試件，不說真人測試已通過；非首次、非同一2015零件。現行3L/蓋口/清乾另屬現行產品與支援。','','## 來源強度與增補定位','','不改三凍結研究。作者對既有US6070767原PDF第7/8頁補精確定位，口播可拆清潔接點與申請人自報35–45mL/s；測試正常條件含口含、咬開與吸吮，不作自然灌水或全SKU保證，未口播倍率/供氧效果。其餘新增定位僅取既有SW個案、CARE/CLEAN/Crux原頁段，逐句進claims。待獨立reviewer直接讀原件裁定。','','## 官方字量與時長','','全旁白 '+total+' native spokenUnits，含coldopen '+coldopen+'與有聲CTA '+CTA+'。扣coldopen '+(total-coldopen)+'；再扣CTA '+(total-coldopen-CTA)+'，兩個只屬規劃分項。官方body是actual narration timeline整份，只排另加5s/21s branding。4–5units/s算術範圍 '+(total/5).toFixed(1)+'–'+(total/4).toFixed(1)+'秒，4.5/s約'+(total/4.5).toFixed(1)+'秒；不是實聲。有效量低於rough3500，13min/720–840s仍強HOLD，不用慢播、警語、重述、商業副線或假想失敗補字。','','## 執行規格（recipe，未取素材）','','精確複製C06現行voice整個物件（gemini/Sulafat與STORYstyle/performance）。image-01，唯一look {preset:cute-mystery}；英文匿名無品牌/真人名/logo/可讀字prompt，stillmotion，正文至少70%插畫、最多連3卡；每shot估計≤12s。繁中burn_in true並保留CC。縮圖layout d，CAMELBAK大字、黃字黑框主標、白短副標。coldopen後5s正式片頭、有聲CTA後21s正式v4片尾，只列recipe，無媒體provider/付費生成或素材取得。','','## 隔離與待審','','只對c14執行正常prepare-runtime，root '+RUNTIME+'；media base /workspace/work/brand-story-20261025/media。正常初始化自己的不可變字典，不借其他集snapshot/核准；不得覆蓋已批准runtime。原生loadProject/lintProject僅機械診斷，不能視為來源、敘事或owner自審。無verify、approve、provider、backend mutation、git或spawn。獨立來源/書面圖、新讀者、讀音/實聲、生成圖/聲圖ownerQA均待辦。',''].join('\n');
fs.writeFileSync(path.join(OUT,'brief.md'),brief);
for(const f of protectedFiles)assert.equal(fileSha(f.path),f.sha256,f.path);assert.equal(fileSha(voiceSource),voiceSourceSha);
const timeline=estimateTimeline(doc);
const shots=timeline.scenes.filter(s=>doc.scenes.find(x=>x.id===s.id)?.template==='shot');
const maxShot=Math.max(...shots.map(s=>(s.end_frame-s.start_frame)/FPS));
const lineMap=new Map([...eachLine(doc)].map(({line})=>[line.id,line]));
const outroAt=timeline.scenes.at(-1).start_frame/FPS;
const questionStarts=timeline.lines.filter(l=>/[？?][」”]?$/.test(lineMap.get(l.id).text)&&l.start_frame/FPS<outroAt).map(l=>l.start_frame/FPS);
const cadencePoints=[...new Set([0,...questionStarts,...timeline.chapters.map(c=>c.start_frame/FPS),outroAt])].sort((a,b)=>a-b);
const maximumQuestionOrChapterGap=Math.max(...cadencePoints.slice(1).map((p,i)=>p-cadencePoints[i]));
assert(maximumQuestionOrChapterGap<=45,maximumQuestionOrChapterGap);
const info={schema_version:1,candidate_revision:'c14-r2',author:'/root/c05_r10_author',author_is_original_researcher:true,status:'DRAFT_HOLD_PENDING_INITIALIZED_NATIVE_DIAGNOSTICS_AND_INDEPENDENT_QA',slug:SLUG,counts:{lines:rows.length,scenes:scenes.length,chapters:new Set(materials.chapters.map(c=>c.title)).size,illustrations:shots.length,cards:1,loops:loops.length,source_documents:usedSources.length,anchors:usedAnchors.length,evidence_bindings:claims.reduce((n,c)=>n+c.evidence.length,0),rows_with_source:claims.filter(c=>c.anchor_ids.length).length,editorial_CTA_without_historical_claims:2},native_units:{counter:'spokenUnits(spokenText(line))',official_narration_body_planning_units:total,coldopen,voiced_CTA:CTA,after_opening_planning_only:total-coldopen,after_opening_and_CTA_planning_only:total-coldopen-CTA,official_duration_scope:'all actual narration including coldopen and voiced CTA; excludes separately added 5s/21s channel bookends',arithmetic_seconds_at_4_to_5:[total/5,total/4],at_4_5_units_per_second:total/4.5,actual_tts_seconds:null,actual_duration_verified:false,length_hold:true,length_hold_reason:'有效內容未達rough3500；字量不等時長，正常4–5units/s算術低於720–840s實聲目標。資料/結果不足不補警語、重述、慢播或支線。'},maximum_estimated_shot_seconds:maxShot,estimated_cadence:{basis:'DEFAULT_CPM250 planning only, not actual voice',questions_or_chapter_starts:cadencePoints,maximum_gap_seconds:maximumQuestionOrChapterGap,actual_audio_cadence_pending:true},source_bindings:{source_ids:usedSources,anchor_ids:usedAnchors,author_added_locators_existing_raw_only:usedAnchors.filter(a=>a.startsWith('A_')),all_fifteen_frozen_raw_http_status_bytes_sha_and_text_hashes_match:true,all_32_current_anchor_context_quote_hashes_match:true,background_company_1989_A01_separate:true,frozen_research_sha256:RESEARCH_SHA},protected_inputs:{old_files:35,readonly_snapshots:35,original_and_snapshot_hashes_unchanged:true,snapshot_manifest_sha256:preservation.snapshot_manifest_sha256,research_files:3,research_unchanged:true,files:protectedFiles},voice_source:{path:voiceSource,file_sha256:voiceSourceSha,voice_object_sha256:sha(JSON.stringify(voice)),exact_copy:true,pronunciation_audition_pending:true},execution_recipe:{image_model:'image-01',look:{preset:'cute-mystery'},stillmotion:true,minimum_body_illustration_share:0.70,maximum_consecutive_cards:3,planned_illustration_spoken_unit_share:(total-CTA)/total,burn_in_zh_tw:true,cc_zh_tw:true,intro:{seconds:5,placement:'after coldopen',executed:false},outro:{seconds:21,version:'formal-v4',placement:'after voiced CTA',executed:false},media_obtained_or_generated:false},runtime_root:RUNTIME,series_rebind:false,approval_created:false,verify_written:false,source_pass_claimed:false,narrative_pass_claimed:false,owner_approval:false,provider_calls:0,paid_calls:0,backend_mutations:0,git_commands:0,subagents_spawned:0};
if(!process.argv.includes('--draft')){
 const project=loadProject({root:RUNTIME,slug:SLUG});assert.equal(fileSha(project.file),fileSha(path.join(OUT,'video.json')));
 const lexBefore=sha(JSON.stringify(project.shelfLexicon));const lint=lintProject(project);assert.equal(sha(JSON.stringify(project.shelfLexicon)),lexBefore);
 const cadence=lint.warnings.filter(w=>/no open loop|no hook between|open loops? planted|condensation plants/.test(w.message));
 info.native_proper_context={root:RUNTIME,slug:SLUG,scope:'Initialized native mechanical lint only, not a source/narrative/owner review.',runtime_video_sha256:fileSha(project.file),immutable_lexicon_sha256:lexBefore,lexicon_not_overwritten:true,result:lint,errors:lint.errors.length,cadence_warnings:cadence,maximum_estimated_shot_seconds:maxShot};
 assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));assert.equal(cadence.length,0,JSON.stringify(cadence));assert(maxShot<=12,maxShot);
 const manifest=read(path.join(RUNTIME,'runtime-manifest.json'));assert.deepEqual(manifest.projects.map(p=>p.id),['c14']);
 info.runtime_preparation={helper:path.join(OUT,'prepare-runtime.mjs'),runtime_manifest_sha256:fileSha(path.join(RUNTIME,'runtime-manifest.json')),prepared_project_ids:['c14'],ordinary_immutable_lexicon_initialization:true,other_episode_dictionary_or_approval_copied:false,approvals_created:0,paid_media_created:false};
 info.status='HOLD_PENDING_INDEPENDENT_SOURCE_FRESH_READERS_AND_ACTUAL_DURATION';
}
info.at_least_eight_concrete_action_payoff_bindings=loops.filter(l=>['c14r1h04','c14r1h06','c14r1o07','c14r1v08','c14r1v10','c14r1v13','c14r1v18','c14r1t04','c14r1t11','c14r1m03','c14r1r04','c14r1r08','c14r1d05','c14r1d08','c14r1d11'].includes(l.setup)).map(l=>({...l,status:'AUTHOR_INTENT_PENDING_INDEPENDENT_JUDGMENT'}));
const sourceRevisionFile=path.join(OUT,'source2revision.json');
if(fs.existsSync(sourceRevisionFile)){
 const revision=read(sourceRevisionFile);
 if(revision.status==='AUTHOR_R2_TWO_REQUIRED_SOURCE_WORDING_CORRECTIONS_COMPLETED_PENDING_INDEPENDENT_DELTA_REVIEW'){
  for(const f of revision.protected_before)assert.equal(fileSha(f.path),f.sha256,f.path);
  info.source2revision={path:sourceRevisionFile,sha256:fileSha(sourceRevisionFile),changed_line_ids:revision.required_corrections.map(c=>c.line_id),spoken_units_delta:revision.native_units.delta,independent_delta_review_pending:true,r1_actual_native_panel_executed:false,next_actual_native_panel:1};
 }
}
info.file_sha256=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','author-materials.json','build-candidate.mjs','prepare-runtime.mjs',...(info.source2revision?['source2revision.json']:[])].map(f=>[f,fileSha(path.join(OUT,f))]));
info.review_four_sha256=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(f=>[f,info.file_sha256[f]]));info.frozen_at_utc=new Date().toISOString();write('author-notes.json',info);
console.log(JSON.stringify({status:info.status,counts:info.counts,native_units:info.native_units,max_estimated_shot_seconds:maxShot,native_proper_context:info.native_proper_context?{errors:info.native_proper_context.errors,cadence:info.native_proper_context.cadence_warnings}:null,review_four_sha256:info.review_four_sha256},null,2));
