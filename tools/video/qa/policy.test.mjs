import assert from "node:assert/strict";
import { test } from "node:test";

import { policyVerdict } from "./policy.mjs";

// An explainer, a story, a drama and a cut Short are not asked for a demonstration
// (apps/api/app/video_automation/judge.py `policy_questions_for`): the answer's `demo` is null.

test("an answer whose demo is null passes or fails on the judge's flag and shows the site's note", () => {
  const note = "Jev：符合立場 0.82、有示範：不適用（解說）、建議 0.05、業配 0.10，通過";
  const answer = { stance: 0.82, demo: null, advice: 0.05, sponsored: 0.1, passed: true, note, questions: "explainer", observation: null, disparage: null };
  assert.deepEqual(policyVerdict(answer), { ok: true, detail: note });
  const failed = "Jev：符合立場 0.40、有示範：不適用（解說）、建議 0.05、業配 0.10；沒過（符合立場低於 0.6）";
  assert.deepEqual(policyVerdict({ ...answer, stance: 0.4, passed: false, note: failed }), { ok: false, detail: failed });
});

test("without a note, a null demo reads as not asked and a missing one is left out", () => {
  assert.deepEqual(policyVerdict({ stance: 0.82, demo: null, advice: 0.05, sponsored: 0.1, passed: true, note: "" }), {
    ok: true,
    detail: "Jev passed the narration: stance 0.82, demo not asked, advice 0.05, sponsored 0.10",
  });
  assert.deepEqual(policyVerdict({ stance: 0.4, demo: null, advice: 0.05, sponsored: 0.1, passed: false }), {
    ok: false,
    detail: "Jev did not pass the narration: stance 0.40, demo not asked, advice 0.05, sponsored 0.10",
  });
  assert.deepEqual(policyVerdict({ stance: 0.9, advice: 0, sponsored: 0, passed: true }), {
    ok: true,
    detail: "Jev passed the narration: stance 0.90, advice 0.00, sponsored 0.00",
  });
});

test("a null demo is never a verdict of its own", () => {
  assert.deepEqual(policyVerdict({ demo: null }), { ok: false, detail: "the judge answered without a verdict" });
  assert.deepEqual(policyVerdict({ demo: null, passed: false }), { ok: false, detail: "Jev did not pass the narration: demo not asked" });
});
