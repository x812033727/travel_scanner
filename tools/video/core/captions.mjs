// Caption cues and the SRT / WebVTT files YouTube accepts (support.google.com/youtube/answer/2734698).
//
// Captions are the only thing that subdivides a line. A long line is cut into the fewest cues
// that fit the locale's lines, preferably where a sentence ends, else where a clause ends, and
// the line's speech time is shared among them in proportion to how long each piece takes to say.
// When the timeline carries when each character of the line was spoken (`timing`, written by
// tts from the server's measured times, tts/synthesis.mjs), a cue starts when its first
// character is spoken instead, for the text those times were measured on.
// A number is never parted from its unit, by a cue or by a line break. Each locale cuts its own
// translation inside the same line window, so locales never need the same number of cues:
// English word order makes a one-to-one split with Chinese impossible to keep natural; the
// translator is shown the narration's cue boundaries instead (cuePieces). A translation keeps its
// own cut, and when the narration of its line was measured, its cue changes take their times from
// the narration's measured cue changes (inheritBoundaries); otherwise it shares the time by weight.
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
// A cue that ends on one of these (closing quotes and brackets allowed after it) ends a sentence,
// the best place to cut; on one of the second set, a clause, the next best. A cue must never
// start with one.
const ENDS_SENTENCE = /[。！？.!?][」』）)\]"'”’]*$/u;
const ENDS_CLAUSE = /[，。！？；：、,.!?;:—][」』）)\]"'”’]*$/u;
const OPENS_BADLY = /^[，。！？；：、,.!?;:）」』)\]]/u;
// Chinese and Japanese break between characters but never inside a Latin word or a number.
const LATIN_RUN = "[A-Za-z0-9][A-Za-z0-9.+#'_-]*";
// A number keeps its unit: "300 GB", "15.8%", "1.15×", "US$0.135", "5 分鐘", "2026 年", "3 million".
// The digits may carry a currency sign; the unit is a symbol, a Chinese or Japanese measure word
// (with or without a space), or a Latin unit word after a space. A Latin suffix with no space
// ("24fps", "5G") is a Latin run already. A false match only keeps two things together.
const CURRENCY = "(?:US\\$|NT\\$|HK\\$|[$€£¥₩])";
const DIGITS = "\\d+(?:[,.]\\d+)*";
const SYMBOL_UNIT = "%|％|×|°C|℃|°";
const CJK_UNIT = "分鐘|小時|公里|公尺|公分|公斤|公克|毫秒|美元|美金|台幣|日圓|日元|韓元|人民幣|歐元|英鎊|時間|か月|ヶ月|カ月|年|月|日|週|天|秒|分|元|円|萬|万|億|兆|倍|次|回|個|位|名|人|台|支|款|種|項|頁|行|字|張|條|顆|部|集|季|層|級|歲|度|塊|成|折|筆|組|份|批|場|句|段|篇|章|節|步|幀|格|件|本|枚|點|点|號|つ";
const LATIN_UNIT = "[kKMGTPE]?[bB]|[kKMGT]?Hz|[kKMG]?bps|fps|ms|μs|ns|s|sec|secs|min|mins|h|hr|hrs|km|m|cm|mm|nm|kg|g|mg|lb|lbs|oz|mi|ft|W|kW|MW|Wh|kWh|mAh|px|dpi|ppi|pt|k|K|M|USD|EUR|GBP|JPY|KRW|TWD|NTD|CNY|RMB|HKD|million|billion|trillion|thousand|percent|points?|seconds?|minutes?|hours?|days?|weeks?|months?|years?|tokens?|times|fold|x";
const HANGUL_UNIT = "분|초|시간|일|주|개월|년|원|달러|만|억|배|번|개|명|대|건|회|등|위|점|자|줄|장|퍼센트";
const NUMBER_UNIT = `${CURRENCY}?${DIGITS}(?:\\s?(?:${SYMBOL_UNIT}|${CJK_UNIT})|\\s(?:${LATIN_UNIT}))(?![A-Za-z0-9])`;
// A currency sign stays with its number even without a unit ("US$0.135").
const PRICED = `${CURRENCY}${DIGITS}(?![A-Za-z0-9])`;
const CJK_TOKEN = new RegExp(`${NUMBER_UNIT}|${PRICED}|${LATIN_RUN}|\\s+|.`, "gsu");
// Word-based locales split at spaces; a number and the unit word after it are joined again.
const NUMBER_WORD = new RegExp(`^[(\\[「『"']?${CURRENCY}?${DIGITS}$`, "u");
const UNIT_WORD = new RegExp(`^(?:${SYMBOL_UNIT}|${LATIN_UNIT}|${CJK_UNIT}|${HANGUL_UNIT})[,.;:!?)\\]」』"']*$`, "u");

