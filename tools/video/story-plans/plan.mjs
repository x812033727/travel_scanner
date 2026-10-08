// The brand-story backlog (docs/videos/STORY.md §企劃清單與集數列).
//
// A plan is a directory under docs/videos/story-plans/: series.json (the series row and the look
// every story shares), schedule.json (which story is made on which day and slot, the only place
// the order lives), stories/<id>.json (one story each, the file an author edits) and the
// compiled stories.json, which is what the server imports as episode rows. Everything here is
// a pure function of those files, so the checks run in CI without a network.
import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { atPhoneWidth, headlineSizeEstimate, headlineSplitWords, MIN_HEADLINE_PX_AT_PHONE, PHONE_WIDTH } from "../qa/thumbnail.mjs";
import { headlineCount, THUMB_HEADLINE_MAX, THUMB_HEADLINE_WORDS_MAX } from "../templates/templates.mjs";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..");
export const DEFAULT_PLAN = path.join(ROOT, "docs", "videos", "story-plans", "brand-stories-100");

export const SCHEMA_VERSION = 1;
export const CATEGORIES = ["everyday", "asia-brand", "tech"];
export const REGIONS = ["global", "jp", "kr", "tw"];
export const CHAPTER_KEYS = ["hook", "origin", "idea", "engine", "turn", "now"];
export const SLOTS = ["12:00", "20:00"];
// A source that settles a fact on its own, against one that needs a second, independent one.
export const PRIMARY_KINDS = ["official", "court", "academic", "archive"];
export const SOURCE_KINDS = [...PRIMARY_KINDS, "reference", "news", "book"];
export const SENSITIVITY = ["none", "care"];
export const MIN_SOURCES = 3;
export const MAX_CAST = 3;
// The id's letter says what the story is: A everyday objects and invisible standards, B/K/T a
// brand a traveller meets in Japan, Korea or Taiwan, C technology and software.
export const PREFIXES = {
  A: { category: "everyday", region: null },
  B: { category: "asia-brand", region: "jp" },
  K: { category: "asia-brand", region: "kr" },
  T: { category: "asia-brand", region: "tw" },
  C: { category: "tech", region: null },
};
// `headline` is the channel's thumbnail limit (templates.mjs THUMB_HEADLINE_MAX), counted the way
// the qa stage counts it (headlineCount: a CJK glyph one, a Latin word or a number one, at most
// THUMB_HEADLINE_WORDS_MAX of those); a story over it is a warning (storyWarnings), since the
// builder cuts the headline where a word ends (clipHeadline) and more than half of the hundred
// were written under the twelve of before. `headlineDraft` is that twelve, still a problem: past
// it no headline is left after the cut.
export const LIMITS = { title: 60, logline: 120, question: 120, takeaway: 120, subject: 40, pointMin: 60, pointMax: 400, headline: THUMB_HEADLINE_MAX, headlineDraft: 12, appearance: 800, claim: 200, supports: 240, imageNotes: 400, notes: 800 };

// The fields of a story file, in the order the files are written in.
export const STORY_KEYS = ["id", "slug", "category", "region", "subject", "title", "logline", "question", "chapters", "takeaway", "must_verify", "sources", "names", "cast", "image_notes", "sensitivity", "related_guide", "thumbnail"];

const ID = /^[ABKTC][0-9]{2}$/;
const SLUG = /^story-[a-z0-9](?:[a-z0-9-]{0,52}[a-z0-9])?$/;
const SERIES_SLUG = /^[a-z0-9][a-z0-9-]{1,39}$/;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
const CAST_ID = /^[a-z][a-z0-9-]{1,23}$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const HTTPS = /^https:\/\/[^\s/]+\.[^\s/]+(?:\/\S*)?$/;
const ASCII = /^[\x20-\x7e]+$/;

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const length = (value) => [...String(value)].length;

/** A short text field: present, trimmed, and within its limit. */
function text(story, key, max, problems) {
  const value = story[key];
  if (!isText(value)) problems.push(`${key} is missing`);
  else if (value !== value.trim()) problems.push(`${key} has leading or trailing space`);
  else if (length(value) > max) problems.push(`${key} is ${length(value)} characters, at most ${max}`);
}

// Sites whose every edition and mirror are one voice: the English, Chinese and Japanese
// Wikipedia are three hosts of one encyclopedia, and an article in one is often a translation
// of another, so two of them do not corroborate each other.
const ONE_VOICE = ["wikipedia.org", "wikimedia.org", "wikiwand.com", "wikimili.com"];

// A page kept by the Wayback Machine is its publisher's page: the copy and the live article
// are one source, and two publishers' pages read there are two.
const ARCHIVED = /^https:\/\/web\.archive\.org\/web\/\d{4,14}(?:[a-z]{2}_)?\/(https?:\/\/.+)$/i;

/** The original address of a Wayback Machine copy; any other address as it is. */
export const originalUrl = (url) => ARCHIVED.exec(String(url))?.[1] ?? url;

