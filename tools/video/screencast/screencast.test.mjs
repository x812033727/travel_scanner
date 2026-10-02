import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { lintVideo } from "../core/lint.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { MAX_TRANSITION_FRAMES, FPS } from "../render/browser.mjs";
import { renderPlan, renderProblems } from "../render/plan.mjs";
import { cachedManifest, captureFile, ensureCaptures, manifestFile } from "./capture.mjs";
import { maskRects, NetworkError, runSteps, StepError } from "./runner.mjs";
import { captureUrl, ENTRANCE_MS, REST, screencastHtml, screencastPlan } from "./scene.mjs";
import {
  captureCount,
  captureKey,
  capturePlan,
  fieldProblem,
  publicUrl,
  screencastSceneProblems,
  selectorProblem,
  stepProblems,
  urlProblem,
  USER_AGENT,
  valueProblem,
  VIEWPORT,
} from "./steps.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const fixture = JSON.parse(readFileSync(new URL("./fixtures/tutorial/video.json", import.meta.url), "utf8"));
const lexicon = JSON.parse(readFileSync(new URL("./fixtures/lexicon.json", import.meta.url), "utf8"));
const brief = readFileSync(new URL("./fixtures/tutorial/brief.md", import.meta.url), "utf8");
const screencast = () => structuredClone(fixture.scenes.find((scene) => scene.template === "screencast"));
const goto = { action: "goto", url: "https://example.com/docs" };
const data = (...steps) => ({ steps: [goto, ...steps] });

// A page that records what the runner asks of it, in order.
function fakeDriver({ boxes = {}, fields = {}, secrets = 0, url = "https://example.com/docs?ref=1#top", failGoto = null } = {}) {
  const calls = [];
  return {
    calls,
    goto: async (target) => {
      calls.push(["goto", target]);
      if (failGoto) throw new Error(failGoto);
    },
    waitFor: async (selector) => calls.push(["waitFor", selector]),
    waitMs: async (ms) => calls.push(["waitMs", ms]),
    click: async (selector) => calls.push(["click", selector]),
    fill: async (selector, value) => calls.push(["fill", selector, value]),
    field: async (selector) => fields[selector] ?? { matches: 1, type: "search", autocomplete: "", editable: true },
    boxes: async (selector, options) => {
      calls.push(["boxes", selector, options.scroll]);
      return boxes[selector] ?? [];
    },
    setMasks: async (rects) => calls.push(["setMasks", rects]),
    secretsShown: async () => secrets,
    screenshot: async () => {
      calls.push(["screenshot"]);
      return Buffer.from(`png${calls.length}`);
    },
    url: () => url,
  };
}

test("the fixture's steps are valid and its lines step through every capture", () => {
  const scene = screencast();
  assert.deepEqual(stepProblems(scene.data), []);
  assert.equal(captureCount(scene.data), 3);
  assert.deepEqual(screencastSceneProblems(scene), []);
});

test("bad steps are named: unknown actions and fields, a first step that is not a goto, no capture, out-of-range numbers", () => {
  assert.deepEqual(stepProblems({ steps: [{ action: "type", selector: "a" }, { action: "capture" }] }), [
    "steps[0].action must be one of goto, wait, click, fill, capture, mask",
    "steps[0] must be a goto: a screencast starts on a page it names",
  ]);
  assert.deepEqual(stepProblems(data({ action: "click", selector: "a" })), ["steps need at least one capture"]);
  assert.deepEqual(stepProblems(data({ action: "wait", selector: "a", ms: 5 }, { action: "capture" })), ["steps[1] (wait): give either selector or ms"]);
  assert.deepEqual(stepProblems(data({ action: "wait", ms: 60_000 }, { action: "capture", zoom: 4 })), [
    "steps[1] (wait): ms must be an integer from 0 to 10000",
    "steps[2] (capture): zoom must be a number from 1 to 2.5",
  ]);
  assert.deepEqual(stepProblems(data({ action: "capture", record: true })), ['steps[1] (capture) has an unknown field "record"']);
  assert.deepEqual(stepProblems(data({ action: "mask", rect: { x: 1200, y: 0, w: 200, h: 40 } }, { action: "capture" })), ["steps[1] (mask): rect must lie inside the 1280x720 page"]);
  assert.deepEqual(stepProblems({ steps: [goto], extra: 1 }), ['unknown field "extra"', "steps must be 2 to 40 actions"]);
});

