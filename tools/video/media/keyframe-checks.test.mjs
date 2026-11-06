// The judge's questions for the narrated cute looks (owner 2026-11-05): writing of any kind fails,
// a still marked `nobody` fails when anyone is drawn, and a pictured cast is held to its sheet.
import assert from "node:assert/strict";
import test from "node:test";

import { keyframeChecks, NOBODY_QUESTION, WORDLESS_TEXT_QUESTION, wordlessLook } from "./keyframes.mjs";
import { validateVideo } from "../core/schema.mjs";
import { explainerFixture } from "../core/fixtures/load.mjs";

test("the default checks are unchanged, and the wordless look asks about made-up writing", () => {
  const plain = keyframeChecks();
  assert.deepEqual(plain.map((check) => check.key), ["text", "anatomy", "detached", "subject", "frame", "style", "details", "awkward", "generated"]);
  assert.match(plain[0].question, /do not count/, "the measured question keeps its allowance for marks");
  const wordless = keyframeChecks({ wordless: true });
  assert.equal(wordless[0].question, WORDLESS_TEXT_QUESTION);
  assert.match(WORDLESS_TEXT_QUESTION, /made-up marks that look like writing/);
  assert.equal(wordless.length, plain.length);
});

test("a still marked nobody adds the person question; a cast adds one identity question each", () => {
  const checks = keyframeChecks({ nobody: true, characters: [{ id: "researcher", name: "Ada", appearance: "a woman" }] });
  assert.deepEqual(checks.slice(0, 3).map((check) => check.key), ["identity_researcher", "text", "nobody"]);
  assert.equal(checks[2].question, NOBODY_QUESTION);
  assert.equal(checks[2].cost, 10, "a person where none may be is a redraw fault");
});

test("only the cute-mystery look is wordless, and nobody is a true-or-absent shot field", () => {
  assert.equal(wordlessLook({ look: { preset: "cute-mystery" } }), true);
  assert.equal(wordlessLook({ look: { preset: "cute-cartoon" } }), false);
  assert.equal(wordlessLook({}), false);
  const doc = explainerFixture();
  const index = doc.scenes.findIndex((scene) => scene.template === "shot");
  doc.scenes[index].data.nobody = true;
  assert.deepEqual(validateVideo(doc), []);
  doc.scenes[index].data.nobody = false;
  assert.deepEqual(validateVideo(doc).map((error) => error.path), [`scenes[${index}].data.nobody`]);
});
