// v4 cut of a 種田娶妻 episode, built from the same clips as v3 (no new generation):
//   - tighter timing (dialogue sped 7%, shorter lead/gap/tail) and long shots split into a wide
//     part and a punch-in part, so the cut reads at short-drama pace;
//   - a grade per setting (lower saturation, deeper blacks, cool/warm split, vignette, grain);
//   - burned-in subtitles, a name card the first time a character matters, a title card;
//   - a mix: dialogue, Lyria music cues ducked under dialogue, CC0 effects and synthetic beds.
//   node assemble-v4.mjs <video.json> <overlays.json|-> <edit.json> <workdir> <out.mp4>
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

const [file, overlaysFile, editFile, workArg, out] = process.argv.slice(2);
const work = path.resolve(workArg);
const video = JSON.parse(readFileSync(file, "utf8"));
const overlays = overlaysFile && overlaysFile !== "-" && existsSync(overlaysFile) ? JSON.parse(readFileSync(overlaysFile, "utf8")) : {};
const edit = JSON.parse(readFileSync(editFile, "utf8"));
const TEMPO = edit.tempo ?? 1.07, LEAD = 0.12, GAP = 0.12, TAIL = 0.22, MIN = 1.2, ACTION_MAX = 2.4, SPLIT = 3.0, PUNCH = 1.3;
const FONT = "C\\:/Windows/Fonts/msjhbd.ttc";
const probe = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString().trim());
const segDir = path.join(work, "segments-v4");
const txtDir = path.join(segDir, "text");
const fastDir = path.join(segDir, "lines");
mkdirSync(txtDir, { recursive: true });
mkdirSync(fastDir, { recursive: true });
const esc = (p) => p.replace(/\\/g, "/").replace(/:/g, "\\:");
const textFile = (name, text) => { const f = path.join(txtDir, `${name}.txt`); writeFileSync(f, text); return esc(f); };
const pick = (dir, shot) => { if (!existsSync(dir)) return null; const hits = readdirSync(dir).filter((n) => n.startsWith(`${shot}-t`) && /\.(mp4|png|jpg)$/.test(n)).sort(); return hits.length ? path.join(dir, hits[hits.length - 1]) : null; };
const firstTake = (dir, shot) => { if (!existsSync(dir)) return null; const hits = readdirSync(dir).filter((n) => n.startsWith(`${shot}-t`) && n.endsWith(".mp4") && !n.includes("-tsp")).sort(); return hits.length ? path.join(dir, hits[hits.length - 1]) : null; };

const GRADES = {
  day: "eq=contrast=1.10:saturation=0.80:gamma=0.94:brightness=-0.015,colorbalance=rs=-0.03:bs=0.035:rm=0.01:bm=-0.01:rh=0.025:bh=-0.035",
  indoor: "eq=contrast=1.14:saturation=0.78:gamma=0.90:brightness=-0.03,colorbalance=rs=-0.02:bs=0.03:rh=0.035:gh=0.01:bh=-0.04",
  river: "eq=contrast=1.10:saturation=0.70:gamma=0.95,colorbalance=rs=-0.05:gs=0.01:bs=0.06:rh=0.02:bh=-0.02",
  night: "eq=contrast=1.18:saturation=0.70:gamma=0.92,colorbalance=rs=-0.05:bs=0.08:rm=-0.02:bm=0.04",
  dh: "eq=contrast=1.05:saturation=0.92:gamma=0.98",
  office: "eq=contrast=1.08:saturation=0.72:gamma=0.97,colorbalance=rs=-0.03:bs=0.05:rh=-0.01:bh=0.02",
};
const gradeOf = (id) => { for (const [g, ids] of Object.entries(edit.grades ?? {})) if (ids.includes(id)) return g; return edit.default_grade ?? "day"; };
const FINISH = edit.finish ?? "vignette=angle=PI/4.6,noise=alls=5:allf=t,format=yuv420p";

