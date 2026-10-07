import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { EXIT, main } from "../cli.mjs";
import { compilationSandbox } from "../compile/fixture.mjs";
import { compilationDocument, THUMB_SOURCE } from "../core/compilation.mjs";
import { dramaFixture, explainerFixture, sandbox, tempDir } from "../core/fixtures/load.mjs";
import { estimateTimeline, visualHash } from "../core/timeline.mjs";
import { LAUNCH_ARGS, resolveRequest } from "./browser.mjs";
import { compareRuns } from "./repeat.mjs";
import { localizedThumbnailHash, thumbnailSource, thumbnailSourceHash } from "../core/translations.mjs";
import { coverageProblems, localizedThumbnails } from "./cli.mjs";
import { contactSheetHtml } from "./contact.mjs";
import { bundledCoverage, covers, mergeRanges, parseUnicodeRanges, uncovered } from "./fonts.mjs";
import { assetFile, localeThumbnailFile, renderPlan, renderProblems, sceneAssets, stillFile, themeHash, thumbnailVariantFile, transitionFile } from "./plan.mjs";
import { BLANK_STRIP, blankStripHtml, blankStripKey, STRIP_SIZE, stripFile, stripHtml, subtitlePlan } from "./subtitles.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

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

test("coverage is judged per language: Korean and Simplified Chinese thumbnails have their own font, slides still refuse what only those have", () => {
  const slides = bundledCoverage();
  // 佥 (U+4F65) is the Simplified form of 僉: only the SC font's ranges hold it.
  assert.deepEqual(uncovered("佥", slides), ["佥"], "a Traditional Chinese slide still refuses it");
  assert.deepEqual(uncovered("佥", bundledCoverage("zh-CN")), []);
  assert.deepEqual(uncovered("바이브 코딩 코드 없이", slides), ["바", "브", "코", "딩", "드", "없"]);
  assert.deepEqual(uncovered("바이브 코딩 코드 없이 AI 2026", bundledCoverage("ko")), []);
  assert.deepEqual(uncovered("佥", bundledCoverage("ko")), ["佥"], "each locale adds only its own font");
  // 侭 (U+4FAD) is a Japanese form of 儘: only the JP font's ranges hold it.
  assert.deepEqual(uncovered("侭", slides), ["侭"], "a Traditional Chinese slide refuses it");
  assert.deepEqual(uncovered("直す 骨 写す 侭 バイブ AI 2026", bundledCoverage("ja")), []);
  assert.deepEqual(uncovered("佥 바", bundledCoverage("ja")), ["佥", "바"], "Japanese adds only the JP font");
  assert.deepEqual(uncovered("侭", bundledCoverage("zh-CN")), ["侭"]);
  assert.equal(bundledCoverage("en"), slides, "a locale without a font of its own is the slides' coverage");
  assert.equal(bundledCoverage(), bundledCoverage(null), "and is read once");
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
  const html = (id) => plan.scenes.find((scene) => scene.id === id).states[0].html;
  const label = (id) => /chrome-chapter">(?:<span class="index">[^<]*<\/span>)?([^<]+)</.exec(html(id))?.[1] ?? null;
  assert.equal(label("opening"), null);
  assert.equal(label("part-one"), null);
  assert.equal(label("three-questions"), "三個問題");
  assert.equal(label("keyword"), "三個問題");
  assert.equal(label("numbers"), "比一比");
  assert.match(html("numbers"), /<span class="index">03 \/ 05<\/span>/, "the showcase has five chapters");
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

test("a stock photo is read from the work directory: listed in assets[], fetched, and its bytes part of the key", () => {
  const sha = "f".repeat(64);
  const stock = `stock/${sha}.png`;
  const doc = structuredClone(showcase);
  const index = doc.scenes.findIndex((scene) => scene.id === "screen");
  doc.scenes[index].data.image = stock;
  const root = fileURLToPath(new URL("../../../", import.meta.url));
  const workdir = tempDir("video-render-");
  const where = `scenes[${index}] (screen).data`;
  assert.deepEqual(sceneAssets(doc.scenes[index]), [stock]);
  assert.equal(assetFile(stock, { root, workdir }), path.join(workdir, "stock", `${sha}.png`));
  assert.equal(assetFile(stock, { root }), null, "no work directory, no file to read");
  assert.equal(assetFile("apps/web/public/a.png", { root, workdir }), path.join(root, "apps/web/public/a.png"));
  assert.deepEqual(renderProblems(doc, root, { workdir }), [
    { path: where, message: `${stock} is not in assets[]: stock fetch writes the entry there, and without it the description carries no credit` },
    { path: where, message: `${stock} is not in the work directory; fetch it with stock fetch (tools/video/media/cli.mjs)` },
  ]);
  doc.assets = [{ path: stock, source: "Photo by Lukas Rodriguez on Pexels", license: "Pexels License", author: "Lukas Rodriguez", url: "https://www.pexels.com/photo/seoul-at-night-3573351/" }];
  assert.deepEqual(renderProblems(doc), [], "without root or work directory only the data is checked, as before");
  assert.deepEqual(renderProblems(doc, root).map((problem) => problem.message), [], "without a work directory the file is not looked for");
  assert.match(renderProblems(doc, root, { workdir })[0].message, /not in the work directory/);
  mkdirSync(path.join(workdir, "stock"));
  writeFileSync(path.join(workdir, "stock", `${sha}.png`), "png one");
  assert.deepEqual(renderProblems(doc, root, { workdir }), []);
  const state = (plan) => plan.scenes.find((scene) => scene.id === "screen").states[0];
  const one = state(renderPlan(doc, "t", root, { workdir }));
  assert.match(one.html, new RegExp(`<img src="https://video\\.local/work/stock/${sha}\\.png" alt="">`));
  assert.equal(state(renderPlan(doc, "t", root, { workdir })).key, one.key, "the same bytes, the same key");
  writeFileSync(path.join(workdir, "stock", `${sha}.png`), "png two");
  const two = state(renderPlan(doc, "t", root, { workdir }));
  assert.equal(two.html, one.html);
  assert.notEqual(two.key, one.key, "a swapped photo redraws the slide that shows it");
  assert.notEqual(state(renderPlan(doc, "t", root)).key, two.key, "without the work directory the bytes are not in the key");
  assert.equal(resolveRequest(`https://video.local/work/${stock}`, { root, workdir, pages: new Map() }).file, path.join(workdir, "stock", `${sha}.png`), "the fake origin serves it from the work directory");
});

test("render draws a stock photo slide from the work directory and redraws it when the photo changes", async () => {
  const box = sandbox();
  const sha = "e".repeat(64);
  const stock = `stock/${sha}.png`;
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const [, questions] = doc.scenes;
  doc.scenes[1] = { ...questions, template: "screenshot", data: { title: "首爾的夜景", image: stock, credit: "Photo by Lukas Rodriguez on Pexels" }, lines: questions.lines.map(({ id, text }) => ({ id, text })) };
  doc.assets = [{ path: stock, source: "Photo by Lukas Rodriguez on Pexels", license: "Pexels License", author: "Lukas Rodriguez", url: "https://www.pexels.com/photo/seoul-at-night-3573351/" }];
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const photo = path.join(box.workdir, "stock", `${sha}.png`);
  mkdirSync(path.dirname(photo), { recursive: true });
  writeFileSync(photo, "png one");
  const captures = [];
  let out = "";
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work },
    stdout: { write: (text) => (out += text) },
    stderr: { write: (text) => (out += text) },
    now: () => new Date("2026-10-05T00:00:00Z"),
    openRenderer: async () => ({
      capture: async (key, html) => {
        captures.push({ key, html });
        return { still: Buffer.from(`png ${key}`), frames: [], problems: [] };
      },
      sheet: async () => Buffer.from("sheet"),
      close: async () => {},
    }),
  };
  const args = ["render", "--slug", box.slug];
  assert.equal(await main(args, ctx), EXIT.ok, out);
  const drawn = captures.filter((capture) => capture.html.includes(`https://video.local/work/${stock}`));
  assert.equal(drawn.length, 1, "the photo slide is drawn once, from the work directory");
  assert.match(drawn[0].html, /<div class="credit">Photo by Lukas Rodriguez on Pexels<\/div>/);
  assert.ok(existsSync(path.join(box.workdir, stillFile(drawn[0].key))));
  const manifest = JSON.parse(readFileSync(path.join(box.workdir, "frames", "manifest.json"), "utf8"));
  assert.deepEqual(manifest.scenes.map((scene) => [scene.id, scene.states.length]), [["hook", 1], ["questions", 1], ["wrap", 1]]);
  assert.match(out, /3 states drawn, 0 reused/);

  // The same photo again: every state is reused. Another photo under the name: that slide alone is redrawn.
  const before = captures.length;
  out = "";
  assert.equal(await main(args, ctx), EXIT.ok, out);
  assert.match(out, /0 states drawn, 3 reused/);
  assert.equal(captures.length - before, 1, "only the thumbnail is captured again");
  writeFileSync(photo, "png two");
  out = "";
  assert.equal(await main(args, ctx), EXIT.ok, out);
  assert.match(out, /1 states drawn, 2 reused/);
  const redrawn = captures.slice(before + 1).filter((capture) => capture.html.includes(`/work/${stock}`));
  assert.equal(redrawn.length, 1);
  assert.notEqual(redrawn[0].key, drawn[0].key, "the key carries the photo's bytes");

  // A photo not fetched yet, or not listed in assets[], stops the render with the reason.
  rmSync(photo);
  out = "";
  assert.equal(await main(args, ctx), EXIT.lint);
  assert.match(out, /ERROR scenes\[1\] \(questions\)\.data: stock\/e+\.png is not in the work directory; fetch it with stock fetch/);
  writeFileSync(photo, "png two");
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify({ ...doc, assets: [] }));
  out = "";
  assert.equal(await main(args, ctx), EXIT.lint);
  assert.match(out, /is not in assets\[\]: stock fetch writes the entry there, and without it the description carries no credit/);
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
  assert.match(at("https://video.local/fonts/noto-sans-kr/index.css").file, /noto-sans-kr[\\/]index\.css$/);
  assert.match(at("https://video.local/fonts/noto-sans-sc/files/y.woff2").file, /noto-sans-sc[\\/]files[\\/]y\.woff2$/);
  assert.match(at("https://video.local/fonts/noto-sans-jp/index.css").file, /noto-sans-jp[\\/]index\.css$/);
  assert.equal(at("https://video.local/fonts/noto-serif-jp/index.css"), null, "only the bundled fonts");
  assert.equal(at("https://video.local/fonts/constructor/index.css"), null);
  assert.equal(at("https://video.local/repo/apps/web/public/a.svg").file, path.join(root, "apps/web/public/a.svg"));
  assert.equal(at("https://video.local/repo/apps/api/.env"), null);
  assert.equal(at("https://video.local/repo/apps/web/public/../../api/.env"), null);
  assert.equal(at("https://video.local/work/frames/a.png").file, path.join(path.resolve("/work"), "frames/a.png"));
  assert.equal(at("https://fonts.googleapis.com/css"), null);
});

