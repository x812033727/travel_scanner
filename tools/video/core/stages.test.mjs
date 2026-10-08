import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { dubFingerprint, dubScript, translationHash } from "../dubs/plan.mjs";
import { pinBranding, presentationTimeline, validateBranding } from "./branding.mjs";
import { parseSrt } from "./captions.mjs";
import { sandbox } from "./fixtures/load.mjs";
import { atomicWrite, readJson } from "./paths.mjs";
import { eachLine, textHash } from "./schema.mjs";
import { captionLocalesOf, captionTimelineOf, chosenLocales, currentDub, dubsForUpload, LANGUAGES_FILE, readLanguages, runCaptions, writeLanguages } from "./stages.mjs";
import { dubArtifacts, loadProject } from "./state.mjs";
import { estimateTimeline, frameToMs, speechHash } from "./timeline.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

function translationFor(doc, prefix) {
  const lines = {};
  for (const { line } of eachLine(doc)) lines[line.id] = { source_hash: textHash(line.text), text: `${prefix} ${line.id}` };
  return { title: `${prefix} title`, description: `${prefix} description`, tags: [], chapters: {}, source_hashes: {}, lines };
}

/** A fixture with a translation for each locale named, its narration timed, and the work directory ready. */
function translated(locales) {
  const box = sandbox();
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  const before = loadProject({ slug: box.slug, root: box.root });
  for (const locale of locales) writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), JSON.stringify(translationFor(before.doc, locale.toUpperCase())));
  const project = loadProject({ slug: box.slug, root: box.root });
  const speech = speechHash(project.doc, project.lexicon);
  const timeline = { ...estimateTimeline(project.doc), speech_hash: speech };
  mkdirSync(box.workdir, { recursive: true });
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  return { box, project, speech, timeline };
}

/** A current dub track for a locale, as `dub` leaves it. */
function writeDub(box, project, locale, timeline) {
  const files = dubArtifacts(box.workdir, locale);
  const lines = timeline.lines.map((line) => ({ id: line.id, start_frame: line.start_frame + 5, end_frame: line.start_frame + 5 + Math.ceil(line.audio_samples / 2 / 1600), audio_samples: Math.floor(line.audio_samples / 2), tempo: 1 }));
  const words = translationHash(dubScript(project.doc, project.translations[locale], locale).doc);
  mkdirSync(files.dir, { recursive: true });
  writeFileSync(files.timeline, JSON.stringify({ locale, format: "m4a", file: `${locale}.m4a`, speech_hash: timeline.speech_hash, translation_hash: words, speech_fingerprint: dubFingerprint(project, locale), total_frames: timeline.total_frames, tempo_max: 1.05, windows: [], lines }));
  writeFileSync(files.track("m4a"), "not really audio");
}

function brand(box, timeline, digit = "a") {
  const selection = validateBranding({ schema_version: 1, id: `brand-${digit}`, intro: { file: "intro.mp4", sha256: digit.repeat(64), frames: 150 }, outro: { file: "outro.mp4", sha256: "b".repeat(64), frames: 90 } }, { base: box.workdir });
  pinBranding(box.workdir, selection);
  const applied = { hash: selection.hash, id: selection.id, intro_frames: 150, outro_frames: 90, body_frames: timeline.total_frames, body_file: "body.mp4", body_sha256: "c".repeat(64) };
  atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, speech_hash: timeline.speech_hash, branding: applied }));
  return applied;
}

