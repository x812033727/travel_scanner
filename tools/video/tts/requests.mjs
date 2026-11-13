// What to ask the narration server for: one request per scene, or per run of lines when a scene is
// longer than the server takes at once or (in a drama) the voice changes, with dictionary terms
// marked by their spoken forms.
import { createHash } from "node:crypto";

import { channelAccent } from "../core/accent.mjs";
import { NARRATOR, voiceFor } from "../core/drama.mjs";
import { substitutions, termPattern } from "../core/lexicon.mjs";
import { spokenText } from "../core/schema.mjs";
import { spokenUnits } from "../core/timeline.mjs";

// Mirrors MAX_REQUEST_CHARACTERS in apps/api/app/video_speech/admin_api.py.
export const MAX_REQUEST_CHARACTERS = 1500;
// The break between sentences inside one request: long enough to find, and trimmed away afterwards
// (the timeline adds each line's own pause).
export const SPLIT_BREAK_MS = 800;
const CJK = /[㐀-䶿一-鿿豈-﫿]/gu;

/**
 * The text as parts, with each dictionary term that has a spoken form carrying it as `alias`.
 * Terms match whole words only, longest first, so "Claude Code" wins over "Claude" and "API"
 * inside "APIs" is left alone (termPattern).
 */
export function spokenParts(text, lexicon) {
  const entries = substitutions(lexicon);
  const pattern = termPattern(entries);
  if (!pattern) return [{ text }];
  const spoken = new Map(entries);
  const parts = [];
  let last = 0;
  for (const match of text.matchAll(pattern)) {
    if (match.index > last) parts.push({ text: text.slice(last, match.index) });
    parts.push({ text: match[0], alias: spoken.get(match[0]) });
    last = match.index + match[0].length;
  }
  if (last < text.length) parts.push({ text: text.slice(last) });
  return parts;
}

const partsLength = (parts) => parts.reduce((sum, part) => sum + part.text.length, 0);

// Mirrors VOICE_PREFIX and LONG_PAUSE_FROM_MS in apps/api/app/video_speech/gemini.py.
export const GEMINI_VOICE_PREFIX = "gemini:";
const LONG_PAUSE_FROM_MS = 600;
// Mirrors VOICE_PREFIX, PAUSE_MIN_MS and PAUSE_MAX_MS in apps/api/app/video_speech/minimax.py.
export const MINIMAX_VOICE_PREFIX = "minimax:";
const MINIMAX_PAUSE_MIN_MS = 10;
const MINIMAX_PAUSE_MAX_MS = 99_990;

/**
 * The voice part of a request body. Azure takes a voice name and a rate; Gemini takes a
 * prefixed voice, a written style and optionally a model, and no rate (its pace is in the style).
 * The style goes out with the channel's accent wording (core/accent.mjs): a stored style that
 * still says 「台灣國語」 is rewritten here, so the clip key changes and the clip is recorded again.
 */
export function voiceFields(voice) {
  if (voice.provider === "gemini") {
    return {
      voice: `${GEMINI_VOICE_PREFIX}${voice.name}`,
      ...(voice.style ? { style: channelAccent(voice.style) } : {}),
      ...(voice.model ? { model: voice.model } : {}),
    };
  }
  if (voice.provider === "minimax") {
    return { voice: `${MINIMAX_VOICE_PREFIX}${voice.name}`, rate: voice.rate ?? "+0%", ...(voice.model ? { model: voice.model } : {}) };
  }
  return { voice: voice.name, rate: voice.rate ?? "+0%" };
}

/**
 * The text the server sends MiniMax (minimax.py speech_text); its length is what the MiniMax
 * month counts. Markup characters are dropped, half-width parentheses become full-width, and a
 * pause marker goes only between two segments that have something to say.
 */
