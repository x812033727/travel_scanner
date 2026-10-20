import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { inspectHumanArtReview } from "./local-preview-art-review.mjs";
import { inspectIndependentVisualReview } from "./local-preview-source-review.mjs";

test("a judge pass cannot override a human-held illustration", () => {
  const workdir = mkdtempSync(path.join(os.tmpdir(), "x06-art-guard-"));
  try {
    mkdirSync(path.join(workdir, "review/local-preview"), { recursive: true });
    const doc = { scenes: [{ id: "shot-a", template: "shot", data: {} }] };
    const manifest = { shots: { "shot-a": { file: "keyframes/a.jpg", sha256: "a".repeat(64), judge: { passed: true }, needs_review: false } } };
    const review = { kind: "human-art-gate", status: "PASSED", video_json_sha256: "script", keyframes_manifest_sha256: "manifest",
      shots: { "shot-a": { status: "usable", selected_file: "keyframes/a.jpg", selected_sha256: "a".repeat(64) } } };
    const check = () => inspectHumanArtReview({ doc, manifest, manifestSha: "manifest", scriptSha: "script", workdir }).issues;
    const save = () => writeFileSync(path.join(workdir, "review/local-preview/art-review.json"), JSON.stringify(review));
    save();
    assert.deepEqual(check(), []);
    review.shots["shot-a"].status = "hold";
    save();
    assert.match(check().join("; "), /unapproved or changed illustration: shot-a/);
    review.shots["shot-a"].status = "usable";
    manifest.shots["shot-a"].judge.passed = false;
    save();
    assert.match(check().join("; "), /unapproved or changed illustration: shot-a/);
    manifest.shots["shot-a"].judge.passed = true;
    assert.match(inspectHumanArtReview({ doc, manifest, manifestSha: "changed", scriptSha: "script", workdir }).issues.join("; "), /another keyframes manifest/);
  } finally {
    rmSync(workdir, { recursive: true, force: true });
  }
});

test("two independent visual receipts bind the exact current script", () => {
  const dir = path.dirname(new URL(import.meta.url).pathname);
  const current = createHash("sha256").update(readFileSync(path.join(dir, "video.json"))).digest("hex");
  const review = inspectIndependentVisualReview({ dir, scriptSha: current });
  assert.deepEqual(review.issues, []);
  assert.equal(review.sha256, "b0f8d00eada61391a518dc8c952619b70e7100df91233035e21c73b182411c56");
  assert.deepEqual(inspectIndependentVisualReview({ dir, scriptSha: "907f8e3ff45f3edf0bbed64a54216c761696e8e954d51c315a8a228069e204d1" }).issues, []);
  assert.match(inspectIndependentVisualReview({ dir, scriptSha: "other" }).issues.join("; "), /another video.json/);
});
