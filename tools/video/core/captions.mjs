// Caption cues and the SRT / WebVTT files YouTube accepts (support.google.com/youtube/answer/2734698).
//
// Captions are the only thing that subdivides a line. A long line is cut at punctuation into
// cues that fit the locale's line length, and the line's speech time is shared among them in
// proportion to how long each piece takes to say. Each locale cuts its own translation inside
// the same line window, so locales never need the same number of cues: English word order makes
// a one-to-one split with Chinese impossible to keep natural.
import { frameToMs, samplesToMs, spokenUnits } from "./timeline.mjs";

// Starting values from common subtitle guidelines (characters per line, lines per cue, reading
// speed in characters per second). The captions ticket tunes the non-Chinese ones.
export const LOCALE_RULES = {
  "zh-TW": { maxChars: 16, maxLines: 2, maxCps: 9, words: false },
  "zh-CN": { maxChars: 16, maxLines: 2, maxCps: 9, words: false },
  ja: { maxChars: 16, maxLines: 2, maxCps: 8, words: false },
  ko: { maxChars: 18, maxLines: 2, maxCps: 12, words: true },
  en: { maxChars: 42, maxLines: 2, maxCps: 20, words: true },
};
// A cue shorter than this flashes past; neighbouring pieces are merged instead.
export const MIN_CUE_MS = 900;
// How long the last cue of a line stays up into the pause after it.
export const LINGER_MS = 400;

const WIDE = /[ᄀ-ᅟ⺀-꓏가-힣豈-﫿︰-﹏＀-｠￠-￦]/u;
// Where a clause ends: after Chinese punctuation anywhere, after ASCII punctuation only when a
// space or the end follows, so "5.5" and "Node.js" stay whole.
const CLAUSE_END = /[，。！？；：、]+\s*|[,.!?;:]+(?:\s+|$)/gu;
const TRAILING = /[，。、；：,;:\s]+$/u;

/** Display width in the locale's units: CJK locales count half-width characters as half. */
export function measure(text, rules) {
  if (rules.words) return [...text].length;
  let width = 0;
  for (const char of text) width += WIDE.test(char) ? 1 : 0.5;
  return width;
}

