// Cut one synthesized scene back into its sentences.
//
// The pipeline sends a scene's lines in one request with a fixed break between them, because
// separately synthesized sentences each start their intonation afresh and sound like a list being
// read. The server returns audio only, so the sentence boundaries are found here: the breaks are
// the longest silences. If the pieces do not look like the text (a sentence much shorter or longer
// than its share of the characters), the caller falls back to one request per line.
import { SAMPLE_RATE } from "../core/timeline.mjs";

export const WINDOW = SAMPLE_RATE / 100; // 10 ms
// RMS below this is silence. Azure renders breaks as near digital silence.
export const SILENCE_RMS = 120;
// Shortest silence taken as a sentence break; the requested break is 800 ms.
export const MIN_BREAK_MS = 450;
export const MARGIN_MS = 40;

function windowRms(samples, start) {
  let sum = 0;
  const end = Math.min(samples.length, start + WINDOW);
  for (let index = start; index < end; index++) sum += samples[index] * samples[index];
  return Math.sqrt(sum / Math.max(1, end - start));
}

/** Runs of silence at least `minMs` long, as sample ranges. */
export function silenceRuns(samples, { minMs = MIN_BREAK_MS, threshold = SILENCE_RMS } = {}) {
  const minWindows = Math.ceil(minMs / 10);
  const runs = [];
  let runStart = -1;
  const windows = Math.ceil(samples.length / WINDOW);
  for (let window = 0; window <= windows; window++) {
    const silent = window < windows && windowRms(samples, window * WINDOW) < threshold;
    if (silent && runStart < 0) runStart = window;
    if (!silent && runStart >= 0) {
      if (window - runStart >= minWindows) runs.push({ start: runStart * WINDOW, end: Math.min(samples.length, window * WINDOW) });
      runStart = -1;
    }
  }
  return runs;
}

/**
 * Split into `count` pieces at the `count - 1` longest inner silences, cutting at their middles.
 * Returns null when there are not enough silences to cut at.
 */
export function splitAtSilences(samples, count, options = {}) {
  if (count <= 1) return [{ start: 0, end: samples.length }];
  const inner = silenceRuns(samples, options).filter((run) => run.start > 0 && run.end < samples.length);
  if (inner.length < count - 1) return null;
  const chosen = [...inner]
    .sort((a, b) => b.end - b.start - (a.end - a.start))
    .slice(0, count - 1)
    .sort((a, b) => a.start - b.start);
  const cuts = chosen.map((run) => Math.round((run.start + run.end) / 2));
  const edges = [0, ...cuts, samples.length];
  return edges.slice(1).map((end, index) => ({ start: edges[index], end }));
}

/** Drop leading and trailing silence, keeping a small margin so no consonant is clipped. */
export function trimSilence(samples, { marginMs = MARGIN_MS, threshold = SILENCE_RMS } = {}) {
  const windows = Math.ceil(samples.length / WINDOW);
  let first = 0;
  while (first < windows && windowRms(samples, first * WINDOW) < threshold) first++;
  if (first === windows) return samples.slice(0, 0);
  let last = windows - 1;
  while (last > first && windowRms(samples, last * WINDOW) < threshold) last--;
  const margin = Math.round((marginMs / 1000) * SAMPLE_RATE);
  const start = Math.max(0, first * WINDOW - margin);
  const end = Math.min(samples.length, (last + 1) * WINDOW + margin);
  return samples.slice(start, end);
}

/**
 * Whether the pieces are shaped like the text: each piece's share of the speech against its
 * sentence's share of the spoken weight, within a factor of about two.
 */
export function plausibleSplit(lengths, weights, { low = 0.45, high = 2.2 } = {}) {
  if (lengths.length !== weights.length || lengths.some((length) => length <= 0)) return false;
  const totalLength = lengths.reduce((sum, value) => sum + value, 0);
  const totalWeight = weights.reduce((sum, value) => sum + value, 0);
  return lengths.every((length, index) => {
    const ratio = length / totalLength / (weights[index] / totalWeight);
    return ratio >= low && ratio <= high;
  });
}
