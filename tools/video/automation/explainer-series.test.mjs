// An explainer series' own prompts (explainer-series.mjs), and first of all what they must not
// move: every text and every payload the flat-explainer route had before a second series existed.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { dramaFixture, sandbox } from "../core/fixtures/load.mjs";
import { documentDiscussionPayload } from "./discuss.mjs";
import { settle } from "./flow.mjs";
import { instructionsFor, VARIANT_INSTRUCTIONS } from "./prompts.mjs";
import { canonicalJson } from "./run-receipts.mjs";
import { documentInputs, documentPayload } from "./series.mjs";

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
