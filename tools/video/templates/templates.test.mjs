import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { assetUrl, BRAND, captureRef, CREDIT_MAX_CHARS, escapeHtml, headlineCount, inlineSvg, isStockPath, richText, sceneProblems, slideHtml, svgProblems, TEMPLATE_SPECS, THUMB_HEADLINE_MAX, THUMB_LAYOUTS, THUMB_TONES, THUMB_VARIANT_IDS, thumbnailHtml, thumbnailProblems, thumbnailRotation, thumbnailVariants, visibility, visibleText, workUrl } from "./templates.mjs";

const showcase = JSON.parse(readFileSync(new URL("./fixtures/showcase/video.json", import.meta.url), "utf8"));
const scene = (id) => structuredClone(showcase.scenes.find((each) => each.id === id));
const state = (overrides = {}) => ({ reveal: 0, previousReveal: 0, first: true, totalReveals: 0, chapter: "章節", chapterNumber: 1, ...overrides });

test("every showcase scene is valid for its template", () => {
  for (const each of showcase.scenes) assert.deepEqual(sceneProblems(each), [], each.id);
  assert.deepEqual(thumbnailProblems(showcase.thumbnail), []);
  assert.deepEqual(Object.keys(TEMPLATE_SPECS).sort(), [...new Set(showcase.scenes.map((each) => each.template))].sort(), "the showcase uses every template");
});

