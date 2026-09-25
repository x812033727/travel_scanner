import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { buildSheet, mergeSheet } from "./cli.mjs";

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

test("a sheet marks the lines with no current translation, and merging hashes them from the script", () => {
  const doc = fixture();
  const [first, second] = [...eachLine(doc)].map(({ line }) => line);
  const previous = {
    title: "Old title",
    lines: { [first.id]: { source_hash: textHash(first.text), text: "kept" }, [second.id]: { source_hash: "stale0000000", text: "old" } },
  };
  const sheet = buildSheet(doc, previous, "en");
  assert.deepEqual(sheet.lines.slice(0, 2).map((line) => [line.id, line.todo, line.text]), [[first.id, false, "kept"], [second.id, true, ""]]);
  assert.equal(sheet.title.text, "Old title");

  const { translation, problems } = mergeSheet(doc, filled(sheet), previous);
  assert.deepEqual(problems, []);
  assert.deepEqual(translation.lines[first.id], { source_hash: textHash(first.text), text: "kept" });
  assert.deepEqual(translation.lines[second.id], { source_hash: textHash(second.text), text: `EN ${second.id}` });
  assert.equal(Object.keys(translation.chapters).length, sheet.chapters.length);
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

test("i18n-sheet then i18n-merge leaves lint with no missing or stale lines for the locale", async () => {
  const box = sandbox();
  const make = context(box);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], make.ctx), EXIT.ok, make.out.stderr);
  const sheetPath = path.join(box.workdir, "i18n", "en.todo.json");
  const sheet = JSON.parse(readFileSync(sheetPath, "utf8"));
  assert.ok(sheet.lines.every((line) => line.todo));
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
