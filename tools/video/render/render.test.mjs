import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { estimateTimeline } from "../core/timeline.mjs";
import { resolveRequest } from "./browser.mjs";
import { coverageProblems } from "./cli.mjs";
import { contactSheetHtml } from "./contact.mjs";
import { bundledCoverage, covers, mergeRanges, parseUnicodeRanges, uncovered } from "./fonts.mjs";
import { renderPlan, renderProblems, stillFile, themeHash, transitionFile } from "./plan.mjs";

const showcase = JSON.parse(readFileSync(new URL("../templates/fixtures/showcase/video.json", import.meta.url), "utf8"));

test("unicode-range parsing handles single points, ranges and wildcards, merged and sorted", () => {
  const ranges = parseUnicodeRanges("a{unicode-range: U+4E00-4E05, U+0041;} b{unicode-range: U+4E06,U+30??;}");
  assert.deepEqual(ranges, [[0x41, 0x41], [0x3000, 0x30ff], [0x4e00, 0x4e06]]);
  assert.deepEqual(mergeRanges([[5, 9], [1, 3], [4, 4]]), [[1, 9]]);
  assert.ok(covers(ranges, 0x4e03));
  assert.ok(!covers(ranges, 0x42));
});

test("the bundled fonts cover Traditional Chinese, Latin and full-width punctuation, not emoji", () => {
  const coverage = bundledCoverage();
  assert.deepEqual(uncovered("排行榜第一名，不一定最好用？MMLU-Pro 4.1 秒「」（）→", coverage), []);
  assert.deepEqual(uncovered("好用 🤖", coverage), ["🤖"]);
});

test("a glyph no bundled font has is reported with its code point", () => {
  const doc = structuredClone(showcase);
  doc.scenes[0].data.subtitle = "好用 🤖";
  const problems = coverageProblems(renderPlan(doc, "t"), bundledCoverage());
  assert.equal(problems.length, 1);
  assert.match(problems[0].message, /U\+1F916/);
});

test("the plan has one entry per timeline state, in the same order", () => {
  const plan = renderPlan(showcase, "theme");
  const timeline = estimateTimeline(showcase);
  assert.deepEqual(
    plan.scenes.map((scene) => scene.states.length),
    timeline.scenes.map((scene) => scene.states.length),
  );
  assert.deepEqual(plan.scenes.find((scene) => scene.id === "three-questions").states.map((state) => state.reveal), [1, 2, 3]);
  assert.ok(plan.thumbnail.key);
});

test("keys change with the picture or the theme, and only then", () => {
  const base = renderPlan(showcase, "theme-a");
  const again = renderPlan(showcase, "theme-a");
  assert.deepEqual(base.scenes.map((scene) => scene.states.map((state) => state.key)), again.scenes.map((scene) => scene.states.map((state) => state.key)));
  const otherTheme = renderPlan(showcase, "theme-b");
  assert.notEqual(otherTheme.scenes[0].states[0].key, base.scenes[0].states[0].key);
  const narration = structuredClone(showcase);
  narration.scenes[0].lines[0].text = "旁白改了，畫面沒改。";
  assert.equal(renderPlan(narration, "theme-a").scenes[0].states[0].key, base.scenes[0].states[0].key);
  assert.match(themeHash(), /^[0-9a-f]{16}$/);
});

test("chapter labels carry forward, except on title and chapter cards", () => {
  const plan = renderPlan(showcase, "t");
  const label = (id) => /chrome-chapter">([^<]+)</.exec(plan.scenes.find((scene) => scene.id === id).states[0].html)?.[1] ?? null;
  assert.equal(label("opening"), null);
  assert.equal(label("part-one"), null);
  assert.equal(label("three-questions"), "三個問題");
  assert.equal(label("keyword"), "三個問題");
  assert.equal(label("numbers"), "比一比");
});

test("template data problems are labelled with the scene", () => {
  const doc = structuredClone(showcase);
  doc.scenes[2].data.items = "not a list";
  delete doc.thumbnail.data.headline;
  assert.deepEqual(renderProblems(doc).map((problem) => problem.path), ["scenes[2] (three-questions).data", "thumbnail"]);
});

test("with the repository root, diagrams are inlined and asset bytes are part of the key", () => {
  const root = fileURLToPath(new URL("../../../", import.meta.url));
  const plan = renderPlan(showcase, "t", root);
  const diagram = plan.scenes.find((scene) => scene.id === "cost-diagram").states[0];
  assert.match(diagram.html, /<svg xmlns="http:\/\/www\.w3\.org\/2000\/svg" viewBox="0 0 1600 900"/);
  assert.doesNotMatch(diagram.html, /<img src=[^>]*diagram-1\.svg/);
  assert.match(diagram.text, /三種流程的成本估算/, "the diagram's words go through the font coverage check");
  assert.notEqual(diagram.key, renderPlan(showcase, "t").scenes.find((scene) => scene.id === "cost-diagram").states[0].key);
  assert.deepEqual(renderProblems(showcase, root), []);
  const missing = structuredClone(showcase);
  missing.scenes.find((scene) => scene.id === "screen").data.image = "apps/web/public/nope.png";
  assert.match(renderProblems(missing, root)[0].message, /apps\/web\/public\/nope\.png does not exist/);
});

test("frame paths are relative with forward slashes", () => {
  assert.equal(stillFile("abc"), "frames/abc.png");
  assert.equal(transitionFile("abc", 3), "frames/abc-t03.png");
});

test("the fake origin serves pages, theme, fonts and allowed assets, and nothing else", () => {
  const root = path.resolve("/repo");
  const pages = new Map([["ab12", "<html></html>"]]);
  const at = (url) => resolveRequest(url, { root, workdir: path.resolve("/work"), pages });
  assert.equal(at("https://video.local/state/ab12.html").body, "<html></html>");
  assert.equal(at("https://video.local/state/ffff.html"), null);
  assert.match(at("https://video.local/theme.css").file, /theme\.css$/);
  assert.match(at("https://video.local/fonts/noto-sans-tc/files/x.woff2").file, /noto-sans-tc[\\/]files[\\/]x\.woff2$/);
  assert.equal(at("https://video.local/repo/apps/web/public/a.svg").file, path.join(root, "apps/web/public/a.svg"));
  assert.equal(at("https://video.local/repo/apps/api/.env"), null);
  assert.equal(at("https://video.local/repo/apps/web/public/../../api/.env"), null);
  assert.equal(at("https://video.local/work/frames/a.png").file, path.join(path.resolve("/work"), "frames/a.png"));
  assert.equal(at("https://fonts.googleapis.com/css"), null);
});

test("the contact sheet lists every tile from the work directory", () => {
  const html = contactSheetHtml("標題 <x>", [{ file: "frames/a.png", label: "hook · title · 1/1" }]);
  assert.match(html, /<img src="https:\/\/video\.local\/work\/frames\/a\.png"/);
  assert.match(html, /標題 &lt;x&gt;/);
});
