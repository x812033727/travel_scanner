import assert from "node:assert/strict";
import { readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { compilationDocument, compilationLayout, compilationTimeline } from "../core/compilation.mjs";
import { COMPILATION_REVIEW_FILE, publicTexts, reviewHash } from "../core/compilation-review.mjs";
import { fixture } from "../core/fixtures/load.mjs";
import { creditBytes, DESCRIPTION_MAX_BYTES, SERIES_HASHTAGS } from "../core/metadata.mjs";
import { readJson } from "../core/paths.mjs";
import { writeLanguages } from "../core/stages.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, writeTranslations } from "../compile/fixture.mjs";
import { composeMetadata } from "./metadata.mjs";

test("every locale's description credits the stock photos of assets[], and says so when they tip it over the byte limit", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  doc.assets = [
    { path: "apps/web/public/guides/x/diagram-1.svg", source: "Mokaair 自有圖解（文章 x）", license: "© Mokaair" },
    { path: "stock/a.jpg", source: "Photo by Lukas Rodriguez on Pexels", license: "Pexels License", author: "Lukas Rodriguez", url: "https://www.pexels.com/photo/seoul-at-night-3573351/" },
  ];
  const translations = { en: { title: "How to pick an AI model", description: "Three questions decide it." } };
  const { problems, metadata } = composeMetadata({ doc, timeline, translations });
  assert.deepEqual(problems, []);
  assert.match(metadata.description, /\n\n📚 參考資料\n[^\n]+\n\n📷 圖片來源\nPhoto by Lukas Rodriguez on Pexels（Pexels License）：https:\/\/www\.pexels\.com\/photo\/seoul-at-night-3573351\/\n\n#/);
  assert.doesNotMatch(metadata.description, /Mokaair 自有圖解/, "own diagrams are not credited");
  assert.match(metadata.localizations.en.description, /\n\n📷 Image credits\nPhoto by Lukas Rodriguez on Pexels \(Pexels License\): https:\/\/www\.pexels\.com/);
  // A body that fits without the credits (lint composes it that way) and not with them.
  const credits = creditBytes(doc.assets, "zh-TW");
  const slack = () => DESCRIPTION_MAX_BYTES - Buffer.byteLength(composeMetadata({ doc: { ...doc, assets: [] }, timeline }).metadata.description, "utf8");
  doc.youtube.description += "字".repeat(Math.ceil((slack() - credits + 1) / 3));
  assert.ok(slack() >= 0 && slack() < credits, `${slack()} bytes of room under lint's count, ${credits} needed`);
  assert.deepEqual(composeMetadata({ doc: { ...doc, assets: [] }, timeline }).problems, []);
  const over = composeMetadata({ doc, timeline }).problems;
  assert.equal(over.length, 1);
  assert.match(over[0], new RegExp(`^zh-TW\\.description: \\d+ bytes once composed, at most ${DESCRIPTION_MAX_BYTES} \\(the 圖片來源 credits of assets\\[\\] add ${credits} bytes that lint does not count: shorten youtube\\.description or use fewer stock photos\\)$`));
});

test("every locale's description opens on the hook, links the article once with the video's campaign after the body, and ends on the series hashtag", () => {
  const doc = fixture();
  doc.category = "ai-terms";
  doc.youtube.description = "https://mokaair.com/zh-TW/life/ai-terms-index\nToken 是什麼？這集回答 AI 在數什麼。\n給看過帳單卻搞不懂 token 的人。\n\n索引在 https://mokaair.com/zh-TW/life/ai-terms-index 。\n\n完整文章：https://mokaair.com/zh-TW/life/what-is-a-token";
  doc.youtube.tags = ["token", "詞元", "AI 名詞十分鐘", "分詞"];
  const timeline = estimateTimeline(doc);
  const pack = { slug: "what-is-a-token", kind: "life", locales: { "zh-TW": {}, en: {} } };
  const translations = { en: { title: "What is a token?", description: "What is a token? AI counts its own units.\nFor anyone who read a bill. See https://mokaair.com/en/life/ai-terms-index.", tags: ["token", "tokenizer"] } };
  const { problems, metadata } = composeMetadata({ doc, timeline, translations, pack });
  assert.deepEqual(problems, []);
  const zh = metadata.description;
  const article = `https://mokaair.com/zh-TW/life/what-is-a-token?utm_source=youtube&utm_medium=video&utm_campaign=${doc.slug}`;
  assert.match(zh, /^Token 是什麼？\n給看過帳單卻搞不懂 token 的人。\n\n這集回答 AI 在數什麼。\n\n索引在 https:\/\/mokaair\.com\/zh-TW\/life\/ai-terms-index\?utm_source=youtube&utm_medium=video&utm_campaign=fixture-minimal 。\n\n🔗 完整文章：/, "the first line is the hook, not a URL; the body's own link carries the slug as campaign");
  assert.equal(zh.split(article).length - 1, 1, "the article once, after the body");
  assert.equal((zh.match(/ai-terms-index/g) ?? []).length, 1, "the index page once: its bare first line is dropped, the sentence stays");
  assert.match(zh, new RegExp(`\\n\\n#token #詞元 ${SERIES_HASHTAGS["ai-terms"]}$`), "two topic hashtags and the category's series hashtag");
  const en = metadata.localizations.en.description;
  assert.match(en, /^What is a token\?\nFor anyone who read a bill\. See https:\/\/mokaair\.com\/en\/life\/ai-terms-index\?utm_source=youtube&utm_medium=video&utm_campaign=fixture-minimal\.\n\nAI counts its own units\.\n\n🔗 Full article: https:\/\/mokaair\.com\/en\/life\/what-is-a-token\?utm_source=youtube/, "the same order in every locale, with the locale's labels");
  assert.match(en, new RegExp(`#token #tokenizer ${SERIES_HASHTAGS["ai-terms"]}$`), "the series hashtag is the same in every locale");
  assert.deepEqual(metadata.tags, ["token", "詞元", "AI 名詞十分鐘", "分詞"], "the narration's tags only");
  const plain = composeMetadata({ doc: { ...doc, category: "explainer" }, timeline }).metadata.description;
  assert.match(plain, /\n\n#token #詞元$/, "a category without a series row: two hashtags");
});

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
