// gen-dh.mjs's first-frame list (ff-dh-eNNN.json: the Hailuo image page's jobs) -> a manifest for
// `h3.sh images` (Qwen-Image-Edit-2509 on Colab, .agents/skills/minimax-h3-colab/scripts/images.py).
//
//   node ff2manifest.mjs <ff-dh-eNNN.json> <ep> <out-dir> [--refs DIR] [--take K] [--only s01,s02] [--seed N] [--chunk 40]
//
// <out-dir>/ff-eNNN-partN.json, 40 jobs each (images.py's limit; absolute image paths, prompts in <out-dir>/prompts/ff-sNN.txt), outputs
// sNN-tK.png, which is what assemble-v4.mjs's `pick` reads from <workdir>/first-frames/. --refs is
// the 3D portrait and set directory (default <VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/refs-dh, the
// files fetch-dh.sh saved without their `dh-` prefix). --take is the take number (default 1, or the
// next free one when the first-frames dir of this episode already has files for the shot).
//
// Qwen-Image-Edit takes at most three pictures (TextEncodeQwenImageEditPlus image1-image3): the set
// picture always goes in, then the first two portraits in the shot's order; a dropped portrait is
// printed, and that character keeps only the `Characters:` description already in the prompt. The
// Hailuo prompt's "Reference images: ..." sentence is replaced by one line per picture ("image 1 is
// the character sheet of Xu Yan ...") because that is how Qwen-Image-Edit names its inputs.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const argv = process.argv.slice(2);
const opts = { refs: null, take: null, only: null, seed: null, chunk: 40 };
const positional = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "--refs") opts.refs = argv[++i];
  else if (a === "--take") opts.take = Number(argv[++i]);
  else if (a === "--only") opts.only = new Set(argv[++i].split(",").map((s) => s.trim()).filter(Boolean));
  else if (a === "--seed") opts.seed = Number(argv[++i]);
  else if (a === "--chunk") opts.chunk = Number(argv[++i]);
  else positional.push(a);
}
const [file, epArg, outDir] = positional;
const isMain = import.meta.url === `file://${process.argv[1]}`;
if (isMain && (!file || !epArg || !outDir)) {
  console.error("usage: node ff2manifest.mjs <ff-dh-eNNN.json> <ep> <out-dir> [--refs DIR] [--take K] [--only s01,s02] [--seed N] [--chunk 40]");
  process.exit(2);
}
const ep = Number(epArg);
const ep3 = String(ep).padStart(3, "0");
const VIDEO_WORKDIR = process.env.VIDEO_WORKDIR ?? path.join(os.homedir(), "mokaair-work", "videos");
const refsDir = path.resolve(opts.refs ?? path.join(VIDEO_WORKDIR, "_series", "zhong-tian-qu-qi", "refs-dh"));
const frameDir = path.join(VIDEO_WORKDIR, `zhong-tian-qu-qi-e${ep3}-dh`, "first-frames");

// Same table as gen-dh.mjs's EN map; the portrait file is dh-<id>-portrait-tK.
const EN = { zhengbo: "Steward Zheng", tangwanjin: "Tang Wanjin", weijihuoji: "the Wei shop clerk", hanbo: "Elder Han", weishaoqing: "Wei Shaoqing", shimujiang: "Carpenter Shi", sunzhanggui: "Sun Zhanggui", huxianling: "Magistrate Hu", xuyan: "Xu Yan", aling: "A-ling", qinshuang: "Qin Shuang", tangxiaotang: "Tang Xiaotang", xiaohe: "little Xiaohe", erniu: "Wang Erniu", qianyuanwai: "Qian Yuanwai", zhaobutou: "Zhao Butou", mianshiguan: "the interviewer", laisan: "Lai San" };
const HER = new Set(["aling", "qinshuang", "tangxiaotang", "xiaohe"]);

export function describeRef(name) {
  // "dh-xuyan-portrait-t1.png" -> { file: "xuyan-portrait-t1.png", kind: "portrait", id: "xuyan" }
  const stem = name.replace(/^dh-/, "").replace(/\.png$/i, "");
  if (/^set-/.test(stem)) return { file: `${stem}.png`, kind: "set", id: stem.replace(/^set-/, "").replace(/-t\d+$/, "") };
  const m = stem.match(/^(.+?)-(portrait|modern)-t\d+$/);
  if (m) return { file: `${stem}.png`, kind: m[2], id: m[1] };
  return { file: `${stem}.png`, kind: "other", id: stem };
}