test("the renderer draws in software with main-thread animations, so a frame key draws the same bytes", () => {
  // With the GPU and compositor-thread animations, two runs drew 55/68 stills and about a third
  // of the transition frames alike; with both off, every frame of a whole video matched.
  assert.ok(LAUNCH_ARGS.includes("--disable-gpu"));
  assert.ok(LAUNCH_ARGS.includes("--disable-threaded-animation"));
});

test("repeat compares runs frame by frame and names the states that differ", () => {
  const run = (still, frames) => new Map([["k1", { still: "s", frames: ["a", "b"] }], ["k2", { still, frames }]]);
  const same = compareRuns([run("s2", ["c"]), run("s2", ["c"])]);
  assert.deepEqual(same, { stills: 2, sameStills: 2, frames: 3, sameFrames: 3, stillsDiffer: [], framesDiffer: [] });
  const differ = compareRuns([run("s2", ["c"]), run("s2", ["c"]), run("x", ["d"])]);
  assert.equal(differ.sameStills, 1);
  assert.equal(differ.sameFrames, 2);
  assert.deepEqual(differ.stillsDiffer, ["k2"]);
  assert.deepEqual(differ.framesDiffer, ["k2 (0)"]);
  assert.deepEqual(compareRuns([run("s2", ["c"]), run("s2", ["c", "e"])]).framesDiffer, ["k2 (count)"]);
});

