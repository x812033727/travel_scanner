// One vertical Short an episode (1080×1920, 30 fps), cut from the episode's imported 16:9 final.mp4
// between shorts-dh.json's from/to: the whole picture stays (scaled to 1200 wide, 60 px trimmed off
// each side) over a blurred, darkened fill of itself, with the series title and episode number above,
// the hook line under it, and the channel mark in the Shorts corner (tools/video/core/watermark.mjs).
// The episode's own mix is kept, two-pass loudnorm to -14 LUFS. Captions stay CC (the series rule:
// nothing burned in) — the episode's zh-TW.srt cut to the span, a line the span cuts in half refused.
// Every dub the episode has (dub.<locale>.m4a, <locale>.srt) is cut to the same span, and
// youtube.json carries the title and description in every language. META_ONLY=1 writes only that.
//   [IMPORT=<dir>] [OUT=<dir>] [META_ONLY=1] node shorts-dh.mjs [<episode> ...]
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const H = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1"));
const R = path.resolve(H, "../../../../../..");
const { CURRENT_WATERMARK, WATERMARKS, WATERMARK_DIR } = await import(pathToFileURL(path.join(R, "tools/video/core/watermark.mjs")).href);
const WORK = path.join(os.homedir(), "mokaair-work/videos");
const IMPORT = process.env.IMPORT ?? path.join(WORK, "zhong-tian-qu-qi-import");
const OUT = process.env.OUT ?? path.join(WORK, "zhong-tian-qu-qi-shorts");
const FONT = "/Windows/Fonts/msjhbd.ttc"; // drawtext reads a drive-less path; a "C:" would need escaping
const [W, HT, FPS] = [1080, 1920, 30];
const PIC = { width: 1200, height: 675, y: 600 }; // the 16:9 picture, cropped to W
const pad = (n) => String(n).padStart(3, "0");
const plan = JSON.parse(readFileSync(path.join(H, "shorts-dh.json"), "utf8")).shorts;
const wanted = process.argv.slice(2).map(Number);

const seconds = (t) => { const [h, m, s] = t.split(":"); return Number(h) * 3600 + Number(m) * 60 + Number(s.replace(",", ".")); };
const stamp = (t) => { const ms = Math.round(t * 1000); return `${pad(Math.floor(ms / 3600000)).slice(1)}:${String(Math.floor(ms / 60000) % 60).padStart(2, "0")}:${String(Math.floor(ms / 1000) % 60).padStart(2, "0")},${String(ms % 1000).padStart(3, "0")}`; };
const readSrt = (file) => readFileSync(file, "utf8").replace(/^﻿/, "").trim().split(/\r?\n\r?\n/).map((block) => {
  const lines = block.split(/\r?\n/);
  const [a, b] = lines[1].split(" --> ");
  return { start: seconds(a), end: seconds(b), text: lines.slice(2).join("\n") };
});

// The cues inside [from, to] on the Short's clock; one the span cuts is an error naming it.
function spanCues(cues, from, to) {
  const inside = [];
  for (const cue of cues) {
    if (cue.end <= from || cue.start >= to) continue;
    if (cue.start < from || cue.end > to) throw new Error(`「${cue.text}」 (${cue.start}–${cue.end} s) is cut by the span ${from}–${to}`);
    inside.push({ ...cue, start: cue.start - from, end: cue.end - from });
  }
  return inside;
}

// drawtext reads its words from a file (no escaping); one call a line, so each is centred.
function textLines(dir, name, text, { size, colour, y, gap = 1.3, border = 6 }) {
  return text.split("\n").map((line, i) => {
    const file = `${name}-${i}.txt`;
    writeFileSync(path.join(dir, file), line);
    return `drawtext=fontfile=${FONT}:textfile=${file}:fontsize=${size}:fontcolor=${colour}:borderw=${border}:bordercolor=black@0.85:x=(w-text_w)/2:y=${Math.round(y + i * size * gap)}`;
  });
}

// Two-pass loudnorm to -14 LUFS of the audio of `input` (ffmpeg input arguments), after `pre`.
function loudness(input, pre) {
  const target = "I=-14:TP=-1.5:LRA=11";
  const probe = spawnSync("ffmpeg", ["-hide_banner", "-nostats", ...input, "-vn", "-af", `${pre},loudnorm=${target}:print_format=json`, "-f", "null", "-"], { encoding: "utf8" });
  const m = JSON.parse(probe.stderr.match(/\{[^{}]*"target_offset"[^{}]*\}/)[0]);
  return `${pre},loudnorm=${target}:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true,aresample=48000`;
}
const writeSrt = (file, cues) => writeFileSync(file, cues.map((c, i) => `${i + 1}\n${stamp(c.start)} --> ${stamp(c.end)}\n${c.text}\n`).join("\n"));
const LOCALES = ["en", "ja", "ko", "es", "pt", "id", "vi", "th"];

