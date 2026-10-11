// An explainer series' own prompts (explainer-series.mjs), and first of all what they must not
// move: every text and every payload the flat-explainer route had before a second series existed.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { CUTE_EXPLAINER_PRESETS, EXPLAINER_PRESETS, explainerCardTemplates } from "../core/drama.mjs";
import { dramaFixture, sandbox } from "../core/fixtures/load.mjs";
import { documentDiscussionPayload, documentDiscussVariant, SCRIPT_DISCUSSION_VARIANTS, scriptDiscussVariant } from "./discuss.mjs";
import { cardRules, EXPLAINER_DISCUSS_VARIANTS, EXPLAINER_SERIES_INSTRUCTIONS, EXPLAINER_SERIES_PROFILES, EXPLAINER_VARIANTS, explainerProfile, explainerVariants, isExplainerStageVariant } from "./explainer-series.mjs";
import { Automation, planProblem, settle } from "./flow.mjs";
import { instructionsFor, VARIANT_INSTRUCTIONS } from "./prompts.mjs";
import { canonicalJson } from "./run-receipts.mjs";
import { documentInputs, documentPayload, documentVariant } from "./series.mjs";

const sha256 = (text) => createHash("sha256").update(text, "utf8").digest("hex");
/** sha256 of a payload as the durable key reads it (undefined keys dropped, as JSON drops them). */
const payloadDigest = (payload) => sha256(canonicalJson(JSON.parse(JSON.stringify(payload))));
// What a one-off's series row carries from the long-series form, whatever the request was.
const ROW = { kind: "one-off", genre: "xianxia-bonds", lead: "dual-male", visual_tier: "clips", compilation: false };
const oneOff = (preset) => ({ slug: "one-off-1", kind: "one-off", title: "t", premise: "p", style_preset: preset, target_minutes: 10, genre: "xianxia-bonds" });
const refs = { reference: () => ({ series: "SERIES", drama: "DRAMA" }), dramaPayload: ({ style_preset: preset } = {}) => ({ drama_settings: { style_preset: preset } }) };

// ---------------------------------------------------------------------------------------------
// 1. What exists does not move. Every literal below was computed on main before this file's
// module existed (6c0d2af01). The instructions are part of a stage's durable key: a changed
// digest means every unfinished flat-explainer or story journal of that stage is asked, and paid
// for, again. prompts.test.mjs pins the four explainer texts themselves; these are the others.

test("the composed instructions of the existing explainer and discussion variants are byte for byte what they were", () => {
  const pinned = [
    [["planner", "drama", "", "discuss"], "88d7f55145ecff3e0910f33dc056b86dd8464595e1c626720bae3a2ed0f2cab9"],
    [["writer", "drama", "", "discuss"], "06c8d01e814728158f137b681e9438de81f050654d641bf7d90116cce3c0c0a6"],
    // With a one-off's row, as the bible's planner and its discussion are called.
    [["planner", "drama", "", "bible-explainer", "", ROW], "4dd130e4e03cd978f0deb6196800943984c05e694c6452368e3a12956c17a298"],
    [["planner", "drama", "", "discuss", "", ROW], "29078b6d8256814a28b6e822caf71e1bcb111ba8997a95fedd7820bb5e5242f4"],
    [["writer", "drama", "", "explainer", "", ROW], "28a178a5dcf7d5bc23923bd991e30dfaa951e866c7d996ccb08b2933f94c8d00"],
    [["verifier", "drama", "", "explainer", "", ROW], "767589242dd2d5af85305cdcee2caf1b974e30e56990d18f4a275f8eda468b78"],
    [["writer", "drama", "", "discuss", "", ROW], "1f9670db394d4ce6d41c910803be70f921e821f64ebfdf12866f2f1db92d91c2"],
    // With the owner's standing instructions and the channel's stance.
    [["writer", "drama", "旁白慢一點", "explainer", "1. 先講事實", null], "14c4507ad298ef3c96e13116e3230debc31d9ef7ad7b2e350fe4830a626f83ba"],
    // The story drama's planner, which a variant with no text of its own falls back to.
    [["planner", "drama"], "675c9213407aa771820dc4ae1eb837e33049f5659636135e06d84a624e7f9de9"],
  ];
  for (const [args, digest] of pinned) assert.equal(sha256(instructionsFor(...args)), digest, JSON.stringify(args));
  assert.equal(Object.keys(VARIANT_INSTRUCTIONS).length, 21, "no existing variant table gained or lost a key");
});

