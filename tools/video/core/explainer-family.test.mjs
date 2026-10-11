// The explainer family (docs/videos/DRAMA.md `look`): which presets are narrator-only
// explainers, which series' identity each wears, and the bytes of the first of them.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { composeShotPrompt, promptOverhead, shotPromptBudget } from "../media/prompt-budget.mjs";
import { IMAGE_SIZES } from "../media/stages.mjs";
import { HEADLINE, HEADLINE_SERIES, headlineRule } from "../qa/thumbnail.mjs";
import { thumbnailSeries } from "../render/plan.mjs";
import { EPISODE_SERIES, episodeSeries, ILLUSTRATED_SERIES } from "../shorts/episode.mjs";
import { thumbnailProblems } from "../templates/templates.mjs";
import { EXPLAINER_PRESET, EXPLAINER_PRESETS, explainerSeries, hasCast, isExplainer, isExplainerPreset, isKnowledgeLongform, keyframeKey, lookHash, needsMinimumLength, PRESET_NAMES, PRESETS, resolveLook, timesSilentShots } from "./drama.mjs";
import { dramaFixture, explainerFixture } from "./fixtures/load.mjs";
import { BRIEF_SECTIONS_EXPLAINER, briefSectionsFor, lintVideo } from "./lint.mjs";
import { validateVideo } from "./schema.mjs";
import { visualHash } from "./timeline.mjs";

const sha256 = (text) => createHash("sha256").update(text, "utf8").digest("hex");
const HERE = path.dirname(fileURLToPath(import.meta.url));
const TOOLS = path.resolve(HERE, "..");
const REPO = path.resolve(TOOLS, "..", "..");
/** The explainer fixture redrawn in `preset`. */
const inPreset = (preset) => ({ ...explainerFixture(), look: { preset } });

test("the family is three presets, and nothing else is an explainer", () => {
  assert.deepEqual(EXPLAINER_PRESETS, ["flat-explainer", "cute-cartoon", "cute-mystery"]);
  assert.ok(Object.isFrozen(EXPLAINER_PRESETS));
  for (const preset of EXPLAINER_PRESETS) {
    assert.ok(PRESET_NAMES.includes(preset), preset);
    assert.equal(isExplainerPreset(preset), true, preset);
  }
  assert.equal(EXPLAINER_PRESET, "flat-explainer");
  for (const other of ["ink-wash", "custom", "riso-teal", undefined, null, "constructor"]) assert.equal(isExplainerPreset(other), false, String(other));
});

// The two looks are the texts the owner approved (docs/videos/history-curiosity/look.md).
// Positive only: MiniMax image-01 has no negative prompt, so an avoidance list would be sent
// as picture text.
test("the two cute looks are the decided texts, positive only, and fit a 1,500-character image prompt", () => {
  const decided = {
    "cute-cartoon": { sha: "55521d0368ebd90abc139968e0c0d60c64f5c74f1da9e482f3e145eb96dc9422", length: 378, look: "b2c37ca2bc627cd1", budget: 1093 },
    "cute-mystery": { sha: "357820a7ce41cfb5fc5c3175db292bf0132ee83d84674618abccf9d4f2585900", length: 401, look: "98a370ae40badbaf", budget: 1070 },
  };
  for (const [preset, expected] of Object.entries(decided)) {
    const entry = PRESETS[preset];
    assert.deepEqual(Object.keys(entry), ["style", "negative", "motion"], preset);
    assert.equal(entry.style.length, expected.length, preset);
    assert.equal(sha256(entry.style), expected.sha, preset);
    assert.equal(entry.negative, "", preset);
    assert.equal(entry.motion, PRESETS["flat-explainer"].motion, preset);
    assert.equal(lookHash({ format: "drama", look: { preset }, characters: [] }), expected.look, preset);

    const look = resolveLook({ preset });
    const { prompt } = composeShotPrompt({ prompt: "a lighthouse at dusk", look, camera: "tilt down", cast: "", limit: 1500 });
    assert.ok(prompt.includes(". Style: cute Taiwanese"), prompt);
    assert.doesNotMatch(prompt, /Avoid:/, "no avoidance text reaches a model that would draw it");
    assert.equal(promptOverhead({ look, camera: "tilt down", cast: null }), promptOverhead({ look: { ...look, negative: undefined }, camera: "tilt down", cast: null }), preset);
    assert.equal(shotPromptBudget({ look, camera: "tilt down", cast: null, limit: 1500 }), expected.budget, preset);
  }
});

