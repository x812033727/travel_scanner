#!/usr/bin/env node
// 動態分鏡（animatic）：買任何一秒片段之前，用分鏡表的文字卡或已畫的關鍵影格，照配音的時間軸（沒錄就用 lint 的
// 估法）排成一支可以實速看的片子：節奏、資訊順序、開場 10／30 秒、空間與視線，在這裡看出問題只要改字。
// 輸出一頁自帶的 HTML（關鍵影格與 narration.wav 用相對路徑引用，不內嵌），每鏡照 camera 行模擬推、拉、搖、俯仰，
// 疊上鏡號、台詞、類型與風險；已經買到（clips/manifest.json 裡沒標 needs_review）的片段直接換上去播，同一支片子從文字卡、
// 關鍵影格一路換到素材（動畫業的「一支活的 animatic」），節奏走樣馬上看得到。--mp4 在每鏡都有圖時用 ffmpeg 接成影片
// （只用圖，沒有疊字，不需要字型）。
//
//   node .agents/skills/animation-preproduction/scripts/animatic.mjs --slug <SLUG> | --file <video.json> [--workdir <dir>]
//     [--out <animatic.html>] [--mp4 <animatic.mp4>] [--route server|hailuo|kling] [--plan ...] [--root <repo>]
//
// --slug 的工作目錄照 tools/video 的規則，預設輸出 <workdir>/plan/animatic.html；--file 沒給 --workdir 時只有文字卡，
// 要給 --out。離線、不花錢。結束碼：0；--mp4 但有鏡頭沒有圖是 1；讀不到或參數錯是 2；要 --mp4 卻找不到 ffmpeg 是 5。
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { locateFfmpeg, runTool, ToolMissing } from "../../../../tools/video/assemble/ffmpeg.mjs";
import { readJson } from "../../../../tools/video/core/paths.mjs";
import { estimateTimeline, FPS } from "../../../../tools/video/core/timeline.mjs";
import { loadInputs, PLAN_FLAGS, PLAN_USAGE, planEpisode, planOptions } from "./shot_plan.mjs";

const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);
// The data sits inside <script>: every less-than sign becomes a six-character JSON escape (backslash, u003c), so no
// closing script tag inside a line of dialogue can end the block. U+2028 and U+2029 are legal in a string since ES2019.
const LT_ESCAPE = `${String.fromCharCode(92)}u003c`;
const forScript = (value) => JSON.stringify(value).replaceAll("<", LT_ESCAPE);
const toUrl = (file) => file.split(path.sep).map(encodeURIComponent).join("/");
const linkFrom = (outDir, absolute) => {
  if (!outDir) return pathToFileURL(absolute).href;
  const relative = path.relative(outDir, absolute);
  return path.isAbsolute(relative) ? pathToFileURL(absolute).href : toUrl(relative);
};

/**
 * 每鏡在片子裡的位置與畫面：{ id, start, end, image, video, video_offset, move, kind, setup, camera, motion, lines, risk, buy_s, source }。
 * 時間照 timeline（錄好的或估的）的 scenes；圖是這一鏡的關鍵影格，切鏡用來源鏡頭的圖；clips 是 clips/manifest.json，
 * 有檔案、沒標 needs_review 的素材換上去播（切鏡從來源素材的 from_s 秒播起）。
 */
