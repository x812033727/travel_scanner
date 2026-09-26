import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { assetUrl, escapeHtml, inlineSvg, richText, sceneProblems, slideHtml, svgProblems, TEMPLATE_SPECS, thumbnailHtml, thumbnailProblems, visibility, visibleText } from "./templates.mjs";

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
  assert.deepEqual(thumbnailProblems({ template: "thumb", data: {} }), ["thumbnail.data.headline is required"]);
});

test("visibleText is what the font check sees: text without markup or the head", () => {
  const text = visibleText(slideHtml(scene("keyword"), state({ chapter: "章" })));
  assert.match(text, /MMLU-Pro/);
  assert.doesNotMatch(text, /index\.css|<|style/);
});
