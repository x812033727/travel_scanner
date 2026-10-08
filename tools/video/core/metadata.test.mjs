import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "./fixtures/load.mjs";
import { articlePath, articleUrl, ASSET_FIELDS, bodyLayout, checkYoutubeFields, composeDescription, creditBytes, creditedAssets, creditLine, dedupeLinks, descriptionHashtags, hashtagsFrom, pictureCredits, seriesHashtag, SERIES_HASHTAGS, splitFirstSentence, tagMokaairLinks, tagsLength, TAGS_MAX_COUNT, TITLE_BANNED, TITLE_WARN_WIDTH, titleWidth, unlinkedSources, uploadTags, urlKey, withUtm, youtubeWarnings } from "./metadata.mjs";
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

test("the composed description opens on the hook and the audience, links the article after the body, and closes on the hashtags", () => {
  const doc = fixture();
  const zh = composeDescription({ body: doc.youtube.description, timeline: estimateTimeline(doc), article: "https://mokaair.com/zh-TW/life/x?utm_source=youtube&utm_medium=video&utm_campaign=fixture-minimal", sources: doc.sources, locale: "zh-TW", tags: ["AI 模型", "LLM", "ChatGPT Go", "LLM"] });
  assert.match(zh, /^排行榜第一名不一定最適合你。\n這支用三個問題，幫你挑出適合自己的 AI 模型。\n\n🔗 完整文章：https:\/\/mokaair\.com\/zh-TW\/life\/x\?utm_source=youtube&utm_medium=video&utm_campaign=fixture-minimal\n\n📌 章節\n00:00 開場\n00:\d\d 三個問題\n/, "the hook is the first line, the link comes after the body");
  assert.match(zh, /\n\n📚 參考資料\n範例來源：https:\/\/example\.com\/models\n\n#AI模型 #LLM$/, "two topic hashtags, no series row for a video without a category");
  const series = composeDescription({ body: "Token 是什麼？", locale: "zh-TW", tags: ["token", "AI 名詞十分鐘", "詞元", "分詞"], category: "ai-terms" });
  assert.equal(series, "Token 是什麼？\n\n#token #詞元 #AI名詞十分鐘", "the series hashtag is the third, and a tag that spells it takes no topic slot");
  const en = composeDescription({ body: "Body", timeline: estimateTimeline(doc), chapterTitles: { hook: "Intro" }, sources: doc.sources, locale: "en" });
  assert.match(en, /^Body\n\n📌 Chapters\n00:00 Intro\n/, "no article, no link line");
  assert.match(en, /📚 Sources\n範例來源: https[^\n]*$/, "no tags, no hashtag line");
});

test("the body is laid out as hook, audience, then the rest as the writer paragraphed it", () => {
  assert.deepEqual(splitFirstSentence("Token 是什麼？這集回答 AI 在數什麼。"), ["Token 是什麼？", "這集回答 AI 在數什麼。"]);
  assert.deepEqual(splitFirstSentence("First 2.5% of Omni 1.1 is fine. Then more."), ["First 2.5% of Omni 1.1 is fine.", "Then more."], "a Latin period ends a sentence only before a space");
  assert.deepEqual(splitFirstSentence("「真的嗎？」她問。"), ["「真的嗎？」", "她問。"], "the closing quote stays with its sentence");
  assert.deepEqual(splitFirstSentence("沒有句點"), ["沒有句點", ""]);
  const token = "Token 是什麼？這集回答 AI 在數什麼，以及什麼時候該在意。\n給常把公告貼給 AI 整理的人；不用懂程式。\n\n用一份公告實際算一次。\n\n錄製日期：2026 年 10 月 3 日。";
  assert.deepEqual(bodyLayout(token), { hook: "Token 是什麼？", audience: "給常把公告貼給 AI 整理的人；不用懂程式。", rest: "這集回答 AI 在數什麼，以及什麼時候該在意。\n\n用一份公告實際算一次。\n\n錄製日期：2026 年 10 月 3 日。" });
  assert.deepEqual(bodyLayout("OpenAI 發表了 25 項。這支分五張清單。\n\n給付 Plus 的人。\n\n講到錢。"), { hook: "OpenAI 發表了 25 項。", audience: "給付 Plus 的人。", rest: "這支分五張清單。\n\n講到錢。" }, "a second paragraph is the audience line too");
  assert.deepEqual(bodyLayout("一句鉤子。給誰看。"), { hook: "一句鉤子。", audience: "給誰看。", rest: "" }, "one paragraph: the rest of it is line 2");
  assert.deepEqual(bodyLayout("  \n只有一句\n"), { hook: "只有一句", audience: "", rest: "" });
  assert.deepEqual(bodyLayout(""), { hook: "", audience: "", rest: "" });
  assert.equal(composeDescription({ body: "一句鉤子。還有一句。\n給誰看。\n\n其餘。", locale: "zh-TW" }), "一句鉤子。\n給誰看。\n\n還有一句。\n\n其餘。");
});

test("every Mokaair link carries the video's UTM once, and the same page is linked once", () => {
  assert.equal(withUtm("https://mokaair.com/zh-TW/life/x", "slug-a"), "https://mokaair.com/zh-TW/life/x?utm_source=youtube&utm_medium=video&utm_campaign=slug-a");
  assert.equal(withUtm("https://www.mokaair.com/en/guides/howto/y?ref=1#top", "s"), "https://www.mokaair.com/en/guides/howto/y?ref=1&utm_source=youtube&utm_medium=video&utm_campaign=s#top");
  assert.equal(withUtm("https://mokaair.com/zh-TW/life/x?utm_source=newsletter", "s"), "https://mokaair.com/zh-TW/life/x?utm_source=newsletter", "a tagged link keeps its tags");
  assert.equal(withUtm("https://mokaair.com/zh-TW/life/x", null), "https://mokaair.com/zh-TW/life/x?utm_source=youtube&utm_medium=video", "no campaign known");
  assert.equal(withUtm("https://openai.com/blog", "s"), "https://openai.com/blog");
  assert.equal(withUtm("not a url", "s"), "not a url");
  assert.equal(tagMokaairLinks("見 https://mokaair.com/zh-TW/life/x。再看 https://mokaair.com/zh-TW/life/y, 以及 https://openai.com/a.", "c"), "見 https://mokaair.com/zh-TW/life/x?utm_source=youtube&utm_medium=video&utm_campaign=c。再看 https://mokaair.com/zh-TW/life/y?utm_source=youtube&utm_medium=video&utm_campaign=c, 以及 https://openai.com/a.", "the sentence's punctuation stays outside the URL");
  assert.equal(urlKey("https://Mokaair.com/zh-TW/life/x/?utm_source=youtube#a"), "https://mokaair.com/zh-TW/life/x");
  assert.equal(urlKey("https://mokaair.com/en/y?ref=1&utm_source=a&utm_medium=b&utm_campaign=c#top"), "https://mokaair.com/en/y?ref=1", "only the UTM parameters are dropped");
  assert.notEqual(urlKey("https://www.ntm.gov.tw/cp.aspx?n=5444"), urlKey("https://www.ntm.gov.tw/cp.aspx?n=5445"), "two pages that differ only by their query are two pages");
  assert.equal(urlKey("https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444"), "https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444");
  assert.equal(urlKey("nope"), "nope");
  assert.equal(urlKey("nope/?utm_source=x&a=1#f"), "nope?a=1");
  const article = "https://mokaair.com/zh-TW/life/x?utm_source=youtube&utm_medium=video&utm_campaign=c";
  const body = "https://mokaair.com/zh-TW/life/x?utm_source=youtube\n鉤子。\n給誰看。\n\n完整文章：https://mokaair.com/zh-TW/life/x\n索引：https://mokaair.com/zh-TW/life/ai-terms-index\n🔗 https://mokaair.com/zh-TW/life/ai-terms-index/\n結尾。";
  assert.deepEqual(dedupeLinks(body, article), { body: "鉤子。\n給誰看。\n\n索引：https://mokaair.com/zh-TW/life/ai-terms-index\n結尾。", mentioned: false }, "link-only lines of the article and of a page already linked are dropped");
  assert.deepEqual(dedupeLinks("算式在 https://mokaair.com/zh-TW/life/x 裡。", article), { body: "算式在 https://mokaair.com/zh-TW/life/x 裡。", mentioned: true }, "a mention inside a sentence stays");
  assert.deepEqual(dedupeLinks("https://mokaair.com/zh-TW/life/index\n鉤子。索引在 https://mokaair.com/zh-TW/life/index 。"), { body: "鉤子。索引在 https://mokaair.com/zh-TW/life/index 。", mentioned: false }, "a bare first line is dropped when a sentence below links the same page");
  assert.deepEqual(dedupeLinks("https://mokaair.com/zh-TW/life/only\n鉤子。"), { body: "https://mokaair.com/zh-TW/life/only\n鉤子。", mentioned: false }, "a bare link to a page linked nowhere else stays");
  assert.deepEqual(dedupeLinks("https://mokaair.com/zh-TW/life/twice\n鉤子。\nhttps://mokaair.com/zh-TW/life/twice"), { body: "https://mokaair.com/zh-TW/life/twice\n鉤子。", mentioned: false }, "two bare lines: the first is kept");
  const pages = "https://www.ntm.gov.tw/cp.aspx?n=5444\n鉤子。\n給誰看。\nhttps://www.ntm.gov.tw/cp.aspx?n=5445";
  assert.deepEqual(dedupeLinks(pages), { body: pages, mentioned: false }, "two bare lines to pages that differ only by their query both stay");
  const composed = composeDescription({ body, article, sources: [{ title: "站內", url: "https://mokaair.com/zh-TW/life/z" }], locale: "zh-TW", tags: [] });
  assert.equal(composed, `鉤子。\n給誰看。\n\n索引：https://mokaair.com/zh-TW/life/ai-terms-index?utm_source=youtube&utm_medium=video&utm_campaign=c\n結尾。\n\n🔗 完整文章：${article}\n\n📚 參考資料\n站內：https://mokaair.com/zh-TW/life/z?utm_source=youtube&utm_medium=video&utm_campaign=c`, "the campaign comes from the article link when none is given");
  const mentioned = composeDescription({ body: "鉤子。算式在 https://mokaair.com/zh-TW/life/x 裡。", article, locale: "zh-TW", campaign: "other" });
  assert.equal(mentioned, "鉤子。\n算式在 https://mokaair.com/zh-TW/life/x?utm_source=youtube&utm_medium=video&utm_campaign=other 裡。", "the article mentioned in a sentence is its one appearance: no link line");
  assert.equal((composed.match(/mokaair\.com\/zh-TW\/life\/x/g) ?? []).length, 1);
});

test("a source that is the article, or a page the body links, is not listed again under 📚", () => {
  const article = "https://mokaair.com/zh-TW/life/ai-term-embedding?utm_source=youtube&utm_medium=video&utm_campaign=ai-term-embedding";
  const sources = [
    { title: "Google Embeddings", url: "https://developers.google.com/machine-learning/crash-course/embeddings" },
    { title: "Mokaair 嵌入向量", url: "https://mokaair.com/zh-TW/life/ai-term-embedding" },
    { title: "Mokaair 嵌入向量（再一次）", url: "https://mokaair.com/zh-TW/life/ai-term-embedding/?utm_source=newsletter" },
  ];
  const composed = composeDescription({ body: "鉤子。\n給誰看。", article, sources, locale: "zh-TW" });
  assert.equal(composed, `鉤子。\n給誰看。\n\n🔗 完整文章：${article}\n\n📚 參考資料\nGoogle Embeddings：https://developers.google.com/machine-learning/crash-course/embeddings`, "the article is the 🔗 line and nothing else; a page is listed once");
  assert.equal((composed.match(/ai-term-embedding/g) ?? []).length, 2, "the slug appears in the article URL and its campaign only");
  const mentioned = composeDescription({ body: "鉤子。算式在 https://mokaair.com/zh-TW/life/ai-term-embedding 裡。", article, sources, locale: "zh-TW" });
  assert.equal((mentioned.match(/mokaair\.com\/zh-TW\/life\/ai-term-embedding/g) ?? []).length, 1, "mentioned in a sentence: not listed under 📚 either");
  const inBody = composeDescription({ body: "鉤子。\n給誰看。\n讀 https://developers.google.com/machine-learning/crash-course/embeddings。", sources: sources.slice(0, 1), locale: "zh-TW" });
  assert.equal(inBody, "鉤子。\n給誰看。\n\n讀 https://developers.google.com/machine-learning/crash-course/embeddings。", "every source linked above: no 📚 section at all");
  const pages = [{ title: "票價", url: "https://www.ntm.gov.tw/cp.aspx?n=5444" }, { title: "交通", url: "https://www.ntm.gov.tw/cp.aspx?n=5445" }];
  assert.deepEqual(unlinkedSources(pages), pages, "pages that differ by their query are both listed");
  assert.deepEqual(unlinkedSources(pages, new Set([urlKey("https://www.ntm.gov.tw/cp.aspx?n=5445&utm_source=youtube")])), [pages[0]]);
  assert.deepEqual(unlinkedSources(), []);
});

test("the title rules are warnings: width, one question, the banned shapes, lists, episode numbers, and the tag count", () => {
  assert.equal(titleWidth("Token 是什麼？AI 算的不是字數，是它自己的單位｜AI 名詞十分鐘"), 30, "CJK and full-width punctuation 1, Latin letters and spaces 0.5");
  assert.equal(titleWidth(""), 0);
  assert.deepEqual(youtubeWarnings({ title: "Token 是什麼？AI 算的不是字數，是它自己的單位｜AI 名詞十分鐘", tags: ["a"] }), [], "the series suffix is allowed");
  const long = "掛防火牆就不用更新外掛？Cloudflare 說 AI 打穿 WAF 的數字是誰測的、怎麼讀、怎麼看";
  const warnings = youtubeWarnings({ title: long, tags: Array.from({ length: TAGS_MAX_COUNT + 1 }, (_, n) => `t${n}`) }, "i18n/zh-TW");
  assert.equal(warnings.length, 4, warnings.join("\n"));
  assert.match(warnings[0], new RegExp(`^i18n/zh-TW\\.title: ${titleWidth(long)} full-width characters wide .* at most ${TITLE_WARN_WIDTH} `));
  assert.match(warnings[1], /^i18n\/zh-TW\.title: 「是誰測的」「怎麼讀」「怎麼看」 is the media-literacy shape/);
  assert.match(warnings[2], /^i18n\/zh-TW\.title: lists 3 items with 、/);
  assert.match(warnings[3], new RegExp(`^i18n/zh-TW\\.tags: ${TAGS_MAX_COUNT + 1} tags; package keeps the first ${TAGS_MAX_COUNT}`));
  assert.deepEqual(TITLE_BANNED, ["是誰說的", "是誰測的", "怎麼讀", "怎麼看", "先分清", "先問"]);
  assert.match(youtubeWarnings({ title: "A 是什麼？B 呢？" }).join("\n"), /2 question marks; ask at most 1/);
  assert.equal(youtubeWarnings({ title: "Claude、Codex 同題實測" }).length, 0, "two items are not a list");
  for (const numbered of ["RAG 是什麼？第 3 集", "RAG 是什麼？第三集", "RAG EP3", "RAG ep. 12", "RAG #4"]) assert.match(youtubeWarnings({ title: numbered }).join("\n"), /numbers the episode; the series is named as a suffix/, numbered);
  assert.deepEqual(youtubeWarnings({ title: "偶的江湖 第一季 第1集〈幽皇之女〉｜原創武俠動畫" }, "youtube", { numbered: true }), [], "a drama series counts its episodes");
  assert.equal(youtubeWarnings({ title: "Deep 3 研究" }).length, 0, "EP only as a word");
  assert.deepEqual(youtubeWarnings({}), []);
});

test("hashtags: two topic words then the series by category or series slug; the upload keeps ten tags", () => {
  assert.deepEqual(SERIES_HASHTAGS, { "ai-terms": "#AI名詞十分鐘", tutorial: "#AI工具教學", "ai-news": "#AI新聞拆解" });
  assert.equal(seriesHashtag({ category: "ai-news" }), "#AI新聞拆解");
  assert.equal(seriesHashtag({ category: "explainer" }), null);
  assert.equal(seriesHashtag({ category: "ai-terms", series: { slug: "unknown" } }), "#AI名詞十分鐘", "a series without a row falls back to the category");
  assert.equal(seriesHashtag(), null);
  assert.deepEqual(descriptionHashtags({ tags: ["ChatGPT Go", "Plus", "Pro"], category: "tutorial" }), ["#ChatGPTGo", "#Plus", "#AI工具教學"]);
  assert.deepEqual(descriptionHashtags({ tags: ["ChatGPT Go", "Plus", "Pro"] }), ["#ChatGPTGo", "#Plus"], "no series row: no third");
  assert.deepEqual(descriptionHashtags({ tags: ["ai名詞十分鐘", "token"], category: "ai-terms" }), ["#token", "#AI名詞十分鐘"], "the series tag is not repeated in another case");
  assert.deepEqual(descriptionHashtags({}), []);
  assert.deepEqual(uploadTags(["a", "b", "a", "c"]), ["a", "b", "c"]);
  assert.deepEqual(uploadTags(Array.from({ length: 12 }, (_, n) => `tag${n}`)), Array.from({ length: 10 }, (_, n) => `tag${n}`), "video.json's order, cut to ten");
  assert.deepEqual(uploadTags(["x".repeat(400), "y".repeat(200), "z"]), ["x".repeat(400), "z"], "within YouTube's 500 characters");
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