export function animaticShots(doc, plan, { timeline = null, manifest = null, clips = null, workdir = null, outDir = null } = {}) {
  let placed = timeline;
  if (!placed) {
    try {
      placed = estimateTimeline(doc);
    } catch {
      placed = null;
    }
  }
  const spans = new Map((placed?.scenes ?? []).map((scene) => [scene.id, [scene.start_frame / FPS, scene.end_frame / FPS]]));
  const sceneById = new Map(doc.scenes.map((scene) => [scene.id, scene]));
  let clock = 0;
  return plan.shots.map((shot) => {
    const [start, end] = spans.get(shot.id) ?? [clock, clock + shot.need_s];
    clock = end;
    const imageOf = (id) => {
      const file = manifest?.shots?.[id]?.file;
      if (!file || !workdir) return null;
      const absolute = path.join(workdir, file);
      if (!existsSync(absolute)) return null;
      return { absolute, url: linkFrom(outDir, absolute) };
    };
    const image = shot.visual === "cut" ? imageOf(shot.source.shot) : imageOf(shot.id);
    const clipOf = (id) => {
      const entry = clips?.shots?.[id];
      if (!entry?.file || entry.needs_review || entry.still || entry.source || !workdir) return null;
      const absolute = path.join(workdir, entry.file);
      if (!existsSync(absolute)) return null;
      return linkFrom(outDir, absolute);
    };
    const video = shot.visual === "cut" ? clipOf(shot.source.shot) : shot.visual === "clip" ? clipOf(shot.id) : null;
    const scene = sceneById.get(shot.id);
    return {
      id: shot.id,
      start: Math.round(start * 1000) / 1000,
      end: Math.round(end * 1000) / 1000,
      image: image?.url ?? null,
      video,
      video_offset: video && shot.visual === "cut" ? shot.source.from_s : 0,
      image_file: image?.absolute ?? null,
      move: shot.move.web.group,
      kind: shot.visual,
      setup: `${shot.chapter}／${shot.setup}`,
      camera: shot.camera,
      motion: scene?.data?.motion ?? "",
      lines: shot.lines,
      risk: shot.visual === "cut" ? null : shot.risk.grade,
      risk_reasons: shot.risk.reasons.map((reason) => reason.id),
      buy_s: shot.buy_s,
      source: shot.source,
    };
  });
}

/** 看片時要對的數字：鏡數、中位數、最長、前 10／30 秒開始幾鏡（同 drama-craft.md 的目標）。 */
export function animaticStats(shots) {
  const lengths = shots.map((shot) => shot.end - shot.start).sort((a, b) => a - b);
  const median = lengths.length ? lengths[Math.floor(lengths.length / 2)] : 0;
  return {
    shots: shots.length,
    seconds: shots.length ? Math.round(shots.at(-1).end * 10) / 10 : 0,
    median: Math.round(median * 100) / 100,
    longest: Math.round((lengths.at(-1) ?? 0) * 100) / 100,
    opening_10s: shots.filter((shot) => shot.start < 10).length,
    opening_30s: shots.filter((shot) => shot.start < 30).length,
  };
}

