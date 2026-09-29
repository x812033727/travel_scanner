import assert from "node:assert/strict";
import test from "node:test";

import { dramaFixture, fixture } from "../core/fixtures/load.mjs";
import { assembleItem, captionsItem, COMPILATION_ITEM_IDS, compilationCaptionsItem, disclosureDecision, disclosureItem, item, ITEM_IDS, metadataItem, narrationItem, qaReport, renderItem } from "./checks.mjs";
import { narrationScript, ownerViewpoint, policyRequest, policyVerdict, SCRIPT_MAX_CHARS, VIEWPOINT_MAX_CHARS } from "./policy.mjs";

test("the report lists exactly the eleven items in order and is ok only when every item is", () => {
  assert.deepEqual(ITEM_IDS, ["assemble", "render", "narration", "pace", "captions", "metadata", "facts", "links", "thumbnail", "policy", "disclosure"]);
  const items = ITEM_IDS.map((id) => item(id, true, `${id} fine`));
  const report = qaReport(items, "ab".repeat(32));
  assert.deepEqual(Object.keys(report), ["ok", "final_sha256", "items"]);
  assert.equal(report.ok, true);
  assert.deepEqual(report.items[3], { id: "pace", ok: true, detail: "pace fine" });
  items[7] = item("links", false, "one broken", ["slow"]);
  assert.equal(qaReport(items, null).ok, false);
  assert.deepEqual(qaReport(items, null).items[7], { id: "links", ok: false, detail: "one broken", warnings: ["slow"] });
  assert.equal(qaReport(items, null).final_sha256, null);
  assert.throws(() => qaReport(items.slice(1), null), /exactly assemble, render/);
  assert.throws(() => qaReport([...items].reverse(), null), /exactly assemble, render/);
});

test("assemble reads checks.json: missing, failed, stale or passed", () => {
  assert.match(assembleItem({ checks: null, current: false, finalExists: false }).detail, /final\.mp4 is missing/);
  assert.match(assembleItem({ checks: null, current: false, finalExists: true }).detail, /checks\.json is missing/);
  assert.equal(assembleItem({ checks: { ok: false, problems: ["1 frame short", "loud"] }, current: false, finalExists: true }).detail, "checks failed: 1 frame short; loud");
  assert.match(assembleItem({ checks: { ok: true, problems: [] }, current: false, finalExists: true }).detail, /older script/);
  const passed = assembleItem({ checks: { ok: true, problems: [], metrics: { frames: 1200, loudness: { integrated: -14.1 }, psnr: [{}, {}] } }, current: true, finalExists: true });
  assert.deepEqual(passed, { id: "assemble", ok: true, detail: "1200 frames, -14.1 LUFS, 2 frames matched their slides; every check passed" });
});

test("render reads the manifest and the cache the renderer left", () => {
  const manifest = { visual_hash: "v1", scenes: [{ id: "hook", states: [{ still: "frames/aaaa.png" }, { still: "frames/bbbb.png" }] }], thumbnail: "thumbnail.jpg" };
  const base = { visual: "v1", speech: "s1", subtitles: null, burnIn: false, hasThumbnail: true };
  assert.match(renderItem({ ...base, manifest: null, cache: null }).detail, /missing; run render/);
  assert.match(renderItem({ ...base, manifest: { ...manifest, visual_hash: "old" }, cache: {} }).detail, /older script/);
  const clean = renderItem({ ...base, manifest, cache: { aaaa: { problems: [] }, cccc: { problems: ["unused state, stale problem"] } } });
  assert.deepEqual(clean, { id: "render", ok: true, detail: "2 slide states drawn with no layout, glyph or font problem, thumbnail included" });
  const clipped = renderItem({ ...base, manifest, cache: { bbbb: { problems: ["the code panel shows 9 of 13 lines; shorten the code"] } } });
  assert.deepEqual([clipped.ok, clipped.detail], [false, "hook state 1: the code panel shows 9 of 13 lines; shorten the code"]);
  assert.match(renderItem({ ...base, manifest: { ...manifest, thumbnail: null }, cache: {} }).detail, /thumbnail was not drawn/);
  const drama = renderItem({ ...base, burnIn: true, subtitles: "sub1", manifest: { ...manifest, speech_hash: "s1", subtitles_hash: "old" }, cache: {} });
  assert.match(drama.detail, /subtitle strips for an older narration/);
  assert.equal(renderItem({ ...base, burnIn: true, subtitles: "sub1", manifest: { ...manifest, speech_hash: "s1", subtitles_hash: "sub1" }, cache: {} }).ok, true);
});