test("a drama's shots are clips the plan leaves to the media stages; its cards and thumbnail are drawn", () => {
  const doc = dramaFixture();
  assert.deepEqual(renderProblems(doc), [], "shot prompts are lint's business, not the templates'");
  const plan = renderPlan(doc, "t");
  assert.deepEqual(
    plan.scenes.map((scene) => [scene.id, scene.kind, scene.states.length]),
    [["opening", "clip", 0], ["farewell", "clip", 0], ["sea-storm", "clip", 0], ["bird", "clip", 0], ["wrap", "stills", 1]],
  );
  assert.ok(renderPlan(showcase, "t").scenes.every((scene) => scene.kind === "stills"));
  assert.match(plan.scenes.at(-1).states[0].html, /下一集：夸父逐日/);
  // The thumbnail names a shot: without its keyframe the plan says so; with it, the picture is
  // the background and its hash is part of the key, so a regenerated keyframe redraws it.
  assert.equal(plan.thumbnail.shot, "sea-storm");
  assert.equal(plan.thumbnail.keyframe, null);
  const keyframe = { file: "keyframes/sea-storm-ab12.png", sha256: "1".repeat(64) };
  const drawn = renderPlan(doc, "t", null, { keyframes: { "sea-storm": keyframe } });
  assert.deepEqual(drawn.thumbnail.keyframe, keyframe);
  assert.match(drawn.thumbnail.html, /<img class="thumb-bg" src="https:\/\/video\.local\/work\/keyframes\/sea-storm-ab12\.png" alt=""><div class="thumb-scrim"><\/div>/);
  assert.doesNotMatch(drawn.thumbnail.html, /thumb-art/);
  assert.doesNotMatch(drawn.thumbnail.text, /thumb-bg|object-fit/, "the background CSS is not text the fonts must cover");
  assert.notEqual(drawn.thumbnail.key, plan.thumbnail.key);
  const redrawn = renderPlan(doc, "t", null, { keyframes: { "sea-storm": { ...keyframe, sha256: "2".repeat(64) } } });
  assert.notEqual(redrawn.thumbnail.key, drawn.thumbnail.key);
  assert.equal(renderPlan(doc, "t", null, { keyframes: { "sea-storm": keyframe } }).thumbnail.key, drawn.thumbnail.key);
  // A slides thumbnail is untouched by the option.
  assert.equal(renderPlan(showcase, "t", null, { keyframes: { "sea-storm": keyframe } }).thumbnail.key, renderPlan(showcase, "t").thumbnail.key);
});

