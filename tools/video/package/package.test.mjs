import assert from "node:assert/strict";
import test from "node:test";

import { existsSync, readFileSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { compilationDocument, compilationLayout, compilationTimeline } from "../core/compilation.mjs";
import { fixture } from "../core/fixtures/load.mjs";
import { DESCRIPTION_MAX_BYTES } from "../core/metadata.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { audioReviewHtml, finalReviewHtml } from "../review/pages.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, writeTranslations } from "../compile/fixture.mjs";
import { compilationSection, composeMetadata, uploadChecklist } from "./metadata.mjs";
import { linkOrCopy, skippedCaptionLocales } from "./cli.mjs";

const doc = fixture();
const timeline = { ...estimateTimeline(doc), speech_hash: "abc123" };

test("zh-TW metadata carries the composed description with chapters and sources", () => {
  const { problems, metadata } = composeMetadata({ doc, timeline });
  assert.deepEqual(problems, []);
  assert.equal(metadata.default_language, "zh-TW");
  assert.equal(metadata.privacy_status, "private");
  assert.match(metadata.description, /章節\n00:00 開場\n/);
  assert.match(metadata.description, /參考資料\n範例來源：https:\/\/example\.com\/models/);
  assert.deepEqual(metadata.localizations, {});
  assert.deepEqual(metadata.chapters.map((chapter) => chapter.title), ["開場", "三個問題", "結論"]);
});

