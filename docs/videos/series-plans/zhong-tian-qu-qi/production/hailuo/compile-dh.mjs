// Several 3D donghua episodes as one YouTube video (five per upload, later a whole season):
// each episode is cut again with assemble-v4 without its own title card (the first keeps it,
// subtitled with the range), then joined with one chapter per episode and one merged CC track.
// DUBS=en,ja,... adds one dub track and one CC file per locale (<out>.<locale>.m4a / .srt), and every
// locale with a youtube-locales/<locale>.json entry for the range goes into .youtube.json's localizations.
// The channel intro and end-screen outro (<VIDEO_WORKDIR>/_branding/current.json) wrap the whole
// video, the dubs included; BRANDING=0 leaves them out. Every description ends with the links block.
//   [DUBS=<locales>] [BRANDING=0] node compile-dh.mjs <first> <last> <out.mp4>
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmdirSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const [first, last, out] = [Number(process.argv[2]), Number(process.argv[3]), path.resolve(process.argv[4])];
const H = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1"));
const R = path.resolve(H, "../../../../../..");
const tmp = path.join(path.dirname(out), path.basename(out, ".mp4") + "-parts");
mkdirSync(tmp, { recursive: true });
const pad = (n) => String(n).padStart(3, "0");
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
  const W = path.join(process.env.VIDEO_WORKDIR ?? path.join(os.homedir(), "mokaair-work", "videos"), `zhong-tian-qu-qi-e${e}-dh`);
  const mp4 = path.join(tmp, `e${e}.mp4`);
  // REUSE=1 keeps a part already cut (delete the part of an episode that changed).
  if (!(process.env.REUSE === "1" && existsSync(mp4) && existsSync(mp4.replace(/\.mp4$/, ".zh-TW.srt")))) assemble(W, [path.join(D, "video.json"), path.join(D, "overlays.json"), editFile, W, mp4]);
  parts.push({ n, D, W, editFile, mp4, srt: mp4.replace(/\.mp4$/, ".zh-TW.srt"), dur: probe(mp4) });
  console.log(`e${e} ${parts.at(-1).dur.toFixed(2)}s`);
}
// The channel intro and outro, re-encoded like an assemble-v4 segment (24 fps, x264 fast/crf 17,
// the parts' track timescale) so the concat can copy them; the outro's last 17 s leave room for the
// end-screen cards set in Studio.
const VW = process.env.VIDEO_WORKDIR ?? path.join(os.homedir(), "mokaair-work", "videos");
const brand = process.env.BRANDING === "0" ? null : JSON.parse(readFileSync(path.join(VW, "_branding", "current.json"), "utf8"));
const wrap = {};
for (const role of brand ? ["intro", "outro"] : []) {
  const mp4 = path.join(tmp, `${role}.mp4`);
  const m4a = mp4.replace(/\.mp4$/, ".m4a");
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", path.join(VW, "_branding", brand[role].file), "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-video_track_timescale", "16000", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", mp4]);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", mp4, "-vn", "-c:a", "copy", m4a]);
  wrap[role] = { mp4, m4a, dur: probe(mp4) };
}
const lead = wrap.intro?.dur ?? 0;
const tail = wrap.outro?.dur ?? 0;
// One CC track: every cue shifted by the intro and the length of the episodes before it.
const ms = (s) => { const [h, m, r] = s.split(":"); const [sec, milli] = r.split(","); return ((+h * 60 + +m) * 60 + +sec) * 1000 + +milli; };
const fmt = (t) => { const z = (v, w = 2) => String(Math.floor(v)).padStart(w, "0"); return `${z(t / 3600000)}:${z((t / 60000) % 60)}:${z((t / 1000) % 60)},${z(t % 1000, 3)}`; };
const joinSrt = (files, to) => {
  const cues = [];
  let at = lead * 1000;
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
// The intro is too short for a chapter of its own (YouTube wants 10 s): the first episode's chapter
// starts at 0:00 and the last one runs through the outro.
const chapters = [];
let at = lead * 1000;
for (const p of parts) {
  chapters.push({ start: chapters.length ? at : 0, end: at + p.dur * 1000, title: `第 ${p.n} 集` });
  at += p.dur * 1000;
}
chapters.at(-1).end += tail * 1000;
const srt = out.replace(/\.mp4$/, ".zh-TW.srt");
joinSrt(parts.map((p) => p.srt), srt);
const meta = path.join(tmp, "chapters.txt");
writeFileSync(meta, ";FFMETADATA1\n" + chapters.map((c) => `[CHAPTER]\nTIMEBASE=1/1000\nSTART=${Math.round(c.start)}\nEND=${Math.round(c.end)}\ntitle=${c.title}\n`).join(""));
const list = path.join(tmp, "list.txt");
writeFileSync(list, [wrap.intro, ...parts, wrap.outro].filter(Boolean).map((p) => `file '${p.mp4.replace(/\\/g, "/")}'`).join("\n"));
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-i", meta, "-i", srt, "-map", "0:v", "-map", "0:a", "-map", "2:s", "-map_metadata", "1", "-map_chapters", "1", "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", "-movflags", "+faststart", out]);
// YouTube description chapters: 0:00 第 1 集 ...
const stamp = (t) => `${Math.floor(t / 60000)}:${String(Math.floor(t / 1000) % 60).padStart(2, "0")}`;
const yt = chapters.map((c) => `${stamp(c.start)} ${c.title}`).join("\n");
// The links every description carries, between the body and the chapters (publish.md order): the
// channel with its subscribe prompt, and the site's video library in the viewer's language (the site
// has zh-TW, en, ja and ko; the other locales get the English page), tagged for the campaign.
const LINK_LABELS = {
  "zh-TW": ["▶ 訂閱 Mokaair：", "🔗 更多影片："],
  en: ["▶ Subscribe to Mokaair:", "🔗 More videos:"],
  ja: ["▶ Mokaair をチャンネル登録：", "🔗 ほかの動画："],
  ko: ["▶ Mokaair 구독하기:", "🔗 다른 영상:"],
  es: ["▶ Suscríbete a Mokaair:", "🔗 Más videos:"],
  pt: ["▶ Inscreva-se no Mokaair:", "🔗 Mais vídeos:"],
  id: ["▶ Subscribe Mokaair:", "🔗 Video lainnya:"],
  vi: ["▶ Đăng ký kênh Mokaair:", "🔗 Xem thêm video:"],
  th: ["▶ กดติดตาม Mokaair:", "🔗 วิดีโอเพิ่มเติม:"],
};
const campaign = `zhong-tian-qu-qi-e${pad(first)}-${pad(last)}`;
const links = (locale) => {
  const [sub, more] = LINK_LABELS[locale] ?? LINK_LABELS.en;
  const site = ["zh-TW", "ja", "ko"].includes(locale) ? locale : "en";
  return [`${sub} https://www.youtube.com/channel/UCR0rRWT4blMDUwEMx-TZ57Q?sub_confirmation=1`, `${more} https://mokaair.com/${site}/videos?utm_source=youtube&utm_medium=video&utm_campaign=${campaign}`].join("\n");
};
// A translated description written before the intro existed: keep its body and chapter names, put
// the links in and the chapter times on this cut.
const relocalize = (description, locale) => {
  const lines = description.trimEnd().split("\n");
  let k = lines.length;
  while (k > 0 && /^\d+:\d\d(:\d\d)? /.test(lines[k - 1])) k--;
  const names = lines.slice(k).map((l) => l.replace(/^\S+ /, ""));
  if (names.length !== chapters.length) throw new Error(`${locale}: ${names.length} chapter lines for ${chapters.length} chapters`);
  const body = lines.slice(0, k).join("\n").trimEnd().replace(/\n+(▶|🔗)[^\n]*(\n(▶|🔗)[^\n]*)*$/, "");
  return [body, "", links(locale), "", ...chapters.map((c, i) => `${stamp(c.start)} ${names[i]}`)].join("\n");
};
writeFileSync(out.replace(/\.mp4$/, ".chapters.txt"), yt + "\n");
// Owner 2026-10-17: the title is the series name, the episode range and "| CC字幕".
const eps = parts.map((p) => JSON.parse(readFileSync(path.join(R, `docs/videos/zhong-tian-qu-qi-e${pad(p.n)}/video.json`), "utf8")));
const youtube = {
  ...eps[0].youtube,
  title: `種田娶妻打天下 第${first}–${last}集 | CC字幕`,
  description: [`《種田娶妻打天下》第 ${first}–${last} 集連看，附中文 CC 字幕。`, "", ...eps.map((v, i) => `第 ${parts[i].n} 集：${v.youtube.title.split("｜")[0]}`), "", links("zh-TW"), "", yt].join("\n"),
  tags: [...new Set(eps.flatMap((v) => v.youtube.tags))],
  video_id: null,
};
// Translated titles and descriptions (youtube-locales/<locale>.json, written with the dubs).
const range = `${first}-${last}`;
const localizations = {};
const locDir = path.join(H, "youtube-locales");
for (const f of existsSync(locDir) ? readdirSync(locDir).filter((f) => f.endsWith(".json")).sort() : []) {
  const loc = JSON.parse(readFileSync(path.join(locDir, f), "utf8"));
  if (loc.compilation?.[range]) localizations[loc.locale] = { ...loc.compilation[range], description: relocalize(loc.compilation[range].description, loc.locale) };
}
if (Object.keys(localizations).length) youtube.localizations = localizations;
writeFileSync(out.replace(/\.mp4$/, ".youtube.json"), JSON.stringify(youtube, null, 1));
// The dubs: each part dubbed again on its own compilation timing (assemble-v4 DUB=<locale> with the
// part's edit, so a dropped title card moves the dub exactly as it moved the zh lines), then joined.
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
  // The intro's and outro's own sound (no words) go round every language's track, each piece padded
  // to its picture so the track lines up with the video.
  const pieces = [...(wrap.intro ? [{ file: wrap.intro.m4a, dur: wrap.intro.dur }] : []), ...tracks.map((t, i) => ({ file: t, dur: parts[i].dur })), ...(wrap.outro ? [{ file: wrap.outro.m4a, dur: wrap.outro.dur }] : [])];
  const pads = pieces.map((p, i) => `[${i}:a]aresample=48000,apad=whole_dur=${p.dur.toFixed(3)},atrim=0:${p.dur.toFixed(3)}[p${i}]`);
  execFileSync("ffmpeg", ["-v", "error", "-y", ...pieces.flatMap((p) => ["-i", p.file]), "-filter_complex", `${pads.join(";")};${pieces.map((_, i) => `[p${i}]`).join("")}concat=n=${pieces.length}:v=0:a=1[a]`, "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", track]);
  joinSrt(tracks.map((t) => t.replace(/\.m4a$/, ".srt")), out.replace(/\.mp4$/, `.${locale}.srt`));
  console.log(`${locale}: ${probe(track).toFixed(2)} s against ${probe(out).toFixed(2)} s -> ${track}`);
}
console.log(`total ${probe(out).toFixed(1)}s (intro ${lead.toFixed(2)} s, outro ${tail.toFixed(2)} s) -> ${out}\n${yt}`);
