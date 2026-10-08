// A series' approved character sheets, kept beside the videos' work directories
// (<VIDEO_WORKDIR>/_series/<series>/characters/, docs/videos/SERIES.md), so an episode reuses the
// sheet the owner approved for a character instead of generating and choosing it again. A sheet
// is keyed by everything that goes into drawing it: the character's id, appearance and sheet
// prompt, and the resolved look; change any of them and the character is drawn anew.
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync, realpathSync } from "node:fs";
import path from "node:path";

import { resolveLook } from "../core/drama.mjs";
import { atomicWrite, readJson } from "../core/paths.mjs";

export const STORE_DIR = "_series";
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

/** Imported artwork stays bound to the repository sources checked when it was brought in. */
export function externalSourcesCurrent(provenance, root) {
  if (!root || !Array.isArray(provenance?.source_files) || !provenance.source_files.length) return false;
  try {
    return provenance.source_files.every((entry) => {
      if (typeof entry.path !== "string" || entry.path.includes("\\") || entry.path.includes(":") || path.posix.isAbsolute(entry.path) || entry.path.split("/").some((part) => !part || part === "." || part === "..") || !/^[a-f0-9]{64}$/.test(entry.sha256 ?? "")) return false;
      const file = realpathSync(path.join(root, entry.path));
      const relative = path.relative(realpathSync(root), file);
      return relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative) && sha(readFileSync(file)) === entry.sha256;
    });
  } catch { return false; }
}

function importedReceipt(base, external) {
  if (!external?.source_file || !/^[a-f0-9]{64}$/.test(external.source_sha256 ?? "")) return null;
  const file = path.resolve(base, external.source_file);
  const relative = path.relative(base, file);
  if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) return null;
  try { return sha(readFileSync(file)) === external.source_sha256 ? file : null; }
  catch { return null; }
}

/** A selected/offered external candidate needs real judge evidence and intact bound sources. */
export function externalCandidateProblem(candidate, { workdir, sourceRoot, character, look }) {
  const external = candidate?.external_import;
  if (!external) return null;
  if (candidate.superseded_by) return "external candidate was superseded after a source change; choose the current import";
  if (!candidate.judge) return "external candidate has not been judged; run look import with --judge";
  if (!character || external.character_key !== sheetKey(character, look)) return "external candidate appearance/style changed; import and review the current artwork";
  if (!importedReceipt(workdir, external) || !externalSourcesCurrent(external, sourceRoot)) return "external candidate source SHA-256 changed or its receipt is missing";
  try {
    if (sha(readFileSync(path.join(workdir, candidate.file))) !== candidate.sha256) return "external candidate PNG SHA-256 changed";
  } catch { return "external candidate PNG is missing"; }
  return null;
}

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
export function reuseSheets({ workBase, workdir, seriesSlug, characters, look, image = null, sourceRoot = null }) {
  const dir = storeDir(workBase, seriesSlug);
  const index = readStore(workBase, seriesSlug);
  const reused = {};
  const missing = [];
  for (const character of characters) {
    const key = sheetKey(character, look);
    const kept = index.sheets?.[key];
    const source = kept ? path.join(dir, kept.file) : null;
    const external = kept?.external_import;
    const receipt = external ? importedReceipt(dir, external) : null;
    if (!kept || !source || !existsSync(source)
      || (external && (sha(readFileSync(source)) !== kept.sha256 || !kept.judge || external.character_key !== key || !receipt || !externalSourcesCurrent(external, sourceRoot)))
      || (!external && image && (kept.image?.provider !== image.provider || kept.image?.model !== image.model))) {
      missing.push(character);
      continue;
    }
    const file = path.join("characters", character.id, `series-${key}.png`);
    mkdirSync(path.dirname(path.join(workdir, file)), { recursive: true });
    copyFileSync(source, path.join(workdir, file));
    const sourceFile = `characters/${character.id}/series-${key}.source.json`;
    if (receipt) copyFileSync(receipt, path.join(workdir, sourceFile));
    reused[character.id] = {
      n: 1,
      seed: 0,
      file,
      sha256: kept.sha256,
      key,
      judge: kept.judge ?? { overall: 10, passed: true, scores: {}, problems: [], notes: "approved earlier for this series" },
      reused_from: kept.from,
      ...(kept.image ? { image: kept.image } : {}),
      ...(external ? { external_import: { ...external, source_file: sourceFile } } : {}),
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
    const external = candidate.external_import;
    const receipt = external ? importedReceipt(workdir, external) : null;
    const actualSha256 = sha(readFileSync(path.join(workdir, candidate.file)));
    if (external && (candidate.sha256 !== actualSha256 || !candidate.judge || candidate.superseded_by || external.character_key !== key || !receipt)) continue;
    const sha256 = external ? actualSha256 : candidate.sha256 ?? actualSha256;
    const file = path.join(character.id, `${key}.png`);
    mkdirSync(path.join(dir, character.id), { recursive: true });
    copyFileSync(path.join(workdir, candidate.file), path.join(dir, file));
    const sourceFile = `${character.id}/${key}.source.json`;
    if (receipt) copyFileSync(receipt, path.join(dir, sourceFile));
    const image = candidate.image ?? (!external && !candidate.reused_from && manifest.image_selection_version === 1 ? manifest.image : null);
    index.sheets[key] = { id: character.id, name: character.name, file, sha256, judge: candidate.judge ?? null, from: doc.slug, at: now.toISOString(), ...(image ? { image: { provider: image.provider, model: image.model } } : {}), ...(external ? { external_import: { ...external, source_file: sourceFile } } : {}) };
    kept += 1;
  }
  if (kept) atomicWrite(path.join(dir, "index.json"), `${JSON.stringify(index, null, 2)}\n`);
  return kept;
}