/** Display width in the locale's units: CJK locales count half-width characters as half. */
export function measure(text, rules) {
  if (rules.words) return [...text].length;
  let width = 0;
  for (const char of text) width += WIDE.test(char) ? 1 : 0.5;
  return width;
}

// "300", " ", "GB" become "300 GB": a number and its unit word are one token.
function joinUnits(parts) {
  const joined = [];
  for (const token of parts) {
    const at = joined.length;
    if (at >= 2 && UNIT_WORD.test(token) && !joined[at - 1].trim() && NUMBER_WORD.test(joined[at - 2])) {
      joined.splice(at - 2, 2, joined[at - 2] + joined[at - 1] + token);
    } else {
      joined.push(token);
    }
  }
  return joined;
}

function rawTokens(text, rules) {
  return rules.words ? joinUnits(text.split(/(\s+)/).filter(Boolean)) : (text.match(CJK_TOKEN) ?? []);
}

function tokens(text, rules) {
  const parts = rawTokens(text, rules);
  const grouped = [];
  for (const token of parts) {
    if (OPENS_BADLY.test(token)) {
      // Spaces before closing punctuation cannot make it safe to start a line.
      // Attach the whole closing run, including those spaces, to its preceding token.
      let closing = token;
      while (grouped.length && !grouped.at(-1).trim()) closing = grouped.pop() + closing;
      if (grouped.length) grouped[grouped.length - 1] += closing;
      else grouped.push(closing);
    } else grouped.push(token);
  }
  return grouped;
}

