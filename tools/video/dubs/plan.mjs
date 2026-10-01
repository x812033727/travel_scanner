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

import { emptyLexicon } from "../core/lexicon.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, narrationLocale, spokenText, textHash } from "../core/schema.mjs";
import { FPS, SAMPLE_RATE, SAMPLES_PER_FRAME, framesFor, msToSamples } from "../core/timeline.mjs";
import { planRequests } from "../tts/requests.mjs";

export const DUB_LOCALES = LOCALES.filter((locale) => locale !== NARRATION_LOCALE);
/** The locales one video can be dubbed in: every caption locale but the one it is narrated in. */
export const dubLocales = (doc) => LOCALES.filter((locale) => locale !== narrationLocale(doc));
// The locales whose dictionary aliases may be written in Chinese characters ("P 九十五").
export const CHINESE_LOCALES = new Set(["zh-TW", "zh-CN"]);
// What gets a dub when nobody chose (no --locale, no languages.json): not zh-CN. A viewer who
// reads Simplified hears Mandarin already in the zh-TW narration, so that track adds nothing
// unless the owner ticks it for a video (the owner's call, 2026-09-28).
export const DEFAULT_DUB_LOCALES = DUB_LOCALES.filter((locale) => locale !== "zh-CN");
/** The same default for one video, whatever it is narrated in (DEFAULT_DUB_LOCALES for zh-TW). */
export const defaultDubLocales = (doc) => dubLocales(doc).filter((locale) => locale !== "zh-CN");
export const DUB_FORMATS = ["m4a", "mp3", "wav"];
export const DEFAULT_FORMAT = "m4a";
// Silence between two dubbed lines once the original pause is used up.
export const GAP_MS = 250;
// Silence kept before a window ends, so a dub never runs into the next slide's first word.
export const GUARD_MS = 100;
// The most a window is sped up before its translation must be shortened instead.
export const MAX_TEMPO = 1.15;
export const TEMPO_STEP = 0.01;
// Speaking rates, in characters of the translation per second of speech, relative to the zh-TW
// narration's own rate: what the same voice manages in each language. The zh-TW rate is measured
// from the narration itself (5.8 characters a second on the 2026-09-26 batch), so a video read
// faster or slower than usual carries that into its budgets. The rate a finished dub measured
// replaces the estimate (fit.json), so the next video's budgets are real.
export const RATE_RATIOS = { en: 2.6, ja: 1.35, ko: 1.15, "zh-CN": 1.0 };
// When the narration cannot be measured (no audio lengths in the timeline).
export const DEFAULT_RATES = { en: 15, ja: 7.8, ko: 6.7, "zh-CN": 5.8, "zh-TW": 5.8 };
// Budgets leave this much of the room unused: a translator lands close to the limit, not on it.
export const BUDGET_MARGIN = 0.97;
// What a line costs before its first word and after its last (breath, the trimmed margins, the
// final syllable's stretch): on the 2026-09-26 English dub, seconds = 0.51 + 0.055 × characters.
// Budgets take it off the room a line has, or a short line gets more characters than it can say.
export const LINE_OVERHEAD_MS = 400;

const STYLE_TAIL = "Natural rise and fall in intonation, light emphasis on key words, never flat or like reading a script. Medium-brisk pace.";
// The zh-TW style names Taiwan Mandarin; a dub keeps the manner and changes the language.
export const DUB_STYLES = {
  "zh-TW": `Relaxed, conversational tech explainer talking to a friend, in Taiwan Mandarin with a natural Taiwanese accent. ${STYLE_TAIL}`,
  en: `Relaxed, conversational tech explainer talking to a friend, in clear, natural English. ${STYLE_TAIL}`,
  ja: `Relaxed, conversational tech explainer talking to a friend, in natural standard Japanese. ${STYLE_TAIL}`,
  ko: `Relaxed, conversational tech explainer talking to a friend, in natural standard Korean. ${STYLE_TAIL}`,
  "zh-CN": `Relaxed, conversational tech explainer talking to a friend, in natural Mandarin as spoken in mainland China. ${STYLE_TAIL}`,
};

const CJK = /[぀-ヿ㐀-鿿豈-﫿ｦ-ﾟ가-힯]/u;

