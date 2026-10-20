// A channel's current bookends are a default for first builds only. Every completed cut pins
// its choice locally, so changing the channel default never schedules an old video again.
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";

import { readApprovals } from "./approvals.mjs";
import { isCompilation } from "./compilation.mjs";
import { explainerSeries, hasCast, isExplainer } from "./drama.mjs";
import { atomicWrite, readJson, UsageError } from "./paths.mjs";
import { isStory } from "./story.mjs";
import { FPS, frameToMs } from "./timeline.mjs";

export const BRANDING_FILE = "branding.json";
/**
 * Where the intro plays (docs/videos/BRANDING.md §片頭位置). "start" is every cut made before
 * 2026-10-13 and every drama with a cast, compilation and Short; a narrated long video opens on
 * its 30–60 s condensation (chapter 1) and plays the intro at the start of chapter 2.
 */
export const INTRO_AT_START = "start";
export const INTRO_AFTER_FIRST_CHAPTER = "after_first_chapter";
export const INTRO_PLACEMENTS = Object.freeze([INTRO_AT_START, INTRO_AFTER_FIRST_CHAPTER]);
export const CURRENT_BRANDING_FILE = path.join("_branding", "current.json");
export function currentBrandingFile(series = null) {
  if (series === null) return CURRENT_BRANDING_FILE;
  if (series !== "sothatswhy") throw new UsageError("branding --series supports only sothatswhy");
  return path.join("_branding", "series", series, "current.json");
}
const SHA256 = /^[a-f0-9]{64}$/i;
const LONG_FORMATS = new Set(["slides", "screencast", "drama"]);

/** Validate a source package or pin without touching its media. Relative paths use `base`. */
export function validateBranding(value, { base = process.cwd() } = {}) {
  if (value === null || value?.enabled === false) return null;
  if (!value || value.schema_version !== 1 || typeof value.id !== "string" || !value.id.trim()) {
    throw new UsageError("branding needs schema_version 1 and a non-empty id");
  }
  const result = { schema_version: 1, id: value.id.trim() };
  for (const role of ["intro", "outro"]) {
    const clip = value[role];
    if (!clip || typeof clip.file !== "string" || !clip.file.trim() || !SHA256.test(clip.sha256 ?? "") || !Number.isInteger(clip.frames) || clip.frames <= 0 || clip.frames > FPS * 30) {
      throw new UsageError(`branding ${role} needs a file, SHA-256 and 1–${FPS * 30} frames`);
    }
    result[role] = { file: path.resolve(base, clip.file), sha256: clip.sha256.toLowerCase(), frames: clip.frames };
  }
  // A pin without the field is a cut made before the placement existed: its intro is at the start.
  const introAt = value.intro_at ?? INTRO_AT_START;
  if (!INTRO_PLACEMENTS.includes(introAt)) throw new UsageError(`branding intro_at must be one of ${INTRO_PLACEMENTS.join(", ")}`);
  if (introAt !== INTRO_AT_START) result.intro_at = introAt;
  result.hash = brandingHash(result);
  if (value.hash !== undefined && value.hash !== result.hash) throw new UsageError("branding hash does not match its pinned assets");
  return result;
}

/**
 * Paths and adoption dates do not affect the pictures or sound; the intro's place does. An intro
 * at the start keeps the original hash, so every existing pin, caption manifest and package stays
 * bound; one after the first chapter hashes differently, so nothing timed for the other placement
 * is reused.
 */
export function brandingHash(branding) {
  if (!branding) return null;
  const introAt = branding.intro_at ?? INTRO_AT_START;
  return createHash("sha256").update(JSON.stringify([
    introAt === INTRO_AT_START ? "channel-bookends-v1" : "channel-bookends-v2", FPS,
    ...["intro", "outro"].map((role) => [branding[role].sha256.toLowerCase(), branding[role].frames]),
    ...(introAt === INTRO_AT_START ? [] : [introAt]),
  ])).digest("hex");
}

