// `i18n-sheet` and `i18n-merge`: caption and metadata translations without hand-kept hashes.
//
// A translation file (docs/videos/<slug>/i18n/<locale>.json) keys each line by its id and records
// the hash of the zh-TW text it was made from, so lint and `captions` can tell a stale line from
// a current one; the title, description, tags and chapter titles have theirs in `source_hashes`
// (core/translations.mjs). Agents should never compute those hashes. `i18n-sheet` writes a
// worksheet in the work directory with every zh-TW line, chapter and YouTube field beside its
// current translation, marking the ones to do; the translator fills in `text`; `i18n-merge` checks
// the sheet against the script as it is now and writes the translation file, hashes included.
// Anything whose zh-TW text changed after the sheet was made is left out and reported, so it
// cannot be merged against the wrong source. `--parts` narrows a sheet to what the owner chose for
// the locale (docs/videos/LANGUAGES.md): "metadata" is the title, description, tags and chapter
// names, "captions" the lines; a part left out keeps whatever translation it had.
import path from "node:path";
import { parseArgs } from "node:util";

import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, narrationLocale, textHash } from "../core/schema.mjs";
import { readLanguages } from "../core/stages.mjs";
import { ARTIFACTS, dubArtifacts, loadProject } from "../core/state.mjs";
import { TITLE_MAX_CHARS } from "../core/metadata.mjs";
import { speechHash } from "../core/timeline.mjs";
import { chapterScenes, METADATA_FIELDS, metadataStatus, sourceHashes } from "../core/translations.mjs";
import { defaultRate, lineBudgets } from "../dubs/plan.mjs";

export const TARGET_LOCALES = LOCALES.filter((locale) => locale !== NARRATION_LOCALE);
/** The locales one video is translated into: every caption locale but the one it is narrated in. */
export const targetLocales = (doc) => LOCALES.filter((locale) => locale !== narrationLocale(doc));
// What a sheet can hold; a dub reads the captions' lines, so it never needs a part of its own.
export const SHEET_PARTS = ["metadata", "captions"];

const sheetFile = (workdir, locale) => path.join(workdir, "i18n", `${locale}.todo.json`);
const translationFile = (dir, locale) => path.join(dir, "i18n", `${locale}.json`);

const SHEET_NOTE = "Fill the `text` of everything marked todo: lines, chapters, the title, the description, the tags. The rest already has a current translation. Keep `id`, `scene`, `source` and `todo` as they are.";
const PART_NOTES = { metadata: "This sheet holds only the title, the description, the tags and the chapter names; the lines are not wanted for this locale.", captions: "This sheet holds only the lines; the title, description, tags and chapter names are not wanted for this locale." };
const BUDGET_NOTE = " `max_chars` is how many characters a line's dub may have (docs/videos/DUBS.md): the translation is also read aloud in the time the narration line takes, so stay under it.";

const partsOf = (sheet) => (Array.isArray(sheet?.parts) && sheet.parts.length ? sheet.parts : SHEET_PARTS);

/**
 * The worksheet for one locale: every line, chapter and YouTube field with its current
 * translation. One whose zh-TW source changed since the merge, or that was merged before its source
 * was hashed, is marked todo with an empty `text`, like a missing one. With `budgets` (line id to
 * characters, from the narration timeline), each line also says how long its dub may be. `parts`
 * narrows the sheet: without "captions" it has no lines, without "metadata" no title,
 * description, tags or chapters (those fields are null and the list empty).
 */
export function buildSheet(doc, translation, locale, budgets = null, parts = SHEET_PARTS) {
  const current = translation ?? {};
  const wantLines = parts.includes("captions");
  const wantMetadata = parts.includes("metadata");
  const lines = [];
  for (const { scene, line } of wantLines ? eachLine(doc) : []) {
    const entry = current.lines?.[line.id];
    const fresh = entry && entry.source_hash === textHash(line.text) && entry.text;
    lines.push({ id: line.id, scene: scene.id, todo: !fresh, source: line.text, text: fresh ? entry.text : "", ...(budgets ? { max_chars: budgets[line.id] } : {}) });
  }
  const state = metadataStatus(doc, current);
  const chapters = chapterScenes(doc).map((scene) => {
    const fresh = state.chapters[scene.id] === "current";
    return { scene: scene.id, todo: !fresh, source: scene.chapter, text: fresh ? current.chapters[scene.id] : "" };
  });
  const field = (name, empty) => {
    const fresh = state[name] === "current";
    return { todo: !fresh, source: doc.youtube[name], text: fresh ? current[name] ?? empty : empty };
  };
  const only = parts.length === 1 ? ` ${PART_NOTES[parts[0]]}` : "";
  return {
    locale,
    slug: doc.slug,
    parts: [...parts],
    note: `${SHEET_NOTE}${only}${budgets ? BUDGET_NOTE : ""}`,
    title: wantMetadata ? field("title", "") : null,
    description: wantMetadata ? field("description", "") : null,
    tags: wantMetadata ? field("tags", []) : null,
    chapters: wantMetadata ? chapters : [],
    lines,
  };
}

