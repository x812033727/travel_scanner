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
import { FPS } from "../core/timeline.mjs";
import { requireSfxManifest, sfxDir, sfxManifestVersion, sfxSetProblems, sfxSounds } from "./sfx.mjs";

/**
 * The music under the voice, when the script names any: the owner's own file under
 * <work base>/_music/ (checked against music.sha256 when given) or the track the music stage
 * generated into the work directory. `{ music, track }`, or `{ problem }`.
 */
export async function musicInputs(doc, workdir, workBase, { requiredSeconds = null } = {}) {
  const music = resolveMusic(doc);
  let track = null;
  if (music?.track) {
    const file = path.join(workBase, "_music", music.track);
    if (!existsSync(file)) return { problem: `music.track ${music.track} is not in ${path.join(workBase, "_music")}` };
    if (music.sha256 && (await sha256File(file)) !== music.sha256) return { problem: `${music.track} does not match music.sha256; check the file or update video.json` };
    track = { file, sha256: music.sha256 ?? (await sha256File(file)) };
  } else if (music) {
    const generated = readJson(path.join(workdir, ARTIFACTS.music), null);
    if (!generated?.file) return { problem: "music/manifest.json is missing; run music first" };
    if (generated.source === "generated" && generated.duration_hold) {
      return { problem: `generated music decodes to ${Number(generated.actual_seconds).toFixed(3)} s and is on a duration hold; keep the paid file and arrange an explicit checked loop or another licensed track before assemble` };
    }
    if (generated.mix_hash !== mixHash(doc)) return { problem: "music/manifest.json was made for older music settings; run music first" };
    const file = path.join(workdir, generated.file);
    if (!existsSync(file)) return { problem: `generated music file is missing: ${generated.file}; restore the paid artifact or run music to reuse its cached job` };
    if (generated.source === "generated" && !generated.sha256) return { problem: `generated music ${generated.file} has no SHA-256 binding; run music again to verify the retained file` };
    if (generated.sha256 && (await sha256File(file)) !== generated.sha256) return { problem: `generated music ${generated.file} no longer matches its manifest SHA-256; restore the paid artifact` };
    if (generated.source === "generated") {
      if (!(Number.isFinite(generated.actual_seconds) && generated.actual_seconds > 0 && generated.duration_measurement === "ffmpeg_full_decode")) {
        return { problem: "generated music has no fully decoded actual duration; run music again to measure the retained track before assemble" };
      }
      const needed = requiredSeconds ?? (readJson(path.join(workdir, ARTIFACTS.timeline), null)?.total_frames / FPS);
      if (!(Number.isFinite(needed) && needed > 0)) {
        return { problem: "generated music has no current cut length to compare against; run tts or pass the required duration before mixing" };
      }
      if (generated.actual_seconds < needed) {
        return { problem: `generated music decodes to ${generated.actual_seconds.toFixed(3)} s, shorter than the ${needed.toFixed(3)} s cut; keep the paid file and arrange an explicit checked loop or another licensed track before assemble` };
      }
    }
    track = { file, sha256: generated.sha256 ?? null };
  }
  return { music, track };
}

/** The set's manifest file under the work base. */
export const sfxManifestFile = (workBase, set) => path.join(sfxDir(workBase, set), "manifest.json");

/**
 * The sound-effect set the script names (docs/videos/ILLUSTRATED.md §配樂與音效): its manifest
 * under <work base>/_sfx/<set>/ (checked against sfx.sha256 when the script binds it) and every
 * file it names, checked against the hashes it gives; every cue of the script's sheet must name
 * a sound the set holds. `{ sfx: { set, gain_db, cues?, manifest, files, version, sounds,
 * trim_db } }` (sfx null when the script names none), or `{ problem }`. `trim_db` is what the
 * script's gain_db means for this set: a version 1 set's whole-track gain (-12 when unwritten),
 * or a trim on every cue of a version 2 set (0 when unwritten), whose levels come from the
 * manifest's measurements and targets.
 */
export async function sfxInputs(doc, workBase) {
  const sfx = resolveSfx(doc);
  if (!sfx) return { sfx: null };
  const dir = sfxDir(workBase, sfx.set);
  const manifestFile = sfxManifestFile(workBase, sfx.set);
  const manifest = readJson(manifestFile, null);
  if (!manifest) return { problem: `sfx.set ${sfx.set} has no manifest.json in ${dir}: put the licensed sounds there with a manifest (docs/videos/ILLUSTRATED.md)` };
  const problems = sfxSetProblems(manifest);
  if (problems.length) return { problem: `the sound-effect set ${sfx.set} is not usable: ${problems.join("; ")}` };
  if (sfx.sha256 && (await sha256File(manifestFile)) !== sfx.sha256) {
    return { problem: `manifest.json of set ${sfx.set} does not match sfx.sha256: the set changed since the script bound it; check the set, then write its manifest's new hash into video.json` };
  }
  const files = {};
  for (const [name, sound] of Object.entries(manifest.sounds)) {
    const file = path.join(dir, sound.file);
    if (!existsSync(file)) return { problem: `sound ${name} of set ${sfx.set} is missing: ${file}` };
    if (sound.sha256 && (await sha256File(file)) !== sound.sha256) return { problem: `${sound.file} does not match its sha256 in the set's manifest` };
    files[name] = file;
  }
  for (const [index, cue] of (sfx.cues ?? []).entries()) {
    if (!manifest.sounds[cue.sound]) return { problem: `sfx.cues[${index}] names sound "${cue.sound}", which set ${sfx.set} does not hold (it has ${Object.keys(manifest.sounds).join(", ")})` };
  }
  const version = sfxManifestVersion(manifest);
  const trim = version === 2 ? (doc.sfx.gain_db ?? 0) : sfx.gain_db;
  return { sfx: { ...sfx, manifest: requireSfxManifest(manifest), files, version, sounds: sfxSounds(manifest), trim_db: trim } };
}
