// Drive a page through a screencast scene's steps and keep a still at every `capture`.
//
// The browser sits behind a small driver interface (browser.mjs adapts Playwright to it), so the
// rules here — masks drawn before every still, the cursor target measured before the click it
// points at, no typing into a secret field, no still of a filled password — are tested with a
// fake page and no browser:
//
//   goto(url) · waitFor(selector) · waitMs(ms) · click(selector) · fill(selector, value)
//   field(selector) -> { matches, type, autocomplete, editable }
//   boxes(selector, { scroll }) -> [{ x, y, w, h }] in page pixels, every visible match (maybe off the page)
//   setMasks([{ x, y, w, h }]) · secretsShown() -> number · screenshot() -> Buffer · url() -> string
import { capturePlan, fieldProblem, publicUrl, selectorProblem, stepProblems, valueProblem, VIEWPORT } from "./steps.mjs";

/** A step that cannot be done as written: a missing element, a refused field, a broken mask. */
export class StepError extends Error {}
/** The page could not be reached: the "external service" exit, worth a retry later. */
export class NetworkError extends Error {}

// A mask reaches this far past the element it covers, so anti-aliased edges never peek out.
export const MASK_PAD = 4;

/** Mask rectangles padded, clipped to the page, rounded out to whole pixels; empty ones dropped. */
export function maskRects(rects, { pad = MASK_PAD, viewport = VIEWPORT } = {}) {
  const out = [];
  for (const rect of rects) {
    const left = Math.max(0, Math.floor(rect.x - pad));
    const top = Math.max(0, Math.floor(rect.y - pad));
    const right = Math.min(viewport.width, Math.ceil(rect.x + rect.w + pad));
    const bottom = Math.min(viewport.height, Math.ceil(rect.y + rect.h + pad));
    if (right > left && bottom > top) out.push({ x: left, y: top, w: right - left, h: bottom - top });
  }
  return out;
}

/** A box clipped to the page, or null when none of it is on the page. */
export function clipBox(box, viewport = VIEWPORT) {
  if (!box) return null;
  const x = Math.max(0, box.x);
  const y = Math.max(0, box.y);
  const w = Math.min(viewport.width, box.x + box.w) - x;
  const h = Math.min(viewport.height, box.y + box.h) - y;
  return w > 0 && h > 0 ? { x: round(x), y: round(y), w: round(w), h: round(h) } : null;
}

const round = (value) => Math.round(value * 10) / 10;

const where = (index, step) => `steps[${index}] (${step.action}${step.selector ? ` ${step.selector}` : ""})`;

async function attempt(index, step, work) {
  try {
    return await work();
  } catch (error) {
    if (error instanceof StepError) throw error;
    const message = `${where(index, step)}: ${String(error.message).split("\n")[0]}`;
    if (step.action === "goto" && /net::ERR_|ERR_INTERNET|ERR_NAME|ECONN|ENOTFOUND/.test(String(error.message))) throw new NetworkError(message);
    throw new StepError(message);
  }
}

/**
 * Run the steps on `driver`. Returns { captures: [{ png, url, target, press, zoom, masks }] },
 * boxes in page pixels. Throws StepError when a step cannot be done or must not be.
 */
export async function runSteps(data, driver) {
  const problems = stepProblems(data);
  if (problems.length) throw new StepError(problems.join("; "));
  const plan = capturePlan(data.steps);
  const captures = [];
  for (const [index, step] of data.steps.entries()) {
    switch (step.action) {
      case "goto":
        await attempt(index, step, () => driver.goto(step.url));
        break;
      case "wait":
        if (step.selector !== undefined) await attempt(index, step, () => driver.waitFor(step.selector));
        else await driver.waitMs(step.ms);
        break;
      case "click":
        await attempt(index, step, () => driver.click(step.selector));
        break;
      case "fill": {
        // Checked again at run time: the validator ran on the file, this runs on what will be typed.
        const refused = selectorProblem(step.selector) ?? valueProblem(step.value);
        if (refused) throw new StepError(`${where(index, step)}: ${refused}`);
        const field = await attempt(index, step, () => driver.field(step.selector));
        const problem = fieldProblem(field);
        if (problem) throw new StepError(`${where(index, step)}: ${problem}`);
        await attempt(index, step, () => driver.fill(step.selector, step.value));
        break;
      }
      case "mask":
        break;
      case "capture": {
        const own = plan[captures.length];
        // The target first: scrolling it into view moves everything a mask must then cover.
        let target = null;
        if (own.target) {
          const found = await attempt(index, step, () => driver.boxes(own.target, { scroll: true }));
          target = clipBox(found[0] ?? null);
          if (!target) throw new StepError(`${where(index, step)}: the cursor target "${own.target}" is not on the page`);
        }
        const rects = [];
        for (const mask of own.masks) {
          if (mask.rect) {
            rects.push(mask.rect);
            continue;
          }
          // A mask whose element is not on the page at all has most likely lost its selector, and
          // what it was meant to hide may be showing: stop. One merely scrolled out of view hides nothing.
          const found = await attempt(index, step, () => driver.boxes(mask.selector, { scroll: false }));
          if (!found.length && !mask.optional) throw new StepError(`${where(index, step)}: the mask "${mask.selector}" matches nothing on this page; fix the selector, or mark the mask optional if the page may not show it`);
          rects.push(...found.map((box) => clipBox(box)).filter(Boolean));
        }
        if ((await driver.secretsShown()) > 0) throw new StepError(`${where(index, step)}: a password field on the page holds a value; refusing to take a still`);
        const masks = maskRects(rects);
        await driver.setMasks(masks);
        let png;
        try {
          png = await driver.screenshot();
        } finally {
          await driver.setMasks([]);
        }
        captures.push({ png, url: publicUrl(driver.url()), target, press: own.press, zoom: own.zoom, masks });
        break;
      }
    }
  }
  return { captures };
}
