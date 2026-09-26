// A series' approved character sheets, kept beside the videos' work directories
// (<VIDEO_WORKDIR>/_series/<series>/characters/, docs/videos/SERIES.md), so an episode reuses the
// sheet the owner approved for a character instead of generating and choosing it again. A sheet
// is keyed by everything that goes into drawing it: the character's id, appearance and sheet
// prompt, and the resolved look; change any of them and the character is drawn anew.
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";

import { resolveLook } from "../core/drama.mjs";
import { atomicWrite, readJson } from "../core/paths.mjs";

export const STORE_DIR = "_series";

export function sheetKey(character, look) {
  const digest = createHash("sha256");
  digest.update(JSON.stringify([character.id, character.appearance, character.sheet_prompt ?? null, resolveLook(look)]));
  return digest.digest("hex").slice(0, 16);
}

export function storeDir(workBase, seriesSlug) {
  return path.join(workBase, STORE_DIR, seriesSlug, "characters");
}

/** The store's index: sheet key -> { id, file, sha256, judge, from, at }. */
export function readStore(workBase, seriesSlug) {
  return readJson(path.join(storeDir(workBase, seriesSlug), "index.json"), { sheets: {} });
}

/**
 * The characters whose approved sheet the store holds: each copied into the episode's work
 * directory as its single candidate. Returns { reused: { id: candidate }, missing: [character] }.
 */
export function reuseSheets({ workBase, workdir, seriesSlug, characters, look }) {
  const dir = storeDir(workBase, seriesSlug);
  const index = readStore(workBase, seriesSlug);
  const reused = {};
  const missing = [];
  for (const character of characters) {
    const key = sheetKey(character, look);
    const kept = index.sheets?.[key];
    const source = kept ? path.join(dir, kept.file) : null;
    if (!kept || !source || !existsSync(source)) {
      missing.push(character);
      continue;
    }
    const file = path.join("characters", character.id, `series-${key}.png`);
    mkdirSync(path.dirname(path.join(workdir, file)), { recursive: true });
    copyFileSync(source, path.join(workdir, file));
    reused[character.id] = {
      n: 1,
      seed: 0,
      file,
      sha256: kept.sha256,
      key,
      judge: kept.judge ?? { overall: 10, passed: true, scores: {}, problems: [], notes: "approved earlier for this series" },
      reused_from: kept.from,
    };
  }
  return { reused, missing };
}

/** Keep the sheets the owner chose for a series' characters, so the next episode reuses them. */
export function keepSheets({ workBase, workdir, seriesSlug, doc, manifest, chosen, now = new Date() }) {
  const dir = storeDir(workBase, seriesSlug);
  mkdirSync(dir, { recursive: true });
  const index = readStore(workBase, seriesSlug);
  index.sheets ??= {};
  let kept = 0;
  for (const character of doc.characters ?? []) {
    const entry = manifest.characters?.[character.id];
    const pick = chosen?.[character.id];
    const candidate = entry?.candidates?.find((each) => each.n === pick);
    if (!candidate || !existsSync(path.join(workdir, candidate.file))) continue;
    const key = sheetKey(character, doc.look);
    const file = path.join(character.id, `${key}.png`);
    mkdirSync(path.join(dir, character.id), { recursive: true });
    copyFileSync(path.join(workdir, candidate.file), path.join(dir, file));
    const sha256 = candidate.sha256 ?? createHash("sha256").update(readFileSync(path.join(dir, file))).digest("hex");
    index.sheets[key] = { id: character.id, name: character.name, file, sha256, judge: candidate.judge ?? null, from: doc.slug, at: now.toISOString() };
    kept += 1;
  }
  if (kept) atomicWrite(path.join(dir, "index.json"), `${JSON.stringify(index, null, 2)}\n`);
  return kept;
}
