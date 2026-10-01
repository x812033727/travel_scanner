// The step format of a `screencast` scene (docs/videos/DESIGN.md, phase three): what Playwright
// does on a public page, written in video.json, and the checks that keep it safe to run.
//
// A screencast scene's `data.steps` is a list of declarative actions: goto, wait, click, fill,
// capture and mask. The runner (runner.mjs) drives a browser through them and keeps one still per
// `capture`; the template (scene.mjs) draws the cursor, the highlight box and the zoom on top.
// Playwright's recordVideo is never used: VP8 at a variable frame rate cannot be cut to the
// narration's 30 fps grid.
//
// Nothing here may put a secret or personal data on screen (.agents/skills/youtube-video/SKILL.md
// rule 4). So: `fill` types only the literal value written in video.json, never into a password,
// one-time-code, card or contact field, and never a value that looks like an address, a phone or
// card number or a key; `goto` opens only public https pages without credentials or tokens in the
// URL; and `mask` covers whatever else must not be seen before any still is taken.
import { createHash } from "node:crypto";

export const SCREENCAST_TEMPLATE = "screencast";
export const isScreencast = (scene) => scene?.template === SCREENCAST_TEMPLATE;

// The page is laid out at a laptop's 1280x720 and captured at 1.5x, so a still is 1920x1080 pixels.
export const VIEWPORT = { width: 1280, height: 720 };
export const SCALE = 1.5;
// Every request the browser makes carries this, and nothing that names a person.
export const USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)";
// Part of every capture key: change how the runner captures and every screencast is taken again.
export const RUNNER_VERSION = "screencast-v1";

export const ACTIONS = ["goto", "wait", "click", "fill", "capture", "mask"];
export const MAX_STEPS = 40;
export const MAX_WAIT_MS = 10_000;
export const MAX_ZOOM = 2.5;
export const MAX_VALUE = 120;
const MAX_SELECTOR = 200;
const TITLE_MAX = 24;

const STEP_KEYS = {
  goto: ["url"],
  wait: ["selector", "ms"],
  click: ["selector"],
  fill: ["selector", "value"],
  capture: ["focus", "zoom"],
  mask: ["selector", "rect", "optional"],
};
const DATA_KEYS = new Set(["title", "caption", "steps"]);