const COLORS = { panel: "0x5ec8ff", task: "0xffd75e", affection: "0xff8fb8", reward: "0xffe08a", penalty: "0xff6b6b" };
function panelFilters(shot) {
  const items = (overlays[shot] ?? []).slice(0, 2);
  if (!items.length) return "";
  const h = 70 + 64 * items.length, y0 = 120, start = 0.15;
  let f = `,drawbox=x=(iw-1000)/2:y=${y0}:w=1000:h=${h}:color=0x0b2a4a@0.62:t=fill:enable='gte(t,${start})'`;
  f += `,drawbox=x=(iw-1000)/2:y=${y0}:w=1000:h=${h}:color=0x7fd6ff@0.9:t=3:enable='gte(t,${start})'`;
  items.forEach((item, i) => {
    f += `,drawtext=fontfile='${FONT}':textfile='${textFile(`${shot}-p${i}`, item.text)}':fontsize=52:fontcolor=${COLORS[item.kind] ?? COLORS.panel}:shadowcolor=0x000000@0.8:shadowx=2:shadowy=2:x=(w-text_w)/2:y=${y0 + 38 + 64 * i}:enable='gte(t,${start + 0.1 * i})'`;
  });
  return f;
}
// The first time a character matters: gold name and a white tag, bottom-left above the subtitles.
function nameCard(shot) {
  const card = edit.names?.[shot];
  if (!card) return "";
  const [name, tag] = card, a = 0.25, b = 2.6;
  const alpha = `if(lt(t,${a}),0,if(lt(t,${a + 0.25}),(t-${a})/0.25,if(lt(t,${b - 0.3}),1,max(0,(${b}-t)/0.3))))`;
  return `,drawbox=x=96:y=596:w=8:h=150:color=0xe8c26a@0.95:t=fill:enable='between(t,${a},${b})'` +
    `,drawtext=fontfile='${FONT}':textfile='${textFile(`${shot}-n`, name)}':fontsize=84:fontcolor=0xf3d27a:alpha='${alpha}':borderw=3:bordercolor=0x000000@0.7:x=124:y=598` +
    `,drawtext=fontfile='${FONT}':textfile='${textFile(`${shot}-t`, tag)}':fontsize=40:fontcolor=0xffffff:alpha='${alpha}':borderw=2:bordercolor=0x000000@0.7:x=128:y=700`;
}
function titleCard(shot) {
  const tc = edit.title;
  if (!tc || tc.shot !== shot) return "";
  const a = tc.from ?? 0.2, b = tc.to ?? 3.2;
  const alpha = `if(lt(t,${a}),0,if(lt(t,${a + 0.3}),(t-${a})/0.3,if(lt(t,${b - 0.4}),1,max(0,(${b}-t)/0.4))))`;
  return `,drawtext=fontfile='${FONT}':textfile='${textFile(`${shot}-title`, tc.text)}':fontsize=96:fontcolor=0xf3d27a:alpha='${alpha}':borderw=4:bordercolor=0x2a1400@0.85:x=(w-text_w)/2:y=110` +
    `,drawtext=fontfile='${FONT}':textfile='${textFile(`${shot}-sub`, tc.sub)}':fontsize=44:fontcolor=0xffffff:alpha='${alpha}':borderw=3:bordercolor=0x000000@0.8:x=(w-text_w)/2:y=226`;
}
const subtitle = (name, text, a, b, color = "0xffffff") =>
  `,drawtext=fontfile='${FONT}':textfile='${textFile(name, text)}':fontsize=60:fontcolor=${color}:borderw=4:bordercolor=0x000000@0.9:shadowcolor=0x000000@0.6:shadowx=2:shadowy=3:x=(w-text_w)/2:y=h-160:enable='between(t,${a.toFixed(3)},${b.toFixed(3)})'`;
const stillMove = (id, f) => { const k = [...id].reduce((a, c) => a + c.charCodeAt(0), 0) % 4; if (k === 0) return `z='1+0.16*on/${f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'`; if (k === 1) return `z='1.16-0.14*on/${f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'`; if (k === 2) return `z='1.14':x='(iw-iw/zoom)*on/${f}':y='ih/2-(ih/zoom/2)'`; return `z='1.14':x='(iw-iw/zoom)*(1-on/${f})':y='ih/2-(ih/zoom/2)'`; };

