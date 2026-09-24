import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "../core/fixtures/load.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { audioReviewHtml, finalReviewHtml } from "../review/pages.mjs";
import { composeMetadata, uploadChecklist } from "./metadata.mjs";

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

test("the checklist starts private and leaves the disclosure decisions to the owner", () => {
  const { metadata } = composeMetadata({ doc, timeline });
  const text = uploadChecklist({ metadata, captions: ["captions/zh-TW.srt"], thumbnail: true });
  assert.match(text, /瀏覽權限先選「私人」/);
  assert.match(text, /captions\/zh-TW\.srt/);
  assert.match(text, /AI 使用揭露/);
  assert.match(text, /非原創內容政策/);
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
