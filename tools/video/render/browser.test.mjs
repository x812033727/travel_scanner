import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { ORIGIN, slideHtml } from "../templates/templates.mjs";
import { openRenderer } from "./browser.mjs";

// This exercises the actual layout engine. Opt in on a host with Chromium installed:
// VIDEO_RENDER_BROWSER_TESTS=1 VIDEO_BROWSER_CHANNEL=msedge node --test tools/video/render/browser.test.mjs
const browserTests = process.env.VIDEO_RENDER_BROWSER_TESTS === "1";
const root = fileURLToPath(new URL("../../../", import.meta.url));
const digest = (buffer) => createHash("sha256").update(buffer).digest("hex");
const style = (html, css) => html.replace("</head>", `<style>${css}</style></head>`);
const content = (html, body) => html.replace(/<main[^>]*>.*?<\/main>/s, `<main class="content">${body}</main>`);

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
