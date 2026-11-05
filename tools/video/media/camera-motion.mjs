// Did the clip make the camera move its shot asked for? Measured from the pictures, not the prompt.
//
// H3 drifts on a locked shot unless told otherwise, and a "push in" can come back static or as a
// pan (.agents/skills/minimax-h3-colab/references/motion-quality.md §5); nothing measured that. This
// estimates the global camera motion of a clip from ffmpeg's grey frames: block matching between
// frames a few apart, then a robust fit of one zoom about the centre plus one translation, with the
// blocks that move unlike the rest (a character crossing the frame) dropped before the final fit.
// Summed over the clip that gives a push or pull (total zoom), a pan (horizontal travel) and a tilt
// (vertical travel), which are compared with what craft reads from the shot's `camera` field
// (tools/video/core/craft.mjs `cameraMove`). Thresholds live here so a pilot can calibrate them.
import { spawnSync } from "node:child_process";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { cameraMove } from "../core/craft.mjs";

export const THRESHOLDS = {
  // Analysis size: a 16:9 clip is read at 320x180 grey.
  width: 320,
  height: 180,
  // Frames between the two pictures of a pair (24 fps: a sixth of a second).
  stride: 4,
  block: 24,
  search: 10,
  // Blocks flatter than this (grey-level variance) carry no motion information.
  min_block_variance: 40,
  // Fraction of blocks kept after dropping the worst residuals of the first fit.
  keep_fraction: 0.7,
  // Whole-clip totals: zoom as a ratio, pan and tilt as a fraction of the frame's width/height.
  move_zoom: 0.04,
  move_travel: 0.03,
  // A locked shot may drift this much before it is reported.
  locked_zoom: 0.02,
  locked_travel: 0.015,
};

/** ffmpeg: the clip as raw grey frames at the analysis size, on stdout. */
export function greyFramesArgs(file, thresholds = THRESHOLDS) {
  return ["-v", "error", "-i", file, "-an", "-vf", `scale=${thresholds.width}:${thresholds.height}:flags=area,format=gray`, "-f", "rawvideo", "-"];
}

/** Split ffmpeg's raw grey output into frames. */
export function splitFrames(buffer, thresholds = THRESHOLDS) {
  const size = thresholds.width * thresholds.height;
  const frames = [];
  for (let offset = 0; offset + size <= buffer.length; offset += size) frames.push(buffer.subarray(offset, offset + size));
  return frames;
}

function blockVariance(frame, width, x0, y0, block) {
  let sum = 0;
  let squares = 0;
  for (let y = y0; y < y0 + block; y++) {
    for (let x = x0; x < x0 + block; x++) {
      const value = frame[y * width + x];
      sum += value;
      squares += value * value;
    }
  }
  const n = block * block;
  return squares / n - (sum / n) ** 2;
}

function sad(a, b, width, x0, y0, u, v, block) {
  let total = 0;
  for (let y = y0; y < y0 + block; y++) {
    const rowA = y * width;
    const rowB = (y + v) * width + u;
    for (let x = x0; x < x0 + block; x++) total += Math.abs(a[rowA + x] - b[rowB + x]);
  }
  return total;
}

// Sub-pixel offset of a minimum from the costs either side of it (parabola through three points).
function refine(left, centre, right) {
  const denominator = left - 2 * centre + right;
  return denominator > 0 ? Math.max(-0.5, Math.min(0.5, (left - right) / (2 * denominator))) : 0;
}