test("goto opens only public https pages with nothing secret in the URL", () => {
  assert.equal(urlProblem("https://mokaair.com/zh-TW/guides?topic=transport"), null);
  assert.equal(urlProblem("http://mokaair.com"), "url must be https");
  assert.match(urlProblem("https://user:hunter2@example.com"), /user name or password/);
  assert.match(urlProblem("https://localhost:3000/admin"), /not a public host/);
  assert.match(urlProblem("https://192.168.1.10/"), /not a public host/);
  assert.match(urlProblem("https://example.com/?access_token=abc"), /"access_token" parameter/);
  assert.match(urlProblem("https://example.com/cb?code=xyz"), /"code" parameter/);
});

test("fill types only short literal values, never into a secret field and never personal data", () => {
  assert.equal(valueProblem("東京交通"), null);
  assert.match(valueProblem("someone@example.com"), /email/);
  assert.match(valueProblem("0912 345 678"), /phone, card or account number/);
  assert.match(valueProblem("4111-1111-1111-1111"), /phone, card or account number/);
  assert.match(valueProblem("sk-proj-abcdefghijklmnop"), /key or token/);
  assert.match(valueProblem("x".repeat(121)), /longer than 120/);
  for (const selector of ["input[type=password]", "#login-password", "input[name=otp]", "[autocomplete=cc-number]", "input[name=api_key]", "#密碼"]) {
    assert.ok(selectorProblem(selector), selector);
  }
  assert.equal(selectorProblem('input[placeholder="搜尋文章與攻略"]'), null);
  // The validator refuses them in video.json before anything runs.
  const problems = stepProblems(data({ action: "fill", selector: "input[type=password]", value: "demo" }, { action: "capture" }));
  assert.equal(problems.length, 1);
  assert.match(problems[0], /never types into one/);
});

test("the page's own field is checked at run time: password, code, card and contact fields are refused", () => {
  assert.equal(fieldProblem({ matches: 1, type: "search", autocomplete: "off", editable: true }), null);
  assert.match(fieldProblem({ matches: 1, type: "password", autocomplete: "", editable: true }), /type password/);
  assert.match(fieldProblem({ matches: 1, type: "text", autocomplete: "current-password", editable: true }), /current-password/);
  assert.match(fieldProblem({ matches: 1, type: "text", autocomplete: "one-time-code", editable: true }), /one-time-code/);
  assert.match(fieldProblem({ matches: 1, type: "text", autocomplete: "cc-number", editable: true }), /cc-number/);
  assert.match(fieldProblem({ matches: 1, type: "email", autocomplete: "", editable: true }), /type email/);
  assert.match(fieldProblem({ matches: 0 }), /no field on screen/);
  assert.match(fieldProblem({ matches: 2 }), /2 fields on screen/);
  assert.match(fieldProblem({ matches: 1, type: "text", editable: false }), /not an editable/);
});

test("a fill whose harmless-looking selector lands on a password field stops the run before typing", async () => {
  const driver = fakeDriver({ fields: { "#q": { matches: 1, type: "password", autocomplete: "", editable: true } } });
  await assert.rejects(runSteps(data({ action: "fill", selector: "#q", value: "demo" }, { action: "capture" }), driver), (error) => error instanceof StepError && /type password/.test(error.message));
  assert.equal(driver.calls.some(([name]) => name === "fill"), false);
});

test("masks are drawn before every still and taken off after it; a selector mask covers every match", async () => {
  const steps = data(
    { action: "mask", selector: ".account" },
    { action: "mask", rect: { x: 10, y: 10, w: 100, h: 20 } },
    { action: "capture" },
    { action: "capture" },
  );
  const driver = fakeDriver({ boxes: { ".account": [{ x: 700, y: 20, w: 60, h: 40 }, { x: 1250, y: 700, w: 100, h: 100 }] } });
  const { captures } = await runSteps(steps, driver);
  const order = driver.calls.filter(([name]) => name === "setMasks" || name === "screenshot").map(([name, rects]) => (name === "setMasks" ? rects.length : "shot"));
  assert.deepEqual(order, [3, "shot", 0, 3, "shot", 0]);
  assert.deepEqual(captures[0].masks, [
    { x: 696, y: 16, w: 68, h: 48 },
    { x: 1246, y: 696, w: 34, h: 24 },
    { x: 6, y: 6, w: 108, h: 28 },
  ]);
  assert.equal(captures[0].url, "https://example.com/docs", "the query and fragment never reach the manifest");
});

