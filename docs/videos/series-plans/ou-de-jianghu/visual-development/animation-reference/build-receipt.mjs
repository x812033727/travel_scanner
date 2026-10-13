import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
const root=process.cwd(), out=path.dirname(fileURLToPath(import.meta.url));
const media=path.resolve(process.argv[2]||"");
if(!process.argv[2] || !fs.existsSync(path.join(media,"portraits/20261008"))) throw Error("Pass the existing episode media directory outside the repository");
const refdir=path.join(media,"animation-reference/20261008");
const read=p=>JSON.parse(fs.readFileSync(p,"utf8").replace(/^\uFEFF/,""));
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const ids=["shen-guihe","ji-wushuang","ji-wen","bao-sanqian","yin-wusheng","yan-hui","nie-gutie","xuanmen-elder","luo-qingyan"];
const names=["沈歸鶴","姬無霜","寂聞","包三錢","殷無聲","燕迴","聶孤鐵","玄門長老","洛青衍"];
const views=["back","left-profile","right-profile","left-three-quarter","right-three-quarter","expressions","action-phases","construction-details"];
const labels={"front":"正面全身","back":"背面","left-profile":"左側","right-profile":"右側","left-three-quarter":"左3/4","right-three-quarter":"右3/4","expressions":"六表情","action-phases":"動作階段","construction-details":"服裝與道具細節"};
const overrides={"ji-wushuang-back":2,"ji-wushuang-left-profile":2,"ji-wushuang-right-profile":2,"ji-wushuang-right-three-quarter":4,"bao-sanqian-left-three-quarter":2,"yan-hui-right-three-quarter":3,"shen-guihe-construction-details":2,"xuanmen-elder-back":2,"xuanmen-elder-action-phases":2};
const inventory=read(path.resolve(out,"../asset-inventory.json"));
for(const source of inventory.source_files) assert.equal(sha(fs.readFileSync(path.join(root,source.path))),source.sha256,source.path);
const cast=read(path.join(root,"docs/videos/series-plans/ou-de-jianghu/production/cast.json"));
const localize=p=>{const normalized=p.replaceAll("\\","/");return normalized.startsWith(media.replaceAll("\\","/"))?normalized.replace(media.replaceAll("\\","/"),"<EPISODE_MEDIA>"):"<IMAGEGEN_ORIGINAL>/"+path.basename(p);};
const png=p=>{const b=fs.readFileSync(p);assert.equal(b.subarray(0,8).toString("hex"),"89504e470d0a1a0a");return {sha256:sha(b),bytes:b.length,width:b.readUInt32BE(16),height:b.readUInt32BE(20)};};
const promptFiles=["prompts.json","correction-prompts.json","correction-final-prompts.json","extra-prompts.json","prompts-lineup-agent.json","prompts-scene-agent-corrections.json"];
const promptRecords=[];
for(const name of promptFiles) {
 const p=path.join(refdir,name);if(!fs.existsSync(p))continue;const x=read(p);
 const rows=Array.isArray(x)?x:x.entries??x.prompts??[];
 rows.forEach((e,index)=>{
  const state=name==="correction-prompts.json"&&index>=4?"superseded_before_execution":name==="extra-prompts.json"&&index>=2?"validation_rejected_no_image":"generated";
  promptRecords.push({...e,attempt_id:name+"#"+index,execution_state:state,prompt_sha256:sha(e.prompt??""),references:e.references?.map(r=>({path:localize(r),...png(r)})),output:state==="generated"?{key:e.key,...png(path.join(refdir,e.key+".png"))}:null});
 });
}
const outputFiles=["outputs.json","outputs-scene-agent.json","outputs-lineup-agent.json"];
const origins=[];
for(const name of outputFiles) {const p=path.join(refdir,name);if(!fs.existsSync(p))continue;const x=read(p);origins.push(...(Array.isArray(x)?x:x.outputs??x.entries??[]));}
const originByKey=new Map(origins.map(o=>[o.key,o]));
const entries=[];
const item=(key,id,view,file,reused=false)=>{
 const p=path.join(media,file), stat=png(p), source=originByKey.get(key);
 if(source?.original)assert.equal(stat.sha256,png(source.original).sha256,"Copied original differs: "+key);
 return {key,character_id:id,view,file:"ou-de-jianghu-e001/"+file.replaceAll("\\","/"),...stat,reused_prior_master:reused,status:"reviewed_candidate",owner_accepted:false,judge:null,rigged:false,
 ...(!reused?{generation_method:"builtin_imagegen",original_bytes_preserved:!!source?.original}:{}),
 limitations:view==="expressions"?["表情近景，不取代完整冠飾參照"]:view==="action-phases"?["姿態分解提案，不是已驗證動畫中間格"]:view.includes("profile")?["2D側面參考，非精確正交3D轉台"]:[]};
};
for(const id of ids){
 entries.push(item(id+"-full-body-v1",id,"front","portraits/20261008/"+id+"-full-body-v1.png",true));
 for(const view of views){const stem=id+"-"+view;const v=overrides[stem]||1;entries.push(item(stem+"-v"+v,id,view,"animation-reference/20261008/"+stem+"-v"+v+".png"));}
}
for(const kind of ["color","silhouette"]) {const version=kind==="silhouette"?2:1;const key="ensemble-"+kind+"-lineup-v"+version;entries.push(item(key,"ensemble",kind+"-lineup","animation-reference/20261008/"+key+".png"));}
assert.equal(entries.length,83);assert.equal(entries.filter(x=>!x.reused_prior_master).length,74);
const selected=new Set(entries.map(e=>e.key));
const all=fs.readdirSync(refdir).filter(n=>n.endsWith(".png")&&(originByKey.has(n.slice(0,-4))||n==="ensemble-silhouette-candidate-v1.png")).map(n=>({key:n.slice(0,-4),file:"ou-de-jianghu-e001/animation-reference/20261008/"+n,...png(path.join(refdir,n)),selected:selected.has(n.slice(0,-4))}));
const receipt={schema_version:1,episode:"ou-de-jianghu-e001",source_commit:execFileSync("git",["rev-parse","HEAD"],{encoding:"utf8"}).trim(),source_files:inventory.source_files,status:"reference_package_prepared_pending_owner_selection",scope:"2D and I2V reference proposals; not rigged assets, physical turntables or approved animation",accepted_style:"保留目前華麗古裝與細緻人物風格",owner_asset_selection:false,animation_reference_ready:false,proposed_reference_set_complete:true,counts:{characters:9,new_selected_png:74,reused_front_png:9,total_reference_uses:83,all_new_png_including_history:all.length},entries,retained_originals:all,limitations:["Native full-body outputs are generally 1024x1536 and do not meet the proposed 2048-pixel long edge; no upscaling or repackaged pixel claims.","Yan right-three-quarter v3 deliberately lowers the saber in his right hand; this is a neutral pose variation, not identical-pose turntable geometry.","Hair, crown chains and embroidery have small perspective/generation differences; final keyframes require shot-specific continuity QA.","Ensemble scale is an editorial proposal, not canonical centimeter measurements.","Builtin imagegen billing was not returned. Validation-rejected 9-reference lineup calls produced no image; retained revisions still count as generated assets."]};
receipt.counts.unique_generated_images=new Set(all.map(e=>e.sha256)).size;
receipt.counts.generated_prompt_attempts=promptRecords.filter(p=>p.execution_state==="generated").length;
receipt.counts.validation_rejected_no_image=promptRecords.filter(p=>p.execution_state==="validation_rejected_no_image").length;
receipt.counts.superseded_before_execution=promptRecords.filter(p=>p.execution_state==="superseded_before_execution").length;
for(const e of all)if(e.key==="ensemble-silhouette-candidate-v1")e.alias_of="ensemble-silhouette-lineup-v1";
assert.equal(receipt.counts.unique_generated_images,receipt.counts.generated_prompt_attempts);
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,"media-receipt.json"),JSON.stringify(receipt,null,2)+"\n");
fs.writeFileSync(path.join(out,"prompts.json"),JSON.stringify({schema_version:1,records:promptRecords},null,2)+"\n");
fs.writeFileSync(path.join(refdir,"manifest.json"),JSON.stringify(receipt,null,2)+"\n");
const esc=s=>String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll('"',"&quot;");
const imageCard=e=>{const rel=path.relative(refdir,path.join(media,e.file.replace(/^ou-de-jianghu-e001\//,""))).replaceAll("\\","/");return '<button class="card" data-src="'+esc(rel)+'" data-label="'+esc(e.character_id+" · "+(labels[e.view]||e.view))+'"><img loading="lazy" src="'+esc(rel)+'" alt="'+esc(labels[e.view]||e.view)+'"><span>'+esc(labels[e.view]||e.view)+'</span><small>'+e.width+' × '+e.height+' · '+esc(e.key)+'</small></button>';};
const body=ids.map((id,i)=>'<section data-character="'+id+'"><h2>'+names[i]+'</h2><div class="grid">'+entries.filter(e=>e.character_id===id).map(imageCard).join("")+'</div></section>').join("");
const html='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>偶的江湖｜第一集動畫參照</title><style>*{box-sizing:border-box}body{margin:0;background:#12131a;color:#eee7dd;font:16px/1.6 system-ui,sans-serif}header,main{max-width:1440px;margin:auto;padding:28px}header{border-bottom:1px solid #41414b}h1{font-size:36px;margin:8px 0}h2{font-size:27px;margin:35px 0 14px}p{max-width:960px;color:#bbbcc8}a{color:#d9b775}nav{display:flex;gap:12px;flex-wrap:wrap}select{font:inherit;background:#252731;color:#fff;padding:10px;border:1px solid #686773;border-radius:6px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}.card{border:1px solid #44404a;background:#202129;color:#f7efe2;padding:8px;text-align:left;cursor:pointer;border-radius:8px;min-width:0}.card img{display:block;width:100%;height:290px;object-fit:contain;background:#d2d0cd;border-radius:3px}.card span{display:block;font-size:16px;margin-top:8px}.card small{display:block;color:#a9a8b4;font-size:10px;overflow-wrap:anywhere}.ensemble img{height:420px}dialog{background:#171821;color:white;border:1px solid #877b66;max-width:95vw;max-height:95vh}dialog::backdrop{background:#000d}dialog img{display:block;max-width:85vw;max-height:77vh;object-fit:contain}dialog button{font:inherit;padding:8px;float:right}.badge{color:#e4c082;font-size:14px}section[hidden]{display:none}@media(max-width:600px){header,main{padding:16px}h1{font-size:27px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.card img{height:245px}.ensemble img{height:220px}}</style><header><div class="badge">第一集 · 可審閱參照包 · 待個別採用</div><h1>偶的江湖</h1><p>九人多角度、表情、動作階段與服裝道具。74張新參照＋9張沿用正面全身。點圖放大；側面屬2D參考，動作板不是已完成動畫。原生尺寸與每張版本完整保留。</p><nav><a href="../../portraits/20261008/gallery.html">27張畫像</a><a href="../../scene-props/20261008/gallery.html">場景與道具</a><a href="../../plan/preflight-20261008-v3.1/animatic.html">文字動態分鏡</a></nav><p><label>查看角色 <select id="filter"><option value="all">全部九人</option>'+ids.map((id,i)=>'<option value="'+id+'">'+names[i]+'</option>').join("")+'</select></label></p></header><main><section class="ensemble"><h2>尺度與輪廓提案</h2><div class="grid">'+entries.filter(e=>e.character_id==="ensemble").map(imageCard).join("")+'</div><p>相對尺度供構圖比較，沒有設定精確公分數；完整角色細節以單人圖為準。</p></section>'+body+'</main><dialog id="viewer"><button id="close">關閉 ×</button><p id="caption"></p><img id="large" alt=""></dialog><script>const d=document.querySelector("#viewer");document.querySelectorAll(".card").forEach(b=>b.onclick=()=>{document.querySelector("#large").src=b.dataset.src;document.querySelector("#large").alt=b.dataset.label;document.querySelector("#caption").textContent=b.dataset.label;d.showModal()});document.querySelector("#close").onclick=()=>d.close();document.querySelector("#filter").onchange=e=>document.querySelectorAll("[data-character]").forEach(s=>s.hidden=e.target.value!=="all"&&s.dataset.character!==e.target.value);</script></html>';
fs.writeFileSync(path.join(refdir,"gallery.html"),html);
console.log(JSON.stringify({counts:receipt.counts,sources_verified:inventory.source_files.length,gallery:path.join(refdir,"gallery.html")}));
