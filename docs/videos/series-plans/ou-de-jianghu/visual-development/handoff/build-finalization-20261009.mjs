import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
const base='docs/videos/series-plans/ou-de-jianghu/visual-development';
const videoWorkdir=path.resolve(process.argv[2]||'');
const working=path.resolve(process.argv[3]||'');
const check=process.argv.includes('--check');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const hashText=t=>crypto.createHash('sha256').update(t).digest('hex');
const expected='cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17';
assert.equal(sha(path.join(working,'video.json')),expected,'Expected the two-correction v4 working video');
const video=read(path.join(working,'video.json'));
const portraitReceipt=`${base}/episode1-portraits/finalized-views-receipt.json`;
const animationReceipt=`${base}/animation-reference/finalized-media-receipt.json`;
const portraits=read(portraitReceipt);
const animation=read(animationReceipt);
const props=read(`${base}/scene-prop-design/shot-props.json`);
const scenes=read(`${base}/scene-prop-design/media-receipt.json`);
const camera=read(path.join(working,'camera-ledger.json'));
const risk=read(path.join(working,'risk-ledger.json'));
const plan=read(path.join(working,'shot-plan.json'));
const sourceFiles=portraits.source_files.map(x=>({...x,current_sha256:sha(x.path)}));
assert.equal(sourceFiles.length,12); for(const s of sourceFiles)assert.equal(s.sha256,s.current_sha256,s.path);
const ids=['shen-guihe','ji-wushuang','ji-wen','bao-sanqian','yin-wusheng','yan-hui','nie-gutie','xuanmen-elder','luo-qingyan'];
const aliases={'shen-guihe':/\b(?:shen-guihe|Shen)\b/i,'ji-wushuang':/\b(?:ji-wushuang|Wushuang)\b/i,'ji-wen':/\b(?:ji-wen|Ji Wen)\b/i,'bao-sanqian':/\b(?:bao-sanqian|Bao)\b/i,'yin-wusheng':/\b(?:yin-wusheng|Yin)\b/i,'yan-hui':/\b(?:yan-hui|Yan Hui|Yan's)\b/i,'nie-gutie':/\b(?:nie-gutie|Nie)\b/i,'xuanmen-elder':/\b(?:xuanmen-elder|elder)\b/i,'luo-qingyan':/\b(?:luo-qingyan|Luo)\b/i};
const candidates=new Map();
function candidate(key,file,hash,receipt,extra={}){
  const logical=key.replace(/-v\d+$/,'');const version=Number(key.match(/-v(\d+)$/)?.[1]||1);
  if((candidates.get(logical)?.version||0)>version)return;
  candidates.set(logical,{logical_key:logical,candidate_key:key,version,file,sha256:hash,receipt,...extra});
}
for(const a of portraits.assets)candidate(a.key,a.path,a.sha256,portraitReceipt,{native_dimensions:a.native_dimensions});
for(const a of animation.entries)candidate(a.key,`<VIDEO_WORKDIR>/${a.file}`,a.sha256,animationReceipt,{limitations:a.limitations||[]});
for(const a of scenes.media.filter(x=>x.status==='candidate'&&!x.id.startsWith('chess-guestroom-cold')))candidate(`${a.id}-v${a.version}`,`<VIDEO_WORKDIR>/ou-de-jianghu-e001/${a.file}`,a.sha256,`${base}/scene-prop-design/media-receipt.json`);
const used=new Set();
function ref(key,purpose,condition='apply only when the described feature is visible'){
  used.add(key);return {logical_key:key,purpose,condition};
}
const dimensionAudit=portraits.assets.map(a=>{
  const file=a.path.replace('<VIDEO_WORKDIR>',videoWorkdir),buf=fs.readFileSync(file);
  const measured={width:buf.readUInt32BE(16),height:buf.readUInt32BE(20)};
  assert.equal(sha(file),a.sha256);assert.equal(measured.width,a.native_dimensions.width);assert.equal(measured.height,a.native_dimensions.height);
  return {key:a.key,sha256:a.sha256,...measured,aspect_ratio:measured.width/measured.height,original_target:a.output_target,original_dimension_status:a.dimension_status,disposition:'retain_native_for_identity_costume_reference_proposal',upscaled:false,cropped:false,owner_accepted:false};
});
const decision=(id,shots,before,after,proposal)=>({id,shots,before,after,editorial_proposal:proposal,action_rewrite:false});
const decisions=[
  decision('four-arrows',['a01-s004','a01-s005','a01-s007','a01-s008','a05-s078'],'s004 鉗口接觸同一束三長一短箭的箭桿；弓囊在畫左。','s005 結果插鏡：四箭已尖端向下入同一囊，鉗口開在囊口上不接觸；s007 弓囊已脫離、朝左被黑風帶走；聶右手已握半截弦。s008 收拳；s078 重用 s008。','四桿平行、短箭位置固定為束的靠觀眾側；這是數量辨識提案，不新增箭或落箭動作。'),
  decision('palm-and-nape',['a02-s035','a02-s036','a02-s037','a04-s043','a04-s044'],'寂聞右掌距固定冠脊 1 cm；跪者雙手藏袖放在匣上，左前臂三圈念珠；髮先遮後頸。','s036 只下移接觸實心冠脊並停；不碰細鏈。s037 撥髮露唯一月痕；洛 s043 同部位，s044 髮覆回。','保留冠鏈向兩側落下；月痕形狀照 controlled-crescent-nape，僅圖形呼應，不替劇情回答身分。'),
  decision('document-box',['a02-s056','a02-s057','a02-s058'],'s056 沈右手閉扇輕敲左掌；接匣過程在剪點外。','s057 靜態結果：沈左手托匣底在畫右上，無霜雙手已收空袖；s058 左胸前匣只抬既有 10 cm，扇仍右手。','匣長軸直立貼左胸、面朝鏡頭，底部由左掌承重；不得補一鏡雙方手掌交錯的傳遞動畫。'),
  decision('uncrowned',['a03-s085','a03-s086','a03-s087'],'s085 已摘冠，冠立於桌面、鏈收桌上，雙手放下。','s086 無冠、銀白髮散落；v4 刪除矛盾通用 complete crown 片語；s087 才讀右手單一金線。','既有無冠狀態優先於有冠基底；生成首格要明確覆寫冠、細鏈並維持左眼霜花，不可直接套冠版母圖。'),
  decision('gangplank-shell',['a04-s029','a04-s030','a04-s036','a04-s037','a04-s038','a04-s039'],'包在岸側跳板低處畫左、洛在船欄高處畫右；包抬右掌。','s038 v4：白色圓孔貝錢一枚已在包右掌，洛右手退到上緣外；s039 幣到唇下但嘴合不咬。','保持岸左船右與高低差，跳板靠岸端為包落腳點；此掌無銅錢，交易接觸不另補動作。'),
  decision('tea-door-floor',['a05-s018','a05-s019','a05-s022','a05-s023','a05-s026','a05-s030','a05-s031','a05-s035','a05-s042','a05-s073'],'s018 雙手送茶；s019 左掌承托盤、右指叩門兩次；s022 右手推開左前方滑門；s023 入門仍托盤，燭已滅。','s026 才放盤桌上；s030 才切到翻盤結果，地上一壺一杯、一灘茶；s031/035/042 沿用此結果。s073 殷關門才切掉暖廊光。','翻盤朝桌南、靠門一側，地面茶色而非血色；具體散落落點是最小連戲提案。原稿與 v3/v4 的送茶索引一致，舊場景包 s017/s018 是索引錯誤，應以 video 為準。'),
  decision('window-string',['a05-s074','a05-s076','a05-s077','a05-s078','a05-s081'],'s074 後右紙窗開手掌寬；s076 窗框外側木條向室內翻，只有一釘固定半截弦。','s077 靜態結果：沈左掌一段半弦、右指一釘已離木，孔可見；s078 插回舊聶手；s081 沈在窗右，左弦右釘。','釘孔在同一根外側木條、弦毛端朝室內；拔與接只在結果讀到，不新增第二半弦或雙弦接合。'),
  decision('last-white',['a04-s090','a04-s091','a05-s025','a05-s090','a05-s091'],'長老右手在棋盤空角上方懸一白，右前臂桌上，拂塵膝上；a04-s091 燭滅；a05-s025 棋子仍未落。','a05-s091 結果插鏡：末白已在畫左角點 [1,17]，長老空指在畫右不動；共 17 子，其餘 16 坐標不變。','懸子點與最後角點用同一棋盤坐標鎖定；末鏡不是生成空中墜落軌跡，無新增棋子。'),
  decision('cancel-cold-master',['a05-s031','a05-s035','a05-s042'],'使用 chess-guestroom-master-v4 的乾淨紙窗、房間幾何與桌門位置。','冷光、局部霜、滅燭、翻盤後地面状態由逐鏡 spec 覆寫；開門暖廊光保留至 s073。','所有 chess-guestroom-cold-v* 保留為失敗證據並 not-for-input；取消獨立冷場母圖，不宣稱舊月輪已修成功。')
];
const black=[[3,3],[3,5],[5,4],[15,4],[14,5],[12,14],[15,15],[4,15]],white=[[4,3],[4,5],[5,5],[15,3],[14,4],[13,14],[14,15],[5,15]];
const placements=[{shot:'a04-s051',color:'white',point:[4,3]},{shot:'a04-s062',color:'black',point:[5,4]},{shot:'a04-s071',color:'white',point:[15,3]},{shot:'a04-s079',color:'white',point:[5,5]}];
function goState(id){
  let b=black.filter(p=>!placements.some(x=>x.color==='black'&&String(p)===String(x.point))),w=white.filter(p=>!placements.some(x=>x.color==='white'&&String(p)===String(x.point)));
  for(const x of placements)if(id>=x.shot)(x.color==='black'?b:w).push(x.point);
  if(id>='a05-s091')w.push([1,17]);
  return {black:b,white:w,count:b.length+w.length,held_stones_excluded:true};
}
const goDecision=read(`${base}/scene-prop-design/go-layout-decision.json`);
for(const state of goDecision.states){const own=goState(state.after_shot||'a04-s050');assert.deepEqual(own.black,state.black);assert.deepEqual(own.white,state.white);assert.equal(own.count,state.board_stones);assert.equal(new Set([...own.black,...own.white].map(String)).size,own.count);}
const coldSpec=read(`${base}/scene-prop-design/cold-state-spec.json`);
assert.equal(coldSpec.base.sha256,candidates.get('chess-guestroom-master').sha256);
const sceneBase={forge:'forge-master',tower:'watchtower-master',gate:'alliance-gate-master',council:'alliance-hall-master',terrace:'alliance-terrace',court:'guest-courtyard-interior',port:'outer-harbor-master',room:'chess-guestroom-master',corridor:'guestroom-corridor'};
const byId=a=>new Map(a.map(x=>[x.id||x.shot_id,x]));
const cm=byId(camera.rows),pm=byId(props.shots),rm=byId(risk),pl=byId(plan.shots);
const rows=video.scenes.flatMap((s,index)=>{
  if(s.template!=='shot')return [];
  const c=cm.get(s.id),p=pm.get(s.id),r=rm.get(s.id),q=pl.get(s.id);assert.ok(c&&p&&r&&q,s.id);
  const declared=s.data.characters||[];for(const id of declared)assert.ok(ids.includes(id),id);
  const visibleText=(s.data.prompt||'').replace(/\b(?:shen-guihe|ji-wushuang|ji-wen|bao-sanqian|yin-wusheng|yan-hui|nie-gutie|xuanmen-elder|luo-qingyan|Shen|Wushuang|Ji Wen|Bao|Yin|Yan Hui|Nie|the elder|Luo)\s+speaks? off[ -]screen\b/gi,'');
  const inferred=ids.filter(id=>!declared.includes(id)&&aliases[id].test(visibleText));
  const visible=[...new Set([...declared,...inferred])];
  const speakers=[...new Set((s.lines||[]).map(x=>x.speaker).filter(x=>ids.includes(x)))];
  const mouthVisible=speakers.filter(id=>declared.includes(id)&&!new RegExp(`${id} speaks? off[ -]screen`,'i').test(s.data.prompt||'')&&!/^(?:insert|extreme close-up).*(?:hand|palm|eye|nape|coin|board|window|crown)/i.test(s.data.camera||'')&&!/back view|from behind/i.test(s.data.camera||''));
  const characterRefs=visible.map(id=>({character_id:id,identity_basis:declared.includes(id)?'declared':'named_visible_body_or_identity_in_prompt; planning inference',
    base:ref(`${id}-full-body`,'identity, costume silhouette and material; generate the first frame before I2V'),
    head:ref(`${id}-front-headshot`,'face identity; do not force a frontal pose','face visible; skip hand/back-only insert'),
    detail:ref(`${id}-construction-details`,'crown, hair, costume fastenings and hand/prop construction','use only relevant construction; working-shot state overrides sheet default'),
    mouth:mouthVisible.includes(id)&&id!=='yin-wusheng'?ref(`${id}-mouth-shapes`,'static mouth shape drawing guide; no exact phoneme or lipsync claim','on-screen speaking face only; facial identity takes precedence'):null,
    mouth_disposition:mouthVisible.includes(id)&&id!=='yin-wusheng'?'candidate_static_shapes_pending_final_binding':'no mouth sheet input assigned to this framing / offscreen / silent character'}));
  let sk=sceneBase[c.space];
  if(c.space==='tower'&&Number(s.id.slice(-3))<=16)sk='qiyun-mountain';
  if(c.space==='court')sk=s.id==='a05-s016'?'guest-courtyard-dark':/exterior|wide shot.*courtyard|guards|moon.?gate/i.test(s.data.camera+' '+s.data.prompt)?'guest-courtyard-exterior':'guest-courtyard-interior';
  const sceneRefs=[ref(sk,'spatial geometry, door/window/boat coordinates and motivated light direction','working-shot time/state overrides static master lighting')];
  const mentioned=props.prop_rules.filter(rule=>new RegExp(rule.pattern,'i').test(`${s.data.prompt||''} ${s.data.motion||''}`));
  const propRefs=[...new Set(mentioned.map(x=>x.board).filter(Boolean))].map(key=>ref(key,'prop shape, material and count; first/last state is defined by v4 shot and continuity decisions','only the prop explicitly visible in this shot; do not add absent inventory'));
  const needsFanPolicy=visible.includes('shen-guihe')||mentioned.some(x=>x.id==='fan');
  if(needsFanPolicy&&!propRefs.some(x=>x.logical_key==='personal-prop-states'))propRefs.push(ref('personal-prop-states','authoritative white-jade / white-paper closed fan construction; no fan tassel, chain, charm or dangling bead','only if fan is visible; do not add a fan to an otherwise empty hand'));
  if(needsFanPolicy){
    if(!characterRefs.some(x=>x.character_id==='shen-guihe'))propRefs.push(ref('shen-guihe-construction-details','authoritative fan topology paired with personal-prop-states','fan details only; do not insert Shen into an anonymous prop shot'));
    for(const item of propRefs)if(item.logical_key==='personal-prop-states')item.fan_geometry_priority='Together with shen-guihe-construction-details, overrides tiny hand-adjacent lines/beads in character pose, concept, color and group sheets. Those are identity/costume/pose/color references only.';
  }
  const continuity={axis:c.axis,phase:c.phase,station:c.station,first_frame:s.data.prompt,end_frame:c.end_frame,decision_ids:decisions.filter(x=>x.shots.includes(s.id)).map(x=>x.id)};
  if(needsFanPolicy)continuity.fan_reference_policy={masters:['shen-guihe-construction-details','personal-prop-states'],anatomy:'white jade outer guards/ribs, white paper, no fan tassel/chain/charm/dangling bead',shot_state:'v4 prompt governs which hand, closed state or sash position; no new action or inventory',other_character_art:'identity/costume/pose/color only; small dangling hand-adjacent marks are not fan anatomy evidence',source_prompt_edited:false};
  if(c.space==='room'){
    continuity.go_state=goState(s.id);
    continuity.go_state.reference_state=goDecision.states.filter(x=>!x.after_shot||s.id>=x.after_shot).at(-1).id;
    continuity.go_state.geometry_decision=`${base}/scene-prop-design/go-layout-decision.json`;
    continuity.candle=s.id>='a04-s091'?'extinguished; no lit flame':'lit until a04-s091';
    continuity.door=s.id>='a05-s073'?'closed; warm corridor light cut':s.id>='a05-s022'?'open; warm corridor spill remains':'shot framing governs; no invented door move';
    continuity.tea=s.id>='a05-s030'?'overturned tray, one pot, one cup and tea on floor':s.id>='a05-s026'?'tray on table':s.id>='a05-s023'?'Bao still carries tray':'do not pre-show later spill';
    if(['a05-s031','a05-s035','a05-s042'].includes(s.id)){
      continuity.scene_state_override='clean master-v4 geometry and paper window + cold blue light, local frost, dead candle, post-s030 overturned tray; no independent cold master or added moon';
      continuity.cold_spec={file:`${base}/scene-prop-design/cold-state-spec.json`,sha256:sha(`${base}/scene-prop-design/cold-state-spec.json`),base_sha256:coldSpec.base.sha256,rendered:false,shot: coldSpec.shots.find(x=>x.shot_id===s.id),common_overrides:coldSpec.common_overrides};
    }
  }
  return [{shot_id:s.id,source_pointer:`/scenes/${index}`,working_video_sha256:expected,prompt_sha256:hashText(s.data.prompt||''),characters_declared:declared,characters_inferred_for_partial_visible_identity:inferred,offscreen_or_nonvisible_speakers:speakers.filter(x=>!mouthVisible.includes(x)),visual:q.visual,source_reuse:s.data.source||s.source||q.source||null,delivery:q.source?'reuse_existing_source; do not buy another clip':'reference assignment proposal for first-frame preparation',risk:{machine:r.machine_grade,human:r.human_grade,reason:r.reason},references:{characters:characterRefs,scenes:sceneRefs,props:propRefs},prop_mentions_v4:mentioned.map(x=>x.id),continuity,runtime_references_written:false,owner_accepted:false}];
});
assert.equal(rows.length,455);assert.equal(new Set(rows.map(x=>x.shot_id)).size,455);
for(const row of rows.filter(x=>x.continuity.fan_reference_policy)){
  const keys=[...row.references.characters.map(x=>x.detail.logical_key),...row.references.props.map(x=>x.logical_key)];
  for(const key of row.continuity.fan_reference_policy.masters)assert.ok(keys.includes(key),`Fan master assignment missing ${key} at ${row.shot_id}`);
}
const catalog=[...used].sort().map(key=>{
  assert.ok(!key.startsWith('chess-guestroom-cold'));
  const c=candidates.get(key);
  if(!c){assert.ok(key.endsWith('-mouth-shapes')&&key!=='yin-wusheng-mouth-shapes',`Missing unplanned reference ${key}`);return {logical_key:key,candidate_key:`${key}-v1_or_later`,status:'parallel_mouth_candidate_final_receipt_pending',final_binding:null,owner_accepted:false,runtime_integrated:false};}
  const file=c.file.replace('<VIDEO_WORKDIR>',videoWorkdir);assert.equal(sha(file),c.sha256,`candidate changed: ${key}`);
  return {...c,status:'candidate_snapshot_only',final_binding:null,requires_root_latest_version_resolution:true,owner_accepted:false,runtime_integrated:false};
});
assert.equal(catalog.find(x=>x.logical_key==='chess-guestroom-master').version,4);
const output={schema_version:1,status:'engineering_handoff_proposal_pending_owner_selection_and_runtime_binding',episode:'ou-de-jianghu-e001',audit_date:'2026-10-09',source_commit:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),source_files:sourceFiles,parent_working_video:{file:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261008-v3/video.json',sha256:'7f7676d1ce39a6f9dbbdc4cacc5bc8cb39b9979e66e4a906213d2ea4235014df'},working_video:{file:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/video.json',sha256:expected,html_sha256:sha(path.join(working,'animatic.html'))},precedence:['v4 working prompt/state and two-correction receipt','v3 retained dialogue/timing/motion and manual risk','scene-prop index for prop discovery only; never restore superseded original complex actions','static asset sheets; shot-specific states override crowns, candles and spills'],scope:{shots:455,episode_only:true,owner_accepted:false,runtime_references_written:false,paid_calls:0,normal_look_choices_written:false,production_source_modified:false},size_disposition:{hard_import_minimum:'512 px each dimension; maximum 8192 each, 16 Mi pixels, 32 MiB; supported 8-bit noninterlaced PNG RGB/RGBA with CRC/IDAT validation',editorial_targets_not_hard_gate:'front 1024, half 1600, full 2048 long edge remain original editorial targets',native_identity_reference_proposal:true,retained_native_below_target:dimensionAudit.filter(x=>x.original_dimension_status==='native_below_target').length,resize_or_regeneration_required_by_import:false,final_first_frame_2k:'separate desired delivery target, not automatic current drama output; must implement/select and verify a capable route and actual native dimensions',assets:dimensionAudit},capabilities:{builtin_imagegen:'no explicit size/quality schema control; natural-language dimensions do not prove native delivery',normal_drama_keyframes:'sizeFor is null; provider default 1K. IMAGE_SIZE cache label is not measured native dimensions',normal_reference_selection:'approved chosen look sheets, one base per character, MAX_REFS 4. This document does not make arbitrary detail/head/mouth refs automatically consumed',h3:'first/last frame I2V and reference_images are mutually exclusive. Identity sheets guide prior first-frame creation; do not attach them as extra refs alongside first_frame',proof_sources:[{file:'tools/video/media/look.mjs',line:100},{file:'tools/video/media/keyframes.mjs',line:448},{file:'tools/video/media/keyframes.mjs',line:463},{file:'tools/video/media/stages.mjs',line:287},{file:'apps/api/app/video_media/providers/minimax.py',line:301},{file:`${base}/production-list.md`,line:22}]},mouth_policy:{speaking_characters:ids.filter(x=>x!=='yin-wusheng'),silent_character:'yin-wusheng',static_only:true,phoneme_timing_verified:false,audio_or_lipsync_qa:false},chess:{coordinate_system:'0-based [x,y], north/top fixed, never mirror or rotate between shots',original_16:{black,white},placements,final_white:[1,17],timeline_counts:[12,13,14,15,16,17],proposal:'Earlier placements use subsets of the same original 16; held/unplayed and bowl stones are excluded. No added coordinates or story beats.'},continuity_decisions:decisions,excluded_model_inputs:[{pattern:'chess-guestroom-cold-v*',reason:'retired failed moon-free attempts; use clean master-v4 + shot state override',retained_as_evidence:true}],reference_catalog:catalog,shots:rows,validation:{unique_shots:rows.length,source_hashes_verified:12,portrait_native_headers_and_hashes_verified:27,assigned_reference_keys:catalog.length,existing_candidate_hashes_verified:catalog.filter(x=>x.sha256).length,expected_parallel_mouth_bindings:catalog.filter(x=>!x.sha256).length,missing_unplanned_reference_keys:[],cold_master_input_count:0,all_asset_final_bindings_pending:true,automatic_reference_request_readback:false,full_episode_visual_qa_claimed:false,old_staging:'historical v3-bound pending candidates; not rebound or accepted by this file'}};
output.reference_snapshot_sources=[portraitReceipt,animationReceipt,`${base}/scene-prop-design/media-receipt.json`,`${base}/scene-prop-design/go-layout-decision.json`,`${base}/scene-prop-design/cold-state-spec.json`].map(file=>({file,sha256:sha(file)}));
output.working_ledger_sources=['camera-ledger.json','risk-ledger.json','shot-plan.json','budget-and-batches.json'].map(file=>({file:`<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/${file}`,sha256:sha(path.join(working,file))}));
output.validation.go_state_counts_verified_against_scene_decision=[12,13,14,15,16,17];
output.validation.clean_master_sha_matches_cold_spec=true;
assert.equal(candidates.get('shen-guihe-construction-details').candidate_key,'shen-guihe-construction-details-v3');
assert.equal(candidates.get('personal-prop-states').candidate_key,'personal-prop-states-v3');
output.fan_reference_policy={status:'editorial_reference_role_decision_not_global_pixel_consistency_claim',masters:['shen-guihe-construction-details','personal-prop-states'].map(key=>({logical_key:key,candidate_key:candidates.get(key).candidate_key,sha256:candidates.get(key).sha256})),construction:'white jade guards/ribs, white paper; no fan tassel, chain, charm or dangling bead',remaining_character_sheet_marks:'Tiny short lines/beads may remain in small full-body concept or pose imagery. They are excluded as fan topology evidence, not claimed to have been perfectly corrected.',character_sheet_purposes:['identity','costume','pose','color'],assigned_condition:'For every shot with visible/named Shen or an explicit fan mention, use the two masters for visible fan geometry. Do not add absent inventory.',runtime_request_readback:false,owner_accepted:false};
output.fan_reference_policy.explicit_limited_candidates=['shen-guihe-concept-v5','shen-guihe-right-profile-v3','shen-guihe-left-three-quarter-v3'];
output.fan_reference_policy.limited_candidate_rule='Identity/costume reference only; visible small hand-adjacent marks are not an accepted tassel/chain topology. Other revised character images still do not replace the two prop masters.';
output.validation.fan_master_assigned_shots=rows.filter(x=>x.continuity.fan_reference_policy).length;
const json=JSON.stringify(output,null,2)+'\n';
const target=`${base}/handoff/finalization-20261009.json`;
if(check){assert.equal(fs.readFileSync(target,'utf8'),json);console.log('PASS deterministic finalization readback');}else fs.writeFileSync(target,json);
console.log(JSON.stringify(output.validation,null,2));
