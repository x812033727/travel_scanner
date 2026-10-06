import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { ORIGIN, slideHtml } from "../templates/templates.mjs";
import { FPS, LAUNCH_ARGS, MAX_TRANSITION_FRAMES, openRenderer, pauseAnimations, seekAnimations } from "./browser.mjs";

// This exercises the actual layout engine. Opt in on a host with Chromium installed:
// VIDEO_RENDER_BROWSER_TESTS=1 VIDEO_BROWSER_CHANNEL=msedge node --test tools/video/render/browser.test.mjs
const browserTests = process.env.VIDEO_RENDER_BROWSER_TESTS === "1";
const root = fileURLToPath(new URL("../../../", import.meta.url));
const digest = (buffer) => createHash("sha256").update(buffer).digest("hex");
const style = (html, css) => html.replace("</head>", `<style>${css}</style></head>`);
const content = (html, body) => html.replace(/<main[^>]*>.*?<\/main>/s, `<main class="content">${body}</main>`);

test("the page functions that freeze an entrance are shared with the Shorts renderer: self-contained, sent into a page as they are", () => {
  // shorts/build.mjs sends them into its own card page with page.evaluate, so neither may
  // reach for anything of this module: only the page's document and animation frames.
  assert.equal(typeof pauseAnimations, "function");
  assert.equal(typeof seekAnimations, "function");
  assert.equal(pauseAnimations.length, 0);
  assert.equal(seekAnimations.length, 1);
  assert.match(String(pauseAnimations), /document\.getAnimations\(\)/);
  assert.match(String(pauseAnimations), /animation\.pause\(\)/);
  assert.match(String(pauseAnimations), /getComputedTiming\(\)/);
  assert.match(String(seekAnimations), /animation\.currentTime = time/);
  assert.equal((String(seekAnimations).match(/requestAnimationFrame/g) ?? []).length, 2, "two frames: the first draws the seek, the second starts after it");
  for (const fn of [pauseAnimations, seekAnimations]) assert.ok(!/\b(?:FPS|ORIGIN|SIZE|import|require)\b/.test(String(fn)), "nothing of the module");
  assert.equal(FPS, 30);
  assert.equal(MAX_TRANSITION_FRAMES, 18);
  assert.deepEqual(LAUNCH_ARGS, ["--disable-gpu", "--disable-threaded-animation"]);
});

test("in a page, the functions pause every animation at the time asked and resolve once that frame is drawn", {
  skip: browserTests ? false : "set VIDEO_RENDER_BROWSER_TESTS=1 to run the actual browser regression",
}, async () => {
  const { chromium } = await import("@playwright/test");
  const browser = await chromium.launch({ headless: true, args: LAUNCH_ARGS, ...(process.env.VIDEO_BROWSER_CHANNEL ? { channel: process.env.VIDEO_BROWSER_CHANNEL } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 400, height: 200 }, deviceScaleFactor: 1 });
    await page.setContent('<style>body{margin:0;background:#123}@keyframes rise{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}.in{animation:rise 240ms linear both;animation-delay:calc(var(--i,0)*40ms);animation-play-state:paused}h1{color:#fff;font:40px sans-serif;margin:20px}</style><h1 class="in" style="--i:0">Headline</h1><h1 class="in" style="--i:4">Row</h1>');
    assert.equal(await page.evaluate(pauseAnimations), 400, "the end of the longest animation, delay and duration");
    assert.deepEqual(await page.evaluate(() => document.getAnimations().map((animation) => animation.playState)), ["paused", "paused"]);
    await page.evaluate(seekAnimations, 401);
    const still = digest(await page.screenshot());
    await page.evaluate(seekAnimations, 0);
    const first = digest(await page.screenshot());
    assert.notEqual(first, still, "frame 0 is the moment before anything has moved");
    await page.evaluate(seekAnimations, 200);
    assert.deepEqual(await page.evaluate(() => document.getAnimations().map((animation) => animation.currentTime)), [200, 200]);
    const mid = digest(await page.screenshot());
    assert.notEqual(mid, first);
    assert.notEqual(mid, still);
    await page.evaluate(seekAnimations, 0);
    await page.evaluate(seekAnimations, 200);
    assert.equal(digest(await page.screenshot()), mid, "a seek draws the same frame every time");
  } finally {
    await browser.close();
  }
});