test("the bible payload and the bible discussion payload of a flat-explainer and of a story one-off are what they were", () => {
  const bible = (preset) => ({ kind: "bible", series: oneOff(preset), context: {} });
  const flat = documentPayload(refs, bible("flat-explainer"));
  assert.deepEqual(Object.keys(flat), ["kind", "series", "genre_spec", "series_reference", "drama", "drama_settings"]);
  assert.equal(flat.genre_spec.label, "仙俠羈絆", "the long-series form's default genre still rides along, as it did");
  assert.equal(payloadDigest(flat), "a899826ee8d58662a544d4049ebf427458644700bf0e459156c0f9af5736d82e");
  assert.equal(payloadDigest(documentPayload(refs, bible("ink-wash"))), "384a63d71ba30dcee42bc5a0ecfbb90e08fa56c31c2fd87fdcd439ca3a38980b");
  assert.equal(documentInputs(bible("flat-explainer")), "879e9c8c590c71948f20b5d44d464b8a897afce4b7d758501cf49cbcf0c7701a");
  assert.equal(documentInputs(bible("ink-wash")), "aa30359c8a1a9f50f32c193d9d52e5b3bafd5a5a22868acd821e0a8b9229bce3");
  const line = (preset) => ({ subject: "bible", message: { id: "m1", body_md: "鉤子再短一點" }, thread: [], series: oneOff(preset), doc: { kind: "bible", version: 1, status: "review", body_md: "# t", body_json: { characters: [] } }, context: {} });
  const asked = { reference: refs.reference, dramaPayload: () => ({ drama_settings: {} }) };
  assert.equal(payloadDigest(documentDiscussionPayload(asked, line("flat-explainer"))), "136b1cac1b54679d6bc5a9ef3fbf08f7c0c2aabec5ea4baa84c9f71861bc5145");
  assert.equal(payloadDigest(documentDiscussionPayload(asked, line("ink-wash"))), "9b40a5434846f5fdaee4528d540b58dd6ad0ccde8e7391db29173880d29a0f8e");
});

test("settle keeps what a flat-explainer's writer added to the look, as it did", () => {
  const settings = { voice: { provider: "gemini", name: "Sulafat", style: "s", model: null, rate: "+0%" }, drama: { style_preset: "cinematic-3d", music_enabled: true } };
  const written = { ...dramaFixture(), slug: "x", look: { preset: "flat-explainer", style: "my own style", negative: "text, letters" }, thumbnail: { template: "thumb", data: { headline: "h", tag: "t", shot: "a" } } };
  const settled = settle(written, { slug: "why", settings, sourceGuide: null, root: sandbox().root, format: "drama", stylePreset: "flat-explainer" });
  assert.deepEqual(settled.look, { preset: "flat-explainer", style: "my own style", negative: "text, letters" });
  assert.deepEqual(settled.characters, []);
  assert.deepEqual(settled.thumbnail, written.thumbnail, "settle never writes the thumbnail");
});

// ---------------------------------------------------------------------------------------------
// 2. The one table, the names, and the ten texts of the two profiled series.

/** The five model calls a one-off makes under `variants`, as [stage, variant]. */
const sent = (variants) => [["planner", variants.bible], ["writer", variants.stage], ["verifier", variants.stage], ["planner", variants.discuss], ["writer", variants.discuss]];