test("template data problems name the field", () => {
  const bullets = scene("three-questions");
  bullets.data.items = [];
  assert.deepEqual(sceneProblems(bullets), ["items must be 1 to 6 strings"]);
  const table = scene("numbers");
  table.data.rows[1] = ["只有兩格", "x"];
  assert.deepEqual(sceneProblems(table), ["rows must be 1 to 8 arrays as long as columns", "highlight must be a row index"]);
  const code = scene("api-call");
  code.data.code = Array.from({ length: 20 }, () => "x").join("\n");
  assert.match(sceneProblems(code)[0], /20 lines; at most 16 fit/);
  const diagram = scene("cost-diagram");
  diagram.data.svg = "../../secret.svg";
  assert.match(sceneProblems(diagram)[0], /repository path under apps\/web\/public\//);
});

test("a scene cannot reveal more than its template has", () => {
  const compare = scene("flagship-vs-small");
  compare.lines[0].reveal = 2;
  assert.deepEqual(sceneProblems(compare), ["reveals 3 elements but the compare slide has 2"]);
});

test("reveals apply to the last elements: three reveals over three items start from none", () => {
  const at = (reveal, previous, first) => [0, 1, 2].map(visibility(3, 3, reveal, previous, first));
  assert.deepEqual(at(1, 0, true).map((each) => each.shown), [true, false, false]);
  assert.deepEqual(at(2, 1, false).map((each) => [each.shown, each.entering]), [[true, false], [true, true], [false, false]]);
  // One reveal over three items: the first two are there from the start.
  assert.deepEqual([0, 1, 2].map(visibility(3, 1, 0, 0, true)).map((each) => each.shown), [true, true, false]);
  // An element that enters alone has no stagger delay.
  assert.equal(visibility(3, 3, 3, 2, false)(2).order, 0);
});

test("hidden elements keep their space, so the layout does not jump when they appear", () => {
  const bullets = scene("three-questions");
  const html = slideHtml(bullets, state({ reveal: 1, totalReveals: 3 }));
  assert.equal((html.match(/data-hidden/g) ?? []).length, 2);
  assert.match(html, /<li class="enter"/);
});

test("only elements that appear in a state animate in it", () => {
  const bullets = scene("three-questions");
  const html = slideHtml(bullets, state({ reveal: 2, previousReveal: 1, first: false, totalReveals: 3 }));
  assert.equal((html.match(/class="enter"/g) ?? []).length, 1);
  assert.doesNotMatch(html, /heading fit enter/);
});

test("text is escaped and **emphasis** is the only markup", () => {
  assert.equal(escapeHtml(`<b>"&'`), "&lt;b&gt;&quot;&amp;&#39;");
  assert.equal(richText("排行榜 **不一定** <x>"), "排行榜 <em>不一定</em> &lt;x&gt;");
  const title = scene("opening");
  title.data.title = "<script>alert(1)</script>";
  assert.doesNotMatch(slideHtml(title, state()), /<script>/);
});

test("pages load only the theme, the bundled fonts and repository assets from the fake origin", () => {
  const html = slideHtml(scene("cost-diagram"), state());
  const urls = [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map((match) => match[1]);
  assert.deepEqual(urls, [
    "https://video.local/fonts/noto-sans-tc/index.css",
    "https://video.local/fonts/jetbrains-mono/index.css",
    "https://video.local/theme.css",
    assetUrl("apps/web/public/guides/ai-workflow-cost-quality-latency/diagram-1.svg"),
  ]);
});

test("the chapter label is drawn when given and the brand always is", () => {
  const html = slideHtml(scene("numbers"), state({ chapter: "比一比" }));
  assert.match(html, /<div class="chrome-chapter">比一比<\/div><div class="chrome-brand">MOKAAIR<\/div>/);
  assert.doesNotMatch(slideHtml(scene("numbers"), state({ chapter: null })), /chrome-chapter/);
});

test("with the chapter count known, the corner says 02 / 06 and a bar marks the chapters seen and current", () => {
  const html = slideHtml(scene("numbers"), state({ chapter: "比一比", chapterNumber: 2, chapterCount: 4 }));
  assert.match(html, /<div class="chrome-progress"><span class="done"><\/span><span class="now"><\/span><span><\/span><span><\/span><\/div>/);
  assert.match(html, /<div class="chrome-chapter"><span class="index">02 \/ 04<\/span>比一比<\/div>/);
  assert.doesNotMatch(slideHtml(scene("opening"), state({ chapter: null, chapterCount: 4 })), /chrome-progress/, "the title card opens clean");
  assert.match(slideHtml(scene("part-one"), state({ chapter: null, chapterNumber: 2, chapterCount: 4 })), /<div class="number enter" style="--i:0">02<span class="of">\/ 04<\/span><\/div>/);
  assert.doesNotMatch(slideHtml(scene("numbers"), state({ chapterCount: 1 })), /chrome-progress|class="index"/, "one chapter needs no map");
});

test("the new templates check their data and reveal one element at a time", () => {
  const chat = scene("ask-once");
  const first = slideHtml(chat, state({ reveal: 1, totalReveals: 2 }));
  assert.equal((first.match(/class="msg (left|right)[^"]*"/g) ?? []).length, 2);
  assert.equal((first.match(/data-hidden/g) ?? []).length, 1, "the answer waits for its line");
  chat.data.messages[0].side = "middle";
  assert.match(sceneProblems(chat)[0], /side: left\|right/);
  const quote = scene("own-words");
  delete quote.data.source;
  assert.deepEqual(sceneProblems(quote), ["source is required: where the words come from"]);
  const stats = scene("speed-cost");
  stats.lines[0].reveal = 3;
  assert.deepEqual(sceneProblems(stats), ["reveals 4 elements but the stats slide has 2"]);
  assert.match(slideHtml(scene("speed-cost"), state({ reveal: 2, totalReveals: 2 })), /style="--n:2"/);
  assert.match(slideHtml(scene("article-card"), state()), /<div class="site">mokaair\.com<\/div><\/div>/);
});

test("the terminal slide brings its own CSS; every other slide's head is what it was, so their frame keys hold", () => {
  for (const each of showcase.scenes) {
    const head = /<style>([^<]*)<\/style>/.exec(slideHtml(each, state()))[1];
    if (each.template === "terminal") assert.match(head, /^:root\{--width:1920px;--height:1080px\}\.t-terminal /);
    else assert.equal(head, ":root{--width:1920px;--height:1080px}", each.id);
  }
  const terminal = scene("check-version");
  assert.match(slideHtml(terminal, state({ totalReveals: 1 })), /<span class="ps">\$<\/span> <span class="cmd"><span class="k" style="animation-delay:0ms">c<\/span>/);
  delete terminal.data.tool_version;
  assert.match(sceneProblems(terminal)[0], /^tool_version is required/);
});

test("chat lint keeps every accepted bubble within the 1080p layout budget", () => {
  const chat = scene("ask-once");
  assert.deepEqual(sceneProblems(chat), [], "the two long named bubbles are renderable");
  chat.data.messages = Array.from({ length: 4 }, (_, index) => ({ side: index % 2 ? "left" : "right", name: "你", text: "短句" }));
  assert.match(sceneProblems(chat).join("; "), /messages must be 1 to 3/);
  chat.data.messages.pop();
  assert.deepEqual(sceneProblems(chat), ["named chat messages are limited to 2"]);
  chat.data.messages.forEach((message) => delete message.name);
  assert.deepEqual(sceneProblems(chat), [], "three unnamed bubbles fit");
  chat.data.messages[0].text = "字".repeat(45);
  assert.match(sceneProblems(chat).join("; "), /at most 44 characters/);
  chat.data.messages[0].text = "短句\n下一行";
  assert.match(sceneProblems(chat).join("; "), /at most 44 characters/);
  chat.data.messages[0].text = "短句";
  chat.data.title = "標題".repeat(11);
  assert.match(sceneProblems(chat).join("; "), /chat title must fit on one line/);
});

test("a screenshot slide takes a stock photo from the work directory, with an optional credit that brings its own CSS", () => {
  const sha = "a".repeat(64);
  const shot = scene("screen");
  const plain = slideHtml(shot, state());
  shot.data.image = `stock/${sha}.jpg`;
  assert.deepEqual(sceneProblems(shot), []);
  const html = slideHtml(shot, state());
  assert.match(html, new RegExp(`<img src="https://video\\.local/work/stock/${sha}\\.jpg" alt="">`), "served from the work directory, as the keyframes are");
  assert.doesNotMatch(html, /\/repo\//);
  const head = (markup) => markup.slice(0, markup.indexOf("<body>"));
  assert.equal(head(html), head(plain), "without a credit the head is every screenshot's head, so no frame key moves");
  assert.doesNotMatch(html, /class="credit"/);
  shot.data.credit = "Photo by Lukas Rodriguez on Pexels";
  assert.deepEqual(sceneProblems(shot), []);
  const credited = slideHtml(shot, state());
  assert.match(credited, /<\/div><div class="credit">Photo by Lukas Rodriguez on Pexels<\/div><\/div><\/div><div class="caption-line">/, "in the picture's corner, after the highlight box");
  assert.match(credited, /<style>:root\{--width:1920px;--height:1080px\}\.t-screenshot \.credit\{position:absolute;right:16px;bottom:14px;/, "the credit's CSS rides in the page, not the theme");
  assert.match(visibleText(credited), /Photo by Lukas Rodriguez on Pexels/, "the credit's glyphs go through the font check");
  // Where the picture may come from, and nowhere else: the tool writes stock/<sha256>.<png|jpg|webp>.
  for (const image of [`stock/${sha}.gif`, `stock/${sha.slice(0, 63)}.jpg`, `stock/../${sha}.jpg`, `STOCK/${sha}.jpg`, `stock/${sha}.JPG`, `stock/${sha}.jpeg`, `work/stock/${sha}.jpg`, "stock/"]) {
    shot.data.image = image;
    assert.match(sceneProblems(shot)[0] ?? "", /^image must be a repository path under apps\/web\/public\/ or docs\/videos\/, or a stock photo fetched into the work directory/, image);
  }
  shot.data.image = `stock/${sha}.webp`;
  for (const credit of ["", "two\nlines", "字".repeat(CREDIT_MAX_CHARS + 1), 7]) {
    shot.data.credit = credit;
    assert.deepEqual(sceneProblems(shot), [`credit must be one line of text (at most ${CREDIT_MAX_CHARS} characters)`], JSON.stringify(credit));
  }
  shot.data.credit = "字".repeat(CREDIT_MAX_CHARS);
  assert.deepEqual(sceneProblems(shot), []);
  assert.ok(isStockPath(`stock/${sha}.png`) && !isStockPath(`stock/${sha}.svg`) && !isStockPath(null));
  assert.equal(workUrl("stock/a b.png"), "https://video.local/work/stock/a%20b.png");
});

test("an inlined SVG loses its prolog and fixed size; scripts and network loads are refused", () => {
  const svg = '<?xml version="1.0"?><!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900"><text>圖</text></svg>';
  assert.equal(inlineSvg(svg), '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><text>圖</text></svg>');
  assert.deepEqual(svgProblems(svg), []);
  assert.equal(svgProblems('<svg><script>x()</script></svg>').length, 1);
  assert.equal(svgProblems('<svg><rect onload="x()"/></svg>').length, 1);
  assert.equal(svgProblems('<svg><image href="https://example.com/a.png"/></svg>').length, 1);
  assert.deepEqual(svgProblems("not svg"), ["the file is not an SVG"]);
  const html = slideHtml(scene("cost-diagram"), state({ svg }));
  assert.match(html, /<div class="paper enter" style="--i:1"><svg xmlns/);
});

test("the thumbnail is its own 1280x720 page: the words in the left column, the subject's area on the right", () => {
  const html = thumbnailHtml(showcase.thumbnail);
  assert.match(html, /--width:1280px;--height:720px/);
  assert.match(html, /<h1 class="fit"><em>不一定<\/em>最好用<\/h1>/);
  // The showcase names layout a; without a picture the subject's area is a flat tone.
  assert.match(html, /<body><div class="thumb-subject layout-a tone-[a-z]+"><\/div><div class="thumb column layout-a tone-[a-z]+"><div class="tag">AI 模型怎麼挑<\/div><h1/);
  assert.match(html, /<div class="sub fit">三個問題幫你決定<\/div><div class="brand">MOKAAIR<\/div><\/div><\/body>/);
  assert.doesNotMatch(html, /thumb-art|thumb-bg|thumb-scrim|<style>:root\{[^}]*\}\./, "no ring, no series CSS: the theme draws the channel's layouts");
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: {} }), ["thumbnail.data.headline is required"]);
  // A picture: a keyframe is cropped to its right side, a page still to its top left corner.
  const onKeyframe = thumbnailHtml(showcase.thumbnail, { background: "https://video.local/work/keyframes/a.png" });
  assert.match(onKeyframe, /<body><div class="thumb-subject layout-a tone-[a-z]+ from-shot"><img src="https:\/\/video\.local\/work\/keyframes\/a\.png" alt=""><\/div><div class="thumb column/);
  const onStill = thumbnailHtml(showcase.thumbnail, { background: "https://video.local/work/screencast/k/01.png", subject: "capture" });
  assert.match(onStill, /<div class="thumb-subject layout-a tone-[a-z]+ from-capture"><img src="https:\/\/video\.local\/work\/screencast\/k\/01\.png" alt="">/);
  assert.doesNotMatch(visibleText(onStill), /from-capture|object-fit/);
  assert.equal(thumbnailHtml(showcase.thumbnail, { background: "https://video.local/work/keyframes/a.png", subject: "nosuch" }), onKeyframe, "an unknown subject kind is drawn like a keyframe");
});

test("the channel's layout and tone rotate by slug, a variant one step on, and data.layout or data.tone name one", () => {
  const thumb = { template: "thumb", data: { headline: "驗證碼\n別給", tag: "詐騙" } };
  const rotation = thumbnailRotation("facebook-code-scam");
  assert.ok(THUMB_LAYOUTS.includes(rotation.layout) && THUMB_TONES.includes(rotation.tone));
  assert.deepEqual(thumbnailRotation("facebook-code-scam"), rotation, "the same slug, the same thumbnail");
  assert.match(thumbnailHtml(thumb, { slug: "facebook-code-scam" }), new RegExp(`<div class="thumb column layout-${rotation.layout} tone-${rotation.tone}">`));
  const seen = new Set(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"].map((slug) => thumbnailRotation(slug).layout));
  assert.deepEqual([...seen].sort(), THUMB_LAYOUTS, "twelve slugs reach all three layouts");
  const next = thumbnailRotation("facebook-code-scam", 1);
  assert.notEqual(next.layout, rotation.layout, "the B variant takes the next layout");
  assert.notEqual(next.tone, rotation.tone, "and the next tone");
  assert.notEqual(thumbnailRotation("facebook-code-scam", 2).layout, next.layout);
  assert.match(thumbnailHtml({ ...thumb, data: { ...thumb.data, layout: "c", tone: "plum" } }, { slug: "facebook-code-scam" }), /<div class="thumb-subject layout-c tone-plum"><\/div><div class="thumb column layout-c tone-plum">/);
  assert.match(thumbnailHtml(thumb), /layout-[abc] tone-(teal|plum|navy|forest)/, "no slug: still a layout and a tone");
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "x", layout: "left", tone: "red" } }), ["thumbnail.data.layout must be one of a, b, c", "thumbnail.data.tone must be one of teal, plum, navy, forest"]);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "x", layout: "b", tone: "navy", capture: "find-guides#2", shot: "hall" } }), []);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "x", capture: "Find Guides", shot: 3 } }), ['thumbnail.data.capture must name a screencast scene, "<scene id>" or "<scene id>#<n>" for its n-th capture', "thumbnail.data.shot must be a shot's id"]);
  assert.deepEqual(captureRef("find-guides"), { scene: "find-guides", index: 0 });
  assert.deepEqual(captureRef("find-guides#3"), { scene: "find-guides", index: 2 });
  assert.equal(captureRef("find-guides#0"), null);
  assert.equal(captureRef(null), null);
  assert.deepEqual(headlineCount("驗證碼\n別給"), { cjk: 5, words: [], count: 5 });
  assert.deepEqual(headlineCount("**128 GB**\n裝得下嗎"), { cjk: 4, words: ["128", "GB"], count: 6 });
  assert.deepEqual(headlineCount("Can it cost\n**16x more?**"), { cjk: 0, words: ["Can", "it", "cost", "16x", "more"], count: 5 });
  // A price or a number with a thousands separator is one number, as the rule says.
  assert.deepEqual(headlineCount("NT$270 一年"), { cjk: 2, words: ["NT$270"], count: 3 });
  assert.deepEqual(headlineCount("**1,000** 元差在哪"), { cjk: 4, words: ["1,000"], count: 5 });
  assert.deepEqual(headlineCount("$1,000 vs 500").words, ["$1,000", "vs", "500"]);
  assert.deepEqual(headlineCount("US$20 或 €18").words, ["US$20", "€18"]);
  assert.deepEqual(headlineCount("Yes, 可以").words, ["Yes"], "a comma at the end is the sentence's");
  assert.equal(THUMB_HEADLINE_MAX, 6);
});