test("subtitle strips follow the zh-TW cues: one per distinct text, keyed by what they show, timed in frames", () => {
  const doc = dramaFixture();
  const timeline = estimateTimeline(doc);
  const plan = subtitlePlan(doc, timeline);
  assert.equal(plan.style, "drama");
  assert.ok(plan.cues.length >= timeline.lines.length, "at least one cue per line");
  const byId = new Map(timeline.lines.map((line) => [line.id, line]));
  for (const cue of plan.cues) {
    const line = byId.get(cue.line);
    assert.ok(cue.start_frame >= line.start_frame && cue.end_frame <= line.end_frame && cue.end_frame > cue.start_frame, JSON.stringify(cue));
    assert.ok(plan.strips.some((strip) => strip.key === cue.key), "every cue has its strip");
  }
  plan.cues.forEach((cue, index) => {
    if (index) assert.ok(cue.start_frame >= plan.cues[index - 1].end_frame, "cues never overlap");
  });
  assert.equal(new Set(plan.strips.map((strip) => strip.key)).size, plan.strips.length);
  const html = plan.strips[0].html;
  assert.match(html, /font-size: 56px; font-weight: 600/);
  assert.match(html, /-webkit-text-stroke: 5px #000/);
  assert.doesNotMatch(html, /theme\.css/, "a strip paints no slide background");
  assert.match(html, /body \{ margin: 0; padding: 0; background: transparent; \}/);
  // The same words share a strip; another style or a speaker prefix is another strip.
  assert.equal(stripHtml("你好", "drama"), stripHtml("你好", "drama"));
  assert.notEqual(stripHtml("你好", "drama"), stripHtml("你好", "plain"));
  assert.match(stripHtml("你好 <b>", "drama", "精衛"), /<div class="strip"><span class="speaker">【精衛】<\/span>你好 &lt;b&gt;<\/div>/);
  const prefixed = subtitlePlan({ ...doc, subtitles: { burn_in: true, style: "drama", speaker_prefix: true } }, timeline);
  const jingwei = prefixed.cues.filter((cue) => cue.line === "x9fe");
  assert.match(jingwei[0].text, /^【精衛】父王/);
  assert.ok(prefixed.cues.filter((cue) => cue.line === "k7p2").every((cue) => !cue.text.includes("【")), "the narrator has no prefix");
  const cueKey = (each, id) => each.cues.find((cue) => cue.line === id).key;
  assert.notEqual(cueKey(prefixed, "x9fe"), cueKey(plan, "x9fe"), "a prefixed cue is another strip");
  assert.equal(cueKey(prefixed, "k7p2"), cueKey(plan, "k7p2"), "a narrator's cue is the same strip");
  assert.equal(stripFile("ab12"), "frames/sub-ab12.png");
  assert.equal(BLANK_STRIP, "frames/sub-blank.png");
  assert.match(blankStripHtml(), /background: transparent/);
  assert.doesNotMatch(blankStripHtml(), /class="strip"/);
  assert.match(blankStripKey(), /^[0-9a-f]{16}$/, "the renderer serves pages under hex keys");
  assert.deepEqual(STRIP_SIZE, { width: 1920, height: 260 });
});

test("a glyph a subtitle needs is checked like a slide's", () => {
  const doc = dramaFixture();
  doc.scenes[0].lines[0].text = "很久以前 🤖，發鳩山上住著炎帝最小的女兒。";
  const subtitles = subtitlePlan(doc, estimateTimeline(doc));
  assert.deepEqual(coverageProblems(renderPlan(doc, "t"), bundledCoverage()), [], "the shot itself has no text to draw");
  const problems = coverageProblems(renderPlan(doc, "t"), bundledCoverage(), subtitles);
  assert.equal(problems.length, 1);
  assert.match(problems[0].path, /^subtitle "/);
  assert.match(problems[0].message, /U\+1F916/);
  assert.deepEqual(coverageProblems(renderPlan(dramaFixture(), "t"), bundledCoverage(), subtitlePlan(dramaFixture(), estimateTimeline(dramaFixture()))), []);
});

test("the contact sheet lists every tile from the work directory", () => {
  const html = contactSheetHtml("標題 <x>", [{ file: "frames/a.png", label: "hook · title · 1/1" }]);
  assert.match(html, /<img src="https:\/\/video\.local\/work\/frames\/a\.png"/);
  assert.match(html, /標題 &lt;x&gt;/);
});

test("a compilation renders its chapter cards and outro as stills, numbered by episode, and its thumbnail on the chosen keyframe", () => {
  const doc = compilationDocument({ series: "wuxia", episodes: [{ slug: "wuxia-ep-11", number: 11, title: "重返" }, { slug: "wuxia-ep-12", number: 12, title: "夜探藏經閣" }], voice: { provider: "gemini", name: "Sulafat" } });
  doc.thumbnail.data.headline = "仙門風雲 第二篇";
  assert.deepEqual(renderProblems(doc), []);
  const plan = renderPlan(doc, "t");
  assert.deepEqual(plan.scenes.map((scene) => [scene.id, scene.kind, scene.states.length]), [["card-11", "stills", 1], ["card-12", "stills", 1], ["outro", "stills", 1]]);
  assert.match(plan.scenes[0].states[0].html, /重返/);
  assert.match(plan.scenes[1].states[0].html, /class="number enter"[^>]*>02<span class="of">\/ 02<\/span><\/div>/, "the card counts its place among the cards");
  assert.match(plan.scenes[2].states[0].html, /全集完/);
  assert.deepEqual(coverageProblems(plan, bundledCoverage()), []);
  assert.equal(plan.thumbnail.shot, "thumb");
  assert.equal(plan.thumbnail.keyframe, null, "the worker has not chosen the keyframe yet");
  const keyframe = { file: "keyframes/thumb-source.png", sha256: "3".repeat(64) };
  const drawn = renderPlan(doc, "t", null, { keyframes: { thumb: keyframe } });
  assert.deepEqual(drawn.thumbnail.keyframe, keyframe);
  assert.match(drawn.thumbnail.html, /thumb-bg" src="https:\/\/video\.local\/work\/keyframes\/thumb-source\.png"/);
  const bare = compilationDocument({ series: "wuxia", episodes: [{ slug: "wuxia-ep-1", number: 1 }], chapterCards: false, outro: false });
  assert.deepEqual(renderPlan(bare, "t").scenes, [], "nothing to draw but the thumbnail");
  assert.ok(renderPlan(bare, "t").thumbnail.key);
});

test("an explainer's thumbnail variants are drawn beside A, each on its own keyframe, and checked for glyphs", () => {
  const doc = explainerFixture();
  const keyframes = { flash: { file: "keyframes/flash-1.png", sha256: "aa" }, race: { file: "keyframes/race-1.png", sha256: "bb" } };
  const plan = renderPlan(doc, "t", null, { keyframes });
  assert.deepEqual(plan.thumbnail.variants.map((variant) => [variant.id, variant.file, variant.shot]), [["b", "thumbnail-b.jpg", "flash"], ["c", "thumbnail-c.jpg", "race"]]);
  assert.equal(thumbnailVariantFile("c"), "thumbnail-c.jpg");
  assert.match(plan.thumbnail.variants[0].html, /每 3 秒/);
  assert.match(plan.thumbnail.variants[0].html, /原來如此事務所/, "a variant wears the series look too");
  assert.match(plan.thumbnail.variants[1].html, /keyframes\/race-1\.png/);
  assert.match(plan.thumbnail.variants[1].html, /layout-right/);
  assert.equal(new Set([plan.thumbnail.key, ...plan.thumbnail.variants.map((variant) => variant.key)]).size, 3);
  assert.equal(plan.thumbnail.html, renderPlan({ ...doc, thumbnail: { template: doc.thumbnail.template, data: doc.thumbnail.data } }, "t", null, { keyframes }).thumbnail.html, "A is unchanged by its variants");
  assert.equal(renderPlan(doc, "t", null, { keyframes: { flash: keyframes.flash } }).thumbnail.variants[1].keyframe, null, "C's shot is not drawn yet");
  assert.deepEqual(renderProblems(doc), []);
  const stray = structuredClone(doc);
  stray.thumbnail.variants[1].data.shot = "nowhere";
  assert.deepEqual(renderProblems(stray), [{ path: "thumbnail", message: 'variant c: data.shot "nowhere" is not a shot of this video' }]);
  const odd = structuredClone(doc);
  odd.thumbnail.variants[0].data.headline = "𝕏";
  assert.deepEqual(coverageProblems(renderPlan(odd, "t", null, { keyframes }), bundledCoverage()).map((problem) => problem.path), ["thumbnail variant b"]);
  assert.equal(renderPlan(dramaFixture(), "t").thumbnail.variants, undefined, "no variants: the plan is as it was");
});

test("each caption locale with current thumbnail words gets its own thumbnail on the same picture; the others are notes", () => {
  const doc = explainerFixture();
  const keyframes = { flash: { file: "keyframes/flash-1.png", sha256: "aa" }, race: { file: "keyframes/race-1.png", sha256: "bb" } };
  const words = (prefix) => Object.fromEntries(Object.keys(thumbnailSource(doc)).map((name) => [name, `${prefix} ${name}`]));
  const merged = (thumbnail) => ({ thumbnail, source_hashes: { thumbnail: thumbnailSourceHash(doc) } });
  const translations = { en: merged(words("Why")), ko: merged({ ...words("왜"), headline: "테스트" }), "zh-CN": { thumbnail: words("为何") } };
  const plan = renderPlan(doc, "t", null, { keyframes, translations });
  assert.deepEqual(plan.thumbnail.locales.map((own) => [own.locale, own.file]), [["en", "thumbnails/en.jpg"], ["ko", "thumbnails/ko.jpg"]]);
  const [en] = plan.thumbnail.locales;
  assert.equal(localeThumbnailFile("ja"), "thumbnails/ja.jpg");
  assert.match(en.html, /Why headline/);
  assert.match(en.html, /keyframes\/flash-1\.png/, "the same picture as A");
  assert.match(en.html, /原來如此事務所/, "and the same series look");
  assert.equal(en.hash, localizedThumbnailHash(doc, translations.en));
  assert.notEqual(en.key, plan.thumbnail.key);
  assert.deepEqual(Object.keys(plan.thumbnail.gaps), ["ja", "zh-CN"]);
  assert.match(plan.thumbnail.gaps["zh-CN"], /not merged by i18n-merge/);
  assert.match(plan.thumbnail.gaps.ja, /i18n\/ja\.json has no thumbnail words/);
  // Korean is set in its own font, which has the Hangul the slide font lacks.
  const [, ko] = plan.thumbnail.locales;
  assert.match(ko.html, /<html lang="ko">.*fonts\/noto-sans-kr\/index\.css/);
  assert.doesNotMatch(en.html, /noto-sans-kr/);
  assert.doesNotMatch(plan.thumbnail.html, /noto-sans-kr/, "the video's own thumbnail is as it was");
  assert.deepEqual(coverageProblems(plan, bundledCoverage()), []);
  const localized = localizedThumbnails(plan);
  assert.deepEqual(localized.drawable.map((own) => own.locale), ["en", "ko"]);
  assert.deepEqual(localized.gaps, plan.thumbnail.gaps);
  // Words a locale's fonts cannot draw are a note for that locale, not a failed render.
  const slideFontsOnly = localizedThumbnails(plan, () => bundledCoverage());
  assert.deepEqual(slideFontsOnly.drawable.map((own) => own.locale), ["en"]);
  assert.match(slideFontsOnly.gaps.ko, /no bundled font has .*U\+D14C/);
  // Without translations the plan is as it was.
  assert.equal(renderPlan(doc, "t", null, { keyframes }).thumbnail.locales, undefined);
  assert.deepEqual(localizedThumbnails(renderPlan(doc, "t", null, { keyframes })), { drawable: [], drawn: {}, gaps: {} });
});

test("a Simplified Chinese thumbnail with a Simplified-only form is drawable in its own font", () => {
  const doc = explainerFixture();
  const keyframes = { flash: { file: "keyframes/flash-1.png", sha256: "aa" }, race: { file: "keyframes/race-1.png", sha256: "bb" } };
  const words = Object.fromEntries(Object.keys(thumbnailSource(doc)).map((name) => [name, `写码 佥 ${name}`]));
  const translations = { "zh-CN": { thumbnail: words, source_hashes: { thumbnail: thumbnailSourceHash(doc) } } };
  const plan = renderPlan(doc, "t", null, { keyframes, translations });
  const [sc] = plan.thumbnail.locales;
  assert.equal(sc.locale, "zh-CN");
  assert.match(sc.html, /<html lang="zh-Hans">.*fonts\/noto-sans-sc\/index\.css.*--font:"Noto Sans SC Variable"/);
  assert.deepEqual(localizedThumbnails(plan).drawable.map((own) => own.locale), ["zh-CN"]);
  assert.match(localizedThumbnails(plan, () => bundledCoverage()).gaps["zh-CN"], /U\+4F65/, "the slide fonts alone lack it");
});

test("a thumbnail whose keyframe's bytes changed, went missing or have no recorded hash is refused before anything is drawn; the approved bytes render as before", async () => {
  // A later keyframes take reuses the selected file name (2026-10-07-the-thumbnail-is-drawn-from-a).
  const box = sandbox("fixture-illustrated", "illustrated");
  const docFile = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(docFile, "utf8"));
  assert.equal(doc.thumbnail.data.shot, "podium");
  // Variant B sits on a keyframe of its own.
  doc.thumbnail.variants = [{ data: { headline: "B 的標題", shot: "desk" } }];
  writeFileSync(docFile, JSON.stringify(doc));
  const work = (...parts) => path.join(box.workdir, ...parts);
  mkdirSync(work("keyframes"), { recursive: true });
  const sha = (text) => createHash("sha256").update(text).digest("hex");
  const pictures = { podium: ["keyframes/podium-1.png", "the approved podium"], desk: ["keyframes/desk-1.png", "the approved desk"] };
  const manifest = (overrides = {}) => ({ shots: Object.fromEntries(Object.entries(pictures).map(([shot, [file, bytes]]) => [shot, { file, sha256: sha(bytes), ...(overrides[shot] ?? {}) }])) });
  const approve = () => {
    for (const [file, bytes] of Object.values(pictures)) writeFileSync(work(file), bytes);
    writeFileSync(work("keyframes", "manifest.json"), JSON.stringify(manifest()));
  };
  approve();
  const words = Object.fromEntries(Object.keys(thumbnailSource(doc)).map((name) => [name, `Why ${name}`]));
  const i18n = path.join(box.dir, "i18n", "en.json");
  mkdirSync(path.dirname(i18n), { recursive: true });
  writeFileSync(i18n, JSON.stringify({ thumbnail: words, source_hashes: { thumbnail: thumbnailSourceHash(doc) } }));
  const captures = [];
  let opened = 0;
  let out = "";
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work },
    stdout: { write: (text) => (out += text) },
    stderr: { write: (text) => (out += text) },
    now: () => new Date("2026-10-07T00:00:00Z"),
    openRenderer: async () => {
      opened += 1;
      return {
        // Every drawing differs from the last, so a picture drawn over another shows on disk.
        capture: async (key, html) => {
          captures.push({ key, html });
          return { still: Buffer.from(`picture ${key} #${captures.length}`), frames: [], problems: [] };
        },
        sheet: async () => Buffer.from("sheet"),
        close: async () => {},
      };
    },
  };
  const render = ["render", "--slug", box.slug];
  const languages = [...render, "--thumbnails-only"];
  assert.equal(await main(render, ctx), EXIT.ok, out);
  assert.ok(captures.some(({ html }) => html.includes("https://video.local/work/keyframes/podium-1.png")), "A sits on podium");
  assert.ok(captures.some(({ html }) => html.includes("https://video.local/work/keyframes/desk-1.png")), "B sits on desk");
  const kept = ["frames/manifest.json", "thumbnail.jpg", "thumbnail-b.jpg", "thumbnails/en.jpg"].map((file) => [file, readFileSync(work(file), "utf8")]);
  const refused = (args, label, said) => async () => {
    captures.length = 0;
    opened = 0;
    out = "";
    assert.equal(await main(args, ctx), EXIT.usage, label);
    assert.match(out, said, label);
    assert.deepEqual([captures.length, opened], [0, 0], `${label}: nothing is drawn, and no browser opens`);
    for (const [file, bytes] of kept) assert.equal(readFileSync(work(file), "utf8"), bytes, `${label}: ${file} is as it was`);
  };

  for (const [what, change, said] of [
    ["A's picture drawn over by a later take", () => writeFileSync(work(pictures.podium[0]), "a later take"), /the thumbnail's background keyframes\/podium-1\.png has changed since keyframes\/manifest\.json recorded it; run keyframes again or restore the approved picture/],
    ["A's picture gone", () => rmSync(work(pictures.podium[0])), /the thumbnail's background keyframes\/podium-1\.png is missing; run keyframes again or restore the approved picture/],
    ["A's picture recorded without a hash", () => writeFileSync(work("keyframes", "manifest.json"), JSON.stringify(manifest({ podium: { sha256: "" } }))), /the thumbnail's background keyframes\/podium-1\.png has no hash in keyframes\/manifest\.json/],
  ]) {
    change();
    for (const args of [render, languages]) await refused(args, `${what}: ${args.join(" ")}`, said)();
    approve();
  }

  // Only B's picture changed: the full render, which draws B, refuses; the language thumbnails sit
  // on A's picture and are drawn as before.
  writeFileSync(work(pictures.desk[0]), "a later desk");
  await refused(render, "B's picture drawn over: render", /keyframes\/desk-1\.png has changed/)();
  assert.doesNotMatch(out, /podium/, "A's picture is not blamed");
  captures.length = 0;
  out = "";
  assert.equal(await main(languages, ctx), EXIT.ok, out);
  assert.deepEqual(captures.map(({ html }) => /Why headline/.test(html)), [true], "the en thumbnail, on A's picture");
  approve();

  // A checked alone: no caption locale has a thumbnail of its own.
  rmSync(i18n);
  writeFileSync(work(pictures.podium[0]), "a later take");
  out = "";
  assert.equal(await main(render, ctx), EXIT.usage);
  assert.match(out, /keyframes\/podium-1\.png has changed/);
  approve();

  // The approved bytes back: both commands go on as before.
  writeFileSync(i18n, JSON.stringify({ thumbnail: words, source_hashes: { thumbnail: thumbnailSourceHash(doc) } }));
  out = "";
  assert.equal(await main(render, ctx), EXIT.ok, out);
  assert.equal(await main(languages, ctx), EXIT.ok, out);
});

test("render --thumbnails-only draws the language thumbnails alone, and only over frames rendered for this script", async () => {
  const box = sandbox();
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const words = Object.fromEntries(Object.keys(thumbnailSource(doc)).map((name) => [name, `Why ${name}`]));
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify({ thumbnail: words, source_hashes: { thumbnail: thumbnailSourceHash(doc) } }));
  const captures = [];
  let out = "";
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work },
    stdout: { write: (text) => (out += text) },
    stderr: { write: (text) => (out += text) },
    now: () => new Date("2026-10-02T00:00:00Z"),
    openRenderer: async () => ({
      capture: async (key, html) => {
        captures.push({ key, html });
        return { still: Buffer.from(`jpeg ${key}`), frames: [], problems: [] };
      },
      close: async () => {},
    }),
  };
  const args = ["render", "--slug", box.slug, "--thumbnails-only"];
  const work = (...parts) => path.join(box.workdir, ...parts);

  // No frames yet, or frames of an older script: the full render comes first.
  assert.equal(await main(args, ctx), EXIT.usage);
  mkdirSync(work("frames"), { recursive: true });
  const manifest = { visual_hash: "older", scenes: [{ id: "hook", states: [{ still: "frames/a.png" }] }], thumbnail: "thumbnail.jpg", thumbnail_locale_gaps: { en: "i18n/en.json has no thumbnail words" } };
  writeFileSync(work("frames", "manifest.json"), JSON.stringify(manifest));
  assert.equal(await main(args, ctx), EXIT.usage);
  assert.match(out, /run render without --thumbnails-only first/);
  assert.equal(captures.length, 0);

  // What the approved final.mp4 was cut from, as a full render and assemble leave it.
  manifest.visual_hash = visualHash(doc);
  writeFileSync(work("frames", "manifest.json"), JSON.stringify(manifest));
  const kept = [["thumbnail.jpg", "the approved A"], [path.join("frames", "cache.json"), "{}"], [path.join("frames", "a.png"), "a slide"], ["final.mp4", "the approved cut"]];
  for (const [name, bytes] of kept) writeFileSync(work(name), bytes);
  mkdirSync(work("thumbnails"), { recursive: true });
  writeFileSync(work("thumbnails", "ja.jpg"), "words ja no longer has");
  assert.equal(await main(args, ctx), EXIT.ok);
  assert.deepEqual(captures.map(({ html }) => /Why headline/.test(html)), [true], "one picture: the en thumbnail");
  assert.equal(readFileSync(work("thumbnails", "en.jpg"), "utf8"), `jpeg ${captures[0].key}`);
  assert.ok(!existsSync(work("thumbnails", "ja.jpg")), "a locale without current words keeps no older picture");
  const { thumbnail_locales: drawn, thumbnail_locale_gaps: gaps, ...rest } = JSON.parse(readFileSync(work("frames", "manifest.json"), "utf8"));
  const before = { ...manifest };
  delete before.thumbnail_locale_gaps;
  assert.deepEqual(rest, before, "visual_hash and the scenes are as they were");
  assert.deepEqual(Object.keys(drawn), ["en"]);
  assert.deepEqual(Object.keys(gaps), ["ja", "ko", "zh-CN"]);
  for (const [name, bytes] of kept) assert.equal(readFileSync(work(name), "utf8"), bytes, `${name} untouched`);
  assert.ok(!existsSync(work("contact-sheet.png")), "no contact sheet is drawn");
  assert.match(out, /1 language thumbnails drawn .*; the frames are as they were/);
});