test("narration needs the approved timeline to be the current one", () => {
  assert.match(narrationItem({ approval: { status: "absent" }, current: false }).detail, /missing; run tts/);
  assert.match(narrationItem({ approval: { status: "approved" }, current: false }).detail, /older script/);
  assert.match(narrationItem({ approval: { status: "missing" }, current: true }).detail, /not been approved/);
  assert.match(narrationItem({ approval: { status: "stale" }, current: true }).detail, /changed since/);
  assert.deepEqual(narrationItem({ approval: { status: "approved", entry: { approved_at: "2026-09-27T01:00:00Z" } }, current: true }), { id: "narration", ok: true, detail: "timeline.json approved at 2026-09-27T01:00:00Z" });
});

test("captions: stale translations fail, reading speed only warns, every locale needs a file", () => {
  const locales = ["zh-TW", "en"];
  const manifest = { locales: { "zh-TW": { cues: 9, problems: ["cue 3 (k7p2): 11.2 characters a second, above 9"] }, en: { cues: 9, problems: [] } }, skipped: {} };
  const hasFile = () => true;
  const fine = captionsItem({ lintWarnings: [{ path: "scenes", message: "about 1.2 minutes" }], manifest, current: true, locales, hasCaptionFile: hasFile });
  assert.deepEqual(fine, { id: "captions", ok: true, detail: "caption files for zh-TW, en, every translation current", warnings: ["zh-TW: cue 3 (k7p2): 11.2 characters a second, above 9"] });
  const stale = captionsItem({
    lintWarnings: [
      { path: "i18n/en.json", message: "2 translations older than the zh-TW line: k7p2, m4qa" },
      { path: "i18n/en.json", message: "translations older than the zh-TW text: title, chapter hook" },
      { path: "i18n/en.json", message: "chapter titles for scenes that no longer open a chapter: old; i18n-merge drops them" },
    ],
    manifest,
    current: true,
    locales,
    hasCaptionFile: hasFile,
  });
  assert.equal(stale.ok, false);
  assert.equal(stale.detail, "i18n/en.json: 2 translations older than the zh-TW line: k7p2, m4qa; i18n/en.json: translations older than the zh-TW text: title, chapter hook");
  assert.deepEqual(stale.warnings, ["i18n/en.json: chapter titles for scenes that no longer open a chapter: old; i18n-merge drops them", "zh-TW: cue 3 (k7p2): 11.2 characters a second, above 9"]);
  assert.match(captionsItem({ lintWarnings: [], manifest: null, current: false, locales, hasCaptionFile: hasFile }).detail, /manifest\.json is missing/);
  assert.match(captionsItem({ lintWarnings: [], manifest, current: false, locales, hasCaptionFile: hasFile }).detail, /older narration/);
  const skipped = captionsItem({ lintWarnings: [], manifest: { ...manifest, skipped: { en: ["k7p2"] } }, current: true, locales, hasCaptionFile: hasFile });
  assert.equal(skipped.detail, "en: no caption file, 1 lines missing or older than zh-TW (k7p2)");
  assert.equal(captionsItem({ lintWarnings: [], manifest, current: true, locales: [...locales, "ja"], hasCaptionFile: hasFile }).detail, "ja: no caption file");
  assert.equal(captionsItem({ lintWarnings: [], manifest, current: true, locales, hasCaptionFile: (locale) => locale !== "en" }).detail, "en: no caption file");
  const overlap = captionsItem({ lintWarnings: [], manifest: { ...manifest, locales: { ...manifest.locales, en: { problems: ["cue 2 (m4qa): overlaps the previous cue"] } } }, current: true, locales, hasCaptionFile: hasFile });
  assert.deepEqual([overlap.ok, overlap.detail], [false, "en: cue 2 (m4qa): overlaps the previous cue"]);
});

test("metadata gathers YouTube's limits and the chapter rules", () => {
  const ok = metadataItem({ problems: [], tagProblems: [], chapterProblems: [], locales: ["zh-TW", "en"], chapters: 4, timelineCurrent: true });
  assert.deepEqual(ok, { id: "metadata", ok: true, detail: "title, description and tags within YouTube's limits for zh-TW, en; 4 chapters" });
  const bad = metadataItem({ problems: ["en.title: 120 characters, at most 100"], tagProblems: ["youtube.tags: 600 characters counted YouTube's way, at most 500"], chapterProblems: ['chapter "x" lasts 4.0 s; YouTube needs 10 s'], locales: ["zh-TW"], chapters: 3, timelineCurrent: true });
  assert.equal(bad.ok, false);
  assert.equal(bad.detail, 'en.title: 120 characters, at most 100; youtube.tags: 600 characters counted YouTube\'s way, at most 500; chapter "x" lasts 4.0 s; YouTube needs 10 s');
  assert.match(metadataItem({ problems: [], tagProblems: [], chapterProblems: [], locales: ["zh-TW"], chapters: 0, timelineCurrent: false }).detail, /chapter times are unknown/);
});