const report = [], segs = [], starts = {}, lineAt = [], srt = [];
let t = 0;
for (const scene of video.scenes) {
  if (scene.template !== "shot") continue;
  const lines = (scene.lines ?? []).map((l) => ({ ...l, wav: path.join(work, "audio", `${l.id}.wav`) }));
  // Each line is trimmed of its own leading/trailing silence and sped up into its own file first:
  // atempo inside the segment graph (before adelay) silently cut every segment's audio to 0.12 s.
  for (const l of lines) {
    const fast = path.join(fastDir, `${l.id}.wav`);
    execFileSync("ffmpeg", ["-v", "error", "-y", "-i", l.wav, "-af", `silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,atempo=${TEMPO}`, "-ar", "48000", "-ac", "2", fast]);
    l.wav = fast;
    l.len = probe(fast);
  }
  let dur = lines.length ? LEAD + lines.reduce((a, l) => a + l.len, 0) + GAP * (lines.length - 1) + TAIL : Math.min(scene.action_seconds ?? scene.data?.action_seconds ?? 2, ACTION_MAX);
  dur = Math.max(dur, MIN, edit.min?.[scene.id] ?? 0);
  const src = scene.data?.source;
  const clip = src ? firstTake(path.join(work, "clips"), src.shot) : pick(path.join(work, "clips"), scene.id);
  const still = pick(path.join(work, "first-frames"), src ? src.shot : scene.id);
  const seg = path.join(segDir, `${scene.id}.mp4`);
  const args = ["-v", "error", "-y"];
  // Where each line sits in the shot, and its subtitle (system lines live on the panel instead).
  let at = LEAD;
  let subs = "";
  const placed = lines.map((l, i) => {
    const p = { ...l, at };
    if (edit.burn_subtitles && !(l.speaker === "xitong" && overlays[scene.id])) subs += subtitle(`${scene.id}-s${i}`, l.text, at, Math.min(dur, at + l.len + 0.08), l.speaker === "xitong" ? "0x9fe3ff" : "0xffffff");
    lineAt.push({ shot: scene.id, speaker: l.speaker, start: t + at, len: l.len });
    srt.push({ start: t + at, end: t + at + l.len, text: l.text });
    at += l.len + GAP;
    return p;
  });
  const decor = `${GRADES[gradeOf(scene.id)]},${FINISH}${panelFilters(scene.id)}${nameCard(scene.id)}${titleCard(scene.id)}${subs}`;
  let vf, note;
  if (clip) {
    const from = src ? Number(src.from_s ?? 0) : 0;
    const clipLen = probe(clip) - from;
    args.push("-ss", from.toFixed(3), "-i", clip);
    const slow = dur > clipLen ? Math.min(dur / clipLen, 1.35) : 1;
    const base = `[0:v]setpts=${slow.toFixed(4)}*(PTS-STARTPTS),scale=1920:1080:flags=lanczos,fps=24,format=yuv420p,tpad=stop_mode=clone:stop_duration=${Math.max(0, dur - clipLen * slow + 0.1).toFixed(3)},trim=duration=${dur.toFixed(3)},setpts=PTS-STARTPTS`;
    const split = edit.split?.[scene.id] ?? (dur > SPLIT && !overlays[scene.id] && edit.nosplit?.includes(scene.id) !== true);
    if (split) {
      // Cut at the start of the second line when there is one, else in the middle; the second part is a punch-in.
      let cut = placed.length > 1 ? placed[1].at - 0.06 : dur * 0.5;
      if (cut < 1.0 || dur - cut < 1.0) cut = dur * 0.5;
      const [ax, ay] = edit.punch?.[scene.id] ?? [0.5, 0.3];
      const w = `iw/${PUNCH}`, h = `ih/${PUNCH}`;
      vf = `${base}[b];[b]split[x][y];[x]trim=duration=${cut.toFixed(3)},setpts=PTS-STARTPTS[p1];[y]trim=start=${cut.toFixed(3)},setpts=PTS-STARTPTS,crop=${w}:${h}:(iw-${w})*${ax}:(ih-${h})*${ay},scale=1920:1080:flags=lanczos,setsar=1[p2];[p1][p2]concat=n=2:v=1:a=0,${decor}[v]`;
      note = `${path.basename(clip)} split@${cut.toFixed(2)}`;
    } else {
      vf = `${base},${decor}[v]`;
      note = path.basename(clip);
    }
    if (dur > clipLen * slow) note += ` held ${(dur - clipLen * slow).toFixed(2)}s`;
  } else {
    if (!still) throw new Error(`${scene.id}: no clip and no first frame`);
    const frames = Math.ceil(dur * 24) + 2;
    args.push("-i", still);
    vf = `[0:v]scale=3840:2160:flags=lanczos,zoompan=${stillMove(scene.id, frames)}:d=${frames}:s=1920x1080:fps=24,format=yuv420p,trim=duration=${dur.toFixed(3)},setpts=PTS-STARTPTS,${decor}[v]`;
    note = `still ${path.basename(still)}`;
  }
  const amix = [];
  placed.forEach((l, i) => {
    args.push("-i", l.wav);
    const ms = Math.round(l.at * 1000);
    amix.push(`[${i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${ms}|${ms}[a${i}]`);
  });
  args.push("-f", "lavfi", "-t", dur.toFixed(3), "-i", "anullsrc=r=48000:cl=stereo");
  const silence = placed.length + 1;
  const graph = [vf, ...amix, `${placed.map((_, i) => `[a${i}]`).join("")}[${silence}:a]amix=inputs=${placed.length + 1}:normalize=0:duration=longest,atrim=duration=${dur.toFixed(3)}[a]`].join(";");
  args.push("-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-c:a", "pcm_s16le", "-t", dur.toFixed(3), seg.replace(/\.mp4$/, ".mkv"));
  execFileSync("ffmpeg", args, { stdio: "inherit" });
  // Guard: the segment's audio must be as long as its picture, or every later line drifts.
  const wavCheck = path.join(fastDir, `_${scene.id}.wav`);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", seg.replace(/\.mp4$/, ".mkv"), "-map", "0:a", wavCheck]);
  const got = probe(wavCheck);
  if (Math.abs(got - dur) > 0.05) throw new Error(`${scene.id}: audio ${got.toFixed(3)} s but shot ${dur.toFixed(3)} s`);
  segs.push(seg.replace(/\.mp4$/, ".mkv"));
  starts[scene.id] = { start: t, dur };
  report.push(`${scene.id} ${t.toFixed(2)} +${dur.toFixed(2)}s ${note}`);
  t += dur;
}
const total = t;

