// gen-dh.mjs's clip list + first-frame list -> manifests for `h3.sh batch` in MiniMax H3 **reference**
// mode (Ref2VA): no first frame is painted; every shot takes the 3D portraits of the characters in
// it (plus up to two extra-angle face crops per character) and the set picture as <Picture N>, and
// H3 draws the shot itself. 2026-10-28 pilot: this keeps the Hailuo-era faces and the photoreal CG
// skin that Qwen-Image-Edit first frames could not, and 1920x1088 holds the faces through head turns.
//
//   node ref2manifest.mjs <clips-dh-eNNN.json> <ff-dh-eNNN.json> <ep> <out-dir> [--refs DIR] [--take K]
//                         [--only s01,s02] [--seed N] [--chunk 20] [--width 1920] [--height 1088]
//                         [--cast cast.json] [--angles 2]
//
// Pictures, in order: for each character of the shot (the order of ff-dh's refs), the portrait
// (<refs>/<id>-portrait-tK.png, or the modern look) then its angle crops <refs>/angles/<id>-angle-*.png
// (sorted, at most --angles each); the set picture last. Nine pictures at most (H3's limit): angle
// crops are dropped from the last characters first, never a portrait or the set, and each drop is
// printed. The clip prompt is gen-dh's locked text with the first_frame alignment line and the
// `shown in <Picture 1>` anchor rewritten for several pictures, and the cast.json appearance of each
// character pasted verbatim into its anchor clause, before the action (identity text in every shot,
// same wording every time). The prompt goes to <out-dir>/prompts/ref-sNN.txt with its SHA-256 in
// prompt_sha256; output <workdir>/clips/sNN-tK.mp4 (K = --take or the next free take), which
// assemble-v4.mjs's `pick` reads; 20 jobs a manifest (the upstream runner's limit).
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
// gen-dh.mjs's English names (the clip prompts use them) and the women, for the anchor wording.
const EN = { diaoqi: "Diao Qi", baidaifu: "Doctor Bai", zhengbo: "Steward Zheng", tangwanjin: "Tang Wanjin", weijihuoji: "the Wei shop clerk", hanbo: "Elder Han", weishaoqing: "Wei Shaoqing", shimujiang: "Carpenter Shi", sunzhanggui: "Sun Zhanggui", huxianling: "Magistrate Hu", xuyan: "Xu Yan", aling: "A-ling", qinshuang: "Qin Shuang", tangxiaotang: "Tang Xiaotang", xiaohe: "little Xiaohe", erniu: "Wang Erniu", qianyuanwai: "Qian Yuanwai", zhaobutou: "Zhao Butou", mianshiguan: "the interviewer", laisan: "Lai San" };
const HER = new Set(["aling", "qinshuang", "tangxiaotang", "xiaohe", "mianshiguan"]);
const ALIGN_FF = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.";
const ANCHOR_FF = /^(.+?) shown in <Picture 1> keeps? the same face, hair, costume and props as the first frame; the set layout stays as it is\.\s*/;
const ANCHOR_SCENE = "The scene shown in <Picture 1> keeps the first frame's set layout and props.";
const TAIL_FF = "faces, hair and costumes stay as in the first frame.";
const TAIL_REF = "faces, hair and costumes stay as in their reference pictures.";

export function describeRef(name) {
  const base = name.replace(/\.png$/, "").replace(/^dh-/, "");
  if (base.startsWith("set-")) return { kind: "set", id: base.slice(4).replace(/-t\d+$/, ""), file: `${base}.png` };
  const m = base.match(/^(.+?)-(portrait|modern)-t\d+$/);
  return m ? { kind: m[2], id: m[1], file: `${base}.png` } : { kind: "other", id: base, file: `${base}.png` };
}

export function angleCrops(refsDir, id, max) {
  const dir = path.join(refsDir, "angles");
  if (!existsSync(dir) || max <= 0) return [];
  return readdirSync(dir).filter((n) => new RegExp(`^${id}-angle-[a-z0-9]+\\.(png|jpg)$`).test(n)).sort().slice(0, max).map((n) => path.join(dir, n));
}

// The picture list of one shot: [{ id, kind, pictures: [abs paths] }], set last, nine pictures at most.
export function pictureSet(refs, { refsDir, angles = 2, limit = 9 }) {
  const people = [];
  let set = null;
  for (const name of refs) {
    const r = describeRef(name);
    if (r.kind === "set") { set = { id: r.id, kind: "set", pictures: [path.join(refsDir, r.file)] }; continue; }
    if (r.kind === "other") continue;
    people.push({ id: r.id, kind: r.kind, pictures: [path.join(refsDir, r.file), ...(r.kind === "portrait" ? angleCrops(refsDir, r.id, angles) : [])] });
  }
  const dropped = [];
  const count = () => people.reduce((a, p) => a + p.pictures.length, 0) + (set ? 1 : 0);
  for (let i = people.length - 1; count() > limit && i >= 0; i--) {
    while (people[i].pictures.length > 1 && count() > limit) dropped.push(`${people[i].id}: ${path.basename(people[i].pictures.pop())}`);
  }
  return { people, set, dropped };
}