test("disclosure: slides with a stock voice need none, a drama always does, and the item never fails", () => {
  const slides = disclosureDecision(fixture());
  assert.equal(slides.synthetic, false);
  const drama = disclosureDecision(dramaFixture());
  assert.equal(drama.synthetic, true);
  assert.deepEqual(disclosureItem(slides, null).ok, true);
  assert.match(disclosureItem(slides, null).detail, /^no disclosure needed: slides read by a stock TTS voice/);
  assert.match(disclosureItem(drama, true).detail, /^tick altered or synthetic content: a drama.*; written to upload\/metadata\.json$/);
  assert.match(disclosureItem(drama, false).detail, /already says so$/);
});

test("the policy request is exactly the judge's slug, script and viewpoint", () => {
  const doc = fixture();
  const brief = "# 標題\n\n## 觀眾看完能做到的事\n挑模型\n\n## 站主觀點\n<!-- 草稿 -->\n排行榜只是起點；先看工作類型。\n\n## 章節大綱\n1. 開場\n";
  const request = policyRequest({ doc, brief });
  assert.deepEqual(Object.keys(request), ["slug", "script", "viewpoint"], "the endpoint refuses any other field");
  assert.equal(request.slug, "fixture-minimal");
  assert.equal(request.viewpoint, "排行榜只是起點；先看工作類型。");
  const lines = doc.scenes.map((scene) => scene.lines.map((line) => line.text));
  assert.equal(request.script, `${lines[0].join("\n")}\n\n${lines[1].join("\n")}\n\n${lines[2].join("\n")}`, "every line in order, a blank line between scenes");
  assert.equal(narrationScript(doc).split("\n\n").length, 3);
  assert.equal(ownerViewpoint(null), "");
  assert.equal(ownerViewpoint("## 觀眾\n上班族"), "", "a brief without the section sends an empty viewpoint");
  assert.equal(policyRequest({ doc, brief: null }).viewpoint, "");
  // The limits the endpoint enforces, counted in characters as Python does.
  const long = fixture();
  long.scenes[0].lines[0].text = "字".repeat(SCRIPT_MAX_CHARS + 5);
  assert.equal([...policyRequest({ doc: long, brief: null }).script].length, SCRIPT_MAX_CHARS);
  assert.equal([...policyRequest({ doc, brief: `## 站主觀點\n${"觀".repeat(VIEWPOINT_MAX_CHARS + 1)}` }).viewpoint].length, VIEWPOINT_MAX_CHARS);
});

test("the verdict is the judge's passed flag with its note, and never a pass by default", () => {
  const note = "Jev：符合立場 0.82、有示範 0.70、建議 0.05、業配 0.10，通過";
  assert.deepEqual(policyVerdict({ stance: 0.82, demo: 0.7, advice: 0.05, sponsored: 0.1, passed: true, note }), { ok: true, detail: note });
  const failed = "Jev：符合立場 0.40、有示範 0.70、建議 0.05、業配 0.10，沒過";
  assert.deepEqual(policyVerdict({ stance: 0.4, demo: 0.7, advice: 0.05, sponsored: 0.1, passed: false, note: failed }), { ok: false, detail: failed });
  assert.deepEqual(policyVerdict({ stance: 0.91, demo: 0.8, advice: 0.05, sponsored: 0, passed: true, note: "" }), { ok: true, detail: "Jev passed the narration: stance 0.91, demo 0.80, advice 0.05, sponsored 0.00" });
  assert.deepEqual(policyVerdict({ passed: false }), { ok: false, detail: "Jev did not pass the narration" });
  assert.deepEqual(policyVerdict({ ok: true, note: "not the field the endpoint uses" }), { ok: false, detail: "the judge answered without a verdict" });
  assert.deepEqual(policyVerdict({}), { ok: false, detail: "the judge answered without a verdict" });
  assert.equal(policyVerdict(null).ok, false);
});

test("captions look only at the wanted locales' translations, and a dub track given up on warns instead of failing", () => {
  const manifest = { locales: { "zh-TW": { cues: 9, problems: [] }, en: { cues: 9, problems: [] } }, skipped: {} };
  const staleKo = [{ path: "i18n/ko.json", message: "2 translations older than the zh-TW line: k7p2, m4qa" }];
  const ignored = captionsItem({ lintWarnings: staleKo, manifest, current: true, locales: ["zh-TW", "en"], hasCaptionFile: () => true, skippedDubs: { en: "two shortening rounds were not enough" } });
  assert.deepEqual(ignored, { id: "captions", ok: true, detail: "caption files for zh-TW, en, every translation current", warnings: ["en: dub track skipped (two shortening rounds were not enough); its captions follow the narration"] });
  const wanted = captionsItem({ lintWarnings: staleKo, manifest, current: true, locales: ["zh-TW", "en", "ko"], hasCaptionFile: () => true });
  assert.equal(wanted.ok, false);
  assert.match(wanted.detail, /^i18n\/ko\.json: 2 translations older/);
  assert.match(captionsItem({ lintWarnings: [], manifest, current: true, locales: ["zh-TW"], hasCaptionFile: () => true, skippedDubs: { ja: "" } }).warnings[0], /ja: dub track skipped \(no reason recorded\)/);
});

