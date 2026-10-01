// An English narration (`narration_locale: "en"`): the same pipeline, with English as the source
// language of captions, translations, dubs and the description, and a lighter dictionary rule.
import assert from "node:assert/strict";
import { randomBytes } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { defaultRate, dubLocales, speechLexicon } from "../dubs/plan.mjs";
import { targetLocales } from "../i18n/cli.mjs";
import { packageLocalesWanted } from "../package/check.mjs";
import { captionsCurrent } from "../package/cli.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { jpegBytes } from "../qa/test-images.mjs";
import { parseDubLocale } from "../tts/check.mjs";
import { approve } from "./approvals.mjs";
import { enBrief, enFixture, fixture, fixtureLexicon, sandbox } from "./fixtures/load.mjs";
import { hasAcronym, unknownTermsFor } from "./lexicon.mjs";
import { lintVideo } from "./lint.mjs";
import { atomicWrite } from "./paths.mjs";
import { eachLine, narrationLocale, textHash, validateVideo } from "./schema.mjs";
import { alwaysLocales, captionLocalesOf, dubLocalesOf, localeTexts, metadataLocalesOf, readLanguages, runCaptions, writeLanguages } from "./stages.mjs";
import { loadProject } from "./state.mjs";
import { buildTimeline, estimateTimeline, SAMPLE_RATE, speechHash, visualHash } from "./timeline.mjs";
import { sourceHashes } from "./translations.mjs";

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

test("the owner's language choice keeps the narration's own locale and zh-TW, whatever is ticked", () => {
  const en = enFixture();
  assert.deepEqual(alwaysLocales(), ["zh-TW"]);
  assert.deepEqual(alwaysLocales("en"), ["en", "zh-TW"]);
  const jaCaptions = { locales: { ja: { metadata: false, captions: true, dub: false } }, decided_at: "2026-10-01T00:00:00Z" };
  assert.deepEqual(captionLocalesOf(jaCaptions), ["zh-TW", "ja"], "a zh-TW video, as before");
  assert.deepEqual(captionLocalesOf(jaCaptions, "en"), ["en", "zh-TW", "ja"]);
  assert.deepEqual(metadataLocalesOf(jaCaptions, "en"), ["en", "zh-TW"]);
  assert.deepEqual(metadataLocalesOf(null, "en"), null, "without a choice, every translated locale");
  assert.deepEqual(captionLocalesOf(null, "en"), ["zh-TW", "en", "ja", "ko", "zh-CN"]);
  // The panel offers English to an English video too: ticking it adds nothing and dubs nothing.
  const enTicked = { locales: { en: { metadata: true, captions: true, dub: true }, ko: { metadata: true, captions: true, dub: true } }, decided_at: null };
  assert.deepEqual(captionLocalesOf(enTicked, "en"), ["en", "zh-TW", "ko"]);
  assert.deepEqual(metadataLocalesOf(enTicked, "en"), ["en", "zh-TW", "ko"]);
  assert.deepEqual(dubLocalesOf(enTicked, en), ["ko"]);
  assert.deepEqual(dubLocalesOf(null, en), ["zh-TW", "ja", "ko"], "the English video's default dubs");
  assert.deepEqual(dubLocalesOf(null, fixture()), ["en", "ja", "ko"], "the zh-TW default, as before");
  // The narration always has captions; an untranslated locale cannot.
  const manifest = { speech_hash: "s", locales: { en: {}, ja: {} }, skipped: {} };
  assert.equal(captionsCurrent(manifest, "s", ["en", "zh-TW", "ja"], { ja: {} }, null, "en"), true, "zh-TW has no translation to cut");
  assert.equal(captionsCurrent({ ...manifest, locales: { ja: {} } }, "s", ["en", "zh-TW", "ja"], { ja: {} }, null, "en"), false, "the narration's captions are missing");
});

