import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "./fixtures/load.mjs";
import { articlePath, articleUrl, ASSET_FIELDS, checkYoutubeFields, composeDescription, creditBytes, creditedAssets, creditLine, hashtagsFrom, pictureCredits, tagsLength } from "./metadata.mjs";
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
  assert.equal(articlePath({ slug: "ai-news-gpt-6-sol-luna-20260923", kind: "life" }), "/life/ai-news-gpt-6-sol-luna-20260923");
  assert.equal(articlePath({ slug: "tokyo-subway", kind: "howto" }), "/guides/howto/tokyo-subway");
});

test("the composed description opens with the article, then body, chapters, sources and hashtags", () => {
  const doc = fixture();
  const zh = composeDescription({ body: doc.youtube.description, timeline: estimateTimeline(doc), article: "https://mokaair.com/zh-TW/life/x", sources: doc.sources, locale: "zh-TW", tags: ["AI 模型", "LLM", "ChatGPT Go", "LLM"] });
  assert.match(zh, /^🔗 完整文章：https:\/\/mokaair\.com\/zh-TW\/life\/x\n\n排行榜第一名/, "the link is the first line, visible before 'more'");
  assert.match(zh, /\n\n📌 章節\n00:00 開場\n00:\d\d 三個問題\n/);
  assert.match(zh, /\n\n📚 參考資料\n範例來源：https:\/\/example\.com\/models\n\n#AI模型 #LLM #ChatGPTGo$/);
  const en = composeDescription({ body: "Body", timeline: estimateTimeline(doc), chapterTitles: { hook: "Intro" }, sources: doc.sources, locale: "en" });
  assert.match(en, /^Body\n\n📌 Chapters\n00:00 Intro\n/, "no article, no link line");
  assert.match(en, /📚 Sources\n範例來源: https[^\n]*$/, "no tags, no hashtag line");
});

test("the description credits the stock photos after the sources, in the vendors' wording, and leaves own diagrams out", () => {
  const pexels = { path: "stock/a.jpg", source: "Photo by Lukas Rodriguez on Pexels", license: "Pexels License", author: "Lukas Rodriguez", url: "https://www.pexels.com/photo/seoul-at-night-3573351/" };
  const pixabay = { path: "stock/b.jpg", source: "Image by Josch13 from Pixabay", license: "Pixabay Content License", author: "Josch13", url: "https://pixabay.com/photos/seoul-korea-195893/" };
  const own = { path: "apps/web/public/guides/x/diagram-1.svg", source: "Mokaair 自有圖解（文章 x）", license: "© Mokaair" };
  const assets = [own, pexels, pixabay, { ...pexels, source: "the same photo listed twice" }];
  assert.deepEqual(ASSET_FIELDS, ["path", "source", "license", "author", "url"]);
  assert.deepEqual(creditedAssets(assets), [pexels, pixabay], "an author or a page is what makes a credit; one line per path");
  assert.deepEqual(creditedAssets(undefined), []);
  assert.deepEqual(creditedAssets([null, "x", { path: "p", author: "A" }]), [], "a credit needs the source line the schema requires");
  const doc = fixture();
  const zh = composeDescription({ body: "正文", timeline: estimateTimeline(doc), sources: doc.sources, assets, locale: "zh-TW", tags: ["AI 模型"] });
  assert.match(
    zh,
    /\n\n📚 參考資料\n範例來源：https:\/\/example\.com\/models\n\n📷 圖片來源\nPhoto by Lukas Rodriguez on Pexels（Pexels License）：https:\/\/www\.pexels\.com\/photo\/seoul-at-night-3573351\/\nImage by Josch13 from Pixabay（Pixabay Content License）：https:\/\/pixabay\.com\/photos\/seoul-korea-195893\/\n\n#AI模型$/,
    "after the sources, before the hashtags",
  );
  assert.match(composeDescription({ body: "Body", assets, locale: "en" }), /^Body\n\n📷 Image credits\nPhoto by Lukas Rodriguez on Pexels \(Pexels License\): https:\/\/www\.pexels\.com[^\n]*\nImage by Josch13 from Pixabay \(Pixabay Content License\): https/);
  assert.match(composeDescription({ body: "Body", assets, locale: "ko" }), /\n\n📷 이미지 출처\nPhoto by Lukas Rodriguez on Pexels \(Pexels License\): https/);
  assert.match(composeDescription({ body: "Body", assets, locale: "ja" }), /\n\n📷 画像の出典\nPhoto by Lukas Rodriguez on Pexels（Pexels License）：https/);
  assert.match(composeDescription({ body: "Body", assets, locale: "zh-CN" }), /\n\n📷 图片来源\n/);
  assert.equal(composeDescription({ body: "Body", assets: [own], locale: "en" }), "Body", "own diagrams: no block, so the descriptions of the videos that list them do not move");
  assert.equal(composeDescription({ body: "Body", locale: "en" }), "Body");
  assert.equal(creditLine({ path: "p", source: " Photo by A on Pexels ", license: " ", author: "A" }, "ko"), "Photo by A on Pexels", "no licence, no page: the credit alone");
  assert.equal(creditLine({ path: "p", source: "Photo by A on Pexels", license: "Pexels License", url: "https://x" }, "ja"), "Photo by A on Pexels（Pexels License）：https://x");
  assert.equal(pictureCredits([own], "zh-TW"), "");
  assert.equal(creditBytes([own], "zh-TW"), 0);
  assert.equal(creditBytes(assets, "zh-TW"), Buffer.byteLength(`\n\n${pictureCredits(assets, "zh-TW")}`, "utf8"), "what the block adds to a description, blank lines included");
  assert.ok(creditBytes(assets, "zh-TW") > 200 && creditBytes(assets, "zh-TW") < 300, `two credits cost ${creditBytes(assets, "zh-TW")} bytes`);
});

test("hashtags drop spaces and punctuation, skip repeats in any case and stop at three", () => {
  assert.deepEqual(hashtagsFrom(["ChatGPT Go", "AI·廣告", "chatgpt-go", "ChatGPTGo", "Plus", "Pro"]), ["#ChatGPTGo", "#AI廣告", "#Plus"]);
  assert.deepEqual(hashtagsFrom(["!!!", ""]), []);
});