/** Where each textured block of `a` went in `b`: [{x, y, u, v}] with x, y the block centre. */
export function blockVectors(a, b, thresholds = THRESHOLDS) {
  const { width, height, block, search, min_block_variance: minVariance } = thresholds;
  const vectors = [];
  for (let y0 = search; y0 + block + search <= height; y0 += block) {
    for (let x0 = search; x0 + block + search <= width; x0 += block) {
      if (blockVariance(a, width, x0, y0, block) < minVariance) continue;
      let best = Infinity;
      let bestU = 0;
      let bestV = 0;
      const side = 2 * search + 1;
      const costs = new Float64Array(side * side);
      for (let v = -search; v <= search; v++) {
        for (let u = -search; u <= search; u++) {
          const cost = sad(a, b, width, x0, y0, u, v, block);
          costs[(v + search) * side + u + search] = cost;
          if (cost < best) {
            best = cost;
            bestU = u;
            bestV = v;
          }
        }
      }
      const at = (u, v) => costs[(v + search) * side + u + search];
      const du = Math.abs(bestU) < search ? refine(at(bestU - 1, bestV), best, at(bestU + 1, bestV)) : 0;
      const dv = Math.abs(bestV) < search ? refine(at(bestU, bestV - 1), best, at(bestU, bestV + 1)) : 0;
      vectors.push({ x: x0 + block / 2, y: y0 + block / 2, u: bestU + du, v: bestV + dv });
    }
  }
  return vectors;
}

// Least squares for u = a*(x - cx) + tx, v = a*(y - cy) + ty: one zoom and one translation.
function fitSimilarity(vectors, cx, cy) {
  const n = vectors.length;
  const mean = (pick) => vectors.reduce((total, item) => total + pick(item), 0) / n;
  const mx = mean((p) => p.x - cx);
  const my = mean((p) => p.y - cy);
  const mu = mean((p) => p.u);
  const mv = mean((p) => p.v);
  let numerator = 0;
  let denominator = 0;
  for (const p of vectors) {
    const x = p.x - cx - mx;
    const y = p.y - cy - my;
    numerator += x * (p.u - mu) + y * (p.v - mv);
    denominator += x * x + y * y;
  }
  const a = denominator > 0 ? numerator / denominator : 0;
  return { a, tx: mu - a * mx, ty: mv - a * my };
}

/** One frame pair's camera motion: scale (>1 is a push), dx and dy in analysis pixels. */
export function pairMotion(vectors, thresholds = THRESHOLDS) {
  if (vectors.length < 4) return null;
  const cx = thresholds.width / 2;
  const cy = thresholds.height / 2;
  let fit = fitSimilarity(vectors, cx, cy);
  const residual = (p) => Math.hypot(p.u - (fit.a * (p.x - cx) + fit.tx), p.v - (fit.a * (p.y - cy) + fit.ty));
  const kept = [...vectors].sort((p, q) => residual(p) - residual(q)).slice(0, Math.max(4, Math.round(vectors.length * thresholds.keep_fraction)));
  fit = fitSimilarity(kept, cx, cy);
  return { scale: 1 + fit.a, dx: fit.tx, dy: fit.ty, blocks: kept.length };
}

/** The whole clip: total zoom, and pan and tilt as fractions of the frame (content motion reversed). */
export function summarize(pairs, thresholds = THRESHOLDS) {
  const usable = pairs.filter(Boolean);
  const zoom = usable.reduce((total, pair) => total * pair.scale, 1);
  // When the camera pans right the picture slides left, so the camera's travel is minus the content's.
  const pan = -usable.reduce((total, pair) => total + pair.dx, 0) / thresholds.width;
  const tilt = -usable.reduce((total, pair) => total + pair.dy, 0) / thresholds.height;
  return { zoom, pan, tilt, pairs: usable.length };
}

/**
 * What the clip did: locked, push, pull, pan (left/right), tilt (up/down), drift or mixed (a pan
 * and a tilt together). A push or pull toward a point off the centre also slides the picture, so
 * with a clear zoom the travel is reported as `also`, not as a second move: the e030 pilot pushes
 * in on faces above the centre measured a 5% tilt with their 8% zoom.
 */
export function classify(summary, thresholds = THRESHOLDS) {
  const zoomed = Math.abs(summary.zoom - 1) >= thresholds.move_zoom;
  const panned = Math.abs(summary.pan) >= thresholds.move_travel;
  const tilted = Math.abs(summary.tilt) >= thresholds.move_travel;
  if (zoomed) {
    const also = [
      ...(panned ? [`pan ${summary.pan > 0 ? "right" : "left"}`] : []),
      ...(tilted ? [`tilt ${summary.tilt > 0 ? "down" : "up"}`] : []),
    ];
    return { move: summary.zoom > 1 ? "push" : "pull", ...(also.length ? { also } : {}) };
  }
  if (panned && tilted) return { move: "mixed" };
  if (panned) return { move: "pan", direction: summary.pan > 0 ? "right" : "left" };
  if (tilted) return { move: "tilt", direction: summary.tilt > 0 ? "down" : "up" };
  const still = Math.abs(summary.zoom - 1) < thresholds.locked_zoom
    && Math.abs(summary.pan) < thresholds.locked_travel && Math.abs(summary.tilt) < thresholds.locked_travel;
  return { move: still ? "locked" : "drift" };
}

