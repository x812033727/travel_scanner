// A dubbed audio track for one locale, as pure functions (docs/videos/DUBS.md): the script the
// voice reads (the caption translation), which lines share a window, where each translated clip
// goes inside it, how much a window must speed up to fit, and how many characters a translation
// may have before it cannot fit at all.
//
// The picture is timed by the zh-TW narration (core/timeline.mjs) and a dub never moves it. A
// window is one slide state: the viewer sees something new only at a reveal or a scene change,
// so inside a window the dubbed lines may shift, and at its end they must be over. Every track
// is exactly as long as the video, to the sample.
import { createHash } from "node:crypto";

import { LOCALES, NARRATION_LOCALE, textHash } from "../core/schema.mjs";
import { FPS, SAMPLE_RATE, SAMPLES_PER_FRAME, framesFor, msToSamples } from "../core/timeline.mjs";

export const DUB_LOCALES = LOCALES.filter((locale) => locale !== NARRATION_LOCALE);
export const DUB_FORMATS = ["m4a", "mp3", "wav"];
export const DEFAULT_FORMAT = "m4a";
// Silence between two dubbed lines once the original pause is used up.
export const GAP_MS = 250;
// Silence kept before a window ends, so a dub never runs into the next slide's first word.
export const GUARD_MS = 100;
// The most a window is sped up before its translation must be shortened instead.
export const MAX_TEMPO = 1.15;
export const TEMPO_STEP = 0.01;
// Starting speaking rates, in characters of the translation per second of speech. The rates a
// finished dub measured replace them (fit.json), so the second video's budgets are real.
export const DEFAULT_RATES = { en: 15, ja: 7, ko: 6, "zh-CN": 4.5 };
// Budgets leave this much of the room unused: a translator lands close to the limit, not on it.
export const BUDGET_MARGIN = 0.97;

const STYLE_TAIL = "Natural rise and fall in intonation, light emphasis on key words, never flat or like reading a script. Medium-brisk pace.";
// The zh-TW style names Taiwan Mandarin; a dub keeps the manner and changes the language.
export const DUB_STYLES = {
  en: `Relaxed, conversational tech explainer talking to a friend, in clear, natural English. ${STYLE_TAIL}`,
  ja: `Relaxed, conversational tech explainer talking to a friend, in natural standard Japanese. ${STYLE_TAIL}`,
  ko: `Relaxed, conversational tech explainer talking to a friend, in natural standard Korean. ${STYLE_TAIL}`,
  "zh-CN": `Relaxed, conversational tech explainer talking to a friend, in natural Mandarin as spoken in mainland China. ${STYLE_TAIL}`,
};

const CJK = /[぀-ヿ㐀-鿿豈-﫿가-힯]/u;

/** The narration voice with the locale's style: one Gemini voice speaks every language. */
export function dubVoice(doc, locale, style = null) {
  const { rate, lang, ...voice } = doc.voice;
  return { ...voice, style: style ?? DUB_STYLES[locale] };
}

/**
 * The dictionary a dub uses: a spoken form written in Latin letters ("A P I") applies in any
 * language; one written in Chinese ("P 九十五") does not, and that term is read as written.
 */
export function dubLexicon(lexicon) {
  const terms = {};
  for (const [term, say] of Object.entries(lexicon?.terms ?? {})) terms[term] = typeof say === "string" && !CJK.test(say) ? say : null;
  return { ...(lexicon ?? {}), terms };
}

/**
 * The video with every line's text replaced by its current translation, for the request planner:
 * a dub reads the caption translation itself, never the zh-TW spoken form. Lines whose translation
 * is missing or older than their zh-TW text are listed in `missing` and keep their zh-TW text.
 */
export function dubScript(doc, translation, locale, style = null) {
  const missing = [];
  const scenes = doc.scenes.map((scene) => ({
    ...scene,
    lines: scene.lines.map((line) => {
      const entry = translation?.lines?.[line.id];
      const text = entry && entry.source_hash === textHash(line.text) && typeof entry.text === "string" ? entry.text.trim() : "";
      if (!text) missing.push(line.id);
      const { say, say_for, ...rest } = line;
      return { ...rest, text: text || line.text };
    }),
  }));
  return { doc: { ...doc, voice: dubVoice(doc, locale, style), scenes }, missing };
}

/** Hash of the words a dub speaks, line by line; status treats a track made from other words as stale. */
export function translationHash(script) {
  const hash = createHash("sha256");
  for (const scene of script.scenes) for (const line of scene.lines) hash.update(JSON.stringify([line.id, line.text]));
  return hash.digest("hex").slice(0, 16);
}

/** The slide states of the zh-TW timeline as windows, each with the lines spoken inside it. */
export function windowsOf(timeline) {
  const windows = [];
  for (const scene of timeline.scenes) {
    scene.states.forEach((state, index) => {
      const lines = timeline.lines
        .filter((line) => line.scene === scene.id && line.start_frame >= state.start_frame && line.start_frame < state.end_frame)
        .map((line) => line.id);
      windows.push({ scene: scene.id, state: index, start_frame: state.start_frame, end_frame: state.end_frame, lines });
    });
  }
  return windows;
}

const gapFramesFor = (gapMs) => framesFor(msToSamples(gapMs));

/**
 * Lay the window's clips out in order at one tempo. With `keepStarts`, a clip waits for its zh-TW
 * line's start when the previous clip ends early, which keeps the original rhythm; without it the
 * clips pack with the minimum gap, which is how a long translation fits.
 */
