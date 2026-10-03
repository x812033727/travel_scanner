// A still that came back with a paper margin around it (the print looks of docs/videos/ILLUSTRATED.md
// §第二輪: asked for a print, the model often paints the paper too, a flat cream band a few percent
// wide on every side) is trimmed before it is used: the margin is measured on a small grey copy,
// the largest 16:9 box inside it is cut out and scaled back to the picture's size. Under a camera
// move a margin would travel with the picture and read as a sloppy crop; cut off, the picture
// fills the frame as the looks ask. Best effort: no ffmpeg, or a picture ffmpeg cannot read, and
// the picture is used as it came.
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";

import { locateFfmpeg } from "../assemble/ffmpeg.mjs";

const exec = promisify(execFile);

// The grey copy the margins are measured on: 16:9 like the pictures, small enough to read in a blink.
export const ANALYSIS = { width: 512, height: 288 };
// A line of pixels is a margin when it is this flat (standard deviation out of 255) and this close
// to the edge line's tone; the walk inward stops at MARGIN_MAX_SHARE of the dimension, and a margin
// under MARGIN_MIN_SHARE on every side is left alone (a dark vignette is not a border).
export const MARGIN_FLAT_STD = 10;
export const MARGIN_TONE_STEP = 8;
export const MARGIN_MAX_SHARE = 0.08;
export const MARGIN_MIN_SHARE = 0.006;

function lineStats(gray, width, height, side, index) {
  let sum = 0;
  let squares = 0;
  const count = side === "top" || side === "bottom" ? width : height;
  for (let step = 0; step < count; step++) {
    const x = side === "left" ? index : side === "right" ? width - 1 - index : step;
    const y = side === "top" ? index : side === "bottom" ? height - 1 - index : step;
    const value = gray[y * width + x];
    sum += value;
    squares += value * value;
  }
  const mean = sum / count;
  return { mean, std: Math.sqrt(Math.max(0, squares / count - mean * mean)) };
}

/**
 * The flat margin on each side of a grey picture, in pixels of that picture: lines are walked
 * inward from the edge while they are as flat as a painted border and as light or dark as the
 * edge line, up to `maxShare` of the dimension.
 */
export function marginsOf(gray, width, height, { flat = MARGIN_FLAT_STD, tone = MARGIN_TONE_STEP, maxShare = MARGIN_MAX_SHARE } = {}) {
  const margins = {};
  for (const side of ["top", "bottom", "left", "right"]) {
    const limit = Math.floor((side === "top" || side === "bottom" ? height : width) * maxShare);
    const edge = lineStats(gray, width, height, side, 0);
    let depth = 0;
    while (depth < limit) {
      const line = lineStats(gray, width, height, side, depth);
      if (line.std > flat || Math.abs(line.mean - edge.mean) > tone) break;
      depth += 1;
    }
    margins[side] = depth;
  }
  return margins;
}

/**
 * The largest box of the picture's own aspect inside the margins, centred, as `{ x, y, w, h }`
 * in that picture's pixels (even numbers), or null when no side has a margin worth cutting.
 */
export function marginCrop(margins, width, height, { minShare = MARGIN_MIN_SHARE } = {}) {
  const shares = [margins.top / height, margins.bottom / height, margins.left / width, margins.right / width];
  if (Math.max(...shares) < minShare) return null;
  const innerW = width - margins.left - margins.right;
  const innerH = height - margins.top - margins.bottom;
  const aspect = width / height;
  let w = innerW;
  let h = innerH;
  if (w / h > aspect) w = h * aspect;
  else h = w / aspect;
  w = Math.floor(w / 2) * 2;
  h = Math.floor(h / 2) * 2;
  const x = Math.round(margins.left + (innerW - w) / 2);
  const y = Math.round(margins.top + (innerH - h) / 2);
  return { x, y, w, h };
}

/** A crop measured on the analysis copy, scaled to the picture's own size. */
export function scaleCrop(crop, from, to) {
  const sx = to.width / from.width;
  const sy = to.height / from.height;
  const w = Math.floor((crop.w * sx) / 2) * 2;
  const h = Math.floor((crop.h * sy) / 2) * 2;
  return { x: Math.min(Math.round(crop.x * sx), to.width - w), y: Math.min(Math.round(crop.y * sy), to.height - h), w, h };
}

export const grayArgs = (file) => ["-hide_banner", "-loglevel", "error", "-i", file, "-vf", `scale=${ANALYSIS.width}:${ANALYSIS.height}:flags=area,format=gray`, "-frames:v", "1", "-f", "rawvideo", "-"];
export const sizeArgs = (file) => ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", file];
export const trimArgs = (file, crop, size, outFile) => ["-hide_banner", "-loglevel", "error", "-y", "-i", file, "-vf", `crop=${crop.w}:${crop.h}:${crop.x}:${crop.y},scale=${size.width}:${size.height}:flags=lanczos`, "-frames:v", "1", outFile];

/** The trimmed file's name beside the picture: keyframes/podium-1.png → keyframes/podium-1-trim.png. */
export const trimmedName = (file) => file.replace(/(\.[a-z0-9]+)$/i, "-trim$1");

/**
 * Trim the paper margin off a picture in `workdir` when it has one. Returns
 * `{ file, sha256, margins }` for the trimmed copy (file relative to the workdir, as the
 * manifest records it), or null when nothing was cut: no margin, no ffmpeg, or a picture ffmpeg
 * could not read. `ctx.trimImage(file) → { file, sha256, margins } | null` stands in for tests.
 */
export async function trimMargins(ctx, workdir, file) {
  if (ctx.trimImage) return ctx.trimImage(file);
  let tools;
  try {
    tools = await locateFfmpeg(ctx.env);
  } catch {
    return null;
  }
  const source = path.join(workdir, file);
  try {
    const { stdout: gray } = await exec(tools.ffmpeg, grayArgs(source), { encoding: "buffer", maxBuffer: 4 << 20, windowsHide: true });
    if (gray.length !== ANALYSIS.width * ANALYSIS.height) return null;
    const margins = marginsOf(gray, ANALYSIS.width, ANALYSIS.height);
    const crop = marginCrop(margins, ANALYSIS.width, ANALYSIS.height);
    if (!crop) return null;
    const probe = JSON.parse((await exec(tools.ffprobe, sizeArgs(source), { windowsHide: true })).stdout);
    const size = { width: Number(probe.streams?.[0]?.width), height: Number(probe.streams?.[0]?.height) };
    if (!(size.width > 0 && size.height > 0)) return null;
    const out = trimmedName(file);
    await exec(tools.ffmpeg, trimArgs(source, scaleCrop(crop, ANALYSIS, size), size, path.join(workdir, out)), { windowsHide: true });
    const sha256 = createHash("sha256").update(readFileSync(path.join(workdir, out))).digest("hex");
    const share = (side) => Math.round((margins[side] / (side === "top" || side === "bottom" ? ANALYSIS.height : ANALYSIS.width)) * 1000) / 10;
    return { file: out, sha256, margins: { top: share("top"), bottom: share("bottom"), left: share("left"), right: share("right") } };
  } catch {
    return null;
  }
}
