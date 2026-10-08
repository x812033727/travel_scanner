import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const ROOT=process.cwd();
const HERE=path.join(ROOT,'docs/videos/series-plans/ou-de-jianghu/visual-development/scene-prop-design');
const WORK=process.env.OU_DE_JIANGHU_WORKDIR;
if(!WORK)throw Error('Set OU_DE_JIANGHU_WORKDIR to the episode media directory before rebuilding.');
const IMAGEGEN_ROOT=process.env.IMAGEGEN_ORIGINAL;
if(!IMAGEGEN_ROOT)throw Error('Set IMAGEGEN_ORIGINAL to the local generated-image root before rebuilding.');
function resolveMedia(p){
  for(const [token,root] of [['<IMAGEGEN_ORIGINAL>',IMAGEGEN_ROOT],['<VIDEO_WORKDIR>/ou-de-jianghu-e001',WORK]]){
    if(p.startsWith(token+'/'))return path.join(root,p.slice(token.length+1));
  }
  throw Error('Media paths must use a documented portable root: '+p);
}
const OUT=path.join(WORK,'scene-props/20261008');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(path.resolve(ROOT,p));
const write=(name,obj)=>fs.writeFileSync(path.join(HERE,name),JSON.stringify(obj,null,2)+'\n');
const worklog=JSON.parse(fs.readFileSync(path.join(HERE,'generation-worklog.json'),'utf8'));
const sourcePaths=['docs/videos/ou-de-jianghu-e001/video.json','docs/videos/ou-de-jianghu-e001/script.md','docs/videos/ou-de-jianghu-e001/brief.md','docs/videos/series-plans/ou-de-jianghu/production/cast.json','docs/videos/series-plans/ou-de-jianghu/production/cast-notes.md','docs/videos/series-plans/ou-de-jianghu/production/ep1/beats.md','docs/videos/series-plans/ou-de-jianghu/setting.json'];
const sources=sourcePaths.map(p=>({path:p,sha256:sha(read(p))}));
const video=JSON.parse(read(sourcePaths[0])), cast=JSON.parse(read(sourcePaths[3]));
const ids=new Set(video.scenes.map(s=>s.id));
function location(id){const m=id.match(/^a(\d+)-s(\d+)$/);if(!m)throw Error(id);const a=+m[1],n=+m[2];if(a===1)return n<=8?'forge':n===9?'title':n<=17?'mountain':n<=44?'watchtower':'gate';if(a===2)return 'gate';if(a===3)return n<=65?'hall':n<=81?'terrace':'courtyard';if(a===4)return n<=49?'harbor':'chess-room';if(a===5)return n===78?'forge':n<=14||n>=17&&n<=22||n>=32&&n<=34?'corridor':n<=16?'courtyard':'chess-room';throw Error(id);}
const specs=[
['fan','白合扇','\\b(?:fan|white jade ribs)\\b','shen-guihe','1把；閉合；右手或腰帶，另鏡明示左手持匣，不以扇為兵器','personal-prop-states'],
['beads','三圈木珠','prayer beads|wooden.*bead|split bead|bead splits','ji-wen','左前臂3圈；a05-s067裂一珠，s068掃落裂珠，不重置完整','personal-prop-states'],
['copper-coins','三枚方孔銅錢','copper coins?|square-holed','bao-sanqian','3枚/紅繩；a05-s089末枚落地後繩上2枚，地上1枚','personal-prop-states'],
['saber','紅穗彎刀','sabre|saber|red tassel','yan-hui','1把闊彎刀；右肩；紅穗隨肩動作，無雙刀','blade-and-tongs-reference'],
['sword','直劍黑鞘','straight sword|sword|scabbard','yin-wusheng','1把直劍/1素黑鞘；背負柄出本人右肩；出鞘不能仍留另一柄','blade-and-tongs-reference'],
['tongs','長鍛鉗','forge tongs|iron tongs','nie-gutie','1把雙臂單樞軸；a01-s002右手舉；s005夾四箭後放入','blade-and-tongs-reference'],
['bow','黑漆弓','lacquered bow|black bow|bowstring','nie-gutie','1黑漆長弓；首集弓弦紅黑浸血；s007奪走並斷弦','wugui-bow-arrows'],
['arrows','三長一短箭','black arrows?|four arrows|three long','', '共4支：3長1短；s005全入單囊；首集姬不持弓箭','wugui-bow-arrows'],
['quiver','黑漆箭囊','quiver','', '1囊掛弓；不是獨立多囊；長箭需容納深度','wugui-bow-arrows'],
['broken-string','半截斷弦/鐵釘','bowstring|iron nail|dark-red string','', 's008聶右手半截；a05-s076窗外橫木一釘固定另一截；s077右手拔釘/左掌接弦；s081右釘左弦','wugui-bow-arrows'],
['document-box','降書黑匣','document box|lacquered.*box|surrender.*box','ji-wushuang','1前臂長扁匣/銀霜蕨；a02-s057沈左手接；a03盟堂桌上','surrender-document-box'],
['go-set','棋盤/棋子','go board|white stone|black stone|go stone','', '1低木棋盤/黑白子；白子長老右側手間停住，a05-s091才落入空角；點位是待採用提案','go-candle-reference'],
['candle','棋桌單燭','candle|candlelight','', '客房1燭；亮→a04-s091鏡末熄滅→a05不重燃','go-candle-reference'],
['tea-set','茶盤一壺一杯','tray|teapot|tea|one cup','bao-sanqian','1黑盤/1小陶壺/1杯；a05-s017送茶，s026置桌，s030翻盤，s031後茶水留地','tea-tray-states'],
['shell-coin','白貝錢','shell coin','luo-qingyan','1白色圓孔貝錢；s038洛→包右掌，s039試咬，s040收錢袋','shell-coin-doll'],
['doll','焦布偶','cloth doll','', '1灰紫焦布偶由女孩雙臂抱；不是木偶角色或武器','shell-coin-doll'],
['whisk','白拂塵','horsetail whisk|whisk','xuanmen-elder','1白拂塵；日間左臂，客房膝上；a05-s046沈扶正，無常駐第二把',null],
['crescent','後頸月牙','crescent|birthmark','', '僅a02-s037、a04-s043/s044露出；同構圖同開口同尺寸；非身份答案','controlled-crescent-nape'],
['gold-seal','右手一道金印','seal mark|gold mark|slanted brush','ji-wushuang','右手背1淡金斜筆；s050/s054/s087受控露出；盟堂只有沈看見','controlled-right-hand-seal'],
['black-wind','無形黑風','black wind','', 'a01-s006/s007；無臉、冠、身體、身份；北後景→鏡頭','controlled-anonymous-black-wind'],
['crown','冠/除冠','crown|coral crown','', '各角色基底不同；姬a03-s085除冠，s086起此場無冠；非新全域造型',null],
['lamp','客院油灯/長廊灯','oil lamp|lantern','', '客院1小油灯，a05-s015/s016暗窗；長廊暖灯與客房燭光不可混',null],
['rope','綑腕繩/繫船繩','rope-bound|bound wrist|mooring|rope','', '鑄爐綑腕繩和外港繫船繩分開，不能畫成同道具',null],
['crowd-weapons','守衛槍/弟子刀','spear|disciple.*blade','', '客院2守衛各1槍；門前弟子兵器按鏡景深擺位，不變成角色多持武器',null],
['cane','老者手杖','cane','', '老者前排支撐，單杖；與布偶一起保留群眾連戲',null]
].map(([id,name,pattern,character,rule,board])=>({id,name,pattern,character,rule,board}));
const overrides={
'a01-s005':['3長1短4箭由鉗放入1囊，鉗必須一次夾住四支；弓/囊關係不得換。'],
'a01-s008':['只剩聶右手半截弦，無傷手釘孔（那是後集造型）。'],
'a02-s035':['門前三級階，寂由右下階；使用gate master，不把正反打當翻圖。'],
'a02-s036':['寂右掌與姬鳳冠接觸，三圈珠在左臂；接觸/銀鏈遮擋尚需pilot。'],
'a02-s037':['受控胎記；人物基底不能常駐露印；原首格已露/動作再分髮的衝突留劇本持有人处理。'],
'a02-s057':['沈左手接匣；原文女手一/雙手未定，正式首尾格需選定；不修改原稿。'],
'a03-s050':['右手在左手上；右手背朝觀眾，袖滑落才顯一道印。'],
'a03-s051':['寂視線受袖擋；不可借圖把他畫成已看到金印。'],
'a03-s054':['左指拉黑袖蓋右手背；一印不得多筆。'],
'a03-s085':['姬自行除冠動作；後續無冠屬單場狀態。'],
'a03-s087':['左拇指擦的是印旁空皮膚，非抹掉金印。'],
'a04-s038':['1白圓孔貝錢落入包右掌；與3方孔銅錢區別。'],
'a04-s043':['與a02-s037同後頸角度比例；只給觀眾看，不推導親屬答案。'],
'a04-s044':['風吹止，髮重新遮月牙。'],
'a05-s015':['外觀暗窗，不證明姬在或不在。'],
'a05-s022':['包右手拉開同一客房門，门先關。'],
'a05-s030':['一壺一杯翻盤，壺/杯不可增殖，下一鏡地面留茶。'],
'a05-s035':['沈扇入腰帶，雙手可探脈；屍身無血無箭傷。'],
'a05-s067':['左臂3圈珠、左拳收緊，1珠裂。'],
'a05-s068':['裂珠被右手掃落；后鏡不可把珠恢复全新。'],
'a05-s073':['殷关門，暖廊光切斷。'],
'a05-s074':['閉紙窗被風吹開一掌寬；背面橫木才轉向室內。'],
'a05-s076':['外橫木1鐵釘固定1短斷弦；不能畫箭命中傷口。'],
'a05-s077':['右手拔釘、左掌接弦；兩件左右不要合併。'],
'a05-s078':['source a01-s008、from_s0回憶2秒；用原母鏡，不買另一支。'],
'a05-s081':['沈左掌弦、右指釘，窗半開。'],
'a05-s089':['原3枚，末枚落地；餘2枚，需先鬆開末端結。'],
'a05-s091':['長老指間1白子此時才落入棋局空角；不是新局。']
};
function state(s,loc){const a=+s.id.slice(1,3),n=+s.id.slice(5);const list=[];if(loc==='chess-room'){list.push(a===4&&n<91?'棋桌單燭亮；結霜程度以該鏡文字為準':'燭已滅；右窗/衣上霜依該鏡文字');if(a===5){list.push(n<73?'客房左門開（s022後），暖廊光可入':'s073關門後，暖廊光消失');list.push(n<74?'紙窗關':'s074後紙窗一掌寬開，外橫木可見');if(n>=30)list.push('茶盤已翻、地面茶水不重置');if(n>=68)list.push('寂左臂珠有裂/失珠狀態');if(n>=89)list.push('包繩上2枚/地面1枚銅錢');}}if(loc==='courtyard')list.push(a===5?'深夜暗窗；無法推定室內人':'单油灯暖；a03-s085後姬此場無冠');if(loc==='forge')list.push(a===5||n===8?'餘燼/右手半弦回憶':'夜/左爐橘光；黑風只在s006/s007');return list;}
const shots=video.scenes.flatMap((s,i)=>s.template!=='shot'?[]:[{shot_id:s.id,source_pointer:'/scenes/'+i,source_sha256:sources[0].sha256,location_id:location(s.id),camera:s.data.camera||'',prompt_exact:s.data.prompt||'',motion_exact:s.data.motion||'',characters_declared:s.data.characters||[],source_reuse:s.data.source||null,explicit_prop_mentions:specs.filter(p=>new RegExp(p.pattern,'i').test((s.data.prompt||'')+' '+(s.data.motion||''))).map(p=>p.id),character_inventory_check:specs.filter(p=>p.character&&(s.data.characters||[]).includes(p.character)).map(p=>({prop_id:p.id,rule:p.rule,visibility:'inventory only; source framing determines visibility'})),continuity_state_after_shot:state(s,location(s.id)),manual_notes:overrides[s.id]||[],review_status:overrides[s.id]?'critical_transition_text_reviewed':'source_indexed_not_per_frame_visual_qa'}]);
const latest=worklog.media.filter(m=>m.status==='candidate');
for(const m of worklog.media){for(const id of m.sourceIds)if(!ids.has(id))throw Error('bad source '+id);if(!m.qa)throw Error('missing visual QA '+m.id);}
fs.mkdirSync(OUT,{recursive:true});
const normalized=worklog.media.map(m=>{const filename=m.id+'-v'+m.version+'.png',target=path.join(OUT,filename),buf=fs.readFileSync(resolveMedia(m.originalPath));if(fs.existsSync(target)){if(sha(fs.readFileSync(target))!==sha(buf))throw Error('copy conflict '+filename);}else fs.copyFileSync(resolveMedia(m.originalPath),target);const ref_inputs=(m.references||[]).map(p=>{const prior=worklog.media.find(x=>x.originalPath===p);return{path:prior?'scene-props/20261008/'+prior.id+'-v'+prior.version+'.png':path.relative(WORK,resolveMedia(p)).replaceAll('\\','/'),sha256:sha(fs.readFileSync(resolveMedia(p))),kind:prior?'generated_reference':'portrait_reference'};});return{id:m.id,version:m.version,kind:m.kind,status:m.status,file:'scene-props/20261008/'+filename,original_path:m.originalPath,sha256:sha(buf),width:buf.readUInt32BE(16),height:buf.readUInt32BE(20),source_ids:m.sourceIds,source_pointers:m.sourceIds.map(id=>'/scenes/'+video.scenes.findIndex(s=>s.id===id)),references:ref_inputs,visual_qa:m.qa,owner_accepted:false,look_imported:false,animation_verified:false};});
const characterIds=['shen-guihe','ji-wushuang','ji-wen','bao-sanqian','yin-wusheng','yan-hui','nie-gutie','luo-qingyan','xuanmen-elder'];
const appearances=characterIds.map(id=>{let i=cast.characters.findIndex(c=>c.id===id);if(i<0)throw Error(id);return{character_id:id,source:sourcePaths[3],pointer:'/characters/'+i+'/appearance',text:cast.characters[i].appearance};});
write('shot-props.json',{schema_version:1,status:'source_bound_continuity_index_not_animation_validation',source:sources[0],counts:{scenes:video.scenes.length,shots:shots.length,title_cards:video.scenes.filter(s=>s.template!=='shot').length},extraction_note:'Exact source text retained for every shot. Prop mentions are mechanical index; character inventories are not assertions of on-screen visibility. Critical transition notes were manually reviewed; no frame/video exists for per-frame QA.',prop_rules:specs,excluded_title_cards:video.scenes.filter(s=>s.template!=='shot').map(s=>s.id),shots});
write('prompts.json',{schema_version:1,tool:'built-in image_gen.imagegen',billing:{actual_cost:null,other_paid_provider_called:false},media:worklog.media.map(({qa,status,originalPath,...m})=>({...m,output_original_path:originalPath,status}))});
const points={schema_version:1,status:'editorial_layout_proposal_not_canon',grid_lines:19,coordinates:'0-based x,y intersections; north at top',black:[[3,3],[3,5],[5,4],[15,4],[14,5],[12,14],[15,15],[4,15]],white:[[4,3],[4,5],[5,5],[15,3],[14,4],[13,14],[14,15],[5,15]],final_white_candidate:[1,17],note:'Source specifies unfinished game/empty corner, not moves. These positions support continuity discussion only. Freeze selected layout and mirror no board before keyframes.'};
write('go-layout-proposal.json',points);
const svg=(after)=>{let a=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000"><rect width="1000" height="1000" fill="#d9ae69"/>'];for(let i=0;i<19;i++){let p=100+i*800/18;a.push('<path d="M100 '+p+' H900 M'+p+' 100 V900" stroke="#343027" stroke-width="2" fill="none"/>');}for(const x of [3,9,15])for(const y of [3,9,15])a.push('<circle cx="'+(100+x*800/18)+'" cy="'+(100+y*800/18)+'" r="5" fill="#343027"/>');for(const [color,pts] of [['#171a1f',points.black],['#faf7ef',points.white.concat(after?[points.final_white_candidate]:[])]])for(const [x,y]of pts)a.push('<circle cx="'+(100+x*800/18)+'" cy="'+(100+y*800/18)+'" r="19" fill="'+color+'" stroke="#4c453a" stroke-width="2"/>');a.push('</svg>');return a.join('\n');};
const auxiliary=[];for(const after of [false,true]){const file='go-layout-'+(after?'after':'before')+'.svg',dest=path.join(OUT,file);fs.writeFileSync(dest,svg(after));auxiliary.push({file:'scene-props/20261008/'+file,sha256:sha(fs.readFileSync(dest)),status:'editable_geometry_proposal',generated_image:false});}
const receipt={schema_version:1,episode:'ou-de-jianghu-e001',status:'generated_and_visually_reviewed_candidates_pending_owner_selection',video_workdir_example:'<VIDEO_WORKDIR>/ou-de-jianghu-e001',media_paths_relative_to:'<VIDEO_WORKDIR>/ou-de-jianghu-e001',source_files:sources,appearance_sources:appearances,counts:{original_pngs:normalized.length,latest_pngs:latest.length,latest_scene_pngs:latest.filter(m=>m.kind.startsWith('scene')).length,latest_prop_boards:latest.filter(m=>m.kind==='prop').length,latest_controlled_cards:latest.filter(m=>m.kind==='controlled-detail').length,shots_indexed:shots.length,title_cards:4},acceptance:{style_direction_user_quote:'保留目前華麗古裝與細緻人物風格',scope:'style direction only; no per-image owner selection or detail acceptance',owner_accepted:false,normal_look_imported:false,animation_verified:false},media:normalized,auxiliary};
write('media-receipt.json',receipt);
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const html='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>偶的江湖 場景道具候選</title><style>body{background:#141923;color:#eee;font:16px system-ui;margin:28px}h1{font-size:28px}small{color:#b9c3d0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:24px}article{background:#202938;padding:14px;border-radius:12px}img{width:100%;height:auto;display:block}p{line-height:1.6}a{color:#a9d1ff}summary{cursor:pointer}</style><h1>偶的江湖｜首集場景・道具</h1><p>29張最新候選：19空景/狀態、7道具板、3受控細節。40原圖保留。風格方向已接受；個圖未採用、未匯入look、未驗動畫。受控卡只供特定鏡頭，不混入中性畫像。</p><p><strong>客房 master v3、angle-b v2、cold v2 三張紙窗仍有淡月輪／透景殘影，只作空間與光線提案，不准用作紙窗近景（CU）母圖。cold v2 僅適用 a05-s031/s035/s042 翻盤後，不能作 a05-s023 同態首格。</strong></p><div class="grid">'+normalized.filter(m=>m.status==='candidate').map(m=>'<article><h2>'+escape(m.id)+' v'+m.version+'</h2><a href="'+path.basename(m.file)+'"><img loading="lazy" src="'+path.basename(m.file)+'" alt="'+escape(m.id)+'"></a><p>'+escape(m.visual_qa)+'</p><small>'+m.width+' × '+m.height+' · '+escape(m.source_ids.join(', '))+'</small></article>').join('')+'</div><p>棋盤生成圖不作格線/點位母版：<a href="go-layout-before.svg">19路落子前提案</a> / <a href="go-layout-after.svg">末尾落子後提案</a>。點位未定稿。</p></html>';
fs.writeFileSync(path.join(OUT,'gallery.html'),html);
const verification={schema_version:1,verified_at:new Date().toISOString(),source_files:sources.length,source_hashes_match:true,original_pngs:normalized.length,original_copied_hashes_match:true,latest_pngs:latest.length,valid_source_pointers:true,appearance_pointers:appearances.length,reference_inputs:normalized.reduce((n,m)=>n+m.references.length,0),shots:shots.length,unique_shot_ids:new Set(shots.map(s=>s.shot_id)).size,coverage:shots.length===455&&video.scenes.length===459,owner_accepted:false,animation_verified:false};
if(normalized.length!==40||latest.length!==29||shots.length!==455||!verification.coverage)throw Error('count mismatch');
write('verification.json',verification);
console.log(JSON.stringify(verification));