/** The same assets with the intro at `introAt`, re-hashed. */
export function placeBranding(branding, introAt) {
  if (!branding) return null;
  const { hash, intro_at: ignored, ...assets } = branding;
  return validateBranding({ ...assets, intro_at: introAt });
}

/**
 * Narrated long videos move the intro behind their condensation: slides and screencasts, the
 * explainer dramas and brand stories (narrated even when their pictures have a cast). Dramas with
 * a cast, compilations and Shorts keep it at the start (owner default, 2026-10-12 task).
 */
export function narratedLong(doc, series = null) {
  if (!LONG_FORMATS.has(doc?.format) || isCompilation(doc)) return false;
  return !hasCast(doc) || isExplainer(doc) || isStory(series);
}

export const defaultIntroAt = (doc, series = null) => (narratedLong(doc, series) ? INTRO_AFTER_FIRST_CHAPTER : INTRO_AT_START);

/**
 * The body frame the intro is inserted before. An applied record (checks.branding) names it; a
 * pin or package placed after the first chapter takes the timeline's second chapter start, which
 * is a scene start and so a hard cut between two sentences.
 */
export function introAtFrame(branding, timeline = null) {
  if (!branding) return 0;
  if (branding.intro_at_frame !== undefined) {
    if (!Number.isSafeInteger(branding.intro_at_frame) || branding.intro_at_frame < 0) throw new UsageError("branding intro_at_frame must be a non-negative integer");
    return branding.intro_at_frame;
  }
  if ((branding.intro_at ?? INTRO_AT_START) === INTRO_AT_START) return 0;
  const frame = timeline?.chapters?.[1]?.start_frame;
  if (!Number.isSafeInteger(frame) || frame <= 0 || (Number.isSafeInteger(timeline.total_frames) && frame >= timeline.total_frames)) {
    throw new UsageError("an intro after the first chapter needs a timeline with a second chapter; add one or keep the intro at the start");
  }
  return frame;
}

export function readBranding(workdir) {
  const file = path.join(workdir, BRANDING_FILE);
  return validateBranding(readJson(file, null), { base: workdir });
}

export function readCurrentBranding(workBase, { series = null } = {}) {
  const file = path.join(workBase, currentBrandingFile(series));
  return validateBranding(readJson(file, null), { base: path.dirname(file) });
}

/** Only an absent series registry falls back; an explicit disabled choice stays disabled. */
export function readDefaultBranding(workBase, doc) {
  const series = explainerSeries(doc);
  if (series && existsSync(path.join(workBase, currentBrandingFile(series)))) return readCurrentBranding(workBase, { series });
  return readCurrentBranding(workBase);
}

/** This check never reads the channel default or hashes source media of completed videos. */
export function brandingCurrent(checks, selection) {
  return (checks?.branding?.hash ?? null) === brandingHash(selection);
}

export const appliedBranding = (checks) => checks?.branding ?? null;

/** The gates whose approval means the body itself was approved again (a new script, voice or pictures). */
const CONTENT_GATES = new Set(["script", "audio", "storyboard"]);

/**
 * Whether an approved cut is being remade: the owner approved a script, narration or storyboard
 * after the newest final or publish approval, so the cut that approval names is no longer the one
 * this build makes (2026-10-13: five recuts got a new opening after their finals were approved,
 * and the old 3-second outro without music would otherwise have stayed on them). The approvals
 * stay where they are; they just stop pinning the old bookends.
 */
export function remakingApprovedCut(workdir) {
  const approvals = readApprovals(workdir).approvals;
  const newest = (gates) => Math.max(0, ...approvals.filter((entry) => gates(entry.gate)).map((entry) => Date.parse(entry.approved_at) || 0));
  const cut = newest((gate) => gate === "final" || gate === "publish");
  return cut > 0 && newest((gate) => CONTENT_GATES.has(gate)) > cut;
}