function wrapTokens(parts, width, rules) {
  const pieces = [];
  let current = "";
  for (const token of parts) {
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

// The last resort, for text with no break that fits: fill each piece up to the width.
function hardSplit(text, width, rules) {
  return wrapTokens(tokens(text, rules), width, rules);
}

/** Join two pieces of one line again, keeping the space between words in word-based locales. */
export function joinPieces(first, second, rules) {
  return rules.words && first && second ? `${first.trimEnd()} ${second.trimStart()}` : `${first}${second}`;
}

/**
 * Whether the text takes at most maxLines using the same legal breaks as wrapCue's fallback.
 * An indivisible token wider than maxChars stays intact for checkCues to report, not to be split.
 */
export function fits(text, rules) {
  return hardSplit(text.trim(), rules.maxChars, rules).length <= rules.maxLines;
}

function fitsDisplayed(text, rules) {
  // Keep the old raw-text capacity limit: stripping punctuation must not merge
  // previously separate cues. Then require the actual displayed text to wrap safely.
  // Only measure a stripped copy; splitting scores and timing still use the raw text.
  return wrapTokens(rawTokens(text.trim(), rules), rules.maxChars, rules).length <= rules.maxLines
    && fits(displayText(text, rules), rules);
}

/** The fit check buildCues uses: the displayed text for the CJK locales, the raw text for word-based ones. */
const canFitFor = (rules) => (rules.words ? fits : fitsDisplayed);

/**
 * Cut one line's text into cue-sized pieces: the fewest cues that fit, as even in length as
 * possible, preferring to cut where a sentence ends, then where a clause ends. Every piece fits
 * in the locale's cue, and a number stays with its unit (tokens).
 */
export function splitText(text, rules, canFit = fits) {
  const clean = text.trim();
  if (canFit(clean, rules)) return [clean];
  const parts = tokens(clean, rules);
  const piece = (from, to) => parts.slice(from, to).join("").trim();
  const cap = rules.maxChars * rules.maxLines;
  // Cutting mid-clause costs about as much as leaving one cue a quarter of the others' length;
  // cutting at a clause end (a comma) half of that, so a sentence end wins over a comma unless
  // the pieces become clearly lopsided, and a comma wins over mid-clause the same way.
  const midClause = (cap * cap) / 4;
  const cutCost = (text) => (ENDS_SENTENCE.test(text) ? 0 : ENDS_CLAUSE.test(text) ? midClause / 2 : midClause);
  // best[to] = the cheapest way to cut parts[0..to): fewest cues first, then the most even.
  const best = [{ count: 0, cost: 0, from: -1 }];
  for (let to = 1; to <= parts.length; to++) {
    best[to] = null;
    if (!parts[to - 1].trim() || (to < parts.length && OPENS_BADLY.test(piece(to, parts.length)))) continue;
    for (let from = to - 1; from >= 0; from--) {
      const text = piece(from, to);
      if (!text || !best[from]) continue;
      if (!canFit(text, rules)) break;
      const size = measure(text, rules);
      const count = best[from].count + 1;
      const cost = best[from].cost + size * size + (to < parts.length ? cutCost(text) : 0);
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
 * The pieces one line's captions are cut into before timing, for a locale: what a translator is
 * shown as the narration's cue boundaries (tools/video/i18n/cli.mjs translationContext).
 * timePieces may still merge a piece that would flash past.
 */
export function cuePieces(text, locale) {
  const rules = LOCALE_RULES[locale];
  if (!rules) throw new Error(`no caption rules for locale ${locale}`);
  return splitText(text, rules, canFitFor(rules));
}

/**
 * Break a cue into two lines near the middle when it is wider than one line: after punctuation
 * if possible, never inside a Latin word, a number or a number and its unit, at a space for
 * word-based locales.
 */
export function wrapCue(text, rules) {
  if (measure(text, rules) <= rules.maxChars || rules.maxLines < 2) return text;
  const chars = [...text];
  const boundaries = new Set();
  let offset = 0;
  for (const token of tokens(text, rules)) {
    const length = [...token].length;
    // Keep the old scoring opportunities inside harmless whitespace runs; trim()
    // makes the resulting lines identical, but their midpoint scores can differ.
    if (!token.trim()) for (let index = 1; index < length; index++) boundaries.add(offset + index);
    offset += length;
    boundaries.add(offset);
  }
  const half = measure(text, rules) / 2;
  let best = null;
  let width = 0;
  for (let index = 0; index < chars.length - 1; index++) {
    width += measure(chars[index], rules);
    if (!boundaries.has(index + 1)) continue;
    const [char, next] = [chars[index], chars[index + 1]];
    let penalty = 0;
    if (rules.words) {
      if (!/\s/.test(char) && !/\s/.test(next)) continue;
    } else {
      penalty = /[，、；：,;:？！]/.test(char) ? 0 : 3;
    }
    const left = chars.slice(0, index + 1).join("").trim();
    const right = chars.slice(index + 1).join("").trim();
    if (!left || !right || OPENS_BADLY.test(right) || measure(left, rules) > rules.maxChars || measure(right, rules) > rules.maxChars) continue;
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

// What is heard: a letter or a number. Spaces are never timed, and punctuation, which the server
// times only by filling the gap between its neighbours (apps/api/app/video_speech/align.py), is
// never where a cue starts.
const SPOKEN = /[\p{L}\p{N}]/u;

/**
 * When each piece of a line is first heard, from the line's measured characters: `chars` are the
 * written units the server timed ({ text, start_ms, end_ms }, a CJK character, a Latin word or
 * number, a term read through its spoken form, a punctuation mark), relative to the line's own
 * clip, which starts at `startMs`. A piece starts where the unit holding its first spoken
 * character starts. Null, so the caller shares the time by weight, when the pieces and the units
 * do not line up: their letters and numbers differ in any way or order (a `say` that changes the
 * words, a translation), a piece starts inside a unit (in the middle of a term read as one), or a
 * start runs backwards or outside [startMs, endMs).
 */
function measuredStarts(pieces, startMs, endMs, chars) {
  const heard = [];
  chars.forEach((unit, index) => {
    let first = true;
    for (const char of String(unit?.text ?? "").normalize("NFC")) {
      if (!SPOKEN.test(char)) continue;
      heard.push({ char, unit: index, first });
      first = false;
    }
  });
  const starts = [];
  let at = 0;
  for (const piece of pieces) {
    const spoken = [...piece.normalize("NFC")].filter((char) => SPOKEN.test(char));
    const head = heard[at];
    if (!spoken.length || !head?.first) return null;
    for (const char of spoken) if (heard[at++]?.char !== char) return null;
    const start = startMs + Number(chars[head.unit].start_ms);
    if (!Number.isFinite(start) || start < startMs || start >= endMs || (starts.length && start <= starts.at(-1))) return null;
    starts.push(start);
  }
  return at === heard.length ? starts : null;
}

/**
 * Merge each piece that would last less than MIN_CUE_MS with a neighbour, the next one first;
 * when `rules` are given only if the merged cue still fits, so a short piece with no neighbour it
 * fits with stays short rather than wrapping onto a third line. `duration(entries, index)` is how
 * long a piece would last, `combine(first, second, text)` the entry two pieces merge into.
 */
function mergeShort(entries, duration, combine, rules, canFit) {
  const merged = (first, second) => (rules ? joinPieces(first.text, second.text, rules) : `${first.text}${second.text}`);
  for (;;) {
    const short = entries.findIndex((entry, index) => !entry.settled && duration(entries, index) < MIN_CUE_MS);
    if (short < 0 || entries.length === 1) break;
    const neighbours = [short + 1, short - 1].filter((index) => index >= 0 && index < entries.length);
    const other = neighbours.find((index) => {
      const [first, second] = [Math.min(short, index), Math.max(short, index)];
      return !rules || canFit(merged(entries[first], entries[second]), rules);
    });
    if (other === undefined) {
      entries[short].settled = true;
      continue;
    }
    const [first, second] = [Math.min(short, other), Math.max(short, other)];
    entries.splice(first, 2, combine(entries[first], entries[second], merged(entries[first], entries[second])));
  }
  return entries;
}

/**
 * Time the pieces of one line inside [startMs, endMs], the line's speech window. With `chars`,
 * the line's measured characters relative to its clip (see measuredStarts), each piece starts
 * when its first spoken character does and runs to the next piece's start, the last to endMs;
 * a piece merged for being short starts at the first character of the first of the two.
 * Otherwise, or when the characters do not line up with the pieces, the window is shared by
 * spoken weight, from startMs. Either way a piece that would be shorter than MIN_CUE_MS is merged
 * with a neighbour (mergeShort).
 */
export function timePieces(pieces, startMs, endMs, rules = null, canFit = fits, chars = null) {
  const starts = Array.isArray(chars) ? measuredStarts(pieces, startMs, endMs, chars) : null;
  if (starts) {
    const until = (entries, index) => (index + 1 < entries.length ? entries[index + 1].start : endMs);
    const entries = mergeShort(
      pieces.map((text, index) => ({ text, start: starts[index] })),
      (all, index) => until(all, index) - all[index].start,
      (first, _second, text) => ({ text, start: first.start }),
      rules,
      canFit,
    );
    return entries.map((entry, index) => ({ start_ms: Math.round(entry.start), end_ms: Math.round(until(entries, index)), text: entry.text }));
  }
  const span = Math.max(0, endMs - startMs);
  const total = (entries) => entries.reduce((sum, entry) => sum + entry.weight, 0);
  const duration = (entry, sum) => (span * entry.weight) / sum;
  const entries = mergeShort(
    pieces.map((text) => ({ text, weight: weight(text) })),
    (all, index) => duration(all[index], total(all)),
    (first, second, text) => ({ text, weight: first.weight + second.weight }),
    rules,
    canFit,
  );
  const sum = total(entries);
  let cursor = startMs;
  return entries.map((entry, index) => {
    const end = index === entries.length - 1 ? endMs : cursor + duration(entry, sum);
    const cue = { start_ms: Math.round(cursor), end_ms: Math.round(end), text: entry.text };
    cursor = end;
    return cue;
  });
}

/**
 * When each narration cue after the first starts, for one line: the narration's text cut as its
 * own captions are and timed by its measured characters (timePieces). Null when the characters do
 * not line up with that text, or it is cut into one cue, so a translation has nothing to inherit.
 */
function narrationBoundaries(text, locale, startMs, endMs, chars) {
  const rules = LOCALE_RULES[locale];
  if (!rules || typeof text !== "string" || !text.trim()) return null;
  const canFit = canFitFor(rules);
  const pieces = splitText(text, rules, canFit);
  if (!measuredStarts(pieces, startMs, endMs, chars)) return null;
  const starts = timePieces(pieces, startMs, endMs, rules, canFit, chars).slice(1).map((cue) => cue.start_ms);
  return starts.length ? starts : null;
}

/**
 * For each value of `from` in order, the index of the nearest value of `to` after the one picked
 * before it, leaving enough of `to` for the values still to come (`from` is not longer than `to`).
 */
function nearestInOrder(from, to) {
  const picked = [];
  let next = 0;
  from.forEach((value, index) => {
    const last = to.length - (from.length - index);
    let best = next;
    for (let at = next + 1; at <= last; at++) if (Math.abs(to[at] - value) < Math.abs(to[best] - value)) best = at;
    picked.push(best);
    next = best + 1;
  });
  return picked;
}

/**
 * A translation's cues for one line, `weighted` (its own cut, timed by weight), moved onto the
 * narration's measured cue changes, `boundaries` (when each narration cue after the first
 * starts). The cut, the first start and the last end stay; only the changes between cues move.
 * Equal counts take the narration's changes one for one. Fewer translated changes each take, in
 * order, the nearest narration change not yet taken. More translated changes pin each narration
 * change to the nearest translated one, in order, and the others keep their weighted shares of
 * the span between the pins around them. Null, so the line keeps its weighted times, when a cue
 * would then be shorter than MIN_CUE_MS, or (given the locale's `rules`) read faster than its
 * maxCps, where its weighted time was not.
 */
export function inheritBoundaries(weighted, boundaries, rules = null) {
  const own = weighted.slice(1).map((cue) => cue.start_ms);
  if (!own.length || !boundaries?.length) return null;
  const startMs = weighted[0].start_ms;
  const endMs = weighted.at(-1).end_ms;
  const starts = [...own];
  if (own.length <= boundaries.length) {
    nearestInOrder(own, boundaries).forEach((at, index) => {
      starts[index] = boundaries[at];
    });
  } else {
    const pins = nearestInOrder(boundaries, own);
    let [fromIndex, fromOwn, fromTime] = [-1, startMs, startMs];
    for (const [pinIndex, pin] of [...pins.map((at, index) => [at, boundaries[index]]), [own.length, endMs]]) {
      const pinOwn = pinIndex < own.length ? own[pinIndex] : endMs;
      for (let index = fromIndex + 1; index < pinIndex; index++) {
        starts[index] = Math.round(fromTime + ((own[index] - fromOwn) * (pin - fromTime)) / (pinOwn - fromOwn));
      }
      if (pinIndex < own.length) starts[pinIndex] = pin;
      [fromIndex, fromOwn, fromTime] = [pinIndex, pinOwn, pin];
    }
  }
  const cues = weighted.map((cue, index) => ({
    ...cue,
    start_ms: index === 0 ? startMs : starts[index - 1],
    end_ms: index + 1 < weighted.length ? starts[index] : endMs,
  }));
  const tooFast = (cue) => Boolean(rules) && (measure(cue.text, rules) * 1000) / (cue.end_ms - cue.start_ms) > rules.maxCps;
  const worse = cues.some((cue, index) => {
    const length = cue.end_ms - cue.start_ms;
    if (length <= 0) return true;
    const before = weighted[index];
    return (length < MIN_CUE_MS && length < before.end_ms - before.start_ms) || (tooFast(cue) && !tooFast(before));
  });
  return worse ? null : cues;
}

/**
 * Cues for one locale. `texts` maps line id to that locale's text (the narration itself for
 * zh-TW); a line missing from it is skipped and reported. A line whose timeline entry carries
 * `timing.chars` (its measured characters, relative to its clip) has its cues start when their
 * first characters are spoken, when the text is the one that was timed (timePieces). A
 * translation keeps its own cut; given `narration` ({ locale, texts }, the narration's texts by
 * line id), its cue changes take their times from the narration's measured ones
 * (inheritBoundaries). Any other text, or a line the narration's times do not fit, shares the
 * line's time by weight.
 */
export function buildCues(timeline, texts, locale, narration = null) {
  const rules = LOCALE_RULES[locale];
  if (!rules) throw new Error(`no caption rules for locale ${locale}`);
  const canFit = canFitFor(rules);
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
    const chars = Array.isArray(line.timing?.chars) ? line.timing.chars : null;
    let timedPieces = timePieces(splitText(text, rules, canFit), start, end, rules, canFit, chars);
    if (chars && narration && narration.locale !== locale) {
      const boundaries = narrationBoundaries(narration.texts?.[line.id], narration.locale, start, end, chars);
      timedPieces = (boundaries && inheritBoundaries(timedPieces, boundaries, rules)) || timedPieces;
    }
    for (const cue of timedPieces) {
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