test("maskRects pads, clips to the page and drops what is off it", () => {
  assert.deepEqual(maskRects([{ x: 0.4, y: 2, w: 10.2, h: 5 }]), [{ x: 0, y: 0, w: 15, h: 11 }]);
  assert.deepEqual(maskRects([{ x: 1300, y: 10, w: 50, h: 50 }]), []);
  assert.deepEqual(maskRects([{ x: 1270, y: 710, w: 50, h: 50 }], { pad: 0 }), [{ x: 1270, y: 710, w: 10, h: 10 }]);
});

test("a mask that matches nothing stops the run unless it is optional; one scrolled off the page hides nothing", async () => {
  const run = (mask, boxes = {}) => runSteps(data(mask, { action: "capture" }), fakeDriver({ boxes }));
  await assert.rejects(run({ action: "mask", selector: ".gone" }), (error) => error instanceof StepError && /matches nothing/.test(error.message));
  assert.deepEqual((await run({ action: "mask", selector: ".gone", optional: true })).captures[0].masks, []);
  assert.deepEqual((await run({ action: "mask", selector: ".far" }, { ".far": [{ x: 10, y: 3000, w: 100, h: 40 }] })).captures[0].masks, []);
});

test("no still is taken while a password field on the page holds a value", async () => {
  await assert.rejects(runSteps(data({ action: "capture" }), fakeDriver({ secrets: 1 })), /password field on the page holds a value/);
});

test("the cursor target of a capture is the next click, measured before the click, scrolled into view", async () => {
  const steps = data({ action: "capture" }, { action: "click", selector: "#go" }, { action: "capture", focus: "#title", zoom: 1.5 });
  const driver = fakeDriver({ boxes: { "#go": [{ x: 100, y: 50, w: 80, h: 30 }], "#title": [{ x: 10, y: 100, w: 400, h: 60 }] } });
  const { captures } = await runSteps(steps, driver);
  const names = driver.calls.map((call) => call.slice(0, 3).join(" "));
  assert.ok(names.indexOf("boxes #go true") < names.indexOf("click #go"));
  assert.deepEqual(captures.map((capture) => [capture.target, capture.press, capture.zoom]), [
    [{ x: 100, y: 50, w: 80, h: 30 }, true, 1],
    [{ x: 10, y: 100, w: 400, h: 60 }, false, 1.5],
  ]);
  await assert.rejects(runSteps(data({ action: "capture", focus: "#nowhere" }), fakeDriver()), /cursor target "#nowhere" is not on the page/);
});

test("capturePlan: a capture's focus wins, else the next click until the next capture or goto; masks in force so far", () => {
  const plan = capturePlan([
    goto,
    { action: "mask", rect: { x: 0, y: 0, w: 10, h: 10 } },
    { action: "capture" },
    { action: "wait", ms: 100 },
    { action: "click", selector: "#a" },
    { action: "capture" },
    { action: "goto", url: "https://example.com/b" },
    { action: "click", selector: "#b" },
    { action: "capture", focus: "#c" },
  ]);
  assert.deepEqual(plan.map((each) => [each.target, each.press, each.masks.length]), [["#a", true, 1], [null, false, 1], ["#c", false, 1]]);
});

test("a page that cannot be reached is a network failure, a selector that never shows a step failure", async () => {
  await assert.rejects(runSteps(data({ action: "capture" }), fakeDriver({ failGoto: "page.goto: net::ERR_NAME_NOT_RESOLVED at https://example.com/docs" })), NetworkError);
  const driver = fakeDriver();
  driver.waitFor = async () => {
    throw new Error("locator.waitFor: Timeout 25000ms exceeded.\nCall log: ...");
  };
  await assert.rejects(runSteps(data({ action: "wait", selector: "#late" }, { action: "capture" }), driver), (error) => error instanceof StepError && error.message === "steps[1] (wait #late): locator.waitFor: Timeout 25000ms exceeded.");
});

