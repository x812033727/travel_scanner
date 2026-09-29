// Sound effects for an illustrated slides video (docs/videos/ILLUSTRATED.md), as pure functions:
// which licensed sounds a set holds, where the cut's beats fall (a stamp on a chapter card, a
// whoosh into a dissolve, a pop on a reveal), and the ffmpeg arguments that lay them on one
// stereo track as long as the video. The set lives outside the repository, under
// <work base>/_sfx/<set>/, beside a manifest the owner writes: the files, their hashes, where
// they come from and under which licence (the skill's rule 6).
import { createHash } from "node:crypto";

import { resolveSfx } from "../core/drama.mjs";
import { FPS, SAMPLE_RATE } from "../core/timeline.mjs";
import { PlanError } from "./plan.mjs";

// The sounds a set must hold, and what each is for.
export const SFX_SOUNDS = {
  stamp: "a chapter card opens (the stamp lands)",
  whoosh: "a picture dissolves into the next",
  pop: "one more item appears on a card",
};
export const SFX_NAMES = Object.keys(SFX_SOUNDS);
// Two effects never sound within this of each other, and pops are no denser than one per window.
export const MIN_GAP_FRAMES = Math.round(1.5 * FPS);
export const POP_WINDOW_FRAMES = 2 * FPS;
// A whoosh starts this many frames before the dissolve it announces.
export const WHOOSH_LEAD_FRAMES = 5;
const SHA256 = /^[0-9a-f]{64}$/;
const FILE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}\.(?:wav|mp3|m4a|flac|ogg)$/;

/** Everything wrong with a set's manifest, as strings; empty when every sound is named. */
export function sfxSetProblems(manifest) {
  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) return ["manifest.json must hold an object { sounds: { stamp, whoosh, pop } }"];
  const sounds = manifest.sounds;
  if (!sounds || typeof sounds !== "object" || Array.isArray(sounds)) return ["manifest.json needs a sounds object: { stamp: { file }, whoosh: { file }, pop: { file } }"];
  const problems = [];
  for (const name of SFX_NAMES) {
    const sound = sounds[name];
    if (!sound || typeof sound !== "object") {
      problems.push(`sounds.${name} is missing: ${SFX_SOUNDS[name]}`);
      continue;
    }
    if (typeof sound.file !== "string" || !FILE.test(sound.file)) problems.push(`sounds.${name}.file must be a file name in the set's directory (wav, mp3, m4a, flac or ogg)`);
    if (sound.sha256 !== undefined && !(typeof sound.sha256 === "string" && SHA256.test(sound.sha256))) problems.push(`sounds.${name}.sha256 must be 64 hex characters`);
  }
  return problems;
}

/**
 * Where the effects fall on a cut: [{ frame, sound, scene }] in frame order. `layout` is the
 * assembled scenes (with `transition`), `timeline` the synthesized one (its scenes' states say
 * where reveals start), `doc` the script (which scenes open a chapter). Beats too close to the
 * last one are dropped, pops are thinned to one per window, and nothing sounds on frame 0.
 */
export function sfxPlan(layout, timeline, doc) {
  const wanted = [];
  layout.forEach((scene, index) => {
    const source = doc.scenes.find((each) => each.id === scene.id);
    const placed = timeline.scenes.find((each) => each.id === scene.id);
    if (!source || !placed) return;
    // A chapter card is the beat: the stamp lands even when the writer dissolves into it, and no whoosh crowds it.
    const stamp = index > 0 && Boolean(source.chapter);
    if (stamp) wanted.push({ frame: scene.start_frame, sound: "stamp", scene: scene.id });
    if (scene.transition === "dissolve" && !stamp) wanted.push({ frame: Math.max(0, scene.start_frame - WHOOSH_LEAD_FRAMES), sound: "whoosh", scene: scene.id });
    for (const state of placed.states ?? []) {
      if ((state.reveal ?? 0) > 0) wanted.push({ frame: state.start_frame, sound: "pop", scene: scene.id });
    }
  });
  wanted.sort((a, b) => a.frame - b.frame || SFX_NAMES.indexOf(a.sound) - SFX_NAMES.indexOf(b.sound));
  const events = [];
  let last = -Infinity;
  let lastPop = -Infinity;
  for (const event of wanted) {
    if (event.frame <= 0) continue;
    if (event.frame - last < MIN_GAP_FRAMES) continue;
    if (event.sound === "pop" && event.frame - lastPop < POP_WINDOW_FRAMES) continue;
    events.push(event);
    last = event.frame;
    if (event.sound === "pop") lastPop = event.frame;
  }
  return events;
}

/**
 * ffmpeg arguments for the effects track: every sound file opened once, each event delayed to
 * its frame, all mixed without normalizing, gained, then padded and cut to exactly the video's
 * length as 48 kHz stereo PCM. `files` maps a sound name to its path. Null when there is no event.
 */
export function sfxTrackArgs(events, files, totalFrames, gainDb, outFile) {
  if (!events.length) return null;
  const names = [...new Set(events.map((event) => event.sound))];
  const inputs = names.flatMap((name) => ["-i", files[name]]);
  const seconds = (totalFrames / FPS).toFixed(6);
  const graph = [];
  const labels = [];
  events.forEach((event, index) => {
    const ms = Math.round((event.frame * 1000) / FPS);
    graph.push(`[${names.indexOf(event.sound)}:a]aformat=sample_rates=${SAMPLE_RATE}:channel_layouts=stereo,adelay=${ms}|${ms}[e${index}]`);
    labels.push(`[e${index}]`);
  });
  const mixed = labels.length === 1 ? `${labels[0]}acopy[all]` : `${labels.join("")}amix=inputs=${labels.length}:duration=longest:dropout_transition=0:normalize=0[all]`;
  graph.push(mixed);
  graph.push(`[all]volume=${gainDb}dB,apad=whole_dur=${seconds},atrim=0:${seconds},asetpts=PTS-STARTPTS[out]`);
  return ["-hide_banner", "-y", "-loglevel", "error", ...inputs, "-filter_complex", graph.join(";"), "-map", "[out]", "-c:a", "pcm_s16le", "-ar", String(SAMPLE_RATE), "-ac", "2", outFile];
}

/** What a cut's effects were made from: the script's sfx block and the set's file hashes. */
export function sfxSetHash(doc, manifest) {
  const sounds = SFX_NAMES.map((name) => [name, manifest?.sounds?.[name]?.sha256 ?? manifest?.sounds?.[name]?.file ?? null]);
  return createHash("sha256").update(JSON.stringify(["sfx-set", resolveSfx(doc), sounds])).digest("hex").slice(0, 16);
}

/** The set's directory under the work base. */
export const sfxDir = (workBase, set) => `${workBase}/_sfx/${set}`;

export function requireSfxManifest(manifest) {
  const problems = sfxSetProblems(manifest);
  if (problems.length) throw new PlanError(`the sound-effect set is not usable: ${problems.join("; ")}`);
  return manifest;
}
