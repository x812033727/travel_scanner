// Sound effects for an illustrated slides video (docs/videos/ILLUSTRATED.md §配樂與音效), as pure
// functions: which licensed sounds a set holds and how loud each file is, where the cut's beats
// fall (a stamp on a chapter card, a whoosh into a dissolve, a pop on a reveal) and where the
// script's own cue sheet puts more, the gain that brings each cue to its sound's target
// loudness, the ffmpeg arguments that lay them on one stereo track as long as the video, and the
// measurement that proves every cue is heard over the bed and clips nothing. The set lives
// outside the repository, under <work base>/_sfx/<set>/, beside a manifest the owner writes: the
// files, their hashes, where they come from and under which licence (the skill's rule 6). A
// version 2 manifest also carries each file's measured loudness (`assemble sfx-measure`), which
// is what lets a cue be placed at a level instead of at one gain for the whole track.
import { createHash } from "node:crypto";

import { resolveSfx, SFX_SOUND_NAME } from "../core/drama.mjs";
import { FPS, SAMPLE_RATE } from "../core/timeline.mjs";
import { bedFilter, DUCK_ATTACK_MS, DUCK_RELEASE_MS, DUCK_THRESHOLD, duckRatio, soundGraph } from "./drama.mjs";
import { LOUDNESS, parseEbur128, PlanError } from "./plan.mjs";

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
// A version 1 manifest names files and places them at the script's one gain_db; version 2 adds
// each file's measured loudness and places every cue at its sound's target.
export const SFX_MANIFEST_VERSIONS = [1, 2];
// Where a sound's loudest 400 ms sits in the finished mix (a -14 LUFS programme), by name: the
// stamp as loud as the voice, in the pause a chapter card opens on; the others a little under it.
export const SFX_TARGET_LUFS = { stamp: -14, whoosh: -16, pop: -16 };
export const SFX_DEFAULT_TARGET_LUFS = -16;
// A cue's gain never lifts its sound's true peak above this in the finished mix, whatever the target.
export const SFX_PEAK_CEILING_DBTP = -3;
// A cue is heard when its loudest momentary window sits at least this far above the music bed under it.
export const SFX_ABOVE_BED_DB = 6;
// EBU R128 momentary loudness is a 400 ms window, which ebur128 reports every 100 ms.
export const MOMENTARY_SECONDS = 0.4;
// A file is measured with this much silence after it, so a sound shorter than one window still
// fills one (ebur128 reports no loudness at all for a 250 ms file on its own).
export const SFX_MEASURE_PAD_SECONDS = 1;
const SHA256 = /^[0-9a-f]{64}$/;
const FILE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}\.(?:wav|mp3|m4a|flac|ogg)$/;
const STEREO = "pan=stereo|c0=c0|c1=c0";
const EBUR128 = "ebur128=peak=true";

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const inRange = (value, low, high) => typeof value === "number" && Number.isFinite(value) && value >= low && value <= high;
const tenth = (value) => (Number.isFinite(value) ? Number(value.toFixed(1)) : null);

/** The manifest's version: 1 when it names none. */
export const sfxManifestVersion = (manifest) => manifest?.manifest_version ?? 1;

/** Where a sound's loudest window should sit in the finished mix: the manifest's word, else the name's default. */
export function sfxTargetLufs(name, sound = null) {
  return sound?.target_lufs ?? SFX_TARGET_LUFS[name] ?? SFX_DEFAULT_TARGET_LUFS;
}

/**
 * Everything wrong with a set's manifest, as strings; empty when every sound is named. A version
 * 2 manifest must carry each sound's measurement unless `measured` is false (the measuring step
 * reads a manifest that is about to get them).
 */
