import assert from "node:assert/strict";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { textHash } from "../core/schema.mjs";
import { buildSheet } from "../i18n/cli.mjs";
import { assembleSheet, clearUnits, readUnits, refusedUnits, sheetUnits, UNIT_CHARS, UNIT_LINES, unitGaps, unitKey, unitVideo, writeUnits } from "./sheet-units.mjs";

// The fixture's seven lines, in three scenes: k7p2 m4qa (hook), x9fe b3tn r8wd (questions), h2cz p5vs (wrap).
const sheet = (translation = null, parts = undefined, budgets = null) => buildSheet(fixture(), translation, "en", budgets, parts);
const filled = (unit) => ({ ...unit, lines: unit.lines.map((line) => ({ ...line, text: line.text || `en ${line.id}` })) });

test("a sheet whose lines fit one unit is asked whole, as the same object", () => {
  const whole = sheet();
  assert.deepEqual(sheetUnits(whole), [whole]);
  assert.equal(sheetUnits(whole)[0], whole);
  assert.ok(UNIT_LINES >= 20 && UNIT_CHARS >= 2000, "the defaults hold a usual scene run");
});

test("a long sheet is asked as its metadata and runs of its todo lines, within the line and character limits", () => {
  const whole = sheet();
  const units = sheetUnits(whole, { lines: 3, chars: 10_000 });
  assert.deepEqual(units.map((unit) => [unit.parts, unit.lines.map((line) => line.id)]), [
    [["metadata"], []],
    [["captions"], ["k7p2", "m4qa", "x9fe"]],
    [["captions"], ["b3tn", "r8wd", "h2cz"]],
    [["captions"], ["p5vs"]],
  ]);
  const [metadata, lines] = units;
  assert.deepEqual([metadata.title, metadata.chapters, metadata.thumbnail], [whole.title, whole.chapters, whole.thumbnail], "the metadata unit carries every metadata entry");
  assert.deepEqual([lines.title, lines.description, lines.tags, lines.thumbnail, lines.chapters], [null, null, null, null, []], "a lines unit holds no metadata");
  assert.ok(units.every((unit) => unit.slug === whole.slug && unit.locale === "en"), "the sheet's identity travels with every unit");
  assert.deepEqual(lines.lines[0], whole.lines[0], "ids, scenes, sources and todo flags as the sheet has them");
  assert.match(units[2].note, /part 3 of 4 of the en worksheet/);
  assert.ok(units[2].note.startsWith(whole.note));

  // A run closes before it passes the characters, one long line still goes alone.
  const byChars = sheetUnits(whole, { lines: 50, chars: 70 });
  assert.deepEqual(byChars.slice(1).map((unit) => unit.lines.map((line) => line.id)), [["k7p2", "m4qa"], ["x9fe", "b3tn", "r8wd"], ["h2cz", "p5vs"]]);
  assert.deepEqual(sheetUnits(whole, { lines: 50, chars: 10 }).slice(1).map((unit) => unit.lines.length), [1, 1, 1, 1, 1, 1, 1]);
});

test("only what is still to do goes into units: current lines stay out, a captions-only sheet has no metadata unit", () => {
  const done = Object.fromEntries(["k7p2", "m4qa", "x9fe"].map((id) => [id, fixture().scenes.flatMap((scene) => scene.lines).find((line) => line.id === id)]));
  // Three lines already translated: they are current in the sheet and are not asked again.
  const current = buildSheet(fixture(), { lines: Object.fromEntries(Object.entries(done).map(([id, line]) => [id, { source_hash: textHash(line.text), text: `en ${id}` }])) }, "en", null, ["captions"]);
  assert.equal(current.lines.filter((line) => !line.todo).length, 3);
  const units = sheetUnits(current, { lines: 3, chars: 10_000 });
  assert.deepEqual(units.map((unit) => [unit.parts, unit.lines.map((line) => line.id)]), [[["captions"], ["b3tn", "r8wd", "h2cz"]], [["captions"], ["p5vs"]]]);

  // Every line current and only the title to do: the metadata alone.
  const titleOnly = { ...sheet(), lines: sheet().lines.map((line) => ({ ...line, todo: false, text: `en ${line.id}` })), description: { ...sheet().description, todo: false, text: "d" }, tags: { ...sheet().tags, todo: false, text: ["t"] }, thumbnail: null, chapters: sheet().chapters.map((chapter) => ({ ...chapter, todo: false, text: "c" })) };
  assert.deepEqual(sheetUnits(titleOnly, { lines: 3, chars: 10_000 }).map((unit) => unit.parts), [["metadata"]]);
});

test("a unit's key is what it asks for: a changed source, budget or narration language is a new unit", () => {
  const [, first] = sheetUnits(sheet(), { lines: 3, chars: 10_000 });
  const again = sheetUnits(sheet(), { lines: 3, chars: 10_000 })[1];
  assert.equal(unitKey(first), unitKey(again), "the same sheet gives the same keys round after round");
  const changed = { ...first, lines: first.lines.map((line, index) => (index ? line : { ...line, source: `${line.source}！` })) };
  assert.notEqual(unitKey(changed), unitKey(first));
  const budgeted = sheetUnits(sheet(null, undefined, Object.fromEntries(sheet().lines.map((line) => [line.id, 40]))), { lines: 3, chars: 10_000 })[1];
  assert.notEqual(unitKey(budgeted), unitKey(first), "a dub's budget is part of what was asked");
  assert.notEqual(unitKey(first, "en"), unitKey(first));
});

