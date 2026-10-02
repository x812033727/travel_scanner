import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { DIRECTORY, ROOT } from "./plans.mjs";
import { checkDurationReview, durationReviewProblems } from "./review.mjs";

test("the shipped independent duration review binds the current plans and implementation", () => {
  assert.deepEqual(checkDurationReview(), []);
});

test("self-review, a removed binding, changed report or later file revision invalidates acceptance", () => {
  const receipt = JSON.parse(readFileSync(path.join(ROOT, DIRECTORY, "review.json"), "utf8"));
  const report = readFileSync(path.join(ROOT, DIRECTORY, "review.md"), "utf8");
  const hashes = (file) => receipt.reviewed_files[file];
  assert.ok(durationReviewProblems({ ...receipt, reviewer_agent: receipt.author_agent }, report, hashes).some((problem) => /independent/.test(problem)));
  const missing = structuredClone(receipt);
  delete missing.reviewed_files["tools/video/core/duration.mjs"];
  assert.ok(durationReviewProblems(missing, report, hashes).some((problem) => /cover every/.test(problem)));
  assert.ok(durationReviewProblems(receipt, `${report}\nchanged`, hashes).some((problem) => /report is stale/.test(problem)));
  assert.ok(durationReviewProblems(receipt, report, (file) => file === "docs/videos/long-form/plans.json" ? "0".repeat(64) : hashes(file)).some((problem) => /stale duration review binding/.test(problem)));
});