// The shot's composition from gen-dh's first-frame prompt (everything before ", 16:9 frame."): in
// reference mode nothing else tells H3 the framing, who stands where and which props are in hand.
export function composition(ffPrompt) {
  const head = String(ffPrompt ?? "").split(", 16:9 frame.")[0].trim();
  return head ? head.replace(/[.;,]+$/, "") : "";
}

// gen-dh's first_frame prompt -> the reference prompt: pictures named per character, appearance pasted
// in, then the first-frame prompt's composition as the shot's opening state.
export function rewritePrompt(text, { people, set }, cast, ffPrompt) {
  const total = people.reduce((a, p) => a + p.pictures.length, 0) + (set ? 1 : 0);
  const tags = Array.from({ length: total }, (_, i) => `<Picture ${i + 1}>`);
  const list = tags.length > 1 ? `${tags.slice(0, -1).join(", ")} and ${tags[tags.length - 1]}` : tags[0];
  let out = text.replace(ALIGN_FF, `For the target video, ${list} ${tags.length > 1 ? "are" : "is"} referenced throughout.`);
  let n = 0;
  const clauses = [];
  for (const p of people) {
    const mine = p.pictures.map(() => `<Picture ${++n}>`);
    const own = mine.length > 1 ? `${mine.slice(0, -1).join(", ")} and ${mine[mine.length - 1]} (the same ${HER.has(p.id) ? "woman" : "man"} from several angles)` : mine[0];
    const look = cast?.[p.id]?.appearance ? `: ${cast[p.id].appearance}` : "";
    clauses.push(`${EN[p.id] ?? p.id} shown in ${own} keeps exactly the same face, hair and costume as the pictures${look}`);
  }
  if (set) clauses.push(`the location shown in <Picture ${++n}> is the set, keeping its layout and props`);
  const comp = composition(ffPrompt);
  // Reference mode likes to paint the portrait a second time in the background of a close-up:
  // say how many people the frame holds.
  const only = people.length === 1 ? ` ${HER.has(people[0].id) ? "She" : "He"} is the only person in the frame; no second copy of anyone appears.` : people.length > 1 ? ` Only these ${people.length} people are in the frame; no second copy of anyone appears.` : "";
  // The portraits grin; without this the model smiles through a drought (e032 s01, s18).
  const faces = people.length ? " Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood." : "";
  const anchor = `${clauses.join("; ")}.${comp ? ` Initial composition: ${comp}.` : ""}${only}${faces}`;
  const body = out.split("integrated_multimodal_description: [Shot 1] 3D CG. ");
  if (body.length === 2) {
    let rest = body[1];
    if (ANCHOR_FF.test(rest)) rest = rest.replace(ANCHOR_FF, `${anchor} `);
    else if (rest.startsWith(ANCHOR_SCENE)) rest = rest.replace(ANCHOR_SCENE, anchor);
    else rest = `${anchor} ${rest}`;
    out = `${body[0]}integrated_multimodal_description: [Shot 1] 3D CG. ${rest}`;
  }
  return out.replace(TAIL_FF, TAIL_REF);
}

export function nextClipTake(dir, shot) {
  if (!existsSync(dir)) return 1;
  const takes = readdirSync(dir).map((n) => n.match(new RegExp(`^${shot}-t(\\d+)\\.mp4$`))).filter(Boolean).map((m) => Number(m[1]));
  return takes.length ? Math.max(...takes) + 1 : 1;
}

export function build(clips, ff, { ep, refsDir, clipDir, cast, take, only, seed, chunk = 20, width = 1920, height = 1088, angles = 2 }) {
  const byShot = new Map(ff.map((j) => [j.id, j]));
  const jobs = [];
  const notes = [];
  const missing = [];
  for (const [key, [text, , seconds]] of Object.entries(clips)) {
    const m = key.match(/^a(\d+)-(s[0-9a-z]+)$/);
    if (!m || Number(m[1]) !== ep) continue;
    const shot = m[2];
    if (only && !only.has(shot)) continue;
    const entry = byShot.get(shot);
    if (!entry) { missing.push(shot); continue; }
    const pics = pictureSet(entry.refs ?? [], { refsDir, angles });
    for (const d of pics.dropped) notes.push(`${shot}: dropped ${d} (nine pictures at most)`);
    const all = [...pics.people.flatMap((p) => p.pictures), ...(pics.set ? pics.set.pictures : [])];
    const absent = all.filter((p) => !existsSync(p));
    if (absent.length) { missing.push(`${shot} (${absent.map((p) => path.basename(p)).join(", ")})`); continue; }
    if (!all.length) { missing.push(`${shot} (no pictures: a shot with no character and no set)`); continue; }
    const prompt = rewritePrompt(text, pics, cast, entry.prompt);
    const t = take ?? nextClipTake(clipDir, shot);
    const job = {
      id: shot,
      title: `zhong-tian-qu-qi-e${String(ep).padStart(3, "0")} ${shot} ref2va`,
      inference_mode: "reference",
      reference_images: all,
      prompt_file: `prompts/ref-${shot}.txt`,
      prompt_sha256: createHash("sha256").update(prompt).digest("hex"),
      duration_seconds: seconds,
      width,
      height,
      output_path: path.join(clipDir, `${shot}-t${t}.mp4`),
    };
    if (seed != null) job.seed = seed;
    jobs.push({ job, prompt });
  }
  const parts = [];
  for (let i = 0; i < jobs.length; i += chunk) parts.push(jobs.slice(i, i + chunk));
  return { parts, notes, missing };
}