export const hostOf = (url) => {
  try {
    const host = new URL(originalUrl(url)).hostname.replace(/^www\./, "").toLowerCase();
    return ONE_VOICE.some((site) => host === site || host.endsWith(`.${site}`)) ? "wikipedia.org" : host;
  } catch {
    return "";
  }
};

/**
 * Whether the sources a claim cites are enough (docs/videos/STORY.md §查核與來源規則): one
 * primary source, or two sources from different publishers and different hosts; a claim marked
 * `attributed` is an anecdote the narration tells as somebody's account, and one source will do.
 */
export function claimSupported(claim, sources) {
  const cited = (claim.sources ?? []).map((index) => sources[index]).filter(Boolean);
  if (!cited.length) return false;
  if (claim.attributed === true) return true;
  if (cited.some((source) => PRIMARY_KINDS.includes(source.kind))) return true;
  const publishers = new Set(cited.map((source) => String(source.publisher).trim().toLowerCase()));
  const hosts = new Set(cited.map((source) => hostOf(source.url)));
  return publishers.size >= 2 && hosts.size >= 2;
}

/** Everything wrong with one story, as a list of sentences; empty when it is sound. */
export function storyProblems(story, fileId = story?.id) {
  const problems = [];
  if (!isObject(story)) return ["the file is not a JSON object"];
  for (const key of Object.keys(story)) if (!STORY_KEYS.includes(key)) problems.push(`unknown field "${key}"`);
  if (typeof story.id !== "string" || !ID.test(story.id)) problems.push(`id "${story.id}" is not a letter A, B, K, T or C and two digits`);
  else if (story.id !== fileId) problems.push(`id "${story.id}" does not match the file name ${fileId}.json`);
  if (typeof story.slug !== "string" || !SLUG.test(story.slug)) problems.push(`slug "${story.slug}" must be story-<lowercase letters, digits, hyphens>, at most 60 characters`);
  const prefix = PREFIXES[String(story.id ?? "")[0]];
  if (!CATEGORIES.includes(story.category)) problems.push(`category must be one of ${CATEGORIES.join(", ")}`);
  else if (prefix && story.category !== prefix.category) problems.push(`category "${story.category}" does not fit id ${story.id} (${prefix.category})`);
  if (!REGIONS.includes(story.region)) problems.push(`region must be one of ${REGIONS.join(", ")}`);
  else if (prefix?.region && story.region !== prefix.region) problems.push(`region "${story.region}" does not fit id ${story.id} (${prefix.region})`);
  text(story, "subject", LIMITS.subject, problems);
  text(story, "title", LIMITS.title, problems);
  text(story, "logline", LIMITS.logline, problems);
  text(story, "question", LIMITS.question, problems);
  text(story, "takeaway", LIMITS.takeaway, problems);
  if (isText(story.title) && /[<>]/.test(story.title)) problems.push("title has an angle bracket, which YouTube refuses");

  if (!Array.isArray(story.chapters) || story.chapters.length !== CHAPTER_KEYS.length) {
    problems.push(`chapters must be the ${CHAPTER_KEYS.length} parts ${CHAPTER_KEYS.join(", ")}`);
  } else {
    story.chapters.forEach((chapter, index) => {
      const key = CHAPTER_KEYS[index];
      if (chapter?.key !== key) problems.push(`chapters[${index}].key is "${chapter?.key}", expected "${key}"`);
      if (!isText(chapter?.point)) problems.push(`chapters[${index}] (${key}) has no point`);
      else if (length(chapter.point) < LIMITS.pointMin || length(chapter.point) > LIMITS.pointMax) {
        problems.push(`chapters[${index}] (${key}) is ${length(chapter.point)} characters, expected ${LIMITS.pointMin}-${LIMITS.pointMax}`);
      }
    });
  }

  const sources = Array.isArray(story.sources) ? story.sources : [];
  if (sources.length < MIN_SOURCES) problems.push(`sources has ${sources.length} entries, at least ${MIN_SOURCES}`);
  const urls = new Set();
  sources.forEach((source, index) => {
    const where = `sources[${index}]`;
    if (!isObject(source)) {
      problems.push(`${where} is not an object`);
      return;
    }
    // The Wayback Machine's copy of a page is that page: listing both is listing it twice.
    const address = String(originalUrl(source.url)).replace(/^https?:\/\//i, "").replace(/\/$/, "");
    if (typeof source.url !== "string" || !HTTPS.test(source.url)) problems.push(`${where}.url must be an https URL`);
    else if (urls.has(address)) problems.push(`${where}.url repeats an earlier source`);
    else urls.add(address);
    if (!isText(source.publisher)) problems.push(`${where}.publisher is missing`);
    if (!SOURCE_KINDS.includes(source.kind)) problems.push(`${where}.kind must be one of ${SOURCE_KINDS.join(", ")}`);
    if (!isText(source.supports)) problems.push(`${where}.supports is missing: say what this page is the evidence for`);
    else if (length(source.supports) > LIMITS.supports) problems.push(`${where}.supports is over ${LIMITS.supports} characters`);
    if (typeof source.checked !== "string" || !DATE.test(source.checked)) problems.push(`${where}.checked must be the date the page was read, YYYY-MM-DD`);
  });

  const claims = Array.isArray(story.must_verify) ? story.must_verify : [];
  if (claims.length < 4 || claims.length > 10) problems.push(`must_verify has ${claims.length} claims, expected 4-10`);
  claims.forEach((claim, index) => {
    const where = `must_verify[${index}]`;
    if (!isObject(claim) || !isText(claim.claim)) {
      problems.push(`${where} needs a claim`);
      return;
    }
    if (length(claim.claim) > LIMITS.claim) problems.push(`${where}.claim is over ${LIMITS.claim} characters`);
    if (!Array.isArray(claim.sources) || !claim.sources.length || !claim.sources.every((each) => Number.isInteger(each) && each >= 0 && each < sources.length)) {
      problems.push(`${where}.sources must list indexes into sources`);
      return;
    }
    if (claim.attributed !== undefined && typeof claim.attributed !== "boolean") problems.push(`${where}.attributed must be true or false`);
    if (!claimSupported(claim, sources)) {
      problems.push(`${where} rests on one secondary source: cite a primary one, a second independent one, or mark it attributed (the narration then says whose account it is)`);
    }
  });
  if (isText(story.title) && claims.length && !claims.some((claim) => claim.core === true)) {
    problems.push("no must_verify claim is marked core: the one the title rests on");
  }

  const names = Array.isArray(story.names) ? story.names : [];
  if (!names.length || !names.every(isText)) problems.push("names must list the brand, product and personal names the pictures may not show");

  const cast = Array.isArray(story.cast) ? story.cast : null;
  if (!cast) problems.push("cast must be an array (empty when no figure recurs)");
  else {
    if (cast.length > MAX_CAST) problems.push(`cast has ${cast.length} figures, at most ${MAX_CAST}`);
    const ids = new Set();
    cast.forEach((figure, index) => {
      const where = `cast[${index}]`;
      if (typeof figure?.id !== "string" || !CAST_ID.test(figure.id) || figure.id === "narrator") problems.push(`${where}.id must be 2-24 lowercase letters, digits or hyphens, and not "narrator"`);
      else if (ids.has(figure.id)) problems.push(`${where}.id repeats`);
      else ids.add(figure.id);
      if (!isText(figure?.role)) problems.push(`${where}.role is missing`);
      if (!isText(figure?.appearance) || !ASCII.test(figure.appearance) || figure.appearance.length > LIMITS.appearance) {
        problems.push(`${where}.appearance must be English for the image model, at most ${LIMITS.appearance} characters`);
      } else {
        const lower = figure.appearance.toLowerCase();
        for (const name of names.filter((each) => isText(each) && ASCII.test(each))) {
          if (lower.includes(name.toLowerCase())) problems.push(`${where}.appearance names "${name}": a figure is generic, never a likeness`);
        }
      }
    });
  }

  if (!isText(story.image_notes)) problems.push("image_notes is missing: say what the pictures show and what they must not");
  else if (length(story.image_notes) > LIMITS.imageNotes) problems.push(`image_notes is over ${LIMITS.imageNotes} characters`);
  if (!SENSITIVITY.includes(story.sensitivity)) problems.push(`sensitivity must be one of ${SENSITIVITY.join(", ")}`);
  if (story.related_guide !== null && !(typeof story.related_guide === "string" && GUIDE_SLUG.test(story.related_guide))) problems.push("related_guide must be a site article's slug, or null");
  if (!isObject(story.thumbnail) || !isText(story.thumbnail.headline) || !isText(story.thumbnail.idea)) problems.push("thumbnail needs a headline and an idea");
  else if (headlineCount(story.thumbnail.headline).count > LIMITS.headlineDraft) problems.push(`thumbnail.headline counts ${headlineCount(story.thumbnail.headline).count} characters (a Latin word or a number counts one), at most ${LIMITS.headlineDraft}: nothing readable is left once it is cut to the channel's ${LIMITS.headline}`);
  return problems;
}

/**
 * What a story's author should still change, though the file is sound: the thumbnail headline
 * the channel's rule would cut. The builder (automation/story.mjs) cuts it where a word ends
 * (clipHeadline), so the video never carries one the qa stage fails; the author's own six say
 * it better. When nothing the builder cuts it to passes (a Latin word of eight or more letters
 * is too wide for the column at any length), the warning says so instead of promising a cut:
 * the qa stage fails the video until the author writes another.
 */
export function storyWarnings(story) {
  const headline = story?.thumbnail?.headline;
  if (!isText(headline)) return [];
  const problem = headlineProblem(headline);
  if (!problem) return [];
  const cut = clipHeadline(headline);
  const left = headlineProblem(cut);
  const shown = `「${cut.replace(/\n/g, "\\n")}」`;
  if (left) return [`${problem}; the builder cannot cut it to the rule (${shown} still ${left.replace(/^thumbnail\.headline /, "")}), so write the six yourself`];
  return [`${problem}; the builder cuts it to ${shown}, so write the six yourself`];
}

/**
 * Why a thumbnail headline fails the channel's rule, or null. The rule is the qa stage's
 * (tools/video/qa/thumbnail.mjs thumbnailChecks, .agents/skills/youtube-video/references/visuals.md
 * §縮圖), its four checks in its words: at most THUMB_HEADLINE_MAX characters where a CJK glyph
 * counts one and a Latin word or a number counts one, at most THUMB_HEADLINE_WORDS_MAX of those,
 * no line break inside a word (the writer's `\n` or the one the renderer's column makes), and
 * still MIN_HEADLINE_PX_AT_PHONE tall at PHONE_WIDTH wide once the renderer has shrunk it to fit
 * the column, which a Latin word of eight or more letters never is.
 */
export function headlineProblem(headline) {
  const { count, words } = headlineCount(headline);
  if (count > THUMB_HEADLINE_MAX) return `thumbnail.headline counts ${count} characters (a Latin word or a number counts one); at most ${THUMB_HEADLINE_MAX} read at a glance, so say one thing in six`;
  if (words.length > THUMB_HEADLINE_WORDS_MAX) return `thumbnail.headline has ${words.length} Latin words or numbers (${words.join(", ")}); at most ${THUMB_HEADLINE_WORDS_MAX} fit the column`;
  const split = headlineSplitWords(headline);
  if (split.length) return `thumbnail.headline breaks inside the word ${split.map(({ word }) => `「${word}」`).join(", ")}; put \\n where a word ends`;
  const px = atPhoneWidth(headlineSizeEstimate(headline));
  if (px < MIN_HEADLINE_PX_AT_PHONE) return `thumbnail.headline shrinks to about ${px} px at ${PHONE_WIDTH} px wide; at least ${MIN_HEADLINE_PX_AT_PHONE} px reads on a phone, so shorten it`;
  return null;
}

const SEGMENTER = new Intl.Segmenter("zh", { granularity: "word" });
// Function words a cut headline must not end on: they bind to the word the cut took away.
const DANGLING = new Set([..."的了沒不也就才還很都把被讓和與跟第在從到比而或及之其"]);
const TRAILING = /[\s\p{P}\p{S}]+$/u;
const LEADING = /^[\s\p{P}\p{S}]+/u;
const PUNCTUATION = /^[\s\p{P}\p{S}]+$/u;
const LATIN = /[A-Za-z0-9]/;
const MIN_CUT = 3;
const overRule = ({ count, words }) => count > THUMB_HEADLINE_MAX || words.length > THUMB_HEADLINE_WORDS_MAX;
// The text on one line, a break read as the qa stage reads it: a space between two Latin runs, nothing between CJK glyphs.
const unbroken = (text) => text.replace(/(.?)\n(.?)/gsu, (_, before, after) => `${before}${LATIN.test(before) && LATIN.test(after) ? " " : ""}${after}`);

/**
 * The text on the one or two lines the column keeps whole (visuals.md §縮圖): a break the writer
 * put inside a word is taken out, and when the column would break a word of a one-line text, a
 * `\n` is put where that word starts. A second break is never added, so a text whose second
 * line the column still breaks comes back failing; clipHeadline shortens it instead.
 */
function lined(text) {
  let cut = text;
  let [split] = headlineSplitWords(cut);
  if (split?.chosen) {
    cut = unbroken(cut);
    [split] = headlineSplitWords(cut);
  }
  if (split && !split.chosen && !cut.includes("\n")) {
    const at = cut.indexOf(split.word);
    if (at > 0) cut = `${cut.slice(0, at).replace(TRAILING, "")}\n${cut.slice(at)}`;
  }
  return cut;
}

/**
 * The headline cut to the channel's rule where a word ends (Intl.Segmenter, zh), never through
 * one: 「名字沒註冊的辣椒醬」 is 「名字沒註冊」, not 「名字沒註冊的辣」. A function word the cut
 * would end on (DANGLING: a lone 第 of 第一部, a trailing 的 or 沒) is dropped while MIN_CUT
 * characters remain.
 * A headline that already fits comes back as written, stress marks and line breaks included; a
 * cut one keeps a line break that falls between words and loses the stress. When the renderer's
 * column would break the result inside a word, a `\n` is put where that word starts (lined), and
 * the result is read as the qa stage reads it (headlineProblem): while it still fails (the second
 * line too long for the column, 「Nike\n曾是代理商」), the last word goes and the rest is lined
 * again, down to MIN_CUT characters, so what the builder writes into video.json is what the qa
 * stage passes. What nothing shorter mends (a Latin word of eight or more letters is too wide
 * at any length) comes back as the longest cut, and storyWarnings says so. A first word longer
 * than the rule is cut through, as nothing shorter is left.
 */
export function clipHeadline(headline) {
  const own = String(headline ?? "").trim();
  if (!own || !headlineProblem(own)) return own;
  const plain = own.replace(/\*\*/g, "");
  const segments = [...SEGMENTER.segment(plain)].map(({ segment }) => segment);
  let kept = [];
  for (const segment of segments) {
    if (overRule(headlineCount([...kept, segment].join("")))) break;
    kept.push(segment);
  }
  let shortened = kept.length < segments.length;
  if (!kept.join("").replace(TRAILING, "").replace(LEADING, "")) {
    kept = [[...plain.replace(LEADING, "")].slice(0, THUMB_HEADLINE_MAX).join("")];
    shortened = true;
  }
  let longest = null;
  for (;;) {
    // A cut's end is tidied: the punctuation and the function word the cut left dangling go. A
    // headline that lost nothing keeps its end (「廉航怎麼賺？」 keeps the question mark).
    while (shortened && kept.length > 1 && (PUNCTUATION.test(kept.at(-1)) || (DANGLING.has(kept.at(-1)) && headlineCount(kept.slice(0, -1).join("")).count >= MIN_CUT))) kept.pop();
    const cut = lined(shortened ? kept.join("").replace(TRAILING, "").replace(LEADING, "") : plain);
    if (!headlineProblem(cut)) return cut;
    longest ??= cut;
    const shorter = kept.slice(0, -1);
    if (!shorter.length || headlineCount(shorter.join("")).count < MIN_CUT) return longest;
    kept = shorter;
    shortened = true;
  }
}

/** The story with its fields in STORY_KEYS order, as the files are kept. */
export function canonical(story) {
  const ordered = {};
  for (const key of STORY_KEYS) if (story[key] !== undefined) ordered[key] = story[key];
  for (const key of Object.keys(story)) if (!(key in ordered)) ordered[key] = story[key];
  return ordered;
}

/** Problems with schedule.json by itself: days in order, both slots each day, no story twice. */
export function scheduleProblems(schedule) {
  const problems = [];
  if (!isObject(schedule) || !Array.isArray(schedule.days)) return ["schedule.json needs days: [{ day, slots: { \"12:00\": id, \"20:00\": id } }]"];
  const seen = new Map();
  schedule.days.forEach((entry, index) => {
    if (entry?.day !== index + 1) problems.push(`days[${index}].day is ${entry?.day}, expected ${index + 1}`);
    for (const slot of SLOTS) {
      const id = entry?.slots?.[slot];
      if (typeof id !== "string" || !ID.test(id)) problems.push(`day ${index + 1} has no story at ${slot}`);
      else if (seen.has(id)) problems.push(`${id} is scheduled on day ${seen.get(id)} and day ${index + 1}`);
      else seen.set(id, index + 1);
    }
  });
  return problems;
}

/** The production order: story id -> { number, day, slot }. */
export function order(schedule) {
  const placed = new Map();
  for (const entry of schedule.days ?? []) {
    SLOTS.forEach((slot, index) => {
      const id = entry.slots?.[slot];
      if (typeof id === "string" && !placed.has(id)) placed.set(id, { number: (entry.day - 1) * SLOTS.length + index + 1, day: entry.day, slot });
    });
  }
  return placed;
}

/** Problems with series.json: the series row the stories are imported under. */
export function seriesProblems(series) {
  const problems = [];
  if (!isObject(series)) return ["series.json is not a JSON object"];
  if (typeof series.slug !== "string" || !SERIES_SLUG.test(series.slug)) problems.push("series.slug must be lowercase letters, digits and hyphens, 2-40 characters");
  if (!isText(series.title)) problems.push("series.title is missing");
  if (series.kind !== "story") problems.push('series.kind must be "story"');
  if (series.visual_tier !== "stills") problems.push('series.visual_tier must be "stills"');
  if (series.hands_off !== true) problems.push("series.hands_off must be true");
  if (!(Number.isInteger(series.target_minutes) && series.target_minutes >= 12 && series.target_minutes <= 15)) problems.push("series.target_minutes must be 12 to 15");
  if (!(Number.isInteger(series.episodes_per_day) && series.episodes_per_day >= 1 && series.episodes_per_day <= 12)) problems.push("series.episodes_per_day must be 1 to 12");
  if (!isText(series.image_model)) problems.push("series.image_model is missing");
  if (!isObject(series.look) || !isText(series.look.style) || !isText(series.look.negative)) problems.push("series.look needs a style and a negative prompt");
  else {
    if (series.look.style.length > 600) problems.push("series.look.style is over 600 characters");
    if (series.look.negative.length > 400) problems.push("series.look.negative is over 400 characters");
  }
  return problems;
}

/**
 * What a review is bound to: the story's content with its fields in order, so reformatting the
 * file changes nothing and changing a word does.
 */
export function storyHash(story) {
  return createHash("sha256").update(JSON.stringify(canonical(story))).digest("hex");
}

export const REVIEW_VERDICTS = ["pass", "fixed"];
export const REVIEW_KEYS = ["id", "reviewed", "reviewer", "story_sha256", "verdict", "sources_opened", "changes", "notes", "reviewer_only"];

/**
 * The must_verify facts (by index) whose every source is a document the worker's reader cannot
 * turn into text (a PDF, a page over its size): the reviewer read the document, the worker
 * takes the plan's word. The list is the reviewer's finding; `validate.mjs --fetch` holds it to
 * what the reader does get.
 */
export const reviewerOnly = (review) => (Array.isArray(review?.reviewer_only) ? review.reviewer_only.filter(Number.isInteger) : []);

/**
 * Problems with a story's review (reviews/<id>.json): a second reader opened the sources and
 * checked the claims against them. The review names the story it read by hash, so a story
 * edited afterwards has no review until it is read again.
 */
export function reviewProblems(review, story, fileId = review?.id) {
  const problems = [];
  if (!isObject(review)) return ["the review is not a JSON object"];
  for (const key of Object.keys(review)) if (!REVIEW_KEYS.includes(key)) problems.push(`unknown field "${key}"`);
  if (review.id !== fileId) problems.push(`id "${review.id}" does not match the file name ${fileId}.json`);
  if (typeof review.reviewed !== "string" || !DATE.test(review.reviewed)) problems.push("reviewed must be the date of the review, YYYY-MM-DD");
  if (!isText(review.reviewer)) problems.push("reviewer is missing: say who or which model read it");
  if (!REVIEW_VERDICTS.includes(review.verdict)) problems.push(`verdict must be one of ${REVIEW_VERDICTS.join(", ")}`);
  if (!(Number.isInteger(review.sources_opened) && review.sources_opened >= 0)) problems.push("sources_opened must be how many of the sources the reviewer opened");
  else if (story && review.sources_opened < Math.min(MIN_SOURCES, (story.sources ?? []).length)) problems.push(`sources_opened is ${review.sources_opened}: the reviewer opens at least ${MIN_SOURCES} sources`);
  if (!Array.isArray(review.changes) || !review.changes.every(isText)) problems.push("changes must list what the reviewer changed (empty when nothing)");
  else if (review.verdict === "fixed" && !review.changes.length) problems.push('verdict "fixed" needs the changes it made');
  else if (review.verdict === "pass" && review.changes.length) problems.push('verdict "pass" has changes: it is "fixed"');
  if (review.notes !== undefined && typeof review.notes !== "string") problems.push("notes must be text");
  else if (length(review.notes ?? "") > LIMITS.notes) problems.push(`notes is ${length(review.notes)} characters, at most ${LIMITS.notes}: the writer reads them with the story`);
  if (review.reviewer_only !== undefined) {
    const listed = review.reviewer_only;
    const claims = Array.isArray(story?.must_verify) ? story.must_verify.length : Infinity;
    if (!Array.isArray(listed) || !listed.every((each) => Number.isInteger(each) && each >= 0 && each < claims) || new Set(listed).size !== listed.length) {
      problems.push("reviewer_only must list, once each, the indexes of the must_verify facts whose sources the worker cannot read");
    }
  }
  if (typeof review.story_sha256 !== "string" || !/^[0-9a-f]{64}$/.test(review.story_sha256)) problems.push("story_sha256 must be the story's hash (validate.mjs --hash <id>)");
  else if (story && review.story_sha256 !== storyHash(story)) problems.push("the story changed after this review: read it again and record the new hash (validate.mjs --hash <id>)");
  return problems;
}

/** Read a plan directory: { series, schedule, stories: [{ id, file, story | error, review? }] }. */
export function loadPlan(dir = DEFAULT_PLAN) {
  const read = (name) => JSON.parse(readFileSync(path.join(dir, name), "utf8"));
  const storiesDir = path.join(dir, "stories");
  const reviewsDir = path.join(dir, "reviews");
  const files = existsSync(storiesDir) ? readdirSync(storiesDir).filter((name) => name.endsWith(".json")).sort() : [];
  const stories = files.map((name) => {
    const id = name.slice(0, -".json".length);
    const entry = { id, file: path.join(storiesDir, name) };
    try {
      entry.story = JSON.parse(readFileSync(entry.file, "utf8"));
    } catch (error) {
      entry.error = error.message;
    }
    const reviewFile = path.join(reviewsDir, name);
    if (existsSync(reviewFile)) {
      try {
        entry.review = JSON.parse(readFileSync(reviewFile, "utf8"));
      } catch (error) {
        entry.reviewError = error.message;
      }
    }
    return entry;
  });
  const orphans = existsSync(reviewsDir) ? readdirSync(reviewsDir).filter((name) => name.endsWith(".json") && !files.includes(name)).map((name) => name.slice(0, -".json".length)) : [];
  // What the owner approved, kept so the schedule can show which titles the fact check changed.
  const seeds = existsSync(path.join(dir, "approved-seeds.json")) ? (read("approved-seeds.json").seeds ?? []) : [];
  return { dir, series: read("series.json"), schedule: read("schedule.json"), stories, orphans, seeds, guides: siteGuides() };
}

/**
 * The slugs of the site's articles (the content packs of apps/api), for `related_guide`: a
 * story's description links to its article, and a slug nobody wrote is a dead link in it. Null
 * when the packs are not there to read.
 */
export function siteGuides(dir = path.join(ROOT, "apps", "api", "app", "guides", "content")) {
  if (!existsSync(dir)) return null;
  return new Set(readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => name.slice(0, -".json".length)));
}

