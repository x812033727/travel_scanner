import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { writeLanguages } from "../core/stages.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { estimateTimeline, speechHash } from "../core/timeline.mjs";
import { localizedThumbnail, sourceHashes, thumbnailGap, thumbnailSourceHash, thumbnailStatus } from "../core/translations.mjs";
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
  thumbnail: sheet.thumbnail?.todo ? { ...sheet.thumbnail, text: Object.fromEntries(Object.entries(sheet.thumbnail.source).map(([name, word]) => [name, `${prefix} ${word}`])) } : sheet.thumbnail,
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
  assert.deepEqual(translation.source_hashes, { ...sourceHashes(repaced), thumbnail: thumbnailSourceHash(repaced) });
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
  assert.match(make.out.stdout, /^en: to translate 0 of 7 lines, 3 of 3 chapters, the title, the description, the tags, the thumbnail's words; /);
  const sheetPath = path.join(box.workdir, "i18n", "en.todo.json");
  writeFileSync(sheetPath, JSON.stringify(fillTodo(JSON.parse(readFileSync(sheetPath, "utf8")))));
  const merge = context(box);
  assert.equal(await main(["i18n-merge", "--slug", box.slug, "--locale", "en"], merge.ctx), EXIT.ok, merge.out.stdout);
  assert.deepEqual(lintOf(), []);
  const written = JSON.parse(readFileSync(path.join(box.dir, "i18n", "en.json"), "utf8"));
  assert.deepEqual(Object.keys(written.chapters), ["hook", "questions", "wrap"]);
  assert.deepEqual(Object.keys(written), ["title", "description", "tags", "thumbnail", "chapters", "source_hashes", "lines"]);
});

test("a sheet narrowed with --parts holds only that part, merging keeps the rest untouched, and the dub budget comes only with a dub chosen", async () => {
  const box = sandbox();
  // A full translation first, so the untouched parts have something to keep.
  const full = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], full.ctx), EXIT.ok, full.out.stderr);
  const sheetPath = path.join(box.workdir, "i18n", "en.todo.json");
  writeFileSync(sheetPath, JSON.stringify(filled(JSON.parse(readFileSync(sheetPath, "utf8")))));
  assert.equal(await main(["i18n-merge", "--slug", box.slug, "--locale", "en"], context(box).ctx), EXIT.ok);
  const file = path.join(box.dir, "i18n", "en.json");
  const before = JSON.parse(readFileSync(file, "utf8"));

  // Metadata only: no lines on the sheet; a merge keeps the lines as they were.
  const meta = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en", "--parts", "metadata"], meta.ctx), EXIT.ok, meta.out.stderr);
  assert.match(meta.out.stdout, /^en: to translate 0 of 3 chapters, the thumbnail's words; .*\(metadata only\)\n$/);
  const metaSheet = JSON.parse(readFileSync(sheetPath, "utf8"));
  assert.deepEqual([metaSheet.parts, metaSheet.lines, metaSheet.title.text, metaSheet.chapters.length], [["metadata"], [], "How to choose an AI model", 3]);
  assert.match(metaSheet.note, /only the title, the description, the tags, the chapter names and the thumbnail's words/);
  metaSheet.title.text = "A better English title";
  writeFileSync(sheetPath, JSON.stringify(metaSheet));
  assert.equal(await main(["i18n-merge", "--slug", box.slug, "--locale", "en"], context(box).ctx), EXIT.ok);
  const afterMeta = JSON.parse(readFileSync(file, "utf8"));
  assert.equal(afterMeta.title, "A better English title");
  assert.deepEqual(afterMeta.lines, before.lines, "the lines were not on the sheet, so they stay");
  assert.deepEqual(Object.keys(afterMeta), Object.keys(before));

  // Captions only: no title, description, tags or chapters; a merge keeps them.
  const caps = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en", "--parts", "captions"], caps.ctx), EXIT.ok, caps.out.stderr);
  assert.match(caps.out.stdout, /^en: to translate 0 of 7 lines; .*\(captions only\)\n$/);
  const capSheet = JSON.parse(readFileSync(sheetPath, "utf8"));
  assert.deepEqual([capSheet.parts, capSheet.title, capSheet.description, capSheet.tags, capSheet.chapters, capSheet.lines.length], [["captions"], null, null, null, [], 7]);
  assert.ok(capSheet.lines.every((line) => line.max_chars === undefined), "no narration timed yet: no budget");
  capSheet.lines[0].text = "Shorter";
  writeFileSync(sheetPath, JSON.stringify(capSheet));
  assert.equal(await main(["i18n-merge", "--slug", box.slug, "--locale", "en"], context(box).ctx), EXIT.ok);
  const afterCaps = JSON.parse(readFileSync(file, "utf8"));
  assert.equal(afterCaps.lines[capSheet.lines[0].id].text, "Shorter");
  assert.deepEqual([afterCaps.title, afterCaps.description, afterCaps.tags, afterCaps.chapters, afterCaps.source_hashes], [afterMeta.title, afterMeta.description, afterMeta.tags, afterMeta.chapters, afterMeta.source_hashes]);

  // With the narration timed, the budget goes on the sheet only when the owner chose a dub for the locale.
  const project = loadProject({ slug: box.slug, root: box.root });
  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify({ ...estimateTimeline(project.doc), speech_hash: speechHash(project.doc, project.lexicon) }));
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en", "--parts", "captions"], context(box).ctx), EXIT.ok);
  assert.ok(JSON.parse(readFileSync(sheetPath, "utf8")).lines.every((line) => Number.isInteger(line.max_chars)), "no choice written: budgets as before");
  writeLanguages(box.workdir, { locales: { en: { metadata: true, captions: true, dub: false } }, decided_at: "2026-09-27T10:00:00Z" });
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], context(box).ctx), EXIT.ok);
  assert.ok(JSON.parse(readFileSync(sheetPath, "utf8")).lines.every((line) => line.max_chars === undefined), "captions without a dub: no budget");
  writeLanguages(box.workdir, { locales: { en: { metadata: true, captions: true, dub: true } }, decided_at: "2026-09-27T10:00:00Z" });
  const dubbed = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], dubbed.ctx), EXIT.ok);
  assert.ok(JSON.parse(readFileSync(sheetPath, "utf8")).lines.every((line) => Number.isInteger(line.max_chars)), "a dub chosen: every line has its budget");
  assert.match(dubbed.out.stdout, /with max_chars for the dub/);

  const bad = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en", "--parts", "dub"], bad.ctx), EXIT.usage);
  assert.match(bad.out.stderr, /--parts must be among metadata, captions/);
});

