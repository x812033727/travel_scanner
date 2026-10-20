// Several 3D donghua episodes as one YouTube video (five per upload, later a whole season):
// each episode is cut again with assemble-v4 without its own title card (the first keeps it,
// subtitled with the range), then joined with one chapter per episode and one merged CC track.
// DUBS=en,ja,... adds one dub track and one CC file per locale (<out>.<locale>.m4a / .srt), and every
// locale with a youtube-locales/<locale>.json entry for the range goes into .youtube.json's localizations.
// The whole is wrapped in the channel intro and end-screen outro (<VIDEO_WORKDIR>/_branding/current.json,
// or BRANDING=<pin.json>; BRANDING=none leaves them out): CC, chapters, description times and dubs move with it.
//   [DUBS=<locales>] [BRANDING=<pin.json>|none] node compile-dh.mjs <first> <last> <out.mp4>
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmdirSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const [first, last, out] = [Number(process.argv[2]), Number(process.argv[3]), path.resolve(process.argv[4])];
const H = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1"));
const R = path.resolve(H, "../../../../../..");
const tmp = path.join(path.dirname(out), path.basename(out, ".mp4") + "-parts");
mkdirSync(tmp, { recursive: true });
const pad = (n) => String(n).padStart(3, "0");
const V = process.env.VIDEO_WORKDIR ?? path.join(os.homedir(), "mokaair-work", "videos");
// assemble-v4 rewrites an episode's shared segments-v4/lines on every run: take the same
// per-episode lock directory as local/dub.sh while one runs.
const assemble = (W, args, env = process.env) => {
  const lock = path.join(W, ".dub-lock");
  for (let n = 0; ; n++) {
    try { mkdirSync(lock); break; } catch (e) {
      if (e.code !== "EEXIST") throw e;
      if (n > 360) throw new Error(`${lock} held for 30 min (remove it if no dub is running)`);
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 5000);
    }
  }
  try { execFileSync("node", [path.join(H, "assemble-v4.mjs"), ...args], { env, stdio: ["ignore", "ignore", "inherit"] }); } finally { rmdirSync(lock); }
};
const audioLen = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "csv=p=0", f]).toString().trim());
const hasAudio = (f) => execFileSync("ffprobe", ["-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", f]).toString().trim() !== "";
const probe = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString().trim());
const parts = [];
for (let n = first; n <= last; n++) {
  const e = pad(n);
  const edit = JSON.parse(readFileSync(path.join(H, `edit-dh-e${e}.json`), "utf8"));
  if (n === first) edit.title = { ...edit.title, sub: `第 ${first}–${last} 集` };
  else delete edit.title;
  const editFile = path.join(tmp, `edit-e${e}.json`);
  writeFileSync(editFile, JSON.stringify(edit, null, 1));
  const D = path.join(R, `docs/videos/zhong-tian-qu-qi-e${e}`);
  const W = path.join(V, `zhong-tian-qu-qi-e${e}-dh`);
  const mp4 = path.join(tmp, `e${e}.mp4`);
  // REUSE=1 keeps a part already cut (delete the part of an episode that changed).
  if (!(process.env.REUSE === "1" && existsSync(mp4) && existsSync(mp4.replace(/\.mp4$/, ".zh-TW.srt")))) assemble(W, [path.join(D, "video.json"), path.join(D, "overlays.json"), editFile, W, mp4]);
  parts.push({ n, D, W, editFile, mp4, srt: mp4.replace(/\.mp4$/, ".zh-TW.srt"), dur: probe(mp4) });
  console.log(`e${e} ${parts.at(-1).dur.toFixed(2)}s`);
}
// Owner 2026-10-20: the compilation opens on the channel intro and closes on the end-screen outro, the
// same bookends as the pipeline's long videos (docs/videos/BRANDING.md), so the end screen's video
// cards and subscribe button have their 17 s of layout to sit on.
const { validateBranding } = await import(pathToFileURL(path.join(R, "tools/video/core/branding.mjs")).href);
const brandingFile = process.env.BRANDING ?? path.join(V, "_branding", "current.json");
const branding = process.env.BRANDING === "none" ? null : validateBranding(JSON.parse(readFileSync(brandingFile, "utf8")), { base: path.dirname(path.resolve(brandingFile)) });
const intro = branding?.intro.file, outro = branding?.outro.file;
const introMs = intro ? probe(intro) * 1000 : 0;
// The end screen's elements start 17 s before the end (BRANDING.md §結束畫面片尾).
const END_SCREEN_S = 17;

