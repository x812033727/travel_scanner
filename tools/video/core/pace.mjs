// Narration speed for the two narrated cartoon series (.agents/skills/producer/references/pace-targets.md):
// 奇聞檔案局 (curio-) and 原來如此事務所 (sothatswhy-) speak fast (PACE_FLOORS below); the reference
// channel measured 5.06 characters a second. Gemini voices take no rate; their pace is only what the written
// style asks for, and P06 (2026-11-11) asked for 「一秒四到五個字」 and came out at 3.74. Nothing
// measured it until then, so `tts` reports it here once the takes are in.

/**
 * The floor each series keeps, by slug prefix (owner, 2026-11-11: 「之後都調快」). 奇聞檔案局 keeps the
 * 4.5 of pace-targets.md. 原來如此事務所's owner heard three styles of the same P06 script (3.74,
 * 4.39 and 4.95 characters a second) and chose the 4.39 one, so its floor is 4.3: that style passes
 * with room for one episode's spread, and the 3.74 it replaced is still warned.
 */
export const PACE_FLOORS = Object.freeze({ curio: 4.5, sothatswhy: 4.3 });
export const PACE_MIN_CHARS_PER_SECOND = PACE_FLOORS.curio;

const seriesOf = (doc) => /^(curio|sothatswhy)-/.exec(doc?.slug ?? "")?.[1] ?? null;

/** Whether a video belongs to a series with a floor in PACE_FLOORS. */
export const isPacedNarration = (doc) => seriesOf(doc) !== null;

/** The floor a video's series keeps, or null. */
export const paceFloor = (doc) => PACE_FLOORS[seriesOf(doc)] ?? null;

// Han characters only, as the episodes' build_scenes.py counts them: punctuation, Latin words and
// digits are left out, so a line full of numbers does not look faster than it is.
const HAN = /[㐀-䶿一-鿿豈-﫿]/g;

/** Han characters in a piece of narration. */
export const hanCount = (text) => (String(text ?? "").match(HAN) ?? []).length;

/**
 * Characters a second of the recorded narration: the Han characters of every line the timeline
 * carries, over the seconds of audio recorded for them (`audio_samples`), so pauses between lines
 * and scenes do not count. Returns null when nothing is recorded yet.
 */
export function narrationPace(doc, timeline) {
  const sampleRate = timeline?.sample_rate;
  if (!sampleRate || !Array.isArray(timeline?.lines)) return null;
  const text = new Map();
  for (const scene of doc?.scenes ?? []) for (const line of scene.lines ?? []) text.set(line.id, line.text);
  let chars = 0;
  let samples = 0;
  for (const line of timeline.lines) {
    if (!line.audio_samples || !text.has(line.id)) continue;
    chars += hanCount(text.get(line.id));
    samples += line.audio_samples;
  }
  if (!samples || !chars) return null;
  const seconds = samples / sampleRate;
  return { chars, seconds, rate: chars / seconds };
}

/**
 * The warning `tts` prints for a paced series spoken slower than the floor, or null. It never
 * fails the run: the narration may already be approved, and the fix (a faster written style, then
 * tts again) re-records and goes back to the owner.
 */
export function paceWarning(doc, timeline) {
  const floor = paceFloor(doc);
  if (floor === null) return null;
  const pace = narrationPace(doc, timeline);
  if (!pace || pace.rate >= floor) return null;
  return `narration speaks ${pace.rate.toFixed(2)} characters a second (${pace.chars} characters in ${pace.seconds.toFixed(1)} s of speech); this series keeps at least ${floor} (pace-targets.md). Ask for a faster pace in each voice's style, then tts again; the narration goes back to the owner`;
}