// Complete letter spellings of words (App → A P P, iOS → i O S) are Mandarin aliases.
// Acronyms (CBS → C B S) and partial spellings (OpenAI → Open A I) still apply elsewhere.
function spellsWord(term, say) {
  return /^[A-Za-z]{2,}$/.test(term) && /[a-z]/.test(term)
    && /^[A-Za-z](?:\s+[A-Za-z])+$/.test(say.trim())
    && say.replace(/\s/g, "").toUpperCase() === term.toUpperCase();
}

/** The narration voice with the locale's style: one Gemini voice speaks every language. */
export function dubVoice(doc, locale, style = null) {
  const { rate, lang, ...voice } = doc.voice;
  return { ...voice, style: style ?? DUB_STYLES[locale] };
}

/**
 * The dictionary outside Chinese: acronyms and partial Latin spellings still apply; CJK
 * readings and full letter spellings of mixed-case words leave the original term to the voice.
 */
export function dubLexicon(lexicon) {
  const terms = {};
  for (const [term, say] of Object.entries(lexicon?.terms ?? {})) {
    terms[term] = typeof say === "string" && !CJK.test(say) && !spellsWord(term, say) ? say : null;
  }
  return { ...(lexicon ?? {}), terms };
}

/**
 * The dictionary as the voice speaking `locale` may use it: whole for Mandarin, filtered for
 * any other language (an English narration is a dub in this sense).
 */
