import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "../core/fixtures/load.mjs";
import { buildTimeline, SAMPLE_RATE } from "../core/timeline.mjs";
import { MAX_STATE_SECONDS, paceDetail, paceProblems, slideStates } from "./pace.mjs";

const seconds = (n) => n * SAMPLE_RATE;

function timelineWith(doc, secondsById) {
  const samples = {};
  for (const scene of doc.scenes) for (const line of scene.lines) samples[line.id] = seconds(secondsById[line.id] ?? 2);
  return buildTimeline(doc, samples);
}

test("a scene opens a state on its first line and every reveal starts the next one", () => {
  const doc = fixture();
  const timeline = timelineWith(doc, {});
  const states = slideStates(doc, timeline);
  assert.deepEqual(states.map((state) => `${state.scene}/${state.index}`), ["hook/0", "questions/0", "questions/1", "questions/2", "wrap/0"]);
  // Each state ends where the next begins; the last one ends with the video.
  states.forEach((state, position) => assert.equal(state.end_frame, states[position + 1]?.start_frame ?? timeline.total_frames));
  assert.deepEqual(states.map((state) => state.start_frame), timeline.scenes.flatMap((scene) => scene.states.map((state) => state.start_frame)), "the same states the tts stage laid out");
  assert.deepEqual(paceProblems(states), []);
  assert.match(paceDetail(states, []), /^5 slide states, the longest [\d.]+ s; none over 15 s$/);
});

test("a state held longer than the limit is named with its scene and seconds", () => {
  const doc = fixture();
  const states = slideStates(doc, timelineWith(doc, { k7p2: 12, m4qa: 8 }));
  const problems = paceProblems(states);
  assert.equal(problems.length, 1);
  assert.equal(problems[0].scene, "hook");
  assert.equal(problems[0].index, 0);
  assert.ok(problems[0].seconds > 20 && problems[0].seconds < 22, `hook runs about 20.6 s: ${problems[0].seconds}`);
  assert.match(paceDetail(states, problems), /^1 of 5 slide states stay over 15 s: hook state 0 \(2[01]\.\d s\)$/);
  assert.equal(MAX_STATE_SECONDS, 15);
  assert.equal(paceProblems(states, 30).length, 0);
});

test("a reveal on a scene's first line does not add a state; a missing line is an error", () => {
  const doc = fixture();
  doc.scenes[1].lines[0].reveal = 1;
  doc.scenes[1].lines[1].reveal = undefined;
  const states = slideStates(doc, timelineWith(doc, {}));
  assert.deepEqual(states.filter((state) => state.scene === "questions").map((state) => state.index), [0, 1]);
  const stale = timelineWith(doc, {});
  stale.lines = stale.lines.filter((line) => line.id !== "r8wd");
  assert.throws(() => slideStates(doc, stale), /timeline\.json has no line r8wd/);
});
