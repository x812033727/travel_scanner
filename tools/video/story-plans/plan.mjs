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
export const LIMITS = { title: 60, logline: 120, question: 120, takeaway: 120, subject: 40, pointMin: 60, pointMax: 400, headline: 12, appearance: 800, claim: 200, supports: 240, imageNotes: 400 };

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

const hostOf = (url) => {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
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
    if (typeof source.url !== "string" || !HTTPS.test(source.url)) problems.push(`${where}.url must be an https URL`);
    else if (urls.has(source.url)) problems.push(`${where}.url repeats an earlier source`);
    else urls.add(source.url);
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
  else if (length(story.thumbnail.headline) > LIMITS.headline) problems.push(`thumbnail.headline is ${length(story.thumbnail.headline)} characters, at most ${LIMITS.headline}`);
  return problems;
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
export const REVIEW_KEYS = ["id", "reviewed", "reviewer", "story_sha256", "verdict", "sources_opened", "changes", "notes"];

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
  return { dir, series: read("series.json"), schedule: read("schedule.json"), stories, orphans };
}

/**
 * The file the server imports (apps/api video-story-import): the series row, then every story
 * in production order with its number and its publishing slot. Stories the schedule does not
 * place are left out; `planProblems` says so.
 */
export function compile(plan) {
  const placed = order(plan.schedule);
  const stories = plan.stories
    .filter((entry) => entry.story && placed.has(entry.id))
    .map((entry) => {
      const { number, day, slot } = placed.get(entry.id);
      return { number, ...entry.story, publish: { day, slot } };
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
  return lines.join("\n");
}
