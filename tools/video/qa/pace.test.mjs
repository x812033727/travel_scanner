import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "../core/fixtures/load.mjs";
import { buildTimeline, SAMPLE_RATE } from "../core/timeline.mjs";
import { MAX_STATE_SECONDS, paceDetail, paceProblems, slideStates, terminalHoldDetail, terminalHoldProblems } from "./pace.mjs";

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

test("a human-typed terminal state whose narration, as cut, ends before the typing does is named with both times", () => {
  const doc = fixture();
  // Turn the hook into a terminal typed at a human pace: 16 keys take 1.4 s, then one line.
  doc.scenes[0].template = "terminal";
  doc.scenes[0].data = { command: "claude --version", output: ["2.1.285 (Claude Code)"], ran_on: "2026-10-01", tool_version: "2.1.285 (Claude Code)", typing: "human" };
  assert.deepEqual(terminalHoldProblems(doc, timelineWith(doc, { k7p2: 3 })), [], "3 s of narration carries 1.4 s of typing, a line and the half second to read");
  const fast = terminalHoldProblems(doc, timelineWith(doc, { k7p2: 0.3, m4qa: 0.3 }));
  assert.equal(fast.length, 1);
  assert.equal(fast[0].scene, "hook");
  assert.equal(fast[0].index, 0);
  assert.equal(fast[0].needs, 1.7);
  assert.ok(fast[0].seconds < 2.2, `the hook holds about 1.9 s: ${fast[0].seconds}`);
  assert.match(terminalHoldDetail(fast), /^1 human-typed terminal states outrun their narration \(typing plus 0\.5 s to read\): hook state 0 \(1\.7 s of typing in [\d.]+ s\)$/);
  assert.equal(terminalHoldDetail([]), "");
  delete doc.scenes[0].data.typing;
  assert.deepEqual(terminalHoldProblems(doc, timelineWith(doc, { k7p2: 0.3, m4qa: 0.3 })), [], "the 18-frame burst is never held");
});
