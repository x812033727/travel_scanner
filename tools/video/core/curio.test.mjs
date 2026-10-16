import assert from "node:assert/strict";
import test from "node:test";

import { CURIO_MAX_CARD_RUN, CURIO_MIN_SHOT_SHARE, CURIO_PRESET, curioProblems, isCurio } from "./curio.mjs";
import { resolveLook } from "./drama.mjs";
import { fixture, fixtureBrief, fixtureLexicon } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";

const shot = (id) => ({ id, template: "shot", data: { prompt: "Medium shot of a sailor holding a lantern in a wet cabin at night" } });
const card = (id) => ({ id, template: "big", data: { headline: "1872" } });
// An episode drawn the way the delivered ones are: mostly illustrations, a card now and then.
const episode = (scenes, look = { preset: CURIO_PRESET }) => ({ slug: "curio-x01", look, scenes });
const paths = (problems) => problems.map((problem) => problem.path);

test("only a curio- slug is an episode of the series", () => {
  assert.equal(isCurio({ slug: "curio-h04-v2" }), true);
  assert.equal(isCurio({ slug: "sothatswhy-t26" }), false);
  assert.deepEqual(curioProblems({ slug: "ai-term-token", scenes: [card("a"), card("b"), card("c"), card("d"), card("e")] }), []);
});

test("an episode in the series look with illustrations between short card runs passes", () => {
  const scenes = [shot("s1"), card("c1"), shot("s2"), shot("s3"), card("c2"), card("c3"), card("c4"), shot("s4"), shot("s5"), shot("s6"), shot("s7"), shot("s8"), shot("s9"), shot("s10"), shot("s11"), { id: "end", template: "outro", data: {} }];
  assert.deepEqual(curioProblems(episode(scenes)), []);
});

test("the series look is the preset word for word, the way the first three episodes wrote it out", () => {
  const scenes = [shot("s1"), shot("s2")];
  const written = { preset: "custom", style: resolveLook({ preset: CURIO_PRESET }).style, negative: "" };
  assert.deepEqual(curioProblems(episode(scenes, written)), []);
  assert.deepEqual(paths(curioProblems(episode(scenes, null))), ["look"]);
  const added = { preset: CURIO_PRESET, style: `${resolveLook({ preset: CURIO_PRESET }).style}, historical gear uses period materials` };
  assert.deepEqual(paths(curioProblems(episode(scenes, added))), ["look.style"]);
  assert.deepEqual(paths(curioProblems(episode(scenes, { preset: CURIO_PRESET, negative: "photorealistic" }))), ["look.negative"]);
});

test("a body under the illustration share, or a long run of cards, is refused", () => {
  const few = [shot("s1"), card("c1"), shot("s2"), card("c2"), card("c3")];
  const share = curioProblems(episode(few));
  assert.ok(share.some((problem) => problem.path === "scenes" && /2 of 5 body scenes/.test(problem.message)), JSON.stringify(share));
  assert.ok(CURIO_MIN_SHOT_SHARE > 0.4);

  const run = Array.from({ length: CURIO_MAX_CARD_RUN + 1 }, (_, i) => card(`c${i}`));
  const scenes = [...Array.from({ length: 12 }, (_, i) => shot(`s${i}`)), ...run, shot("last")];
  const runs = curioProblems(episode(scenes));
  assert.equal(runs.length, 1);
  assert.match(runs[0].message, new RegExp(`${CURIO_MAX_CARD_RUN + 1} cards in a row \\(c0 … c${CURIO_MAX_CARD_RUN}\\)`));
});

test("lint reports the series problems as errors on a curio- slug and not on any other", () => {
  const context = { lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {} };
  const other = lintVideo(fixture(), context);
  assert.ok(!other.errors.some((problem) => problem.path === "look"), JSON.stringify(other.errors));
  const curio = lintVideo({ ...fixture(), slug: "curio-x01" }, context);
  assert.ok(curio.errors.some((problem) => problem.path === "look" && /cute-mystery/.test(problem.message)), JSON.stringify(curio.errors));
});
