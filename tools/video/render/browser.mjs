// Headless Chromium that draws slide states into PNG frames.
//
// Everything a slide loads comes from a fake origin served from disk: the page, the theme, the
// fonts from node_modules, and images from the repository's asset roots. Every other request is
// refused and reported, so a slide can never depend on the network or on what a machine has
// installed. Entrance animations are frozen with the Web Animations API at exact 1/30 s steps,
// so a transition renders the same frames on every run.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

import { ASSET_ROOTS, ORIGIN, SIZE } from "../templates/templates.mjs";
import { fontDir } from "./fonts.mjs";
import { THEME_FILE } from "./plan.mjs";

export const FPS = 30;

/** A browser that is missing or will not start: the "tool missing" exit, not a crash. */
export class RendererError extends Error {}
// The longest entrance the renderer captures frame by frame; the theme's stay well under it.
export const MAX_TRANSITION_FRAMES = 18;

const TYPES = { ".css": "text/css", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".html": "text/html" };

/** Map a URL on the fake origin to a file, or null when nothing may be served for it. */
export function resolveRequest(url, { root, workdir, pages }) {
  if (!url.startsWith(`${ORIGIN}/`)) return null;
  const pathname = decodeURIComponent(new URL(url).pathname);
  if (pathname.includes("..")) return null;
  const page = /^\/state\/([0-9a-f]+)\.html$/.exec(pathname);
  if (page) return pages.has(page[1]) ? { body: pages.get(page[1]), type: TYPES[".html"] } : null;
  if (pathname === "/theme.css") return { file: THEME_FILE };
  const font = /^\/fonts\/(noto-sans-tc|jetbrains-mono)\/(.+)$/.exec(pathname);
  if (font) return { file: path.join(fontDir(font[1]), font[2]) };
  if (pathname.startsWith("/repo/")) {
    const relative = pathname.slice("/repo/".length);
    return ASSET_ROOTS.some((prefix) => relative.startsWith(prefix)) ? { file: path.join(root, relative) } : null;
  }
  if (workdir && pathname.startsWith("/work/")) return { file: path.join(workdir, pathname.slice("/work/".length)) };
  return null;
}

// Runs in the page: shrink each .fit element's type until it fits, to at most 40% smaller.
// CJK fonts draw taller than a tight line-height, so even one line "overflows" by a fraction of
// the font size; only more than 0.4 em (a line that does not fit) counts vertically.
function fitText() {
  const overflows = (element) => {
    const size = parseFloat(getComputedStyle(element).fontSize);
    return element.scrollHeight - element.clientHeight > size * 0.4 || element.scrollWidth - element.clientWidth > 1;
  };
  for (const element of document.querySelectorAll(".fit")) {
    const start = parseFloat(getComputedStyle(element).fontSize);
    let size = start;
    while (overflows(element) && size > start * 0.6) {
      size -= 2;
      element.style.fontSize = `${size}px`;
    }
    element.dataset.overflow = overflows(element) ? "yes" : "";
  }
}

// Runs in the page: what still does not fit once fitText has done what it can.
function layoutProblems(fontFamily) {
  const problems = [];
  const excerpt = (element) => element.textContent.trim().replace(/\s+/g, " ").slice(0, 30);
  for (const element of document.querySelectorAll(".fit")) {
    if (element.closest("[data-hidden]")) continue;
    if (element.dataset.overflow) problems.push(`text does not fit even at 60% size: "${excerpt(element)}"`);
  }
  for (const box of document.querySelectorAll(".content, .thumb")) {
    if (box.scrollHeight > box.clientHeight + 1) problems.push(`the slide's content is ${box.scrollHeight - box.clientHeight}px taller than its area`);
    if (box.scrollWidth > box.clientWidth + 1) problems.push(`the slide's content is ${box.scrollWidth - box.clientWidth}px wider than its area`);
  }
  for (const image of document.images) if (!image.complete || image.naturalWidth === 0) problems.push(`image did not load: ${image.getAttribute("src")}`);
  // Code is set in the monospace font, so Noto's Latin subsets may rightly never load for it.
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let text = "";
  while (walker.nextNode()) if (!walker.currentNode.parentElement.closest("pre")) text += walker.currentNode.nodeValue;
  if (text.trim() && !document.fonts.check(`40px "${fontFamily}"`, text)) problems.push("the slide font did not load for all of its text");
  return problems;
}

