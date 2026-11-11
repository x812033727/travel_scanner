// Narration speed for the two narrated cartoon series (.agents/skills/producer/references/pace-targets.md):
// 奇聞檔案局 (curio-) and 原來如此事務所 (sothatswhy-) speak at least 4.5 characters a second, the
// reference channel measured 5.06. Gemini voices take no rate; their pace is only what the written
// style asks for, and P06 (2026-11-11) asked for 「一秒四到五個字」 and came out at 3.74. Nothing
// measured it until then, so `tts` reports it here once the takes are in.

/** The floor both series keep (owner, 2026-11-11: 「之後都調快」). */
export const PACE_MIN_CHARS_PER_SECOND = 4.5;

/** Whether a video belongs to a series that keeps PACE_MIN_CHARS_PER_SECOND. */
export const isPacedNarration = (doc) => /^(curio|sothatswhy)-/.test(doc?.slug ?? "");

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
  if (!isPacedNarration(doc)) return null;
  const pace = narrationPace(doc, timeline);
  if (!pace || pace.rate >= PACE_MIN_CHARS_PER_SECOND) return null;
  return `narration speaks ${pace.rate.toFixed(2)} characters a second (${pace.chars} characters in ${pace.seconds.toFixed(1)} s of speech); this series keeps at least ${PACE_MIN_CHARS_PER_SECOND} (pace-targets.md). Ask for a faster pace in each voice's style, then tts again; the narration goes back to the owner`;
}