export function speechLexicon(lexicon, locale) {
  return CHINESE_LOCALES.has(locale) ? lexicon : dubLexicon(lexicon);
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

/**
 * What `dub` asks the voice for in `locale`: the caption translation in the dub voice, read with
 * the shelf's raw dictionary filtered by the target language (project.shelfLexicon, so a Chinese
 * dub of an English video gets its Chinese aliases back, for --file projects too). No requests
 * while a line has no current translation.
 */
export function dubRequests(project, locale, style = null) {
  const { doc: script, missing } = dubScript(project.doc, project.translations?.[locale], locale, style);
  const lexicon = speechLexicon(project.shelfLexicon ?? emptyLexicon(), locale);
  return { script, missing, lexicon, requests: missing.length ? [] : planRequests(script, lexicon) };
}

/**
 * Hash of what the voice is asked to say, line by line: each line's clip key, which binds the
 * effective voice (name, model, style) and the line's words with the aliases actually applied.
 * An alias the lines do not use, or two aliases the target language discards alike, leave it as
 * it is; another locale's changes never reach it. Computed from the plan alone: no network.
 */
export function speechFingerprint(requests) {
  const hash = createHash("sha256");
  for (const request of requests) for (const line of request.lines) hash.update(JSON.stringify([line.id, line.key]));
  return hash.digest("hex").slice(0, 16);
}

/** The fingerprint `dub` would record for `locale` now; null when it cannot be planned (no project, a missing translation, a line too long). */
export function dubFingerprint(project, locale, style = null) {
  if (!project?.doc) return null;
  try {
    const { missing, requests } = dubRequests(project, locale, style);
    return missing.length ? null : speechFingerprint(requests);
  } catch {
    return null;
  }
}

/**
 * Whether a dub record (its timeline.json, or the fit.json of a run that was over budget) was
 * made with the speech `dub` would request now, in the style it was made with (`--style`, kept as
 * style_override).
 *
 * A record from before dubs recorded a fingerprint (2026-10-01) is judged by the locale's clip
 * cache (`cache`, dubs/<locale>/audio/cache.json): current when every line `dub` would plan now
 * has the clip key it would ask for (the line's or its request's, as `dub` reuses a clip), since
 * the track was laid from those clips. No cache, an unreadable one, or one key that differs or is
 * absent leaves it stale; running `dub` again records a fingerprint and synthesizes only the lines
 * whose keys changed. The cache can run ahead of the track when a later run synthesized new clips
 * and did not finish; `legacyGuard` is false when a newer run's fit.json shows that happened.
 */
export function speechCurrent(project, locale, record, { cache = null, legacyGuard = true } = {}) {
  if (typeof record?.speech_fingerprint === "string") {
    return record.speech_fingerprint === dubFingerprint(project, locale, record.style_override ?? null);
  }
  if (!legacyGuard || !project?.doc || !cache?.lines || typeof cache.lines !== "object") return false;
  try {
    const { missing, requests } = dubRequests(project, locale, record?.style_override ?? null);
    if (missing.length || !requests.length) return false;
    return requests.every((request) => request.lines.every((line) => [line.key, request.key].includes(cache.lines[line.id])));
  } catch {
    return false;
  }
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
    // The scene rides along: check-audio batches its Jev questions per scene, for dubs too.
    lines.push({ id, scene: window.scene, start_frame: start, end_frame: end, audio_samples: samples, tempo });
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

/** Characters a second of the zh-TW narration itself, from the timeline's clip lengths; null before tts. */
export function narrationRate(doc, timeline) {
  const texts = new Map();
  for (const { line } of eachLine(doc)) texts.set(line.id, spokenText(line));
  const lengths = new Map((timeline?.lines ?? []).filter((line) => Number.isInteger(line.audio_samples)).map((line) => [line.id, line.audio_samples]));
  return measureRate(texts, lengths);
}

/** The rate to plan a locale's dub with before it is measured: the narration's own rate, scaled. */
export function defaultRate(locale, doc, timeline) {
  const anchor = timeline ? narrationRate(doc, timeline) : null;
  if (!anchor) return DEFAULT_RATES[locale];
  // The ratios were measured against a zh-TW narration; another narration language scales the
  // fixed starting rates instead.
  const narration = narrationLocale(doc);
  const ratio = narration === NARRATION_LOCALE ? RATE_RATIOS[locale] : DEFAULT_RATES[locale] / DEFAULT_RATES[narration];
  return Math.round(anchor * ratio * 100) / 100;
}

/**
 * How many characters each line's translation may have, from its own zh-TW slot, the locale's
 * rate and the speed-up a window can absorb. A guide for the translator ahead of synthesis: the
 * real fit is decided per window, where short neighbours lend their room.
 */
export function lineBudgets(timeline, rate, { gapMs = GAP_MS, maxTempo = MAX_TEMPO, overheadMs = LINE_OVERHEAD_MS } = {}) {
  const budgets = {};
  for (const line of timeline.lines) {
    const seconds = (line.end_frame - line.start_frame) / FPS - (gapMs + overheadMs) / 1000;
    budgets[line.id] = Math.max(1, Math.floor(Math.max(0, seconds) * rate * maxTempo * BUDGET_MARGIN));
  }
  return budgets;
}

/**
 * For a window that is over even at MAX_TEMPO: how many characters each of its lines may keep,
 * shrinking every line's words by the same share, so the translator knows exactly how much to
 * cut. With `lengths` (clip samples by line id) each line also carries the seconds it took: a
 * line full of numbers or currency reads far slower than its character count says, and the
 * translator should cut the words around them.
 */
export function shrinkBudgets(window, texts, { gapMs = GAP_MS, guardMs = GUARD_MS, overheadMs = LINE_OVERHEAD_MS, lengths = null } = {}) {
  const gap = gapFramesFor(gapMs);
  const overhead = framesFor(msToSamples(overheadMs));
  const limit = window.end_frame - framesFor(msToSamples(guardMs));
  const count = window.lines.length;
  const available = Math.max(1, limit - window.start_frame - gap * Math.max(0, count - 1) - overhead * count);
  const spoken = Math.max(1, window.lines.reduce((sum, line) => sum + (line.end_frame - line.start_frame), 0) - overhead * count);
  const ratio = Math.min(1, (available / spoken) * BUDGET_MARGIN);
  const over = Math.max(0, (window.lines.at(-1)?.end_frame ?? window.start_frame) - limit) / FPS;
  return window.lines.map((line) => {
    const characters = [...(texts.get(line.id) ?? "")].length;
    const entry = { id: line.id, chars: characters, max_chars: Math.max(1, Math.floor(characters * ratio)), window_over_seconds: Math.round(over * 100) / 100 };
    if (lengths?.has(line.id)) entry.seconds = Math.round((lengths.get(line.id) / SAMPLE_RATE) * 100) / 100;
    return entry;
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
