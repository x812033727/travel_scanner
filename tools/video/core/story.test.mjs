import assert from "node:assert/strict";
import test from "node:test";

import { fixture, fixtureLexicon, storyBrief, storyFixture, storySeries } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";
import { validateVideo } from "./schema.mjs";
import { isStory, MEAN_SHOT_SECONDS, MIN_STORY_SOURCES, namePattern, STORY_CHAPTERS, STORY_KIND, STORY_RULES, storyProblems } from "./story.mjs";
import { estimateTimeline } from "./timeline.mjs";

const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: storyBrief(), series: storySeries(), others: [], translations: {}, ...overrides });
const found = (problems) => problems.map((problem) => [problem.path, problem.message]);
const story = (doc, series = storySeries()) => storyProblems(doc, series, estimateTimeline(doc));

test("the story example is valid and lints clean: five chapters, three sources, stills and the narrator only", () => {
  const doc = storyFixture();
  assert.deepEqual(validateVideo(doc), []);
  const result = lintVideo(doc, context());
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  assert.equal(result.summary.chapters.length, 5);
  assert.deepEqual(story(doc), { errors: [], warnings: [] });
  assert.deepEqual(doc.characters, [], "no cast: the look steps are skipped (state.mjs narratorOnly)");
  assert.equal(storySeries().kind, STORY_KIND);
  assert.ok(isStory(storySeries()));
  assert.ok(!isStory(null) && !isStory({ ...storySeries(), kind: undefined }), "an episode of a plain series is no story");
});

test("the rule list the worker quotes to the writer covers every rule, errors first", () => {
  assert.deepEqual(STORY_RULES.map((rule) => [rule.id, rule.level]), [
    ["stills", "error"],
    ["narrator", "error"],
    ["sources", "error"],
    ["chapters", "error"],
    ["names", "error"],
    ["pace", "warning"],
  ]);
  for (const rule of STORY_RULES) assert.match(rule.rule, /^\S.*\.$/, `${rule.id} reads as prose the writer can follow`);
  assert.match(STORY_RULES.find((rule) => rule.id === "sources").rule, new RegExp(`at least ${MIN_STORY_SOURCES} `));
  assert.match(STORY_RULES.find((rule) => rule.id === "chapters").rule, new RegExp(`^${STORY_CHAPTERS.min} to ${STORY_CHAPTERS.max} chapters`));
});

test("every shot of a story is a still: a clip, written out or left to the default, is an error", () => {
  const doc = storyFixture();
  doc.scenes[1].data.visual = "clip";
  delete doc.scenes[3].data.visual;
  assert.deepEqual(found(story(doc).errors), [
    ["scenes[1].data.visual", 'a story is still pictures only: set visual "still" (a clip is bought by the second)'],
    ["scenes[3].data.visual", 'a story is still pictures only: set visual "still" (a clip is bought by the second)'],
  ]);
});

test("every line of a story is the narrator's, even when a character is on screen", () => {
  const doc = storyFixture();
  doc.characters = [{ id: "clerk", name: "店員", appearance: "a cheerful supermarket cashier in a green apron, short curly hair, round glasses", voice: { provider: "gemini", name: "Kore" } }];
  doc.scenes[0].data.characters = ["clerk"];
  doc.scenes[0].lines[1].speaker = "clerk";
  doc.scenes[1].lines[0].speaker = "narrator";
  assert.deepEqual(validateVideo(doc), [], "the drama format allows a speaking character; the story does not");
  assert.deepEqual(found(story(doc).errors), [["scenes[0].lines[1] (mv8c).speaker", 'a story is narrated: every line is the narrator\'s, and "clerk" speaks this one']]);
});

test("a story needs three sources, each an https URL", () => {
  const doc = storyFixture();
  doc.sources.pop();
  assert.deepEqual(found(story(doc).errors), [["sources", "a story needs at least 3 sources for its facts; it has 2"]]);
  const plain = storyFixture();
  plain.sources[1].url = "http://en.wikipedia.org/wiki/Barcode";
  plain.sources[2].url = "wikipedia: GS1";
  assert.deepEqual(found(story(plain).errors), [
    ["sources[1].url", "a story's source is an https URL the checker can open"],
    ["sources[2].url", "a story's source is an https URL the checker can open"],
  ]);
  delete plain.sources;
  assert.deepEqual(found(story(plain).errors), [["sources", "a story needs at least 3 sources for its facts; it has 0"]]);
});

