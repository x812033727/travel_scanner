import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "./fixtures/load.mjs";
import { articleUrl, checkYoutubeFields, composeDescription, tagsLength } from "./metadata.mjs";
import { estimateTimeline } from "./timeline.mjs";

test("tag length is counted YouTube's way: commas between tags, quotes around tags with spaces", () => {
  assert.equal(tagsLength(["a b", "cd"]), 3 + 2 + 2 + 1);
  assert.equal(tagsLength([]), 0);
});

test("the description limit is in bytes, so 1,700 Chinese characters are already too many", () => {
  const ok = { title: "標題", description: "字".repeat(1666), tags: [] };
  assert.deepEqual(checkYoutubeFields(ok), []);
  const problems = checkYoutubeFields({ title: "x".repeat(101), description: `${"字".repeat(1700)}<b>`, tags: ["t".repeat(501)] });
  assert.equal(problems.length, 4);
  assert.match(problems.join("\n"), /5\d{3} bytes/);
});

test("article links follow the site's URL shapes and carry the video campaign", () => {
  assert.equal(
    articleUrl({ slug: "ai-workflow-cost-quality-latency", kind: "life" }, "zh-TW", "ai-model-choice"),
    "https://mokaair.com/zh-TW/life/ai-workflow-cost-quality-latency?utm_source=youtube&utm_medium=video&utm_campaign=ai-model-choice",
  );
  assert.equal(articleUrl({ slug: "tokyo-subway", kind: "howto" }, "en", "x"), "https://mokaair.com/en/guides/howto/tokyo-subway?utm_source=youtube&utm_medium=video&utm_campaign=x");
  assert.equal(articleUrl(null, "zh-TW", "x"), null);
});

test("the composed description has body, chapters, article and sources, labelled per locale", () => {
  const doc = fixture();
  const zh = composeDescription({ body: doc.youtube.description, timeline: estimateTimeline(doc), article: "https://mokaair.com/zh-TW/life/x", sources: doc.sources, locale: "zh-TW" });
  assert.match(zh, /^排行榜第一名/);
  assert.match(zh, /\n\n章節\n00:00 開場\n00:\d\d 三個問題\n/);
  assert.match(zh, /\n\n完整文章\nhttps:\/\/mokaair\.com\/zh-TW\/life\/x\n\n參考資料\n範例來源：https:\/\/example\.com\/models$/);
  const en = composeDescription({ body: "Body", timeline: estimateTimeline(doc), chapterTitles: { hook: "Intro" }, sources: doc.sources, locale: "en" });
  assert.match(en, /Chapters\n00:00 Intro\n/);
  assert.match(en, /Sources\n範例來源: https/);
});