export function placeLines(window, originals, lengths, { tempo = 1, gapMs = GAP_MS, keepStarts = true } = {}) {
  const gap = gapFramesFor(gapMs);
  const lines = [];
  let cursor = window.start_frame;
  for (const id of window.lines) {
    const samples = Math.max(1, Math.round(lengths.get(id) / tempo));
    const start = keepStarts ? Math.max(originals.get(id).start_frame, cursor) : cursor;
    const end = start + framesFor(samples);
    lines.push({ id, start_frame: start, end_frame: end, audio_samples: samples, tempo });
    cursor = end + gap;
  }
  return lines;
}

const lastFrame = (lines, fallback) => (lines.length ? lines.at(-1).end_frame : fallback);

/**
 * Where a window's dubbed lines go and how fast they must be spoken. The original rhythm first;
 * then packed; then packed and sped up, a hundredth at a time, up to MAX_TEMPO. Past that the
 * window is `over`: its lines are laid out at MAX_TEMPO anyway, with how many frames stick out.
 */
export function layoutWindow(window, originals, lengths, { gapMs = GAP_MS, guardMs = GUARD_MS, maxTempo = MAX_TEMPO } = {}) {
  const limit = window.end_frame - framesFor(msToSamples(guardMs));
  const result = (lines, tempo, keepStarts) => ({
    ...window,
    lines,
    tempo,
    kept_starts: keepStarts,
    over: lastFrame(lines, window.start_frame) > limit,
    slack_frames: limit - lastFrame(lines, window.start_frame),
  });
  const kept = placeLines(window, originals, lengths, { gapMs, keepStarts: true });
  if (lastFrame(kept, window.start_frame) <= limit) return result(kept, 1, true);
  let tempo = 1;
  while (tempo <= maxTempo + 1e-9) {
    const packed = placeLines(window, originals, lengths, { tempo, gapMs, keepStarts: false });
    if (lastFrame(packed, window.start_frame) <= limit) return result(packed, tempo, false);
    tempo = Math.round((tempo + TEMPO_STEP) * 100) / 100;
  }
  return result(placeLines(window, originals, lengths, { tempo: maxTempo, gapMs, keepStarts: false }), maxTempo, false);
}

/** Every window laid out; `originals` and `lengths` map line ids to the zh-TW line and the clip's samples. */
export function layoutDub(timeline, lengths, options = {}) {
  const originals = new Map(timeline.lines.map((line) => [line.id, line]));
  return windowsOf(timeline).map((window) => layoutWindow(window, originals, lengths, options));
}

/** Characters per second the voice spoke, from the clips it made of these texts (tempo 1). */
export function measureRate(texts, lengths) {
  let characters = 0;
  let samples = 0;
  for (const [id, text] of texts) {
    if (!lengths.has(id)) continue;
    characters += [...text].length;
    samples += lengths.get(id);
  }
  return samples > 0 ? Math.round(((characters * SAMPLE_RATE) / samples) * 100) / 100 : null;
}

/**
 * How many characters each line's translation may have, from its own zh-TW slot, the locale's
 * rate and the speed-up a window can absorb. A guide for the translator ahead of synthesis: the
 * real fit is decided per window, where short neighbours lend their room.
 */
export function lineBudgets(timeline, rate, { gapMs = GAP_MS, maxTempo = MAX_TEMPO } = {}) {
  const budgets = {};
  for (const line of timeline.lines) {
    const seconds = (line.end_frame - line.start_frame) / FPS - gapMs / 1000;
    budgets[line.id] = Math.max(1, Math.floor(Math.max(0, seconds) * rate * maxTempo * BUDGET_MARGIN));
  }
  return budgets;
}

/**
 * For a window that is over even at MAX_TEMPO: how many characters each of its lines may keep,
 * shrinking every line by the same share, so the translator knows exactly how much to cut.
 */
export function shrinkBudgets(window, texts, { gapMs = GAP_MS, guardMs = GUARD_MS } = {}) {
  const gap = gapFramesFor(gapMs);
  const limit = window.end_frame - framesFor(msToSamples(guardMs));
  const available = Math.max(1, limit - window.start_frame - gap * Math.max(0, window.lines.length - 1));
  const spoken = window.lines.reduce((sum, line) => sum + (line.end_frame - line.start_frame), 0);
  const ratio = Math.min(1, (available / Math.max(1, spoken)) * BUDGET_MARGIN);
  return window.lines.map((line) => {
    const characters = [...(texts.get(line.id) ?? "")].length;
    return { id: line.id, chars: characters, max_chars: Math.max(1, Math.floor(characters * ratio)) };
  });
}

/** Clip lengths a translation would take at a rate, for a dry run's estimate before any audio exists. */
export function estimatedLengths(texts, rate) {
  const lengths = new Map();
  for (const [id, text] of texts) lengths.set(id, Math.max(SAMPLES_PER_FRAME, Math.round(([...text].length / rate) * SAMPLE_RATE)));
  return lengths;
}

/**
 * The whole track: every clip at its frame, silence everywhere else, as many samples as the
 * video has frames times 1,600. A clip longer than its slot is a bug in the layout, not something
 * to trim quietly.
 */
export function assembleTrack(totalFrames, lines, clips) {
  const track = new Int16Array(totalFrames * SAMPLES_PER_FRAME);
  for (const line of lines) {
    const clip = clips.get(line.id);
    if (!clip) throw new Error(`no clip for line ${line.id}`);
    const start = line.start_frame * SAMPLES_PER_FRAME;
    const span = (line.end_frame - line.start_frame) * SAMPLES_PER_FRAME;
    if (clip.length > span) throw new Error(`clip ${line.id} has ${clip.length} samples, its slot ${span}`);
    if (start + clip.length > track.length) throw new Error(`clip ${line.id} runs past the end of the video`);
    track.set(clip, start);
  }
  return track;
}
