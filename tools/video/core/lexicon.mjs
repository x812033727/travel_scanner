// The shared pronunciation dictionary, docs/videos/lexicon.json.
//
// A Mandarin voice reads Chinese well and English acronyms badly: "LLM" or "p95" come out as
// whatever the voice guesses. So every Latin term in the narration must be in the dictionary,
// either with the spoken form to substitute (an SSML <sub alias> at synthesis time) or with
// null, meaning somebody listened and the voice reads it correctly as written. Lint refuses an
// unknown term; the fix is one line in the dictionary, and every later video benefits.
export const LEXICON_VERSION = 1;

// A Latin word, possibly joined by - . + # ' to letters or digits: "GPT-5", "p95", "C#", "Node.js".
const LATIN_TERM = /[A-Za-z][A-Za-z0-9]*(?:[-.+#'][A-Za-z0-9]+)*[+#]*/g;
const JOINERS = /[-.+#']+/;

export function emptyLexicon() {
  return { schema_version: LEXICON_VERSION, terms: {} };
}

export function validateLexicon(lexicon) {
  const errors = [];
  if (lexicon === null || typeof lexicon !== "object" || Array.isArray(lexicon)) {
    return [{ path: "", message: "lexicon.json must hold a JSON object" }];
  }
  if (lexicon.schema_version !== LEXICON_VERSION) errors.push({ path: "schema_version", message: `must be ${LEXICON_VERSION}` });
  if (lexicon.terms === null || typeof lexicon.terms !== "object" || Array.isArray(lexicon.terms)) {
    errors.push({ path: "terms", message: "must map each term to its spoken form or null" });
    return errors;
  }
  for (const [term, say] of Object.entries(lexicon.terms)) {
    if (!/^[A-Za-z]/.test(term)) errors.push({ path: `terms.${term}`, message: "a term starts with a Latin letter" });
    if (say !== null && (typeof say !== "string" || say.trim() === "")) {
      errors.push({ path: `terms.${term}`, message: "must be the spoken form, or null when the voice already reads it right" });
    }
  }
  return errors;
}

/** The distinct Latin terms in a piece of narration, in order of appearance. */
export function latinTerms(text) {
  return [...new Set(String(text).match(LATIN_TERM) ?? [])];
}

/**
 * Whether the dictionary covers a term. A single letter is always fine (voices spell letters),
 * and a joined term is covered when every part is: "GPT-5" needs "GPT", "Claude.ai" needs both.
 */
export function isKnownTerm(term, lexicon) {
  const terms = lexicon?.terms ?? {};
  if (Object.hasOwn(terms, term)) return true;
  if (/^[A-Za-z]$/.test(term)) return true;
  const parts = term.split(JOINERS).filter(Boolean);
  if (parts.length <= 1) return false;
  return parts.every((part) => /^\d+$/.test(part) || /^[A-Za-z]$/.test(part) || Object.hasOwn(terms, part));
}

export function unknownTerms(text, lexicon) {
  return latinTerms(text).filter((term) => !isKnownTerm(term, lexicon));
}

// An all-caps part of a term ("SEC", the "GPT" of "GPT-6", "AI"): what an English voice spells
// out or guesses at. Ordinary words it reads as written.
const ACRONYM_PART = /^[A-Z]{2,}[0-9]*$/;

export function hasAcronym(term) {
  return String(term).split(JOINERS).some((part) => ACRONYM_PART.test(part));
}

/**
 * The terms a narration in `locale` needs the dictionary for. A Mandarin voice needs every Latin
 * term (unknownTerms); an English voice reads its own language, so only acronyms are checked.
 */
export function unknownTermsFor(text, lexicon, locale = "zh-TW") {
  const unknown = unknownTerms(text, lexicon);
  return locale === "en" ? unknown.filter(hasAcronym) : unknown;
}

/** Dictionary entries with a spoken form, longest first so "Claude Code" wins over "Claude". */
export function substitutions(lexicon) {
  return Object.entries(lexicon?.terms ?? {})
    .filter(([, say]) => typeof say === "string")
    .sort(([a], [b]) => b.length - a.length);
}

const escapeRegExp = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * The pattern that finds substitution terms in a line: whole words only, longest first, so
 * "Claude Code" wins over "Claude" and "API" inside "APIs" is left alone. Null when there are none.
 */
export function termPattern(entries) {
  return entries.length ? new RegExp(`(?<![A-Za-z0-9])(${entries.map(([term]) => escapeRegExp(term)).join("|")})(?![A-Za-z0-9])`, "gu") : null;
}

/**
 * The substitutions some texts actually use, found the way the speech request finds them, sorted
 * by term. The shared dictionary grows with every video, so what a narration depends on is the
 * entries its own lines use, not the whole file.
 */
export function termsUsed(texts, lexicon) {
  const entries = substitutions(lexicon);
  const pattern = termPattern(entries);
  if (!pattern) return [];
  const used = new Set();
  for (const text of texts) for (const match of text.matchAll(pattern)) used.add(match[0]);
  return entries.filter(([term]) => used.has(term)).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0));
}
