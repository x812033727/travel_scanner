import assert from "node:assert/strict";
import test from "node:test";

import { dramaBrief, dramaFixture, explainerBrief, explainerFixture, fixture, fixtureBrief, fixtureLexicon, storyBrief, storyFixture, storySeries } from "./fixtures/load.mjs";
import { billableEstimate, briefSections, checkBrief, lintVideo, productionShotProblems, stancePoints, stanceProblems, templateSimilarity } from "./lint.mjs";
import { estimateTimeline } from "./timeline.mjs";
import { MIN_EPISODE_MINUTES, minEpisodeMinutes, textHash } from "./schema.mjs";
import { sourceHashes } from "./translations.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {}, ...overrides });
const messages = (problems) => problems.map((problem) => problem.message).join("\n");

test("the minimal example lints clean", () => {
  const result = lintVideo(fixture(), context());
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  assert.equal(result.summary.chapters.length, 3);
});

test("the production profile blocks stills, frozen tails and estimated or measured shots over eight seconds", () => {
  const doc = dramaFixture();
  const series = { production: { profile: { visual_tier: "clips" } } };
  for (const scene of doc.scenes) delete scene.data.fit;
  for (const scene of doc.scenes) for (const line of scene.lines) line.text = "走。";
  const short = estimateTimeline(doc);
  assert.deepEqual(productionShotProblems(doc, series, short), []);
  doc.scenes[1].data.visual = "still";
  doc.scenes[2].data.fit = "freeze";
  const changed = structuredClone(short);
  changed.scenes[0].end_frame = changed.scenes[0].start_frame + 241;
  const errors = productionShotProblems(doc, series, changed);
  assert.match(messages(errors), /animated clips, not stills/);
  assert.match(messages(errors), /does not allow freeze-frame padding/);
  assert.match(messages(errors), /8 seconds including pauses/);
  assert.deepEqual(productionShotProblems(doc, null, changed), [], "legacy dramas retain their existing fitting rules");
  const result = lintVideo(doc, context({ brief: dramaBrief(), series }));
  assert.match(messages(result.errors), /animated clips, not stills/);
  assert.match(messages(result.errors), /freeze-frame padding/);
  delete doc.scenes[1].data.visual;
  delete doc.scenes[2].data.fit;
  doc.scenes[0].lines[0].text = "風".repeat(40);
  assert.match(messages(lintVideo(doc, context({ brief: dramaBrief(), series })).errors), /8 seconds including pauses/);
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

test("scene data the renderer would refuse is a lint error, so the writer fixes it before the audio", () => {
  const doc = fixture();
  doc.scenes[1].template = "chat";
  doc.scenes[1].data = { messages: [{ side: "right", name: "你", text: "可以用中文嗎？" }, { side: "left", name: "說明頁", text: "只支援英文。" }, { side: "left", name: "建議", text: "先備英文提示。" }] };
  doc.scenes[1].lines.forEach((line) => delete line.reveal);
  const errors = lintVideo(doc, context()).errors;
  assert.deepEqual(errors.map((error) => `${error.path}: ${error.message}`), ["scenes[1] (" + doc.scenes[1].id + ").data: named chat messages are limited to 2"]);
  doc.scenes[1].data.messages.forEach((message) => delete message.name);
  assert.deepEqual(lintVideo(doc, context()).errors, []);
});

test("a terminal scene without the real run's date and tool version is refused, and its reveals count output parts", () => {
  const doc = fixture();
  doc.scenes[1].template = "terminal";
  doc.scenes[1].data = { command: "claude --version", output: ["2.1.285 (Claude Code)", "second part", "third part"], ran_on: "2026-10-01", tool_version: "2.1.285 (Claude Code)" };
  assert.deepEqual(lintVideo(doc, context()).errors, [], "three reveals over three output parts");
  const where = `scenes[1] (${doc.scenes[1].id}).data`;
  delete doc.scenes[1].data.ran_on;
  delete doc.scenes[1].data.tool_version;
  const errors = lintVideo(doc, context()).errors;
  assert.deepEqual(errors.map((error) => error.path), [where, where]);
  assert.match(errors[0].message, /^ran_on is required: the date \(YYYY-MM-DD\) the command was really run/);
  assert.match(errors[1].message, /^tool_version is required/);
  doc.scenes[1].data.ran_on = "2026-10-01";
  doc.scenes[1].data.tool_version = "2.1.285 (Claude Code)";
  doc.scenes[1].data.output.pop();
  assert.match(messages(lintVideo(doc, context()).errors), /reveals 3 elements but the terminal slide has 2/);
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

function animeEpisode() {
  const doc = dramaFixture();
  doc.slug = "borrowed-dawn-production-e001";
  doc.category = "anime";
  doc.look = { preset: "anime-2d" };
  doc.target_minutes = [22, 22];
  doc.production_policy = "long-anime-v1";
  doc.runtime_spec = { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 };
  doc.series = { slug: "borrowed-dawn-production", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false };
  for (const scene of doc.scenes) {
    delete scene.data.fit;
    for (const line of scene.lines) line.text = "走。";
  }
  const series = {
    ...doc.series, category: "anime", style_preset: "anime-2d", target_minutes: 22,
    production_policy: doc.production_policy, runtime_spec: structuredClone(doc.runtime_spec),
    characters: structuredClone(doc.characters), visual_tier: "clips", compilation: false,
  };
  return { doc, series, context: context({ brief: dramaBrief(), series }) };
}

test("a native anime lints against its current approved series and reports body duration as an estimate", () => {
  const { doc, context: ctx } = animeEpisode();
  const result = lintVideo(doc, ctx);
  assert.deepEqual(result.errors, []);
  assert.ok(result.summary.minutes < 1, "this short fixture does not pretend to contain 22 minutes of measured media");
  assert.ok(result.warnings.some((warning) => warning.path === "runtime_spec" && /estimated story body/.test(warning.message) && /measured acceptance is 1260–1380 seconds/.test(warning.message) && /excluding OP\/ED and broadcast reserve/.test(warning.message)));
  assert.equal(Object.hasOwn(result.summary, "ready_for_production"), false);
  assert.equal(Object.hasOwn(result.summary, "measured_body_seconds"), false);
});

test("anime requires its approved series context and rejects missing or incomplete snapshot policies", () => {
  const absent = animeEpisode();
  delete absent.context.series;
  const result = lintVideo(absent.doc, absent.context);
  assert.ok(result.errors.some((error) => error.path === "series" && /no series.json/.test(error.message)));
  assert.ok(!result.warnings.some((warning) => /no series.json/.test(warning.message)), "missing trusted anime context is an error");
  for (const change of [
    (series) => { delete series.production_policy; },
    (series) => { delete series.runtime_spec; },
    (series) => { series.production_policy = "long-anime-v2"; },
    (series) => { series.category = "drama"; },
    (series) => { series.style_preset = "cinematic-3d"; },
    (series) => { series.target_minutes = 3; },
    (series) => { series.runtime_spec.op_ed_budget_seconds = -1; },
  ]) {
    const current = animeEpisode();
    change(current.series);
    assert.ok(lintVideo(current.doc, current.context).errors.some((error) => error.path === "series" && /complete approved long-anime production policy/.test(error.message)));
  }
});

test("a stale anime snapshot cannot change identity, counts or closed-ending declarations", () => {
  for (const [key, value] of [
    ["slug", "another-production"], ["episode", 2], ["chapter", 2],
    ["planned_episodes", 119], ["open_ended", true], ["closed_ending", true],
    ["kind", "one-off"], ["genre", "urban-return"], ["lead", "male"],
  ]) {
    const current = animeEpisode();
    current.series[key] = value;
    const result = lintVideo(current.doc, current.context);
    assert.ok(result.errors.length > 0, `${key} drift must not pass`);
    if (["kind", "genre", "lead"].includes(key)) assert.match(messages(result.errors), /complete approved long-anime production policy/);
    else assert.ok(result.errors.some((error) => error.path === "series" || error.path === `series.${key}` || error.path === "runtime_spec"), `${key}: ${messages(result.errors)}`);
  }
  for (const key of ["planned_episodes", "open_ended", "closed_ending"]) {
    const current = animeEpisode();
    delete current.series[key];
    assert.ok(lintVideo(current.doc, current.context).errors.length > 0, `${key} must not be inferred from the video`);
  }
});

test("different valid runtime budgets still fail the approved anime snapshot binding", () => {
  const current = animeEpisode();
  current.series.target_minutes = 21;
  current.series.runtime_spec.body_target_seconds = 1260;
  current.series.runtime_spec.slot_reserve_seconds = 360;
  assert.ok(lintVideo(current.doc, current.context).errors.some((error) => error.path === "runtime_spec" && /differs from the approved series production policy/.test(error.message)));
  const casting = animeEpisode();
  casting.series.characters[0].voice.name = "Puck";
  assert.ok(lintVideo(casting.doc, casting.context).errors.some((error) => error.path === "characters[0].voice" && /series' setting book/.test(error.message)));
});

test("an anime episode cannot lose its policy and fall back to ordinary drama", () => {
  const current = animeEpisode();
  delete current.doc.production_policy;
  delete current.doc.runtime_spec;
  current.doc.target_minutes = [1, 8];
  const { slug, episode: number, chapter } = current.doc.series;
  current.doc.series = { slug, episode: number, chapter };
  assert.ok(lintVideo(current.doc, current.context).errors.some((error) => error.path === "production_policy" && /lost its series' long-anime production policy/.test(error.message)));
  const ordinary = episode();
  delete ordinary.context.series;
  const result = lintVideo(ordinary.doc, ordinary.context);
  assert.deepEqual(result.errors, [], "ordinary drama retains its existing missing-snapshot warning");
  assert.ok(result.warnings.some((warning) => /no series.json/.test(warning.message)));
});

test("native anime's production profile accepts silent action but rejects stills and frame padding", () => {
  const current = animeEpisode();
  current.series.production = { profile: { visual_tier: "clips" } };
  current.doc.scenes[1].action_seconds = 8;
  current.doc.scenes[1].lines = [];
  current.doc.scenes[1].data.motion = "the worker lifts the valve handle and seats it in the bracket";
  assert.deepEqual(lintVideo(current.doc, current.context).errors, []);
  const actual = estimateTimeline(current.doc);
  const action = actual.scenes.find((scene) => scene.id === current.doc.scenes[1].id);
  assert.equal(action.end_frame - action.start_frame, 240);
  assert.deepEqual(productionShotProblems(current.doc, current.series, actual), []);
  action.end_frame++;
  assert.match(messages(productionShotProblems(current.doc, current.series, actual)), /limits a shot to 8 seconds/);
  const still = animeEpisode();
  still.series.production = { profile: { visual_tier: "clips" } };
  still.doc.scenes[1].data.visual = "still";
  assert.match(messages(lintVideo(still.doc, still.context).errors), /animated clips, not stills/);
  for (const fit of ["freeze", "slow"]) {
    const padded = animeEpisode();
    padded.series.production = { profile: { visual_tier: "clips" } };
    padded.doc.scenes[1].data.fit = fit;
    assert.match(messages(lintVideo(padded.doc, padded.context).errors), /frozen tails or slowed clips/);
  }
});

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

test("illustrated slides lint clean, warn on cadence, and are compared by their cards alone", async () => {
  const { illustratedFixture, illustratedBrief } = await import("./fixtures/load.mjs");
  const context = { lexicon: fixtureLexicon(), brief: illustratedBrief(), others: [], translations: {} };
  const clean = lintVideo(illustratedFixture(), context);
  assert.deepEqual(clean.errors, []);
  assert.deepEqual(clean.warnings, []);
  // A shot holding three sentences is past the 8 s a picture may stay: a warning, never a block.
  const slow = illustratedFixture();
  slow.scenes[1].lines.push({ id: "z1zz", text: "這一句讓圖停太久，觀眾會滑走。" });
  const result = lintVideo(slow, context);
  assert.deepEqual(result.errors, []);
  assert.ok(result.warnings.some((warning) => warning.path === "scenes (podium state 0)" && /estimated/.test(warning.message)), JSON.stringify(result.warnings));
  // A look on a video with nothing to draw is an error; music under slides is not a warning.
  const bare = fixture();
  bare.look = { preset: "tech-story" };
  assert.ok(lintVideo(bare, { ...context, brief: fixtureBrief() }).errors.some((error) => error.path === "look"));
  const music = fixture();
  music.music = { track: "bed.mp3" };
  assert.ok(!lintVideo(music, { ...context, brief: fixtureBrief() }).warnings.some((warning) => warning.path === "music"));
  // Two illustrated videos with the same cards but different pictures are still look-alikes; shots do not count.
  const a = illustratedFixture();
  const b = illustratedFixture();
  b.scenes.splice(2, 0, { id: "extra", template: "shot", data: { prompt: "flat illustration of a lighthouse", camera: "drift", visual: "still" }, lines: [{ id: "z3zz", text: "多一張圖。" }] });
  assert.equal(templateSimilarity(a, b), 1);
});

test("every episode but a drama's runs at least eight minutes: slides and the explainer are held to it, a drama is not", () => {
  assert.equal(MIN_EPISODE_MINUTES, 8);
  assert.equal(minEpisodeMinutes({}), 8);
  assert.equal(minEpisodeMinutes({ VIDEO_MIN_EPISODE_MINUTES: "0" }), 8, "an ordinary process cannot lower the floor");
  assert.equal(minEpisodeMinutes({ NODE_TEST_CONTEXT: "child-v8", VIDEO_MIN_EPISODE_MINUTES: "0" }), 0, "only fixture runners may use short test videos");
  assert.equal(minEpisodeMinutes({ VIDEO_MIN_EPISODE_MINUTES: "nonsense" }), 8);
  const saved = process.env.VIDEO_MIN_EPISODE_MINUTES;
  delete process.env.VIDEO_MIN_EPISODE_MINUTES;
  try {
    const slides = lintVideo(fixture(), context());
    assert.ok(slides.errors.some((each) => each.path === "target_minutes" && /at least 8/.test(each.message)), messages(slides.errors));
    assert.ok(slides.errors.some((each) => each.path === "scenes" && /at least 8: write more narration/.test(each.message)), messages(slides.errors));
    const explainer = lintVideo(explainerFixture(), context({ brief: explainerBrief() }));
    assert.ok(explainer.errors.some((each) => /at least 8/.test(each.message)), messages(explainer.errors));
    const drama = lintVideo(dramaFixture(), context({ brief: dramaBrief() }));
    assert.ok(!drama.errors.some((each) => /at least 8/.test(each.message)), messages(drama.errors));
  } finally {
    if (saved === undefined) delete process.env.VIDEO_MIN_EPISODE_MINUTES;
    else process.env.VIDEO_MIN_EPISODE_MINUTES = saved;
  }
});

test("the upper end of target_minutes is an aim, not a limit, where the eight-minute floor holds; a drama keeps both sides", () => {
  const length = (result) => result.warnings.filter((each) => each.path === "scenes" && /minutes; the target is/.test(each.message));
  const over = (doc) => ({ ...doc, target_minutes: [0.1, 0.2] });
  const slides = lintVideo(over(fixture()), context());
  assert.deepEqual(slides.errors, []);
  assert.deepEqual(length(slides), [], "slides over the upper end lint with no length warning");
  assert.deepEqual(length(lintVideo(over(explainerFixture()), context({ brief: explainerBrief() }))), []);
  assert.match(messages(length(lintVideo({ ...fixture(), target_minutes: [5, 6] }, context()))), /the target is 5-6/, "under the lower end still warns");
  assert.match(messages(length(lintVideo(over(dramaFixture()), context({ brief: dramaBrief() })))), /the target is 0\.1-0\.2/);
  // Under the floor is still an error, whatever the target says.
  const saved = process.env.VIDEO_MIN_EPISODE_MINUTES;
  delete process.env.VIDEO_MIN_EPISODE_MINUTES;
  try {
    const short = lintVideo({ ...fixture(), target_minutes: [8, 12] }, context());
    assert.ok(short.errors.some((each) => each.path === "scenes" && /at least 8: write more narration/.test(each.message)), messages(short.errors));
  } finally {
    if (saved === undefined) delete process.env.VIDEO_MIN_EPISODE_MINUTES;
    else process.env.VIDEO_MIN_EPISODE_MINUTES = saved;
  }
});

test("a drama with a cast is read against the craft spec: the missed rows are warnings, a narrated drama gets none", () => {
  const drama = lintVideo(dramaFixture(), context({ brief: dramaBrief() }));
  assert.deepEqual(drama.errors, []);
  const craft = drama.warnings.filter((warning) => /^craft /.test(warning.message));
  assert.ok(craft.some((warning) => warning.path === "scenes" && /^craft hook\.opening: shots that start in the first 10 s 2, target ≥ 4; open inside the event/.test(warning.message)), messages(drama.warnings));
  assert.ok(craft.every((warning) => /drama-craft\.md\)$/.test(warning.message)), "every row points at the spec");
  assert.ok(!craft.some((warning) => /craft pace\.short|craft size\.setups|craft motion\.locked/.test(warning.message)), "rows that only report numbers are not warnings");
  const narrated = dramaFixture();
  narrated.characters = [];
  for (const scene of narrated.scenes) {
    delete scene.data.characters;
    for (const line of scene.lines) delete line.speaker;
  }
  const result = lintVideo(narrated, context({ brief: dramaBrief() }));
  assert.deepEqual(result.errors, []);
  assert.ok(!result.warnings.some((warning) => /^craft /.test(warning.message)), "a retelling with no cast follows its own references");
});

test("the median-shot warning starts under 2 s for a drama with a cast and points at the craft spec; a narrated drama keeps 3 s", () => {
  const quick = (doc, text) => {
    for (const scene of doc.scenes) {
      delete scene.data.fit;
      scene.lines = [{ ...scene.lines[0], text }];
    }
  };
  const cast = dramaFixture();
  quick(cast, "走。");
  const fast = lintVideo(cast, context({ brief: dramaBrief() }));
  assert.ok(fast.warnings.some((warning) => /the median shot is 1\.3 s; the measured dramas sit at 1\.5–2\.25 s, but under 2 s this pipeline pays a clip per cut: merge some shots \(.*drama-craft\.md §五\)/.test(warning.message)), messages(fast.warnings));
  const steady = dramaFixture();
  quick(steady, "媽，請喝茶，先別急。");
  assert.ok(!lintVideo(steady, context({ brief: dramaBrief() })).warnings.some((warning) => /median shot/.test(warning.message)), "about 2.7 s a shot is what the spec asks for, not a montage");
  const narrated = dramaFixture();
  narrated.characters = [];
  quick(narrated, "媽，請喝茶，先別急。");
  for (const scene of narrated.scenes) {
    delete scene.data.characters;
    for (const line of scene.lines) delete line.speaker;
  }
  assert.ok(lintVideo(narrated, context({ brief: dramaBrief() })).warnings.some((warning) => /the median shot is 2\.7 s; cuts this fast read as a montage/.test(warning.message)), "a narrated drama keeps the older threshold");
});

test("a drama with a cast may time a silent shot with action_seconds; a narrated one may not", () => {
  const doc = dramaFixture();
  doc.scenes[1].action_seconds = 3;
  doc.scenes[1].lines = [];
  const result = lintVideo(doc, context({ brief: dramaBrief() }));
  assert.deepEqual(result.errors, [], messages(result.errors));
  const timeline = estimateTimeline(doc);
  const silent = timeline.scenes.find((scene) => scene.id === doc.scenes[1].id);
  assert.equal(silent.end_frame - silent.start_frame, 90);
  assert.ok(!result.warnings.some((warning) => /craft lines\.empty/.test(warning.message)), "a timed shot is not an empty one");
  const narrated = dramaFixture();
  narrated.characters = [];
  for (const scene of narrated.scenes) {
    delete scene.data.characters;
    for (const line of scene.lines) delete line.speaker;
  }
  narrated.scenes[1].action_seconds = 3;
  narrated.scenes[1].lines = [];
  assert.match(messages(lintVideo(narrated, context({ brief: dramaBrief() })).errors), /requires a drama with a cast and no length floor, or a complete long-anime production policy/);
});

test("a shot cut from another shot's clip must end inside that clip, and the production profile's eight seconds", () => {
  const doc = dramaFixture();
  const bird = doc.scenes.find((scene) => scene.id === "bird");
  delete bird.data.start_frame;
  bird.data.source = { shot: "sea-storm", from_s: 2 };
  const result = lintVideo(doc, context({ brief: dramaBrief() }));
  assert.ok(result.errors.some((error) => error.path === "scenes[3] (bird).data.source" && /cut from sea-storm's clip at 2 s and about [\d.]+ s long, it ends past 10 s/.test(error.message)), messages(result.errors));
  bird.data.source.from_s = 0.3;
  assert.deepEqual(lintVideo(doc, context({ brief: dramaBrief() })).errors, []);
  const series = { production: { profile: { visual_tier: "clips" } } };
  for (const scene of doc.scenes) {
    delete scene.data.fit;
    for (const line of scene.lines) line.text = "媽，請喝茶，先別急。";
  }
  bird.data.source.from_s = 6;
  assert.ok(productionShotProblems(doc, series, estimateTimeline(doc)).some((problem) => problem.path === "scenes[3] (bird).data.source" && /must end inside them/.test(problem.message)));
  bird.data.source.from_s = 1;
  assert.deepEqual(productionShotProblems(doc, series, estimateTimeline(doc)), []);
});
