// The caption bar of a Short lit group by group as the phrase is spoken (docs/videos/SHORTS.md
// §工具端, "karaoke"). Nothing here touches a browser or ffmpeg: from a phrase's text and the PCM
// of its clip this module decides the caption's lines, the groups a line is lit in, how long each
// group is lit, and the sequence of states motion.mjs lays over the card as its own overlay.
//
// The timing is ESTIMATED: the speech server returns audio only, so a group's start is its share
// of the spoken weight inside the span where the clip is not silent. timing.json says so
// (`source: "estimated"`); the alignment ticket replaces the estimate with measured character
// times in the same shape, and the quality check carries a warning until then.
import { measure, wrapCue } from '../core/captions.mjs';
import { SAMPLE_RATE, spokenUnits } from '../core/timeline.mjs';
import { PROFILE } from './core.mjs';

// Folded into the build id through build.mjs's code hash: a change here is another cut.
export const KARAOKE_VERSION = 'shorts-karaoke-v1';
export const CAPTION_STYLES = Object.freeze(['plain', 'karaoke']);
// Plain until the owner has seen a karaoke sample: a Short the worker makes is approved on the
// site without anyone watching it (docs/videos/SHORTS.md §自動品管).
export const DEFAULT_CAPTIONS = 'plain';
export const CAPTIONS_ENV = 'VIDEO_SHORTS_CAPTIONS';
// The caption box of core.mjs sceneHtml: the layer is drawn and clipped to exactly this box.
export const CAPTION_BOX = Object.freeze({ x: 80, y: 1430, width: 820, height: 165 });
// A line of the box: 820 px minus 20 px of padding a side holds 15 full-width glyphs of 49 px
// (16 would be 784 px); two lines fit the 165 px box at line-height 1.36. The schema's 38
// characters a phrase was never the real limit: the layout measurement of build.mjs is.
export const CAPTION_RULES = Object.freeze({ maxChars: 15, maxLines: 2, maxCps: 9, words: false });
// A lit group is 5–10 display units: one group lights a short line, a long line lights in two or
// three, so the eye follows the voice without a flash every character.
export const GROUP_MAX = 10;
export const GROUP_MIN = 5;
// A state shorter than this is folded into the one before it: two frames is the least a change
// of colour reads as a change and not a flicker.
export const MIN_STATE_FRAMES = 2;
// How the silence at the clip's edges is found: 10 ms windows, a window counts as speech when
// its RMS is above the floor (the server's silence is near digital, as split.mjs knows) and above
// a fiftieth of the loudest window (a noisy clip still finds its edges), three windows in a row.
export const WINDOW_MS = 10;
export const SPEECH_FLOOR_RMS = 120;
export const SPEECH_PEAK_SHARE = 0.02;
export const SPEECH_WINDOWS = 3;
export const SPEECH_LEAD_MS = 30;
export const SPEECH_TAIL_MS = 60;