test("one table maps each explainer preset to its variants; every name fits the site's column", () => {
  assert.deepEqual(Object.keys(EXPLAINER_VARIANTS), [...EXPLAINER_PRESETS]);
  assert.deepEqual(EXPLAINER_VARIANTS["flat-explainer"], { bible: "bible-explainer", stage: "explainer", discuss: "discuss" }, "flat-explainer keeps the names it had");
  assert.deepEqual(EXPLAINER_VARIANTS["cute-cartoon"], { bible: "bible-explainer-cartoon", stage: "explainer-cartoon", discuss: "discuss-cartoon" });
  assert.deepEqual(EXPLAINER_VARIANTS["cute-mystery"], { bible: "bible-explainer-mystery", stage: "explainer-mystery", discuss: "discuss-mystery" });
  assert.deepEqual(Object.keys(EXPLAINER_SERIES_PROFILES), [...CUTE_EXPLAINER_PRESETS], "the profiled series are the cute presets, and only they");
  assert.equal(explainerVariants("ink-wash"), null);
  assert.equal(explainerVariants("constructor"), null, "an inherited name is not a preset");
  assert.equal(explainerProfile("flat-explainer"), null, "the first explainer keeps its texts in prompts.mjs");
  assert.equal(explainerProfile("toString"), null);
  assert.deepEqual([...EXPLAINER_DISCUSS_VARIANTS], ["discuss-cartoon", "discuss-mystery"]);
  for (const stage of ["explainer", "explainer-cartoon", "explainer-mystery"]) assert.equal(isExplainerStageVariant(stage), true, stage);
  for (const other of ["episode", "discuss-mystery", "bible-explainer", null, undefined]) assert.equal(isExplainerStageVariant(other), false, String(other));
  for (const variants of Object.values(EXPLAINER_VARIANTS)) {
    for (const [stage, variant] of sent(variants)) {
      // apps/api schemas.py StageRunIn.variant, and VideoAiRun.stage (String(32)) keeps "<stage>/<variant>".
      assert.match(variant, /^[a-z][a-z0-9_-]{0,31}$/);
      assert.ok(`${stage}/${variant}`.length <= 32, `${stage}/${variant}`);
    }
  }
});

// Computed from this file's module as committed, never copied from the design's orders. A change
// to any of them is a new prompt: it stops every unfinished run of that cute series at that stage
// with video_ai_receipt_input_changed, and never a flat-explainer one (the pins of group 1).
const SERIES_TEXT_PINS = {
  "planner:bible-explainer-cartoon": [5802, "20c1a532ad3ffec98c219aa99c28185de95aaf72ef2cd7879bff88d9713e6bbb"],
  "writer:explainer-cartoon": [14310, "914a8755093ae6e859a719499aeeef771d5362dd15beb109e376919e572f470f"],
  "verifier:explainer-cartoon": [4299, "47f82dfe89a3187964608f589513ef2ab6a35fc8f1c2fa6750cd30de0e7996ff"],
  "planner:discuss-cartoon": [6529, "bbed6c573d1906262c275a57f38108db015794fd7925429d648e504e78d6f767"],
  "writer:discuss-cartoon": [12775, "d6e2413cdf587fc9fbb38551faf751837248cf5028be073569a84a9675e2e8b2"],
  "planner:bible-explainer-mystery": [8518, "6af531eb54da7534334a07a292b51b8a767fe1dff04f4699229486385bd2943e"],
  "writer:explainer-mystery": [16423, "469569af118b3e5e5af1fa6e5f67ff07392e28e2b13fe31cb8a3e955c17f744b"],
  "verifier:explainer-mystery": [6066, "294b02dbcf64d5be26674fae713b09dfd958362d32356e2cb154f0dd8ca76b43"],
  "planner:discuss-mystery": [9147, "8eb3c680ca1784854091f0fd5c6878139a5423ed2117037c434784bcde085353"],
  "writer:discuss-mystery": [14969, "b7d75b482fc4b6335b9a2e92716853bcb2f1cb0e8bfe47869181d39ee37f08c0"],
};

