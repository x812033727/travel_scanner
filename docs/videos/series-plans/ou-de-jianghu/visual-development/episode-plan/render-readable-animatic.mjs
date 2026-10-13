#!/usr/bin/env node
// Presentation-only v3.1 overlay. Preserve the frozen v3 HTML and all timing/dialogue data.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const base=path.resolve(process.argv[2]||'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const out=path.resolve(process.argv[3]||path.join(path.dirname(base),'preflight-20261008-v3.1'));
if(base===out)throw Error('Use a separate v3.1 directory; frozen v3 must remain intact');
const sha=b=>createHash('sha256').update(b).digest('hex');
const raw=fs.readFileSync(path.join(base,'animatic.html'),'utf8');
if(sha(raw)!=='2d8d5457f4056a3b99f46cf34d580b41791dd172aec0d60119b22a406b96353c')throw Error('Unexpected v3 HTML: re-review before changing its presentation');
const video=fs.readFileSync(path.join(base,'video.json'));
const doc=JSON.parse(video),shots=JSON.parse(fs.readFileSync(path.join(base,'animatic-scenes.json'),'utf8'));
const frameText=Object.fromEntries(doc.scenes.filter(s=>s.template==='shot').map(s=>[s.id,{first:s.data.prompt,end:s.data.end_frame?.prompt||null}]));
if(Object.keys(frameText).length!==455||Object.values(frameText).some(f=>!f.first))throw Error('Missing first-frame narrative');
let html=raw.replaceAll('｜v3 提案','｜v3.1 卡面補充（沿用v3時間）');
html=html.replace('</style>',`.card{justify-content:flex-start;padding:44px 4% 98px;gap:7px}.card h2{font-size:clamp(16px,2vw,25px)}.card p{font-size:clamp(12px,1.25vw,16px);line-height:1.45}.card .frame{color:#edf3e7}.frame b{color:#b8d7a4}.card .motion{color:#bfcdd8}.card .end{color:#ecd7a4}.sub{bottom:3%;font-size:clamp(14px,1.8vw,22px)}select{max-width:190px;background:#233746;color:#eef2f5;border:1px solid #506676;padding:8px;border-radius:6px}\n</style>`);
const old="safe(s.motion)+'</p></div>'";
const replacement="safe(s.motion)+'</p>'+frameMarkup(s)+'</div>'";
if(!html.includes(old))throw Error('Unknown card template');
html=html.replace(old,replacement);
const overlay=`const frameText=${JSON.stringify(frameText).replace(/</g,'\\u003c')};
function frameMarkup(s){const f=frameText[s.id];if(!f)return '';return '<p class="frame"><b>'+ (s.kind==='still'?'靜態結果':'首格')+'：</b>'+safe(f.first)+'</p>'+(f.end?'<p class="end"><b>末格：</b>'+safe(f.end)+'</p>':'')}
`;
html=html.replace('function show(time){',overlay+'function show(time){');
html=html.replace('<button id="prev">','<label for="shot-jump">跳至鏡號</label><select id="shot-jump" aria-label="跳至鏡號"></select><button id="prev">');
html=html.replace('show(0);',`$("shot-jump").innerHTML=shots.map((s,i)=>'<option value="'+i+'">'+safe(s.id)+'</option>').join('');
$("shot-jump").onchange=e=>{stop();show(shots[+e.target.value].start);if(audio)audio.currentTime=t};
show(0);`);
html=html.replace('$("sub").textContent=lineAt(s,t);','$("shot-jump").value=i;$("sub").textContent=lineAt(s,t);');
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'animatic.html'),html);
fs.writeFileSync(path.join(out,'frame-text.json'),JSON.stringify(frameText,null,2)+'\n');
const receipt={version:'v3.1-presentation-only',created_at:new Date().toISOString(),base_video_sha256:sha(video),base_html_sha256:sha(raw),html_sha256:sha(html),frames:455,end_frames:Object.values(frameText).filter(f=>f.end).length,scene_count:shots.length,exact_seconds:shots.at(-1).end,changes:['Display original working-video first-frame prompt on all 455 shot cards, including 30 still results.','Display 3 planned end-frame prompts.','Add an explicit shot-id jump control for targeted review.'],unchanged:['working video','scene order','start/end times','dialogue','motion','camera','risk labels','budget'],verification:{all_first_frames_present:true,frozen_base_html_unchanged:sha(fs.readFileSync(path.join(base,'animatic.html')))===sha(raw),no_full_speed_v31_review_claimed:true},browser_targeted_review:'pending independent viewer'};
fs.writeFileSync(path.join(out,'presentation-change.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify(receipt,null,2));
