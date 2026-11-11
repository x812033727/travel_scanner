import assert from "node:assert/strict";
import test from "node:test";

import { PACE_FLOORS, hanCount, narrationPace, paceFloor, paceWarning } from "./pace.mjs";

const RATE = 24000;
const doc = (slug, lines) => ({ slug, scenes: [{ id: "s1", lines: lines.map(([id, text]) => ({ id, text })) }] });
const timeline = (lines) => ({ sample_rate: RATE, lines: lines.map(([id, seconds]) => ({ id, audio_samples: Math.round(seconds * RATE) })) });

test("only Han characters count", () => {
  assert.equal(hanCount("泡泡，2 個 bubble！"), 3);
  assert.equal(hanCount(""), 0);
});

test("the pace is characters over seconds of speech, pauses left out", () => {
  const pace = narrationPace(doc("sothatswhy-x", [["p1", "一二三四五"], ["p2", "六七八九十"]]), timeline([["p1", 1], ["p2", 1]]));
  assert.equal(pace.chars, 10);
  assert.equal(pace.seconds, 2);
  assert.equal(pace.rate, 5);
});

test("a slow sothatswhy or curio narration is warned, a fast one is not", () => {
  const lines = [["p1", "一二三四五六七"]];
  assert.match(paceWarning(doc("sothatswhy-p06", lines), timeline([["p1", 2]])), /3\.50 characters a second/);
  assert.match(paceWarning(doc("curio-h01", lines), timeline([["p1", 2]])), /at least 4\.5/);
  assert.equal(paceWarning(doc("curio-h01", lines), timeline([["p1", 7 / PACE_FLOORS.curio]])), null);
});

test("each series keeps its own floor: 原來如此 passes the 4.39 style the owner chose, 奇聞 does not", () => {
  const lines = [["p1", "一".repeat(439)]];
  assert.equal(paceFloor(doc("sothatswhy-p07", lines)), 4.3);
  assert.equal(paceFloor(doc("curio-h01", lines)), 4.5);
  assert.equal(paceWarning(doc("sothatswhy-p07", lines), timeline([["p1", 100]])), null);
  assert.match(paceWarning(doc("curio-h01", lines), timeline([["p1", 100]])), /4\.39 characters a second/);
  assert.match(paceWarning(doc("sothatswhy-p06", [["p1", "一".repeat(374)]]), timeline([["p1", 100]])), /at least 4\.3/);
});

test("other series and unrecorded narration get no warning", () => {
  const lines = [["p1", "一二三"]];
  assert.equal(paceWarning(doc("story-x", lines), timeline([["p1", 3]])), null);
  assert.equal(paceWarning(doc("sothatswhy-p06", lines), { sample_rate: RATE, lines: [] }), null);
  assert.equal(narrationPace(doc("sothatswhy-p06", lines), null), null);
});