const mark = WATERMARKS[CURRENT_WATERMARK].shorts;
for (const short of plan.filter((s) => !wanted.length || wanted.includes(s.episode))) {
  const src = path.join(IMPORT, `zhong-tian-qu-qi-e${pad(short.episode)}`);
  const dir = path.join(OUT, `zhong-tian-qu-qi-e${pad(short.episode)}-short`);
  mkdirSync(dir, { recursive: true });
  const length = short.to - short.from;
  if (length < 25 || length > 55) throw new Error(`episode ${short.episode}: ${length.toFixed(2)} s is not a Short (25–55 s, tools/video/shorts/core.mjs PROFILE)`);
  const cues = spanCues(readSrt(path.join(src, "zh-TW.srt")), short.from, short.to);
  writeSrt(path.join(dir, "zh-TW.srt"), cues);
  // Title and description in every language: the episode's own (meta.json, youtube-locales), its
  // "| CC" tail traded for #Shorts, the description pointing at the full episode.
  const episodeMeta = JSON.parse(readFileSync(path.join(src, "meta.json"), "utf8"));
  const youtube = { "zh-TW": { title: `${episodeMeta.title.replace(/\s*\|.*$/, "")} #Shorts`, description: `${short.hook.replace("\n", "，").replace(/[^！？。…]$/, "$&。")}\n完整第 ${short.episode} 集在頻道。\n\n${episodeMeta.description}\n\n#Shorts #種田娶妻打天下 #國漫` } };
  for (const locale of LOCALES) {
    const entry = JSON.parse(readFileSync(path.join(H, "youtube-locales", `${locale}.json`), "utf8")).episodes[String(short.episode)];
    if (entry) youtube[locale] = { title: `${entry.title.replace(/\s*\|.*$/, "")} #Shorts`, description: `${entry.description}\n\n#Shorts` };
  }
  writeFileSync(path.join(dir, "youtube.json"), `${JSON.stringify({ episode: short.episode, from: short.from, to: short.to, localizations: youtube }, null, 2)}\n`);
  // What the site takes: meta.json for tools/video/shorts import (a drama Short pointing back at
  // its episode), and description.<locale>.txt (title, blank line, description) for
  // tools/video/cli.mjs import --languages.
  const slug = `zhong-tian-qu-qi-e${pad(short.episode)}`;
  writeFileSync(path.join(dir, "meta.json"), `${JSON.stringify({
    slug: `${slug}-short`, line: "drama", series: "zhong-tian-qu-qi",
    titles: [youtube["zh-TW"].title, `${short.hook.replace("\n", "，")}｜種田娶妻打天下 #Shorts`],
    description: youtube["zh-TW"].description, source: { slug, start_seconds: short.from, end_seconds: short.to }, synthetic_media: true,
  }, null, 2)}\n`);
  for (const locale of LOCALES) if (youtube[locale]) writeFileSync(path.join(dir, `description.${locale}.txt`), `${youtube[locale].title}\n\n${youtube[locale].description}\n`);
  if (process.env.META_ONLY === "1") continue;

  const words = [
    ...textLines(dir, "title", "種田娶妻打天下", { size: 104, colour: "0xF4C963", y: 250, border: 8 }),
    ...textLines(dir, "episode", `第 ${short.episode} 集`, { size: 60, colour: "white", y: 390 }),
    ...textLines(dir, "hook", short.hook, { size: 72, colour: "white", y: PIC.y + PIC.height + 90 }),
  ];
  const picture = [
    `[0:v]fps=${FPS},setsar=1,split[a][b]`,
    `[a]scale=-2:${HT},crop=${W}:${HT},boxblur=40:3,eq=brightness=-0.22:saturation=0.8[bg]`,
    `[b]scale=${PIC.width}:${PIC.height},crop=${W}:${PIC.height}[fg]`,
    `[bg][fg]overlay=0:${PIC.y},${words.join(",")}[t]`,
    `[t][1:v]overlay=${mark.box.x}:${mark.box.y},format=yuv420p[v]`,
  ].join(";");
  const cut = ["-ss", String(short.from), "-t", length.toFixed(3), "-i", path.join(src, "final.mp4")];
  const fades = `afade=t=in:d=0.08,afade=t=out:st=${(length - 0.35).toFixed(3)}:d=0.35`;
  const sound = loudness(cut, fades);
  const out = path.join(dir, "final.mp4");
  execFileSync("ffmpeg", ["-v", "error", "-y", ...cut, "-i", path.join(WATERMARK_DIR, CURRENT_WATERMARK, mark.file),
    "-filter_complex", `${picture};[0:a]${sound}[s]`, "-map", "[v]", "-map", "[s]", "-t", length.toFixed(3),
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", String(FPS),
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], { cwd: dir, stdio: "inherit" });
  const lufs = spawnSync("ffmpeg", ["-hide_banner", "-nostats", "-i", out, "-af", "ebur128", "-f", "null", "-"], { encoding: "utf8" }).stderr.match(/I:\s+(-?[\d.]+) LUFS\s*\n\s*Threshold[\s\S]*$/)?.[1];
  console.log(`e${pad(short.episode)}: ${length.toFixed(2)} s, ${cues.length} captions, ${lufs} LUFS -> ${out}`);
  // Each dub the episode has: the same span of its full-length track and its CC.
  for (const locale of LOCALES) {
    const dub = path.join(src, `dub.${locale}.m4a`);
    if (!existsSync(dub)) continue;
    // apad: a dub track can end a tenth of a second before the episode picture does.
    const lines = spanCues(readSrt(path.join(src, `${locale}.srt`)), short.from, short.to);
    writeSrt(path.join(dir, `${locale}.srt`), lines);
    const input = ["-ss", String(short.from), "-t", length.toFixed(3), "-i", dub];
    execFileSync("ffmpeg", ["-v", "error", "-y", ...input, "-af", `${loudness(input, fades)},apad`, "-t", length.toFixed(3), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", path.join(dir, `dub.${locale}.m4a`)]);
    console.log(`  ${locale}: ${lines.length} captions`);
  }
}