test("a compilation's report has its six items and says so, and its captions item reads compile's merge", () => {
  assert.deepEqual(COMPILATION_ITEM_IDS, ["assemble", "captions", "metadata", "links", "thumbnail", "disclosure"]);
  const items = COMPILATION_ITEM_IDS.map((id) => item(id, true, `${id} fine`));
  const report = qaReport(items, "ab".repeat(32), COMPILATION_ITEM_IDS);
  assert.deepEqual(Object.keys(report), ["ok", "final_sha256", "kind", "items"]);
  assert.equal(report.kind, "compilation");
  assert.equal(report.ok, true);
  assert.throws(() => qaReport(items, null), /exactly assemble, render/, "the eleven are the default");
  assert.throws(() => qaReport(ITEM_IDS.map((id) => item(id, true, "")), null, COMPILATION_ITEM_IDS), /exactly assemble, captions/);
  assert.equal("kind" in qaReport(ITEM_IDS.map((id) => item(id, true, "")), null), false);
  assert.match(assembleItem({ checks: { ok: true }, current: false, finalExists: true, command: "compile", stale: "other cuts or cards" }).detail, /^checks\.json was written for other cuts or cards; run compile again$/);
  assert.match(assembleItem({ checks: null, current: false, finalExists: false, command: "compile" }).detail, /run compile$/);
  assert.match(metadataItem({ problems: [], tagProblems: [], chapterProblems: [], locales: ["zh-TW"], chapters: 0, timelineCurrent: false, command: "compile" }).detail, /run compile$/);
  const manifest = { compilation_hash: "h", locales: { "zh-TW": { cues: 6, problems: [] }, en: { cues: 6, problems: ["cue 4 overlaps the previous cue"] } }, skipped: { ja: ["wuxia-ep-2"] } };
  const locales = ["zh-TW", "en", "ja"];
  const fine = compilationCaptionsItem({ lintWarnings: [{ path: "scenes", message: "x" }], manifest: { ...manifest, locales: { ...manifest.locales, en: { cues: 6, problems: [] } }, skipped: {} }, current: true, locales: ["zh-TW", "en"], hasCaptionFile: () => true });
  assert.deepEqual(fine, { id: "captions", ok: true, detail: "caption files for zh-TW, en, merged from every episode" });
  const broken = compilationCaptionsItem({ lintWarnings: [{ path: "i18n/en.json", message: "not translated: title" }], manifest, current: true, locales, hasCaptionFile: () => true });
  assert.equal(broken.ok, false);
  assert.equal(broken.detail, "i18n/en.json: not translated: title; en: cue 4 overlaps the previous cue; ja: no caption file, 1 episodes have none (wuxia-ep-2)");
  assert.match(compilationCaptionsItem({ lintWarnings: [], manifest: null, current: false, locales, hasCaptionFile: () => true }).detail, /missing; run compile/);
  assert.match(compilationCaptionsItem({ lintWarnings: [], manifest, current: false, locales, hasCaptionFile: () => true }).detail, /merged for other cuts; run compile again/);
  assert.equal(compilationCaptionsItem({ lintWarnings: [], manifest, current: true, locales: ["zh-TW"], hasCaptionFile: () => false }).detail, "zh-TW: no caption file");
});

test("disclosure for illustrated slides: stylised pictures under a licensed bed need none; a realistic look or generated music does", async () => {
  const { illustratedFixture } = await import("../core/fixtures/load.mjs");
  const { REALISTIC_PRESETS } = await import("./checks.mjs");
  assert.deepEqual(REALISTIC_PRESETS, ["cinematic-3d"]);
  const doc = illustratedFixture();
  const licensed = disclosureDecision(doc, { musicSource: "track" });
  assert.equal(licensed.synthetic, false);
  assert.match(licensed.reason, /stylised tech-story pictures, a licensed music bed/);
  assert.equal(disclosureDecision(doc, { musicSource: "generated" }).synthetic, true);
  const realistic = illustratedFixture();
  realistic.look = { preset: "cinematic-3d" };
  assert.equal(disclosureDecision(realistic, { musicSource: "track" }).synthetic, true);
  const plain = fixture();
  plain.music = { prompt: "soft piano" };
  assert.equal(disclosureDecision(plain, { musicSource: "generated" }).synthetic, true, "generated music under plain slides is disclosed too");
  assert.equal(disclosureDecision(fixture()).synthetic, false);
});