export function sfxSetProblems(manifest, { measured = true } = {}) {
  if (!isObject(manifest)) return ["manifest.json must hold an object { sounds: { stamp, whoosh, pop } }"];
  const version = manifest.manifest_version;
  if (version !== undefined && !SFX_MANIFEST_VERSIONS.includes(version)) return [`manifest_version must be ${SFX_MANIFEST_VERSIONS.join(" or ")}`];
  const sounds = manifest.sounds;
  if (!isObject(sounds)) return ["manifest.json needs a sounds object: { stamp: { file }, whoosh: { file }, pop: { file } }"];
  const problems = [];
  for (const name of SFX_NAMES) {
    if (!isObject(sounds[name])) problems.push(`sounds.${name} is missing: ${SFX_SOUNDS[name]}`);
  }
  for (const [name, sound] of Object.entries(sounds)) {
    if (!SFX_SOUND_NAME.test(name)) {
      problems.push(`sounds.${name}: a sound's name is lowercase letters, digits, _ or -, up to 32 characters`);
      continue;
    }
    if (!isObject(sound)) {
      if (!SFX_NAMES.includes(name)) problems.push(`sounds.${name} must be an object { file, sha256?, ... }`);
      continue;
    }
    if (typeof sound.file !== "string" || !FILE.test(sound.file)) problems.push(`sounds.${name}.file must be a file name in the set's directory (wav, mp3, m4a, flac or ogg)`);
    if (sound.sha256 !== undefined && !(typeof sound.sha256 === "string" && SHA256.test(sound.sha256))) problems.push(`sounds.${name}.sha256 must be 64 hex characters`);
    if (sound.target_lufs !== undefined && !inRange(sound.target_lufs, -40, -6)) problems.push(`sounds.${name}.target_lufs must be -40 to -6 LUFS`);
    if (sound.seconds !== undefined && !(inRange(sound.seconds, 0, 60) && sound.seconds > 0)) problems.push(`sounds.${name}.seconds must be the file's length in seconds, up to 60`);
    if (version !== 2) continue;
    for (const [key, low, high] of [["lufs_i", -70, 0], ["lufs_m", -70, 0], ["peak_dbtp", -70, 6]]) {
      if (sound[key] === undefined) {
        if (measured && key !== "lufs_m") problems.push(`sounds.${name}.${key} is not measured; run node tools/video/cli.mjs assemble sfx-measure --set <set>`);
      } else if (!inRange(sound[key], low, high)) {
        problems.push(`sounds.${name}.${key} must be a number, ${low} to ${high}`);
      }
    }
  }
  return problems;
}

/**
 * The set's sounds as the assembly uses them: file, hash, the measured loudness (null in a
 * version 1 set), the file's length when known and the target each cue is gained toward.
 */
export function sfxSounds(manifest) {
  const measured = sfxManifestVersion(manifest) === 2;
  return Object.fromEntries(Object.entries(manifest.sounds).map(([name, sound]) => [name, {
    file: sound.file,
    sha256: sound.sha256 ?? null,
    lufs_i: measured ? sound.lufs_i : null,
    lufs_m: measured ? (sound.lufs_m ?? sound.lufs_i) : null,
    peak_dbtp: measured ? sound.peak_dbtp : null,
    seconds: sound.seconds ?? null,
    target_lufs: sfxTargetLufs(name, sound),
  }]));
}

/**
 * The script's own cues (video.json sfx.cues) on the timeline: a scene cue sounds as that scene
 * opens, a frame cue on that very frame. [{ frame, sound, scene, cue, gain_db? }] in sheet order;
 * a frame past the video is a PlanError, as is a scene the timeline does not have.
 */
export function sfxCues(doc, timeline) {
  const cues = resolveSfx(doc)?.cues ?? [];
  return cues.map((cue, index) => {
    let frame;
    let scene;
    if (cue.scene !== undefined) {
      const placed = timeline.scenes.find((each) => each.id === cue.scene);
      if (!placed) throw new PlanError(`sfx.cues[${index}] names scene ${cue.scene}, which the timeline does not have; run tts again`);
      frame = placed.start_frame;
      scene = cue.scene;
    } else {
      frame = cue.frame;
      if (frame >= timeline.total_frames) throw new PlanError(`sfx.cues[${index}] is at frame ${frame}, past the video's ${timeline.total_frames} frames`);
      scene = timeline.scenes.find((each) => frame >= each.start_frame && frame < each.end_frame)?.id ?? null;
    }
    return { frame, sound: cue.sound, scene, cue: index, ...(cue.gain_db !== undefined ? { gain_db: cue.gain_db } : {}) };
  });
}

/**
 * Where the effects fall on a cut: [{ frame, sound, scene }] in frame order. `layout` is the
 * assembled scenes (with `transition`), `timeline` the synthesized one (its scenes' states say
 * where reveals start), `doc` the script (which scenes open a chapter, and its cue sheet). Beats
 * too close to the last one are dropped, pops are thinned to one per window, and nothing sounds
 * on frame 0. The script's own cues are laid on top: each sounds where the writer put it, and a
 * rule's beat within the minimum gap of one gives way to it.
 */