test("translated locales get their own title, description, chapter titles and article link", () => {
  const translations = {
    en: { title: "How to pick an AI model", description: "Three questions.", tags: ["AI models", "AI 模型"], chapters: { hook: "Intro" } },
    ja: { title: "", description: "incomplete" },
  };
  const pack = { slug: "ai-workflow-cost-quality-latency", kind: "life", locales: { "zh-TW": {}, en: {} } };
  const { metadata } = composeMetadata({ doc: { ...doc, source_guide: pack.slug }, timeline, translations, pack });
  assert.deepEqual(Object.keys(metadata.localizations), ["en"]);
  assert.match(metadata.localizations.en.description, /Chapters\n00:00 Intro\n/);
  assert.match(metadata.localizations.en.description, /https:\/\/mokaair\.com\/en\/life\/ai-workflow-cost-quality-latency\?utm_source=youtube/);
  assert.match(metadata.description, /https:\/\/mokaair\.com\/zh-TW\/life\//);
  assert.deepEqual(metadata.tags, ["AI 模型", "模型選擇", "AI models"]);
});

test("a description over YouTube's byte limit is a problem, named by locale", () => {
  const long = { ...doc, youtube: { ...doc.youtube, description: "字".repeat(1700) } };
  const { problems } = composeMetadata({ doc: long, timeline });
  assert.match(problems.join("\n"), /zh-TW\.description: \d+ bytes/);
});

test("UPLOAD.md keeps only the Studio steps: private first, the disclosure as metadata.json says, no self-check list", () => {
  const { metadata } = composeMetadata({ doc, timeline });
  const slides = uploadChecklist({ metadata, captions: ["captions/zh-TW.srt"], thumbnail: true, disclosure: { synthetic: false, reason: "slides read by a stock TTS voice" } });
  assert.match(slides, /瀏覽權限先選「私人」/);
  assert.match(slides, /captions\/zh-TW\.srt/);
  assert.match(slides, /「變造或合成內容」：不用勾。`metadata\.json` 的 `contains_synthetic_media` 是 `false`（slides read by a stock TTS voice）/);
  assert.match(slides, /貼上 YouTube 網址/);
  assert.doesNotMatch(slides, /- \[ \]/, "the self-check list moved into the automatic checks");
  assert.doesNotMatch(slides, /非原創內容政策|AI 使用揭露|youtube-sync/);
  const drama = uploadChecklist({ metadata: { ...metadata, contains_synthetic_media: true, disclosure_reason: "AI-generated shots and voices" }, captions: [], thumbnail: false, drama: true });
  assert.match(drama, /「變造或合成內容」：勾「是」。`metadata\.json` 的 `contains_synthetic_media` 是 `true`（AI-generated shots and voices）/);
  assert.match(drama, /還沒有字幕檔/);
});

test("the audio review page lists every line with its clip and exports flags with the timeline version", () => {
  const html = audioReviewHtml(doc, timeline);
  for (const line of doc.scenes.flatMap((scene) => scene.lines)) assert.ok(html.includes(`src="../audio/${line.id}.wav"`), line.id);
  assert.match(html, /唸成：完整的比較表，放在說明欄的文章裡/);
  assert.match(html, /"speech_hash":"abc123"/);
  assert.match(html, /download="flags\.json"|link\.download="flags\.json"/);
});

test("review pages escape the script's text", () => {
  const hostile = structuredClone(doc);
  hostile.youtube.title = "<script>alert(1)</script>";
  hostile.scenes[0].lines[0].text = "</script><img src=x onerror=alert(1)>";
  for (const html of [audioReviewHtml(hostile, timeline), finalReviewHtml(hostile, timeline, { problems: [] })]) {
    assert.doesNotMatch(html, /<script>alert/);
    assert.doesNotMatch(html, /<img src=x/);
  }
});

test("the final review page plays final.mp4 and seeks from chapters and lines", () => {
  const html = finalReviewHtml(doc, timeline, { problems: [], metrics: { loudness: { integrated: -14 } } });
  assert.match(html, /<video id="video" controls preload="metadata" src="\.\.\/final\.mp4">/);
  assert.equal((html.match(/class="cue"/g) ?? []).length, 3 + 7);
  assert.match(html, /自動檢查全部通過/);
  assert.match(finalReviewHtml(doc, timeline, { problems: ["loudness off"] }), /自動檢查有問題：loudness off/);
});

test("a compilation's metadata keys its chapters on episode slugs and falls back to 「第 N 集」 when eighty titles would not fit", () => {
  const episodes = Array.from({ length: 80 }, (_, index) => ({ slug: `wuxia-ep-${index + 1}`, number: index + 1, title: "山海經最倔強的一隻鳥到底為什麼要填海呢這是第一部的長標題" }));
  const long = compilationDocument({ series: "wuxia", episodes, voice: doc.voice });
  long.youtube.title = "仙門風雲 全集";
  long.youtube.description = "第一部的每一集。";
  const compiled = compilationTimeline(compilationLayout(long, long.compilation.episodes.map((slug) => ({ slug, frames: 7200 }))), long.compilation.titles);
  const translations = { en: { title: "Part one", description: "All of part one.", tags: ["wuxia"], chapters: Object.fromEntries(episodes.map((episode) => [episode.slug, `Episode ${episode.number}: a long English title that goes on and on and on`])) } };
  const { problems, metadata } = composeMetadata({ doc: long, timeline: compiled, translations });
  assert.deepEqual(problems, []);
  assert.ok(Buffer.byteLength(metadata.description, "utf8") <= DESCRIPTION_MAX_BYTES);
  assert.match(metadata.description, /\n00:00 第 1 集\n04:02 第 2 集\n/);
  assert.match(metadata.localizations.en.description, /Chapters\n00:00 Episode 1\n/);
  assert.deepEqual(metadata.chapters.slice(0, 2), [{ at: "00:00", title: "第 1 集" }, { at: "04:02", title: "第 2 集" }]);
  assert.equal(metadata.chapters.length, 80);
  // Three episodes fit: the titles stay, in zh-TW and in the translation keyed by slug.
  const short = compilationDocument({ series: "wuxia", episodes: episodes.slice(0, 3), voice: doc.voice });
  short.youtube.title = "仙門風雲 全集";
  const three = compilationTimeline(compilationLayout(short, short.compilation.episodes.map((slug) => ({ slug, frames: 7200 }))), short.compilation.titles);
  const fits = composeMetadata({ doc: short, timeline: three, translations: { en: { ...translations.en, chapters: { "wuxia-ep-2": "Episode 2: The Library" } } } });
  assert.match(fits.metadata.description, /00:00 第 1 集 山海經/);
  assert.match(fits.metadata.localizations.en.description, /04:02 Episode 2: The Library\n08:04 第 3 集 山海經/);
  assert.equal(fits.metadata.chapters[0].title, "第 1 集 山海經最倔強的一隻鳥到底為什麼要填海呢這是第一部的長標題");
});

test("UPLOAD.md of a compilation says the file is downloaded from the site and the chapters are in the description", () => {
  const { metadata } = composeMetadata({ doc, timeline });
  const text = uploadChecklist({ metadata: { ...metadata, download: "upload/final.mp4" }, captions: ["captions/zh-TW.srt"], thumbnail: true, drama: true, disclosure: { synthetic: true, reason: "a drama" }, compilation: { episodes: 40, size_bytes: 2.5 * 1024 ** 3 } });
  assert.match(text, /## 合集\n\n- 這支是 40 集的合集：每集一章，章節時間戳已經在說明欄裡（`metadata\.json` 的 `chapters` 有 3 章）/);
  assert.match(text, /約 2\.50 GB，不走審核檔案區：到 \/admin\/videos 這支的「可以上架」卡片下載（`upload\/final\.mp4`），再照第 1 節在 Studio 上傳，瀏覽權限一樣先選「私人」/);
  assert.match(text, /## 1\. 上傳/);
  assert.doesNotMatch(uploadChecklist({ metadata, captions: [], thumbnail: false }), /## 合集/);
  assert.match(compilationSection({ chapters: [] }, {}), /0 集的合集/);
  assert.deepEqual(skippedCaptionLocales({ skipped: { ja: ["ep-2"] } }, ["captions/zh-TW.srt"], { compilation: true }), { en: "no caption file merged", ja: "no caption file in episodes ep-2", ko: "no caption file merged", "zh-CN": "no caption file merged" });
});

test("package links a compilation's final.mp4, records the download, the size and the episodes, and passes its check", async () => {
  const box = compilationSandbox();
  writeTranslations(box, box.doc);
  const total = EPISODES.reduce((sum, slug) => sum + EPISODE_FRAMES[slug], 0) + EPISODES.length * 60 + 120;
  const compiled = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["compile", "--slug", box.slug], compiled.ctx), EXIT.ok, compiled.out.stderr);
  const before = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["package", "--slug", box.slug], before.ctx), EXIT.owner, "the cut is not approved yet");
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir, now: new Date("2026-09-27T06:00:00Z") });
  const { out, ctx } = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["package", "--slug", box.slug], ctx), EXIT.ok, out.stderr + out.stdout);
  const upload = path.join(box.workdir, "upload");
  const final = path.join(upload, "final.mp4");
  assert.equal(statSync(final).ino, statSync(path.join(box.workdir, "final.mp4")).ino, "a hard link, not a copy");
  const metadata = JSON.parse(readFileSync(path.join(upload, "metadata.json"), "utf8"));
  assert.equal(metadata.compilation, true);
  assert.equal(metadata.download, "upload/final.mp4");
  assert.equal(metadata.size_bytes, statSync(final).size);
  assert.deepEqual(metadata.episodes.map((episode) => [episode.slug, episode.start_frame]), [["wuxia-ep-1", 60], ["wuxia-ep-2", 4441], ["wuxia-ep-3", 8401]]);
  assert.equal(metadata.episodes[0].sha256, box.episodes["wuxia-ep-1"].sha256);
  assert.deepEqual(metadata.captions, ["captions/en.srt", "captions/zh-TW.srt"]);
  assert.deepEqual(metadata.skipped_caption_locales, { ja: "no caption file in episodes wuxia-ep-1, wuxia-ep-2, wuxia-ep-3", ko: "no caption file in episodes wuxia-ep-1, wuxia-ep-2, wuxia-ep-3", "zh-CN": "no caption file in episodes wuxia-ep-1, wuxia-ep-2, wuxia-ep-3" });
  assert.equal(metadata.contains_synthetic_media, true);
  assert.deepEqual(Object.keys(metadata).slice(-2), ["contains_synthetic_media", "disclosure_reason"], "the disclosure stays last, so qa's rewrite leaves the bytes alone");
  assert.deepEqual(metadata.chapters.map((chapter) => chapter.title), ["第 1 集 初入山門", "第 2 集 夜探藏經閣", "第 3 集 劍冢之約"]);
  assert.match(metadata.localizations.en.description, /00:00 en wuxia-ep-1\n/, "translated chapters are read by episode slug");
  const md = readFileSync(path.join(upload, "UPLOAD.md"), "utf8");
  assert.match(md, /## 合集\n\n- 這支是 3 集的合集/);
  assert.ok(existsSync(path.join(upload, "description.ko.txt")));
  assert.match(out.stdout, /final\.mp4 \(linked, 0\.00 GB, 3 episodes\)/);
  assert.match(out.stdout, /package check: 4 of 4 passed/);
  // Without compile's captions for these cuts, package refuses rather than cutting captions itself.
  const manifest = path.join(box.workdir, "captions", "manifest.json");
  const saved = readFileSync(manifest, "utf8");
  writeFileSync(manifest, JSON.stringify({ compilation_hash: "stale", locales: {}, skipped: {} }));
  const stale = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["package", "--slug", box.slug], stale.ctx), EXIT.usage);
  assert.match(stale.out.stderr, /merged for other cuts; run compile again/);
  writeFileSync(manifest, saved);
  assert.equal(linkOrCopy(path.join(box.workdir, "final.mp4"), path.join(box.workdir, "copy.mp4")), "linked");
});