export function adoptionRefusal({ doc, workdir }) {
  if (!LONG_FORMATS.has(doc?.format)) return "channel bookends apply to long videos only; Shorts stay unchanged";
  const state = readJson(path.join(workdir, "auto.json"), null);
  if (doc.youtube?.video_id || state?.youtube_video_id || ["done", "dropped"].includes(state?.status)) return "this video is already uploaded or finished; its branding stays unchanged";
  const remaking = remakingApprovedCut(workdir);
  if (!remaking && readApprovals(workdir).approvals.some((entry) => ["final", "publish"].includes(entry.gate))) return "this video already has a final or publish approval; its branding stays unchanged";
  if (!remaking && existsSync(path.join(workdir, "upload", "metadata.json"))) return "this video already has an upload package; its branding stays unchanged";
  return null;
}

function previouslyBuilt(workdir) {
  if (["final.mp4", "checks.json", path.join("upload", "metadata.json")].some((file) => existsSync(path.join(workdir, file)))) return true;
  return (readJson(path.join(workdir, "state.json"), { runs: [] }).runs ?? []).some((entry) => entry.ok !== false && ["assemble", "compile", "import"].includes(entry.stage));
}

/**
 * Why a cut's intro may not be moved behind its condensation, or null. Only a narrated long video
 * that is not on YouTube yet: the rebuilt final has new bytes, so any final or publish approval
 * and any upload package of the old cut stop matching it and are asked for again.
 */
export function replacementRefusal({ doc, workdir, series = null }) {
  if (!narratedLong(doc, series)) return "only a narrated long video plays its intro after the condensation; dramas with a cast, compilations and Shorts keep it at the start";
  const state = readJson(path.join(workdir, "auto.json"), null);
  if (doc.youtube?.video_id || state?.youtube_video_id || ["done", "dropped"].includes(state?.status)) return "this video is already uploaded or finished; its intro stays where it was";
  return null;
}

/**
 * Resolve, but do not save, the choice for this build. --force never adopts a new default.
 * A legacy cut with no pin stays unbranded unless explicitly selected with --adopt-branding.
 * A pin keeps its intro where it was; a first build or an adoption takes the placement of its
 * kind of video (defaultIntroAt). `introAfterCondensation` (assemble --intro-after-condensation)
 * deliberately re-places a not-yet-uploaded narrated video's pinned intro after its first chapter.
 */
export async function selectBrandingForBuild({ doc, workdir, workBase, adoptCurrent = false, series = null, introAfterCondensation = false }) {
  if (introAfterCondensation) {
    const refusal = replacementRefusal({ doc, workdir, series });
    if (refusal) throw new UsageError(refusal);
    const chosen = adoptCurrent ? await selectBrandingForBuild({ doc, workdir, workBase, adoptCurrent, series }) : readBranding(workdir) ?? readDefaultBranding(workBase, doc);
    if (!chosen) throw new UsageError("no branding is pinned or installed for this video");
    return placeBranding(chosen, INTRO_AFTER_FIRST_CHAPTER);
  }
  if (adoptCurrent) {
    const refusal = adoptionRefusal({ doc, workdir });
    if (refusal) throw new UsageError(refusal);
    const current = readDefaultBranding(workBase, doc);
    if (!current) throw new UsageError("no current branding package is installed for this video");
    return placeBranding(current, defaultIntroAt(doc, series));
  }
  if (!LONG_FORMATS.has(doc?.format)) return null;
  const pinned = readBranding(workdir);
  if (pinned) return pinned;
  if (adoptionRefusal({ doc, workdir }) || previouslyBuilt(workdir)) return null;
  return placeBranding(readDefaultBranding(workBase, doc), defaultIntroAt(doc, series));
}

