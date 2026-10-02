// A long translation worksheet asked in bounded units (docs/videos/LANGUAGES.md).
//
// The translator and the caption reviewer each answer a whole worksheet in one model call, and
// the answer repeats every line of it. On 2026-09-29 a 94-line sheet took the translator 302 s
// on a subscription, past the web route's 295 s (nginx and Node's fetch both stop at 300 s): the
// server recorded the run as ok and paid for, and the worker never saw its answer. A sheet longer
// than one unit is therefore asked in parts: its metadata on its own, and its lines still to
// translate in runs of at most UNIT_LINES lines and UNIT_CHARS characters. Each part is
// translated and then reviewed, and each answer is kept in <workdir>/i18n/<locale>.units.json
// under the hash of what was asked, so a round that stops halfway resumes with the next request
// nobody answered instead of paying for an answered one again. Nothing is merged until every part
// has its own review. A sheet that fits one unit is asked whole, as it always was.
import { createHash } from "node:crypto";
import { rmSync } from "node:fs";
import path from "node:path";

import { atomicWrite, readJson } from "../core/paths.mjs";

/** At most this many lines in one unit: about 80 s of a subscription translator at 2026-09-29's 3.2 s a line. */
export const UNIT_LINES = 24;
/** And at most this many characters of source and current text, for a script of long lines. */
export const UNIT_CHARS = 2400;

const METADATA_NAMES = ["title", "description", "tags"];
const size = (line) => String(line?.source ?? "").length + String(line?.text ?? "").length;
const metadataTodo = (sheet) => Boolean(METADATA_NAMES.some((name) => sheet[name]?.todo) || sheet.thumbnail?.todo || (sheet.chapters ?? []).some((chapter) => chapter?.todo));
const unitsFile = (workdir, locale) => path.join(workdir, "i18n", `${locale}.units.json`);

/**
 * The units a worksheet is asked in: the sheet itself when its lines fit one, else a metadata unit
 * (when the sheet holds metadata with something to do) and runs of the lines marked todo. A unit
 * is a worksheet of its own, with the sheet's identity, its own `parts` and a note saying which
 * part it is; a lines unit holds no metadata, so the prompt's "fill only what it holds" applies.
 */
export function sheetUnits(sheet, { lines: maxLines = UNIT_LINES, chars: maxChars = UNIT_CHARS } = {}) {
  const all = sheet.lines ?? [];
  if (all.length <= maxLines && all.reduce((sum, line) => sum + size(line), 0) <= maxChars) return [sheet];
  const units = [];
  if ((sheet.parts ?? []).includes("metadata") && metadataTodo(sheet)) units.push({ ...sheet, parts: ["metadata"], lines: [] });
  let run = [];
  let chars = 0;
  const close = () => {
    if (run.length) units.push({ ...sheet, parts: ["captions"], title: null, description: null, tags: null, thumbnail: null, chapters: [], lines: run });
    run = [];
    chars = 0;
  };
  for (const line of all.filter((each) => each.todo)) {
    if (run.length >= maxLines || (run.length && chars + size(line) > maxChars)) close();
    run.push(line);
    chars += size(line);
  }
  close();
  if (!units.length) return [sheet];
  return units.map((unit, index) => ({
    ...unit,
    note: `${sheet.note ?? ""} This is part ${index + 1} of ${units.length} of the ${sheet.locale} worksheet: fill what it holds; the other parts are asked on their own.`.trim(),
  }));
}

/** The hash a unit's answers are kept under: the worksheet asked for and the narration language. */
export function unitKey(unit, sourceLocale = null) {
  return createHash("sha256").update(JSON.stringify({ worksheet: unit, source_locale: sourceLocale })).digest("hex");
}

/**
 * The video a unit is shown: all of it for the whole sheet and for the metadata, only the scenes
 * its lines are in for a lines unit, so the request stays the size of the unit.
 */
export function unitVideo(video, unit, whole) {
  if (whole || unit.parts.includes("metadata") || !Array.isArray(video?.scenes)) return video;
  const scenes = new Set(unit.lines.map((line) => line.scene));
  return { ...video, scenes: video.scenes.filter((scene) => scenes.has(scene.id)) };
}

