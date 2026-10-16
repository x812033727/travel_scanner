// Cuts a 種田娶妻 episode: like 長燈村's assemble.mjs (lines-driven shot length, Hailuo audio dropped,
// zh-TW soft SRT) plus three things this series needs:
//   - data.source cuts play the source shot's clip from from_s;
//   - visual "still" shots get a slow push-in on their first frame;
//   - overlays.json draws the pale-blue system panel over a shot.
//   node assemble-zt.mjs <video.json> <overlays.json|-> <workdir> <out.mp4>
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

const [file, overlaysFile, workArg, out] = process.argv.slice(2);
const work = path.resolve(workArg);
const video = JSON.parse(readFileSync(file, "utf8"));
const overlays = overlaysFile && overlaysFile !== "-" && existsSync(overlaysFile) ? JSON.parse(readFileSync(overlaysFile, "utf8")) : {};
const LEAD = 0.25, GAP = 0.3, TAIL = 0.45, MIN = 1.6;
const FONT = "C\\:/Windows/Fonts/msjhbd.ttc";
const probe = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString().trim());
const segDir = path.join(work, "segments");
const txtDir = path.join(work, "segments", "text");
mkdirSync(txtDir, { recursive: true });
const pick = (dir, shot, ext) => { if (!existsSync(dir)) return null; const hits = readdirSync(dir).filter((n) => n.startsWith(`${shot}-t`) && n.endsWith(ext)).sort(); return hits.length ? path.join(dir, hits[hits.length - 1]) : null; };
const byId = Object.fromEntries(video.scenes.map((s) => [s.id, s]));
const COLORS = { panel: "0x5ec8ff", task: "0xffd75e", affection: "0xff8fb8", reward: "0xffe08a", penalty: "0xff6b6b" };

function panelFilters(shot, dur) {
  const items = overlays[shot] ?? [];
  if (!items.length) return "";
  const lines = items.slice(0, 2);
  const h = 70 + 64 * lines.length;
  const y0 = 120;
  const start = 0.15;
  let f = `,drawbox=x=(iw-1000)/2:y=${y0}:w=1000:h=${h}:color=0x0b2a4a@0.62:t=fill:enable='gte(t,${start})'`;
  f += `,drawbox=x=(iw-1000)/2:y=${y0}:w=1000:h=${h}:color=0x7fd6ff@0.9:t=3:enable='gte(t,${start})'`;
  lines.forEach((item, i) => {
    const tf = path.join(txtDir, `${shot}-${i}.txt`);
    writeFileSync(tf, item.text);
    const tfEsc = tf.replace(/\\/g, "/").replace(/:/g, "\\:");
    const color = COLORS[item.kind] ?? COLORS.panel;
    f += `,drawtext=fontfile='${FONT}':textfile='${tfEsc}':fontsize=52:fontcolor=${color}:shadowcolor=0x000000@0.8:shadowx=2:shadowy=2:x=(w-text_w)/2:y=${y0 + 38 + 64 * i}:enable='gte(t,${start + 0.1 * i})'`;
  });
  return f;
}