test("the capture key follows the steps alone: key order, title and caption do not move it, a step or a profile does", () => {
  const scene = screencast();
  const key = captureKey(scene.data);
  const reordered = { ...scene.data, steps: scene.data.steps.map((step) => Object.fromEntries(Object.entries(step).reverse())) };
  assert.equal(captureKey(reordered), key);
  assert.equal(captureKey({ ...scene.data, title: "另一個標題", caption: "別的說明" }), key);
  const changed = structuredClone(scene.data);
  changed.steps[7].value = "大阪交通";
  assert.notEqual(captureKey(changed), key);
  assert.notEqual(captureKey(scene.data, { profile: true }), key);
  assert.match(key, /^[0-9a-f]{16}$/);
  assert.equal(USER_AGENT, "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)");
});

test("the scene's reveals must step through the captures one by one, starting on the first", () => {
  const scene = screencast();
  scene.lines[2].reveal = 0;
  assert.match(screencastSceneProblems(scene)[0], /must reveal 2 times in all .* they reveal 1/);
  const early = screencast();
  early.lines[0].reveal = 1;
  early.lines[2].reveal = 0;
  assert.match(screencastSceneProblems(early)[0], /opens on its first capture/);
});

const manifest = (key = "k1") => ({
  key,
  viewport: VIEWPORT,
  captures: [
    { file: `screencast/${key}/01.png`, sha256: "a1", target: { x: 640, y: 20, w: 100, h: 40 }, press: true, zoom: 1, masks: [] },
    { file: `screencast/${key}/02.png`, sha256: "a2", target: null, press: false, zoom: 1, masks: [] },
    { file: `screencast/${key}/03.png`, sha256: "a3", target: { x: 128, y: 360, w: 256, h: 72 }, press: false, zoom: 2, masks: [] },
  ],
});

test("the frame plan: the cursor comes in from the corner, stays put on a capture with no target, and moves on", () => {
  const plan = screencastPlan(manifest(), [{ reveal: 0 }, { reveal: 1 }, { reveal: 2 }]);
  assert.deepEqual(plan[0].cursor, { from: REST, to: { x: 53.91, y: 6.67 }, moves: true });
  assert.deepEqual(plan[0].highlight, { x: 49.5, y: 2.28, w: 8.81, h: 6.56 });
  assert.equal(plan[0].press, true);
  assert.equal(plan[0].zoom, null);
  assert.deepEqual(plan[1].cursor, { from: { x: 53.91, y: 6.67 }, to: { x: 53.91, y: 6.67 }, moves: false });
  assert.equal(plan[1].highlight, null);
  assert.deepEqual(plan[2].cursor.to, { x: 20, y: 57 });
  assert.deepEqual(plan[2].zoom, { scale: 2, origin: { x: 20, y: 57 } });
  assert.deepEqual(plan.map((each) => each.file), ["screencast/k1/01.png", "screencast/k1/02.png", "screencast/k1/03.png"]);
  const quiet = screencastPlan({ ...manifest(), captures: [{ ...manifest().captures[1] }] }, [{ reveal: 0 }]);
  assert.equal(quiet[0].cursor, null, "no cursor until something is pointed at");
  assert.throws(() => screencastPlan(manifest(), [{ reveal: 3 }]), /has no capture/);
});

