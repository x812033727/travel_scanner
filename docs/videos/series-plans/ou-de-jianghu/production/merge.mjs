#!/usr/bin/env node
// Merge acts/a01..a05.json with header.json into docs/videos/ou-de-jianghu-e001/video.json and
// series.json. Line ids: an id already assigned in an earlier merge is kept (stored in
// ids.json by scene id and line position + text), every other line gets a fresh id from
// `node tools/video/cli.mjs ids`.
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "..", "..");
const ROOT = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const EP = Number(argv[argv.indexOf("--ep") + 1]);
if (!argv.includes("--ep") || !Number.isInteger(EP) || EP < 1) throw new Error("usage: merge.mjs --ep N [--thumb SHOT] [--headline TEXT]");
const HERE = path.join(ROOT, `ep${EP}`);
const SLUG = `ou-de-jianghu-e${String(EP).padStart(3, "0")}`;
const OUT = path.join(REPO, "docs/videos", SLUG);
const header = JSON.parse(readFileSync(path.join(HERE, "header.json"), "utf8"));
const meta = JSON.parse(readFileSync(path.join(HERE, "meta.json"), "utf8"));
const scenes = [];
for (const act of ["a01", "a02", "a03", "a04", "a05"]) {
  for (const scene of JSON.parse(readFileSync(path.join(HERE, "acts", `${act}.json`), "utf8"))) scenes.push(scene);
}
const seen = new Set();
for (const scene of scenes) {
  if (seen.has(scene.id)) throw new Error(`duplicate scene id ${scene.id}`);
  seen.add(scene.id);
}
// Keep ids across re-merges: key = scene id + text.
const idsFile = path.join(HERE, "ids.json");
const kept = existsSync(idsFile) ? JSON.parse(readFileSync(idsFile, "utf8")) : {};
const used = new Set(Object.values(kept));
const need = [];
for (const scene of scenes)
  for (const [index, line] of (scene.lines ?? []).entries()) {
    const key = `${scene.id}#${index}#${line.text}`;
    if (kept[key]) line.id = kept[key];
    else need.push([key, line]);
  }
if (need.length) {
  let fresh = [];
  while (fresh.length < need.length) {
    const count = Math.min(500, need.length - fresh.length + 20);
    const out = execFileSync("node", [path.join(REPO, "tools/video/cli.mjs"), "ids", "--count", String(count)], { cwd: REPO, encoding: "utf8" });
    for (const id of out.split("\n").map((s) => s.trim()).filter(Boolean)) if (!used.has(id) && !fresh.includes(id)) fresh.push(id);
  }
  for (const [key, line] of need) {
    const id = fresh.shift();
    line.id = id;
    kept[key] = id;
    used.add(id);
  }
}
// Drop keys for lines that no longer exist.
const live = new Set();
for (const scene of scenes) for (const [index, line] of (scene.lines ?? []).entries()) live.add(`${scene.id}#${index}#${line.text}`);
for (const key of Object.keys(kept)) if (!live.has(key)) delete kept[key];
writeFileSync(idsFile, JSON.stringify(kept, null, 2));

// Put `id` first in every line for readability.
for (const scene of scenes) if (Array.isArray(scene.lines)) scene.lines = scene.lines.map(({ id, ...rest }) => ({ id, ...rest }));

const thumbShot = argv.includes("--thumb") ? argv[argv.indexOf("--thumb") + 1] : meta.thumbnail?.shot;
const headline = argv.includes("--headline") ? argv[argv.indexOf("--headline") + 1] : meta.thumbnail?.headline ?? meta.title;
const doc = {
  schema_version: header.schema_version,
  slug: header.slug,
  format: header.format,
  category: header.category,
  target_minutes: header.target_minutes,
  production_policy: header.production_policy,
  runtime_spec: header.runtime_spec,
  voice: header.voice,
  youtube: header.youtube,
  ...(thumbShot ? { thumbnail: { template: "thumb", data: { headline, tag: `第 ${EP} 集`, shot: thumbShot } } } : {}),
  sources: header.sources,
  look: header.look,
  characters: header.characters,
  music: header.music,
  subtitles: header.subtitles,
  series: header.series,
  scenes,
};
mkdirSync(OUT, { recursive: true });
writeFileSync(path.join(OUT, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);

const plan = path.join(REPO, "docs/videos/series-plans/ou-de-jianghu");
const season = JSON.parse(readFileSync(path.join(plan, "season-01.json"), "utf8"));
const setting = JSON.parse(readFileSync(path.join(plan, "setting.json"), "utf8"));
const planJson = JSON.parse(readFileSync(path.join(plan, "plan.json"), "utf8"));
const beats = season.episodes.find((e) => e.number === EP);
const next = season.episodes.find((e) => e.number === EP + 1);
const series = {
  ...header.series,
  title: beats.title,
  logline: beats.logline,
  category: "anime",
  style_preset: "anime-2d",
  target_minutes: header.runtime_spec.body_target_seconds / 60,
  production_policy: header.production_policy,
  runtime_spec: header.runtime_spec,
  characters: header.characters,
  beats,
  recaps: [],
  earlier: season.episodes.filter((e) => e.number < EP).map(({ number, title, logline }) => ({ number, title, logline })),
  next_logline: next?.logline ?? null,
  mysteries: setting.mysteries.filter((m) => (beats.setups ?? []).includes(m.id)),
  series: {
    kind: "series",
    category: "anime",
    production_policy: header.production_policy,
    runtime_spec: header.runtime_spec,
    target_minutes: header.runtime_spec.body_target_seconds / 60,
    planned_episodes: header.series.planned_episodes,
    closed_ending: false,
    title: planJson.title,
    premise: setting.world.premise,
    style_preset: "anime-2d",
    open_ended: true,
    genre: "custom",
    lead: "ensemble",
    visual_tier: "clips",
    compilation: false,
  },
  visual_tier: "clips",
  compilation: false,
};
writeFileSync(path.join(OUT, "series.json"), `${JSON.stringify(series, null, 2)}\n`);
let lines = 0;
for (const scene of scenes) lines += (scene.lines ?? []).length;
console.log(`merged ${scenes.length} scenes, ${lines} lines (${need.length} new ids) into ${OUT}`);