export function sfxPlan(layout, timeline, doc) {
  const cues = sfxCues(doc, timeline);
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
    if (cues.some((cue) => Math.abs(cue.frame - event.frame) < MIN_GAP_FRAMES)) continue;
    if (event.frame - last < MIN_GAP_FRAMES) continue;
    if (event.sound === "pop" && event.frame - lastPop < POP_WINDOW_FRAMES) continue;
    events.push(event);
    last = event.frame;
    if (event.sound === "pop") lastPop = event.frame;
  }
  return [...events, ...cues].sort((a, b) => a.frame - b.frame || (a.cue ?? -1) - (b.cue ?? -1));
}

/**
 * Each event with the gain that puts its sound at its target in the finished mix. `sfx` is what
 * sound.mjs found (version, sounds, trim_db); `gainToTarget` is what the final normalization
 * will add to the whole mix, so a target in the finished mix becomes a level on the track. The
 * gain is capped where the sound's true peak would pass the ceiling (`capped: true`). A version 1
 * set has no measurements: its events keep only a cue's own gain_db, over the track's gain.
 */
export function sfxGains(events, sfx, gainToTarget) {
  const trim = sfx.trim_db ?? 0;
  return events.map((event) => {
    const offset = event.gain_db ?? 0;
    if (sfx.version !== 2) return event.gain_db === undefined ? event : { ...event, gain_db: tenth(offset) };
    const sound = sfx.sounds[event.sound];
    const wanted = sound.target_lufs - gainToTarget - sound.lufs_m + offset + trim;
    const ceiling = SFX_PEAK_CEILING_DBTP - gainToTarget - sound.peak_dbtp;
    const capped = wanted > ceiling;
    return { ...event, gain_db: tenth(capped ? ceiling : wanted), target_lufs: sound.target_lufs, ...(capped ? { capped: true } : {}) };
  });
}

/** The gain of the whole effects track: a version 1 set's gain_db; a version 2 set's gains are on each cue. */
export const sfxTrackGainDb = (sfx) => (sfx.version === 2 ? 0 : sfx.gain_db);

/**
 * ffmpeg arguments for the effects track: every sound file opened once, each event delayed to
 * its frame (and gained by its own gain_db when it carries one), all mixed without normalizing,
 * gained, then padded and cut to exactly the video's length as 48 kHz stereo PCM. `files` maps a
 * sound name to its path. Null when there is no event.
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
    const gain = Number.isFinite(event.gain_db) ? `volume=${event.gain_db}dB,` : "";
    graph.push(`[${names.indexOf(event.sound)}:a]aformat=sample_rates=${SAMPLE_RATE}:channel_layouts=stereo,${gain}adelay=${ms}|${ms}[e${index}]`);
    labels.push(`[e${index}]`);
  });
  const mixed = labels.length === 1 ? `${labels[0]}acopy[all]` : `${labels.join("")}amix=inputs=${labels.length}:duration=longest:dropout_transition=0:normalize=0[all]`;
  graph.push(mixed);
  graph.push(`[all]volume=${gainDb}dB,apad=whole_dur=${seconds},atrim=0:${seconds},asetpts=PTS-STARTPTS[out]`);
  return ["-hide_banner", "-y", "-loglevel", "error", ...inputs, "-filter_complex", graph.join(";"), "-map", "[out]", "-c:a", "pcm_s16le", "-ar", String(SAMPLE_RATE), "-ac", "2", outFile];
}

/** One sound file through ebur128 as the track will carry it (48 kHz stereo), padded so a short hit still fills a window. */
export function sfxMeasureArgs(file) {
  return ["-hide_banner", "-nostats", "-i", file, "-af", `aformat=sample_rates=${SAMPLE_RATE}:channel_layouts=stereo,apad=pad_dur=${SFX_MEASURE_PAD_SECONDS},${EBUR128}`, "-f", "null", "-"];
}