export function animaticHtml({ title, shots, stats, audio = null, basis }) {
  return `<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>動態分鏡：${escapeHtml(title)}</title>
<style>
:root{--bg:#0f1418;--panel:#182129;--line:#2c3a45;--text:#eef2f5;--muted:#a9b6c1;--a:#7fc8a9;--b:#f0c674;--c:#ef8a80}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 system-ui,sans-serif}
header,main{max-width:1180px;margin:auto;padding:16px}h1{font-size:22px;margin:0 0 4px}small,.muted{color:var(--muted)}
.stage{position:relative;aspect-ratio:16/9;background:#000;overflow:hidden;border-radius:10px;border:1px solid var(--line)}
.stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform-origin:50% 50%}
.card{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:8px;padding:6%;background:linear-gradient(160deg,#1d2a33,#0d1216)}
.card h2{margin:0;font-size:clamp(18px,3vw,34px)}.card p{margin:0;font-size:clamp(13px,1.8vw,20px);color:#d7e0e6}
.tag{position:absolute;top:10px;left:10px;background:rgba(0,0,0,.7);padding:3px 10px;border-radius:6px;font:13px/1.5 ui-monospace,monospace}
.sub{position:absolute;left:8%;right:8%;bottom:6%;text-align:center;font-size:clamp(14px,2.2vw,26px);text-shadow:0 0 6px #000,0 0 2px #000}
.risk-A{color:var(--a)}.risk-B{color:var(--b)}.risk-C{color:var(--c)}
.bar{display:flex;gap:8px;align-items:center;margin:10px 0;flex-wrap:wrap}button{font:inherit;background:#233746;color:inherit;border:1px solid #506676;border-radius:8px;padding:6px 12px;cursor:pointer}
input[type=range]{flex:1;min-width:200px}.strip{display:flex;height:22px;border:1px solid var(--line);border-radius:6px;overflow:hidden;cursor:pointer}
.strip div{border-right:1px solid #0008;font:11px/22px ui-monospace,monospace;overflow:hidden;white-space:nowrap;padding-left:3px}
.k-clip{background:#2d4b63}.k-still{background:#3f4a2d}.k-cut{background:#4b2d55}
main{overflow-wrap:anywhere}.scroll{overflow-x:auto;max-width:100%}table{min-width:720px;width:100%;border-collapse:collapse;margin-top:14px;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:5px;text-align:left;vertical-align:top}tr.on{background:#22323d}
</style>
<header><h1>動態分鏡：${escapeHtml(title)}</h1><small>${escapeHtml(basis)}。這是前製預覽：畫面是文字卡或已畫的關鍵影格，運鏡是在圖上模擬的，不是買來的動畫。先實速看一次，再逐鏡停。</small>
<p class="muted">${stats.shots} 鏡、約 ${stats.seconds} 秒；鏡長中位數 ${stats.median} 秒、最長 ${stats.longest} 秒；前 10 秒開始 ${stats.opening_10s} 鏡、前 30 秒 ${stats.opening_30s} 鏡（drama-craft.md 的目標：中位數 2–4 秒、建議 2.5–3.5，最長 ≤ 8，前 10 秒 ≥ 4，前 30 秒 ≥ 10；運鏡是在圖上模擬的，方向照攝影機：pan left 畫面往右跑）</p></header>
<main><div class="stage" id="stage"></div>
<div class="bar"><button id="play">播放</button><button id="prev">上一鏡</button><button id="next">下一鏡</button><input id="clock" type="range" min="0" step="0.05" aria-label="時間"><span id="time" class="muted"></span></div>
<div class="strip" id="strip"></div>
<div class="scroll"><table><thead><tr><th>鏡</th><th>時間</th><th>場／鏡位</th><th>類型</th><th>camera</th><th>動作</th><th>台詞</th><th>風險</th></tr></thead><tbody id="rows"></tbody></table></div>
${audio ? `<audio id="audio" src="${escapeHtml(audio)}" preload="auto"></audio>` : ""}
</main>
<script>
const shots=${forScript(shots)};const total=shots.length?shots[shots.length-1].end:0;const $=id=>document.getElementById(id);
const audio=$("audio");let playing=false,t=0,last=null,current=-1;
const safe=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const KIND={clip:"clip",still:"still",cut:"切"};
$("clock").max=total;
$("strip").innerHTML=shots.map((s,i)=>'<div class="k-'+s.kind+'" data-i="'+i+'" style="flex:'+Math.max(.05,s.end-s.start)+'">'+safe(s.id)+'</div>').join("");
$("rows").innerHTML=shots.map((s,i)=>'<tr data-i="'+i+'"><td>'+safe(s.id)+'</td><td>'+s.start.toFixed(1)+'–'+s.end.toFixed(1)+'</td><td>'+safe(s.setup)+'</td><td>'+(s.kind==="cut"?"切自 "+safe(s.source.shot):KIND[s.kind]+(s.buy_s?" "+s.buy_s+" s":""))+'</td><td>'+safe(s.camera)+'</td><td>'+safe(s.motion)+'</td><td>'+s.lines.map(l=>safe(l.speaker)+"："+safe(l.text)).join("<br>")+'</td><td class="risk-'+(s.risk||"A")+'">'+(s.risk?s.risk+(s.risk_reasons.length?" "+safe(s.risk_reasons.join(", ")):""):"—")+'</td></tr>').join("");
function moveTransform(move,p){switch(move){case"push in":return"scale("+(1+.1*p)+")";case"pull out":return"scale("+(1.1-.1*p)+")";case"pan left":return"scale(1.08) translateX("+(-3+6*p)+"%)";case"pan right":return"scale(1.08) translateX("+(3-6*p)+"%)";case"tilt up":return"scale(1.08) translateY("+(-3+6*p)+"%)";case"tilt down":return"scale(1.08) translateY("+(3-6*p)+"%)";case"drift":case null:return"scale(1.04) translate("+(-1+2*p)+"%,0)";default:return"none"}}
function lineAt(s,time){if(!s.lines.length)return"";const span=(s.end-s.start)/s.lines.length;const k=Math.min(s.lines.length-1,Math.floor((time-s.start)/span));return s.lines[k].speaker+"："+s.lines[k].text}
function show(time){t=Math.max(0,Math.min(total,time));const i=Math.max(0,shots.findIndex(s=>t<s.end));const s=shots[i]??shots[shots.length-1];if(!s)return;
if(i!==current){current=i;const body=s.video?'<video id="vid" src="'+safe(s.video)+'" muted playsinline preload="auto" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000"></video>':s.image?'<img id="img" src="'+safe(s.image)+'" alt="">':'<div class="card"><h2>'+safe(s.id)+'｜'+safe(s.setup)+'</h2><p>'+safe(s.camera)+'</p><p>'+safe(s.motion)+'</p></div>';
$("stage").innerHTML=body+'<div class="tag">'+safe(s.id)+' '+(s.video?"素材 ":s.image?"關鍵影格 ":"文字卡 ")+(s.kind==="cut"?"切自 "+safe(s.source.shot):KIND[s.kind])+(s.risk?' <span class="risk-'+s.risk+'">'+s.risk+'</span>':'')+'</div><div class="sub" id="sub"></div>';
document.querySelectorAll("#rows tr").forEach(r=>r.classList.toggle("on",+r.dataset.i===i))}
const img=$("img");if(img)img.style.transform=moveTransform(s.move,(t-s.start)/Math.max(.001,s.end-s.start));
const vid=$("vid");if(vid){const want=s.video_offset+(t-s.start);if(Math.abs(vid.currentTime-want)>.25)vid.currentTime=want;if(playing&&vid.paused)vid.play().catch(()=>{});if(!playing&&!vid.paused)vid.pause()}
$("sub").textContent=lineAt(s,t);$("clock").value=t;$("time").textContent=t.toFixed(1)+" / "+total.toFixed(1)+" 秒"}
function tick(now){if(!playing)return;if(audio&&!audio.paused){show(audio.currentTime)}else if(!audio){if(last!==null)show(t+(now-last)/1000);last=now}if(t>=total){stop();return}requestAnimationFrame(tick)}
function play(){if(t>=total)t=0;playing=true;last=null;$("play").textContent="暫停";if(audio){audio.currentTime=t;audio.play().catch(()=>{})}requestAnimationFrame(tick)}
function stop(){playing=false;$("play").textContent="播放";if(audio)audio.pause()}
$("play").onclick=()=>playing?stop():play();
$("prev").onclick=()=>{const i=Math.max(0,current-1);stop();show(shots[i].start);if(audio)audio.currentTime=t};
$("next").onclick=()=>{const i=Math.min(shots.length-1,current+1);stop();show(shots[i].start);if(audio)audio.currentTime=t};
$("clock").oninput=e=>{show(+e.target.value);if(audio)audio.currentTime=t};
$("strip").onclick=e=>{const i=e.target.dataset.i;if(i!==undefined){show(shots[+i].start);if(audio)audio.currentTime=t}};
document.addEventListener("keydown",e=>{if(e.code==="Space"){e.preventDefault();playing?stop():play()}if(e.code==="ArrowRight")$("next").click();if(e.code==="ArrowLeft")$("prev").click()});
show(0);
</script></html>
`;
}

