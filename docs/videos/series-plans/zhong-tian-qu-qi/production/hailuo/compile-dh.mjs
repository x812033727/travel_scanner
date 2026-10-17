// Several 3D donghua episodes as one YouTube video (five per upload, later a whole season):
// each episode is cut again with assemble-v4 without its own title card (the first keeps it,
// subtitled with the range), then joined with one chapter per episode and one merged CC track.
//   node compile-dh.mjs <first> <last> <out.mp4>
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const [first, last, out] = [Number(process.argv[2]), Number(process.argv[3]), path.resolve(process.argv[4])];
const H = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1"));
const R = path.resolve(H, "../../../../../..");
const tmp = path.join(path.dirname(out), path.basename(out, ".mp4") + "-parts");
mkdirSync(tmp, { recursive: true });
const pad = (n) => String(n).padStart(3, "0");
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
  if (!(process.env.REUSE === "1" && existsSync(mp4) && existsSync(mp4.replace(/\.mp4$/, ".zh-TW.srt")))) execFileSync("node", [path.join(H, "assemble-v4.mjs"), path.join(D, "video.json"), path.join(D, "overlays.json"), editFile, W, mp4], { stdio: ["ignore", "ignore", "inherit"] });
  parts.push({ n, mp4, srt: mp4.replace(/\.mp4$/, ".zh-TW.srt"), dur: probe(mp4) });
  console.log(`e${e} ${parts.at(-1).dur.toFixed(2)}s`);
}
// One CC track: every cue shifted by the length of the episodes before it.
const ms = (s) => { const [h, m, r] = s.split(":"); const [sec, milli] = r.split(","); return ((+h * 60 + +m) * 60 + +sec) * 1000 + +milli; };
const fmt = (t) => { const z = (v, w = 2) => String(Math.floor(v)).padStart(w, "0"); return `${z(t / 3600000)}:${z((t / 60000) % 60)}:${z((t / 1000) % 60)},${z(t % 1000, 3)}`; };
const cues = [];
const chapters = [];
let at = 0;
for (const p of parts) {
  chapters.push({ start: at, end: at + p.dur * 1000, title: `第 ${p.n} 集` });
  for (const block of readFileSync(p.srt, "utf8").split(/\r?\n\r?\n/).filter((b) => b.trim())) {
    const [, time, ...text] = block.split(/\r?\n/);
    const [a, b] = time.split(" --> ");
    cues.push(`${fmt(ms(a) + at)} --> ${fmt(ms(b) + at)}\n${text.join("\n")}`);
  }
  at += p.dur * 1000;
}
const srt = out.replace(/\.mp4$/, ".zh-TW.srt");
writeFileSync(srt, cues.map((c, i) => `${i + 1}\n${c}\n`).join("\n"));
const meta = path.join(tmp, "chapters.txt");
writeFileSync(meta, ";FFMETADATA1\n" + chapters.map((c) => `[CHAPTER]\nTIMEBASE=1/1000\nSTART=${Math.round(c.start)}\nEND=${Math.round(c.end)}\ntitle=${c.title}\n`).join(""));
const list = path.join(tmp, "list.txt");
writeFileSync(list, parts.map((p) => `file '${p.mp4.replace(/\\/g, "/")}'`).join("\n"));
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-i", meta, "-i", srt, "-map", "0:v", "-map", "0:a", "-map", "2:s", "-map_metadata", "1", "-map_chapters", "1", "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", "-movflags", "+faststart", out]);
// YouTube description chapters: 0:00 第 1 集 ...
const yt = chapters.map((c) => `${Math.floor(c.start / 60000)}:${String(Math.floor(c.start / 1000) % 60).padStart(2, "0")} ${c.title}`).join("\n");
writeFileSync(out.replace(/\.mp4$/, ".chapters.txt"), yt + "\n");
// Owner 2026-10-17: the title is the series name, the episode range and "| CC字幕".
const eps = parts.map((p) => JSON.parse(readFileSync(path.join(R, `docs/videos/zhong-tian-qu-qi-e${pad(p.n)}/video.json`), "utf8")));
const youtube = {
  ...eps[0].youtube,
  title: `種田娶妻打天下 第${first}–${last}集 | CC字幕`,
  description: [`《種田娶妻打天下》第 ${first}–${last} 集連看，附中文 CC 字幕。`, "", ...eps.map((v, i) => `第 ${parts[i].n} 集：${v.youtube.title.split("｜")[0]}`), "", yt].join("\n"),
  tags: [...new Set(eps.flatMap((v) => v.youtube.tags))],
  video_id: null,
};
writeFileSync(out.replace(/\.mp4$/, ".youtube.json"), JSON.stringify(youtube, null, 1));
console.log(`total ${(at / 1000).toFixed(1)}s -> ${out}\n${yt}`);