export function minimaxText(segments) {
  const spoken = segments
    .map((segment) => ({ segment, text: segment.parts.map((part) => (part.alias || part.text).replace(/[<>#]/g, " ").replaceAll("(", "（").replaceAll(")", "）")).join("").trim() }))
    .filter((entry) => entry.text);
  return spoken
    .map(({ segment, text }, index) => {
      if (index === spoken.length - 1 || !(segment.break_after_ms > 0)) return text;
      const ms = Math.min(MINIMAX_PAUSE_MAX_MS, Math.max(MINIMAX_PAUSE_MIN_MS, segment.break_after_ms));
      return `${text}<#${(ms / 1000).toFixed(2)}#>`;
    })
    .join("");
}

/** The transcript the server sends Gemini; its length is what the Gemini month counts. */
export function geminiText(segments) {
  let text = "";
  for (const segment of segments) {
    for (const part of segment.parts) text += (part.alias || part.text).replace(/[<>]/g, " ");
    if (segment.break_after_ms >= LONG_PAUSE_FROM_MS) text += " <long pause> ";
    else if (segment.break_after_ms > 0) text += " <short pause> ";
  }
  return text.trim();
}

/** Local post-synthesis speedup factor (`> 1`), or `null` when omitted or `1` (wire body stays unchanged). */
export const effectiveTempo = (voice) => (typeof voice?.tempo === "number" && voice.tempo > 1 ? voice.tempo : null);

/**
 * Every request for a video, in narration order. A request carries one voice: a scene is cut
 * where it outgrows the server's limit and where the speaker or the effective voice changes
 * (`voiceFor` folds the narration's performance plan and a line's emotion into a Gemini style;
 * Azure voices ignore both, and lint warns). A slides video has one voice and no speakers, so
 * without a plan or a cue its requests and clip keys are what they always were; a line with a
 * cue takes a style of its own, so it is a request and a take of its own.
 */
export function planRequests(doc, lexicon) {
  const requests = [];
  const originals = new Map();
  for (const scene of doc.scenes) {
    let chunk = [];
    let characters = 0;
    let fields = null;
    let speaker = null;
    let tempo = null;
    const flush = () => {
      if (!chunk.length) return;
      const segments = chunk.map((line, index) => ({ parts: line.parts, break_after_ms: index < chunk.length - 1 ? SPLIT_BREAK_MS : 0 }));
      const body = { ...fields, segments };
      const key = createHash("sha256").update(JSON.stringify(tempo ? [chunk.map((line) => line.id), body, tempo] : [chunk.map((line) => line.id), body])).digest("hex").slice(0, 16);
      requests.push({ id: `${scene.id}#${requests.filter((request) => request.scene === scene.id).length}`, scene: scene.id, speaker, lines: chunk, body, key, ...(tempo ? { tempo } : {}) });
      chunk = [];
      characters = 0;
    };
    for (const line of scene.lines) {
      const parts = spokenParts(spokenText(line), lexicon);
      const length = partsLength(parts);
      if (length > MAX_REQUEST_CHARACTERS) throw new Error(`line ${line.id} has ${length} characters; the server takes ${MAX_REQUEST_CHARACTERS} at once`);
      const resolved = voiceFor(doc, line);
      const voice = voiceFields(resolved);
      const lineTempo = effectiveTempo(resolved);
      const lineSpeaker = line.speaker ?? NARRATOR;
      const canonical = parts.map((part) => part.alias || part.text).join("").normalize("NFC").trim();
      if (line.audio_ref !== undefined) {
        const original = originals.get(line.audio_ref);
        if (!original || original.reference || original.speaker !== lineSpeaker || original.canonical !== canonical || JSON.stringify(original.voice) !== JSON.stringify(voice) || (original.tempo ?? null) !== lineTempo) throw new Error(`line ${line.id}: audio_ref must name an earlier original take with identical speaker, spoken content and effective voice`);
        flush();
        const key = createHash("sha256").update(JSON.stringify(lineTempo ? [voice, parts, lineTempo] : [voice, parts])).digest("hex").slice(0, 16);
        requests.push({ id: `${scene.id}#ref-${line.id}`, scene: scene.id, speaker: lineSpeaker, audio_ref: line.audio_ref, lines: [{ id: line.id, parts, weight: Math.max(1, spokenUnits(spokenText(line))), key }], body: { ...voice, segments: [{ parts, break_after_ms: 0 }] }, key, ...(lineTempo ? { tempo: lineTempo } : {}) });
        originals.set(line.id, { reference: true });
        continue;
      }
      originals.set(line.id, { speaker: lineSpeaker, canonical, voice, ...(lineTempo ? { tempo: lineTempo } : {}) });
      if (characters + length > MAX_REQUEST_CHARACTERS || lineSpeaker !== speaker || lineTempo !== tempo || JSON.stringify(voice) !== JSON.stringify(fields)) flush();
      fields = voice;
      speaker = lineSpeaker;
      tempo = lineTempo;
      // A clip stays current while its own words and the voice stay the same, whatever its
      // neighbours do, so an edit to one line retakes that line alone.
      const key = createHash("sha256").update(JSON.stringify(lineTempo ? [voice, parts, lineTempo] : [voice, parts])).digest("hex").slice(0, 16);
      chunk.push({ id: line.id, parts, weight: Math.max(1, spokenUnits(spokenText(line))), key });
      characters += length;
    }
    flush();
  }
  return requests;
}

/**
 * Billable characters the server will count for a request: for Azure its SSML inside <voice>,
 * for Gemini and MiniMax the characters of the text they are sent.
 */
export function billableForRequest(body) {
  if (body.voice.startsWith(GEMINI_VOICE_PREFIX)) return geminiText(body.segments).length;
  if (body.voice.startsWith(MINIMAX_VOICE_PREFIX)) return minimaxText(body.segments).length;
  let markup = 0;
  for (const segment of body.segments) {
    for (const part of segment.parts) {
      const text = part.text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      markup += part.alias ? `<sub alias="${part.alias}">${text}</sub>`.length + (part.alias.match(CJK)?.length ?? 0) : text.length;
      markup += text.match(CJK)?.length ?? 0;
    }
    if (segment.break_after_ms) markup += `<break time="${segment.break_after_ms}ms"/>`.length;
  }
  if (body.rate && !["+0%", "-0%"].includes(body.rate)) markup += `<prosody rate="${body.rate}"></prosody>`.length;
  if (!body.voice.startsWith("zh-TW-")) markup += '<lang xml:lang="zh-TW"></lang>'.length;
  return markup;
}
