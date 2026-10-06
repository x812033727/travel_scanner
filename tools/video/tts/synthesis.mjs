// From one request to one clip per line, and from clips to the frame-aligned narration.
//
// An answer may say when each written unit of its text was spoken (`timing`: an Azure voice's
// word boundaries from POST /video/speech/align, tts/client.mjs synthesizeAligned), relative to
// that answer's audio. Each line keeps the units that are provably its own, shifted to its own
// clip, so its CC cues can start on the spoken character (core/captions.mjs); a line whose units
// cannot be told apart gets no timing and its captions keep their estimate. The timing is derived
// from the audio, never an input: no request, clip key or speech hash depends on it.
import { SAMPLES_PER_FRAME, samplesToMs } from "../core/timeline.mjs";
import { plausibleSplit, splitAtSilences, trimSilence } from "./split.mjs";
import { concatSamples, parseWav, requireNarrationFormat } from "./wav.mjs";

// The written units the server times (apps/api/app/video_speech/align.py units_of), in text
// order: a part read through an alias is one unit, its written text; otherwise a Latin word or
// number is one, whitespace is none, and any other character is one.
const LATIN = /[A-Za-z0-9][A-Za-z0-9.+#'_%-]*/y;
// A unit holding a letter or a number is heard. The server times punctuation only by filling the
// gap between its neighbours, so a mark may sit in the silence on either side of a clip.
const SPOKEN = /[\p{L}\p{N}]/u;
// How far outside its line's clip a heard unit may start and still be the line's: a line's first
// unit can start a little before the trimmed edge when its onset is quiet, while a unit spoken in a
// neighbour's clip starts beyond the silence between them (split.mjs cuts in silences of at least
// 450 ms and keeps 40 ms of margin a side, so about 185 ms or more outside).
const OUTSIDE_MS = 100;

function writtenUnits(parts) {
  const units = [];
  for (const part of parts) {
    const text = String(part.text ?? "");
    if (part.alias) {
      units.push(text);
      continue;
    }
    for (let position = 0; position < text.length; ) {
      LATIN.lastIndex = position;
      const latin = LATIN.exec(text);
      if (latin) {
        units.push(latin[0]);
        position = LATIN.lastIndex;
        continue;
      }
      const char = String.fromCodePoint(text.codePointAt(position));
      position += char.length;
      if (!/\s/u.test(char)) units.push(char);
    }
  }
  return units;
}

/** Where `clip`, which trimSilence cut from `audio`, starts in it (in samples); null when it is not there. */
function startOf(audio, clip) {
  const loud = clip.findIndex((sample) => sample !== 0);
  if (loud < 0) return null;
  for (let start = 0; start + clip.length <= audio.length; start++) {
    if (audio[start + loud] !== clip[loud]) continue;
    let index = 0;
    while (index < clip.length && audio[start + index] === clip[index]) index++;
    if (index === clip.length) return start;
  }
  return null;
}

/**
 * Each line's timing relative to its own clip, from the `timing` of the answer that carried the
 * lines. The units the server timed must be exactly the units of the request's text, in order;
 * each line then takes its own run of them (text order is what tells two lines apart) and moves
 * them to where its clip starts in that answer: `placed[i]` is line i's clip and the `audio` it
 * was cut from, which starts at `base` samples into the answer. A line gets no timing when its
 * clip cannot be found there or a heard unit of it starts outside the clip; nothing is guessed.
 */
function lineTimings(lines, placed, timing) {
  const timings = new Map();
  const chars = timing?.chars;
  if (!Array.isArray(chars) || !chars.length) return timings;
  const units = lines.map((line) => writtenUnits(line.parts));
  const all = units.flat();
  if (all.length !== chars.length || all.some((text, index) => text !== chars[index]?.text)) return timings;
  let next = 0;
  lines.forEach((line, index) => {
    const own = chars.slice(next, next + units[index].length);
    next += units[index].length;
    const { audio, clip, base } = placed[index];
    const within = own.length ? startOf(audio, clip) : null;
    if (within === null) return;
    const shift = samplesToMs(base + within);
    const length = Math.floor(samplesToMs(clip.length));
    if (own.some((char) => SPOKEN.test(char.text) && (char.start_ms - shift < -OUTSIDE_MS || char.start_ms - shift > length + OUTSIDE_MS))) return;
    const clamp = (ms) => Math.min(length, Math.max(0, Math.round(ms - shift)));
    timings.set(line.id, {
      source: timing.source,
      model: timing.model,
      chars: own.map((char) => ({ text: char.text, start_ms: clamp(char.start_ms), end_ms: Math.max(clamp(char.start_ms), clamp(char.end_ms)) })),
    });
  });
  return timings;
}

/**
 * Synthesize a request and cut it into its lines. When the silences do not give pieces shaped
 * like the text, every line of the request is synthesized on its own instead.
 * `synthesize(body)` resolves to { wav, billable }, and `timing` when the server measured when
 * each written unit was spoken. Resolves to { clips, timings, billable, fallback }: `timings` maps
 * the id of a line whose units are provably its own to its timing, relative to its clip.
 */
export async function synthesizeRequest(request, synthesize) {
  const whole = await synthesize(request.body);
  const samples = requireNarrationFormat(parseWav(whole.wav));
  let billable = whole.billable;
  if (request.lines.length === 1) {
    const clip = trimSilence(samples);
    const timings = lineTimings(request.lines, [{ audio: samples, clip, base: 0 }], whole.timing);
    return { clips: new Map([[request.lines[0].id, clip]]), timings, billable, fallback: false };
  }
  const ranges = splitAtSilences(samples, request.lines.length);
  const pieces = ranges?.map((range) => trimSilence(samples.slice(range.start, range.end)));
  if (pieces && plausibleSplit(pieces.map((piece) => piece.length), request.lines.map((line) => line.weight))) {
    const placed = pieces.map((clip, index) => ({ audio: samples.subarray(ranges[index].start, ranges[index].end), clip, base: ranges[index].start }));
    return { clips: new Map(request.lines.map((line, index) => [line.id, pieces[index]])), timings: lineTimings(request.lines, placed, whole.timing), billable, fallback: false };
  }
  // The whole answer is set aside, and its timing with it: each line brings its own.
  const single = await synthesizeLines(request, request.lines, synthesize);
  return { clips: single.clips, timings: single.timings, billable: billable + single.billable, fallback: true };
}

/** The request body for one of a request's lines on its own. */
export function lineBody(request, line) {
  return { ...request.body, segments: [{ parts: line.parts, break_after_ms: 0 }] };
}

/**
 * Each line on a request of its own: the fallback for a bad split, and how `tts --redo` retakes
 * lines. Resolves to { clips, timings, billable }, `timings` as for synthesizeRequest.
 */
export async function synthesizeLines(request, lines, synthesize) {
  const clips = new Map();
  const timings = new Map();
  let billable = 0;
  for (const line of lines) {
    const single = await synthesize(lineBody(request, line));
    billable += single.billable;
    const samples = requireNarrationFormat(parseWav(single.wav));
    const clip = trimSilence(samples);
    clips.set(line.id, clip);
    for (const [id, timing] of lineTimings([line], [{ audio: samples, clip, base: 0 }], single.timing)) timings.set(id, timing);
  }
  return { clips, timings, billable };
}

/** Each line's clip followed by silence up to its end frame: the whole narration, frame-exact. */
export function buildNarration(timeline, clips) {
  const parts = [];
  let position = 0;
  for (const line of timeline.lines) {
    const clip = clips.get(line.id);
    if (!clip) throw new Error(`no clip for line ${line.id}`);
    if (clip.length !== line.audio_samples) throw new Error(`clip ${line.id} has ${clip.length} samples, the timeline expects ${line.audio_samples}`);
    if (!Number.isSafeInteger(line.start_frame) || line.start_frame < position) throw new Error(`line ${line.id} overlaps the preceding audio`);
    if (line.start_frame > position) parts.push(new Int16Array((line.start_frame - position) * SAMPLES_PER_FRAME));
    const span = (line.end_frame - line.start_frame) * SAMPLES_PER_FRAME;
    parts.push(clip, new Int16Array(span - clip.length));
    position = line.end_frame;
  }
  if (!Number.isSafeInteger(timeline.total_frames) || timeline.total_frames < position) throw new Error("the narration timeline ends before its audio");
  if (timeline.total_frames > position) parts.push(new Int16Array((timeline.total_frames - position) * SAMPLES_PER_FRAME));
  return concatSamples(parts);
}

/** Line ids flagged on the audio review page: { flags: [...] }, a bare array, or { lines: { id: true } }. */
export function flaggedLines(json) {
  if (Array.isArray(json)) return new Set(json.map(String));
  if (Array.isArray(json?.flags)) return new Set(json.flags.map(String));
  if (json?.lines && typeof json.lines === "object") return new Set(Object.entries(json.lines).filter(([, flagged]) => flagged).map(([id]) => id));
  throw new Error("flags file must be { flags: [line ids] }");
}