// One CC track: every cue shifted by the intro and the length of the episodes before it.
const ms = (s) => { const [h, m, r] = s.split(":"); const [sec, milli] = r.split(","); return ((+h * 60 + +m) * 60 + +sec) * 1000 + +milli; };
const fmt = (t) => { const z = (v, w = 2) => String(Math.floor(v)).padStart(w, "0"); return `${z(t / 3600000)}:${z((t / 60000) % 60)}:${z((t / 1000) % 60)},${z(t % 1000, 3)}`; };
const joinSrt = (files, to) => {
  const cues = [];
  let at = introMs;
  files.forEach((f, k) => {
    for (const block of readFileSync(f, "utf8").split(/\r?\n\r?\n/).filter((b) => b.trim())) {
      const [, time, ...text] = block.split(/\r?\n/);
      const [a, b] = time.split(" --> ");
      cues.push(`${fmt(ms(a) + at)} --> ${fmt(ms(b) + at)}\n${text.join("\n")}`);
    }
    at += parts[k].dur * 1000;
  });
  writeFileSync(to, cues.map((c, i) => `${i + 1}\n${c}\n`).join("\n"));
};
const srt = out.replace(/\.mp4$/, ".zh-TW.srt");
joinSrt(parts.map((p) => p.srt), srt);
const list = path.join(tmp, "list.txt");
writeFileSync(list, parts.map((p) => `file '${p.mp4.replace(/\\/g, "/")}'`).join("\n"));
const body = intro ? path.join(tmp, "body.mp4") : out;
const bodyMs = parts.reduce((t, p) => t + p.dur * 1000, 0);
let total = bodyMs;
const chapters = [];
const chapterMeta = () => path.join(tmp, "chapters.txt");
const writeChapters = () => {
  // Chapter 1 starts at 0:00 (YouTube wants it) and takes the intro; the last takes the outro.
  chapters.length = 0;
  let at = introMs;
  parts.forEach((p, i) => {
    chapters.push({ start: i ? at : 0, end: i === parts.length - 1 ? total : at + p.dur * 1000, title: `第 ${p.n} 集` });
    at += p.dur * 1000;
  });
  writeFileSync(chapterMeta(), ";FFMETADATA1\n" + chapters.map((c) => `[CHAPTER]\nTIMEBASE=1/1000\nSTART=${Math.round(c.start)}\nEND=${Math.round(c.end)}\ntitle=${c.title}\n`).join(""));
};
writeChapters();
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-i", chapterMeta(), "-i", srt, "-map", "0:v", "-map", "0:a", "-map", "2:s", "-map_metadata", "1", "-map_chapters", "1", "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", "-movflags", "+faststart", body]);
// The bookends are 30 fps; the episodes 24. Everything is encoded once more at the episodes' frame
// rate (the intro and outro lose frames, the animation keeps all of its own).
const fps = execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", parts[0].mp4]).toString().trim();
// [label] of a clip's sound at 48 kHz stereo, or of silence as long as the clip when it has none.
const sound = (i, file, label) => hasAudio(file) ? `[${i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[${label}]` : `anullsrc=r=48000:cl=stereo,atrim=duration=${probe(file).toFixed(3)}[${label}]`;
if (intro) {
  const picture = (i, label) => `[${i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${fps},format=yuv420p[${label}]`;
  const graph = [picture(0, "v0"), sound(0, intro, "a0"), picture(1, "v1"), sound(1, body, "a1"), picture(2, "v2"), sound(2, outro, "a2"), "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]"].join(";");
  total = introMs + probe(body) * 1000 + probe(outro) * 1000;
  writeChapters();
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", intro, "-i", body, "-i", outro, "-i", chapterMeta(), "-i", srt, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-map", "4:s", "-map_metadata", "3", "-map_chapters", "3", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", "-movflags", "+faststart", out]);
  total = probe(out) * 1000;
}
// YouTube description chapters: 0:00 第 1 集 ...
const clock = (t) => `${Math.floor(t / 60000)}:${String(Math.floor(t / 1000) % 60).padStart(2, "0")}`;
const yt = chapters.map((c) => `${clock(c.start)} ${c.title}`).join("\n");
writeFileSync(out.replace(/\.mp4$/, ".chapters.txt"), yt + "\n");
// The links every description ends on: the channel with its subscribe prompt.
const CHANNEL = "https://www.youtube.com/@Mokaair?sub_confirmation=1";
const SUBSCRIBE = {
  "zh-TW": "▶ 訂閱 Mokaair，新集數上架不錯過",
  en: "▶ Subscribe to Mokaair for new episodes",
  ja: "▶ Mokaair をチャンネル登録して新エピソードをチェック",
  ko: "▶ Mokaair 구독하고 새 에피소드 받아보기",
  es: "▶ Suscríbete a Mokaair para ver los nuevos capítulos",
  pt: "▶ Inscreva-se na Mokaair para ver os novos episódios",
  id: "▶ Subscribe Mokaair untuk episode terbaru",
  vi: "▶ Đăng ký kênh Mokaair để xem tập mới",
  th: "▶ กดติดตาม Mokaair เพื่อดูตอนใหม่",
};
const links = (locale) => `${SUBSCRIBE[locale]}\n${CHANNEL}`;
// A translated description's "0:00 Ep. 1" lines take this cut's chapter times, in order.
const retime = (text) => { let k = 0; return text.replace(/^\d+:\d{2}(?=\s)/gm, (t) => (k < chapters.length ? clock(chapters[k++].start) : t)); };
// Owner 2026-10-17: the title is the series name, the episode range and "| CC字幕".
const eps = parts.map((p) => JSON.parse(readFileSync(path.join(R, `docs/videos/zhong-tian-qu-qi-e${pad(p.n)}/video.json`), "utf8")));
const youtube = {
  ...eps[0].youtube,
  title: `種田娶妻打天下 第${first}–${last}集 | CC字幕`,
  description: [`《種田娶妻打天下》第 ${first}–${last} 集連看，附中文 CC 字幕。`, "", ...eps.map((v, i) => `第 ${parts[i].n} 集：${v.youtube.title.split("｜")[0]}`), "", yt, "", links("zh-TW")].join("\n"),
  tags: [...new Set(eps.flatMap((v) => v.youtube.tags))],
  video_id: null,
};
// The end screen is set in Studio, imported from the template video, starting 17 s before the end.
if (outro) youtube.end_screen = { template_video_id: "oxEtlA8GWas", start: clock(total - END_SCREEN_S * 1000), start_seconds: Math.round((total / 1000 - END_SCREEN_S) * 1000) / 1000 };
// Translated titles and descriptions (youtube-locales/<locale>.json, written with the dubs).
const range = `${first}-${last}`;
const localizations = {};
const locDir = path.join(H, "youtube-locales");
for (const f of existsSync(locDir) ? readdirSync(locDir).filter((f) => f.endsWith(".json")).sort() : []) {
  const loc = JSON.parse(readFileSync(path.join(locDir, f), "utf8"));
  const entry = loc.compilation?.[range];
  if (entry) localizations[loc.locale] = { ...entry, description: `${retime(entry.description).trimEnd()}\n\n${links(loc.locale)}` };
}
if (Object.keys(localizations).length) youtube.localizations = localizations;
writeFileSync(out.replace(/\.mp4$/, ".youtube.json"), JSON.stringify(youtube, null, 1));
// The dubs: each part dubbed again on its own compilation timing (assemble-v4 DUB=<locale> with the
// part's edit, so a dropped title card moves the dub exactly as it moved the zh lines), then joined
// between the intro's and the outro's own sound.
for (const locale of (process.env.DUBS ?? "").split(",").map((l) => l.trim()).filter(Boolean)) {
  const tracks = [];
  for (const p of parts) {
    const m4a = p.mp4.replace(/\.mp4$/, `.${locale}.m4a`);
    if (!(process.env.REUSE === "1" && existsSync(m4a) && existsSync(m4a.replace(/\.m4a$/, ".srt")))) assemble(p.W, [path.join(p.D, "video.json"), path.join(p.D, "overlays.json"), p.editFile, p.W, p.mp4], { ...process.env, DUB: locale });
    // A part's picture runs ~0.1 s past its audio; the zh concat starts each part at the end of the
    // previous part's picture, so each dub part is checked against the zh part's audio and padded
    // with silence to the picture.
    const len = probe(m4a), zh = audioLen(p.mp4);
    if (Math.abs(len - zh) > 0.05) throw new Error(`${path.basename(m4a)} is ${len.toFixed(3)} s against ${zh.toFixed(3)} s of zh audio`);
    tracks.push(m4a);
  }
  const track = out.replace(/\.mp4$/, `.${locale}.m4a`);
  const inputs = [...(intro ? [intro] : []), ...tracks, ...(outro ? [outro] : [])];
  const off = intro ? 1 : 0;
  const pads = tracks.map((t, i) => `[${off + i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,apad=whole_dur=${parts[i].dur.toFixed(3)}[p${off + i}]`);
  if (intro) pads.unshift(sound(0, intro, "p0"));
  if (outro) pads.push(sound(inputs.length - 1, outro, `p${inputs.length - 1}`));
  execFileSync("ffmpeg", ["-v", "error", "-y", ...inputs.flatMap((t) => ["-i", t]), "-filter_complex", `${pads.join(";")};${inputs.map((_, i) => `[p${i}]`).join("")}concat=n=${inputs.length}:v=0:a=1[a]`, "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", track]);
  joinSrt(tracks.map((t) => t.replace(/\.m4a$/, ".srt")), out.replace(/\.mp4$/, `.${locale}.srt`));
  const len = probe(track);
  if (Math.abs(len - total / 1000) > 0.3) throw new Error(`${path.basename(track)} is ${len.toFixed(3)} s against ${(total / 1000).toFixed(3)} s of picture`);
  console.log(`${locale}: ${len.toFixed(2)} s against ${(total / 1000).toFixed(2)} s -> ${track}`);
}
console.log(`total ${(total / 1000).toFixed(1)}s -> ${out}\n${yt}`);
if (youtube.end_screen) console.log(`end screen: import from ${youtube.end_screen.template_video_id} in Studio, start ${youtube.end_screen.start}`);