function hardSplit(text, cap, rules) {
  const pieces = [];
  if (rules.words) {
    let current = "";
    for (const word of text.split(/(\s+)/)) {
      if (current && measure(current + word, rules) > cap && current.trim()) {
        pieces.push(current.trim());
        current = word.trimStart();
      } else {
        current += word;
      }
    }
    if (current.trim()) pieces.push(current.trim());
    return pieces;
  }
  // Never cut inside a Latin word or a number.
  const tokens = text.match(/[A-Za-z0-9][A-Za-z0-9.+#'_-]*|\s+|./gsu) ?? [];
  let current = "";
  for (const token of tokens) {
    if (current && measure(current + token, rules) > cap) {
      pieces.push(current);
      current = token.trimStart();
    } else {
      current += token;
    }
  }
  if (current) pieces.push(current);
  return pieces;
}

export function clauses(text) {
  const result = [];
  let start = 0;
  for (const match of text.matchAll(CLAUSE_END)) {
    const end = match.index + match[0].length;
    result.push(text.slice(start, end));
    start = end;
  }
  if (start < text.length) result.push(text.slice(start));
  return result;
}

/** Cut one line's text into cue-sized pieces, preferring clause boundaries. */
export function splitText(text, rules) {
  const cap = rules.maxChars * rules.maxLines;
  const clean = text.trim();
  if (measure(clean, rules) <= cap) return [clean];
  const parts = clauses(clean).flatMap((clause) => (measure(clause, rules) > cap ? hardSplit(clause, cap, rules) : [clause]));
  const pieces = [];
  let current = "";
  for (const clause of parts) {
    if (current && measure(current + clause, rules) > cap) {
      pieces.push(current.trim());
      current = clause;
    } else {
      current += clause;
    }
  }
  if (current.trim()) pieces.push(current.trim());
  return pieces;
}

/**
 * Break a cue into two lines near the middle when it is wider than one line: after punctuation
 * if possible, never inside a Latin word or a number, at a space for word-based locales.
 */
export function wrapCue(text, rules) {
  if (measure(text, rules) <= rules.maxChars || rules.maxLines < 2) return text;
  const chars = [...text];
  const half = measure(text, rules) / 2;
  let best = null;
  let width = 0;
  for (let index = 0; index < chars.length - 1; index++) {
    width += measure(chars[index], rules);
    const [char, next] = [chars[index], chars[index + 1]];
    let penalty = 0;
    if (rules.words) {
      if (!/\s/.test(char) && !/\s/.test(next)) continue;
    } else {
      if (/[A-Za-z0-9]/.test(char) && /[A-Za-z0-9]/.test(next)) continue;
      penalty = /[，、；：,;:？！]/.test(char) ? 0 : 3;
    }
    const left = chars.slice(0, index + 1).join("").trim();
    const right = chars.slice(index + 1).join("").trim();
    if (!left || !right || measure(left, rules) > rules.maxChars || measure(right, rules) > rules.maxChars) continue;
    const score = Math.abs(width - half) + penalty;
    if (!best || score < best.score) best = { score, left, right };
  }
  return best ? `${best.left}\n${best.right}` : hardSplit(text, rules.maxChars, rules).join("\n");
}

/** Chinese and Japanese subtitles drop a cue's trailing comma or full stop; word-based ones keep it. */
export function displayText(text, rules) {
  return rules.words ? text.trim() : text.replace(TRAILING, "");
}

function weight(text) {
  return Math.max(1, spokenUnits(text)) + (text.match(/[，。！？；：、,.!?;:]/gu)?.length ?? 0) * 0.5;
}

/**
 * Share [startMs, endMs] among the pieces by spoken weight. Pieces that would be shorter than
 * MIN_CUE_MS are merged with their neighbour.
 */
export function timePieces(pieces, startMs, endMs) {
  let entries = pieces.map((text) => ({ text, weight: weight(text) }));
  const span = Math.max(0, endMs - startMs);
  const duration = (entry, total) => (span * entry.weight) / total;
  for (;;) {
    const total = entries.reduce((sum, entry) => sum + entry.weight, 0);
    const short = entries.findIndex((entry) => duration(entry, total) < MIN_CUE_MS);
    if (short < 0 || entries.length === 1) break;
    const other = short === entries.length - 1 ? short - 1 : short + 1;
    const [first, second] = [Math.min(short, other), Math.max(short, other)];
    entries.splice(first, 2, { text: `${entries[first].text}${entries[second].text}`, weight: entries[first].weight + entries[second].weight });
  }
  const total = entries.reduce((sum, entry) => sum + entry.weight, 0);
  let cursor = startMs;
  return entries.map((entry, index) => {
    const end = index === entries.length - 1 ? endMs : cursor + duration(entry, total);
    const cue = { start_ms: Math.round(cursor), end_ms: Math.round(end), text: entry.text };
    cursor = end;
    return cue;
  });
}

/**
 * Cues for one locale. `texts` maps line id to that locale's text (the narration itself for
 * zh-TW); a line missing from it is skipped and reported.
 */
export function buildCues(timeline, texts, locale) {
  const rules = LOCALE_RULES[locale];
  if (!rules) throw new Error(`no caption rules for locale ${locale}`);
  const cues = [];
  const missing = [];
  for (const line of timeline.lines) {
    const text = texts[line.id];
    if (typeof text !== "string" || !text.trim()) {
      missing.push(line.id);
      continue;
    }
    const start = frameToMs(line.start_frame);
    const speechEnd = start + samplesToMs(line.audio_samples);
    const end = Math.min(frameToMs(line.end_frame), speechEnd + LINGER_MS);
    for (const cue of timePieces(splitText(text, rules), start, end)) {
      cues.push({ ...cue, line: line.id, text: wrapCue(displayText(cue.text, rules), rules) });
    }
  }
  return { cues, missing };
}

/** Problems a viewer would notice: overlong lines, too many lines, reading too fast, overlaps. */
export function checkCues(cues, locale) {
  const rules = LOCALE_RULES[locale];
  const problems = [];
  cues.forEach((cue, index) => {
    const where = `cue ${index + 1} (${cue.line ?? "?"})`;
    const lines = cue.text.split("\n");
    if (lines.length > rules.maxLines) problems.push(`${where}: ${lines.length} lines, at most ${rules.maxLines}`);
    for (const line of lines) {
      if (measure(line, rules) > rules.maxChars) problems.push(`${where}: "${line}" is wider than ${rules.maxChars}`);
    }
    const seconds = (cue.end_ms - cue.start_ms) / 1000;
    if (seconds <= 0) problems.push(`${where}: ends before it starts`);
    else if (measure(cue.text.replace(/\n/g, ""), rules) / seconds > rules.maxCps) {
      problems.push(`${where}: ${(measure(cue.text, rules) / seconds).toFixed(1)} characters a second, above ${rules.maxCps}`);
    }
    if (index > 0 && cue.start_ms < cues[index - 1].end_ms) problems.push(`${where}: overlaps the previous cue`);
  });
  return problems;
}

function clock(ms, separator) {
  const total = Math.max(0, Math.round(ms));
  const hours = Math.floor(total / 3_600_000);
  const minutes = Math.floor((total % 3_600_000) / 60_000);
  const seconds = Math.floor((total % 60_000) / 1000);
  const millis = total % 1000;
  const pad = (value, width = 2) => String(value).padStart(width, "0");
  return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}${separator}${pad(millis, 3)}`;
}

export function toSrt(cues) {
  return cues.map((cue, index) => `${index + 1}\n${clock(cue.start_ms, ",")} --> ${clock(cue.end_ms, ",")}\n${cue.text}\n`).join("\n");
}

export function toVtt(cues) {
  return `WEBVTT\n\n${cues.map((cue) => `${clock(cue.start_ms, ".")} --> ${clock(cue.end_ms, ".")}\n${cue.text}\n`).join("\n")}`;
}

function parseClock(value) {
  const match = /^(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})$/.exec(value.trim());
  if (!match) throw new Error(`not a caption timestamp: ${value}`);
  const [, hours, minutes, seconds, millis] = match.map(Number);
  return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis;
}

/** Read an SRT file back, e.g. to check a caption file before it is uploaded. */
export function parseSrt(source) {
  return source
    .replace(/\r\n/g, "\n")
    .replace(/^﻿/, "")
    .trim()
    .split(/\n{2,}/)
    .filter(Boolean)
    .map((block) => {
      const lines = block.split("\n");
      const timing = lines.findIndex((line) => line.includes("-->"));
      if (timing < 0) throw new Error(`caption block without a timing line: ${block.slice(0, 40)}`);
      const [start, end] = lines[timing].split("-->");
      return { start_ms: parseClock(start), end_ms: parseClock(end), text: lines.slice(timing + 1).join("\n") };
    });
}
