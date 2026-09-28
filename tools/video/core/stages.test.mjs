import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { dubScript, translationHash } from "../dubs/plan.mjs";
import { sandbox } from "./fixtures/load.mjs";
import { atomicWrite, readJson } from "./paths.mjs";
import { eachLine, textHash } from "./schema.mjs";
import { captionLocalesOf, chosenLocales, dubsForUpload, LANGUAGES_FILE, readLanguages, runCaptions, writeLanguages } from "./stages.mjs";
import { dubArtifacts, loadProject } from "./state.mjs";
import { estimateTimeline, speechHash } from "./timeline.mjs";

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
  writeFileSync(files.timeline, JSON.stringify({ locale, format: "m4a", file: `${locale}.m4a`, speech_hash: timeline.speech_hash, translation_hash: words, total_frames: timeline.total_frames, tempo_max: 1.05, windows: [], lines }));
  writeFileSync(files.track("m4a"), "not really audio");
}

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