// Recorded on main before the family existed. A change to any of these moves the look hash of
// every flat-explainer video already drawn, so its pictures would be asked for (and paid for)
// again, and the image cache key of every picture it still has to draw.
test("flat-explainer is what it was: preset bytes, look hash, visual hash, composed prompt and image keys", () => {
  assert.equal(sha256(JSON.stringify(PRESETS["flat-explainer"])), "0646ae3434271709496daa3d9e83f1d5c19bfe0e6760c1d6c2860e6a3afb6881");
  const fixture = explainerFixture();
  assert.equal(lookHash(fixture), "bd2b3b49af8e9623");
  assert.equal(lookHash({ format: "drama", look: { preset: "flat-explainer" }, characters: [] }), "bd2b3b49af8e9623");
  assert.equal(visualHash(fixture), "1ee426698cc02ed3");

  const shot = fixture.scenes.find((scene) => scene.id === "flash");
  const look = resolveLook(fixture.look);
  const { prompt } = composeShotPrompt({ prompt: shot.data.prompt, look, camera: shot.data.camera, cast: "", limit: 4000 });
  assert.equal(sha256(prompt), "ea312665764d5a793065d1fd6ef3a76cc70c31be1232315c03896c59d11147e3");
  const key = (size) => keyframeKey({ provider: "gemini", model: "gemini-3-pro-image", prompt, negative: look.negative, ...IMAGE_SIZES[size], seed: 1, references: [] });
  assert.equal(key("2K"), "5169040efab27447");
  assert.equal(key("1K"), "7c56c03a202a1cc8");
});

test("each of the three presets is held to the explainer's rules: no cast, stills only, the eight-minute floor, the question's brief", () => {
  const baseline = lintVideo(explainerFixture());
  for (const preset of EXPLAINER_PRESETS) {
    const doc = inPreset(preset);
    assert.deepEqual(validateVideo(doc), [], preset);
    assert.equal(isExplainer(doc), true, preset);
    assert.equal(hasCast(doc), false, preset);
    assert.equal(needsMinimumLength(doc), true, preset);
    assert.equal(isKnowledgeLongform(doc), true, preset);
    assert.equal(timesSilentShots(doc), false, preset);
    assert.equal(briefSectionsFor("drama", preset), BRIEF_SECTIONS_EXPLAINER, preset);

    const cast = validateVideo({ ...doc, characters: dramaFixture().characters.slice(0, 1) }).filter((error) => error.path === "characters");
    assert.equal(cast.length, 1, preset);
    assert.equal(cast[0].message, `an explainer (look preset "${preset}") has no characters: the narrator tells it`);

    const clip = structuredClone(doc);
    const index = clip.scenes.findIndex((scene) => scene.template === "shot");
    clip.scenes[index].data.visual = "clip";
    assert.deepEqual(validateVideo(clip).map((error) => error.path), [`scenes[${index}].data.visual`], preset);

    // The fixture's thumbnail is So That's Why's (a pillar, a long headline), so only the
    // presets that wear that identity lint as it does; cute-mystery takes the channel's rules.
    if (explainerSeries(doc) !== "sothatswhy") continue;
    const linted = lintVideo(doc);
    assert.deepEqual(linted.errors, baseline.errors, preset);
    assert.deepEqual(linted.warnings, baseline.warnings, preset);
  }
  assert.equal(briefSectionsFor("drama", "ink-wash").includes("問題"), false);
});

// Being an explainer and being So That's Why are two questions: cute-cartoon is So That's Why
// redrawn and keeps its bookends, thumbnail and Shorts theme; cute-mystery is another series'
// explainer and wears the channel's until it has an identity of its own.
test("identity: flat-explainer and cute-cartoon are So That's Why's, cute-mystery is the channel's", () => {
  const identity = { "flat-explainer": "sothatswhy", "cute-cartoon": "sothatswhy", "cute-mystery": null };
  for (const [preset, series] of Object.entries(identity)) {
    const doc = inPreset(preset);
    assert.equal(explainerSeries(doc), series, preset);
    assert.equal(thumbnailSeries(doc), series, preset);
    assert.equal(episodeSeries(doc), series ? EPISODE_SERIES : ILLUSTRATED_SERIES, preset);
    assert.equal(headlineRule(thumbnailSeries(doc)), series ? HEADLINE_SERIES : HEADLINE, preset);
    if (series) assert.deepEqual(thumbnailProblems(doc.thumbnail, { series: thumbnailSeries(doc) }), [], preset);
  }
  assert.equal(EPISODE_SERIES, "sothatswhy");
  for (const other of [dramaFixture(), { format: "slides", look: { preset: "flat-explainer" } }, { format: "slides", look: { preset: "cute-cartoon" } }, undefined]) {
    assert.equal(explainerSeries(other), null);
    assert.equal(thumbnailSeries(other), null);
    assert.equal(episodeSeries(other), ILLUSTRATED_SERIES);
  }
});

