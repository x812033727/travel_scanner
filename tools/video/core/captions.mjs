// Caption cues and the SRT / WebVTT files YouTube accepts (support.google.com/youtube/answer/2734698).
//
// Captions are the only thing that subdivides a line. A long line is cut into the fewest cues
// that fit the locale's lines, preferably where a clause ends, and the line's speech time is
// shared among them in proportion to how long each piece takes to say. Each locale cuts its own
// translation inside the same line window, so locales never need the same number of cues:
// English word order makes a one-to-one split with Chinese impossible to keep natural.
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
const TRAILING = /[，。、；：,;:\s]+$/u;
// A cue that ends on one of these ends a clause; a cue must never start with one.
const ENDS_CLAUSE = /[，。！？；：、,.!?;:—]$/u;
const OPENS_BADLY = /^[，。！？；：、,.!?;:）」』)\]]/u;
// Chinese and Japanese break between characters but never inside a Latin word or a number.
const CJK_TOKEN = /[A-Za-z0-9][A-Za-z0-9.+#'_-]*|\s+|./gsu;

/** Display width in the locale's units: CJK locales count half-width characters as half. */
export function measure(text, rules) {
  if (rules.words) return [...text].length;
  let width = 0;
  for (const char of text) width += WIDE.test(char) ? 1 : 0.5;
  return width;
}

function tokens(text, rules) {
  return rules.words ? text.split(/(\s+)/).filter(Boolean) : (text.match(CJK_TOKEN) ?? []);
}

// The last resort, for text with no break that fits: fill each piece up to the width.
function hardSplit(text, width, rules) {
  const pieces = [];
  let current = "";
  for (const token of tokens(text, rules)) {
    if (current.trim() && measure(`${current}${token}`.trim(), rules) > width) {
      pieces.push(current.trim());
      current = token.trimStart();
    } else {
      current += token;
    }
  }
  if (current.trim()) pieces.push(current.trim());
  return pieces;
}

/** Join two pieces of one line again, keeping the space between words in word-based locales. */
export function joinPieces(first, second, rules) {
  return rules.words && first && second ? `${first.trimEnd()} ${second.trimStart()}` : `${first}${second}`;
}

/**
 * Whether the text can be shown as one cue: laid out greedily, it takes at most maxLines lines of
 * maxChars. Greedy layout uses the fewest lines, so wrapCue can always find a break when this holds.
 */
export function fits(text, rules) {
  let lines = 1;
  let current = "";
  for (const token of tokens(text.trim(), rules)) {
    if (current.trim() && measure(`${current}${token}`.trim(), rules) > rules.maxChars) {
      lines += 1;
      current = token.trimStart();
    } else {
      current += token;
    }
  }
  return lines <= rules.maxLines;
}

/**
 * Cut one line's text into cue-sized pieces: the fewest cues that fit, as even in length as
 * possible, preferring to cut where a clause ends. Every piece fits in the locale's cue.
 */
export function splitText(text, rules) {
  const clean = text.trim();
  if (fits(clean, rules)) return [clean];
  const parts = tokens(clean, rules);
  const piece = (from, to) => parts.slice(from, to).join("").trim();
  const cap = rules.maxChars * rules.maxLines;
  // Cutting mid-clause costs about as much as leaving one cue a quarter of the others' length.
  const midClause = (cap * cap) / 4;
  // best[to] = the cheapest way to cut parts[0..to): fewest cues first, then the most even.
  const best = [{ count: 0, cost: 0, from: -1 }];
  for (let to = 1; to <= parts.length; to++) {
    best[to] = null;
    if (!parts[to - 1].trim() || (to < parts.length && OPENS_BADLY.test(piece(to, parts.length)))) continue;
    for (let from = to - 1; from >= 0; from--) {
      const text = piece(from, to);
      if (!text || !best[from]) continue;
      if (!fits(text, rules)) break;
      const size = measure(text, rules);
      const count = best[from].count + 1;
      const cost = best[from].cost + size * size + (to < parts.length && !ENDS_CLAUSE.test(text) ? midClause : 0);
      const current = best[to];
      if (!current || count < current.count || (count === current.count && cost < current.cost)) best[to] = { count, cost, from };
    }
  }
  if (!best[parts.length]) return hardSplit(clean, cap, rules);
  const pieces = [];
  for (let to = parts.length; to > 0; to = best[to].from) pieces.unshift(piece(best[to].from, to));
  return pieces.filter(Boolean);
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
 * Share [startMs, endMs] among the pieces by spoken weight. A piece that would be shorter than
 * MIN_CUE_MS is merged with a neighbour, when `rules` are given only if the merged cue still fits;
 * a short piece with no neighbour it fits with stays short rather than wrapping onto a third line.
 */
export function timePieces(pieces, startMs, endMs, rules = null) {
  let entries = pieces.map((text) => ({ text, weight: weight(text) }));
  const span = Math.max(0, endMs - startMs);
  const duration = (entry, total) => (span * entry.weight) / total;
  const merged = (first, second) => (rules ? joinPieces(first.text, second.text, rules) : `${first.text}${second.text}`);
  for (;;) {
    const total = entries.reduce((sum, entry) => sum + entry.weight, 0);
    const short = entries.findIndex((entry) => !entry.settled && duration(entry, total) < MIN_CUE_MS);
    if (short < 0 || entries.length === 1) break;
    const neighbours = [short + 1, short - 1].filter((index) => index >= 0 && index < entries.length);
    const other = neighbours.find((index) => {
      const [first, second] = [Math.min(short, index), Math.max(short, index)];
      return !rules || fits(merged(entries[first], entries[second]), rules);
    });
    if (other === undefined) {
      entries[short].settled = true;
      continue;
    }
    const [first, second] = [Math.min(short, other), Math.max(short, other)];
    entries.splice(first, 2, { text: merged(entries[first], entries[second]), weight: entries[first].weight + entries[second].weight });
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
    for (const cue of timePieces(splitText(text, rules), start, end, rules)) {
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