// Picture and dialogue joined.
const list = path.join(segDir, "list.txt");
writeFileSync(list, segs.map((s) => `file '${s.replace(/\\/g, "/")}'`).join("\n") + "\n");
const joined = path.join(segDir, "joined.mkv");
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", joined], { stdio: "inherit" });

// The mix: music cues (ducked under dialogue), effects and beds.
const sfxIndex = {};
for (const dir of edit.sfx_dirs ?? []) {
  const walk = (d) => { for (const n of readdirSync(d, { withFileTypes: true })) { const p = path.join(d, n.name); if (n.isDirectory()) walk(p); else if (/\.(wav|ogg|flac|mp3)$/.test(n.name) && !n.name.startsWith("._")) { const k = n.name.replace(/-48k(?=\.wav$)/, "").replace(/\.(wav|ogg|flac|mp3)$/, ""); if (!sfxIndex[k] || /-48k\.wav$/.test(n.name)) sfxIndex[k] = p; } } };
  walk(dir);
}
const SYNTH = {
  ding: "sine=f=1568:d=1.2[s1];sine=f=2349:d=1.2[s2];[s1][s2]amix=inputs=2,afade=t=out:st=0.05:d=1.1:curve=exp,volume=0.9",
  rain: "anoisesrc=color=pink:amplitude=0.5:d=DUR,highpass=f=700,lowpass=f=9000,volume=0.8",
  underwater: "anoisesrc=color=brown:amplitude=0.6:d=DUR,lowpass=f=320,volume=1.4",
  river: "anoisesrc=color=brown:amplitude=0.4:d=DUR,bandpass=f=900:width_type=o:w=2.5,volume=0.7",
};
const inputs = ["-i", joined];
const parts = [], musicParts = [], sfxParts = [];
let n = 1;
const tAt = (shot, off = 0) => starts[shot].start + off;
const tEnd = (shot) => starts[shot].start + starts[shot].dur;
for (const [i, m] of (edit.music ?? []).entries()) {
  const a = tAt(m.from, m.from_off ?? 0), b = tEnd(m.to) + (m.tail ?? 0);
  const len = Math.min(b, total) - a;
  inputs.push("-i", path.join(work, "music", `cue-${m.cue}.mp3`));
  const ms = Math.round(a * 1000);
  parts.push(`[${n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start=${m.offset ?? 0}:duration=${len.toFixed(3)},asetpts=PTS-STARTPTS,afade=t=in:d=${m.fade_in ?? 0.4},afade=t=out:st=${Math.max(0, len - (m.fade_out ?? 0.8)).toFixed(3)}:d=${m.fade_out ?? 0.8},volume=${m.gain ?? -20}dB,adelay=${ms}|${ms}[m${i}]`);
  musicParts.push(`[m${i}]`);
  n++;
}
// Every system line rings a ding just before it.
const cues = [...(edit.sfx ?? [])];
for (const l of lineAt) if (l.speaker === "xitong") cues.push({ synth: "ding", abs: l.start - 0.22, gain: -9 });
for (const name of Object.keys(edit.names ?? {})) cues.push({ file: edit.name_whoosh ?? "swish-9", at: name, off: 0.15, gain: -16 });
for (const [i, c] of cues.entries()) {
  const a = c.abs ?? tAt(c.at, c.off ?? 0);
  const ms = Math.max(0, Math.round(a * 1000));
  let chain;
  if (c.synth) {
    const len = c.to ? tEnd(c.to) - a : 1.3;
    const def = SYNTH[c.synth].replace(/DUR/g, len.toFixed(3));
    if (c.synth === "ding") chain = `${def.replace("[s1];", `[s1_${i}];`).replace("[s2];", `[s2_${i}];`).replace("[s1][s2]", `[s1_${i}][s2_${i}]`)}`;
    else chain = def;
    chain = `${chain},aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=${c.fade ?? 0.05},afade=t=out:st=${Math.max(0, len - (c.fade ?? 0.3)).toFixed(3)}:d=${c.fade ?? 0.3},volume=${c.gain ?? -12}dB,adelay=${ms}|${ms}[x${i}]`;
    parts.push(chain);
  } else {
    const f = sfxIndex[c.file];
    if (!f) throw new Error(`no sound ${c.file}`);
    inputs.push("-i", f);
    const len = c.to ? tEnd(c.to) - a : null;
    parts.push(`[${n}:a]aresample=48000,aformat=channel_layouts=stereo${len ? `,aloop=loop=-1:size=2e9,atrim=duration=${len.toFixed(3)},afade=t=in:d=0.5,afade=t=out:st=${Math.max(0, len - 0.6).toFixed(3)}:d=0.6` : ""},volume=${c.gain ?? -12}dB,adelay=${ms}|${ms}[x${i}]`);
    n++;
  }
  sfxParts.push(`[x${i}]`);
}
const graph = [
  `[0:a]aresample=48000,asplit=2[dlg][key]`,
  ...parts,
  `${musicParts.join("")}amix=inputs=${musicParts.length}:normalize=0:duration=longest[mus]`,
  `[mus][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350:makeup=1[ducked]`,
  `${sfxParts.join("")}amix=inputs=${sfxParts.length}:normalize=0:duration=longest[fx]`,
  `[dlg][ducked][fx]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]`,
].join(";");
const srtFile = out.replace(/\.mp4$/, ".zh-TW.srt");
const fmt = (s) => { const ms = Math.round(s * 1000); const h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, sec = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")},${String(ms % 1000).padStart(3, "0")}`; };
writeFileSync(srtFile, srt.map((c, i) => `${i + 1}\n${fmt(c.start)} --> ${fmt(c.end)}\n${c.text}\n`).join("\n"));
writeFileSync(path.join(segDir, "mix-graph.txt"), graph);
// Subtitles ride as a soft zh-TW track (CC), the owner's choice; burn_subtitles draws them instead.
const subIn = inputs.filter((x) => x === "-i").length;
execFileSync("ffmpeg", ["-v", "error", "-y", ...inputs, "-i", srtFile, "-filter_complex", graph, "-map", "0:v", "-map", "[mix]", "-map", `${subIn}:s`, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", "-t", total.toFixed(3), "-movflags", "+faststart", out], { stdio: "inherit" });
writeFileSync(path.join(segDir, "report.txt"), report.join("\n") + "\n");
console.log(report.join("\n"));
console.log(`total ${total.toFixed(2)}s -> ${out}`);