const stillMove = (id, f) => { const k = [...id].reduce((a, c) => a + c.charCodeAt(0), 0) % 4; if (k === 0) return `z='1+0.16*on/${f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'`; if (k === 1) return `z='1.16-0.14*on/${f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'`; if (k === 2) return `z='1.14':x='(iw-iw/zoom)*on/${f}':y='ih/2-(ih/zoom/2)'`; return `z='1.14':x='(iw-iw/zoom)*(1-on/${f})':y='ih/2-(ih/zoom/2)'`; };
const srt = [];
const report = [];
let t = 0;
const segs = [];
const fmt = (s) => { const ms = Math.round(s * 1000); const h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, sec = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")},${String(ms % 1000).padStart(3, "0")}`; };
for (const scene of video.scenes) {
  if (scene.template !== "shot") continue;
  const lines = (scene.lines ?? []).map((l) => ({ ...l, wav: path.join(work, "audio", `${l.id}.wav`) }));
  for (const l of lines) l.len = probe(l.wav);
  let dur = lines.length ? LEAD + lines.reduce((a, l) => a + l.len, 0) + GAP * (lines.length - 1) + TAIL : scene.action_seconds ?? scene.data?.action_seconds ?? 2;
  dur = Math.max(dur, MIN);
  const src = scene.data?.source;
  const clip = src ? pick(path.join(work, "clips"), src.shot, ".mp4") : pick(path.join(work, "clips"), scene.id, ".mp4");
  const still = pick(path.join(work, "first-frames"), src ? src.shot : scene.id, ".png") ?? pick(path.join(work, "first-frames"), src ? src.shot : scene.id, ".jpg");
  const isStill = scene.data?.visual === "still" || !clip;
  const seg = path.join(segDir, `${scene.id}.mp4`);
  const args = ["-v", "error", "-y"];
  let vf;
  let note;
  const overlay = panelFilters(scene.id, dur);
  if (!isStill) {
    const from = src ? Number(src.from_s ?? 0) : 0;
    const clipLen = probe(clip) - from;
    args.push("-ss", from.toFixed(3), "-i", clip);
    const slow = dur > clipLen ? Math.min(dur / clipLen, 1.6) : 1;
    vf = `[0:v]setpts=${slow.toFixed(4)}*(PTS-STARTPTS),scale=1920:1080:flags=lanczos,fps=24,format=yuv420p,tpad=stop_mode=clone:stop_duration=${Math.max(0, dur - clipLen * slow + 0.1).toFixed(3)},trim=duration=${dur.toFixed(3)},setpts=PTS-STARTPTS${overlay}[v]`;
    note = `${path.basename(clip)}${src ? `@${from}s` : ""} (${clipLen.toFixed(2)}s x${slow.toFixed(2)}${dur > clipLen * slow ? ", held " + (dur - clipLen * slow).toFixed(2) + "s" : ""})`;
  } else {
    if (!still) throw new Error(`${scene.id}: no clip and no first frame`);
    const frames = Math.ceil(dur * 24) + 2;
    args.push("-i", still);
    vf = `[0:v]scale=3840:2160:flags=lanczos,zoompan=${stillMove(scene.id, frames)}:d=${frames}:s=1920x1080:fps=24,format=yuv420p,trim=duration=${dur.toFixed(3)},setpts=PTS-STARTPTS${overlay}[v]`;
    note = `${scene.data?.visual === "still" ? "still" : "STILL-FALLBACK"} ${path.basename(still)}`;
  }
  let at = LEAD;
  const amix = [];
  lines.forEach((l, i) => {
    args.push("-i", l.wav);
    const ms = Math.round(at * 1000);
    amix.push(`[${i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${ms}|${ms}[a${i}]`);
    srt.push({ start: t + at, end: t + at + l.len, text: l.text });
    at += l.len + GAP;
  });
  args.push("-f", "lavfi", "-t", dur.toFixed(3), "-i", "anullsrc=r=48000:cl=stereo");
  const silence = lines.length + 1;
  const graph = [vf, ...amix, `${lines.map((_, i) => `[a${i}]`).join("")}[${silence}:a]amix=inputs=${lines.length + 1}:normalize=0:duration=longest,atrim=duration=${dur.toFixed(3)}[a]`].join(";");
  args.push("-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-t", dur.toFixed(3), seg);
  execFileSync("ffmpeg", args, { stdio: "inherit" });
  segs.push(seg);
  report.push(`${scene.id} ${dur.toFixed(2)}s ${note}${overlays[scene.id] ? " +panel" : ""} ${lines.map((l) => l.id).join(",")}`);
  t += dur;
}
const list = path.join(segDir, "list.txt");
writeFileSync(list, segs.map((s) => `file '${s.replace(/\\/g, "/")}'`).join("\n") + "\n");
const srtFile = out.replace(/\.mp4$/, ".zh-TW.srt");
writeFileSync(srtFile, srt.map((c, i) => `${i + 1}\n${fmt(c.start)} --> ${fmt(c.end)}\n${c.text}\n`).join("\n"));
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-i", srtFile, "-map", "0:v", "-map", "0:a", "-map", "1:s", "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", "-movflags", "+faststart", out], { stdio: "inherit" });
console.log(report.join("\n"));
console.log(`total ${t.toFixed(2)}s -> ${out}`);
