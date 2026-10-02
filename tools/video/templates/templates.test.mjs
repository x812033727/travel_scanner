import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { assetUrl, BRAND, escapeHtml, inlineSvg, richText, sceneProblems, slideHtml, svgProblems, TEMPLATE_SPECS, THUMB_VARIANT_IDS, thumbnailHtml, thumbnailProblems, thumbnailVariants, visibility, visibleText } from "./templates.mjs";

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

test("the thumbnail is its own 1280x720 page", () => {
  const html = thumbnailHtml(showcase.thumbnail);
  assert.match(html, /--width:1280px;--height:720px/);
  assert.match(html, /第一名<em>不一定<\/em>最好用/);
  assert.match(html, /<div class="thumb-art"><\/div>/);
  assert.doesNotMatch(html, /thumb-bg/);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: {} }), ["thumbnail.data.headline is required"]);
  // A drama's thumbnail sits on a keyframe under a scrim, with the CSS in the head, not the theme.
  const onKeyframe = thumbnailHtml(showcase.thumbnail, { background: "https://video.local/work/keyframes/a.png" });
  assert.match(onKeyframe, /<body><img class="thumb-bg" src="https:\/\/video\.local\/work\/keyframes\/a\.png" alt=""><div class="thumb-scrim"><\/div><div class="thumb">/);
  assert.match(onKeyframe, /<style>:root\{[^<]*\.thumb-bg\{position:absolute;inset:0;width:100%;height:100%;object-fit:cover\}/);
  assert.doesNotMatch(onKeyframe, /thumb-art/);
  assert.doesNotMatch(visibleText(onKeyframe), /object-fit/);
});

test("a Korean or Simplified Chinese thumbnail is set in its own font first; every other page keeps its head byte for byte", () => {
  const head = '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-tc/index.css"><link rel="stylesheet" href="https://video.local/fonts/jetbrains-mono/index.css"><link rel="stylesheet" href="https://video.local/theme.css"><style>:root{--width:1280px;--height:720px}';
  const plain = thumbnailHtml(showcase.thumbnail);
  assert.ok(plain.startsWith(head), "the video's own thumbnail: the frame keys of existing videos do not move");
  assert.equal(thumbnailHtml(showcase.thumbnail, { locale: "en" }), plain, "a locale without its own font draws the same page");
  assert.equal(thumbnailHtml(showcase.thumbnail, { locale: "ja" }), plain);
  const ko = thumbnailHtml(showcase.thumbnail, { locale: "ko" });
  assert.ok(ko.startsWith('<!doctype html><html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-kr/index.css"><link rel="stylesheet" href="https://video.local/fonts/noto-sans-tc/index.css">'));
  assert.match(ko, /<style>:root\{--width:1280px;--height:720px;--font:"Noto Sans KR Variable","Noto Sans TC Variable",sans-serif\}/);
  const sc = thumbnailHtml(showcase.thumbnail, { locale: "zh-CN" });
  assert.match(sc, /^<!doctype html><html lang="zh-Hans">.*fonts\/noto-sans-sc\/index\.css/);
  assert.match(sc, /--font:"Noto Sans SC Variable","Noto Sans TC Variable",sans-serif\}/);
  const body = (html) => html.slice(html.indexOf("<body>"));
  assert.equal(body(ko), body(plain), "the same body, only the font differs");
  assert.doesNotMatch(slideHtml(scene("opening"), state()), /noto-sans-(kr|sc)|--font:/, "slides never load the other fonts");
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
  assert.doesNotMatch(plain, /thumb-stamp|pillar-|layout-right|#1f2a44/);
  const own = thumbnailHtml(thumb, { background: "https://video.local/work/keyframes/a.png", series: "sothatswhy" });
  assert.match(own, /<div class="brand">原來如此事務所<\/div>/);
  assert.match(own, /<div class="thumb-stamp" aria-hidden="true"><span>原來<\/span><span>如此<\/span><\/div>/);
  assert.match(own, /<div class="tag pillar-science">科學<\/div>/);
  assert.match(own, /rgba\(31,42,68,\.94\)/, "the ink-navy scrim");
  const right = thumbnailHtml({ ...thumb, data: { ...thumb.data, layout: "right" } }, { background: "https://video.local/work/keyframes/a.png", series: "sothatswhy" });
  assert.match(right, /<div class="thumb-scrim layout-right"><\/div><div class="thumb layout-right">/);
  assert.match(thumbnailHtml({ ...thumb, data: { ...thumb.data, pillar: "sports" } }, { series: "sothatswhy" }), /<div class="tag">科學<\/div>/, "an unknown pillar keeps the default tag");

  assert.deepEqual(thumbnailProblems(thumb, { series: "sothatswhy" }), []);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "一二三四五六七八九十十一" } }), [], "the channel's thumbnails keep their length");
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "一二三四五六七八九十十一" } }, { series: "sothatswhy" }), ["thumbnail.data.headline has a line of 12 characters; this series takes at most 10 a line, readable at phone size"]);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "一\n二\n三" } }, { series: "sothatswhy" }), ["thumbnail.data.headline has 3 lines; this series takes at most 2"]);
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: { headline: "x", layout: "top", pillar: "sports" } }), ["thumbnail.data.layout must be one of left, right", "thumbnail.data.pillar must be one of business, science, travel, tech"]);
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
  assert.deepEqual(thumbnailProblems({ ...thumb, variants: [{ data: { layout: "top" } }] }), ["variant b: thumbnail.data.layout must be one of left, right"]);
  const shape = "thumbnail.variants must be 1 to 2 of { data: {...} } (A is the thumbnail itself; YouTube tests up to three)";
  for (const variants of [[], [{}], "b", [{ data: {} }, { data: {} }, { data: {} }]]) assert.deepEqual(thumbnailProblems({ ...thumb, variants }), [shape], JSON.stringify(variants));
});
