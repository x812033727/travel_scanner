// The Playwright side of a screencast: a browser on the public web, adapted to the runner's driver.
//
// Unlike the slide renderer (tools/video/render/browser.mjs), which refuses every request, this
// browser loads the pages the steps name, so every request carries the editorial User-Agent and
// nothing else about who runs it. It starts with no cookies and no storage. `profile` points it at
// a persistent browser profile instead, for a page that needs the owner signed in: the owner signs
// in to that profile himself, and agents never pass one (.agents/skills/youtube-video/SKILL.md
// rule 4: whatever such a page shows that is personal must be masked in the steps).
import { SCALE, USER_AGENT, VIEWPORT } from "./steps.mjs";

/** A browser that is missing or will not start: the "tool missing" exit. */
export class BrowserMissing extends Error {}

const NAVIGATION_TIMEOUT = 30_000;
const STEP_TIMEOUT = 10_000;
// A control a page renders after its own session check (the site's login link) has taken over 10 s.
const WAIT_TIMEOUT = 25_000;
const LOAD_GRACE = 15_000;

// Runs in the page: draw the masks as opaque striped blocks above everything else.
function drawMasks(rects) {
  document.getElementById("__mokaair_masks")?.remove();
  if (!rects.length) return;
  const layer = document.createElement("div");
  layer.id = "__mokaair_masks";
  layer.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:2147483647";
  for (const rect of rects) {
    const block = document.createElement("div");
    block.style.cssText =
      `position:absolute;left:${rect.x}px;top:${rect.y}px;width:${rect.w}px;height:${rect.h}px;border-radius:4px;` +
      "background:repeating-linear-gradient(135deg,#2a3236 0 10px,#323b40 10px 20px)";
    layer.appendChild(block);
  }
  document.documentElement.appendChild(layer);
}

// Runs in the page: how many password fields hold a value (an autofilled profile could).
function filledPasswords() {
  return [...document.querySelectorAll("input[type=password]")].filter((input) => input.value).length;
}

// Runs on the element: what kind of field it is.
function describeField(element) {
  const tag = element.tagName.toLowerCase();
  const editable = element.isContentEditable || tag === "textarea" || (tag === "input" && !element.readOnly && !element.disabled);
  return { tag, type: tag === "input" ? element.type : "", autocomplete: element.getAttribute("autocomplete") ?? "", editable };
}

// A page whose last image or tracker takes long to arrive is still captured: the steps' own
// `wait` names what must be there, and this only gives the rest a fair chance to finish.
async function settle(page) {
  await page.waitForLoadState("domcontentloaded", { timeout: NAVIGATION_TIMEOUT });
  await page.waitForLoadState("load", { timeout: LOAD_GRACE }).catch(() => {});
  await page.evaluate(() => document.fonts.ready);
}

/** The runner's driver over one Playwright page. */
export function pageDriver(page) {
  // Only what is on screen counts: sites keep hidden copies of their controls for other widths
  // (a phone menu's login link beside the desktop one), and a tutorial points at what is seen.
  const shown = (selector) => page.locator(selector).filter({ visible: true });
  const one = (selector) => shown(selector).first();
  return {
    async goto(url) {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: NAVIGATION_TIMEOUT });
      await settle(page);
    },
    waitFor: (selector) => one(selector).waitFor({ state: "visible", timeout: WAIT_TIMEOUT }),
    waitMs: (ms) => page.waitForTimeout(ms),
    async click(selector) {
      // Strict: a selector that matches two elements is ambiguous, and a tutorial must click the one it shows.
      await shown(selector).click({ timeout: STEP_TIMEOUT });
      await settle(page);
    },
    fill: (selector, value) => shown(selector).fill(value, { timeout: STEP_TIMEOUT }),
    async field(selector) {
      const locator = shown(selector);
      const matches = await locator.count();
      if (matches !== 1) return { matches };
      return { matches, ...(await locator.evaluate(describeField)) };
    },
    async boxes(selector, { scroll = false } = {}) {
      const locator = shown(selector);
      if (scroll) {
        if ((await locator.count()) === 0) return [];
        await one(selector).scrollIntoViewIfNeeded({ timeout: STEP_TIMEOUT });
      }
      const boxes = [];
      for (const each of await locator.all()) {
        const box = await each.boundingBox();
        if (box) boxes.push({ x: box.x, y: box.y, w: box.width, h: box.height });
      }
      return boxes;
    },
    setMasks: (rects) => page.evaluate(drawMasks, rects),
    secretsShown: () => page.evaluate(filledPasswords),
    screenshot: () => page.screenshot({ type: "png", animations: "disabled", caret: "hide", scale: "device" }),
    url: () => page.url(),
  };
}

/**
 * Open a browser for screencast steps. `channel` picks an installed browser ("msedge" runs
 * natively on Windows ARM64); `profile` is a persistent profile directory, or nothing.
 * Returns { newDriver(), close() }: one fresh page per scene.
 */
export async function openScreencastBrowser({ channel = undefined, profile = undefined } = {}) {
  const { chromium } = await import("@playwright/test");
  const options = {
    headless: true,
    ...(channel ? { channel } : {}),
  };
  const contextOptions = {
    viewport: VIEWPORT,
    deviceScaleFactor: SCALE,
    userAgent: USER_AGENT,
    locale: "zh-TW",
    timezoneId: "Asia/Taipei",
    colorScheme: "light",
    reducedMotion: "reduce",
    serviceWorkers: "block",
    acceptDownloads: false,
  };
  let browser = null;
  let context;
  try {
    if (profile) {
      context = await chromium.launchPersistentContext(profile, { ...options, ...contextOptions });
    } else {
      browser = await chromium.launch(options);
      context = await browser.newContext(contextOptions);
    }
  } catch (error) {
    const hint = channel ? `the "${channel}" browser could not start` : "Playwright's Chromium is not installed: run `npx playwright install chromium`, or pass --channel msedge";
    throw new BrowserMissing(`${hint}\n${String(error.message).split("\n")[0]}`);
  }
  // Only the web: no file:, data: navigations or other schemes from a page the steps open.
  await context.route("**/*", (route) => (/^https?:/.test(route.request().url()) ? route.continue() : route.abort()));
  const pages = [];
  return {
    async newDriver() {
      const page = await context.newPage();
      pages.push(page);
      return pageDriver(page);
    },
    async close() {
      for (const page of pages) await page.close().catch(() => {});
      await context.close();
      if (browser) await browser.close();
    },
  };
}