test("a Korean, Simplified Chinese or Japanese thumbnail is set in its own font first; every other page keeps its head byte for byte", () => {
  const head = '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-tc/index.css"><link rel="stylesheet" href="https://video.local/fonts/jetbrains-mono/index.css"><link rel="stylesheet" href="https://video.local/theme.css"><style>:root{--width:1280px;--height:720px}';
  const plain = thumbnailHtml(showcase.thumbnail);
  assert.ok(plain.startsWith(head), "the video's own thumbnail: the frame keys of existing videos do not move");
  assert.equal(thumbnailHtml(showcase.thumbnail, { locale: "en" }), plain, "a locale without its own font draws the same page");
  assert.equal(thumbnailHtml(showcase.thumbnail, { locale: "zh-TW" }), plain);
  const ja = thumbnailHtml(showcase.thumbnail, { locale: "ja" });
  assert.ok(ja.startsWith('<!doctype html><html lang="ja"><head><meta charset="utf-8"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-jp/index.css"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-tc/index.css">'));
  assert.match(ja, /<style>:root\{--width:1280px;--height:720px;--font:"Noto Sans JP Variable","Noto Sans TC Variable",sans-serif\}/);
  const ko = thumbnailHtml(showcase.thumbnail, { locale: "ko" });
  assert.ok(ko.startsWith('<!doctype html><html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-kr/index.css"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-tc/index.css">'));
  assert.match(ko, /<style>:root\{--width:1280px;--height:720px;--font:"Noto Sans KR Variable","Noto Sans TC Variable",sans-serif\}/);
  const sc = thumbnailHtml(showcase.thumbnail, { locale: "zh-CN" });
  assert.match(sc, /^<!doctype html><html lang="zh-Hans">.*fonts\/noto-sans-sc\/index\.css/);
  assert.match(sc, /--font:"Noto Sans SC Variable","Noto Sans TC Variable",sans-serif\}/);
  const body = (html) => html.slice(html.indexOf("<body>"));
  assert.equal(body(ko), body(plain), "the same body, only the font differs");
  assert.equal(body(ja), body(plain));
  assert.doesNotMatch(slideHtml(scene("opening"), state()), /noto-sans-(kr|sc|jp)|--font:/, "slides never load the other fonts");
});

