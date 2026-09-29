import assert from "node:assert/strict";
import test from "node:test";

import { dramaBrief, dramaFixture, fixture, fixtureBrief, fixtureLexicon, storyBrief, storyFixture, storySeries } from "./fixtures/load.mjs";
import { billableEstimate, briefSections, checkBrief, lintVideo, stancePoints, stanceProblems, templateSimilarity } from "./lint.mjs";
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

test("with a channel stance, 站主觀點 opens by naming the stance points it applies", () => {
  const stance = "頻道立場\n1. 先把帳算清楚再花錢。\n2、官方原文優先。\n\n３．AI 的整理要點開來源核對。\n不是條目的一行";
  assert.deepEqual(stancePoints(stance), { 1: "先把帳算清楚再花錢。", 2: "官方原文優先。", 3: "AI 的整理要點開來源核對。" });
  assert.deepEqual(stancePoints(""), {});
  assert.deepEqual(stancePoints(null), {});
  const withLine = (line) => fixtureBrief().replace("排行榜只是起點；我自己是先看工作類型，再看等待時間和價格。", `${line}\n排行榜只是起點；我自己是先看工作類型。`);
  assert.deepEqual(stanceProblems(fixtureBrief(), ""), [], "a blank stance is not checked");
  assert.deepEqual(stanceProblems(fixtureBrief(), "no numbered points here"), [], "a stance without numbered points has nothing to apply");
  assert.deepEqual(stanceProblems(withLine("套用立場：1、3"), stance), []);
  assert.deepEqual(stanceProblems(withLine("套用立場: 2, ３"), stance), [], "an ASCII colon, commas and full-width digits read the same");
  assert.deepEqual(stanceProblems(withLine("\n套用立場：2"), stance), [], "a blank line before it is fine");
  assert.match(stanceProblems(fixtureBrief(), stance)[0], /^the first line of "## 站主觀點" must read 「套用立場：N、M」.*\(found 「排行榜只是起點/);
  assert.match(stanceProblems(withLine("套用立場：4"), stance)[0], /names point 4, but the stance has only 1, 2, 3/);
  assert.deepEqual(stanceProblems(withLine("套用立場：1、4、5"), stance).length, 2, "every unknown number is named");
  assert.match(stanceProblems(withLine("套用立場："), stance)[0], /names no stance point; the stance has 1, 2, 3/);
  assert.match(stanceProblems(withLine("套用立場：一"), stance)[0], /"一", which is not a point number/);
  assert.match(stanceProblems("# x\n## 觀眾\ny\n", stance)[0], /needs a "## 站主觀點" section/);
  assert.match(stanceProblems(null, stance)[0], /brief\.md is missing/);
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

test("a translation whose description passes 5,000 bytes once composed is flagged, before package refuses it", () => {
  const doc = fixture();
  const lines = {};
  for (const scene of doc.scenes) for (const line of scene.lines) lines[line.id] = { source_hash: textHash(line.text), text: "x" };
  const hashes = sourceHashes(doc);
  const short = { title: "T", description: "짧은 설명", tags: ["AI"], chapters: { hook: "I", questions: "Q", wrap: "E" }, source_hashes: hashes, lines };
  assert.deepEqual(lintVideo(doc, context({ translations: { ko: short } })).warnings, []);
  // 1,700 Hangul syllables are 5,100 bytes on their own, before the chapters and sources.
  const long = { ...short, description: "가".repeat(1700) };
  const found = lintVideo(doc, context({ translations: { ko: long } })).warnings.filter((warning) => warning.path === "i18n/ko.json");
  assert.equal(found.length, 1);
  assert.match(found[0].message, /^ko\.description: \d+ bytes once composed, at most 5000 \(package refuses it\)$/);
});

test("a ja or ko number with a zero inside, before 億 or 억, is flagged; round numbers and other locales are not", () => {
  const doc = fixture();
  const ids = [...doc.scenes.flatMap((scene) => scene.lines.map((line) => line.id))];
  const translate = (texts) => ({ lines: Object.fromEntries(ids.map((id, index) => [id, { source_hash: textHash(doc.scenes.flatMap((scene) => scene.lines)[index].text), text: texts[index] ?? "x" }])) });
  const ja = translate(["128GBなら4050億パラメータ", "1200億と11万6175人、3,000万", "4千50億"]);
  const ko = translate(["4,050억 파라미터", "1080p", "4천50억"]);
  const en = translate(["405 billion, 4050億"]);
  const found = lintVideo(doc, context({ translations: { ja, ko, en } })).warnings.filter((warning) => /zero inside/.test(warning.message));
  assert.deepEqual(found.map((warning) => warning.path), ["i18n/ja.json", "i18n/ko.json"]);
  assert.match(found[0].message, new RegExp(`${ids[0]} \\(4050\\); write the thousands out, like 4千50$`));
  assert.match(found[1].message, new RegExp(`${ids[0]} \\(4,050\\); write the thousands out, like 4천50$`));
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

/** The drama example as episode 1 of a series, with series.json's cast beside it. */
function episode() {
  const doc = { ...dramaFixture(), series: { slug: "xianxia", episode: 1, chapter: 1 } };
  const series = { slug: "xianxia", episode: 1, characters: doc.characters.map((character) => ({ ...character })) };
  return { doc, series, context: context({ brief: dramaBrief(), series }) };
}

test("a binge series' visual tier in series.json caps the clips, before the clips stage spends anything", () => {
  const plain = episode();
  assert.deepEqual(lintVideo(plain.doc, plain.context).errors, [], "no tier in series.json, no cap");

  const stills = episode();
  stills.series.visual_tier = "stills";
  const capped = lintVideo(stills.doc, stills.context);
  assert.deepEqual(capped.errors.map((error) => [error.path, error.message]), [["scenes", '4 of 4 shots are clips; the "stills" tier allows at most 1: mark the rest visual "still"']]);
  for (const id of ["farewell", "sea-storm", "bird"]) stills.doc.scenes.find((scene) => scene.id === id).data.visual = "still";
  const kept = lintVideo(stills.doc, stills.context);
  assert.deepEqual(kept.errors, []);
  assert.ok(!kept.warnings.some((warning) => /tier/.test(warning.message)));

  const hybrid = episode();
  hybrid.series.visual_tier = "hybrid";
  assert.match(messages(lintVideo(hybrid.doc, hybrid.context).errors), /4 of 4 shots are clips; the "hybrid" tier allows at most 2/);
  hybrid.doc.scenes[0].data.visual = "still";
  hybrid.doc.scenes[1].data.visual = "still";
  assert.deepEqual(lintVideo(hybrid.doc, hybrid.context).errors, []);

  const clips = episode();
  clips.series.visual_tier = "clips";
  clips.doc.scenes[2].data.visual = "still";
  const remarked = lintVideo(clips.doc, clips.context);
  assert.deepEqual(remarked.errors, []);
  assert.match(messages(remarked.warnings), /the clips tier plays every shot as a clip; 1 still shots/);

  const unknown = episode();
  unknown.series.visual_tier = "gold";
  assert.match(messages(lintVideo(unknown.doc, unknown.context).errors), /"gold" is not a visual tier/);
  const nothing = episode();
  nothing.series.visual_tier = null;
  assert.deepEqual(lintVideo(nothing.doc, nothing.context).errors, [], "a null tier is no tier");
});

test("an episode of a compilation opens cold: no title card first", () => {
  const { doc, series, context: ctx } = episode();
  doc.scenes.unshift({ id: "card", chapter: "開場", template: "title", data: { title: "精衛填海", subtitle: "山海經" }, lines: [{ id: "t1tl", text: "第一集。" }] });
  assert.deepEqual(lintVideo(doc, ctx).errors, [], "a plain episode may still open on a card");
  series.compilation = true;
  const cold = lintVideo(doc, ctx);
  const outro = doc.scenes.findIndex((scene) => scene.template === "outro");
  assert.deepEqual(cold.errors.map((error) => [error.path, error.message]), [
    ["scenes[0]", "a binge episode opens cold: the first line is the hook; drop the title card"],
    [`scenes[${outro}]`, "a binge episode ends on its cliffhanger: the compilation adds the cards; drop the outro"],
  ], "the fixture closes on an outro card, which the compilation's own cards replace");
  doc.scenes.shift();
  doc.scenes.splice(outro - 1, 1);
  doc.scenes.at(-1).chapter = "結尾";
  assert.deepEqual(lintVideo(doc, ctx).errors, [], "without the cards the last shot carries the closing chapter");
  series.compilation = false;
  doc.scenes.push({ id: "bye", chapter: "結尾", template: "outro", data: { title: "下一集", cta: "完整故事在說明欄" }, lines: [{ id: "outr", text: "下一集見。" }] });
  assert.deepEqual(lintVideo(doc, ctx).errors, [], "a plain episode may close on a card");
});

test("series.json's kind decides whether the brand story rules apply", () => {
  const doc = storyFixture();
  doc.scenes[4].data.visual = "clip";
  doc.scenes[5].data.camera = "slow pan past an IBM reading machine";
  const story = lintVideo(doc, context({ brief: storyBrief(), series: storySeries() }));
  assert.deepEqual(story.errors.map((error) => error.path), ["scenes[4].data.visual", "scenes[5].data.camera"]);
  const plain = { ...storySeries(), kind: undefined };
  assert.deepEqual(lintVideo(doc, context({ brief: storyBrief(), series: plain })).errors, [], "the same script in a plain series may buy one clip and name a brand in a picture");
});

test("Azure bills each Chinese character twice, plus markup", () => {
  const doc = { scenes: [{ lines: [{ id: "aaaa", text: "中文AB" }] }] };
  assert.equal(billableEstimate(doc), 4 + 2 + 30);
});