const CLAUSE_END = /[，。！？；：、,.!?;:]$/u;
const PUNCTUATION = /[，。！？；：、,.!?;:]/gu;
// A Latin word or a number is one token (never lit in two halves); everything else is a character.
const TOKEN = /[A-Za-z0-9][A-Za-z0-9.+#'_%-]*|\s+|./gsu;
// What may not start a group: closing punctuation and brackets stay with the token before them.
const CLOSING = /^[，。！？；：、,.!?;:）」』〉》】〕\])…—～~]+$/u;
// What may not end a group: an opening bracket or quote goes with the token after it.
const OPENING = /^[（「『〈《【〔(\[]+$/u;

/** The pieces of a line a group boundary may fall between. */
export function tokens(text) {
  const out = [];
  let opening = '';
  for (const part of String(text).match(TOKEN) ?? []) {
    if (OPENING.test(part)) {
      opening += part;
      continue;
    }
    const token = opening + part;
    opening = '';
    if ((CLOSING.test(part) || !part.trim()) && out.length) out[out.length - 1] += token;
    else out.push(token);
  }
  if (opening) {
    if (out.length) out[out.length - 1] += opening;
    else out.push(opening);
  }
  return out;
}

/** The lines of the caption box, decided once so the card and the layer break alike. */
export function captionLines(text) {
  const clean = String(text).trim();
  if (!clean) return [];
  return wrapCue(clean, CAPTION_RULES).split('\n').map((line) => line.trim()).filter(Boolean);
}

/** The spoken weight of a piece of text: what captions.mjs shares a line's time by. */
export function weightOf(text) {
  return Math.max(1, spokenUnits(text)) + (String(text).match(PUNCTUATION)?.length ?? 0) * 0.5;
}

const width = (text) => measure(text, CAPTION_RULES);

/**
 * Cut one line into the groups it is lit in: as few as the width allows, as even as possible,
 * preferring to end a group where a clause ends. Each group is a run of whole tokens.
 */
export function groupLine(line) {
  const parts = tokens(line);
  if (!parts.length) return [];
  const total = width(line);
  const count = Math.max(1, Math.ceil(total / GROUP_MAX));
  if (count === 1 || parts.length === 1) return [line];
  const groups = Math.min(count, parts.length);
  const target = total / groups;
  const piece = (from, to) => parts.slice(from, to).join('');
  // best[j][i]: the cheapest way to lay parts[0..i) into j groups, and where the last one starts.
  const best = Array.from({ length: groups + 1 }, () => new Array(parts.length + 1).fill(null));
  best[0][0] = { cost: 0, from: -1 };
  for (let j = 1; j <= groups; j++) {
    for (let i = j; i <= parts.length; i++) {
      for (let from = j - 1; from < i; from++) {
        if (!best[j - 1][from]) continue;
        const text = piece(from, i);
        const size = width(text);
        const clause = i < parts.length && CLAUSE_END.test(text.trimEnd()) ? -(target * target) / 4 : 0;
        const cost = best[j - 1][from].cost + (size - target) * (size - target) + clause;
        if (!best[j][i] || cost < best[j][i].cost) best[j][i] = { cost, from };
      }
    }
  }
  const out = [];
  for (let j = groups, i = parts.length; j > 0; j--) {
    const from = best[j][i].from;
    out.unshift(piece(from, i));
    i = from;
  }
  return out;
}

/** Every group of a phrase, each knowing its line, its width and its spoken weight. */
export function phraseGroups(text) {
  const groups = [];
  captionLines(text).forEach((line, index) => {
    for (const group of groupLine(line)) groups.push({ text: group, line: index, width: width(group), weight: weightOf(group) });
  });
  return groups;
}

function windowRms(samples, start, length) {
  let sum = 0;
  const end = Math.min(samples.length, start + length);
  for (let index = start; index < end; index++) sum += samples[index] * samples[index];
  return Math.sqrt(sum / Math.max(1, end - start));
}

/**
 * Where the voice is inside a clip, in seconds: the first and last run of three 10 ms windows
 * above the speech threshold, widened a little so no consonant is lit late. A clip with no such
 * run is taken as spoken end to end.
 */
export function speechSpan(samples, sampleRate = SAMPLE_RATE) {
  const duration = samples.length / sampleRate;
  const length = Math.round((WINDOW_MS / 1000) * sampleRate);
  const windows = Math.ceil(samples.length / length);
  const levels = Array.from({ length: windows }, (_each, index) => windowRms(samples, index * length, length));
  const threshold = Math.max(SPEECH_FLOOR_RMS, Math.max(0, ...levels) * SPEECH_PEAK_SHARE);
  const loud = (index) => levels[index] >= threshold;
  const run = (index) => Array.from({ length: SPEECH_WINDOWS }, (_each, offset) => index + offset).every((each) => each < windows && loud(each));
  let first = -1;
  for (let index = 0; index + SPEECH_WINDOWS <= windows; index++) {
    if (run(index)) {
      first = index;
      break;
    }
  }
  if (first < 0) return { start: 0, end: duration };
  let last = windows - 1;
  for (let index = windows - SPEECH_WINDOWS; index >= first; index--) {
    if (run(index)) {
      last = index + SPEECH_WINDOWS - 1;
      break;
    }
  }
  const start = Math.max(0, (first * WINDOW_MS - SPEECH_LEAD_MS) / 1000);
  const end = Math.min(duration, ((last + 1) * WINDOW_MS + SPEECH_TAIL_MS) / 1000);
  return { start: Number(start.toFixed(3)), end: Number(end.toFixed(3)) };
}

/** Each group's start and end inside the clip: its share of the weight across the speech span. */
export function estimateGroupTimes(groups, span) {
  const total = groups.reduce((sum, group) => sum + group.weight, 0);
  let cursor = span.start;
  return groups.map((group, index) => {
    const end = index === groups.length - 1 ? span.end : cursor + ((span.end - span.start) * group.weight) / total;
    const timed = { ...group, start: Number(cursor.toFixed(3)), end: Number(end.toFixed(3)) };
    cursor = end;
    return timed;
  });
}

/**
 * The states of a cue's caption, each the frames one group stays lit: the first from the cue's
 * first frame (the leading silence belongs to the first group), the last to the cue's last
 * frame (the trailing silence and the timeline's padding belong to the last group), nothing
 * shorter than MIN_STATE_FRAMES, and together exactly the cue's frames.
 */
export function captionStates(cue, groups, fps = PROFILE.fps) {
  if (!groups.length) return [{ group: 0, frames: cue.frames }];
  const starts = groups.map((group, index) => (index === 0 ? 0 : Math.min(cue.frames, Math.round(group.start * fps))));
  const states = [];
  for (let index = 0; index < groups.length; index++) {
    const next = index === groups.length - 1 ? cue.frames : starts[index + 1];
    const frames = next - starts[index];
    const last = states.at(-1);
    if (frames < MIN_STATE_FRAMES && last) last.frames += frames;
    else states.push({ group: index, frames });
  }
  // A short first state has no predecessor to fold into: it takes the second's frames instead.
  while (states.length > 1 && states[0].frames < MIN_STATE_FRAMES) {
    states[0].frames += states[1].frames;
    states.splice(1, 1);
  }
  const total = states.reduce((sum, state) => sum + state.frames, 0);
  if (total !== cue.frames) throw new Error(`caption states cover ${total} frames of a ${cue.frames}-frame cue`);
  return states;
}

/** One phrase of timing.json, from its cue and the PCM of its clip. */
export function phraseTiming(cue, samples, sampleRate = SAMPLE_RATE, fps = PROFILE.fps) {
  const lines = captionLines(cue.text);
  const span = speechSpan(samples, sampleRate);
  const groups = estimateGroupTimes(phraseGroups(cue.text), span);
  return {
    cue: cue.index,
    text: cue.text,
    audio_seconds: Number((samples.length / sampleRate).toFixed(3)),
    speech: span,
    lines,
    groups,
    states: captionStates(cue, groups, fps),
  };
}

/** timing.json: every phrase's lines, groups, times and states, and where the times came from. */
export function timingFile(timeline, wavs) {
  if (wavs.length !== timeline.cues.length) throw new Error('a clip is required for every phrase');
  return {
    version: 1,
    source: 'estimated',
    method: KARAOKE_VERSION,
    fps: timeline.fps,
    phrases: timeline.cues.map((cue) => phraseTiming(cue, wavs[cue.index].samples, wavs[cue.index].sampleRate, timeline.fps)),
  };
}

/** The style a build draws its captions in: the flag, else the environment, else plain. */
export function captionsOption(value, env = process.env) {
  const style = value ?? env?.[CAPTIONS_ENV] ?? DEFAULT_CAPTIONS;
  if (!CAPTION_STYLES.includes(style)) throw new Error(`captions must be one of ${CAPTION_STYLES.join(', ')} (got ${style})`);
  return style;
}

/** What checks.json records about the captions of a build. */
export function captionsSummary(timing) {
  if (!timing) return { style: 'plain' };
  return {
    style: 'karaoke',
    source: timing.source,
    version: timing.method,
    groups: timing.phrases.reduce((sum, phrase) => sum + phrase.groups.length, 0),
    states: timing.phrases.reduce((sum, phrase) => sum + phrase.states.length, 0),
  };
}