/** What a sheet leaves to translate, for the CLI's report. */
export function sheetTodo(sheet) {
  const count = (entries) => `${entries.filter((entry) => entry.todo).length} of ${entries.length}`;
  const parts = partsOf(sheet).includes("captions") ? [`${count(sheet.lines)} lines`] : [];
  if (sheet.chapters?.length) parts.push(`${count(sheet.chapters)} chapters`);
  for (const name of METADATA_FIELDS) if (sheet[name]?.todo) parts.push(`the ${name}`);
  return parts.join(", ") || "nothing";
}

const sameSource = (a, b) => JSON.stringify(a) === JSON.stringify(b);

/** The lines a filled sheet merges, keeping a previous translation where the sheet has none usable. */
function mergeLines(doc, sheet, before, problems) {
  const narration = narrationLocale(doc);
  const byId = new Map((sheet.lines ?? []).map((entry) => [entry.id, entry]));
  const lines = {};
  for (const { line } of eachLine(doc)) {
    const entry = byId.get(line.id);
    const text = typeof entry?.text === "string" ? entry.text.trim() : "";
    if (!entry || !text) {
      problems.push(`${line.id}: not translated`);
      if (before.lines?.[line.id]) lines[line.id] = before.lines[line.id];
      continue;
    }
    if (entry.source !== line.text) {
      problems.push(`${line.id}: the ${narration} line changed after the sheet was made; make a new sheet`);
      if (before.lines?.[line.id]) lines[line.id] = before.lines[line.id];
      continue;
    }
    lines[line.id] = { source_hash: textHash(line.text), text };
  }
  return lines;
}

/**
 * The translation file a filled sheet makes, and what could not go in. Whatever goes in is
 * recorded with the hash of its zh-TW source; whatever cannot keeps its previous translation and
 * hash, so the next sheet marks it again. Only the scenes that open a chapter now get a chapter
 * entry: the package step reads `chapters` by scene id, so a chapter that moved leaves nothing
 * behind under its old scene.
 */
export function mergeSheet(doc, sheet, previous) {
  const narration = narrationLocale(doc);
  const problems = [];
  const before = previous ?? {};
  const kept = before.source_hashes ?? {};
  const hashes = sourceHashes(doc);
  const parts = partsOf(sheet);
  // A part the sheet does not hold keeps its previous translation and hashes untouched.
  if (!parts.includes("metadata")) {
    const lines = parts.includes("captions") ? mergeLines(doc, sheet, before, problems) : { ...(before.lines ?? {}) };
    const translation = { title: before.title, description: before.description, tags: before.tags, chapters: { ...(before.chapters ?? {}) }, source_hashes: { ...kept, chapters: { ...(kept.chapters ?? {}) } }, lines };
    for (const [key, value] of Object.entries(before)) if (!Object.hasOwn(translation, key)) translation[key] = value;
    for (const key of METADATA_FIELDS) if (translation[key] === undefined) delete translation[key];
    return { translation, problems };
  }
  const lines = parts.includes("captions") ? mergeLines(doc, sheet, before, problems) : { ...(before.lines ?? {}) };
  const title = String(sheet.title?.text ?? "").trim();
  const description = String(sheet.description?.text ?? "").trim();
  const tags = Array.isArray(sheet.tags?.text) ? sheet.tags.text.map((tag) => String(tag).trim()).filter(Boolean) : [];
  const fields = {
    title: { value: title, empty: !title, invalid: title.length > TITLE_MAX_CHARS || /[<>]/.test(title) ? `at most ${TITLE_MAX_CHARS} characters and no angle brackets` : null },
    description: { value: description, empty: !description, invalid: /[<>]/.test(description) ? "no angle brackets" : null },
    tags: { value: tags, empty: !tags.length && doc.youtube.tags.length > 0, invalid: null },
  };
  const values = {};
  const recorded = { chapters: {} };
  for (const [name, { value, empty, invalid }] of Object.entries(fields)) {
    const changed = !sameSource(sheet[name]?.source, doc.youtube[name]);
    const problem = empty ? "not translated" : changed ? `the ${narration} ${name} changed after the sheet was made; make a new sheet` : invalid;
    if (!problem) {
      values[name] = value;
      recorded[name] = hashes[name];
      continue;
    }
    problems.push(`${name}: ${problem}`);
    values[name] = before[name];
    recorded[name] = kept[name];
  }

  const bySceneId = new Map((sheet.chapters ?? []).map((entry) => [entry.scene, entry]));
  const chapters = {};
  for (const scene of chapterScenes(doc)) {
    const entry = bySceneId.get(scene.id);
    const text = String(entry?.text ?? "").trim();
    const problem = !text ? "not translated" : entry.source !== scene.chapter ? `the ${narration} chapter title changed after the sheet was made; make a new sheet` : null;
    if (!problem) {
      chapters[scene.id] = text;
      recorded.chapters[scene.id] = hashes.chapters[scene.id];
      continue;
    }
    problems.push(`chapter ${scene.id}: ${problem}`);
    if (before.chapters?.[scene.id]) {
      chapters[scene.id] = before.chapters[scene.id];
      recorded.chapters[scene.id] = kept.chapters?.[scene.id];
    }
  }

  const translation = { ...values, chapters, source_hashes: recorded, lines };
  for (const [key, value] of Object.entries(before)) if (!Object.hasOwn(translation, key)) translation[key] = value;
  return { translation, problems };
}