test("every entrance fits the frames the renderer freezes, and the page animates only what moves", () => {
  assert.ok(ENTRANCE_MS <= (MAX_TRANSITION_FRAMES * 1000) / FPS, `${ENTRANCE_MS} ms`);
  const [first, still] = screencastPlan(manifest(), [{ reveal: 0 }, { reveal: 1 }]);
  const state = { first: true, chapter: "章", chapterNumber: 2, chapterCount: 3 };
  const html = screencastHtml(screencast(), first, state);
  assert.match(html, /@keyframes sc-move\{from\{left:92%;top:94%\}to\{left:53.91%;top:6.67%\}\}/);
  assert.match(html, /\.sc-box\{animation:sc-glow/);
  assert.match(html, /\.sc-press\{animation:sc-press 180ms 420ms ease-out forwards\}/);
  assert.ok(html.includes(`src="${captureUrl("screencast/k1/01.png")}"`));
  assert.match(html, /帳號區已遮蔽/);
  const quiet = screencastHtml(screencast(), still, { ...state, first: false });
  assert.doesNotMatch(quiet, /animation:sc-(move|glow|press|zoom)/);
});

test("lint accepts the fixture and refuses a screencast that would type into a password field", () => {
  const context = { lexicon, brief };
  assert.deepEqual(lintVideo(fixture, context).errors, []);
  const doc = structuredClone(fixture);
  doc.scenes[1].data.steps[7] = { action: "fill", selector: "#password", value: "demo" };
  const errors = lintVideo(doc, context).errors.map((each) => each.message);
  assert.ok(errors.some((message) => /never types into one/.test(message)), errors.join("\n"));
});

test("the render plan draws one state per capture, keyed by the capture's pixels", () => {
  const scene = screencast();
  const key = captureKey(scene.data);
  assert.deepEqual(renderProblems(fixture), []);
  const plan = renderPlan(fixture, "t", null, { screencasts: { [scene.id]: manifest(key) } });
  const drawn = plan.scenes.find((each) => each.id === scene.id);
  assert.equal(drawn.kind, "stills");
  assert.equal(drawn.states.length, estimateTimeline(fixture).scenes[1].states.length);
  assert.deepEqual(drawn.states.map((each) => each.reveal), [0, 1, 2]);
  assert.ok(drawn.states[0].html.includes(`/work/screencast/${key}/01.png`));
  const repainted = manifest(key);
  repainted.captures[0].sha256 = "b1";
  const again = renderPlan(fixture, "t", null, { screencasts: { [scene.id]: repainted } }).scenes[1];
  assert.notEqual(again.states[0].key, drawn.states[0].key);
  assert.equal(again.states[1].key, drawn.states[1].key);
  assert.throws(() => renderPlan(fixture, "t"), /has no captures yet/);
});

test("captures are cached by their steps: a rerun opens no browser, recapture and a changed step take the page again", async () => {
  const workdir = mkdtempSync(path.join(tmpdir(), "screencast-"));
  try {
    let opened = 0;
    const open = async () => {
      opened += 1;
      return { newDriver: async () => fakeDriver({ boxes: { 'role=link[name="旅遊情報攻略" s] >> nth=0': [{ x: 528, y: 18, w: 100, h: 44 }], 'a[href="/zh-TW/guides/topics/transport"]': [{ x: 177, y: 508, w: 36, h: 44 }], 'input[placeholder="搜尋文章與攻略"]': [{ x: 731, y: 16, w: 247, h: 48 }], 'a[href="/zh-TW/login"]': [{ x: 716, y: 21, w: 62, h: 38 }] } }), close: async () => {} };
    };
    const now = () => new Date("2026-10-01T00:00:00Z");
    const first = await ensureCaptures(fixture, workdir, { open, now });
    assert.deepEqual([opened, first.captured, first.reused], [1, ["find-guides"], []]);
    const key = captureKey(screencast().data);
    const written = JSON.parse(readFileSync(path.join(workdir, manifestFile(key)), "utf8"));
    assert.equal(written.captures.length, 3);
    assert.ok(existsSync(path.join(workdir, captureFile(key, 2))));
    assert.deepEqual(written.captures[0].masks, [{ x: 712, y: 17, w: 70, h: 46 }]);
    assert.deepEqual(cachedManifest(workdir, screencast()), written);

    const second = await ensureCaptures(fixture, workdir, { open, now });
    assert.deepEqual([opened, second.reused], [1, ["find-guides"]]);
    assert.deepEqual(second.manifests["find-guides"], written);

    await ensureCaptures(fixture, workdir, { open, now, recapture: true });
    assert.equal(opened, 2);

    const edited = structuredClone(fixture);
    edited.scenes[1].data.steps[7].value = "大阪交通";
    const third = await ensureCaptures(edited, workdir, { open, now });
    assert.equal(opened, 3);
    assert.notEqual(third.manifests["find-guides"].key, key);
  } finally {
    rmSync(workdir, { recursive: true, force: true });
  }
});

test("publicUrl keeps origin and path only", () => {
  assert.equal(publicUrl("https://mokaair.com/zh-TW/guides?q=x#y"), "https://mokaair.com/zh-TW/guides");
  assert.equal(publicUrl("not a url"), null);
});
