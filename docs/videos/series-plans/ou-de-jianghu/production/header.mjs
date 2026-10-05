#!/usr/bin/env node
// Build epN/header.json for 《偶的江湖》 episode N from the series-wide cast and the episode meta.
//
//   node header.mjs --ep 2
//
// Inputs:
//   cast.json        { narrator_voice, characters: [ full character objects ] } — the one source of
//                    every character object; an episode copies them verbatim.
//   epN/meta.json    { title, youtube: { title, description, tags }, cast: [ids] }
//   ep1/header.json  the look, music, subtitles, runtime and policy every episode shares.
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const ep = Number(argv[argv.indexOf("--ep") + 1]);
if (!Number.isInteger(ep) || ep < 1) throw new Error("usage: header.mjs --ep N");
const read = (file) => JSON.parse(readFileSync(path.join(HERE, file), "utf8"));
const base = read("ep1/header.base.json");
const cast = read("cast.json");
const meta = read(`ep${ep}/meta.json`);
const byId = new Map(cast.characters.map((character) => [character.id, character]));
const missing = meta.cast.filter((id) => !byId.has(id));
if (missing.length) throw new Error(`ep${ep}/meta.json cast has ids not in cast.json: ${missing.join(", ")}`);
const characters = [...new Set(meta.cast)].sort().map((id) => byId.get(id));
const header = {
  schema_version: 1,
  slug: `ou-de-jianghu-e${String(ep).padStart(3, "0")}`,
  format: "drama",
  category: "anime",
  target_minutes: base.target_minutes,
  production_policy: base.production_policy,
  runtime_spec: base.runtime_spec,
  voice: cast.narrator_voice,
  youtube: { category_id: 1, made_for_kids: false, default_language: "zh-TW", title: meta.youtube.title, description: meta.youtube.description, tags: meta.youtube.tags, video_id: null },
  sources: [],
  look: base.look,
  characters,
  music: base.music,
  subtitles: base.subtitles,
  series: { ...base.series, episode: ep },
};
writeFileSync(path.join(HERE, `ep${ep}`, "header.json"), `${JSON.stringify(header, null, 2)}\n`);
console.log(`ep${ep}/header.json: ${characters.length} characters (${characters.map((c) => c.id).join(", ")})`);