// Runs in the page: pause every animation and report how long the longest one runs.
function pauseAnimations() {
  let end = 0;
  for (const animation of document.getAnimations()) {
    animation.pause();
    const timing = animation.effect.getComputedTiming();
    end = Math.max(end, timing.endTime);
  }
  return end;
}

function seekAnimations(time) {
  for (const animation of document.getAnimations()) animation.currentTime = time;
}

/**
 * Open the renderer. `channel` picks an installed browser (e.g. "msedge", which runs natively on
 * Windows ARM64 where Playwright's bundled Chromium is emulated); the default is the bundled one.
 */
export async function openRenderer({ root, workdir, channel }) {
  const { chromium } = await import("@playwright/test");
  let browser;
  try {
    browser = await chromium.launch({ headless: true, ...(channel ? { channel } : {}) });
  } catch (error) {
    const hint = channel
      ? `the "${channel}" browser could not start`
      : "Playwright's Chromium for this version is not installed: run `npx playwright install chromium`, or pass --channel msedge (set VIDEO_BROWSER_CHANNEL=msedge to make it the default)";
    throw new RendererError(`${hint}\n${String(error.message).split("\n")[0]}`);
  }
  const context = await browser.newContext({ viewport: SIZE, deviceScaleFactor: 1 });
  const pages = new Map();
  const refused = [];
  await context.route("**/*", async (route) => {
    const url = route.request().url();
    const target = resolveRequest(url, { root, workdir, pages });
    if (!target) {
      refused.push(url);
      return url.startsWith(ORIGIN) ? route.fulfill({ status: 404, body: "" }) : route.abort();
    }
    if (target.body !== undefined) return route.fulfill({ status: 200, contentType: target.type, body: target.body });
    if (!existsSync(target.file)) {
      refused.push(url);
      return route.fulfill({ status: 404, body: "" });
    }
    return route.fulfill({ status: 200, contentType: TYPES[path.extname(target.file).toLowerCase()] ?? "application/octet-stream", body: readFileSync(target.file) });
  });
  const page = await context.newPage();

  async function load(key, html, size) {
    pages.set(key, html);
    await page.setViewportSize(size);
    await page.goto(`${ORIGIN}/state/${key}.html`, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(fitText);
    const problems = await page.evaluate(layoutProblems, "Noto Sans TC Variable");
    pages.delete(key);
    return problems;
  }

  let sheets = 0;

  return {
    /**
     * Draw one state. With `transition`, also every 1/30 s of its entrance animations, frame 0
     * being the moment before anything has moved. Returns PNG buffers and layout problems.
     */
    async capture(key, html, { size = SIZE, transition = false, type = "png", quality } = {}) {
      const refusedBefore = refused.length;
      const problems = await load(key, html, size);
      const end = await page.evaluate(pauseAnimations);
      const frames = [];
      if (transition && end > 0) {
        const count = Math.min(Math.ceil(end / (1000 / FPS)), MAX_TRANSITION_FRAMES);
        for (let index = 0; index < count; index++) {
          await page.evaluate(seekAnimations, (index * 1000) / FPS);
          frames.push(await page.screenshot({ type, quality }));
        }
      }
      await page.evaluate(seekAnimations, end + 1);
      const still = await page.screenshot({ type, quality });
      for (const url of refused.slice(refusedBefore)) problems.push(`refused a request for ${url}`);
      return { frames, still, problems };
    },
    /** A full-page screenshot of arbitrary HTML, e.g. the contact sheet. */
    async sheet(html, width) {
      const key = `ff${(sheets++).toString(16)}`;
      pages.set(key, html);
      await page.setViewportSize({ width, height: 600 });
      await page.goto(`${ORIGIN}/state/${key}.html`, { waitUntil: "load" });
      await page.evaluate(() => Promise.all([...document.images].map((image) => (image.complete ? null : new Promise((resolve) => (image.onload = image.onerror = resolve))))));
      pages.delete(key);
      return page.screenshot({ type: "png", fullPage: true });
    },
    async close() {
      await browser.close();
    },
  };
}