/** The pin as written: the placement is always recorded, even the original "start". */
export function pinRecord(branding, now = new Date()) {
  const pin = validateBranding(branding);
  return { ...pin, intro_at: pin.intro_at ?? INTRO_AT_START, adopted_at: now.toISOString() };
}

/** Save only after a completed replacement, never while the old final is still in use. */
export function pinBranding(workdir, branding, now = new Date()) {
  if (!branding) return;
  atomicWrite(path.join(workdir, BRANDING_FILE), `${JSON.stringify(pinRecord(branding, now), null, 2)}\n`);
}

/**
 * The finished player's timeline. The narration/TTS timeline stays byte-for-byte unchanged.
 * Chapter zero includes the intro; a separate five-second chapter would fail YouTube's rules.
 */
export function presentationTimeline(timeline, branding) {
  if (!timeline || !branding) return timeline;
  if (timeline.branding_hash) {
    if (timeline.branding_hash !== branding.hash) throw new UsageError("presentation timeline has another branding version");
    return timeline;
  }
  // An applied record says intro_frames; a planned pin or package (tts's chapter check) says intro.frames.
  const offset = branding.intro_frames ?? branding.intro?.frames;
  const outro = branding.outro_frames ?? branding.outro?.frames;
  // Everything before the intro keeps its frame; everything from it on moves by the intro's
  // length. An end exactly at the intro stays before it, so chapter 1's last cue never spans it.
  const at = introAtFrame(branding, timeline);
  const startOf = (frame) => (frame >= at ? frame + offset : frame);
  const endOf = (frame) => (at === 0 || frame > at ? frame + offset : frame);
  const shift = (entry) => ({ ...entry, start_frame: startOf(entry.start_frame), ...(entry.end_frame === undefined ? {} : { end_frame: endOf(entry.end_frame) }) });
  return {
    ...timeline,
    branding_hash: branding.hash,
    body_total_frames: timeline.total_frames,
    content_end_frame: offset + timeline.total_frames,
    total_frames: offset + timeline.total_frames + outro,
    ...(at > 0 ? { intro_at_frame: at, intro_end_frame: at + offset } : {}),
    lines: (timeline.lines ?? []).map(shift),
    ...(timeline.actions ? { actions: timeline.actions.map(shift) } : {}),
    scenes: (timeline.scenes ?? []).map((scene) => ({ ...shift(scene), ...(scene.states ? { states: scene.states.map(shift) } : {}) })),
    ...(timeline.windows ? { windows: timeline.windows.map(shift) } : {}),
    chapters: (timeline.chapters ?? []).map((chapter, index) => ({ ...chapter, start_frame: index === 0 ? 0 : startOf(chapter.start_frame) })),
  };
}

/**
 * Body cues to the player's time (direction 1), or back (-1). Cues before the intro keep their
 * time; cues from it on move by its length. `branding` is an applied record (checks.branding).
 */
export function shiftBrandingCues(cues, branding, direction = 1) {
  if (!branding) return cues;
  const offset = frameToMs(branding.intro_frames);
  // Caption timestamps are rounded to whole milliseconds before reaching this helper. Compare
  // against that same rounded boundary, including on the reverse path, or the first cue after an
  // intro at a non-whole-millisecond frame can be mistaken for a cue before it.
  const atMs = Math.round(frameToMs(introAtFrame(branding)));
  const shiftedAtMs = Math.round(atMs + offset);
  const moved = (cue) => (direction > 0 ? cue.start_ms >= atMs : cue.start_ms >= shiftedAtMs);
  return cues.map((cue) => {
    const by = moved(cue) ? offset * direction : 0;
    return { ...cue, start_ms: Math.round(cue.start_ms + by), end_ms: Math.round(cue.end_ms + by) };
  });
}

/** Lines that would be cut in two by the intro (a dub line running past its narration window). */
export function linesAcrossIntro(lines, at) {
  if (!at) return [];
  return (lines ?? []).filter((line) => line.start_frame < at && line.end_frame > at).map((line) => line.id);
}