const isMain = process.argv[1] && import.meta.url === `file://${process.argv[1]}`;
if (isMain) {
  const argv = process.argv.slice(2);
  const opts = { refs: null, take: null, only: null, seed: null, chunk: 20, width: 1920, height: 1088, cast: null, angles: 2 };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--refs") opts.refs = argv[++i];
    else if (a === "--take") opts.take = Number(argv[++i]);
    else if (a === "--only") opts.only = new Set(argv[++i].split(",").map((s) => s.trim()).filter(Boolean));
    else if (a === "--seed") opts.seed = Number(argv[++i]);
    else if (a === "--chunk") opts.chunk = Number(argv[++i]);
    else if (a === "--width") opts.width = Number(argv[++i]);
    else if (a === "--height") opts.height = Number(argv[++i]);
    else if (a === "--cast") opts.cast = argv[++i];
    else if (a === "--angles") opts.angles = Number(argv[++i]);
    else positional.push(a);
  }
  const [clipsFile, ffFile, epArg, outDir] = positional;
  if (!clipsFile || !ffFile || !epArg || !outDir) {
    console.error("usage: node ref2manifest.mjs <clips-dh-eNNN.json> <ff-dh-eNNN.json> <ep> <out-dir> [--refs DIR] [--take K] [--only s01,s02] [--seed N] [--chunk 20] [--width 1920] [--height 1088] [--cast cast.json] [--angles 2]");
    process.exit(2);
  }
  const ep = Number(epArg);
  const ep3 = String(ep).padStart(3, "0");
  const VIDEO_WORKDIR = process.env.VIDEO_WORKDIR ?? path.join(os.homedir(), "mokaair-work", "videos");
  const refsDir = path.resolve(opts.refs ?? path.join(VIDEO_WORKDIR, "_series", "zhong-tian-qu-qi", "refs-dh"));
  const clipDir = path.join(VIDEO_WORKDIR, `zhong-tian-qu-qi-e${ep3}-dh`, "clips");
  const castFile = opts.cast ?? path.join(HERE, "..", "cast.json");
  const castJson = JSON.parse(readFileSync(castFile, "utf8"));
  const cast = Object.fromEntries((castJson.characters ?? []).map((c) => [c.id, c]));
  const clips = JSON.parse(readFileSync(clipsFile, "utf8"));
  const ff = JSON.parse(readFileSync(ffFile, "utf8"));
  const { parts, notes, missing } = build(clips, ff, { ep, refsDir, clipDir, cast, take: opts.take, only: opts.only, seed: opts.seed, chunk: opts.chunk, width: opts.width, height: opts.height, angles: opts.angles });
  for (const n of notes) console.log(n);
  if (missing.length) {
    console.error(`no pictures for: ${missing.join("; ")}`);
    process.exit(1);
  }
  mkdirSync(path.join(outDir, "prompts"), { recursive: true });
  const written = [];
  parts.forEach((part, i) => {
    for (const { job, prompt } of part) writeFileSync(path.join(outDir, job.prompt_file), prompt);
    const file = path.join(outDir, `ref-e${ep3}-part${i + 1}.json`);
    writeFileSync(file, `${JSON.stringify({ jobs: part.map((p) => p.job) }, null, 1)}\n`);
    written.push(file);
  });
  const n = parts.reduce((a, p) => a + p.length, 0);
  const secs = parts.flat().map((p) => p.job.duration_seconds);
  const pics = parts.flat().map((p) => p.job.reference_images.length);
  console.log(`${n} reference jobs (${secs.filter((s) => s === 5).length} × 5 s, ${secs.filter((s) => s === 6).length} × 6 s; ${Math.min(...pics)}–${Math.max(...pics)} pictures) at ${opts.width}x${opts.height} -> ${written.length} manifest(s):`);
  for (const f of written) console.log(`  ${f}`);
}
