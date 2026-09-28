// The structural numbers COMPARE.md asks for, computed the same way for any batch whose works
// each have a `documents.json` of the pipeline's documents (this batch, and Codex's
// binge-five-20260928, whose files have the same shape). It measures structure, never quality:
// how short the hooks are, how dense the satisfaction beats, how long the viewer waits for a
// thread to pay off, and whether neighbouring episodes end the same way.
//   node compare.mjs [batch-dir …]      (default: this directory)
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const spoken = (text) => [...String(text ?? "").replace(/[\p{P}\p{Z}\s]/gu, "")].length;
const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
const fixed = (x, n = 1) => Number(x).toFixed(n);

/** The numbers for one work, from its setting and chapter documents. */
export function measure(documents) {
  const setting = documents.find((d) => d.kind === "setting")?.body_json ?? {};
  const episodes = documents
    .filter((d) => d.kind === "chapter")
    .sort((a, b) => a.chapter_number - b.chapter_number)
    .flatMap((d) => d.body_json.episodes ?? []);
  const hooks = episodes.map((e) => spoken(e.hook));
  const sats = episodes.map((e) => (Array.isArray(e.satisfaction) ? e.satisfaction.length : 0));
  const types = new Set(episodes.flatMap((e) => (e.satisfaction ?? []).map((b) => b.type)));
  let droughts = 0;
  for (let i = 0; i + 4 <= episodes.length; i++) {
    if (!episodes.slice(i, i + 4).some((e) => Array.isArray(e.payoffs) && e.payoffs.length)) droughts++;
  }
  let sameEnds = 0;
  for (let i = 1; i < episodes.length; i++) if (episodes[i].cliffhanger?.type === episodes[i - 1].cliffhanger?.type) sameEnds++;
  const chapterEnds = episodes.filter((e) => e.number % 10 === 0);
  const turningEnds = chapterEnds.filter((e) => ["reveal", "reversal"].includes(e.cliffhanger?.type)).length;
  const arcs = { wins: 0, mixed: 0, suffers: 0 };
  let run = 0;
  let longestWins = 0;
  for (const e of episodes) {
    arcs[e.lead_arc] = (arcs[e.lead_arc] ?? 0) + 1;
    run = e.lead_arc === "wins" ? run + 1 : 0;
    longestWins = Math.max(longestWins, run);
  }
  const mysteries = Array.isArray(setting.mysteries) ? setting.mysteries : [];
  const paid = new Set(episodes.flatMap((e) => e.payoffs ?? []));
  return {
    episodes: episodes.length,
    hook_mean: mean(hooks),
    hook_max: Math.max(0, ...hooks),
    hooks_le_20: hooks.filter((n) => n <= 20).length,
    sat_mean: mean(sats),
    sat_types: types.size,
    first_sat_early: episodes.filter((e) => ["opening", "first_half"].includes(e.satisfaction?.[0]?.beat)).length,
    payoff_episodes: episodes.filter((e) => (e.payoffs ?? []).length).length,
    droughts,
    same_ends: sameEnds,
    chapter_turns: `${turningEnds}/${chapterEnds.length}`,
    arcs: `${arcs.wins}/${arcs.mixed}/${arcs.suffers}`,
    longest_wins: longestWins,
    tension_end: mean(episodes.map((e) => e.tension?.[4] ?? 0)),
    mysteries: `${mysteries.filter((m) => paid.has(m.id)).length}/${mysteries.length}`,
    cast: Array.isArray(setting.characters) ? setting.characters.length : 0,
  };
}

async function works(batchDir) {
  const found = [];
  for (const entry of (await fs.readdir(batchDir, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
    if (!entry.isDirectory()) continue;
    const file = path.join(batchDir, entry.name, "documents.json");
    try {
      const doc = JSON.parse(await fs.readFile(file, "utf8"));
      const title = JSON.parse(await fs.readFile(path.join(batchDir, entry.name, "manifest.json"), "utf8")).title ?? entry.name;
      found.push({ batch: path.basename(batchDir), slug: entry.name, title, ...measure(doc.documents) });
    } catch {
      // not a work directory (reviews/, a work without built documents)
    }
  }
  return found;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const dirs = process.argv.slice(2).length ? process.argv.slice(2) : [HERE];
  const rows = [];
  for (const dir of dirs) rows.push(...(await works(path.resolve(dir))));
  const heads = ["批次", "作品", "集數", "鉤子平均字", "鉤子最長", "鉤子≤20字", "每集爽點", "爽點種類", "首個爽點在前半", "有回收的集", "四集無回收", "相鄰懸念同型", "篇末揭露或反轉", "贏/混/挨打", "最長連贏", "結尾張力", "謎團回收", "角色數"];
  console.log(`| ${heads.join(" | ")} |`);
  console.log(`| ${heads.map(() => "---").join(" | ")} |`);
  for (const r of rows) {
    console.log(`| ${[r.batch, r.title, r.episodes, fixed(r.hook_mean), r.hook_max, r.hooks_le_20, fixed(r.sat_mean, 2), r.sat_types, r.first_sat_early, r.payoff_episodes, r.droughts, r.same_ends, r.chapter_turns, r.arcs, r.longest_wins, fixed(r.tension_end, 2), r.mysteries, r.cast].join(" | ")} |`);
  }
}