export function pickRefs(refs) {
  // At most three: the set last, portraits first in the shot's order; the rest are dropped and named.
  const described = refs.map(describeRef);
  const set = described.filter((r) => r.kind === "set").slice(0, 1);
  const people = described.filter((r) => r.kind !== "set");
  const room = 3 - set.length;
  return { kept: [...people.slice(0, room), ...set], dropped: people.slice(room) };
}

export function rewritePrompt(prompt, kept) {
  const lines = kept.map((r, i) => {
    const n = i + 1;
    if (r.kind === "set") return `image ${n} is the location: keep its layout, architecture, props, lighting and the same 3D donghua art style`;
    const who = EN[r.id] ?? r.id;
    const pronoun = HER.has(r.id) ? "her" : "his";
    return `image ${n} is the character sheet of ${who}: keep ${pronoun} face, hair, costume and the same 3D donghua art style exactly${r.kind === "modern" ? " (modern clothes)" : ""}`;
  });
  const mapping = lines.length ? ` Reference images: ${lines.join("; ")}.` : "";
  // Drop Hailuo's own "Reference images: ..." sentence (it ends before " Not a photograph").
  const stripped = prompt.replace(/ Reference images: [^]*?(?= Not a photograph)/, "");
  return stripped.replace(/ Not a photograph/, `${mapping} Not a photograph`);
}

export function nextTake(dir, shot) {
  if (!existsSync(dir)) return 1;
  const takes = readdirSync(dir).map((n) => n.match(new RegExp(`^${shot}-t(\\d+)\\.(png|jpg)$`))).filter(Boolean).map((m) => Number(m[1]));
  return takes.length ? Math.max(...takes) + 1 : 1;
}

export function build(ff, { ep, refsDir, frameDir, take, only, seed, chunk = 40 }) {
  const jobs = [];
  const notes = [];
  const missing = new Set();
  for (const job of ff) {
    if (only && !only.has(job.id)) continue;
    const { kept, dropped } = pickRefs(job.refs ?? []);
    if (dropped.length) notes.push(`${job.id}: dropped ${dropped.map((r) => r.file).join(", ")} (Qwen-Image-Edit takes three pictures; the text description still carries them)`);
    const images = kept.map((r) => path.join(refsDir, r.file));
    for (const image of images) if (!existsSync(image)) missing.add(image);
    const t = take ?? nextTake(frameDir, job.id);
    const entry = {
      id: job.id,
      title: `zhong-tian-qu-qi-e${String(ep).padStart(3, "0")} ${job.id} first frame`,
      reference_images: images,
      prompt_file: `prompts/ff-${job.id}.txt`,
      width: 1312,
      height: 736,
      output_name: `${job.id}-t${t}.png`,
    };
    if (seed != null && Number.isFinite(seed)) entry.seed = seed;
    jobs.push({ entry, prompt: rewritePrompt(job.prompt, kept) });
  }
  const parts = [];
  for (let i = 0; i < jobs.length; i += chunk) parts.push(jobs.slice(i, i + chunk));
  return { jobs, parts, notes, missing: [...missing] };
}

if (isMain) {
  const ff = JSON.parse(readFileSync(file, "utf8"));
  const { jobs, parts, notes, missing } = build(ff, { ep, refsDir, frameDir, take: opts.take, only: opts.only, seed: opts.seed, chunk: opts.chunk });
  if (!jobs.length) { console.error("no first-frame jobs matched"); process.exit(1); }
  mkdirSync(path.join(outDir, "prompts"), { recursive: true });
  for (const { entry, prompt } of jobs) writeFileSync(path.join(outDir, entry.prompt_file), prompt);
  const written = [];
  parts.forEach((part, i) => {
    const manifestPath = path.join(outDir, `ff-e${ep3}-part${i + 1}.json`);
    writeFileSync(manifestPath, JSON.stringify({ episode: `zhong-tian-qu-qi-e${ep3}`, note: "first frames for h3.sh images (Qwen-Image-Edit-2509, 1312x736); outputs go to <workdir>/first-frames/ as sNN-tK.png", jobs: part.map((j) => j.entry) }, null, 1) + "\n");
    written.push(manifestPath);
  });
  for (const n of notes) console.log(n);
  console.log(`${jobs.length} first-frame jobs -> ${written.length} manifest(s):\n  ${written.join("\n  ")}\noutputs ${jobs.map((j) => j.entry.output_name).slice(0, 3).join(", ")}${jobs.length > 3 ? ", …" : ""}`);
  if (missing.length) {
    console.error(`${missing.length} reference picture(s) missing under ${refsDir}:\n  ${missing.join("\n  ")}\nfetch them with fetch-dh.sh (dh-* labels) before running h3.sh images`);
    process.exit(1);
  }
}