/** The English example after every stage up to the approved cut, translated into every other locale. */
function finishedEnglishVideo() {
  const box = sandbox("fixture-en", "en");
  const doc = enFixture();
  for (const locale of targetLocales(doc)) {
    const lines = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, { source_hash: textHash(line.text), text: `${locale} line ${line.id}` }]));
    const chapters = Object.fromEntries(doc.scenes.filter((scene) => scene.chapter).map((scene) => [scene.id, `${locale} ${scene.id}`]));
    atomicWrite(path.join(box.dir, "i18n", `${locale}.json`), `${JSON.stringify({ title: `${locale} title`, description: `${locale} description`, tags: [`${locale} tag`], chapters, source_hashes: sourceHashes(doc), lines }, null, 2)}\n`);
  }
  const project = loadProject({ slug: box.slug, root: box.root });
  const samples = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
  const timeline = { ...buildTimeline(doc, samples), speech_hash: speechHash(project.doc, project.lexicon) };
  mkdirSync(box.workdir, { recursive: true });
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  writeFileSync(path.join(box.workdir, "thumbnail.jpg"), jpegBytes(1280, 720, 4000));
  writeFileSync(path.join(box.workdir, "final.mp4"), randomBytes(2048));
  atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, speech_hash: timeline.speech_hash, visual_hash: visualHash(project.doc), problems: [], metrics: { frames: timeline.total_frames, loudness: { integrated: -14 }, psnr: [] } }));
  return box;
}

function englishContext(box) {
  const out = { stdout: "", stderr: "" };
  const fetchImpl = async (url) => (url.endsWith("/judge/policy") ? Response.json({ detail: "Not Found" }, { status: 404 }) : new Response("", { status: 200 }));
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: `mkv_${"q".repeat(43)}`, MOKAAIR_SITE: "https://site.test" },
    home: box.base,
    fetch: fetchImpl,
    sleep: async () => {},
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-10-01T02:00:00Z"),
  };
  return { out, ctx };
}

test("an English video whose choice ticks only Japanese captions keeps its own captions and description, and zh-TW's, through captions, qa and package", async (t) => {
  const box = finishedEnglishVideo();
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  writeLanguages(box.workdir, { locales: { ja: { metadata: false, captions: true, dub: false } }, decided_at: "2026-10-01T00:00:00Z" });
  assert.deepEqual(readLanguages(box.workdir).locales, { ja: { metadata: false, captions: true, dub: false } });

  const manifest = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir, now: new Date("2026-10-01T01:00:00Z") });
  assert.deepEqual(Object.keys(manifest.locales), ["en", "zh-TW", "ja"], "ko and zh-CN are translated but not chosen");

  await approve({ gate: "audio", docDir: box.dir, workdir: box.workdir, now: new Date("2026-10-01T01:00:00Z") });
  const qa = englishContext(box);
  await main(["qa", "--slug", box.slug], qa.ctx);
  const items = Object.fromEntries(JSON.parse(readFileSync(path.join(box.workdir, "review", "qa.json"), "utf8")).items.map((item) => [item.id, item]));
  assert.equal(items.captions.ok, true, items.captions.detail);
  assert.match(items.captions.detail, /^caption files for en, zh-TW, ja, every translation current/);
  assert.equal(items.metadata.ok, true, items.metadata.detail);
  assert.match(items.metadata.detail, /for en, zh-TW; 3 chapters$/);

  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir, now: new Date("2026-10-01T01:30:00Z") });
  const packaged = englishContext(box);
  assert.equal(await main(["package", "--slug", box.slug], packaged.ctx), EXIT.ok, packaged.out.stderr + packaged.out.stdout);
  const upload = path.join(box.workdir, "upload");
  const metadata = JSON.parse(readFileSync(path.join(upload, "metadata.json"), "utf8"));
  assert.equal(metadata.default_language, "en");
  assert.deepEqual(Object.keys(metadata.localizations), ["zh-TW"]);
  assert.deepEqual(metadata.captions, ["captions/en.srt", "captions/ja.srt", "captions/zh-TW.srt"]);
  assert.deepEqual(metadata.skipped_caption_locales, {});
  assert.deepEqual(metadata.dubs, []);
  assert.ok(existsSync(path.join(upload, "description.en.txt")) && existsSync(path.join(upload, "description.zh-TW.txt")));
  assert.ok(!existsSync(path.join(upload, "description.ja.txt")), "Japanese titles were not chosen");
  assert.match(packaged.out.stdout, /\[x\] descriptions: descriptions for en, zh-TW/);
  assert.match(packaged.out.stdout, /\[x\] captions: caption files for en, zh-TW, ja/);
  assert.deepEqual(packageLocalesWanted(box.workdir).locales, ["en", "zh-TW", "ja"], "the package check reads the narration from metadata.json");
});
