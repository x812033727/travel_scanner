// The listener's rewrite of a narration line, checked against the line it replaces
// (docs/videos/HANDS-OFF.md §旁白). After the retakes are spent, Jev may still hear a line
// wrong; the listener rewords it for the voice (on 2026-09-26 that was 「和」→「跟」, a
// sentence-final 「答」→「回答」, 「旗艦」→「旗艦模型」), but what a viewer would notice must
// survive the rewording: every number (「1.5」「2026」「10%」「US$3」), every Latin-script word
// and every term of the pronunciation dictionary must appear in the rewrite as often as
// before, and none of those kinds may appear that was not there. A rewrite that breaks this is
// dropped and the line keeps its text; the reason goes to the video's notes.

// A number as the script writes it: an optional currency mark, digits with decimal or thousands
// marks, an optional percent sign.
const NUMBER = String.raw`(?:(?:US|NT|HK|AU|SG)\$|[$€£¥])?\d+(?:[.,]\d+)*%?`;
// A Latin-script word, possibly joined by - . + # to letters or digits: "GPT-5", "p95", "C#", "Node.js".
const LATIN = String.raw`[A-Za-z][A-Za-z0-9+.#-]*`;
const TOKEN = new RegExp(`${NUMBER}|${LATIN}`, "g");
const WORD = /^[A-Za-z][A-Za-z0-9+.#-]*$/;
const FULL_WIDTH_ZERO = "０".charCodeAt(0);

/** Full-width digits and the full-width percent sign as their ASCII forms; nothing else changes. */
const ascii = (text) => String(text).replace(/[０-９]/g, (digit) => String(digit.charCodeAt(0) - FULL_WIDTH_ZERO)).replace(/％/g, "%");

const escapeRegExp = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * The numbers and the Latin-script words of a line, each as written. A period or hyphen that
 * ends a word is punctuation ("OpenAI." is OpenAI), while "Node.js" and "GPT-5" stay whole.
 */
export function factTokens(text) {
  const tokens = { numbers: [], words: [] };
  for (const match of ascii(text).matchAll(TOKEN)) {
    const token = match[0];
    if (WORD.test(token)) tokens.words.push(token.replace(/[.-]+$/, ""));
    else tokens.numbers.push(token);
  }
  return tokens;
}

function counts(items) {
  const map = new Map();
  for (const item of items) map.set(item, (map.get(item) ?? 0) + 1);
  return map;
}

/**
 * What `after` has more or fewer of than `before`, one sentence each, plus the keys that
 * differ. `key` folds tokens that count as the same (a word's case).
 */
function differences(kind, before, after, key = (token) => token) {
  const was = counts(before.map(key));
  const is = counts(after.map(key));
  const spelled = new Map();
  for (const token of [...before, ...after]) if (!spelled.has(key(token))) spelled.set(key(token), token);
  const problems = [];
  const keys = new Set();
  for (const id of new Set([...was.keys(), ...is.keys()])) {
    const [a, b] = [was.get(id) ?? 0, is.get(id) ?? 0];
    if (a === b) continue;
    keys.add(id);
    const shown = kind === "number" ? spelled.get(id) : `"${spelled.get(id)}"`;
    if (b === 0) problems.push(`${kind} ${shown} is missing`);
    else if (a === 0) problems.push(`${kind} ${shown} was added`);
    else problems.push(`${kind} ${shown} appears ${b} times instead of ${a}`);
  }
  return { problems, keys };
}

/** How often a dictionary term occurs as a whole word, matched as the synthesis matches it (tts/requests.mjs). */
function termCount(text, term) {
  const pattern = new RegExp(`(?<![A-Za-z0-9])${escapeRegExp(term)}(?![A-Za-z0-9])`, "gu");
  return (String(text).match(pattern) ?? []).length;
}

/**
 * What a rewrite changed that it may not, as sentences; nothing when it is fine. `before` and
 * `after` are one line's spoken text before and after the rewrite; `lexicon` is the
 * pronunciation dictionary (docs/videos/lexicon.json, { terms: { term: spoken form | null } }).
 * Numbers must match as written; Latin words case-insensitively (the voice reads them the
 * same); dictionary terms as the dictionary spells them, since the synthesis substitutes a
 * term only in that spelling and lint refuses any other. An unchanged line is fine.
 */
export function rewriteProblems(before, after, { lexicon = null } = {}) {
  if (typeof before !== "string" || typeof after !== "string") return ["a line's text must be a string"];
  if (before === after) return [];
  const was = factTokens(before);
  const is = factTokens(after);
  const numbers = differences("number", was.numbers, is.numbers);
  const words = differences("word", was.words, is.words, (word) => word.toLowerCase());
  const problems = [...numbers.problems, ...words.problems];
  for (const term of Object.keys(lexicon?.terms ?? {})) {
    // A single word already reported as a word is not reported again as a term.
    if (words.keys.has(term.toLowerCase())) continue;
    const [a, b] = [termCount(before, term), termCount(after, term)];
    if (a === b) continue;
    if (b === 0) problems.push(`term "${term}" is missing`);
    else if (a === 0) problems.push(`term "${term}" was added`);
    else problems.push(`term "${term}" appears ${b} times instead of ${a}`);
  }
  return problems;
}