/** The move a shot asks for, as craft reads `camera`, with a pan or tilt direction when one is named. */
export function expectedMove(shot) {
  const move = cameraMove(shot);
  const text = String(shot?.camera ?? "").toLowerCase();
  if (move === "pan") {
    const direction = /\bleft\b/.test(text) ? "left" : /\bright\b/.test(text) ? "right" : null;
    return { move, direction };
  }
  if (move === "tilt") {
    const direction = /\b(?:up|upward|rises?|crane(?:s|ing)? up)\b/.test(text) ? "up" : /\b(?:down|downward|descend(?:s|ing)?)\b/.test(text) ? "down" : null;
    return { move, direction };
  }
  return { move, direction: null };
}

/**
 * Problems with the measured move against the asked one, as short sentences ([] when it matches).
 * "none" (no move named) and "track" (moves this estimator does not model) are not judged.
 */
export function compareMove(expected, measured) {
  if (expected.move === "none" || expected.move === "track") return [];
  if (expected.move === "locked") {
    return measured.move === "locked" ? [] : [`a locked shot moved (${measured.move}${measured.direction ? ` ${measured.direction}` : ""})`];
  }
  if (measured.move !== expected.move) {
    return [`asked to ${expected.move}${expected.direction ? ` ${expected.direction}` : ""}, the clip ${measured.move === "locked" ? "stayed still" : `did ${measured.move}${measured.direction ? ` ${measured.direction}` : ""}`}`];
  }
  if (expected.direction && measured.direction && expected.direction !== measured.direction) {
    return [`asked to ${expected.move} ${expected.direction}, the clip went ${measured.direction}`];
  }
  return [];
}

/** Run ffmpeg on a clip and measure it. `shot` (with `camera`) is optional; without it nothing is compared. */
export function measureClip(file, { shot = null, thresholds = THRESHOLDS, ffmpeg = process.env.FFMPEG || "ffmpeg" } = {}) {
  const result = spawnSync(ffmpeg, greyFramesArgs(file, thresholds), { maxBuffer: 1 << 30 });
  if (result.status !== 0) throw new Error(`ffmpeg could not read ${file}: ${String(result.stderr).trim().slice(0, 300)}`);
  const frames = splitFrames(result.stdout, thresholds);
  const pairs = [];
  for (let i = 0; i + thresholds.stride < frames.length; i += thresholds.stride) {
    pairs.push(pairMotion(blockVectors(frames[i], frames[i + thresholds.stride], thresholds), thresholds));
  }
  const summary = summarize(pairs, thresholds);
  const measured = classify(summary, thresholds);
  const expected = shot ? expectedMove(shot) : null;
  return {
    frames: frames.length,
    summary: { zoom: Number(summary.zoom.toFixed(4)), pan: Number(summary.pan.toFixed(4)), tilt: Number(summary.tilt.toFixed(4)), pairs: summary.pairs },
    measured,
    expected,
    problems: expected ? compareMove(expected, measured) : [],
  };
}

// node tools/video/media/camera-motion.mjs <clip.mp4> [--camera "Close-up, slow push in"]
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const [file, ...rest] = process.argv.slice(2);
  const cameraAt = rest.indexOf("--camera");
  const shot = cameraAt >= 0 ? { camera: rest[cameraAt + 1] } : null;
  if (!file) {
    process.stderr.write("usage: camera-motion.mjs <clip.mp4> [--camera \"Medium shot, slow push in\"]\n");
    process.exit(2);
  }
  const report = measureClip(file, { shot });
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exit(report.problems.length ? 1 : 0);
}
