import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { assetUrl, escapeHtml, richText, sceneProblems, slideHtml, TEMPLATE_SPECS, thumbnailHtml, thumbnailProblems, visibility, visibleText } from "./templates.mjs";

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