test("the ten texts of the two profiled series are the pinned ones, composed with no genre section", () => {
  assert.deepEqual(Object.keys(EXPLAINER_SERIES_INSTRUCTIONS), Object.keys(SERIES_TEXT_PINS));
  for (const [key, [length, digest]] of Object.entries(SERIES_TEXT_PINS)) {
    const [stage, variant] = key.split(":");
    const text = instructionsFor(stage, "drama", "", variant);
    assert.equal(text, EXPLAINER_SERIES_INSTRUCTIONS[key], key);
    assert.deepEqual([text.length, sha256(text)], [length, digest], key);
    assert.equal(Object.hasOwn(VARIANT_INSTRUCTIONS, key), false, `${key} collides with an existing variant`);
    assert.equal(instructionsFor(stage, "drama", "", variant, "", ROW), text, `${key} takes no genre section from the row`);
    assert.equal(text.includes("\r"), false, key);
    assert.ok(text.length < 40_000, key);
  }
  // The owner's standing instructions and the channel's stance are still appended, as for any stage.
  const standing = instructionsFor("writer", "drama", "旁白慢一點", "explainer-mystery", "1. 先講事實", null);
  assert.ok(standing.startsWith(EXPLAINER_SERIES_INSTRUCTIONS["writer:explainer-mystery"]) && standing.includes("旁白慢一點") && standing.includes("1. 先講事實"));
});

