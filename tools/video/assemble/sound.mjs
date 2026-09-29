// The sound a video carries beside its narration (docs/videos/ILLUSTRATED.md, docs/videos/DRAMA.md):
// the music track the script names and the sound-effect set it names, each found and checked
// against its hashes. `assemble` mixes them under the zh-TW narration; `dub` mixes the same bed
// and the cut's effects track under every dubbed narration, so a viewer who switches audio
// tracks hears the same video.
import { existsSync } from "node:fs";
import path from "node:path";

import { sha256File } from "../core/approvals.mjs";
import { mixHash, resolveMusic, resolveSfx } from "../core/drama.mjs";
import { readJson } from "../core/paths.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { requireSfxManifest, sfxDir, sfxSetProblems } from "./sfx.mjs";

/**
 * The music under the voice, when the script names any: the owner's own file under
 * <work base>/_music/ (checked against music.sha256 when given) or the track the music stage
 * generated into the work directory. `{ music, track }`, or `{ problem }`.
 */
export async function musicInputs(doc, workdir, workBase) {
  const music = resolveMusic(doc);
  let track = null;
  if (music?.track) {
    const file = path.join(workBase, "_music", music.track);
    if (!existsSync(file)) return { problem: `music.track ${music.track} is not in ${path.join(workBase, "_music")}` };
    if (music.sha256 && (await sha256File(file)) !== music.sha256) return { problem: `${music.track} does not match music.sha256; check the file or update video.json` };
    track = { file, sha256: music.sha256 ?? (await sha256File(file)) };
  } else if (music) {
    const generated = readJson(path.join(workdir, ARTIFACTS.music), null);
    if (!generated?.file || generated.mix_hash !== mixHash(doc)) return { problem: "music/manifest.json is missing or was made for older music settings; run music first" };
    track = { file: path.join(workdir, generated.file), sha256: generated.sha256 ?? null };
  }
  return { music, track };
}

/**
 * The sound-effect set the script names (docs/videos/ILLUSTRATED.md): its manifest under
 * <work base>/_sfx/<set>/ and every file it names, checked against the hashes it gives.
 * `{ sfx: { gain_db, manifest, files } }` (sfx null when the script names none), or `{ problem }`.
 */
export async function sfxInputs(doc, workBase) {
  const sfx = resolveSfx(doc);
  if (!sfx) return { sfx: null };
  const dir = sfxDir(workBase, sfx.set);
  const manifest = readJson(path.join(dir, "manifest.json"), null);
  if (!manifest) return { problem: `sfx.set ${sfx.set} has no manifest.json in ${dir}: put the licensed sounds there with a manifest (docs/videos/ILLUSTRATED.md)` };
  const problems = sfxSetProblems(manifest);
  if (problems.length) return { problem: `the sound-effect set ${sfx.set} is not usable: ${problems.join("; ")}` };
  const files = {};
  for (const [name, sound] of Object.entries(manifest.sounds)) {
    const file = path.join(dir, sound.file);
    if (!existsSync(file)) return { problem: `sound ${name} of set ${sfx.set} is missing: ${file}` };
    if (sound.sha256 && (await sha256File(file)) !== sound.sha256) return { problem: `${sound.file} does not match its sha256 in the set's manifest` };
    files[name] = file;
  }
  return { sfx: { ...sfx, manifest: requireSfxManifest(manifest), files } };
}