test("selected bookends shift narration captions once, bind the manifest, and leave the TTS timeline intact", () => {
  const { box, timeline } = translated([]);
  const options = { slug: box.slug, root: box.root, workdir: box.workdir };
  runCaptions(options);
  const captionFile = path.join(box.workdir, "captions", "zh-TW.srt");
  const before = parseSrt(readFileSync(captionFile, "utf8"));
  const originalTimeline = readFileSync(path.join(box.workdir, "timeline.json"), "utf8");
  const applied = brand(box, timeline);
  const manifest = runCaptions(options);
  const written = readFileSync(captionFile, "utf8");
  const after = parseSrt(written);
  assert.equal(manifest.branding_hash, applied.hash);
  assert.deepEqual(after, before.map((cue) => ({ ...cue, start_ms: cue.start_ms + 5000, end_ms: cue.end_ms + 5000 })));
  assert.ok(after.at(-1).end_ms <= frameToMs(timeline.total_frames + 150), "no narration caption crosses into the CTA");
  runCaptions(options);
  assert.equal(readFileSync(captionFile, "utf8"), written, "rerunning does not add the intro offset a second time");
  assert.equal(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"), originalTimeline);
});

test("dub captions accept only the applied branding and use the already padded timeline without extending into the outro", () => {
  const { box, project, speech, timeline } = translated(["en"]);
  writeDub(box, project, "en", timeline);
  const files = dubArtifacts(box.workdir, "en");
  const bodyDub = readJson(files.timeline);
  const applied = brand(box, timeline);
  assert.deepEqual(currentDub(project, box.workdir, "en", speech), { stale: true }, "a body-only dub cannot accompany the padded final");
  assert.deepEqual(dubsForUpload(project, box.workdir, speech, ["en"]).dubs, []);
  const presented = presentationTimeline(bodyDub, applied);
  writeFileSync(files.timeline, JSON.stringify(presented));
  writeLanguages(box.workdir, { locales: { en: { dub: true } } });
  const manifest = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.equal(manifest.locales.en.timing, "dub");
  const cues = parseSrt(readFileSync(path.join(box.workdir, "captions", "en.srt"), "utf8"));
  assert.equal(cues[0].start_ms, Math.round(frameToMs(bodyDub.lines[0].start_frame + 150)));
  assert.ok(cues.at(-1).end_ms <= frameToMs(presented.content_end_frame));
  assert.equal(captionTimelineOf(presented).lines.at(-1).end_frame, presented.content_end_frame);
  assert.equal(dubsForUpload(project, box.workdir, speech, ["en"]).dubs[0].branding_hash, applied.hash);
  writeFileSync(files.timeline, JSON.stringify({ ...presented, content_end_frame: undefined }));
  assert.deepEqual(currentDub(project, box.workdir, "en", speech), { stale: true }, "a hash alone cannot replace the dub's content boundary");
});

test("a changed branding pin refuses to overwrite captions for the still-old final", () => {
  const { box, timeline } = translated([]);
  brand(box, timeline);
  const options = { slug: box.slug, root: box.root, workdir: box.workdir };
  runCaptions(options);
  const captionFile = path.join(box.workdir, "captions", "zh-TW.srt");
  const written = readFileSync(captionFile, "utf8");
  const pin = readJson(path.join(box.workdir, "branding.json"));
  delete pin.hash;
  pin.intro.sha256 = "d".repeat(64);
  pinBranding(box.workdir, validateBranding(pin));
  assert.throws(() => runCaptions(options), /selected branding; run assemble again/);
  assert.equal(readFileSync(captionFile, "utf8"), written);
});

test("a branded final cannot time captions for a newer narration or a body with different duration", () => {
  const { box, timeline } = translated([]);
  brand(box, timeline);
  const options = { slug: box.slug, root: box.root, workdir: box.workdir };
  runCaptions(options);
  const captionFile = path.join(box.workdir, "captions", "zh-TW.srt");
  const before = readFileSync(captionFile, "utf8");
  const checksFile = path.join(box.workdir, "checks.json");
  const checks = readJson(checksFile);
  for (const changed of [
    { ...checks, speech_hash: "old-narration" },
    { ...checks, branding: { ...checks.branding, body_frames: timeline.total_frames + 1 } },
  ]) {
    writeFileSync(checksFile, JSON.stringify(changed));
    assert.throws(() => runCaptions(options), /another body timeline; run assemble again/);
    assert.equal(readFileSync(captionFile, "utf8"), before);
  }
});

test("the language choice is read as the site writes it: only the ticked languages, a dub implying its captions, and nothing without the file", () => {
  const box = sandbox();
  mkdirSync(box.workdir, { recursive: true });
  assert.equal(readLanguages(box.workdir), null, "no file: no choice");
  assert.equal(chosenLocales(null, "captions"), null);
  assert.deepEqual(captionLocalesOf(null), ["zh-TW", "en", "ja", "ko", "zh-CN"], "without a choice every locale is made, as before");

  writeLanguages(box.workdir, { locales: { ja: { metadata: true, captions: false, dub: true }, en: { metadata: true, captions: false, dub: false }, "zh-CN": { metadata: false, captions: false, dub: false }, "zh-TW": { metadata: true } }, decided_at: "2026-09-27T10:00:00Z", synced_at: "2026-09-27T10:05:00Z" });
  const written = readJson(path.join(box.workdir, LANGUAGES_FILE));
  assert.equal(written.synced_at, "2026-09-27T10:05:00Z");
  const choice = readLanguages(box.workdir);
  assert.deepEqual(choice, { locales: { en: { metadata: true, captions: false, dub: false }, ja: { metadata: true, captions: true, dub: true } }, decided_at: "2026-09-27T10:00:00Z" }, "page order, nothing ticked dropped, zh-TW never listed, dub ticks captions");
  assert.deepEqual(chosenLocales(choice, "metadata"), ["en", "ja"]);
  assert.deepEqual(chosenLocales(choice, "captions"), ["ja"]);
  assert.deepEqual(chosenLocales(choice, "dub"), ["ja"]);
  assert.deepEqual(captionLocalesOf(choice), ["zh-TW", "ja"]);

  writeLanguages(box.workdir, { locales: {}, decided_at: "2026-09-27T10:00:00Z" });
  assert.deepEqual(readLanguages(box.workdir), { locales: {}, decided_at: "2026-09-27T10:00:00Z" }, "Traditional Chinese only");
  assert.deepEqual(captionLocalesOf(readLanguages(box.workdir)), ["zh-TW"]);
  writeFileSync(path.join(box.workdir, LANGUAGES_FILE), "[]");
  assert.equal(readLanguages(box.workdir), null, "a file that is not a choice reads as none");
});

test("captions follow the choice: only zh-TW and the chosen locales are written, a dropped locale's files go, and a dub times its captions only when chosen", () => {
  const { box, project, speech, timeline } = translated(["en", "ja", "ko"]);
  const srt = (locale) => path.join(box.workdir, "captions", `${locale}.srt`);
  // No choice: every translated locale, as before.
  const all = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual(Object.keys(all.locales).sort(), ["en", "ja", "ko", "zh-TW"]);

  writeDub(box, project, "en", timeline);
  writeDub(box, project, "ja", timeline);
  writeLanguages(box.workdir, { locales: { en: { metadata: true, captions: true, dub: true }, ja: { metadata: false, captions: true, dub: false } }, decided_at: "2026-09-27T10:00:00Z" });
  const chosen = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual(Object.keys(chosen.locales).sort(), ["en", "ja", "zh-TW"], "ko is translated but not chosen");
  assert.deepEqual(chosen.skipped, {});
  assert.equal(chosen.locales.en.timing, "dub", "en's dub was chosen, so its captions follow the track");
  assert.equal(chosen.locales.ja.timing, "narration", "ja has a track on disk but no dub chosen, so its captions follow the narration");
  assert.ok(existsSync(srt("en")) && existsSync(srt("ja")) && existsSync(srt("zh-TW")));
  assert.ok(!existsSync(srt("ko")) && !existsSync(path.join(box.workdir, "captions", "ko.vtt")), "the unchosen locale's files from the earlier run are gone");

  writeLanguages(box.workdir, { locales: {}, decided_at: "2026-09-27T10:00:00Z" });
  const zhOnly = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual(Object.keys(zhOnly.locales), ["zh-TW"]);
  assert.ok(!existsSync(srt("en")) && !existsSync(srt("ja")));
  assert.equal(readFileSync(srt("zh-TW"), "utf8"), readFileSync(srt("zh-TW"), "utf8"));

  const { dubs, skipped } = dubsForUpload(project, box.workdir, speech, ["en", "ja", "ko"]);
  assert.deepEqual(dubs.map((dub) => dub.locale), ["en", "ja"]);
  assert.deepEqual(skipped, {});
  assert.deepEqual(dubsForUpload(project, box.workdir, speech, ["ja"]).dubs.map((dub) => dub.locale), ["ja"], "only the locales asked for");
  // A locale the worker gave up on stays skipped, whatever track of it is on disk.
  writeFileSync(dubArtifacts(box.workdir, "ja").skipped, JSON.stringify({ reason: "Jev still hears lines wrong after 2 retakes" }));
  const gaveUp = dubsForUpload(project, box.workdir, speech, ["en", "ja"]);
  assert.deepEqual([gaveUp.dubs.map((dub) => dub.locale), gaveUp.skipped], [["en"], { ja: "Jev still hears lines wrong after 2 retakes" }]);
});

test("a translation captioned under the narration's timeline takes its cue changes from the narration's measured ones", () => {
  const box = sandbox();
  // One narration line long enough for two cues, said with a long breath after its first sentence.
  const scriptFile = path.join(box.dir, "video.json");
  const text = "每次有新模型出來，排行榜就換一次第一名。你真的每次都要跟著換嗎？還是先想清楚自己到底要拿它來做什麼？";
  writeFileSync(scriptFile, readFileSync(scriptFile, "utf8").replace("每次有新模型出來，排行榜就換一次第一名，你真的每次都要跟著換嗎？", text));
  const before = loadProject({ slug: box.slug, root: box.root });
  const translation = translationFor(before.doc, "EN");
  translation.lines.k7p2.text = "Every time a new model comes out, the leaderboard changes. Do you really switch each time, or first decide what it is for?";
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translation));
  const project = loadProject({ slug: box.slug, root: box.root });
  let clock = 30;
  const chars = [...text].map((unit) => {
    const start = clock;
    clock += unit === "。" ? 1500 : 170;
    return { text: unit, start_ms: start, end_ms: clock };
  });
  const timeline = { ...estimateTimeline(project.doc), speech_hash: speechHash(project.doc, project.lexicon) };
  const entry = timeline.lines.find((each) => each.id === "k7p2");
  Object.assign(entry, { audio_samples: (clock + 100) * 48, timing: { source: "azure", model: "zh-TW-HsiaoChenNeural", chars } });
  mkdirSync(box.workdir, { recursive: true });
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  writeLanguages(box.workdir, { locales: { en: { captions: true } } });
  runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  const lineStart = frameToMs(entry.start_frame);
  const changes = (locale) =>
    parseSrt(readFileSync(path.join(box.workdir, "captions", `${locale}.srt`), "utf8"))
      .map((cue) => cue.start_ms)
      .filter((start) => start > lineStart + 30 && start < lineStart + clock);
  const [zh, en] = [changes("zh-TW"), changes("en")];
  assert.ok(zh.length >= 1, `the narration line is cut: ${zh}`);
  assert.ok(en.length >= 1 && en.some((start) => zh.includes(start)), `an English cue changes with the narration: ${en} / ${zh}`);
});