/**
 * The file the server imports (apps/api video-story-import): the series row, then every story
 * in production order with its number and its publishing slot. Two things come from the
 * story's review: `caveats`, what its fact checker left for the writer (the review's notes:
 * which anecdote has no source, which figure the sources disagree on), and `reviewer_only` on
 * each fact whose sources the worker cannot read. Stories the schedule does not place are left
 * out; `planProblems` says so.
 */
export function compile(plan) {
  const placed = order(plan.schedule);
  const stories = plan.stories
    .filter((entry) => entry.story && placed.has(entry.id))
    .map((entry) => {
      const { number, day, slot } = placed.get(entry.id);
      const unread = new Set(reviewerOnly(entry.review));
      const facts = (Array.isArray(entry.story.must_verify) ? entry.story.must_verify : []).map((claim, index) => (unread.has(index) ? { ...claim, reviewer_only: true } : claim));
      return { number, ...entry.story, must_verify: facts, caveats: typeof entry.review?.notes === "string" ? entry.review.notes.trim() : "", publish: { day, slot } };
    })
    .sort((a, b) => a.number - b.number);
  return { schema_version: SCHEMA_VERSION, series: plan.series, stories };
}

export const serialize = (compiled) => `${JSON.stringify(compiled, null, 2)}\n`;

