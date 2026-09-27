// How a compilation's cards and the episodes' cuts become one final.mp4, as pure functions:
// each card's frames, the join list, every ffmpeg argument, the disk and readiness checks.
//
// The picture is joined without re-encoding: every card is a still encoded with the slides'
// segment settings, and every episode's final.mp4 came out of assemble with the same encoder,
// so the concat demuxer copies them (docs/videos/BINGE.md). The sound is not copied: AAC codes
// 1,024-sample frames, so each cut's audio is up to three frames longer than its picture, and
// forty of them copied back to back would drift the last chapter a tenth of a second. Each
// input's audio is instead cut and padded to exactly its frames' worth of samples, the cards
// get silence of their length, and the whole is encoded once.
import { FPS, SAMPLE_RATE, SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import { LOUDNESS, segmentKey } from "../assemble/plan.mjs";

// The episodes were normalized to -14 LUFS one by one; their sum lands within this of it.
export const LOUDNESS_TOLERANCE_LU = 1.5;
export const AUDIO_BITRATE = "384k";
// Free disk the join needs: the cuts again for final.mp4 and its partial, plus room for the
// segments, the preview and the upload package's hard link failing over to a copy.
export const DISK_FACTOR = 1.5;
export const DISK_RESERVE_BYTES = 2.5 * 1024 ** 3;
const GB = 1024 ** 3;

export class CompileError extends Error {}

export const gigabytes = (bytes) => (bytes / GB).toFixed(2);

/** Why an episode is not cleared for upload, or null. `approval` is its last final-gate entry. */
export function episodeProblem({ approval, exists, sha256, checks, timeline }) {
  if (!approval?.sha256) return "final.mp4 was never approved (no final entry in approvals.json)";
  if (!exists) return "final.mp4 is missing";
  if (sha256 !== approval.sha256) return `final.mp4 (${String(sha256).slice(0, 12)}) is not the approved cut (${approval.sha256.slice(0, 12)})`;
  if (!checks?.ok) return checks ? `checks.json failed: ${(checks.problems ?? []).join("; ") || "no reason recorded"}` : "checks.json is missing";
  if (!Number.isInteger(timeline?.total_frames) || timeline.total_frames <= 0) return "timeline.json has no total_frames";
  return null;
}

export function diskNeeded(episodeBytes) {
  return Math.ceil(episodeBytes * DISK_FACTOR + DISK_RESERVE_BYTES);
}

/** The refusal when the work base has less than the join needs, or null. */
export function diskProblem(freeBytes, episodeBytes, workBase) {
  const needed = diskNeeded(episodeBytes);
  if (freeBytes >= needed) return null;
  return `not enough free disk on ${workBase}: ${gigabytes(freeBytes)} GB free, ${gigabytes(needed)} GB needed (${gigabytes(episodeBytes)} GB of cuts × ${DISK_FACTOR} + ${gigabytes(DISK_RESERVE_BYTES)} GB)`;
}

/**
 * A card's images and frame counts, as assemble lays out a slide state: the transition frames
 * first, one frame each, then the still for the rest. `rendered` is the card's scene in
 * frames/manifest.json.
 */
export function cardEntries(rendered, frames) {
  const picture = rendered.states?.[0];
  if (!picture?.still) throw new CompileError(`card ${rendered.id} has no rendered still; run render again`);
  const transition = (picture.transition ?? []).slice(0, Math.max(0, frames - 1));
  const entries = transition.map((file) => ({ file, frames: 1 }));
  if (frames - transition.length > 0) entries.push({ file: picture.still, frames: frames - transition.length });
  return entries;
}

/** Every card of the layout with its entries and cache key: [{ id, kind, frames, entries, key }]. */
export function cardSegments(layout, manifest) {
  const rendered = new Map((manifest.scenes ?? []).map((scene) => [scene.id, scene]));
  return layout
    .filter((entry) => entry.kind !== "episode")
    .map((entry) => {
      const scene = rendered.get(entry.id);
      if (!scene) throw new CompileError(`frames/manifest.json has no card ${entry.id}; run render again`);
      const entries = cardEntries(scene, entry.frames);
      return { id: entry.id, kind: entry.kind, frames: entry.frames, entries, key: segmentKey({ frames: entry.frames, entries }) };
    });
}

const quote = (file) => `'${file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`;

/** The join list: every segment and cut by absolute path, in play order, for the concat demuxer. */
export function joinList(files) {
  return `ffconcat version 1.0\n${files.map((file) => `file ${quote(file)}`).join("\n")}\n`;
}

/** Seconds as ffmpeg reads them, without a float's tail. */
export const seconds = (frames) => Number((frames / FPS).toFixed(6)).toString();

/**
 * The audio inputs, one per layout entry: an episode's own file, or `null` for a card, which
 * gets silence of its length. Each carries its exact length in samples.
 */
export function audioInputs(layout, cutFiles) {
  return layout.map((entry) => ({
    file: entry.kind === "episode" ? cutFiles[entry.id] ?? entry.file : null,
    frames: entry.frames,
    samples: entry.frames * SAMPLES_PER_FRAME,
  }));
}

/**
 * The one ffmpeg call that joins everything. Input 0 is the join list (its video is copied);
 * every card and cut is its own input after it, a card as `anullsrc` of its length. Each input's
 * audio is trimmed and padded to exactly its frames' samples, so the seams stay on the frame
 * grid however AAC padded the cuts, then the pieces are concatenated and encoded once.
 */
export function joinArgs(listFile, inputs, outFile) {
  const args = ["-hide_banner", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listFile];
  const filters = [];
  const labels = [];
  inputs.forEach((input, index) => {
    const k = index + 1;
    if (input.file) args.push("-i", input.file);
    else args.push("-f", "lavfi", "-t", seconds(input.frames), "-i", `anullsrc=r=${SAMPLE_RATE}:cl=stereo`);
    filters.push(`[${k}:a]atrim=end_sample=${input.samples},apad=whole_len=${input.samples}[a${k}]`);
    labels.push(`[a${k}]`);
  });
  filters.push(`${labels.join("")}concat=n=${inputs.length}:v=0:a=1[a]`);
  args.push(
    "-filter_complex", filters.join(";"),
    "-map", "0:v:0", "-c:v", "copy",
    "-map", "[a]", "-c:a", "aac", "-b:a", AUDIO_BITRATE, "-ar", String(SAMPLE_RATE),
    "-movflags", "+faststart", outFile,
  );
  return args;
}

/** Like assemble's loudness check, with the wider tolerance a sum of normalized cuts needs. */
export function checkCompilationLoudness({ integrated, truePeak }, tolerance = LOUDNESS_TOLERANCE_LU) {
  const problems = [];
  if (Math.abs(integrated - LOUDNESS.integrated) > tolerance) problems.push(`loudness ${integrated} LUFS, target ${LOUDNESS.integrated} ± ${tolerance}`);
  if (truePeak !== null && truePeak > LOUDNESS.truePeak + 0.5) problems.push(`true peak ${truePeak} dBFS, above ${LOUDNESS.truePeak}`);
  return problems;
}

/** Cues that start before the previous one ends, as problems; a merged track should have none. */
export function overlapProblems(cues) {
  const problems = [];
  cues.forEach((cue, index) => {
    if (index > 0 && cue.start_ms < cues[index - 1].end_ms) problems.push(`cue ${index + 1} overlaps the previous cue`);
  });
  return problems;
}

/** The dry run's table: one line per layout entry with its clock and length. */
export function layoutLines(layout, chapters) {
  const clock = (frame) => {
    const total = Math.floor(frame / FPS);
    const pad = (value) => String(value).padStart(2, "0");
    return `${Math.floor(total / 3600)}:${pad(Math.floor((total % 3600) / 60))}:${pad(total % 60)}`;
  };
  // The chapter's title goes on the line where the chapter starts: its card, or the cut itself.
  const titles = new Map(chapters.map((chapter) => [chapter.card ?? chapter.scene, chapter.title]));
  return layout.map((entry) => `${clock(entry.start_frame)}  ${entry.kind.padEnd(7)} ${entry.id}  ${entry.frames} frames${titles.has(entry.id) ? `  ${titles.get(entry.id)}` : ""}`);
}
