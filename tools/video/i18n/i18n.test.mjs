import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { sourceHashes } from "../core/translations.mjs";
import { buildSheet, mergeSheet, sheetTodo } from "./cli.mjs";

function context(box) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work },
      home: box.base,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-25T07:00:00Z"),
    },
  };
}

const filled = (sheet) => ({
  ...sheet,
  title: { ...sheet.title, text: "How to choose an AI model" },
  description: { ...sheet.description, text: "Three questions before the leaderboard." },
  tags: { ...sheet.tags, text: ["AI", "model choice"] },
  chapters: sheet.chapters.map((chapter) => ({ ...chapter, text: `EN ${chapter.scene}` })),
  lines: sheet.lines.map((line) => ({ ...line, text: line.text || `EN ${line.id}` })),
});

// Fills only what the sheet marks todo, the way a translator does.
const fillTodo = (sheet, prefix = "EN") => ({
  ...sheet,
  title: sheet.title.todo ? { ...sheet.title, text: `${prefix} title` } : sheet.title,
  description: sheet.description.todo ? { ...sheet.description, text: `${prefix} description` } : sheet.description,
  tags: sheet.tags.todo ? { ...sheet.tags, text: sheet.tags.source.map((tag) => `${prefix} ${tag}`) } : sheet.tags,
  chapters: sheet.chapters.map((chapter) => (chapter.todo ? { ...chapter, text: `${prefix} ${chapter.source}` } : chapter)),
  lines: sheet.lines.map((line) => (line.todo ? { ...line, text: `${prefix} ${line.id}` } : line)),
});

const todoOf = (sheet) => ({
  title: sheet.title.todo,
  description: sheet.description.todo,
  tags: sheet.tags.todo,
  chapters: Object.fromEntries(sheet.chapters.map((chapter) => [chapter.scene, chapter.todo])),
  lines: sheet.lines.filter((line) => line.todo).map((line) => line.id),
});

test("a sheet marks the lines with no current translation, and merging hashes them from the script", () => {
  const doc = fixture();
  const [first, second] = [...eachLine(doc)].map(({ line }) => line);
  const previous = {
    title: "Old title",
    source_hashes: { title: textHash(doc.youtube.title) },
    lines: { [first.id]: { source_hash: textHash(first.text), text: "kept" }, [second.id]: { source_hash: "stale0000000", text: "old" } },
  };
  const sheet = buildSheet(doc, previous, "en");
  assert.deepEqual(sheet.lines.slice(0, 2).map((line) => [line.id, line.todo, line.text]), [[first.id, false, "kept"], [second.id, true, ""]]);
  assert.deepEqual(sheet.title, { todo: false, source: doc.youtube.title, text: "Old title" });

  const { translation, problems } = mergeSheet(doc, filled(sheet), previous);
  assert.deepEqual(problems, []);
  assert.deepEqual(translation.lines[first.id], { source_hash: textHash(first.text), text: "kept" });
  assert.deepEqual(translation.lines[second.id], { source_hash: textHash(second.text), text: `EN ${second.id}` });
  assert.equal(Object.keys(translation.chapters).length, sheet.chapters.length);
  assert.deepEqual(translation.source_hashes, sourceHashes(doc));
});

test("after a re-pace, renamed and new chapters, a new description and reordered tags are todo", () => {
  const doc = fixture();
  const { translation: merged } = mergeSheet(doc, fillTodo(buildSheet(doc, null, "en")), null);
  assert.deepEqual(todoOf(buildSheet(doc, merged, "en")), { title: false, description: false, tags: false, chapters: { hook: false, questions: false, wrap: false }, lines: [] });

  // What happened to batch 2 on 2026-09-26: the opening chapter renamed, "三個問題" moved to a new
  // scene of its own, a paragraph put in front of the description, the tags reordered.
  const repaced = structuredClone(doc);
  repaced.scenes[0].chapter = "ChatGPT 開始有廣告了";
  delete repaced.scenes[1].chapter;
  repaced.scenes.splice(1, 0, { id: "ask", chapter: "三個問題", template: "big", data: {}, lines: [{ id: "q0ab", text: "先問自己三個問題。" }] });
  repaced.youtube.description = `新的開場段落。\n\n${doc.youtube.description}`;
  repaced.youtube.tags = [...doc.youtube.tags].reverse();

  const sheet = buildSheet(repaced, merged, "en");
  assert.deepEqual(todoOf(sheet), { title: false, description: true, tags: true, chapters: { hook: true, ask: true, wrap: false }, lines: ["q0ab"] });
  assert.equal(sheet.chapters[0].text, "", "a renamed chapter does not offer its old title");
  assert.equal(sheet.chapters[2].text, "EN 結論");
  assert.deepEqual([sheet.description.text, sheet.tags.text], ["", []]);
  assert.match(sheetTodo(sheet), /^1 of 8 lines, 2 of 3 chapters, the description, the tags$/);

  const { translation, problems } = mergeSheet(repaced, fillTodo(sheet, "EN2"), merged);
  assert.deepEqual(problems, []);
  assert.deepEqual(translation.chapters, { hook: "EN2 ChatGPT 開始有廣告了", ask: "EN2 三個問題", wrap: "EN 結論" }, "no entry is left under the scene the chapter moved from");
  assert.deepEqual(translation.source_hashes, sourceHashes(repaced));
  assert.equal(translation.title, "EN title");
  assert.deepEqual(todoOf(buildSheet(repaced, translation, "en")), { title: false, description: false, tags: false, chapters: { hook: false, ask: false, wrap: false }, lines: [] });
});