test("each series' texts name their own series, look, cards and rules, and nothing of the flat explainer's or of each other's", () => {
  for (const [preset, variants] of Object.entries(EXPLAINER_VARIANTS)) {
    if (preset === "flat-explainer") continue;
    const profile = EXPLAINER_SERIES_PROFILES[preset];
    for (const [stage, variant] of sent(variants)) {
      const key = `${stage}:${variant}`;
      const text = instructionsFor(stage, "drama", "", variant);
      assert.ok(text.includes(profile.series) && text.includes(profile.docs), key);
      for (const phrase of ["flat editorial", "burned-in", '"preset": "flat-explainer"', "No mascot or recurring character", "burn_in: true", "anonymous figures"]) assert.equal(text.includes(phrase), false, `${key} has ${phrase}`);
      assert.equal(text.includes(preset === "cute-mystery" ? "原來如此" : "奇聞檔案局"), false, `${key} names the other series`);
      if (stage !== "writer") continue;
      assert.ok(text.includes(`"look": {"preset": "${preset}"}`), key);
      for (const card of explainerCardTemplates(preset)) assert.ok(text.includes(`"${card}" {`), `${key} names ${card}`);
      assert.match(text, /ONE person doing ONE concrete thing/);
      assert.match(text, /Never a still life or an empty scene on its own/);
      assert.match(text, /at least a third of the lines carry one \(lint warns below\s+that\)/);
      assert.match(text, /never fall under 8 minutes/, `${key}: the parts scale with target_minutes and keep the floor`);
    }
  }
  const text = (stage, variant) => instructionsFor(stage, "drama", "", variant);
  // The cards the writer is offered are exactly the ones lint accepts for the preset.
  assert.deepEqual(explainerCardTemplates("cute-mystery"), ["title", "chapter", "outro", "big", "stats", "compare", "steps", "table"]);
  assert.doesNotMatch(cardRules(explainerCardTemplates("flat-explainer")), /"steps" \{|"table" \{/, "the card rules follow the list they are given");
  // The thumbnail each series wears.
  assert.match(text("writer", "explainer-mystery"), /no "pillar", no "layout", no "tone" and no "variants"/);
  assert.doesNotMatch(text("writer", "explainer-mystery"), /pillar: business/);
  assert.match(text("writer", "explainer-cartoon"), /pillar: business\|science\|travel\|tech/);
  // 奇聞檔案局's bible keeps the question's shape with its evidence chapters in a fixed order.
  assert.match(text("planner", "bible-explainer-mystery"), /「流傳的版本：…」 once, first[\s\S]*「紀錄：…」 two to four times[\s\S]*「目前最站得住的解釋：…」 once, last/);
  // Both checkers also check the packaging, not only the narration and the cards.
  for (const variant of ["explainer-cartoon", "explainer-mystery"]) {
    assert.match(text("verifier", variant), /in youtube\.title and youtube\.description and in the\s+thumbnail \(headline, sub, and each variant's\)/, variant);
  }
  // The likeness rule of 奇聞檔案局, said the same way to every stage that can act on it.
  for (const [stage, variant] of sent(EXPLAINER_VARIANTS["cute-mystery"])) assert.match(text(stage, variant), /never drawn as that person/, `${stage}:${variant}`);
  assert.match(text("verifier", "explainer-mystery"), /living or died within the last 70 years/);
  for (const [stage, variant] of [["planner", "discuss-mystery"], ["writer", "discuss-mystery"]]) assert.match(text(stage, variant), /a person who is living or died within the last 70 years drawn by name, by face or by any feature that identifies them/, `${stage}:${variant}`);
});

// The writer's payload carries "prompt_budget_chars" at its top level (flow.mjs draftBudget) for
// every cute one-off, whose row always names its image model: the text must say what the key is.
// The flat explainer's text explains it only on fix.targets, and does not move.
test("the cute writers are told what the payload's top-level prompt_budget_chars is; the discussion writers, whose payload has none, are not", () => {
  for (const variant of ["explainer-cartoon", "explainer-mystery"]) {
    const text = instructionsFor("writer", "drama", "", variant);
    assert.match(text, /- "prompt_budget_chars", when the payload carries it at its top level, is the most characters\s+any one shot's "prompt" may have under the image model this episode is drawn with/, variant);
    assert.match(text, /a target in "fix\.targets" may carry a smaller one of its own for that shot/, variant);
    assert.match(text, /When a target in\s+"fix\.targets" carries "prompt_budget_chars"/, variant);
  }
  for (const variant of ["discuss-cartoon", "discuss-mystery"]) assert.doesNotMatch(instructionsFor("writer", "drama", "", variant), /carries it at its top level/, variant);
});

test("a variant with no text of its own falls back as it always did: the legacy brief planner to the story drama's, the listener to its own", () => {
  // No "planner:explainer-<series>" exists on purpose: that key is the legacy request route's brief
  // planner, and a cute request is always a series row. Were it reached, the story drama's planner
  // answers and planProblem refuses the brief for lacking 「## 問題」, which blocks the video.
  for (const variant of ["explainer-cartoon", "explainer-mystery"]) {
    assert.equal(Object.hasOwn(EXPLAINER_SERIES_INSTRUCTIONS, `planner:${variant}`), false);
    assert.equal(instructionsFor("planner", "drama", "", variant), instructionsFor("planner", "drama"), variant);
    assert.equal(instructionsFor("listener", "drama", "", variant), instructionsFor("listener", "drama"), variant);
  }
  assert.equal(sha256(instructionsFor("planner", "drama", "", "explainer-mystery")), "675c9213407aa771820dc4ae1eb837e33049f5659636135e06d84a624e7f9de9");
  assert.match(planProblem({ slug: "why-thunder-is-late", brief: "# t\n\n## 故事前提\nx\n" }, new Set(), new Set(), "drama", "", "cute-mystery"), /^brief lacks ## 問題/);
});

// ---------------------------------------------------------------------------------------------
// 3. The variant is chosen from the preset through the one table.

test("variantOf, documentVariant and the discussion variants read the one table", () => {
  const variantOf = (state) => Automation.prototype.variantOf.call({}, state);
  assert.equal(variantOf({ format: "drama", style_preset: "flat-explainer" }), "explainer");
  assert.equal(variantOf({ format: "drama", style_preset: "cute-cartoon" }), "explainer-cartoon");
  assert.equal(variantOf({ format: "drama", style_preset: "cute-mystery", series: { slug: "one-off-1", episode: 1, chapter: 1, kind: "one-off" } }), "explainer-mystery");
  assert.equal(variantOf({ format: "drama", style_preset: "ink-wash" }), null);
  assert.equal(variantOf({ format: "slides", style_preset: "cute-mystery" }), null);
  assert.equal(variantOf({ format: "drama", style_preset: "cinematic-3d", series: { slug: "s", episode: 1 } }), "episode");
  assert.equal(documentVariant("bible", oneOff("flat-explainer")), "bible-explainer");
  assert.equal(documentVariant("bible", oneOff("cute-cartoon")), "bible-explainer-cartoon");
  assert.equal(documentVariant("bible", oneOff("cute-mystery")), "bible-explainer-mystery");
  assert.equal(documentVariant("bible", oneOff("ink-wash")), "bible");
  assert.equal(documentVariant("setting", { ...oneOff("cute-mystery"), kind: "series" }), "setting");
  assert.equal(documentVariant("bible", { ...oneOff("cute-mystery"), kind: "series" }), "bible", "a long series is never an explainer");
  assert.equal(documentDiscussVariant(oneOff("flat-explainer")), "discuss");
  assert.equal(documentDiscussVariant(oneOff("cute-cartoon")), "discuss-cartoon");
  assert.equal(documentDiscussVariant(oneOff("cute-mystery")), "discuss-mystery");
  assert.equal(documentDiscussVariant(oneOff("ink-wash")), "discuss");
  assert.equal(documentDiscussVariant({ ...oneOff("cute-mystery"), kind: "series" }), "discuss");
  assert.equal(scriptDiscussVariant({ format: "drama", style_preset: "flat-explainer" }), "discuss");
  assert.equal(scriptDiscussVariant({ format: "drama", style_preset: "cute-cartoon" }), "discuss-cartoon");
  assert.equal(scriptDiscussVariant({ format: "drama", style_preset: "cute-mystery" }), "discuss-mystery");
  assert.equal(scriptDiscussVariant({ format: "drama", style_preset: "cinematic-3d" }), "discuss");
  assert.equal(scriptDiscussVariant({ format: "slides", style_preset: "cute-mystery" }), "discuss");
  assert.equal(scriptDiscussVariant(undefined), "discuss");
  // flow.mjs reads a video's saved runs by these to take a discussion up before the video's own stages.
  assert.deepEqual([...SCRIPT_DISCUSSION_VARIANTS], ["discuss", "anime-discuss-plan", "discuss-cartoon", "discuss-mystery"]);
});

// ---------------------------------------------------------------------------------------------
// 4. The payload: nothing new anywhere; a profiled series' bible planner loses the genre spec.

test("a cute bible's payload has the keys it had and a null genre_spec; nothing else of a document payload changes", () => {
  const payloadOf = (preset, kind = "one-off") => documentPayload(refs, { kind: "bible", series: { ...oneOff(preset), kind }, context: {} });
  for (const preset of CUTE_EXPLAINER_PRESETS) {
    assert.deepEqual(Object.keys(payloadOf(preset)), Object.keys(payloadOf("flat-explainer")), preset);
    assert.equal(payloadOf(preset).genre_spec, null, preset);
    assert.equal(payloadOf(preset).series.genre, "xianxia-bonds", "the row's facts are what they were");
    assert.deepEqual({ ...payloadOf(preset), genre_spec: payloadOf("flat-explainer").genre_spec, series: null, drama_settings: null }, { ...payloadOf("flat-explainer"), series: null, drama_settings: null }, `${preset}: only genre_spec differs beside the row and the preset`);
  }
  assert.equal(payloadOf("flat-explainer").genre_spec.label, "仙俠羈絆", "today's payload, kept as it is");
  assert.equal(payloadOf("ink-wash").genre_spec.label, "仙俠羈絆");
});

// ---------------------------------------------------------------------------------------------
// 5. settle keeps a profiled series' look to its preset.

test("settle keeps only the preset of a cute look, whatever the writer answered; the thumbnail is not settle's", () => {
  const settings = { voice: { provider: "gemini", name: "Sulafat", style: "s", model: null, rate: "+0%" }, drama: { style_preset: "cinematic-3d", music_enabled: true } };
  const written = { ...dramaFixture(), slug: "x", look: { preset: "flat-explainer", style: "my own style", negative: "text, letters" }, thumbnail: { template: "thumb", data: { headline: "飛碟？\n**是木板**", tag: "都市傳說", shot: "a" } } };
  for (const preset of CUTE_EXPLAINER_PRESETS) {
    const settled = settle(written, { slug: "curio", settings, sourceGuide: null, root: sandbox().root, format: "drama", stylePreset: preset });
    assert.deepEqual(settled.look, { preset }, preset);
    assert.deepEqual(settled.characters, [], preset);
    assert.deepEqual(settled.thumbnail, written.thumbnail, "settle never writes the thumbnail");
    assert.deepEqual(settle({ ...written, look: undefined }, { slug: "curio", settings, sourceGuide: null, root: sandbox().root, format: "drama", stylePreset: preset }).look, { preset }, `${preset}: a writer that left the look out`);
  }
});