/** ffmpeg 的 concat 清單與參數：每鏡一張圖停在它的長度，配上 narration（有的話）。沒有疊字，不需要字型。 */
export function animaticFfmpegArgs(shots, { list, out, audio = null }) {
  const lines = ["ffconcat version 1.0"];
  for (const shot of shots) {
    lines.push(`file '${shot.image_file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`);
    lines.push(`duration ${(shot.end - shot.start).toFixed(3)}`);
  }
  // The demuxer holds the last entry only when a file follows it; -t below trims the extra copy.
  if (shots.length) lines.push(`file '${shots.at(-1).image_file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`);
  const args = ["-hide_banner", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list];
  if (audio) args.push("-i", audio);
  args.push("-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26");
  if (audio) args.push("-c:a", "aac", "-b:a", "128k", "-shortest");
  // The total length is the timeline's, whatever the demuxer does with the last picture.
  if (shots.length) args.push("-t", shots.at(-1).end.toFixed(3));
  args.push("-movflags", "+faststart", out);
  return { list: `${lines.join("\n")}\n`, args };
}

export async function main(argv, stdout = process.stdout, stderr = process.stderr) {
  let values;
  try {
    ({ values } = parseArgs({
      args: argv,
      options: {
        ...PLAN_FLAGS,
        slug: { type: "string" },
        file: { type: "string" },
        workdir: { type: "string" },
        root: { type: "string" },
        out: { type: "string" },
        mp4: { type: "string" },
      },
      strict: true,
    }));
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  if ((!values.slug && !values.file) || (values.file && !values.workdir && !values.out)) {
    stderr.write(`usage: animatic.mjs --slug <SLUG> | --file <video.json> [--workdir <dir>] [--out <animatic.html>] [--mp4 <animatic.mp4>] ${PLAN_USAGE}\n`);
    return 2;
  }
  let inputs;
  let plan;
  try {
    inputs = loadInputs({ file: values.file, slug: values.slug, workdir: values.workdir, root: values.root, timeline: values.timeline });
    plan = planEpisode(inputs.doc, { ...planOptions(values), timeline: inputs.timeline, manifest: inputs.manifest, series: inputs.series });
  } catch (error) {
    stderr.write(`${values.slug ?? values.file}: ${error.message}\n`);
    return 2;
  }
  const out = path.resolve(values.out ?? path.join(inputs.workdir, "plan", "animatic.html"));
  const outDir = path.dirname(out);
  const clips = inputs.workdir ? readJson(path.join(inputs.workdir, "clips", "manifest.json"), null) : null;
  const shots = animaticShots(inputs.doc, plan, { timeline: inputs.timeline, manifest: inputs.manifest, clips, workdir: inputs.workdir, outDir });
  const stats = animaticStats(shots);
  const narration = inputs.workdir && inputs.timeline && existsSync(path.join(inputs.workdir, "narration.wav")) ? path.join(inputs.workdir, "narration.wav") : null;
  const basis = inputs.timeline ? "時間照錄好的 timeline.json，聲音是 narration.wav" : `時間照 lint 的估法（還沒錄配音${inputs.timeline_stale ? "，或 timeline.json 是舊台詞錄的" : ""}），沒有聲音`;
  mkdirSync(outDir, { recursive: true });
  writeFileSync(out, animaticHtml({ title: inputs.doc.title ?? inputs.doc.slug ?? path.basename(inputs.file), shots, stats, audio: narration ? linkFrom(outDir, narration) : null, basis }));
  const pictured = shots.filter((shot) => shot.image).length;
  const bought = shots.filter((shot) => shot.video).length;
  stdout.write(`動態分鏡 ${out}：${stats.shots} 鏡、約 ${stats.seconds} 秒，${bought} 鏡是買到的素材、${pictured - shots.filter((shot) => shot.video && shot.image).length} 鏡是關鍵影格、${stats.shots - pictured - shots.filter((shot) => shot.video && !shot.image).length} 鏡是文字卡；${basis}\n`);
  if (!values.mp4) return 0;
  const missing = shots.filter((shot) => !shot.image_file);
  if (missing.length) {
    stderr.write(`--mp4 needs a keyframe for every shot; missing: ${missing.map((shot) => shot.id).join(", ")} (the HTML shows them as cards)\n`);
    return 1;
  }
  let tools;
  try {
    tools = await locateFfmpeg();
  } catch (error) {
    if (error instanceof ToolMissing) {
      stderr.write(`${error.message}\n`);
      return 5;
    }
    throw error;
  }
  const mp4 = path.resolve(values.mp4);
  const list = path.join(path.dirname(mp4), `${path.basename(mp4, path.extname(mp4))}.ffconcat`);
  const { list: text, args } = animaticFfmpegArgs(shots, { list, out: mp4, audio: narration });
  writeFileSync(list, text);
  await runTool(tools.ffmpeg, args);
  stdout.write(`影片版 ${mp4}\n`);
  return 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
