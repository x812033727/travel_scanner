import assert from "node:assert/strict";
import test from "node:test";

import { cadenceProblems, cadenceSummary, HOOK_SECONDS, illustrationShare, MAX_PICTURE_SECONDS, MIN_ILLUSTRATION_SHARE, slideStates, TARGET_AVERAGE_SECONDS } from "./cadence.mjs";
import { fixture, illustratedFixture } from "./fixtures/load.mjs";
import { buildTimeline, SAMPLE_RATE } from "./timeline.mjs";

const seconds = (n) => n * SAMPLE_RATE;

function timelineWith(doc, secondsById, fallback = 2) {
  const samples = {};
  for (const scene of doc.scenes) for (const line of scene.lines) samples[line.id] = seconds(secondsById[line.id] ?? fallback);
  return buildTimeline(doc, samples);
}

test("the constants are the ones docs/videos/ILLUSTRATED.md names", () => {
  assert.equal(MAX_PICTURE_SECONDS, 8);
  assert.equal(TARGET_AVERAGE_SECONDS, 6);
  assert.equal(MIN_ILLUSTRATION_SHARE, 0.5);
  assert.equal(HOOK_SECONDS, 20);
});

test("a shot is one state; cards add a state per reveal; the share counts the shots' frames", () => {
  const doc = illustratedFixture();
  // A shot's sentence runs about three seconds, a card's about two, as the example is written.
  const spoken = Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").flatMap((scene) => scene.lines.map((line) => [line.id, 3])));
  const timeline = timelineWith(doc, spoken);
  const states = slideStates(doc, timeline);
  const shots = doc.scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id);
  for (const id of shots) assert.equal(states.filter((state) => state.scene === id).length, 1, `${id} is one state`);
  assert.equal(states.filter((state) => state.scene === "numbers").length, 3, "the stats card reveals twice");
  const share = illustrationShare(doc, timeline);
  assert.ok(share > 0.4 && share < 0.8, `about half the runtime is pictures: ${share}`);
  const summary = cadenceSummary(states);
  assert.equal(summary.count, states.length);
  assert.ok(summary.longest >= summary.average);
  assert.deepEqual(cadenceProblems(doc, timeline), [], "the example keeps the cadence");
});

test("a picture held too long, a slow average and too few pictures are each named", () => {
  const doc = illustratedFixture();
  const slow = timelineWith(doc, { a2pd: 9.5 });
  const over = cadenceProblems(doc, slow);
  assert.ok(over.some((problem) => problem.kind === "over" && problem.path === "scenes (podium state 0)"), JSON.stringify(over));
  const everything = cadenceProblems(doc, timelineWith(doc, {}, 7));
  assert.ok(everything.some((problem) => problem.kind === "average"), "every state at 7 s is slower than the 6 s target");
  const cards = illustratedFixture();
  const withoutShots = cadenceProblems(cards, timelineWith(cards, { a5nm: 20, a6nm: 20, a7nm: 20, a9rl: 20 }));
  assert.ok(withoutShots.some((problem) => problem.kind === "share"), "long cards push the illustration share under half");
  assert.deepEqual(cadenceProblems(doc, slow, { max: 30, average: 30, share: 0 }), [], "the limits are the caller's");
});

test("plain slides have no cadence problems: their rule is qa/pace.mjs", () => {
  const doc = fixture();
  assert.deepEqual(cadenceProblems(doc, timelineWith(doc, { k7p2: 40 })), []);
  assert.equal(illustrationShare(doc, timelineWith(doc, {})), 0);
});
