import assert from "node:assert/strict";
import test from "node:test";

import { fixture, fixtureBrief, fixtureLexicon } from "./fixtures/load.mjs";
import { billableEstimate, briefSections, checkBrief, lintVideo, templateSimilarity } from "./lint.mjs";
import { textHash } from "./schema.mjs";
import { sourceHashes } from "./translations.mjs";

const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {}, ...overrides });
const messages = (problems) => problems.map((problem) => problem.message).join("\n");

test("the minimal example lints clean", () => {
  const result = lintVideo(fixture(), context());
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  assert.equal(result.summary.chapters.length, 3);
});

test("schema errors stop lint before any other rule runs", () => {
  const doc = fixture();
  doc.scenes = [];
  const result = lintVideo(doc, context());
  assert.equal(result.summary, null);
  assert.deepEqual(result.errors.map((error) => error.path), ["scenes"]);
});

test("every Latin term must be in the pronunciation dictionary", () => {
  const doc = fixture();
  doc.scenes[0].lines[0].text = "Gemini 和 LLM 有什麼不一樣？";
  const { errors } = lintVideo(doc, context());
  assert.equal(errors.length, 1);
  assert.match(errors[0].message, /"Gemini" is not in docs\/videos\/lexicon\.json/);
});

test("a say written for an older text is an error that names the new hash", () => {
  const doc = fixture();
  doc.scenes[2].lines[1].text = "完整比較表在說明欄，下一支見。";
  const { errors } = lintVideo(doc, context());
  assert.match(messages(errors), new RegExp(textHash("完整比較表在說明欄，下一支見。")));
});

test("URLs and written language are errors; narrating the checking process is a warning", () => {
  const doc = fixture();
  doc.scenes[0].lines[0].text = "詳細請看 mokaair.com 上的資料。";
  doc.scenes[0].lines[1].text = "綜上所述，經查證這三個問題就夠了。";
  const result = lintVideo(doc, context());
  assert.match(messages(result.errors), /never read a URL aloud/);
  assert.match(messages(result.errors), /"綜上所述" is written language/);
  assert.match(messages(result.warnings), /"經查證" narrates the process/);
});

test("long sentences and parentheses are warnings", () => {
  const doc = fixture();
  doc.scenes[1].lines[0].text = "第一個問題是你要它做什麼工作，因為寫程式、寫文章、整理資料、翻譯和陪你聊天需要的能力完全不一樣。";
  doc.scenes[1].lines[1].text = "第二個問題（也很重要）是你能等多久。";
  const { errors, warnings } = lintVideo(doc, context());
  assert.deepEqual(errors, []);
  assert.match(messages(warnings), /spoken units; split sentences/);
  assert.match(messages(warnings), /parentheses/);
});

test("the brief must state the owner's view and what the viewer can do afterwards", () => {
  assert.deepEqual(checkBrief(fixtureBrief()), []);
  assert.match(checkBrief(null)[0], /brief\.md is missing/);
  const placeholder = fixtureBrief().replace("排行榜只是起點；我自己是先看工作類型，再看等待時間和價格。", "（待填）<!-- 站主寫 -->");
  assert.deepEqual(checkBrief(placeholder), ['brief.md needs a non-empty "## 站主觀點" section']);
  assert.equal(Object.keys(briefSections("## A\nx\n## B\n")).join(","), "A,B");
});

test("a slide cannot reveal more elements than it has", () => {
  const doc = fixture();
  doc.scenes[1].lines[0].reveal = 3;
  assert.match(messages(lintVideo(doc, context()).errors), /reveals 5 elements but the bullets slide has 3/);
});

test("fewer than three chapters is an error; a short estimated chapter is a warning", () => {
  const doc = fixture();
  delete doc.scenes[1].chapter;
  delete doc.scenes[2].chapter;
  assert.match(messages(lintVideo(doc, context()).errors), /1 chapters; YouTube needs at least 3/);
  const short = fixture();
  short.scenes[2].lines = [{ id: "zzzz", text: "再見。" }];
  assert.match(messages(lintVideo(short, context()).warnings), /estimated; the real check runs on the synthesized timeline/);
});

