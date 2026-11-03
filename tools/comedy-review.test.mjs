// The comedy story-plan review (.agents/skills/animation-preproduction/references/comedy-review.md):
// the rubric totals 100, the gates the doc names are the ones the script applies, a judge file
// is checked before it counts, and a round passes only when every gate holds.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import { GATES, RUBRIC, decide, judgeProblems, packet } from "../.agents/skills/animation-preproduction/scripts/comedy_review.mjs";

const doc = readFileSync(new URL("../.agents/skills/animation-preproduction/references/comedy-review.md", import.meta.url), "utf8");

const judge = (name, scores, beats) => ({ judge: name, scores, beats, fixes: [] });
const even = (points) => Object.fromEntries(Object.entries(RUBRIC).map(([key, [max]]) => [key, Math.round((max * points) / 100)]));

test("the rubric totals 100 and the doc lists every axis with its maximum", () => {
  assert.equal(Object.values(RUBRIC).reduce((sum, [max]) => sum + max, 0), 100);
  for (const [key, [max]] of Object.entries(RUBRIC)) assert.match(doc, new RegExp(`\\| \`${key}\` \\| ${max} \\|`));
  for (const value of [GATES.medianTotal, GATES.everyJudgeTotal, GATES.medianLaughs, GATES.medianSurprise]) assert.ok(doc.includes(String(value)));
});

test("a judge file must follow the schema", () => {
  assert.deepEqual(judgeProblems(judge("a", even(90), [{ shot: "s1", joke: "j", funny: 5 }]), new Set(["s1"])), []);
  const bad = judgeProblems({ judge: "a", scores: { ...even(90), laughs: 21 }, beats: [{ shot: "nope", joke: "", funny: 9 }] }, new Set(["s1"]));
  assert.ok(bad.some((p) => p.startsWith("scores.laughs")));
  assert.ok(bad.some((p) => p.startsWith("beats[0].shot")));
  assert.ok(bad.some((p) => p.startsWith("beats[0].funny")));
  assert.ok(bad.some((p) => p.startsWith("fixes")));
});

test("a round passes only when every gate holds", () => {
  const beats = [{ shot: "s1", joke: "a", funny: 5 }, { shot: "s2", joke: "b", funny: 4 }, { shot: "s3", joke: "c", funny: 4 }];
  const good = decide(["a", "b", "c"].map((n) => judge(n, even(85), beats)));
  assert.equal(good.pass, true, good.reasons.join("; "));
  assert.equal(decide(["a", "b"].map((n) => judge(n, even(85), beats))).pass, false, "two judges are not enough");
  const oneBored = decide([judge("a", even(85), beats), judge("b", even(85), beats), judge("c", even(60), beats)]);
  assert.ok(oneBored.reasons.some((r) => r.includes("under 65")));
  const notFunny = decide(["a", "b", "c"].map((n) => judge(n, { ...even(90), laughs: 10 }, beats)));
  assert.ok(notFunny.reasons.some((r) => r.startsWith("laughs")));
  const unlisted = decide([judge("a", even(85), beats), judge("b", even(85), [beats[0]]), judge("c", even(85), [beats[0]])]);
  assert.ok(unlisted.reasons.some((r) => r.includes("beat(s)")), "a beat a judge did not list counts as 1");
});

test("the packet carries shots, lines and cues but nothing of the brief", () => {
  const text = packet({
    slug: "x", characters: [{ id: "dog", name: "麻糬" }], sfx: { set: "s", cues: [{ scene: "a", sound: "laugh" }] },
    scenes: [{ id: "a", template: "shot", data: { prompt: "P", camera: "Close-up", motion: "M" }, lines: [{ text: "汪", speaker: "dog", emotion: "內心" }] }],
  });
  for (const part of ["## 1. a", "Close-up", "P", "M", "【麻糬】（內心）汪", "laugh"]) assert.ok(text.includes(part), part);
});
