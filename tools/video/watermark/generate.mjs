#!/usr/bin/env node
// Draw the channel mark (docs/videos/WATERMARK.md) as the two PNGs a version of it is made of:
// `long.png` for a 1920x1080 cut and `shorts.png` for a 1080x1920 one.
//
//   node tools/video/watermark/generate.mjs --out <dir> [--channel msedge]
//
// The PNGs in tools/video/watermark/<version>/ are what the videos carry, byte for byte: a
// version is never drawn again, because a browser on another machine antialiases a little
// differently and every pinned video would then name bytes that no longer exist. This script is
// how a version was drawn and how the next one is: write to a directory of your own, look at the
// pictures, then copy them into a NEW version directory and register their size and SHA-256 in
// tools/video/core/watermark.mjs (the script prints both).
//
// The mark is opaque: cream letters with a dark outline, the way the burned-in subtitles are
// drawn (render/subtitles.mjs), so it reads on a dark slide and on a bright picture alike, and a
// frame that already carries it can be laid over another that does (a dissolve, a Short's loop)
// without the mark getting brighter where the two overlap.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { ROOT } from "../core/paths.mjs";
import { LAUNCH_ARGS, resolveRequest } from "../render/browser.mjs";
import { SLIDE_FAMILY } from "../render/fonts.mjs";
import { ORIGIN } from "../templates/templates.mjs";

export const MARK_NAME = "Mokaair";
export const MARK_HANDLE = "YouTube @Mokaair";
// The two lines' sizes and outlines, in pixels of the frame the PNG is laid on. A Short is seen
// on a phone at about a third of its pixels, so its mark is drawn larger.
export const MARK_STYLES = {
  long: { name: 36, nameStroke: 4, handle: 20, handleStroke: 3 },
  shorts: { name: 46, nameStroke: 5, handle: 26, handleStroke: 4 },
};
const FILL = "#f7f1e8";
const OUTLINE = "#0e2627";

/** The mark as a page: two lines set flush right on a transparent ground. */
export function markHtml(shape) {
  const style = MARK_STYLES[shape];
  if (!style) throw new Error(`no mark is drawn for "${shape}"`);
  const line = (size, stroke, weight) => `font-size:${size}px;font-weight:${weight};-webkit-text-stroke:${stroke}px ${OUTLINE}`;
  return [
    '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">',
    `<link rel="stylesheet" href="${ORIGIN}/fonts/noto-sans-tc/index.css">`,
    "<style>",
    "* { box-sizing: border-box; }",
    "html, body { margin: 0; padding: 0; background: transparent; }",
    // The outline is centred on the glyph's edge and painted under the fill, so half of it shows;
    // the padding keeps that half inside the picture.
    `.mark { position: absolute; left: 0; top: 0; display: inline-flex; flex-direction: column; align-items: flex-end; padding: 4px 6px; font-family: "${SLIDE_FAMILY}", sans-serif; color: ${FILL}; paint-order: stroke fill; -webkit-font-smoothing: antialiased; text-rendering: geometricPrecision; white-space: nowrap; }`,
    `.name { ${line(style.name, style.nameStroke, 800)}; line-height: 1.1; letter-spacing: 0.01em; }`,
    `.handle { ${line(style.handle, style.handleStroke, 700)}; line-height: 1.25; letter-spacing: 0.02em; }`,
    "</style></head><body>",
    `<div class="mark"><span class="name">${MARK_NAME}</span><span class="handle">${MARK_HANDLE}</span></div>`,
    "</body></html>",
  ].join("");
}

const even = (value) => 2 * Math.ceil(value / 2);

/** Draw both shapes: { long: { png, width, height }, shorts: ... }. */
export async function drawMarks({ channel, root = ROOT } = {}) {
  const { chromium } = await import("@playwright/test");
  const browser = await chromium.launch({ headless: true, args: LAUNCH_ARGS, ...(channel ? { channel } : {}) });
  try {
    const context = await browser.newContext({ viewport: { width: 800, height: 400 }, deviceScaleFactor: 1 });
    const pages = new Map();
    await context.route("**/*", async (route) => {
      const target = resolveRequest(route.request().url(), { root, workdir: null, pages });
      if (!target) return route.abort();
      if (target.body !== undefined) return route.fulfill({ status: 200, contentType: target.type, body: target.body });
      if (!existsSync(target.file)) return route.fulfill({ status: 404, body: "" });
      const type = target.file.endsWith(".css") ? "text/css" : "font/woff2";
      return route.fulfill({ status: 200, contentType: type, body: readFileSync(target.file) });
    });
    const page = await context.newPage();
    const marks = {};
    for (const [index, shape] of Object.keys(MARK_STYLES).entries()) {
      const key = `a${index}`;
      pages.set(key, markHtml(shape));
      await page.goto(`${ORIGIN}/state/${key}.html`, { waitUntil: "load" });
      await page.evaluate(async (text) => {
        for (const weight of [700, 800]) await document.fonts.load(`${weight} 40px "Noto Sans TC Variable"`, text);
        await document.fonts.ready;
      }, `${MARK_NAME}${MARK_HANDLE}`);
      const loaded = await page.evaluate((text) => [700, 800].every((weight) => document.fonts.check(`${weight} 40px "Noto Sans TC Variable"`, text)), `${MARK_NAME}${MARK_HANDLE}`);
      if (!loaded) throw new Error("the bundled font did not load; run npm ci in this checkout");
      const box = await page.evaluate(() => {
        const rect = document.querySelector(".mark").getBoundingClientRect();
        return { width: rect.width, height: rect.height };
      });
      // Even on both sides: the mark is laid over 4:2:0 video, whose colour is sampled every two pixels.
      const width = even(box.width);
      const height = even(box.height);
      await page.evaluate(({ width, height }) => {
        const mark = document.querySelector(".mark");
        mark.style.width = `${width}px`;
        mark.style.height = `${height}px`;
      }, { width, height });
      const png = await page.screenshot({ type: "png", omitBackground: true, clip: { x: 0, y: 0, width, height } });
      marks[shape] = { png, width, height };
      pages.delete(key);
    }
    return marks;
  } finally {
    await browser.close();
  }
}

async function main() {
  const { values } = parseArgs({ options: { out: { type: "string" }, channel: { type: "string" } }, strict: true });
  if (!values.out) {
    process.stderr.write("usage: generate.mjs --out <dir> [--channel msedge]\n");
    return 2;
  }
  const out = path.resolve(values.out);
  const marks = await drawMarks({ channel: values.channel ?? process.env.VIDEO_BROWSER_CHANNEL });
  mkdirSync(out, { recursive: true });
  for (const [shape, mark] of Object.entries(marks)) {
    const file = path.join(out, `${shape}.png`);
    writeFileSync(file, mark.png);
    process.stdout.write(`${file}: ${mark.width}x${mark.height}, sha256 ${createHash("sha256").update(mark.png).digest("hex")}\n`);
  }
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await main();
}