test("YouTube limits apply to the composed description, chapters and sources included", () => {
  const doc = fixture();
  doc.youtube.description = "字".repeat(1650);
  assert.match(messages(lintVideo(doc, context()).errors), /bytes once composed/);
});

test("a source guide that does not exist is an error", () => {
  const doc = fixture();
  doc.source_guide = "no-such-article";
  assert.match(messages(lintVideo(doc, context({ pack: null })).errors), /no content pack named no-such-article/);
});

test("stale and missing translations are listed per locale", () => {
  const doc = fixture();
  const lines = {};
  for (const scene of doc.scenes) for (const line of scene.lines) lines[line.id] = { source_hash: textHash(line.text), text: "x" };
  delete lines.k7p2;
  lines.m4qa.source_hash = "000000000000";
  const { warnings } = lintVideo(doc, context({ translations: { en: { lines } } }));
  assert.match(messages(warnings), /1 lines not translated: k7p2/);
  assert.match(messages(warnings), /1 translations older than the zh-TW line: m4qa/);
});

test("the title, description, tags and chapters are stale, unknown or missing against their zh-TW hashes", () => {
  const doc = fixture();
  const lines = {};
  for (const scene of doc.scenes) for (const line of scene.lines) lines[line.id] = { source_hash: textHash(line.text), text: "x" };
  const hashes = sourceHashes(doc);
  const current = { title: "T", description: "D", tags: ["AI"], chapters: { hook: "Intro", questions: "Q", wrap: "End" }, source_hashes: hashes, lines };
  assert.deepEqual(lintVideo(doc, context({ translations: { en: current } })).warnings, []);

  const reordered = structuredClone(doc);
  reordered.youtube.tags.reverse();
  const translation = {
    ...current,
    tags: [],
    chapters: { hook: "Intro", questions: "Q", moved: "Old place" },
    source_hashes: { title: hashes.title, description: "000000000000", tags: hashes.tags, chapters: { hook: "000000000000" } },
  };
  const found = lintVideo(reordered, context({ translations: { ko: translation } })).warnings.filter((warning) => warning.path === "i18n/ko.json");
  assert.deepEqual(found.map((warning) => warning.message), [
    "not translated: tags, chapter wrap",
    "translations older than the zh-TW text: description, chapter hook",
    "translations merged before i18n-merge hashed their zh-TW text, so possibly stale: chapter questions; i18n-sheet marks them todo",
    "chapter titles for scenes that no longer open a chapter: moved; i18n-merge drops them",
  ]);
  const withTags = { ...translation, tags: ["AI"] };
  assert.match(messages(lintVideo(reordered, context({ translations: { ko: withTags } })).warnings), /older than the zh-TW text: description, tags, chapter hook/);
});

test("a slide sequence that copies another video's is flagged", () => {
  const doc = fixture();
  const extra = ["big", "compare", "steps"].map((template, index) => ({ id: `extra-${index}`, chapter: `章${index}`, template, data: {}, lines: [{ id: `e${index}xx`, text: "這是一句夠長的旁白，讓這一章超過十秒鐘以上。" }] }));
  doc.scenes.push(...extra);
  const copy = structuredClone(doc);
  assert.equal(templateSimilarity(doc, copy), 1);
  const { warnings } = lintVideo(doc, context({ others: [{ slug: "older-video", doc: copy }] }));
  assert.match(messages(warnings), /100% the same as older-video/);
});

test("Azure bills each Chinese character twice, plus markup", () => {
  const doc = { scenes: [{ lines: [{ id: "aaaa", text: "中文AB" }] }] };
  assert.equal(billableEstimate(doc), 4 + 2 + 30);
});