// A selector that names one of these is a field the agent never types into.
const SENSITIVE_SELECTOR = /pass(?:word|wd)?\b|passwd|pwd|密碼|驗證碼|otp\b|one-time|2fa|mfa|token|secret|api[-_ ]?key|credit|card[-_ ]?(?:number|no)|cc-|cvc|cvv|ssn|身分證/i;
// Values that look like personal data or a key.
const EMAIL = /[^\s@]+@[^\s@]+\.[^\s@]+/;
const LONG_NUMBER = /\d(?:[\s-]?\d){6,}/;
const KEY_LIKE = /\b(?:sk|pk|ghp|gho|xox[abp]|AIza|ya29)[-_A-Za-z0-9]{8,}|\b[A-Za-z0-9_-]{32,}\b/;
// Query parameters that carry a credential or a session.
const SENSITIVE_PARAM = /token|key|secret|session|auth|code|pass|sig|jwt|ticket/i;
const PRIVATE_HOST = /^(?:localhost|.*\.(?:local|localhost|internal|test|lan|home))$|^\[|^\d{1,3}(?:\.\d{1,3}){3}$/i;
// The autocomplete tokens and input types of fields that hold a secret or personal data.
const SENSITIVE_TYPES = new Set(["password", "file", "hidden", "email", "tel"]);
const SENSITIVE_AUTOCOMPLETE = /password|one-time-code|cc-|email|tel|username|street|address|postal|bday|webauthn/i;

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isSelector = (value) => isText(value) && value.length <= MAX_SELECTOR;

/** Why a URL may not be opened, or null: public https pages only, nothing secret in it. */
export function urlProblem(value) {
  if (!isText(value)) return "url is required";
  let url;
  try {
    url = new URL(value);
  } catch {
    return `"${value}" is not a URL`;
  }
  if (url.protocol !== "https:") return "url must be https";
  if (url.username || url.password) return "url must not carry a user name or password";
  if (PRIVATE_HOST.test(url.hostname)) return `${url.hostname} is not a public host`;
  for (const name of url.searchParams.keys()) if (SENSITIVE_PARAM.test(name)) return `the url's "${name}" parameter may carry a credential; open a page without it`;
  return null;
}

/** Why a value may not be typed, or null: only short, plainly fictional text. */
export function valueProblem(value) {
  if (typeof value !== "string") return "value must be the literal text to type";
  if (value.length > MAX_VALUE) return `value is longer than ${MAX_VALUE} characters`;
  if (EMAIL.test(value)) return "value looks like an email address; a screencast never types one";
  if (LONG_NUMBER.test(value)) return "value looks like a phone, card or account number; a screencast never types one";
  if (KEY_LIKE.test(value)) return "value looks like a key or token; a screencast never types one";
  return null;
}

/** Why a selector names a field the agent must not type into, or null. */
export function selectorProblem(selector) {
  return SENSITIVE_SELECTOR.test(selector) ? `"${selector}" names a password, code, card or key field; the agent never types into one` : null;
}

/**
 * Whether the element a `fill` found is a field nobody may type into: { matches, type,
 * autocomplete, tag, editable } as the page reports it (`matches` counts the fields on screen the
 * selector found; the rest describe the one). A password field is refused here even when its
 * selector looked harmless.
 */
export function fieldProblem(field) {
  if (!field || field.matches === 0) return "no field on screen matches the selector";
  if (field.matches > 1) return `${field.matches} fields on screen match the selector; make it name one`;
  const type = String(field.type ?? "").toLowerCase();
  if (SENSITIVE_TYPES.has(type)) return `the field is of type ${type}; the agent never types into one`;
  if (SENSITIVE_AUTOCOMPLETE.test(String(field.autocomplete ?? ""))) return `the field asks for ${field.autocomplete}; the agent never types into one`;
  if (!field.editable) return "the field is not an editable text field";
  return null;
}

function rectProblem(rect) {
  if (!isObject(rect) || !["x", "y", "w", "h"].every((key) => typeof rect[key] === "number" && Number.isFinite(rect[key]))) return "rect must be { x, y, w, h } in page pixels";
  if (rect.w <= 0 || rect.h <= 0) return "rect must have a positive width and height";
  if (rect.x < 0 || rect.y < 0 || rect.x + rect.w > VIEWPORT.width || rect.y + rect.h > VIEWPORT.height) return `rect must lie inside the ${VIEWPORT.width}x${VIEWPORT.height} page`;
  return null;
}

function oneStepProblems(step, where) {
  if (!isObject(step)) return [`${where} must be an object with an action`];
  if (!ACTIONS.includes(step.action)) return [`${where}.action must be one of ${ACTIONS.join(", ")}`];
  const problems = [];
  for (const key of Object.keys(step)) if (key !== "action" && !STEP_KEYS[step.action].includes(key)) problems.push(`${where} (${step.action}) has an unknown field "${key}"`);
  const need = (ok, message) => ok || problems.push(`${where} (${step.action}): ${message}`);
  switch (step.action) {
    case "goto": {
      const problem = urlProblem(step.url);
      need(!problem, problem);
      break;
    }
    case "wait":
      need((step.selector === undefined) !== (step.ms === undefined), "give either selector or ms");
      if (step.selector !== undefined) need(isSelector(step.selector), `selector must be text of at most ${MAX_SELECTOR} characters`);
      if (step.ms !== undefined) need(Number.isInteger(step.ms) && step.ms >= 0 && step.ms <= MAX_WAIT_MS, `ms must be an integer from 0 to ${MAX_WAIT_MS}`);
      break;
    case "click":
      need(isSelector(step.selector), `selector must be text of at most ${MAX_SELECTOR} characters`);
      break;
    case "fill": {
      need(isSelector(step.selector), `selector must be text of at most ${MAX_SELECTOR} characters`);
      const field = isSelector(step.selector) && selectorProblem(step.selector);
      need(!field, field);
      const value = valueProblem(step.value);
      need(!value, value);
      break;
    }
    case "capture":
      if (step.focus !== undefined) need(isSelector(step.focus), `focus must be a selector of at most ${MAX_SELECTOR} characters`);
      if (step.zoom !== undefined) need(typeof step.zoom === "number" && step.zoom >= 1 && step.zoom <= MAX_ZOOM, `zoom must be a number from 1 to ${MAX_ZOOM}`);
      break;
    case "mask":
      need((step.selector === undefined) !== (step.rect === undefined), "give either selector or rect");
      if (step.selector !== undefined) need(isSelector(step.selector), `selector must be text of at most ${MAX_SELECTOR} characters`);
      if (step.rect !== undefined) {
        const problem = rectProblem(step.rect);
        need(!problem, problem);
      }
      if (step.optional !== undefined) need(typeof step.optional === "boolean", "optional must be true or false");
      break;
  }
  return problems;
}

/** Every problem with a screencast scene's data, as strings like the slide templates' checks. */
export function stepProblems(data) {
  if (!isObject(data)) return ["data must be an object with steps"];
  const problems = [];
  for (const key of Object.keys(data)) if (!DATA_KEYS.has(key)) problems.push(`unknown field "${key}"`);
  if (data.title !== undefined && !(isText(data.title) && [...data.title].length <= TITLE_MAX && !data.title.includes("\n"))) problems.push(`title must be one line of at most ${TITLE_MAX} characters`);
  if (data.caption !== undefined && !isText(data.caption)) problems.push("caption must be text");
  if (!Array.isArray(data.steps) || data.steps.length < 2 || data.steps.length > MAX_STEPS) {
    problems.push(`steps must be 2 to ${MAX_STEPS} actions`);
    return problems;
  }
  data.steps.forEach((step, index) => problems.push(...oneStepProblems(step, `steps[${index}]`)));
  if (data.steps[0]?.action !== "goto") problems.push("steps[0] must be a goto: a screencast starts on a page it names");
  if (!data.steps.some((step) => step?.action === "capture")) problems.push("steps need at least one capture");
  return problems;
}

/** How many stills a scene's steps take. */
export const captureCount = (data) => (Array.isArray(data?.steps) ? data.steps.filter((step) => step?.action === "capture").length : 0);

/**
 * Everything wrong with a screencast scene: its steps, and its reveals. Every capture is one
 * state of the scene, so a scene of N captures moves on N - 1 times across its lines.
 */
export function screencastSceneProblems(scene) {
  const problems = stepProblems(scene.data);
  if (problems.length) return problems;
  const captures = captureCount(scene.data);
  const reveals = (scene.lines ?? []).reduce((sum, line) => sum + (line.reveal ?? 0), 0);
  if (scene.lines?.[0]?.reveal) problems.push("the scene opens on its first capture: move the first line's reveal to the line where the next capture should appear");
  if (reveals !== captures - 1) problems.push(`the steps take ${captures} captures, so the lines must reveal ${captures - 1} times in all (one per capture after the first); they reveal ${reveals}`);
  return problems;
}

/**
 * For each capture, in order: the selector the cursor goes to and the highlight frames, and
 * whether it is about to be clicked. A capture's own `focus` wins; otherwise the next click
 * before the next capture or goto is the target, so "capture, then click" shows where the
 * click lands before the page changes. Also the masks that are in force at that capture.
 */
export function capturePlan(steps) {
  const plan = [];
  const masks = [];
  steps.forEach((step, index) => {
    if (step.action === "mask") masks.push(step);
    if (step.action !== "capture") return;
    let target = step.focus ?? null;
    let press = false;
    if (!target) {
      for (const next of steps.slice(index + 1)) {
        if (next.action === "capture" || next.action === "goto") break;
        if (next.action === "click") {
          target = next.selector;
          press = true;
          break;
        }
      }
    }
    plan.push({ step: index, target, press, zoom: step.zoom ?? 1, masks: [...masks] });
  });
  return plan;
}

/** JSON with sorted keys, so the same steps written in another key order hash the same. */
export function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (isObject(value)) return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  return JSON.stringify(value);
}

/**
 * The capture cache key: the steps and everything about the browser that changes the stills.
 * The title and caption are drawn by the template and do not take the page again. A capture
 * made with a signed-in profile is never the same as one made without.
 */
export function captureKey(data, { profile = false } = {}) {
  const hash = createHash("sha256");
  hash.update(canonical({ runner: RUNNER_VERSION, viewport: VIEWPORT, scale: SCALE, agent: USER_AGENT, profile: Boolean(profile), steps: data.steps }));
  return hash.digest("hex").slice(0, 16);
}

/** The page a still shows, for the manifest: origin and path, never the query or fragment. */
export function publicUrl(value) {
  try {
    const url = new URL(value);
    return `${url.origin}${url.pathname}`;
  } catch {
    return null;
  }
}