test("visibleText is what the font check sees: text without markup or the head", () => {
  const text = visibleText(slideHtml(scene("keyword"), state({ chapter: "章" })));
  assert.match(text, /MMLU-Pro/);
  assert.doesNotMatch(text, /index\.css|<|style/);
});

test("So That's Why wears its own thumbnail: palette, name, stamp, pillar tag, a mirrored layout and a short headline", () => {
  const thumb = { template: "thumb", data: { headline: "冰為什麼\n會**浮**？", tag: "科學", pillar: "science", shot: "a" } };
  const plain = thumbnailHtml(thumb, { background: "https://video.local/work/keyframes/a.png" });
  assert.match(plain, new RegExp(`<div class="brand">${BRAND}</div>`), "no series: the channel's thumbnail");
  assert.doesNotMatch(plain, /thumb-stamp|pillar-|layout-right|#1f2a44|thumb-bg|thumb-scrim/);
  const own = thumbnailHtml(thumb, { background: "https://video.local/work/keyframes/a.png", series: "sothatswhy" });
  // The series keeps its page: the keyframe fills the frame under a scrim, the column runs full width.
  assert.match(own, /<body><img class="thumb-bg" src="https:\/\/video\.local\/work\/keyframes\/a\.png" alt=""><div class="thumb-scrim"><\/div><div class="thumb series">/);
  assert.match(own, /<style>:root\{[^<]*\.thumb-bg\{position:absolute;inset:0;width:100%;height:100%;object-fit:cover\}/);
  assert.doesNotMatch(visibleText(own), /object-fit/);
  assert.doesNotMatch(thumbnailHtml(thumb, { series: "sothatswhy" }), /thumb-art|thumb-bg|thumb-subject/, "no keyframe: no ring either, the ink ground alone");
  assert.match(own, /<div class="brand">原來如此事務所<\/div>/);
  assert.match(own, /<div class="thumb-stamp" aria-hidden="true"><span>原來<\/span><span>如此<\/span><\/div>/);
  assert.match(own, /<div class="tag pillar-science">科學<\/div>/);
  assert.match(own, /rgba\(31,42,68,\.94\)/, "the ink-navy scrim");
  const right = thumbnailHtml({ ...thumb, data: { ...thumb.data, layout: "right" } }, { background: "https://video.local/work/keyframes/a.png", series: "sothatswhy" });
  assert.match(right, /<div class="thumb-scrim layout-right"><\/div><div class="thumb series layout-right">/);
  assert.match(thumbnailHtml({ ...thumb, data: { ...thumb.data, pillar: "sports" } }, { series: "sothatswhy" }), /<div class="tag">科學<\/div>/, "an unknown pillar keeps the default tag");

  assert.deepEqual(thumbnailProblems(thumb, { series: "sothatswhy" }), []);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "一二三四五六七八九十十一" } }), [], "the channel's thumbnails keep their length");
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "一二三四五六七八九十十一" } }, { series: "sothatswhy" }), ["thumbnail.data.headline has a line of 12 characters; this series takes at most 10 a line, readable at phone size"]);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "一\n二\n三" } }, { series: "sothatswhy" }), ["thumbnail.data.headline has 3 lines; this series takes at most 2"]);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "x", layout: "top", pillar: "sports" } }, { series: "sothatswhy" }), ["thumbnail.data.layout must be one of left, right", "thumbnail.data.pillar must be one of business, science, travel, tech"]);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "x", layout: "right" } }), ["thumbnail.data.layout must be one of a, b, c"], "the channel's layouts are its own");
});