test("a Japanese thumbnail is set in Noto Sans JP, so its kanji take the Japanese forms", () => {
  const doc = explainerFixture();
  const keyframes = { flash: { file: "keyframes/flash-1.png", sha256: "aa" }, race: { file: "keyframes/race-1.png", sha256: "bb" } };
  const words = Object.fromEntries(Object.keys(thumbnailSource(doc)).map((name) => [name, `直す 骨 写す 侭 ${name}`]));
  const translations = { ja: { thumbnail: words, source_hashes: { thumbnail: thumbnailSourceHash(doc) } } };
  const plan = renderPlan(doc, "t", null, { keyframes, translations });
  const [ja] = plan.thumbnail.locales;
  assert.equal(ja.locale, "ja");
  assert.match(ja.html, /<html lang="ja">.*fonts\/noto-sans-jp\/index\.css.*--font:"Noto Sans JP Variable","Noto Sans TC Variable",sans-serif/);
  assert.doesNotMatch(plan.thumbnail.html, /noto-sans-jp|lang="ja"/, "the video's own thumbnail is as it was");
  assert.deepEqual(localizedThumbnails(plan).drawable.map((own) => own.locale), ["ja"]);
  assert.match(localizedThumbnails(plan, () => bundledCoverage()).gaps.ja, /U\+4FAD/, "the slide fonts alone lack it");
});