const diagram = slideHtml(
  { template: "diagram", data: { svg: "docs/videos/fixture.svg" } },
  {
    first: true, reveal: 0, previousReveal: 0, totalReveals: 0,
    svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><rect x="0" y="0" width="1600" height="900" fill="#0d6b68"/></svg>',
  },
);

test("settled layout passes an entering diagram while genuine failures still fail", {
  skip: browserTests ? false : "set VIDEO_RENDER_BROWSER_TESTS=1 to run the actual browser regression",
}, async (t) => {
  const renderer = await openRenderer({ root, channel: process.env.VIDEO_BROWSER_CHANNEL });
  try {
    await t.test("a full-height diagram is checked at its final position, with its entrance preserved", async () => {
      // Hold the real theme's entrance at time zero, removing the wall-clock race from the
      // reproduction. At this time the paper is 28px below its final position. The renderer
      // must seek it explicitly both for transitions and before judging the final layout.
      const html = style(diagram, ".enter{animation-play-state:paused}");
      const captured = await renderer.capture("aa01", html, { transition: true });
      assert.deepEqual(captured.problems, []);
      assert.equal(captured.frames.length, 12, "the 300ms entrance and 70ms delay are still drawn");
      assert.notEqual(digest(captured.frames[0]), digest(captured.still), "the entrance is not replaced by a still");
      const again = await renderer.capture("aa02", html, { transition: true });
      assert.deepEqual(again.problems, []);
      assert.equal(digest(again.still), digest(captured.still));
      assert.deepEqual(again.frames.map(digest), captured.frames.map(digest));
    });

    await t.test("a genuinely oversized paper still fails the unchanged layout limit", async () => {
      const html = style(diagram, ".enter{animation-play-state:paused}.paper{min-height:874px}");
      const captured = await renderer.capture("aa03", html);
      // The 874px paper is centred in the 778px frame, leaving 48px outside at each edge.
      assert.ok(captured.problems.some((problem) => /48px taller than its area/.test(problem)), captured.problems.join("\n"));
    });

    await t.test("text that still does not fit after shrinking remains an error", async () => {
      const html = content(diagram, '<div class="fit" style="width:50px;height:30px;white-space:nowrap;overflow:hidden;font-size:40px">This text cannot fit in fifty pixels.</div>');
      const captured = await renderer.capture("aa04", html);
      assert.ok(captured.problems.some((problem) => /text does not fit even at 60% size/.test(problem)), captured.problems.join("\n"));
    });

    await t.test("a missing image is still reported", async () => {
      const html = content(diagram, `<img src="${ORIGIN}/repo/docs/videos/missing-render-test-fixture.png" alt="">`);
      const captured = await renderer.capture("aa05", html);
      assert.ok(captured.problems.some((problem) => /image did not load:/.test(problem)), captured.problems.join("\n"));
      assert.ok(captured.problems.some((problem) => /refused a request/.test(problem)), captured.problems.join("\n"));
    });

    await t.test("an unloadable font face is still reported", async () => {
      const html = style(diagram, `@font-face{font-family:"Missing Fixture Font";src:url("${ORIGIN}/fonts/noto-sans-tc/files/missing-render-test-fixture.woff2")} :root{--font:"Missing Fixture Font"}`);
      const captured = await renderer.capture("aa06", html);
      assert.ok(captured.problems.some((problem) => /a slide font face would not load:/.test(problem)), captured.problems.join("\n"));
    });
  } finally {
    await renderer.close();
  }
});
