import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const args=Object.fromEntries(process.argv.slice(2).reduce((a,x,i,all)=>x.startsWith('--')?[...a,[x.slice(2),all[i+1]]]:a,[]));
assert(args.repo&&args.out&&args.lexicon,'--repo --out --lexicon required; only new offline output directory');
const repo=path.resolve(args.repo),out=path.resolve(args.out),lexFile=path.resolve(args.lexicon);
assert(!fs.existsSync(out),'refuse to overwrite existing output');
assert(!out.startsWith(path.join(repo,'tools')));
const hash=b=>createHash('sha256').update(b).digest('hex');
const fh=f=>hash(fs.readFileSync(f));
const rr=p=>JSON.parse(fs.readFileSync(path.join(repo,p),'utf8'));
const clone=structuredClone;
const base='docs/videos/brand-stories-pilot-v2-20261015',pre=`${base}/preproduction-20261016`;
const board=rr(`${pre}/B18-storyboard/storyboard.json`);
const paragraphs=rr(`${pre}/B18-10min-narration-candidate-v2/paragraphs.json`).paragraphs;
const checklist=rr(`${pre}/B18-worker-conversion-plan/claim-checklist.json`).rows;
const sourceMap=rr(`${pre}/B18-storyboard/source-map.json`);
const bundle=rr(`${base}/stories.json`),row=bundle.stories.find(s=>s.id==='B18'),seriesInput=rr(`${base}/series.json`);
const sourcePins={...rr(`${pre}/B18-worker-conversion-plan/source-pins.json`).files};
for(const [p,h]of Object.entries(sourcePins))assert.equal(fh(path.join(repo,p)),h,p);
for(const p of [`${base}/series.json`,`${pre}/B18-worker-conversion-plan/claim-checklist.json`,`${pre}/B18-worker-conversion-plan/shot-impact.json`,'tools/video/core/state.mjs','tools/video/core/schema.mjs','tools/video/core/lint.mjs','tools/video/core/timeline.mjs','tools/video/core/drama.mjs','tools/video/core/branding.mjs','tools/video/templates/theme.css','.agents/skills/animation-camera/scripts/shot_reading.mjs','.agents/skills/curio-episode/SKILL.md'])sourcePins[p]=fh(path.join(repo,p));
const voicePath='docs/videos/brand-stories-five-20261014/drafts-20261016/formal-prototypes/A29/initial-stats/series.json';
sourcePins[voicePath]=fh(path.join(repo,voicePath));
assert.equal(fh(lexFile),'ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9');
assert.equal(fh(path.join(repo,`${pre}/B18-10min-narration-candidate-v2/paragraphs.json`)),'a27492b74b84f4bd1e10ce9eeb83ef53a58e38fbb8544b58357034533877525a');
let externalCalls=0;
const forbid=name=>()=>{externalCalls++;throw new Error(`OFFLINE CANDIDATE forbids ${name}`);};
globalThis.fetch=forbid('fetch');
const mod=p=>import(pathToFileURL(path.join(repo,p)).href);
const {composeStory,storySeriesFile,storyCast,storyBrief,advanceStory,cuteStoryVisualProblems,readChapterAnswer}=await mod('tools/video/automation/story.mjs');
const {loadProject,lintProject}=await mod('tools/video/core/state.mjs');
const {spokenUnits,estimateTimeline,FPS}=await mod('tools/video/core/timeline.mjs');
const {slideHtml,visibleText,TEMPLATE_SPECS}=await mod('tools/video/templates/templates.mjs');
const {readDocument}=await mod('.agents/skills/animation-camera/scripts/shot_reading.mjs');
const voice=rr(voicePath).characters[0].voice;
const episode=Object.fromEntries(['number','title','logline','slug'].map(k=>[k,clone(row[k])]));
const plan=Object.fromEntries(Object.entries(row).filter(([k])=>!['number','title','logline','slug'].includes(k)));
const cast=storyCast(plan,voice),info=storySeriesFile({series:seriesInput,episode,plan,cast});
const keys=['hook','origin','idea','engine','turn','now'];
const titles=Object.fromEntries([...fs.readFileSync(path.join(repo,`${pre}/B18-10min-narration-candidate-v2/candidate.md`),'utf8').matchAll(/^## (hook|origin|idea|engine|turn|now)｜([^\r\n]+)/gm)].map(m=>[m[1],m[2]]));
const shots=new Map(board.shots.map(s=>[Number(s.id.slice(-3)),s]));
// Only segmentation changes below: concatenation must equal all reviewed v2 paragraphs exactly.
const edits={
 O01:[[8,'一九四七年，白石從愛媛搬到大阪布施，開了一間料理店。後來店裡也賣壽司。'],[9,'他想讓附近工廠的年輕工人和學生，不必等到特別的日子，'],[10,'也吃得起這一口。於是客人站著吃，一盤四貫，二十日圓。']],
 O02:[[11,'當年壽司常是節慶才吃的料理。白石把價錢寫清楚，'],[12,'還比別家便宜約三成，客人多了起來。'],[14,'可每多一位客人，師傅就得多遞一次盤子；握好的壽司，還是靠人送到面前。']],
 O03:[[15,'發明協會記載，湧進的訂單已超過師傅能握壽司的量；'],[16,'年輕師傅工作太累，沒多久就離開。'],[18,'缺人讓出餐更吃緊，也讓每盤手遞的瓶頸更明顯。'],[19,'即使多找人握壽司，盤子仍要有人送。白石至少得先改掉送盤的方法。']],
 I04:[[33,'從工廠參觀到試作機完成，前後約十年。'],[34,'一九五七年，白石與附近工廠做出「輸送帶旋轉式餐台」試作機；'],[35,'轉彎之外，還得選不易生鏽的材料。'],[37,'兒子博志回憶，父親預先付材料費給協作工廠；'],[38,'他認為這或許讓對方願意幫忙。'],[39,'工廠給的是送瓶子的想法，適合壽司吧台的路，仍靠反覆試作做出來。'],[40,'機器能繞一圈了，店門還沒開。']],
 E01:[[41,'一九五八年四月，近鐵布施站附近，「廻る元禄寿司」第一家店開門。'],[42,'店大約二十坪，只有吧台座位。壽司一盤一盤放上帶子，走到客人面前，客人自己伸手拿。'],[43,'白石終於把「把盤子送到人面前」這件事，從師傅的手裡交給機器。']],
 E03:[[47,'第一家店熱鬧之後，問題換了。這個做法別人看得見，也可能照著做。'],[48,'一九六〇年，第二家店開到大阪道頓堀；白石自己的版圖在長大。'],[49,'一九六二年，輸送帶系統以白石個人名義登記為「實用新案」，'],[50,'名字叫「附輸送帶的料理台」。它保護的是這套裝置的做法，不是壽司本身。']],
 E04:[[51,'元祿壽司因此能替自己的輸送帶守住一段時間。'],[52,'當時碰上相似的店，它在東京和大阪聘律師及專利代理人，發出警告。'],[53,'那段日子，提到迴轉壽司，幾乎就是提到元祿壽司。'],[54,'不過，法律能守住一種裝置，還不能讓全國的人都看過這種店。']],
 E05:[[55,'開場的萬博會場，真的迎來元祿壽司。'],[56,'地方商工會議所邀請東大阪業者，'],[57,'白石把店開在會場單軌列車西口站前。'],[58,'客人愈來愈多，忙到無法按魚料慢慢出餐；'],[59,'於是把三百日圓的握壽司套組裝進壽司桶，放上輸送帶。'],[60,'這不是首店五十日圓四貫的餐盤。'],[61,'兒子博志回憶，自己暑假去幫忙，剝蝦、剪海苔都忙個不停。'],[62,'原先減少遞盤人手的機器，此時接住了會場客流。']],
 T01:[[63,'萬博出店受到表彰。發明協會說，迴轉壽司因此在全國打開知名度；'],[65,'日本中小企業基盤整備機構也記錄，會場迎來外國客人。'],[66,'這種原先在小店裡運轉的輸送帶，讓更多地方的人看見。'],[68,'元祿壽司後來靠加盟擴到約兩百四十家，但主要仍在同一品牌與權利之下。'],[70,'盤子會自己送，茶呢？']],
 T01a:[[71,'一九七一年，石野製作所供應元祿壽司自動給茶裝置，'],[72,'客人用杯子就能接茶；'],[73,'一九七四年，這家公司把它和輸送帶組成一套設備。'],[75,'送餐與喝茶，都成了設備商繼續改良的題目。'],[76,'可白石保護裝置的那項權利，會走到哪一步？']],
 T02:[[77,'開場那項走到期限的權利，就是白石登記的實用新案。'],[78,'一九七八年，它期滿了。這時候，原先由元祿壽司幾乎獨占的市場，出現了更多經營者。'],[79,'大批新業者進入迴轉壽司市場；原本的加盟店，也有人獨立，換上自己的招牌。']],
 T03:[[80,'權利期滿不是全國才開始吃迴轉壽司：'],[81,'萬博已讓許多人認識，元祿壽司也早在展店。'],[83,'新業者進來後，有些店把繞吧台的輸送帶改成直線，從後場送到用餐區。'],[84,'白石花多年解決的轉角，不再是每一家店都得保留的地方。']],
 T04:[[85,'同一條送餐路，連客人伸手拿盤時要付多少錢，也開始有新答案。'],[86,'新進的店在競爭裡試著把魚料從漁民或漁協直接買來；'],[87,'有些店不再讓每盤都賣同一個價，而是用不同顏色的盤子標明價位。'],[88,'客人看盤子，既看想吃哪種壽司，也看這盤的價錢。'],[89,'到了八〇年代中期，郊區出現更大的迴轉壽司店；'],[90,'八〇年代後期，它也成了家庭一起用餐的地方。從白石一人想把盤子送得更快，'],[91,'走到店與店比採購、比價格、比誰能讓一家人坐得下，這條路已經換了好多種走法。'],[92,'後來，連這種吃法的名字，也有了一個意想不到的去處。']],
 N01:[[93,'一九九一年，「迴轉壽司」這個詞收進《廣辭苑》第四版。'],[94,'當年讓路人停在店外看熱鬧的吃法，現在成了一個字典詞條。'],[95,'二〇二一年，日本機械學會把一台一九八五年製造、當時仍在元祿壽司堺東店使用的輸送機，'],[96,'列為第一百一十二號機械遺產；一起被認定的，還有早期那種叫「魚鱗板」的轉彎板片。']],
 N02:[[97,'二〇二三年的報導引用富士經濟調查：'],[98,'二〇二二年市場規模是七千兩百五十二億日圓；二〇二三年超過七千五百億，是當時的預估，'],[99,'不是今天的實績。這些數字，已經離布施那家二十坪小店很遠。'],[100,'可它們指回的，仍是同一個送餐問題：一盤壽司，怎麼走到你面前。']],
 N03:[[101,'那盤壽司先學會轉彎，後來走出元祿壽司自己的店；'],[101,'二〇二三年的報導記下，日本已有四千多家迴轉壽司店。','b'],[102,'你吃迴轉壽司時，會先拿眼前那盤，還是等最想吃的那盤轉過來？'],[103,'喜歡聽熟悉事物怎麼一步步變成今天的樣子，歡迎訂閱。']]
};
// Move overlay text onto an adjacent existing native source/number card where its window matches.
// Three necessary name/source cards replace only the original 032,061,095 illustration placements.
const overlayDest={28:27,29:27,32:32,35:33,37:38,61:61,95:95,96:95,97:98};
const toCard=new Set([32,61,95]);
const sourceDisplay=s=>s.replace(/（S\d(?:／S\d)*）/g,'').replace(/S0/g,'J-Net21').replace(/S1/g,'日本機械學會').replace(/S2/g,'發明協會').replace(/S3/g,'Wikipedia');
const dataForCard=n=>{
 const s=shots.get(n),overlay=Object.entries(overlayDest).filter(([,dest])=>dest===n).map(([origin])=>shots.get(Number(origin)).post_source_overlay);
 const original=s.card;
 const data=original?{title:original.text,subtitle:original.scope,tag:sourceDisplay(original.source)}:
  {title:n===32?'魚鱗板（ウロコ）':n===61?'博志的回憶':'1985 年製；2021 認定時使用中',subtitle:'',tag:sourceDisplay(s.post_source_overlay.source)};
 for(const ov of overlay){if(![data.title,data.subtitle].some(v=>v.includes(ov.scope)))data.subtitle=[data.subtitle,ov.scope].filter(Boolean).join('\n');}
 if(!data.subtitle)delete data.subtitle;
 return data;
};
const chunks=text=>{const out=[];let start=0;while(start<text.length){let end=Math.min(start+40,text.length);if(end<text.length){const prefix=text.slice(start,end);const cuts=[...prefix.matchAll(/[，。；！？：]/g)].map(m=>m.index+1).filter(n=>n>=12);if(cuts.length)end=start+cuts.at(-1);}out.push({start,end,text:text.slice(start,end)});start=end;}return out;};
const chapters=Object.fromEntries(keys.map(key=>[key,{key,title:titles[key],scenes:[],claims:[],loops:[]}]));
const sceneMap=[],lineMap=[],cardMap=[],imageMap=[],claimMap=[],overlayMap=[];
const ids=new Set();
for(const p of paragraphs){
 const items=edits[p.id]??board.shots.filter(s=>s.narration_refs.some(r=>r.paragraph_id===p.id)).map(s=>[Number(s.id.slice(-3)),s.narration_refs.filter(r=>r.paragraph_id===p.id).map(r=>r.text).join('')]);
 assert.equal(items.map(x=>x[1]).join(''),p.text,`exact ${p.id}`);
 let offset=0;
 for(const [number,text,suffix='']of items){
  const original=shots.get(number);assert(original);
  const sceneId=`${p.chapter}-s${String(number).padStart(3,'0')}${suffix}`;
  const lines=chunks(text).map(part=>{const start=offset+part.start,end=offset+part.end;const id=hash(`B18\0${p.id}\0${start}\0${part.text}`).slice(0,8);assert(!ids.has(id));ids.add(id);
   lineMap.push({line_id:id,scene_id:sceneId,paragraph_id:p.id,chapter:p.chapter,start_utf16:start,end_utf16:end,text:part.text,source_cids:p.source_cids,original_shot_id:original.id});return {id,text:part.text};});
  offset+=text.length;
  const isCard=Boolean(original.card)||toCard.has(number);
  const data=isCard?dataForCard(number):{prompt:original.prompt,camera:suffix?'Medium shot, drift':original.camera,visual:'still'};
  const scene={id:sceneId,template:isCard?'title':'shot',data,lines};chapters[p.chapter].scenes.push(scene);
  sceneMap.push({scene_id:sceneId,paragraph_id:p.id,original_shot_id:original.id,original_type:original.type,native_template:scene.template,
   paragraph_start_utf16:offset-text.length,paragraph_end_utf16:offset,visual_change:toCard.has(number)?'ILLUSTRATION_TO_NATIVE_SOURCE_CARD':suffix?'SPLIT_SAME_IMAGE_WITH_POST_CAMERA':original.card?'NATIVE_TITLE_CARD_ADAPTER':'ORIGINAL_ILLUSTRATION',original_visual:clone(original)});
  if(isCard)cardMap.push({scene_id:sceneId,original_shot_id:original.id,original_card:original.card??null,data:clone(data),overlay_sources:Object.entries(overlayDest).filter(([,dest])=>dest===number).map(([n])=>shots.get(Number(n)).id)});
  else imageMap.push({scene_id:sceneId,original_shot_id:original.id,prompt:data.prompt,camera:data.camera,image_asset_key:original.image_asset_key,actual_image_sha256:null,camera_changed:Boolean(suffix)});
 }
 assert.equal(offset,p.text.length);
}
for(const [origin,dest]of Object.entries(overlayDest)){
 const s=shots.get(Number(origin));const target=cardMap.find(c=>c.original_shot_id===shots.get(dest).id);assert(target);
 assert([target.data.title,target.data.subtitle??''].some(t=>t.includes(s.post_source_overlay.scope)),`overlay scope ${origin}`);
 overlayMap.push({original_shot_id:s.id,original_overlay:s.post_source_overlay,native_card_scene_id:target.scene_id,visible_scope_preserved:true,original_illustration_retained:imageMap.some(m=>m.original_shot_id===s.id),
  adaptation:origin===String(dest)?'NATIVE_SOURCE_CARD_AT_ORIGINAL_WINDOW':'ATTRIBUTION_MOVED_TO_NEARBY_NATIVE_CARD_SPOKEN_SCOPE_UNCHANGED',review:'PENDING_INDEPENDENT_VISUAL_MAPPING_REVIEW'});
}
// Bind each atomic checklist to its exact voiced span. Cross-scene context is retained explicitly.
const prefixes={hook:'h',origin:'o',idea:'i',engine:'e',turn:'t',now:'n'};
for(const c of checklist){
 const segments=lineMap.filter(l=>l.paragraph_id===c.paragraph_id&&l.start_utf16<c.end_utf16&&l.end_utf16>c.start_utf16);
 assert(segments.length);const scenes=[...new Set(segments.map(l=>l.scene_id))];
 const chapter=chapters[c.chapter],id=`${prefixes[c.chapter]}${chapter.claims.length+1}`;
 const needsPassage=['B18-PC-I01-2','B18-PC-I04-2'].includes(c.planning_id);
 const native={id,claim:c.quote,scene:scenes[0],source:c.source_index_zero_based,fact:needsPassage?null:c.fact_index_zero_based,verdict:'UNCHECKED',note:`作者映射待真查核；${c.paragraph_id}／${c.cid}。${c.source_boundary}${needsPassage?' 此句還含附近工廠協作／試作機專名，超出必查fact3的文字；整列fact=null，須取真來源段落。':''}${scenes.length>1?' 主張跨鏡，上下文line與scene完整保留於mapping。':''}`};
 chapter.claims.push(native);claimMap.push({planning_id:c.planning_id,claim_id:id,paragraph_id:c.paragraph_id,source_cid:c.cid,native:clone(native),start_utf16:c.start_utf16,end_utf16:c.end_utf16,all_line_ids:segments.map(l=>l.line_id),all_scene_ids:scenes,source_boundary:c.source_boundary,
  fact_boundary_adjustment:needsPassage?{from:c.fact_index_zero_based,to:null,reason:'Checklist broad fact3 does not itself cover the complete nearby-factory / prototype-name statement. Require source passage rather than claiming full plan support.'}:null});
}
const para=id=>paragraphs.find(p=>p.id===id);
const lineAt=(pid,at)=>lineMap.find(l=>l.paragraph_id===pid&&l.start_utf16<=at&&l.end_utf16>at);
const anchor=(pid,quote,last=true)=>{const at=para(pid).text.indexOf(quote);assert(at>=0,`${pid} ${quote}`);return lineAt(pid,at+(last?quote.length-1:0));};
const loopSpecs=[
 ['H01','要是盤子也能自己送過去呢？','O04','客人坐在原位就能伸手拿到；','工廠輸送的想法如何接到客人取盤',['O04']],
 ['H02','那道彎究竟怎麼走通？','I03','讓輸送帶繞過吧台角落；','轉角卡住如何解開',['I01','I03','I04','E01']],
 ['H02','會場的人會怎麼看？','T01','迴轉壽司因此在全國打開知名度；','萬博會場的反應與後續知名度',['E05','T01']],
 ['H02','接下來又會有誰走進這門生意？','T02','大批新業者進入迴轉壽司市場；','權利期滿後誰加入經營',['T02','T03']],
 ['H03','變成大家熟悉的壽司吧台？','N03','後來走出元祿壽司自己的店；','送盤的做法如何走出自家店',['N03']],
 ['O04','還能平穩地走嗎？','I03','讓輸送帶繞過吧台角落；','循環吧台如何轉彎',['I01','I03']],
 ['I04','店門還沒開。','E01','第一家店開門。','試作機何時進入真正店面',['E01']],
 ['E04','還不能讓全國的人都看過這種店。','T01','迴轉壽司因此在全國打開知名度；','如何讓各地的人看見這種吃法',['E05','T01']],
 ['T01','茶呢？','T01a','客人用杯子就能接茶；','送盤之外如何供茶',['T01a']],
 ['T01a','會走到哪一步？','T02','一九七八年，它期滿了。','保護裝置的權利何時到期',['T02']],
 ['T04','有了一個意想不到的去處。','N01','收進《廣辭苑》第四版。','這種吃法的名字去了哪裡',['N01']]
];
const loopMap=[];
for(const [sp,sq,pp,pq,what,window]of loopSpecs){const setup=anchor(sp,sq),payoff=anchor(pp,pq);assert(setup&&payoff);const native={setup:setup.line_id,payoff:payoff.line_id,what};
 assert(lineMap.indexOf(payoff)>lineMap.indexOf(setup));
 if(setup.chapter!==payoff.chapter)chapters[setup.chapter].loops.push({setup:native.setup,what});
 chapters[payoff.chapter].loops.push(native);loopMap.push({native,setup_paragraph:sp,setup_quote:sq,payoff_paragraph:pp,payoff_quote:pq,full_payoff_paragraph_window:window,full_payoff_line_ids:lineMap.filter(l=>window.includes(l.paragraph_id)).map(l=>l.line_id)});
}
assert.equal(new Set(loopMap.map(l=>l.native.setup)).size,loopMap.length,'no collapsed H02 setups');
chapters.hook.thumbnail_shot=chapters.hook.scenes.find(s=>s.template==='shot').id;
const imagePairs=board.hook_visual_reuse.map(pair=>{
 const a=imageMap.find(m=>m.original_shot_id===pair.setup_shot),b=imageMap.find(m=>m.original_shot_id===pair.recovery_shot);assert(a&&b);
 for(const k of ['prompt','camera','image_asset_key'])assert.equal(a[k],b[k],`${pair.asset_key} ${k}`);
 return {original:pair,setup_scene_id:a.scene_id,payoff_scene_id:b.scene_id,same_prompt_camera_key:true,actual_same_file_verified:null};
});
const retainedIds=new Set(sceneMap.map(m=>m.original_shot_id));
const retired=board.shots.filter(s=>!retainedIds.has(s.id)).map(s=>({original:clone(s),reason:'V2文字已收斂；其必要事實與卡片由新的逐字分配保留，不以空畫面或加停頓維持鏡數。'}));
const write=(rel,data)=>{const f=path.join(out,rel);assert(f.startsWith(out+path.sep));fs.mkdirSync(path.dirname(f),{recursive:true});fs.writeFileSync(f,typeof data==='string'?data:JSON.stringify(data,null,2)+'\n');};
write('input-pins.json',{schema_version:1,base:'repository_root',files:sourcePins,lexicon:{file:'fixtures/lexicon.json',sha256:fh(lexFile),meaning:'Saved 2026-10-15 host lexicon snapshot, not refreshed live; no entries changed.'},voice:{file:voicePath,sha256:sourcePins[voicePath],production_voice_approval:false}});
write('fixtures/lexicon.json',fs.readFileSync(lexFile,'utf8'));
write('series.json',info);write('worker-row-reference.json',row);write('series-input-reference.json',seriesInput);
for(const key of keys)write(`chapters/${key}.json`,chapters[key]);
write('mapping.json',{schema_version:1,status:'OFFLINE_AUTHORED_CANDIDATE_PENDING_INDEPENDENT_REVIEW',paragraphs:clone(paragraphs),scenes:sceneMap,lines:lineMap,claims:claimMap,cards:cardMap,source_overlays:overlayMap,images:imageMap,image_reuse:imagePairs,loops:loopMap,retired_original_shots:retired,
 source_index_namespace:sourceMap.sources,end_visual_reuse:{original:board.end_visual_reuse,native_scene_ids:imageMap.filter(i=>board.end_visual_reuse.shot_ids.includes(i.original_shot_id)).map(i=>i.scene_id),actual_same_file_verified:null},bookends:board.bookends,
 cast_policy:'Keep exact compiled plan cast; no native shot binds a real person or synthesizes a look sheet.',narration_text_changed:false,worker_pass:false});
const syntheticRoot=path.join(out,'synthetic/docroot'),work=path.join(out,'synthetic/work',row.slug),docRel=`synthetic/docroot/docs/videos/${row.slug}`;
write(`${docRel}/series.json`,info);write(`${docRel}/brief.md`,storyBrief({episode,plan,cast,look:seriesInput.look}));
write('synthetic/docroot/docs/videos/lexicon.json',fs.readFileSync(lexFile,'utf8'));
for(const key of keys)write(`synthetic/work/${row.slug}/story/chapters/${key}.json`,chapters[key]);
const state={slug:row.slug,title:row.title,premise:row.question,status:'blocked',blocked:'LOCAL_AUTHORED_CANDIDATE_NOT_HOST_STATE',verified:false,listener_done:false,verify_rounds:0,notes:[],story:{id:'B18',narrative_fixes:0,chapters:Object.fromEntries(keys.map(key=>[key,{written:1,lint:null,lint_fixes:0,checked:false,check_rounds:0,listened:false,changed:0}]))}};
write('synthetic/LOCAL-FIXTURE-NOT-PRODUCTION-STATE.json',{purpose:'Only invoke existing offline relint. No host state or gate receipts are imported or created. written=1 is a local fixture, not authority to set it on a worker.',state});
const automation={ctx:{root:syntheticRoot},settings:{drama:{music_enabled:false}},workdir:slug=>{assert.equal(slug,row.slug);return work;},voice:()=>clone(voice),persist:s=>write('synthetic/relint-state-observation.json',s),stage:forbid('model'),report:forbid('host'),reference:forbid('reference'),cleared:forbid('advance'),api:new Proxy({},{get:(_,n)=>forbid(`api:${String(n)}`)}),block:(_s,reason)=>`BLOCKED: ${reason}`};
const result=await advanceStory(automation,state,'script passes lint');
const project=loadProject({slug:row.slug,root:syntheticRoot}),doc=project.doc,lint=lintProject(project),cute=cuteStoryVisualProblems(doc),timeline=estimateTimeline(doc);
assert.deepEqual(composeStory({slug:row.slug,info,chapters,voice,drama:{music_enabled:false},root:syntheticRoot}),doc);
assert.deepEqual(doc.scenes.flatMap(s=>s.lines.map(l=>l.text)),lineMap.map(l=>l.text));
for(const p of paragraphs){const ls=lineMap.filter(l=>l.paragraph_id===p.id);assert.equal(ls.map(l=>l.text).join(''),p.text);let end=0;for(const l of ls){assert.equal(l.start_utf16,end);end=l.end_utf16;}assert.equal(end,p.text.length);}
assert.equal(doc.scenes.flatMap(s=>s.lines.map(l=>l.text)).join(''),paragraphs.map(p=>p.text).join(''));
assert.equal(doc.loops.length,loopMap.length);assert.equal(doc.subtitles.burn_in,false);assert.deepEqual(doc.look,{preset:'cute-mystery'});
assert(Object.values(chapters).every(c=>c.claims.every(r=>r.verdict==='UNCHECKED')));
assert(!fs.existsSync(path.join(work,'auto.json')));assert(!fs.existsSync(path.join(work,'approvals.json')));assert(!fs.existsSync(path.join(out,docRel,'verify-1.md')));
const parser=Object.fromEntries(keys.map(key=>{const got=readChapterAnswer(chapters[key],{key,ids:chapters[key].scenes.flatMap(s=>s.lines.map(l=>l.id)),cast,sources:plan.sources.length,facts:plan.must_verify.length});return [key,{accepted:!got.problem,problem:got.problem??null}];}));
const cardEvidence=cardMap.map(c=>{const errors=TEMPLATE_SPECS.title.check(c.data).filter(Boolean);const html=slideHtml({id:c.scene_id,template:'title',data:c.data,lines:[]},{first:true,reveal:0,previousReveal:0});const visible=visibleText(html);assert.deepEqual(errors,[]);for(const t of Object.values(c.data))assert(visible.includes(t.replace(/\n/g,' '))||t.split('\n').every(s=>visible.includes(s)));return {scene_id:c.scene_id,data:c.data,template_errors:errors,html_sha256:hash(html),visible_text:visible,all_display_fields_visible:true,pixel_layout_checked:false};});
write('card-adapter-evidence.json',{status:'NATIVE_HTML_TEXT_NOT_PIXEL_QA',cards:cardEvidence,source_overlays:overlayMap});
const shotReading=readDocument(doc,{file:`synthetic/docroot/docs/videos/${row.slug}/video.json`});write('shot-reading-evidence.json',shotReading);
let maxCards=0,run=0;for(const s of doc.scenes){run=s.template==='shot'?0:run+1;maxCards=Math.max(run,maxCards);}
const editorUnits=paragraphs.map(p=>p.text).join('').replace(/[\p{P}\p{S}\p{Z}\s]/gu,'').length;
const officialUnits=paragraphs.reduce((n,p)=>n+spokenUnits(p.text),0);
const sceneTimes=timeline.scenes.map(s=>({id:s.id,template:s.template,estimated_seconds:(s.end_frame-s.start_frame)/FPS}));
const evidence={schema_version:1,status:'OFFLINE_AUTHORED_CANDIDATE_WITH_REMAINING_WORK',result,paragraphs:24,editorial_units:editorUnits,official_spoken_units:officialUnits,narration_lines:lineMap.length,scenes:doc.scenes.length,illustrations:imageMap.length,cards:cardMap.length,original_cards_preserved:16,source_overlays_adapted:overlayMap.length,physical_illustration_percent:imageMap.length/doc.scenes.length*100,max_consecutive_cards:maxCards,claims:claimMap.length,cross_scene_claims:claimMap.filter(c=>c.all_scene_ids.length>1),loops:doc.loops.length,exact_paragraph_reconstruction:true,narration_text_changed:false,
 lint,cute_errors:cute,writer_reader:parser,shot_reading:shotReading.summary,scene_timing:sceneTimes,estimated_body_seconds:timeline.total_frames/FPS,measured_body_seconds:null,manual_pause_fields:0,bookends_separate_seconds:26,
 source_files_unchanged:true,source_file_count:Object.keys(sourcePins).length,source_fetches:0,model_calls:0,external_calls:externalCalls,media_calls:0,host_access:false,worker_pass:false};
for(const [p,h]of Object.entries(sourcePins))assert.equal(fh(path.join(repo,p)),h,p);assert.equal(externalCalls,0);
write('compose-lint-evidence.json',evidence);write('synthetic/timeline-estimate.json',timeline);
write('READABLE-SCRIPT.md',paragraphs.map(p=>`## ${p.chapter} / ${p.id}\n\n${p.text}`).join('\n\n')+'\n');
write('build-offline.mjs',fs.readFileSync(fileURLToPath(import.meta.url),'utf8'));
const walk=(dir,start=dir)=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name),start):[path.relative(start,path.join(dir,e.name)).split(path.sep).join('/')]);
write('output-pins.json',{schema_version:1,status:'OFFLINE_CANDIDATE_NOT_APPROVAL',files:Object.fromEntries(walk(out).map(p=>[p,fh(path.join(out,p))]))});
console.log(JSON.stringify({scenes:doc.scenes.length,lines:lineMap.length,illustrations:imageMap.length,cards:cardMap.length,maxCards,physical_percent:evidence.physical_illustration_percent,lint_errors:lint.errors,cute_errors:cute,shot_reading:shotReading.summary,cross_scene_claims:evidence.cross_scene_claims.map(c=>[c.claim_id,c.all_scene_ids]),body_seconds:evidence.estimated_body_seconds,output_sha256:fh(path.join(out,'output-pins.json')),externalCalls},null,2));
