import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { approve } from "./approvals.mjs";
import { EXPLAINER_CARD_TEMPLATES, EXPLAINER_PRESET, hasCast, isExplainer, PRESET_NAMES, resolveLook } from "./drama.mjs";
import { dramaFixture, explainerBrief, explainerFixture, fixtureLexicon, sandbox } from "./fixtures/load.mjs";
import { BRIEF_SECTIONS_DRAMA, BRIEF_SECTIONS_EXPLAINER, briefSectionsFor, lintVideo } from "./lint.mjs";
import { validateVideo } from "./schema.mjs";
import { writeScreenplay } from "./screenplay.mjs";
import { DRAMA_STEPS, pipelineStatus, stepsFor } from "./state.mjs";

const paths = (errors) => errors.map((error) => error.path).sort();
const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: explainerBrief(), others: [], translations: {}, ...overrides });

test("the explainer example is valid, lints clean and is drawn in the flat-explainer preset", () => {
  const doc = explainerFixture();
  assert.deepEqual(validateVideo(doc), []);
  const result = lintVideo(doc, context());
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  assert.ok(PRESET_NAMES.includes(EXPLAINER_PRESET));
  const look = resolveLook(doc.look);
  assert.match(look.style, /^flat editorial illustration/);
  assert.match(look.negative, /mascot/);
  assert.equal(isExplainer(doc), true);
  assert.equal(hasCast(doc), false);
  assert.equal(isExplainer(dramaFixture()), false);
  assert.equal(hasCast(dramaFixture()), true);
});

test("an explainer has no characters, no clips, and may use number and comparison cards", () => {
  const doc = explainerFixture();
  doc.characters = [{ id: "host", name: "所長", appearance: "a capybara", voice: { provider: "gemini", name: "Kore", style: "開朗" } }];
  doc.scenes[0].data.visual = "clip";
  assert.deepEqual(paths(validateVideo(doc)), ["characters", "scenes[0].data.visual"]);
  const missing = explainerFixture();
  delete missing.scenes[0].data.visual;
  assert.match(validateVideo(missing)[0].message, /all "still"/, "a shot is a clip unless it says still");
  assert.deepEqual(EXPLAINER_CARD_TEMPLATES, ["title", "chapter", "outro", "big", "stats", "compare"]);
  const drama = dramaFixture();
  drama.scenes[0] = { ...explainerFixture().scenes.find((scene) => scene.template === "stats"), chapter: "發鳩山" };
  assert.deepEqual(paths(validateVideo(drama)), ["scenes[0].template"], "a story drama keeps its three cards");
});

test("an explainer's brief answers a question instead of carrying a story bible", () => {
  assert.equal(briefSectionsFor("drama", EXPLAINER_PRESET), BRIEF_SECTIONS_EXPLAINER);
  assert.equal(briefSectionsFor("drama", "ink-wash"), BRIEF_SECTIONS_DRAMA);
  const result = lintVideo(explainerFixture(), context({ brief: "# x\n\n## 站主觀點\n\n有\n" }));
  assert.deepEqual(result.errors.map((error) => error.message), ['brief.md needs a non-empty "## 問題" section', 'brief.md needs a non-empty "## 一句答案" section']);
});

test("a drama with no characters skips the look: after the script gate comes the narration", async () => {
  assert.deepEqual(stepsFor(explainerFixture()), DRAMA_STEPS.filter((id) => !["look generated", "look approved", "music generated"].includes(id)));
  const box = sandbox("fixture-explainer", "explainer");
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  mkdirSync(box.workdir, { recursive: true });
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  writeFileSync(path.join(box.dir, "verify-1.md"), "# ok\n");
  assert.equal((await status()).next.id, "script approved");
  writeScreenplay(box.dir, explainerFixture());
  await approve({ gate: "script", docDir: box.dir, workdir: box.workdir });
  assert.equal((await status()).next.id, "narration synthesized");
});
