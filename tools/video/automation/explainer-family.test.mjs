// The explainer family on the worker: what settle() saves, which brief sections and prompt
// variant a request takes, and the inputs a flat-explainer bible job is keyed by.
import assert from "node:assert/strict";
import test from "node:test";

import { EXPLAINER_PRESETS, lookHash } from "../core/drama.mjs";
import { dramaFixture, explainerFixture } from "../core/fixtures/load.mjs";
import { ROOT } from "../core/paths.mjs";
import { visualHash } from "../core/timeline.mjs";
import { Automation, planProblem, settle } from "./flow.mjs";
import { documentInputs, documentVariant, isExplainerOneOff } from "./series.mjs";

const SETTINGS = { voice: { provider: "gemini", name: "Sulafat", style: "s", model: null, rate: "+0%" }, drama: { music_enabled: true } };
const ONE_OFF_EPISODE = { series: { slug: "one-off-7a1b2c3d", episode: 1, chapter: 1, kind: "one-off" }, cast: [] };
const settled = (video, stylePreset, options = {}) => settle(video, { slug: "fixture-explainer", settings: SETTINGS, sourceGuide: null, root: ROOT, format: "drama", stylePreset, ...options });
// What a writer may answer for the look: the preset the prompt names, an empty look, or none.
const writerLooks = () => [explainerFixture(), { ...explainerFixture(), look: {} }, (({ look: _look, ...rest }) => rest)(explainerFixture())];

test("a flat-explainer request settles to the look, look hash and visual hash it always had", () => {
  for (const options of [{}, ONE_OFF_EPISODE]) {
    for (const video of writerLooks()) {
      const saved = settled(video, "flat-explainer", options);
      assert.deepEqual(saved.look, { preset: "flat-explainer" });
      assert.deepEqual(saved.characters, []);
      assert.equal(lookHash(saved), "bd2b3b49af8e9623");
      assert.equal(visualHash(saved), visualHash(explainerFixture()));
    }
  }
});

// Until the cute presets have prompts of their own, their writer is told to answer
// look.preset "flat-explainer". The request's preset is the owner's choice and decides which
// series the video is, so settle() writes it back whatever came.
test("a cute request keeps its own preset whatever look the writer answered, with no cast and no burnt-in subtitles", () => {
  for (const preset of ["cute-cartoon", "cute-mystery"]) {
    for (const options of [{}, ONE_OFF_EPISODE]) {
      for (const video of writerLooks()) {
        const saved = settled({ ...video, characters: dramaFixture().characters, assets: [{ id: "a", file: "a.png" }] }, preset, options);
        assert.equal(saved.look.preset, preset);
        assert.deepEqual(saved.characters, []);
        assert.deepEqual(saved.assets, []);
        assert.equal(saved.subtitles.burn_in, false);
        assert.notEqual(lookHash(saved), "bd2b3b49af8e9623", "another look than flat-explainer's");
      }
    }
  }
});

test("a story request still takes the look preset its writer answered", () => {
  const saved = settled({ ...dramaFixture(), look: { preset: "ink-wash" } }, "anime-2d");
  assert.equal(saved.look.preset, "ink-wash");
  assert.ok(saved.characters.length > 0);
});

test("every explainer preset takes the question's brief sections, bible and stage prompts; a story preset takes none of them", () => {
  const lacks = (preset) => planProblem({ slug: "why-thunder-is-late", brief: "" }, new Set(), new Set(), "drama", "", preset);
  const variant = (style_preset) => Automation.prototype.variantOf.call(null, { format: "drama", style_preset });
  const oneOff = (style_preset) => ({ kind: "one-off", style_preset });
  for (const preset of EXPLAINER_PRESETS) {
    assert.match(lacks(preset), /^brief lacks ## 問題, ## 一句答案, /, preset);
    assert.equal(variant(preset), "explainer", preset);
    assert.equal(isExplainerOneOff(oneOff(preset)), true, preset);
    assert.equal(documentVariant("bible", oneOff(preset)), "bible-explainer", preset);
    assert.equal(isExplainerOneOff({ kind: "series", style_preset: preset }), false, `${preset}: a long series is never an explainer`);
  }
  assert.match(lacks("ink-wash"), /^brief lacks ## 故事前提, /);
  assert.equal(variant("ink-wash"), null);
  assert.equal(Automation.prototype.variantOf.call(null, { format: "slides", style_preset: "cute-cartoon" }), null);
  assert.equal(documentVariant("bible", oneOff("ink-wash")), "bible");
});

// The digest a bible job's journal is keyed by (series.mjs documentInputs). A change here means
// an unfinished flat-explainer bible is planned, and paid for, again.
test("the inputs of a flat-explainer bible job hash to what they did", () => {
  const job = {
    kind: "bible",
    series: { id: "11111111-1111-4111-8111-111111111111", slug: "one-off-7a1b2c3d", kind: "one-off", title: "雷聲", premise: "為什麼雷聲總比閃電晚到？", aspects: [], tone: "no-romance", style_preset: "flat-explainer", target_minutes: 10, planned_episodes: 1, episodes_per_chapter: 1, chapters: 1, open_ended: false, note: null },
    context: {},
  };
  assert.equal(documentInputs(job), "66a99ecc45f9cf42fab4fbfca083f99fca9821095ac70b77f918aaa7eb3157e9");
});