const level = (text) => (text === "-inf" ? -Infinity : Number(text));
const WINDOW = /\bt:\s*(-?\d+(?:\.\d+)?)\s+TARGET:[^\n]*?\bM:\s*(-?\d+(?:\.\d+)?|-inf)\b[^\n]*?\bFTPK:\s*((?:-?\d+(?:\.\d+)?|-inf)(?:\s+(?:-?\d+(?:\.\d+)?|-inf))*)\s+dBFS/g;

/**
 * Everything ebur128 printed: the summary's integrated loudness and true peak, and every 100 ms
 * line as { t, m, tp } (the time the window ends at, its momentary loudness, the loudest channel's
 * true peak in that step). A line before the first full window reads -120.7, silence likewise.
 */
export function parseEbur128Windows(stderr) {
  const { integrated, truePeak } = parseEbur128(stderr);
  const windows = [];
  for (const match of stderr.matchAll(WINDOW)) {
    windows.push({ t: Number(match[1]), m: level(match[2]), tp: Math.max(...match[3].trim().split(/\s+/).map(level)) });
  }
  return { integrated, truePeak, windows };
}

/** What `assemble sfx-measure` writes for one file: its integrated and loudest momentary loudness and its true peak. */
export function soundMeasurement(stderr) {
  const { integrated, truePeak, windows } = parseEbur128Windows(stderr);
  const momentary = windows.reduce((max, window) => Math.max(max, window.m), -Infinity);
  if (!Number.isFinite(integrated) || integrated <= -70 || !Number.isFinite(momentary) || momentary <= -70) throw new PlanError("ebur128 measured no loudness: the file is silent or empty");
  return { lufs_i: tenth(integrated), lufs_m: tenth(momentary), peak_dbtp: tenth(truePeak) };
}

const nullOutput = (inputs, filter) => ["-hide_banner", "-nostats", ...inputs, "-filter_complex", filter, "-map", "[out]", "-f", "null", "-"];

/**
 * The mix the effects are laid over, through ebur128: the voice with the bed ducked under it
 * when there is a track (the cut's own graph), else the voice alone to stereo. Its integrated
 * loudness says what the final normalization will add; its windows say what each cue rises over.
 */
export function underMixArgs(narration, musicFile, music, totalSeconds) {
  if (musicFile) {
    const { inputs, filter } = soundGraph(narration, { musicFile, music }, totalSeconds);
    return nullOutput(inputs, `${filter};[mix]${EBUR128}[out]`);
  }
  return nullOutput(["-i", narration], `[0:a]aformat=sample_rates=${SAMPLE_RATE}:channel_layouts=mono,${STEREO},${EBUR128}[out]`);
}

/**
 * The bed alone as it sits in the mix, ducked under the voice by the same compressor as the
 * mix (drama.mjs mixFilter; the two lines are kept identical), through ebur128.
 */
export function duckedBedArgs(narration, musicFile, music, totalSeconds) {
  const { inputs } = soundGraph(narration, { musicFile, music }, totalSeconds);
  const filter = [
    bedFilter(music, totalSeconds),
    `[0:a]aformat=sample_rates=${SAMPLE_RATE}:channel_layouts=mono,${STEREO}[side]`,
    `[bed][side]sidechaincompress=threshold=${DUCK_THRESHOLD}:ratio=${duckRatio(music.duck_db)}:attack=${DUCK_ATTACK_MS}:release=${DUCK_RELEASE_MS}:makeup=1:level_sc=1[ducked]`,
    `[ducked]${EBUR128}[out]`,
  ].join(";");
  return nullOutput(inputs, filter);
}

/** The whole mix before normalization (voice, bed and effects) through ebur128, for the true peak around each cue. */
export function mixWindowsArgs(narration, musicFile, music, totalSeconds, sfxFile) {
  const { inputs, filter } = soundGraph(narration, { musicFile, music, sfxFile }, totalSeconds);
  return nullOutput(inputs, `${filter};[mix]${EBUR128}[out]`);
}

/**
 * Whether each cue can be heard, from the windows of four measurements made on the same clock:
 * the effects track, the mix under it (voice and bed), the ducked bed alone (null without a
 * track) and the whole mix. A cue's window runs from its frame to the end of its sound plus one
 * momentary window (`seconds` maps a sound to its length). Every level is reported in the
 * finished mix (`finalGain` is what the normalization adds). A cue is masked when its loudest
 * window is under SFX_ABOVE_BED_DB above the bed's, and clips the voice when the mix's true peak
 * in its window would pass the normalization's ceiling. `{ cues, problems, min_bed_margin_db }`.
 */
