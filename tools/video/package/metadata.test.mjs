import assert from "node:assert/strict";
import { readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { compilationDocument, compilationLayout, compilationTimeline } from "../core/compilation.mjs";
import { COMPILATION_REVIEW_FILE, publicTexts, reviewHash } from "../core/compilation-review.mjs";
import { readJson } from "../core/paths.mjs";
import { writeLanguages } from "../core/stages.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, writeTranslations } from "../compile/fixture.mjs";
import { composeMetadata } from "./metadata.mjs";

test("cardless compilation descriptions use revised chapter titles on an older measured timeline", () => {
  const episodes = [{ slug: "mystery-e020", number: 20, title: "她還活著" }, { slug: "mystery-e023", number: 23, title: "舊名" }];
  const doc = compilationDocument({ series: "mystery", episodes, chapterCards: false });
  const timeline = compilationTimeline(compilationLayout(doc, episodes.map((episode) => ({ ...episode, frames: 3600 }))), doc.compilation.titles);
  doc.youtube = { ...doc.youtube, title: "追查失蹤的人", description: "從第一個問題開始。", tags: [] };
  doc.compilation.titles["mystery-e020"] = "門後的腳步";
  delete doc.compilation.titles["mystery-e023"];
  const { metadata } = composeMetadata({ doc, timeline, translations: { en: { title: "The mystery", description: "Follow the clues.", chapters: { "mystery-e020": "Footsteps" } } } });
  assert.equal(timeline.chapters[0].title, "第 20 集 她還活著", "the measured cut is deliberately old");
  assert.deepEqual(metadata.chapters, [{ at: "00:00", title: "第 20 集 門後的腳步" }, { at: "02:00", title: "第 23 集" }]);
  assert.doesNotMatch(metadata.description, /她還活著|舊名/);
  assert.match(metadata.localizations.en.description, /00:00 Footsteps\n02:00 第 23 集/);
});

test("package requires fresh reviews of published compilation text before replacing an existing package", async (t) => {
  const box = compilationSandbox({ chapterCards: false });
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  writeTranslations(box, box.doc);
  const total = EPISODES.reduce((sum, slug) => sum + EPISODE_FRAMES[slug], 0) + 120;
  const compiled = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["compile", "--slug", box.slug], compiled.ctx), EXIT.ok, compiled.out.stderr);
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir });
  const packageRun = async () => {
    const run = compileContext(box, fakeFfmpeg({ total }));
    return { code: await main(["package", "--slug", box.slug], run.ctx), out: run.out };
  };
  assert.equal((await packageRun()).code, EXIT.ok, "explicit no-mystery context keeps prior behavior");
  const metadataFile = path.join(box.workdir, "upload", "metadata.json");
  const existing = readFileSync(metadataFile, "utf8");
  const info = path.join(box.dir, "compilation.json");
  writeFileSync(info, "{}");
  const unknown = await packageRun();
  assert.equal(unknown.code, EXIT.usage);
  assert.match(unknown.out.stderr, /mystery context is unknown/);
  assert.equal(readFileSync(metadataFile, "utf8"), existing);
  const context = { mysteries: [{ id: "m1", answer: "她還活著", revealed: 20 }], reveal_schedule: [{ mystery: "m1", revealed: 20 }] };
  writeFileSync(info, JSON.stringify({ spoiler_context: context }));
  assert.equal((await packageRun()).code, EXIT.owner);
  assert.equal(readFileSync(metadataFile, "utf8"), existing);
  const translations = Object.fromEntries(["en", "ja", "ko", "zh-CN"].map((locale) => [locale, readJson(path.join(box.dir, "i18n", `${locale}.json`), null)]));
  const fields = publicTexts({ doc: box.doc, translations, timeline: readJson(path.join(box.workdir, "timeline.json"), null) });
  const receipts = { schema_version: 1, locales: Object.fromEntries(Object.entries(fields).map(([locale, text]) => [locale, { passed: true, input_sha256: reviewHash(context, locale, text) }])) };
  writeFileSync(path.join(box.dir, COMPILATION_REVIEW_FILE), JSON.stringify(receipts));
  assert.equal((await packageRun()).code, EXIT.ok);
  const accepted = readFileSync(metadataFile, "utf8");
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify({ ...translations.en, title: "She is alive" }));
  const stale = await packageRun();
  assert.equal(stale.code, EXIT.owner);
  assert.match(stale.out.stderr, /current spoiler review for en/);
  assert.equal(readFileSync(metadataFile, "utf8"), accepted);
  writeLanguages(box.workdir, { locales: { ja: { metadata: true } } });
  assert.equal((await packageRun()).code, EXIT.ok, "an unselected locale does not block the published set");
});
