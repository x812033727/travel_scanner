// An English narration (`narration_locale: "en"`): the same pipeline, with English as the source
// language of captions, translations, dubs and the description, and a lighter dictionary rule.
import assert from "node:assert/strict";
import test from "node:test";

import { defaultRate, dubLocales, speechLexicon } from "../dubs/plan.mjs";
import { targetLocales } from "../i18n/cli.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { parseDubLocale } from "../tts/check.mjs";
import { enBrief, enFixture, fixture, fixtureLexicon } from "./fixtures/load.mjs";
import { hasAcronym, unknownTermsFor } from "./lexicon.mjs";
import { lintVideo } from "./lint.mjs";
import { narrationLocale, validateVideo } from "./schema.mjs";
import { localeTexts } from "./stages.mjs";
import { estimateTimeline } from "./timeline.mjs";

const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: enBrief(), others: [], translations: {}, ...overrides });
const messages = (problems) => problems.map((problem) => problem.message).join("\n");

test("a video without the field is narrated in zh-TW, as every video was before", () => {
  assert.equal(narrationLocale(fixture()), "zh-TW");
  assert.equal(narrationLocale({}), "zh-TW");
  assert.deepEqual(validateVideo(fixture()), []);
});

test("the English example lints clean without a dictionary entry for its ordinary words", () => {
  const result = lintVideo(enFixture(), context());
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  assert.equal(result.summary.chapters.length, 3);
});

test("narration_locale must be a caption locale, and default_language must match it", () => {
  const doc = enFixture();
  doc.narration_locale = "fr";
  assert.match(messages(validateVideo(doc)), /must be one of zh-TW, en, ja, ko, zh-CN; leave it out for zh-TW/);
  const mismatch = enFixture();
  mismatch.youtube.default_language = "zh-TW";
  assert.match(messages(validateVideo(mismatch)), /must be en, the narration language/);
  const lang = enFixture();
  lang.voice.lang = "zh-TW";
  assert.match(messages(validateVideo(lang)), /narration is en/);
});

test("an English narration needs the dictionary only for acronyms", () => {
  assert.equal(hasAcronym("SEC"), true);
  assert.equal(hasAcronym("GPT-6"), true);
  assert.equal(hasAcronym("OSWorld"), false);
  assert.equal(hasAcronym("p95"), false);
  const lexicon = { schema_version: 1, terms: { AI: null } };
  assert.deepEqual(unknownTermsFor("The SEC and the Census Bureau saw AI agents on OSWorld.", lexicon, "en"), ["SEC"]);
  assert.deepEqual(unknownTermsFor("Gemini 和 AI", lexicon, "zh-TW"), ["Gemini"]);
  const doc = enFixture();
  doc.scenes[0].lines[0].text = "The SEC noticed the agents first.";
  const { errors } = lintVideo(doc, context());
  assert.equal(errors.length, 1);
  assert.match(errors[0].message, /"SEC" is not in docs\/videos\/lexicon\.json/);
  const known = lintVideo(doc, context({ lexicon: { schema_version: 1, terms: { AI: null, SEC: "S E C" } } }));
  assert.deepEqual(known.errors, []);
});

test("English written-language phrases are errors and process talk is a warning", () => {
  const doc = enFixture();
  doc.scenes[0].lines[0].text = "As shown above, the leaderboard changes weekly.";
  doc.scenes[0].lines[1].text = "We verified the three questions with the vendors.";
  const result = lintVideo(doc, context());
  assert.match(messages(result.errors), /"as shown above" is written language/);
  assert.match(messages(result.warnings), /"we verified" narrates the process/);
});

test("captions, translations and dubs treat English as the source and zh-TW as a target", () => {
  const doc = enFixture();
  const { texts } = localeTexts(doc, {});
  assert.deepEqual(Object.keys(texts), ["en"]);
  assert.deepEqual(targetLocales(doc), ["zh-TW", "ja", "ko", "zh-CN"]);
  assert.deepEqual(dubLocales(doc), ["zh-TW", "ja", "ko", "zh-CN"]);
  assert.deepEqual(dubLocales(fixture()), ["en", "ja", "ko", "zh-CN"]);
  assert.equal(parseDubLocale("zh-TW", "en"), "zh-TW");
  assert.throws(() => parseDubLocale("en", "en"), /the narration is checked without --locale/);
});

test("the English voice never gets a Chinese-character alias, and the dub rate scales from English", () => {
  const lexicon = { schema_version: 1, terms: { API: "A P I", p95: "P 九十五", AI: null } };
  assert.deepEqual(speechLexicon(lexicon, "en").terms, { API: "A P I", p95: null, AI: null });
  assert.deepEqual(speechLexicon(lexicon, "zh-TW").terms, lexicon.terms);
  const doc = enFixture();
  const timeline = estimateTimeline(doc);
  const anchor = defaultRate("en", doc, null);
  assert.equal(anchor, 15);
  // A zh-TW dub of an English narration reads about 5.8 characters where English reads 15.
  const measured = defaultRate("zh-TW", doc, timeline);
  assert.ok(measured > 0 && measured < defaultRate("ja", doc, timeline), `zh-TW ${measured} should be slower than ja`);
});

test("the upload metadata of an English video defaults to English and localizes the rest", () => {
  const doc = enFixture();
  const timeline = estimateTimeline(doc);
  const { metadata, problems } = composeMetadata({ doc, timeline, translations: { "zh-TW": { title: "哪個 AI 模型值得付錢？", description: "三個問題。" } } });
  assert.deepEqual(problems, []);
  assert.equal(metadata.default_language, "en");
  assert.equal(metadata.title, doc.youtube.title);
  assert.match(metadata.description, /📌 Chapters/);
  assert.deepEqual(Object.keys(metadata.localizations), ["zh-TW"]);
});