export function sfxAudibility(events, { effect, under, bed = null, mix }, { seconds = {}, finalGain = 0 } = {}) {
  const problems = [];
  const cues = events.map((event) => {
    const start = event.frame / FPS;
    const end = start + (seconds[event.sound] ?? 0) + MOMENTARY_SECONDS;
    const inWindow = (windows) => windows.filter((window) => window.t > start && window.t < end);
    const loudest = (windows, key) => inWindow(windows).reduce((max, window) => Math.max(max, window[key]), -Infinity) + finalGain;
    const effectM = loudest(effect, "m");
    const underM = loudest(under, "m");
    const bedM = bed ? loudest(bed, "m") : null;
    const mixTp = loudest(mix, "tp");
    const bedMargin = bedM === null ? null : effectM - bedM;
    const where = `${event.sound} at ${start.toFixed(2)} s (${event.cue !== undefined ? `sfx.cues[${event.cue}]` : `scene ${event.scene}`})`;
    const record = {
      frame: event.frame, t: Number(start.toFixed(2)), sound: event.sound, scene: event.scene,
      ...(event.cue !== undefined ? { cue: event.cue } : {}),
      ...(event.gain_db !== undefined ? { gain_db: event.gain_db } : {}),
      ...(event.target_lufs !== undefined ? { target_lufs: event.target_lufs } : {}),
      ...(event.capped ? { capped: true } : {}),
      effect_lufs_m: tenth(effectM), under_lufs_m: tenth(underM), bed_lufs_m: tenth(bedM ?? NaN),
      bed_margin_db: tenth(bedMargin ?? NaN), voice_margin_db: tenth(effectM - underM), peak_dbtp: tenth(mixTp), ok: true,
    };
    if (!Number.isFinite(effectM)) {
      problems.push(`sound effect ${where} was not measured: no ebur128 window covers it`);
      record.ok = false;
    } else if (bedMargin !== null && bedMargin < SFX_ABOVE_BED_DB) {
      problems.push(`sound effect ${where} is masked by the music bed: ${bedMargin.toFixed(1)} dB above it, below ${SFX_ABOVE_BED_DB}; raise the sound's target_lufs or the cue's gain_db, or move the cue`);
      record.ok = false;
    }
    if (Number.isFinite(mixTp) && mixTp > LOUDNESS.truePeak) {
      problems.push(`sound effect ${where} clips the voice: the mix would peak at ${mixTp.toFixed(1)} dBTP after normalization, above ${LOUDNESS.truePeak}; lower the cue's gain_db or the sound's target_lufs`);
      record.ok = false;
    }
    return record;
  });
  const margins = cues.map((cue) => cue.bed_margin_db).filter((margin) => margin !== null);
  return { cues, problems, min_bed_margin_db: margins.length ? Math.min(...margins) : null };
}

/**
 * What a cut's effects were made from: the script's sfx block (its set, gain, cue sheet and
 * bound manifest hash) and every sound's file hash; a version 2 set adds the targets its cues
 * are gained toward. The three rule sounds come first, so a version 1 set hashes as it always has.
 */
export function sfxSetHash(doc, manifest) {
  const sounds = manifest?.sounds ?? {};
  const names = [...SFX_NAMES, ...Object.keys(sounds).filter((name) => !SFX_NAMES.includes(name)).sort()];
  const hashes = names.map((name) => [name, sounds[name]?.sha256 ?? sounds[name]?.file ?? null]);
  const parts = ["sfx-set", resolveSfx(doc), hashes];
  if (sfxManifestVersion(manifest) === 2) parts.push({ version: 2, targets: Object.fromEntries(names.map((name) => [name, sfxTargetLufs(name, sounds[name])])) });
  return createHash("sha256").update(JSON.stringify(parts)).digest("hex").slice(0, 16);
}

/** The set's directory under the work base. */
export const sfxDir = (workBase, set) => `${workBase}/_sfx/${set}`;

export function requireSfxManifest(manifest) {
  const problems = sfxSetProblems(manifest);
  if (problems.length) throw new PlanError(`the sound-effect set is not usable: ${problems.join("; ")}`);
  return manifest;
}