test("a compilation whose thumbnail source changed is told to plan its metadata again, which keyframes cannot do", async () => {
  // keyframes refuses a compilation: the worker copies an approved episode keyframe to
  // THUMB_SOURCE when it plans the metadata (2026-10-07-render-tells-a-compilation-to-run).
  const box = compilationSandbox({ planned: true, rendered: true });
  let out = "";
  let opened = 0;
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work },
    stdout: { write: (text) => (out += text) },
    stderr: { write: (text) => (out += text) },
    now: () => new Date("2026-10-07T00:00:00Z"),
    openRenderer: async () => {
      opened += 1;
      return { capture: async () => ({ still: Buffer.from("picture"), frames: [], problems: [] }), sheet: async () => Buffer.from("sheet"), close: async () => {} };
    },
  };
  // An English thumbnail of its own, which --thumbnails-only draws on the same source.
  const words = Object.fromEntries(Object.keys(thumbnailSource(box.doc)).map((name) => [name, `Why ${name}`]));
  const i18n = path.join(box.dir, "i18n", "en.json");
  mkdirSync(path.dirname(i18n), { recursive: true });
  writeFileSync(i18n, JSON.stringify({ thumbnail: words, source_hashes: { thumbnail: thumbnailSourceHash(box.doc) } }));
  // The copy as the worker records it: the episode keyframe it was taken from, and its hash.
  const approved = readFileSync(path.join(box.workdir, THUMB_SOURCE));
  const manifestFile = path.join(box.workdir, "keyframes", "manifest.json");
  writeFileSync(manifestFile, JSON.stringify({ shots: { thumb: { file: THUMB_SOURCE, sha256: createHash("sha256").update(approved).digest("hex"), source: { episode: "wuxia-ep-1", shot: "s3" } } } }));
  writeFileSync(path.join(box.workdir, THUMB_SOURCE), "a picture nobody approved");
  const languages = ["render", "--slug", box.slug, "--thumbnails-only"];
  for (const args of [["render", "--slug", box.slug], languages]) {
    out = "";
    assert.equal(await main(args, ctx), EXIT.usage, args.join(" "));
    // Restoring the approved picture first: free, and nothing approved changes.
    assert.match(out, /the thumbnail's background keyframes\/thumb-source\.png has changed since keyframes\/manifest\.json recorded it; copy the episode keyframe it was taken from \(wuxia-ep-1, shot s3\) back to keyframes\/thumb-source\.png, if that still holds the hash under shots\.thumb/, args.join(" "));
    // Planning again only when that keyframe changed too, with its translations and its cost.
    assert.match(out, /otherwise delete keyframes\/manifest\.json and the compilation's i18n\/\*\.json so the worker plans and translates its metadata again: a new planner call rewrites the title/, args.join(" "));
    assert.doesNotMatch(out, /run keyframes again/, `${args.join(" ")}: advice a compilation cannot follow`);
  }
  assert.equal(opened, 0, "nothing is drawn");
  // The free remedy works: the approved bytes back, the language thumbnail draws.
  writeFileSync(path.join(box.workdir, THUMB_SOURCE), approved);
  out = "";
  assert.equal(await main(languages, ctx), EXIT.ok, out);
  assert.ok(opened > 0);
});