test("a thumbnail's B and C variants for YouTube's test are laid over A and linted like it", () => {
  const thumb = { template: "thumb", data: { headline: "冰為什麼\n會**浮**？", tag: "科學", pillar: "science", shot: "a" }, variants: [{ data: { headline: "**差 9%**" } }, { data: { headline: "冰 vs 石", sub: "誰會沉下去？", shot: "b" } }] };
  const variants = thumbnailVariants(thumb);
  assert.deepEqual(variants.map((variant) => variant.id), THUMB_VARIANT_IDS);
  assert.deepEqual(variants[0].thumbnail, { template: "thumb", data: { headline: "**差 9%**", tag: "科學", pillar: "science", shot: "a" } }, "B only changes the headline");
  assert.equal(variants[1].thumbnail.data.shot, "b");
  assert.deepEqual(thumbnailVariants({ template: "thumb", data: { headline: "x" } }), [], "no variants: A alone");
  assert.deepEqual(thumbnailProblems(thumb, { series: "sothatswhy" }), []);
  const long = { ...thumb, variants: [{ data: { headline: "一二三四五六七八九十十一" } }] };
  assert.deepEqual(thumbnailProblems(long, { series: "sothatswhy" }), ["variant b: thumbnail.data.headline has a line of 12 characters; this series takes at most 10 a line, readable at phone size"]);
  assert.deepEqual(thumbnailProblems({ ...thumb, variants: [{ data: { layout: "top" } }] }, { series: "sothatswhy" }), ["variant b: thumbnail.data.layout must be one of left, right"]);
  assert.deepEqual(thumbnailProblems({ ...thumb, variants: [{ data: { layout: "top" } }] }), ["variant b: thumbnail.data.layout must be one of a, b, c"]);
  const shape = "thumbnail.variants must be 1 to 2 of { data: {...} } (A is the thumbnail itself; YouTube tests up to three)";
  for (const variants of [[], [{}], "b", [{ data: {} }, { data: {} }, { data: {} }]]) assert.deepEqual(thumbnailProblems({ ...thumb, variants }), [shape], JSON.stringify(variants));
});