function options(args) {
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, locale: { type: "string" }, parts: { type: "string" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("needs --slug (or --file)");
  const parts = values.parts ? values.parts.split(",").map((part) => part.trim()).filter(Boolean) : SHEET_PARTS;
  for (const part of parts) if (!SHEET_PARTS.includes(part)) throw new UsageError(`--parts must be among ${SHEET_PARTS.join(", ")} (a dub reads the captions' lines)`);
  if (!parts.length) throw new UsageError("--parts names at least one part");
  // The locales are checked in run(), once the video's narration language is known.
  const locales = values.locale ? values.locale.split(",").map((locale) => locale.trim()) : null;
  return { ...values, locales, parts: SHEET_PARTS.filter((part) => parts.includes(part)) };
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = options(args);
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc } = project;
  // The locales to translate into depend on the narration language, so they are checked once the video is read.
  const targets = targetLocales(doc);
  const locales = values.locales ?? targets;
  for (const locale of locales) if (!targets.includes(locale)) throw new UsageError(`--locale must be among ${targets.join(", ")}`);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  if (command === "i18n-sheet") {
    // Once the narration exists, each line's slot is known, and so is how long its dub may be;
    // the budgets go on the sheet when the owner chose a dub for the locale, or without a choice.
    const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    const timed = timeline && timeline.speech_hash === speechHash(doc, project.lexicon);
    const languages = readLanguages(workdir);
    for (const locale of locales) {
      const dubbed = timed && values.parts.includes("captions") && (!languages || languages.locales[locale]?.dub === true);
      const fit = dubbed ? readJson(dubArtifacts(workdir, locale).fit, null) : null;
      const budgets = dubbed ? lineBudgets(timeline, fit?.rates?.measured ?? defaultRate(locale, doc, timeline)) : null;
      const sheet = buildSheet(doc, project.translations[locale], locale, budgets, values.parts);
      atomicWrite(sheetFile(workdir, locale), `${JSON.stringify(sheet, null, 2)}\n`);
      const scope = values.parts.length < SHEET_PARTS.length ? ` (${values.parts.join(", ")} only)` : "";
      ctx.stdout.write(`${locale}: to translate ${sheetTodo(sheet)}; ${sheetFile(workdir, locale)}${scope}${budgets ? " (with max_chars for the dub)" : ""}\n`);
    }
    return EXIT.ok;
  }
  let incomplete = false;
  for (const locale of locales) {
    const sheet = readJson(sheetFile(workdir, locale), null);
    if (!sheet) throw new UsageError(`no sheet for ${locale}; run i18n-sheet first`);
    const { translation, problems } = mergeSheet(doc, sheet, project.translations[locale]);
    atomicWrite(translationFile(project.dir, locale), `${JSON.stringify(translation, null, 2)}\n`);
    ctx.stdout.write(`${locale}: ${Object.keys(translation.lines).length} lines written to ${translationFile(project.dir, locale)}${problems.length ? `; ${problems.length} problems` : ""}\n`);
    for (const problem of problems) ctx.stdout.write(`  ${problem}\n`);
    incomplete ||= problems.length > 0;
  }
  return incomplete ? EXIT.lint : EXIT.ok;
}
