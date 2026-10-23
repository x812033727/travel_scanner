// The channel mark a cut carries in its corner (docs/videos/WATERMARK.md): which pictures it is,
// where it sits, and which videos get it.
//
// A version is two PNGs under tools/video/watermark/<id>/, one for each frame shape, registered
// here with its SHA-256 and its box. A version never changes: a video pins the one it was first
// drawn with (watermark.json in its work directory) and is drawn with those bytes ever after, so
// a new look is a new version and never moves a cut that exists.
//
// Render alone decides whether a video carries the mark, once, and says so in frames/manifest.json;
// assemble follows the manifest. Two stages deciding would disagree: a first assemble that fails
// its checks leaves final.mp4 behind, and the next one would take the video for one built before
// the mark existed, with the mark on its slides and not on its shots.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { readApprovals } from "./approvals.mjs";
import { atomicWrite, readJson, UsageError } from "./paths.mjs";

export const WATERMARK_FILE = "watermark.json";
export const WATERMARK_DIR = fileURLToPath(new URL("../watermark/", import.meta.url));

// `box` is where the PNG is laid on the frame, in the frame's pixels. A long cut's mark ends
// where the slides' own chrome does (theme.css --safe-x, 96 px from the right edge: the PNG's 6 px
// of padding puts its letters there), under the progress bar and above the content area. A
// Short's sits at the right end of the cards' header row, inside the safe area
// (docs/videos/SHORTS.md: x 78–902). Every number is even: the mark goes over 4:2:0 video.
export const WATERMARKS = Object.freeze({
  v1: Object.freeze({
    long: Object.freeze({ file: "long.png", sha256: "2d168413a11c5978ff0ea66a40393aa7949dceebeba7fc77bb9cee1a9e41339c", box: Object.freeze({ x: 1622, y: 54, width: 208, height: 74 }) }),
    shorts: Object.freeze({ file: "shorts.png", sha256: "180b6af6f1b7843b32d4ec9dc526acf584ceffb2b1cc8aabe8d7a80a8cbd5a83", box: Object.freeze({ x: 636, y: 80, width: 266, height: 92 }) }),
  }),
});
// What a video drawn for the first time carries.
export const CURRENT_WATERMARK = "v1";

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const verified = new Map();

/**
 * One shape of one version: { id, shape, file, sha256, box }, `file` absolute. The bytes on disk
 * are checked against the registry the first time a shape is asked for, so a PNG edited in place
 * stops the build instead of quietly changing every video pinned to it.
 */
export function watermark(id = CURRENT_WATERMARK, shape = "long") {
  const entry = Object.hasOwn(WATERMARKS, id) ? WATERMARKS[id][shape] : null;
  if (!entry) throw new UsageError(`there is no channel mark "${id}" for a ${shape} cut in this checkout`);
  const file = path.join(WATERMARK_DIR, id, entry.file);
  const key = `${id}/${shape}`;
  if (!verified.has(key)) {
    if (!existsSync(file)) throw new UsageError(`${file} is missing; the channel mark ${id} cannot be drawn`);
    const bytes = readFileSync(file);
    if (sha256(bytes) !== entry.sha256) throw new UsageError(`${file} is not the picture registered as channel mark ${id}; a version is never edited, add a new one`);
    verified.set(key, bytes);
  }
  return { id, shape, file, sha256: entry.sha256, box: { ...entry.box } };
}

/** The PNG as a data URI: a slide carries it whole, since a page may load nothing from tools/. */
export function watermarkDataUri(mark) {
  watermark(mark.id, mark.shape);
  return `data:image/png;base64,${verified.get(`${mark.id}/${mark.shape}`).toString("base64")}`;
}

/** What a manifest or a checks file says of the mark a cut carries. */
export const watermarkRecord = (mark) => (mark ? { id: mark.id, sha256: mark.sha256, box: { ...mark.box } } : null);

/**
 * The mark a record names, for the stage that follows one: null without a record, and an error
 * when the record names bytes this checkout does not hold.
 */
export function resolveWatermark(record, shape = "long") {
  if (record === null || record === undefined) return null;
  if (typeof record?.id !== "string" || typeof record.sha256 !== "string") throw new UsageError("the channel mark record needs an id and a SHA-256");
  const mark = watermark(record.id, shape);
  // A record is written for the long shape; a Short's reads its own.
  if (record.sha256 !== watermark(record.id, "long").sha256) throw new UsageError(`the channel mark ${record.id} recorded for this video is not the one in this checkout; run render again`);
  return mark;
}

/** The version this video is pinned to, or null. */
export function readWatermarkPin(workdir) {
  const pin = readJson(path.join(workdir, WATERMARK_FILE), null);
  if (pin === null) return null;
  if (pin?.schema_version !== 1 || typeof pin.id !== "string" || typeof pin.sha256 !== "string") throw new UsageError(`${WATERMARK_FILE} needs schema_version 1, an id and a SHA-256`);
  return resolveWatermark(pin);
}

/** Written by render beside the manifest that names the same mark, never before it. */
export function pinWatermark(workdir, mark, now = new Date()) {
  if (!mark) return;
  if (existsSync(path.join(workdir, WATERMARK_FILE))) return;
  atomicWrite(path.join(workdir, WATERMARK_FILE), `${JSON.stringify({ schema_version: 1, id: mark.id, sha256: mark.sha256, adopted_at: now.toISOString() }, null, 2)}\n`);
}

/** Why a cut that exists keeps the pictures it has; null when nobody has seen or shipped it. */
export function watermarkRefusal({ doc, workdir }) {
  const state = readJson(path.join(workdir, "auto.json"), null);
  if (doc?.youtube?.video_id || state?.youtube_video_id || ["done", "dropped"].includes(state?.status)) return "this video is already uploaded or finished; its pictures stay as they are";
  if (readApprovals(workdir).approvals.some((entry) => ["final", "publish"].includes(entry.gate))) return "this video already has a final or publish approval; its pictures stay as they are";
  if (existsSync(path.join(workdir, "upload", "metadata.json"))) return "this video already has an upload package; its pictures stay as they are";
  return null;
}

function previouslyBuilt(workdir) {
  if (["final.mp4", "checks.json", path.join("upload", "metadata.json")].some((file) => existsSync(path.join(workdir, file)))) return true;
  return (readJson(path.join(workdir, "state.json"), { runs: [] }).runs ?? []).some((entry) => entry.ok !== false && ["assemble", "compile", "import"].includes(entry.stage));
}

/**
 * The mark render draws this video with, or null for none. A pinned video keeps its version
 * whatever the current one is. A video that was cut before it had a pin stays unmarked, so its
 * frames are redrawn byte for byte; `adopt` (render --adopt-watermark) gives such a cut the
 * current mark, and is refused once the cut has been approved, packaged or uploaded.
 */
export function selectWatermarkForRender({ doc, workdir, adopt = false }) {
  const pinned = readWatermarkPin(workdir);
  if (pinned) return pinned;
  const refusal = watermarkRefusal({ doc, workdir });
  if (adopt) {
    if (refusal) throw new UsageError(refusal);
    return watermark();
  }
  if (refusal || previouslyBuilt(workdir)) return null;
  return watermark();
}