test("a file merged before source hashes were kept loads, and its metadata is todo while its lines are not", () => {
  const doc = fixture();
  const lines = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, { source_hash: textHash(line.text), text: `EN ${line.id}` }]));
  const old = { title: "T", description: "D", tags: ["AI"], chapters: { hook: "Intro", questions: "Three questions", wrap: "Wrap-up" }, lines };
  const sheet = buildSheet(doc, old, "en");
  assert.deepEqual(todoOf(sheet), { title: true, description: true, tags: true, chapters: { hook: true, questions: true, wrap: true }, lines: [] });
  assert.ok(sheet.chapters.every((chapter) => chapter.text === ""));
});

test("a field or chapter whose zh-TW text changed after the sheet keeps its previous translation and hash", () => {
  const doc = fixture();
  const { translation: merged } = mergeSheet(doc, fillTodo(buildSheet(doc, null, "ja"), "JA"), null);
  const sheet = fillTodo(buildSheet(doc, merged, "ja"), "JA");
  const changed = structuredClone(doc);
  changed.youtube.title = "新標題";
  changed.scenes[2].chapter = "最後";
  const { translation, problems } = mergeSheet(changed, { ...sheet, title: { ...sheet.title, text: "Refreshed" } }, merged);
  assert.deepEqual(problems, [
    "title: the zh-TW title changed after the sheet was made; make a new sheet",
    "chapter wrap: the zh-TW chapter title changed after the sheet was made; make a new sheet",
  ]);
  assert.equal(translation.title, merged.title);
  assert.equal(translation.source_hashes.title, merged.source_hashes.title);
  assert.equal(translation.chapters.wrap, merged.chapters.wrap);
  assert.deepEqual(todoOf(buildSheet(changed, translation, "ja")).chapters, { hook: false, questions: false, wrap: true });
  assert.equal(buildSheet(changed, translation, "ja").title.todo, true);
});

test("a line whose zh-TW text changed after the sheet, or an empty title, is not merged", () => {
  const doc = fixture();
  const sheet = filled(buildSheet(doc, null, "ja"));
  const [line] = [...eachLine(doc)].map(({ line: each }) => each);
  line.text = `${line.text}（改）`;
  const { translation, problems } = mergeSheet(doc, { ...sheet, title: { text: "" } }, null);
  assert.equal(translation.lines[line.id], undefined);
  assert.ok(problems.some((problem) => problem.startsWith(`${line.id}: the zh-TW line changed`)));
  assert.ok(problems.includes("title: not translated"));
});

test("i18n-sheet then i18n-merge leaves lint with no missing or stale translations for the locale", async () => {
  const box = sandbox();
  const make = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], make.ctx), EXIT.ok, make.out.stderr);
  const sheetPath = path.join(box.workdir, "i18n", "en.todo.json");
  const sheet = JSON.parse(readFileSync(sheetPath, "utf8"));
  assert.ok(sheet.lines.every((line) => line.todo) && sheet.chapters.every((chapter) => chapter.todo) && sheet.title.todo && sheet.description.todo && sheet.tags.todo);
  writeFileSync(sheetPath, JSON.stringify(filled(sheet)));

  const merge = context(box);
  assert.equal(await main(["i18n-merge", "--slug", box.slug, "--locale", "en"], merge.ctx), EXIT.ok, merge.out.stdout);
  const project = loadProject({ slug: box.slug, root: box.root });
  assert.equal(project.translations.en.title, "How to choose an AI model");
  const warnings = lintProject(project).warnings.filter((warning) => warning.path === "i18n/en.json");
  assert.deepEqual(warnings, []);

  const unknown = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "fr"], unknown.ctx), EXIT.usage);
});

test("an i18n file from before source hashes loads; lint calls its metadata possibly stale until a new sheet is merged", async () => {
  const box = sandbox();
  const { doc } = loadProject({ slug: box.slug, root: box.root });
  const lines = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, { source_hash: textHash(line.text), text: `EN ${line.id}` }]));
  mkdirSync(path.join(box.dir, "i18n"));
  const old = { title: "T", description: "D", tags: ["AI"], chapters: { hook: "Intro", questions: "Three questions", gone: "Moved away" }, lines };
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(old));
  const lintOf = () => lintProject(loadProject({ slug: box.slug, root: box.root })).warnings.filter((warning) => warning.path === "i18n/en.json").map((warning) => warning.message);
  const before = lintOf();
  assert.equal(before.length, 3, before.join("\n"));
  assert.match(before[0], /^not translated: chapter wrap$/);
  assert.match(before[1], /possibly stale: title, description, tags, chapter hook, chapter questions; i18n-sheet marks them todo$/);
  assert.match(before[2], /scenes that no longer open a chapter: gone; i18n-merge drops them$/);

  const make = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], make.ctx), EXIT.ok, make.out.stderr);
  assert.match(make.out.stdout, /^en: to translate 0 of 7 lines, 3 of 3 chapters, the title, the description, the tags; /);
  const sheetPath = path.join(box.workdir, "i18n", "en.todo.json");
  writeFileSync(sheetPath, JSON.stringify(fillTodo(JSON.parse(readFileSync(sheetPath, "utf8")))));
  const merge = context(box);
  assert.equal(await main(["i18n-merge", "--slug", box.slug, "--locale", "en"], merge.ctx), EXIT.ok, merge.out.stdout);
  assert.deepEqual(lintOf(), []);
  const written = JSON.parse(readFileSync(path.join(box.dir, "i18n", "en.json"), "utf8"));
  assert.deepEqual(Object.keys(written.chapters), ["hook", "questions", "wrap"]);
  assert.deepEqual(Object.keys(written), ["title", "description", "tags", "chapters", "source_hashes", "lines"]);
});