/**
 * What leaves a unit's answer unusable before it is kept, or null: a line of the unit missing from
 * the answer, or left empty. The metadata is i18n-merge's to check, as it always was.
 */
export function unitGaps(worksheet, unit) {
  const answered = new Map((worksheet?.lines ?? []).filter((line) => typeof line?.id === "string").map((line) => [line.id, line.text]));
  const gaps = (unit.lines ?? []).filter((line) => typeof answered.get(line.id) !== "string" || !answered.get(line.id).trim()).map((line) => line.id);
  if (!gaps.length) return null;
  return `left ${gaps.length} of ${unit.lines.length} lines out or empty (${gaps.slice(0, 5).join(", ")}${gaps.length > 5 ? ", …" : ""})`;
}

/**
 * The whole worksheet again from its reviewed units: each line's text from the unit holding it,
 * the metadata's texts from the metadata unit, and everything else (ids, sources, budgets, the
 * lines already current) from the sheet as i18n-sheet wrote it.
 */
export function assembleSheet(sheet, reviewed) {
  const texts = new Map();
  let metadata = null;
  for (const unit of reviewed) {
    if (unit.parts?.includes("metadata")) metadata = unit;
    for (const line of unit.lines ?? []) if (typeof line?.id === "string") texts.set(line.id, line.text);
  }
  const text = (entry, answer) => (entry ? { ...entry, text: answer?.text ?? entry.text } : entry);
  const chapters = new Map((metadata?.chapters ?? []).map((chapter) => [chapter?.scene, chapter]));
  return {
    ...sheet,
    ...(metadata
      ? {
          ...Object.fromEntries(METADATA_NAMES.map((name) => [name, text(sheet[name], metadata[name])])),
          thumbnail: sheet.thumbnail && metadata.thumbnail ? { ...sheet.thumbnail, text: metadata.thumbnail.text } : sheet.thumbnail,
          chapters: (sheet.chapters ?? []).map((chapter) => text(chapter, chapters.get(chapter.scene))),
        }
      : {}),
    lines: (sheet.lines ?? []).map((line) => (texts.has(line.id) ? { ...line, text: texts.get(line.id) } : line)),
  };
}

/**
 * The units whose answers i18n-merge refused, read from its report ("  <line id>: …",
 * "  title: …", "  chapter <scene>: …"): those are asked again, and the others stay kept. Every
 * unit when the report names none of them.
 */
export function refusedUnits(out, units) {
  const heads = String(out ?? "")
    .split("\n")
    .filter((line) => /^\s/.test(line) && line.includes(":") && !line.trim().startsWith("note:"))
    .map((line) => line.trim().slice(0, line.trim().indexOf(":")));
  const metadata = heads.some((head) => METADATA_NAMES.includes(head) || head.startsWith("chapter "));
  const refused = units.filter((unit) => (metadata && unit.parts.includes("metadata")) || (unit.lines ?? []).some((line) => heads.includes(line.id)));
  return refused.length ? refused : units;
}

/** The answers kept for a locale's units, by unitKey: { translated, reviewed? }. Nothing when unreadable. */
export function readUnits(workdir, locale) {
  try {
    const kept = readJson(unitsFile(workdir, locale), null);
    return kept?.locale === locale && kept.units && typeof kept.units === "object" ? kept.units : {};
  } catch {
    return {};
  }
}

/** Keep the answers of the units still asked; a unit no longer asked (its lines changed) is dropped. */
export function writeUnits(workdir, locale, kept, keys) {
  const units = Object.fromEntries(keys.filter((key) => kept[key]).map((key) => [key, kept[key]]));
  atomicWrite(unitsFile(workdir, locale), `${JSON.stringify({ schema_version: 1, locale, units }, null, 2)}\n`);
}

/** Forget a locale's units once its translation is merged, or once nothing is left to translate. */
export function clearUnits(workdir, locale) {
  rmSync(unitsFile(workdir, locale), { force: true });
}