test("the thumbnail's words go on the sheet with the metadata, merge with their hash, and turn stale with the thumbnail", () => {
  const doc = fixture();
  const sheet = buildSheet(doc, null, "en");
  assert.deepEqual(sheet.thumbnail, { todo: true, source: { tag: doc.thumbnail.data.tag, headline: doc.thumbnail.data.headline }, text: { tag: "", headline: "" } });
  assert.equal(buildSheet(doc, null, "en", null, ["captions"]).thumbnail, null, "a captions-only sheet has no thumbnail");
  const filledSheet = { ...filled(sheet), thumbnail: { ...sheet.thumbnail, text: { tag: " Picking an AI model ", headline: "No. 1 is not\n**always best**" } } };
  const { translation, problems, notes } = mergeSheet(doc, filledSheet, null);
  assert.deepEqual([problems, notes], [[], []]);
  assert.deepEqual(translation.thumbnail, { tag: "Picking an AI model", headline: "No. 1 is not\n**always best**" });
  assert.equal(translation.source_hashes.thumbnail, thumbnailSourceHash(doc));
  assert.equal(thumbnailStatus(doc, translation), "current");
  assert.deepEqual(localizedThumbnail(doc, translation), { template: "thumb", data: { ...doc.thumbnail.data, tag: "Picking an AI model", headline: "No. 1 is not\n**always best**" } });
  assert.equal(buildSheet(doc, translation, "en").thumbnail.todo, false);

  // A new zh-TW headline: the words are stale, drawn by nobody, and the next sheet asks again.
  const changed = structuredClone(doc);
  changed.thumbnail.data.headline = "排行榜不是答案";
  assert.equal(thumbnailStatus(changed, translation), "stale");
  assert.equal(localizedThumbnail(changed, translation), null);
  assert.match(thumbnailGap(changed, translation, "en"), /older thumbnail/);
  assert.equal(buildSheet(changed, translation, "en").thumbnail.todo, true);
  // The old sheet no longer matches the script: a note, the previous words and hash kept, the merge still clean.
  const again = mergeSheet(changed, filledSheet, translation);
  assert.deepEqual(again.problems, []);
  assert.match(again.notes[0], /thumbnail changed after the sheet was made/);
  assert.deepEqual([again.translation.thumbnail, again.translation.source_hashes.thumbnail], [translation.thumbnail, translation.source_hashes.thumbnail]);
});

test("a sheet without the thumbnail's words still merges: a note, and the locale keeps the video's own thumbnail", () => {
  const doc = fixture();
  const sheet = filled(buildSheet(doc, null, "en"));
  const { translation, problems, notes } = mergeSheet(doc, sheet, null);
  assert.deepEqual(problems, []);
  assert.deepEqual(notes, ["thumbnail: not translated; this locale keeps the video's own thumbnail"]);
  assert.equal(translation.thumbnail, undefined);
  assert.equal(translation.source_hashes.thumbnail, undefined);
  assert.equal(thumbnailStatus(doc, translation), "missing");
  assert.match(thumbnailGap(doc, translation, "en"), /i18n\/en\.json has no thumbnail words/);
  // Half a thumbnail is no thumbnail; a sheet written before the field existed merges as before.
  const half = mergeSheet(doc, { ...sheet, thumbnail: { ...sheet.thumbnail, text: { tag: "", headline: "Only a headline" } } }, null);
  assert.deepEqual(half.notes, ["thumbnail: tag not translated; this locale keeps the video's own thumbnail"]);
  const { thumbnail, ...older } = sheet;
  assert.equal(thumbnail.todo, true);
  assert.deepEqual(mergeSheet(doc, older, null).problems, []);
  // Words written by hand, without i18n-merge, have no source hash: not drawn until merged.
  assert.equal(thumbnailStatus(doc, { thumbnail: { tag: "t", headline: "h" } }), "unknown");
  // A video without a thumbnail has nothing to translate there.
  const bare = structuredClone(doc);
  delete bare.thumbnail;
  assert.equal(buildSheet(bare, null, "en").thumbnail, null);
  assert.equal(thumbnailStatus(bare, null), "none");
  assert.equal(thumbnailGap(bare, null, "en"), null);
});