/**
 * Everything wrong with a plan. `expected` is how many stories of each category a finished plan
 * has; pass null while the plan is still being written and only the stories present are checked.
 */
export function planProblems(plan, { expected = { everyday: 40, "asia-brand": 40, tech: 20 }, regions = { jp: 24, kr: 8, tw: 8 } } = {}) {
  const problems = [];
  for (const problem of seriesProblems(plan.series)) problems.push(`series.json: ${problem}`);
  const scheduled = scheduleProblems(plan.schedule);
  for (const problem of scheduled) problems.push(`schedule.json: ${problem}`);
  const placed = scheduled.length ? new Map() : order(plan.schedule);
  const slugs = new Map();
  const titles = new Map();
  for (const entry of plan.stories) {
    if (entry.error) {
      problems.push(`${entry.id}: not valid JSON (${entry.error})`);
      continue;
    }
    for (const problem of storyProblems(entry.story, entry.id)) problems.push(`${entry.id}: ${problem}`);
    for (const [seen, key] of [[slugs, "slug"], [titles, "title"]]) {
      const value = entry.story[key];
      if (typeof value !== "string") continue;
      if (seen.has(value)) problems.push(`${entry.id}: ${key} "${value}" is also ${seen.get(value)}'s`);
      else seen.set(value, entry.id);
    }
    if (!scheduled.length && !placed.has(entry.id)) problems.push(`${entry.id}: not in schedule.json`);
    const guide = entry.story.related_guide;
    if (plan.guides && typeof guide === "string" && !plan.guides.has(guide)) problems.push(`${entry.id}: related_guide "${guide}" is not an article of the site (apps/api/app/guides/content/${guide}.json)`);
    // A review that is there must be of this text; a finished plan has one for every story.
    if (entry.reviewError) problems.push(`${entry.id}: reviews/${entry.id}.json is not valid JSON (${entry.reviewError})`);
    else if (entry.review) for (const problem of reviewProblems(entry.review, entry.story, entry.id)) problems.push(`${entry.id}: review: ${problem}`);
    else if (expected) problems.push(`${entry.id}: no review yet (reviews/${entry.id}.json)`);
  }
  for (const id of plan.orphans ?? []) problems.push(`${id}: reviews/${id}.json has no story`);
  if (expected) {
    const ids = new Set(plan.stories.map((entry) => entry.id));
    for (const id of placed.keys()) if (!ids.has(id)) problems.push(`${id}: scheduled, but stories/${id}.json does not exist`);
    const sound = plan.stories.filter((entry) => entry.story);
    for (const [category, count] of Object.entries(expected)) {
      const have = sound.filter((entry) => entry.story.category === category).length;
      if (have !== count) problems.push(`${have} stories are ${category}, expected ${count}`);
    }
    for (const [region, count] of Object.entries(regions)) {
      const have = sound.filter((entry) => entry.story.category === "asia-brand" && entry.story.region === region).length;
      if (have !== count) problems.push(`${have} asia-brand stories are ${region}, expected ${count}`);
    }
    const total = Object.values(expected).reduce((sum, count) => sum + count, 0);
    if ((plan.schedule.days ?? []).length * SLOTS.length !== total) problems.push(`the schedule has ${(plan.schedule.days ?? []).length} days, expected ${total / SLOTS.length}`);
  }
  return problems;
}

