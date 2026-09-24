// From one request to one clip per line, and from clips to the frame-aligned narration.
import { SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import { plausibleSplit, splitAtSilences, trimSilence } from "./split.mjs";
import { concatSamples, parseWav, requireNarrationFormat } from "./wav.mjs";

/**
 * Synthesize a request and cut it into its lines. When the silences do not give pieces shaped
 * like the text, every line of the request is synthesized on its own instead.
 * `synthesize(body)` resolves to { wav, billable }.
 */
export async function synthesizeRequest(request, synthesize) {
  const whole = await synthesize(request.body);
  const samples = requireNarrationFormat(parseWav(whole.wav));
  let billable = whole.billable;
  if (request.lines.length === 1) {
    return { clips: new Map([[request.lines[0].id, trimSilence(samples)]]), billable, fallback: false };
  }
  const ranges = splitAtSilences(samples, request.lines.length);
  const pieces = ranges?.map((range) => trimSilence(samples.slice(range.start, range.end)));
  if (pieces && plausibleSplit(pieces.map((piece) => piece.length), request.lines.map((line) => line.weight))) {
    return { clips: new Map(request.lines.map((line, index) => [line.id, pieces[index]])), billable, fallback: false };
  }
  const single = await synthesizeLines(request, request.lines, synthesize);
  return { clips: single.clips, billable: billable + single.billable, fallback: true };
}

/** The request body for one of a request's lines on its own. */
export function lineBody(request, line) {
  return { ...request.body, segments: [{ parts: line.parts, break_after_ms: 0 }] };
}

/** Each line on a request of its own: the fallback for a bad split, and how `tts --redo` retakes lines. */
export async function synthesizeLines(request, lines, synthesize) {
  const clips = new Map();
  let billable = 0;
  for (const line of lines) {
    const single = await synthesize(lineBody(request, line));
    billable += single.billable;
    clips.set(line.id, trimSilence(requireNarrationFormat(parseWav(single.wav))));
  }
  return { clips, billable };
}

/** Each line's clip followed by silence up to its end frame: the whole narration, frame-exact. */
export function buildNarration(timeline, clips) {
  const parts = [];
  for (const line of timeline.lines) {
    const clip = clips.get(line.id);
    if (!clip) throw new Error(`no clip for line ${line.id}`);
    if (clip.length !== line.audio_samples) throw new Error(`clip ${line.id} has ${clip.length} samples, the timeline expects ${line.audio_samples}`);
    const span = (line.end_frame - line.start_frame) * SAMPLES_PER_FRAME;
    parts.push(clip, new Int16Array(span - clip.length));
  }
  return concatSamples(parts);
}

/** Line ids flagged on the audio review page: { flags: [...] }, a bare array, or { lines: { id: true } }. */
export function flaggedLines(json) {
  if (Array.isArray(json)) return new Set(json.map(String));
  if (Array.isArray(json?.flags)) return new Set(json.flags.map(String));
  if (json?.lines && typeof json.lines === "object") return new Set(Object.entries(json.lines).filter(([, flagged]) => flagged).map(([id]) => id));
  throw new Error("flags file must be { flags: [line ids] }");
}
