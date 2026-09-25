// `i18n-sheet` and `i18n-merge`: caption and metadata translations without hand-kept hashes.
//
// A translation file (docs/videos/<slug>/i18n/<locale>.json) keys each line by its id and records
// the hash of the zh-TW text it was made from, so lint and `captions` can tell a stale line from
// a current one. Agents should never compute those hashes. `i18n-sheet` writes a worksheet in the
// work directory with every zh-TW line beside its current translation, marking the lines to do;
// the translator fills in `text`; `i18n-merge` checks the sheet against the script as it is now
// and writes the translation file, hashes included. A line whose zh-TW text changed after the
// sheet was made is left out and reported, so it cannot be merged against the wrong source.
import path from "node:path";
import { parseArgs } from "node:util";

import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, textHash } from "../core/schema.mjs";
import { loadProject } from "../core/state.mjs";
import { TITLE_MAX_CHARS } from "../core/metadata.mjs";

export const TARGET_LOCALES = LOCALES.filter((locale) => locale !== NARRATION_LOCALE);

const sheetFile = (workdir, locale) => path.join(workdir, "i18n", `${locale}.todo.json`);
const translationFile = (dir, locale) => path.join(dir, "i18n", `${locale}.json`);

/** The worksheet for one locale: every line with its current translation, the ones to do marked. */
export function buildSheet(doc, translation, locale) {
  const current = translation ?? {};
  const lines = [];
  for (const { scene, line } of eachLine(doc)) {
    const entry = current.lines?.[line.id];
    const fresh = entry && entry.source_hash === textHash(line.text) && entry.text;
    lines.push({ id: line.id, scene: scene.id, todo: !fresh, source: line.text, text: fresh ? entry.text : "" });
  }
  const chapters = doc.scenes
    .filter((scene) => scene.chapter)
    .map((scene) => ({ scene: scene.id, source: scene.chapter, text: current.chapters?.[scene.id] ?? "" }));
  return {
    locale,
    slug: doc.slug,
    note: "Fill every empty `text` (the lines marked todo, the chapters, the title, the description, the tags). Keep `id`, `scene` and `source` as they are.",
    title: { source: doc.youtube.title, text: current.title ?? "" },
    description: { source: doc.youtube.description, text: current.description ?? "" },
    tags: { source: doc.youtube.tags, text: current.tags ?? [] },
    chapters,
    lines,
  };
}

/** The translation file a filled sheet makes, and what could not go in. */
export function mergeSheet(doc, sheet, previous) {
  const problems = [];
  const byId = new Map(sheet.lines.map((entry) => [entry.id, entry]));
  const lines = {};
  for (const { line } of eachLine(doc)) {
    const entry = byId.get(line.id);
    const text = typeof entry?.text === "string" ? entry.text.trim() : "";
    if (!entry || !text) {
      problems.push(`${line.id}: not translated`);
      if (previous?.lines?.[line.id]) lines[line.id] = previous.lines[line.id];
      continue;
    }
    if (entry.source !== line.text) {
      problems.push(`${line.id}: the zh-TW line changed after the sheet was made; make a new sheet`);
      if (previous?.lines?.[line.id]) lines[line.id] = previous.lines[line.id];
      continue;
    }
    lines[line.id] = { source_hash: textHash(line.text), text };
  }
  const title = String(sheet.title?.text ?? "").trim();
  const description = String(sheet.description?.text ?? "").trim();
  if (!title) problems.push("title: not translated");
  else if (title.length > TITLE_MAX_CHARS || /[<>]/.test(title)) problems.push(`title: at most ${TITLE_MAX_CHARS} characters and no angle brackets`);
  if (!description) problems.push("description: not translated");
  else if (/[<>]/.test(description)) problems.push("description: no angle brackets");
  const tags = Array.isArray(sheet.tags?.text) ? sheet.tags.text.map((tag) => String(tag).trim()).filter(Boolean) : [];
  const chapters = {};
  for (const chapter of sheet.chapters ?? []) {
    const text = String(chapter.text ?? "").trim();
    if (text) chapters[chapter.scene] = text;
    else problems.push(`chapter ${chapter.scene}: not translated`);
  }
  return { translation: { ...previous, title, description, tags, chapters, lines }, problems };
}

function options(args) {
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, locale: { type: "string" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("needs --slug (or --file)");
  const locales = values.locale ? values.locale.split(",").map((locale) => locale.trim()) : TARGET_LOCALES;
  for (const locale of locales) if (!TARGET_LOCALES.includes(locale)) throw new UsageError(`--locale must be among ${TARGET_LOCALES.join(", ")}`);
  return { ...values, locales };
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = options(args);
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc } = project;
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  if (command === "i18n-sheet") {
    for (const locale of values.locales) {
      const sheet = buildSheet(doc, project.translations[locale], locale);
      atomicWrite(sheetFile(workdir, locale), `${JSON.stringify(sheet, null, 2)}\n`);
      ctx.stdout.write(`${locale}: ${sheet.lines.filter((line) => line.todo).length} of ${sheet.lines.length} lines to translate; ${sheetFile(workdir, locale)}\n`);
    }
    return EXIT.ok;
  }
  let incomplete = false;
  for (const locale of values.locales) {
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