/** Whether the generated files on disk (stories.json, SCHEDULE.md) are what the sources give now. */
export function compiledCurrent(plan) {
  const same = (name, expected) => existsSync(path.join(plan.dir, name)) && readFileSync(path.join(plan.dir, name), "utf8") === expected;
  return same("stories.json", serialize(compile(plan))) && same("SCHEDULE.md", scheduleMarkdown(plan));
}

const CATEGORY_LABELS = { everyday: "日常用品與隱形標準", "asia-brand": "日韓台旅途品牌", tech: "科技與軟體" };
const REGION_LABELS = { global: "", jp: "日本", kr: "韓國", tw: "台灣" };

/** SCHEDULE.md: the fifty days as a table a person reads, generated from the plan. */
export function scheduleMarkdown(plan) {
  const byId = new Map(plan.stories.filter((entry) => entry.story).map((entry) => [entry.id, entry.story]));
  const cell = (id) => {
    const story = byId.get(id);
    return story ? `${id} ${String(story.title).replaceAll("|", "｜")}` : `${id}（還沒寫）`;
  };
  const lines = [
    "# 50 天排程",
    "",
    "這個檔是產生的，不要手改：改 `schedule.json` 或故事檔之後跑 `node tools/video/story-plans/validate.mjs --write`。",
    "",
    "第 1 天是第一個上架日，起始日期在上線時決定（`docs/videos/STORY.md`）。時間是台北時間。",
    "",
    "| 天 | 12:00 | 20:00 |",
    "| --- | --- | --- |",
    ...(plan.schedule.days ?? []).map((entry) => `| ${entry.day} | ${cell(entry.slots?.["12:00"])} | ${cell(entry.slots?.["20:00"])} |`),
    "",
    "## 分類",
    "",
    "| 分類 | 數量 |",
    "| --- | --- |",
    ...Object.entries(CATEGORY_LABELS).map(([category, label]) => {
      const stories = [...byId.values()].filter((story) => story.category === category);
      const regions = Object.entries(REGION_LABELS)
        .filter(([region, name]) => name && stories.some((story) => story.region === region))
        .map(([region, name]) => `${name} ${stories.filter((story) => story.region === region).length}`);
      return `| ${label} | ${stories.length}${category === "asia-brand" && regions.length ? `（${regions.join("、")}）` : ""} |`;
    }),
    "",
  ];
  // The owner approved working titles; the fact check changed some. Both are shown side by side.
  const bar = (value) => String(value).replaceAll("|", "｜");
  const changed = (plan.seeds ?? []).filter((seed) => byId.has(seed.id) && (byId.get(seed.id).title !== seed.title || byId.get(seed.id).subject !== seed.subject));
  if (changed.length) {
    lines.push(
      "## 跟核准時不一樣的標題",
      "",
      "寫企劃時查核過每個標題靠的說法；說法跟來源不一樣的，標題改成來源撐得住的版本。",
      "",
      "| 代號 | 核准時 | 現在 |",
      "| --- | --- | --- |",
      ...changed.map((seed) => {
        const story = byId.get(seed.id);
        const subject = story.subject !== seed.subject ? `（主題：${bar(seed.subject)} → ${bar(story.subject)}）` : "";
        return `| ${seed.id} | ${bar(seed.title)} | ${bar(story.title)}${subject} |`;
      }),
      "",
    );
  }
  // The facts only the reviewer could read the evidence for, so the owner sees which they are.
  const unread = plan.stories.flatMap((entry) =>
    reviewerOnly(entry.review)
      .map((index) => ({ id: entry.id, index, claim: entry.story?.must_verify?.[index] }))
      .filter((fact) => fact.claim),
  );
  if (unread.length) {
    lines.push(
      "## 只有查核的人讀得到證據的事實",
      "",
      "這幾條事實的來源都是主機工人讀不到的文件（PDF、太大的頁面）。查核的人讀過文件，也找過工人讀得到的頁面但沒有；製作時工人以企劃為準，只確認稿子沒有多說。",
      "",
      "| 代號 | 事實 | 標題靠它 |",
      "| --- | --- | --- |",
      ...unread.map((fact) => `| ${fact.id} | ${bar(fact.claim.claim)} | ${fact.claim.core === true ? "是" : ""} |`),
      "",
    );
  }
  return lines.join("\n");
}