/** Every non-test module under tools/video, as [relative path, source]. */
function modules(dir = TOOLS, found = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== "node_modules" && entry.name !== "fixtures") modules(file, found);
    } else if (entry.name.endsWith(".mjs") && !entry.name.endsWith(".test.mjs")) {
      found.push([path.relative(TOOLS, file).replaceAll("\\", "/"), readFileSync(file, "utf8")]);
    }
  }
  return found;
}

// A comparison with the one preset is how a new family member gets forgotten: ask
// isExplainerPreset (the family) or explainerSeries (the identity) instead. This only sees
// `===` and `!==` beside the name or the constant; it does not see `.includes("flat-explainer")`,
// a `switch` case or a Set, which a reviewer still has to.
test("no module compares a preset with flat-explainer directly", () => {
  const bare = /[!=]==\s*(?:EXPLAINER_PRESET\b|["']flat-explainer["'])|(?:\bEXPLAINER_PRESET\b|["']flat-explainer["'])\s*[!=]==/;
  const sources = modules();
  assert.ok(sources.length > 100, "the walk found the tools");
  for (const [file, source] of sources) {
    assert.doesNotMatch(source, bare, file);
    if (file !== "core/drama.mjs") assert.doesNotMatch(source, /\bEXPLAINER_PRESET\b/, `${file}: use isExplainerPreset or explainerSeries`);
  }
});

// The API and the web keep their own copy of the list (a CHECK constraint and a form cannot
// import this module). Read as text, as production/design.test.mjs reads API source.
test("the tools, the API and the web name the same explainer family", () => {
  const names = (text) => [...text.matchAll(/"([a-z0-9-]+)"/g)].map((match) => match[1]);
  const api = readFileSync(path.join(REPO, "apps", "api", "app", "video_automation", "schemas.py"), "utf8");
  const apiList = /^EXPLAINER_PRESETS: tuple\[StylePreset, \.\.\.\] = \(([^)]*)\)$/m.exec(api);
  assert.ok(apiList, "schemas.py declares EXPLAINER_PRESETS as a tuple on one line");
  assert.deepEqual(names(apiList[1]), [...EXPLAINER_PRESETS]);
  const web = readFileSync(path.join(REPO, "apps", "web", "lib", "video-presets.ts"), "utf8");
  const webList = /^export const EXPLAINER_PRESETS = \[([^\]]*)\] as const;$/m.exec(web);
  assert.ok(webList, "video-presets.ts declares EXPLAINER_PRESETS on one line");
  assert.deepEqual(names(webList[1]), [...EXPLAINER_PRESETS]);
  // The image model a cute one-off takes when its request names none: the server stores it and
  // the request form preselects it, each from its own copy of one table.
  const apiModels = /^PRESET_IMAGE_MODELS: dict\[str, str\] = \{([^}]*)\}$/m.exec(api);
  assert.ok(apiModels, "schemas.py declares PRESET_IMAGE_MODELS on one line");
  const webModels = /^export const PRESET_IMAGE_MODEL: Readonly<Record<string, string>> = \{([^}]*)\};$/m.exec(web);
  assert.ok(webModels, "video-presets.ts declares PRESET_IMAGE_MODEL on one line");
  assert.deepEqual(names(apiModels[1]), ["cute-cartoon", "image-01", "cute-mystery", "image-01"]);
  assert.deepEqual(names(webModels[1]), names(apiModels[1]));
  for (const [index, name] of names(apiModels[1]).entries()) if (index % 2 === 0) assert.ok(isExplainerPreset(name) && name !== "flat-explainer", `${name}: a cute explainer preset`);
});
