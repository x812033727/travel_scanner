#!/usr/bin/env node
// Check one or more act files of 《偶的江湖》 episode 1 against the repo's own readers.
//
//   node check.mjs --ep N a01            # one act
//   node check.mjs --ep N a01 a02 ... a05 # several, concatenated in order
//   node check.mjs --ep N --all          # the whole episode
//   add --craft for the full craft table, --reading for the full shot_reading output
//
// Act files live in ./epN/acts/<act>.json and are a JSON array of scenes. Lines may omit `id`;
// temporary ids are filled in here (the final ids are assigned at merge).
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "..", "..");
const HERE = path.dirname(fileURLToPath(import.meta.url));
const { validateVideo } = await import(pathToFileURL(path.join(REPO, "tools/video/core/schema.mjs")).href);
const { estimateTimeline, frameToSeconds, spokenUnits } = await import(pathToFileURL(path.join(REPO, "tools/video/core/timeline.mjs")).href);
const { craftChecks, renderCraftReport } = await import(pathToFileURL(path.join(REPO, "tools/video/core/craft.mjs")).href);
const { lintProject, loadProject } = await import(pathToFileURL(path.join(REPO, "tools/video/core/state.mjs")).href);

const raw = process.argv.slice(2);
const epAt = raw.indexOf("--ep");
const EP = Number(raw[epAt + 1]);
if (epAt < 0 || !Number.isInteger(EP) || EP < 1) throw new Error("usage: check.mjs --ep N [a01 ...|--all] [--craft] [--reading]");
const argv = raw.filter((_, i) => i !== epAt && i !== epAt + 1);
const EPDIR = path.join(HERE, `ep${EP}`);
const SLUG = `ou-de-jianghu-e${String(EP).padStart(3, "0")}`;
const flags = new Set(argv.filter((a) => a.startsWith("--")));
let acts = argv.filter((a) => !a.startsWith("--"));
if (flags.has("--all") || !acts.length) acts = ["a01", "a02", "a03", "a04", "a05"];

const header = JSON.parse(readFileSync(path.join(EPDIR, "header.json"), "utf8"));
const scenes = [];
const actOf = new Map();
for (const act of acts) {
  const list = JSON.parse(readFileSync(path.join(EPDIR, "acts", `${act}.json`), "utf8"));
  if (!Array.isArray(list)) throw new Error(`${act}.json must be an array of scenes`);
  for (const scene of list) {
    scenes.push(scene);
    actOf.set(scene.id, act);
  }
}
// Temporary line ids: keep valid given ids, fill the rest.
const taken = new Set();
for (const s of scenes) for (const l of s.lines ?? []) if (typeof l.id === "string" && /^[a-z0-9]{4,8}$/.test(l.id)) taken.add(l.id);
let n = 0;
for (const s of scenes)
  for (const l of s.lines ?? []) {
    if (typeof l.id === "string" && taken.has(l.id) && !l.__seen) {
      l.__seen = true;
      continue;
    }
    let id;
    do id = `t${(n++).toString(36).padStart(4, "0")}`;
    while (taken.has(id));
    taken.add(id);
    l.id = id;
  }
for (const s of scenes) for (const l of s.lines ?? []) delete l.__seen;

const label = acts.length === 5 ? "all" : acts.join("-");
const dir = path.join(EPDIR, `tmp-${label}`, SLUG);
mkdirSync(dir, { recursive: true });
const doc = { ...header, scenes };
const file = path.join(dir, "video.json");
writeFileSync(file, JSON.stringify(doc, null, 2));
writeFileSync(path.join(dir, "brief.md"), "# 測試\n\n## 故事前提\n\n測試。\n\n## 角色\n\n測試。\n\n## 站主觀點\n\n測試。\n");
const series = { ...header.series, category: "anime", style_preset: "anime-2d", target_minutes: 22, production_policy: header.production_policy, runtime_spec: header.runtime_spec, characters: header.characters, visual_tier: "clips", compilation: false };
writeFileSync(path.join(dir, "series.json"), JSON.stringify(series, null, 2));

// 1. Schema errors.
const errors = validateVideo(doc);
console.log(`== ep${EP} ${label}: ${scenes.length} scenes`);
if (errors.length) {
  console.log(`SCHEMA ERRORS (${errors.length}):`);
  for (const e of errors.slice(0, 60)) console.log(`  ${e.path}: ${e.message}`);
}

