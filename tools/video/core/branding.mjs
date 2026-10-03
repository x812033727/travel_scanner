// A channel's current bookends are a default for first builds only. Every completed cut pins
// its choice locally, so changing the channel default never schedules an old video again.
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";

import { readApprovals } from "./approvals.mjs";
import { isExplainer } from "./drama.mjs";
import { atomicWrite, readJson, UsageError } from "./paths.mjs";
import { FPS, frameToMs } from "./timeline.mjs";

export const BRANDING_FILE = "branding.json";
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
  result.hash = brandingHash(result);
  if (value.hash !== undefined && value.hash !== result.hash) throw new UsageError("branding hash does not match its pinned assets");
  return result;
}

/** Paths and adoption dates do not affect the pictures or sound. */
export function brandingHash(branding) {
  if (!branding) return null;
  return createHash("sha256").update(JSON.stringify([
    "channel-bookends-v1", FPS,
    ...["intro", "outro"].map((role) => [branding[role].sha256.toLowerCase(), branding[role].frames]),
  ])).digest("hex");
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
  const series = isExplainer(doc) ? "sothatswhy" : null;
  if (series && existsSync(path.join(workBase, currentBrandingFile(series)))) return readCurrentBranding(workBase, { series });
  return readCurrentBranding(workBase);
}

/** This check never reads the channel default or hashes source media of completed videos. */
export function brandingCurrent(checks, selection) {
  return (checks?.branding?.hash ?? null) === brandingHash(selection);
}

export const appliedBranding = (checks) => checks?.branding ?? null;

export function adoptionRefusal({ doc, workdir }) {
  if (!LONG_FORMATS.has(doc?.format)) return "channel bookends apply to long videos only; Shorts stay unchanged";
  const state = readJson(path.join(workdir, "auto.json"), null);
  if (doc.youtube?.video_id || state?.youtube_video_id || ["done", "dropped"].includes(state?.status)) return "this video is already uploaded or finished; its branding stays unchanged";
  if (readApprovals(workdir).approvals.some((entry) => ["final", "publish"].includes(entry.gate))) return "this video already has a final or publish approval; its branding stays unchanged";
  if (existsSync(path.join(workdir, "upload", "metadata.json"))) return "this video already has an upload package; its branding stays unchanged";
  return null;
}

function previouslyBuilt(workdir) {
  if (["final.mp4", "checks.json", path.join("upload", "metadata.json")].some((file) => existsSync(path.join(workdir, file)))) return true;
  return (readJson(path.join(workdir, "state.json"), { runs: [] }).runs ?? []).some((entry) => entry.ok !== false && ["assemble", "compile", "import"].includes(entry.stage));
}

/**
 * Resolve, but do not save, the choice for this build. --force never adopts a new default.
 * A legacy cut with no pin stays unbranded unless explicitly selected with --adopt-branding.
 */
export async function selectBrandingForBuild({ doc, workdir, workBase, adoptCurrent = false }) {
  if (adoptCurrent) {
    const refusal = adoptionRefusal({ doc, workdir });
    if (refusal) throw new UsageError(refusal);
    const current = readDefaultBranding(workBase, doc);
    if (!current) throw new UsageError("no current branding package is installed for this video");
    return current;
  }
  if (!LONG_FORMATS.has(doc?.format)) return null;
  const pinned = readBranding(workdir);
  if (pinned) return pinned;
  if (adoptionRefusal({ doc, workdir }) || previouslyBuilt(workdir)) return null;
  return readDefaultBranding(workBase, doc);
}

/** Save only after a completed replacement, never while the old final is still in use. */
export function pinBranding(workdir, branding, now = new Date()) {
  if (!branding) return;
  const pin = validateBranding(branding);
  atomicWrite(path.join(workdir, BRANDING_FILE), `${JSON.stringify({ ...pin, adopted_at: now.toISOString() }, null, 2)}\n`);
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
  const offset = branding.intro_frames;
  const shift = (entry) => ({ ...entry, start_frame: entry.start_frame + offset, ...(entry.end_frame === undefined ? {} : { end_frame: entry.end_frame + offset }) });
  return {
    ...timeline,
    branding_hash: branding.hash,
    body_total_frames: timeline.total_frames,
    content_end_frame: offset + timeline.total_frames,
    total_frames: offset + timeline.total_frames + branding.outro_frames,
    lines: (timeline.lines ?? []).map(shift),
    ...(timeline.actions ? { actions: timeline.actions.map(shift) } : {}),
    scenes: (timeline.scenes ?? []).map((scene) => ({ ...shift(scene), ...(scene.states ? { states: scene.states.map(shift) } : {}) })),
    ...(timeline.windows ? { windows: timeline.windows.map(shift) } : {}),
    chapters: (timeline.chapters ?? []).map((chapter, index) => ({ ...chapter, start_frame: index === 0 ? 0 : chapter.start_frame + offset })),
  };
}

export function shiftBrandingCues(cues, branding, direction = 1) {
  if (!branding) return cues;
  const offset = frameToMs(branding.intro_frames) * direction;
  return cues.map((cue) => ({ ...cue, start_ms: Math.round(cue.start_ms + offset), end_ms: Math.round(cue.end_ms + offset) }));
}