test("a story has five to seven chapters", () => {
  const few = storyFixture();
  delete few.scenes[2].chapter;
  delete few.scenes[4].chapter;
  assert.deepEqual(found(story(few).errors), [["scenes", "a story has 5 to 7 chapters (the hook, the origin, the idea, the business, the turn, where it stands now); this one has 3"]]);
  const seven = storyFixture();
  seven.scenes[1].chapter = "號碼的主人";
  seven.scenes[10].chapter = "結尾";
  assert.deepEqual(story(seven).errors, []);
  seven.scenes[3].chapter = "海灘";
  assert.match(story(seven).errors[0].message, /this one has 8$/);
});

test("a picture's words never carry the story's names; the narration may say them", () => {
  const doc = storyFixture();
  assert.ok(doc.scenes[3].lines[0].text.includes("伍德蘭") && storySeries().names.includes("伍德蘭"), "the example narrates a name the pictures may not show");
  doc.scenes[0].data.prompt += ", an ibm cash register on the counter";
  doc.scenes[2].data.camera = "slow pan right to Bernard  Silver at the door";
  doc.scenes[6].data.negative = "no Juicy Fruit wrapper, no GS1 sign";
  doc.characters = [{ id: "inventor", name: "伍德蘭", appearance: "a young man in 1940s summer clothes", voice: { provider: "gemini", name: "Puck" } }];
  assert.deepEqual(found(story(doc).errors), [
    ["scenes[0].data.prompt", 'names "IBM", which series.json lists among the story\'s names: the narration may say it, a picture may not show it; describe it generically'],
    ["scenes[2].data.camera", 'names "Bernard Silver", which series.json lists among the story\'s names: the narration may say it, a picture may not show it; describe it generically'],
    ["scenes[6].data.negative", 'names "GS1", "Juicy Fruit", which series.json lists among the story\'s names: the narration may say it, a picture may not show it; describe it generically'],
    ["characters[0].name", 'names "伍德蘭", which series.json lists among the story\'s names: the narration may say it, a picture may not show it; describe it generically'],
  ]);
  const listed = storyFixture();
  assert.deepEqual(found(story(listed, { ...storySeries(), names: "IBM" }).errors), [["series.json", "names must be a list of the story's brand, product and people names"]]);
});

test("a name matches as a whole phrase in any case, never inside a longer Latin word", () => {
  assert.ok(namePattern("Marsh").test("the Marsh's checkout lane"));
  assert.ok(!namePattern("Marsh").test("a bag of marshmallows"), "part of a longer word is not the name");
  assert.ok(!namePattern("Bernard Silver").test("a silver scanner"), "one word of a name is not the name");
  assert.ok(namePattern("juicy fruit").test("a pack of JUICY\nFRUIT gum"));
  assert.ok(!namePattern("Juicy Fruit").test("juicy fruits in a bowl"));
  assert.ok(namePattern("7-Eleven").test("a 7-eleven at night"));
  assert.ok(!namePattern("GS1").test("GS12 pallet"));
  assert.ok(namePattern("伍德蘭").test("年輕的伍德蘭在海邊"), "a Chinese name has no spaces to stop at");
  assert.ok(namePattern("Ex(it)?").test("an Ex(it)? sign"), "a name is text, not a pattern");
});

test("a story's pace is a warning: the mean shot between five and eleven seconds", () => {
  const quick = storyFixture();
  for (const scene of quick.scenes.filter((each) => each.template === "shot")) scene.lines = [{ ...scene.lines[0], text: "嗶。" }];
  const fast = story(quick);
  assert.deepEqual(fast.errors, []);
  assert.equal(fast.warnings.length, 1);
  assert.match(fast.warnings[0].message, new RegExp(`^the mean shot runs about \\d+\\.\\d s; a story holds a picture ${MEAN_SHOT_SECONDS.min} to ${MEAN_SHOT_SECONDS.max} s, so merge some shots$`));
  const slow = storyFixture();
  for (const scene of slow.scenes.filter((each) => each.template === "shot")) scene.lines.push({ id: `${scene.lines[0].id}x`, text: "這一段旁白把同一張圖撐得更久，久到觀眾開始等下一張。" });
  assert.match(story(slow).warnings[0].message, /so split some shots$/);
});

test("series.json cannot make a slides video a story", () => {
  const slides = fixture();
  assert.deepEqual(found(story(slides).errors), [["format", 'series.json makes this a story, and a story is a drama: set format "drama"']]);
});