// 2. Lint (errors and warnings), skipping episode-level noise when checking a single act.
try {
  const report = lintProject(loadProject({ file }));
  const skip = acts.length === 5 ? [] : [/chapters?/, /opening chapter/, /estimated story body/, /minutes; the target/];
  const quiet = [/no sources/];
  const show = (list, tag) => {
    const kept = list.filter((p) => !skip.some((re) => re.test(p.message)) && !quiet.some((re) => re.test(p.message)));
    if (kept.length) console.log(`LINT ${tag} (${kept.length}):`);
    for (const p of kept.slice(0, 80)) console.log(`  ${p.path}: ${p.message}`);
  };
  show(report.errors, "ERRORS");
  show(report.warnings, "WARNINGS");
} catch (error) {
  console.log(`LINT crashed: ${error.message}`);
}

// 3. Estimate per act.
let timeline;
try {
  timeline = estimateTimeline(doc);
} catch (error) {
  console.log(`ESTIMATE failed: ${error.message}`);
}
if (timeline) {
  const perAct = new Map();
  const shotSeconds = [];
  for (const sc of timeline.scenes) {
    const secs = frameToSeconds(sc.end_frame - sc.start_frame);
    const act = actOf.get(sc.id);
    const entry = perAct.get(act) ?? { seconds: 0, shots: 0, cards: 0 };
    entry.seconds += secs;
    if (sc.template === "shot") {
      entry.shots += 1;
      shotSeconds.push([sc.id, secs]);
    } else entry.cards += 1;
    perAct.set(act, entry);
  }
  let chars = 0;
  let lines = 0;
  let narrator = 0;
  let over20 = 0;
  let over40 = 0;
  const lens = [];
  for (const s of scenes)
    for (const l of s.lines ?? []) {
      const units = spokenUnits(l.say ?? l.text);
      chars += units;
      lines += 1;
      lens.push(units);
      if ((l.speaker ?? "narrator") === "narrator") narrator += 1;
      if (units > 20) over20 += 1;
      if (units > 40) over40 += 1;
    }
  lens.sort((a, b) => a - b);
  const secs = shotSeconds.map(([, s]) => s).sort((a, b) => a - b);
  const q = (arr, p) => arr[Math.min(arr.length - 1, Math.floor(p * (arr.length - 1)))];
  console.log("ESTIMATE:");
  for (const [act, e] of perAct) console.log(`  ${act}: ${e.seconds.toFixed(1)} s, ${e.shots} shots, ${e.cards} cards`);
  console.log(`  total ${frameToSeconds(timeline.total_frames).toFixed(1)} s; spoken units ${chars}; lines ${lines}; narrator ${((100 * narrator) / Math.max(1, lines)).toFixed(1)}%`);
  console.log(`  line length median ${q(lens, 0.5)}; >20: ${((100 * over20) / Math.max(1, lines)).toFixed(1)}%; >40: ${over40}`);
  console.log(`  shot seconds median ${q(secs, 0.5)?.toFixed(2)}; p10 ${q(secs, 0.1)?.toFixed(2)}; p90 ${q(secs, 0.9)?.toFixed(2)}; max ${secs.at(-1)?.toFixed(2)}`);
  const long = shotSeconds.filter(([, s]) => s > 8);
  if (long.length) console.log(`  shots over 8 s: ${long.map(([id, s]) => `${id} ${s.toFixed(1)}`).join(", ")}`);
  if (timeline.chapters?.length) console.log(`  chapters: ${timeline.chapters.map((c) => `${c.title}@${frameToSeconds(c.start_frame).toFixed(0)}`).join(" | ")}`);
}

// 4. Craft table (misses only unless --craft).
try {
  const report = craftChecks(doc);
  if (flags.has("--craft")) console.log(renderCraftReport(report, label));
  else {
    const missed = report.checks.filter((c) => !c.ok);
    console.log(`CRAFT: ${report.checks.length - missed.length}/${report.checks.length} met`);
    for (const c of missed) console.log(`  MISS ${c.id ?? c.key ?? c.name ?? c.label}: value ${JSON.stringify(c.value)} target ${JSON.stringify(c.target)}${c.shots ? ` shots ${JSON.stringify(c.shots).slice(0, 300)}` : ""}`);
  }
} catch (error) {
  console.log(`CRAFT failed: ${error.message}`);
}

// 5. Shot reading traps.
try {
  const out = execFileSync("node", [`${REPO}/.agents/skills/animation-camera/scripts/shot_reading.mjs`, file, "--json"], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
  const data = JSON.parse(out);
  const shots = data.shots ?? data;
  const traps = [];
  for (const s of Array.isArray(shots) ? shots : []) for (const t of s.traps ?? []) traps.push(`${s.id}: ${t.message ?? t.trap ?? JSON.stringify(t)}`);
  console.log(`SHOT READING: ${traps.length} traps`);
  for (const t of (flags.has("--reading") ? traps : traps.slice(0, 40))) console.log(`  ${t}`);
} catch (error) {
  console.log(`SHOT READING failed: ${String(error.stdout ?? error.message).slice(0, 2000)}`);
}