test("a unit's answer with a line missing or empty is not usable", () => {
  const [, unit] = sheetUnits(sheet(), { lines: 3, chars: 10_000 });
  assert.equal(unitGaps(filled(unit), unit), null);
  const answer = filled(unit);
  assert.equal(unitGaps({ ...answer, lines: answer.lines.slice(1) }, unit), "left 1 of 3 lines out or empty (k7p2)");
  assert.equal(unitGaps({ ...answer, lines: answer.lines.map((line) => ({ ...line, text: " " })) }, unit), "left 3 of 3 lines out or empty (k7p2, m4qa, x9fe)");
  assert.match(unitGaps(null, unit), /left 3 of 3/);
  assert.equal(unitGaps({ lines: [] }, sheetUnits(sheet(), { lines: 3, chars: 10_000 })[0]), null, "the metadata is i18n-merge's to check");
});

test("the reviewed units make the whole sheet again: texts by id and by scene, everything else from the sheet", () => {
  const whole = sheet();
  const units = sheetUnits(whole, { lines: 3, chars: 10_000 });
  const reviewed = units.map((unit) => {
    if (unit.parts.includes("metadata")) {
      return { ...unit, title: { ...unit.title, text: "en title" }, description: { ...unit.description, text: "en description" }, tags: { ...unit.tags, text: ["en"] }, chapters: unit.chapters.map((chapter) => ({ ...chapter, source: "changed by the model", text: `en ${chapter.scene}` })), thumbnail: { ...unit.thumbnail, text: { tag: "en tag", headline: "en headline" } } };
    }
    // A model that changes a source does not change the sheet's.
    return { ...filled(unit), lines: filled(unit).lines.map((line) => ({ ...line, source: "changed by the model" })) };
  });
  const assembled = assembleSheet(whole, reviewed);
  assert.deepEqual(assembled.lines.map((line) => [line.id, line.source, line.text]), whole.lines.map((line) => [line.id, line.source, `en ${line.id}`]));
  assert.deepEqual([assembled.title.text, assembled.description.text, assembled.tags.text, assembled.thumbnail.text], ["en title", "en description", ["en"], { tag: "en tag", headline: "en headline" }]);
  assert.deepEqual(assembled.chapters.map((chapter) => [chapter.scene, chapter.source, chapter.text]), whole.chapters.map((chapter) => [chapter.scene, chapter.source, `en ${chapter.scene}`]));
  assert.deepEqual([assembled.locale, assembled.slug, assembled.parts, assembled.note], [whole.locale, whole.slug, whole.parts, whole.note]);
  // Without a metadata unit the sheet's metadata stays as it was.
  assert.deepEqual(assembleSheet(whole, reviewed.slice(1)).title, whole.title);
});

test("the units i18n-merge refused are read from its report; a report naming none refuses them all", () => {
  const units = sheetUnits(sheet(), { lines: 3, chars: 10_000 });
  const out = "en: 7 lines written to x; 2 problems\n  title: at most 100 characters and no angle brackets\n  r8wd: not translated\n  note: thumbnail: not translated; this locale keeps the video's own thumbnail\n";
  assert.deepEqual(refusedUnits(out, units).map((unit) => units.indexOf(unit)), [0, 2]);
  assert.deepEqual(refusedUnits("en: 7 lines written to x; 1 problems\n  chapter hook: not translated\n", units).map((unit) => units.indexOf(unit)), [0]);
  assert.deepEqual(refusedUnits("no sheet for en; run i18n-sheet first", units), units);
});

test("a video's lines unit is shown only its scenes; the whole sheet and the metadata see the whole video", () => {
  const video = fixture();
  const units = sheetUnits(sheet(), { lines: 3, chars: 10_000 });
  assert.deepEqual(unitVideo(video, units[1], false).scenes.map((scene) => scene.id), ["hook", "questions"]);
  assert.deepEqual(unitVideo(video, units[3], false).scenes.map((scene) => scene.id), ["wrap"]);
  assert.equal(unitVideo(video, units[1], false).slug, video.slug);
  assert.equal(unitVideo(video, units[0], false), video);
  assert.equal(unitVideo(video, sheet(), true), video);
});

test("kept answers survive a restart, a unit no longer asked is dropped, and an unreadable file is nothing kept", () => {
  const box = sandbox();
  const workdir = path.join(box.work, "long-video");
  assert.deepEqual(readUnits(workdir, "en"), {});
  writeUnits(workdir, "en", { a: { translated: { lines: [] } }, b: { translated: { lines: [] }, reviewed: { lines: [] } }, stale: { translated: {} } }, ["a", "b"]);
  assert.deepEqual(Object.keys(readUnits(workdir, "en")), ["a", "b"]);
  assert.deepEqual(readUnits(workdir, "ja"), {}, "kept per locale");
  clearUnits(workdir, "en");
  assert.ok(!existsSync(path.join(workdir, "i18n", "en.units.json")));
  clearUnits(workdir, "en");
  mkdirSync(path.join(workdir, "i18n"), { recursive: true });
  writeFileSync(path.join(workdir, "i18n", "en.units.json"), "{ not json");
  assert.deepEqual(readUnits(workdir, "en"), {});
});
