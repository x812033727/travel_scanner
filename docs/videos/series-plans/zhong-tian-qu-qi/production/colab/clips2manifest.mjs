// gen-dh.mjs's clip list (clips-dh-eNNN.json: { "aN-sNN": [prompt, hash16, seconds] }) -> manifests
// for `h3.sh batch` (MiniMax H3 first_frame mode on Colab), 20 jobs each (the upstream runner's limit).
//
//   node clips2manifest.mjs <clips-dh-eNNN.json> <ep> <out-dir> [--first-frames DIR] [--take K]
//                           [--frame-take K] [--only s01,s02] [--seed N] [--skip-missing] [--chunk 20]
//
// Each job: first_frame mode, the shot's latest first frame (<workdir>/first-frames/sNN-tK.png, the
// highest take, or --frame-take), the prompt written to <out-dir>/prompts/clip-sNN.txt byte for byte
// with its full SHA-256 in prompt_sha256 (check_manifest.py refuses a drifted file), the seconds
// gen-dh decided, the 1312x736 canvas, output sNN-tK.mp4 (K = --take, else the next free take in
// <workdir>/clips/), which assemble-v4.mjs's `pick` reads. A shot with no first frame is listed and
// the run stops with 1 unless --skip-missing. Manifests are <out-dir>/clips-eNNN-partN.json.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import os from "node:os";
import path from "node:path";

const argv = process.argv.slice(2);
const opts = { frames: null, take: null, frameTake: null, only: null, seed: null, skipMissing: false, chunk: 20 };
const positional = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "--first-frames") opts.frames = argv[++i];
  else if (a === "--take") opts.take = Number(argv[++i]);
  else if (a === "--frame-take") opts.frameTake = Number(argv[++i]);
  else if (a === "--only") opts.only = new Set(argv[++i].split(",").map((s) => s.trim()).filter(Boolean));
  else if (a === "--seed") opts.seed = Number(argv[++i]);
  else if (a === "--skip-missing") opts.skipMissing = true;
  else if (a === "--chunk") opts.chunk = Number(argv[++i]);
  else positional.push(a);
}
const [file, epArg, outDir] = positional;
const isMain = import.meta.url === `file://${process.argv[1]}`;
if (isMain && (!file || !epArg || !outDir)) {
  console.error("usage: node clips2manifest.mjs <clips-dh-eNNN.json> <ep> <out-dir> [--first-frames DIR] [--take K] [--frame-take K] [--only s01,s02] [--seed N] [--skip-missing] [--chunk 20]");
  process.exit(2);
}
const ep = Number(epArg);
const ep3 = String(ep).padStart(3, "0");
const VIDEO_WORKDIR = process.env.VIDEO_WORKDIR ?? path.join(os.homedir(), "mokaair-work", "videos");
const work = path.join(VIDEO_WORKDIR, `zhong-tian-qu-qi-e${ep3}-dh`);
const frameDir = path.resolve(opts.frames ?? path.join(work, "first-frames"));
const clipDir = path.join(work, "clips");

export function latestFrame(dir, shot, take) {
  if (!existsSync(dir)) return null;
  const hits = readdirSync(dir).filter((n) => new RegExp(`^${shot}-t\\d+\\.(png|jpg)$`).test(n)).sort();
  if (take != null) return hits.find((n) => n.startsWith(`${shot}-t${take}.`)) ? path.join(dir, hits.find((n) => n.startsWith(`${shot}-t${take}.`))) : null;
  return hits.length ? path.join(dir, hits[hits.length - 1]) : null;
}

export function nextClipTake(dir, shot) {
  if (!existsSync(dir)) return 1;
  const takes = readdirSync(dir).map((n) => n.match(new RegExp(`^${shot}-t(\\d+)\\.mp4$`))).filter(Boolean).map((m) => Number(m[1]));
  return takes.length ? Math.max(...takes) + 1 : 1;
}

export function build(clips, { ep, frameDir, clipDir, take, frameTake, only, seed, chunk }) {
  const jobs = [];
  const missing = [];
  for (const [key, [text, , seconds]] of Object.entries(clips)) {
    const m = key.match(/^a(\d+)-(s[0-9a-z]+)$/);
    if (!m) continue;
    if (Number(m[1]) !== ep) continue;
    const shot = m[2];
    if (only && !only.has(shot)) continue;
    const frame = latestFrame(frameDir, shot, frameTake);
    if (!frame) { missing.push(shot); continue; }
    const t = take ?? nextClipTake(clipDir, shot);
    const entry = {
      id: shot,
      title: `zhong-tian-qu-qi-e${String(ep).padStart(3, "0")} ${shot}`,
      inference_mode: "first_frame",
      reference_images: [frame],
      prompt_file: `prompts/clip-${shot}.txt`,
      prompt_sha256: createHash("sha256").update(text).digest("hex"),
      duration_seconds: seconds,
      width: 1312,
      height: 736,
      output_name: `${shot}-t${t}.mp4`,
    };
    if (seed != null && Number.isFinite(seed)) entry.seed = seed;
    jobs.push({ entry, prompt: text });
  }
  const parts = [];
  for (let i = 0; i < jobs.length; i += chunk) parts.push(jobs.slice(i, i + chunk));
  return { jobs, parts, missing };
}

if (isMain) {
  const clips = JSON.parse(readFileSync(file, "utf8"));
  const { jobs, parts, missing } = build(clips, { ep, frameDir, clipDir, take: opts.take, frameTake: opts.frameTake, only: opts.only, seed: opts.seed, chunk: opts.chunk });
  if (missing.length) {
    console.error(`${missing.length} shot(s) have no first frame under ${frameDir}: ${missing.join(", ")}${opts.skipMissing ? " (skipped)" : "\npaint them first (h3.sh images) or pass --skip-missing"}`);
    if (!opts.skipMissing) process.exit(1);
  }
  if (!jobs.length) { console.error("no clip jobs to write"); process.exit(1); }
  mkdirSync(path.join(outDir, "prompts"), { recursive: true });
  for (const { entry, prompt } of jobs) writeFileSync(path.join(outDir, entry.prompt_file), prompt);
  const written = [];
  parts.forEach((part, i) => {
    const manifestPath = path.join(outDir, `clips-e${ep3}-part${i + 1}.json`);
    writeFileSync(manifestPath, JSON.stringify({ episode: `zhong-tian-qu-qi-e${ep3}`, note: "clips for h3.sh batch (MiniMax H3 first_frame, 1312x736); outputs go to <workdir>/clips/ as sNN-tK.mp4", jobs: part.map((j) => j.entry) }, null, 1) + "\n");
    written.push(manifestPath);
  });
  const bySeconds = jobs.reduce((a, j) => ((a[j.entry.duration_seconds] = (a[j.entry.duration_seconds] ?? 0) + 1), a), {});
  console.log(`${jobs.length} clip jobs (${Object.entries(bySeconds).map(([s, n]) => `${n} × ${s} s`).join(", ")}) -> ${written.length} manifest(s):\n  ${written.join("\n  ")}`);
}
