// This episode's lexicon was pinned against its first reviewed draft. Later
// audio wording repairs keep that immutable genesis and need their own review.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, realpathSync, statSync } from "node:fs";
import path from "node:path";

import { isInside } from "../../../../tools/video/core/paths.mjs";

export const CHANGED_AUDIO_LINE_IDS = Object.freeze([
  "nx0306", "nx0307", "nx0408", "nx0411", "nx0414", "nx0415",
  "nx0419", "nx0420", "nx0501", "nx0514", "nx0606", "nx0618",
]);
const ROLES = ["source", "narrative_a", "narrative_b"];
const ORIGINAL_EVIDENCE = {
  source: "reviews/source-review-release.md",
  narrative_a: "reviews/blind-a-release.md",
  narrative_b: "reviews/blind-b-release.md",
};
const REVISED_EVIDENCE = {
  source: "reviews/source-review-audio-revision.md",
  narrative_a: "reviews/blind-a-audio-revision.md",
  narrative_b: "reviews/blind-b-audio-revision.md",
};
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const readJsonBytes = (file) => {
  const bytes = readFileSync(file);
  return { value: JSON.parse(bytes.toString("utf8")), sha256: sha256(bytes) };
};

function verifyEvidence({ projectDir, entries, expected, boundVideoSha }) {
  assert.ok(Array.isArray(entries), "review evidence must be an array");
  assert.deepEqual(entries.map((item) => item.role), ROLES, "source and two independent narrative roles");
  const reviewDir = path.join(projectDir, "reviews");
  const realReviewDir = realpathSync(reviewDir);
  return entries.map((item) => {
    assert.equal(item.file, expected[item.role], "review evidence file: " + item.role);
    assert.match(item.sha256, /^[a-f0-9]{64}$/, "review evidence SHA: " + item.role);
    const file = path.resolve(projectDir, item.file);
    assert.ok(isInside(file, reviewDir), "review evidence escapes reviews/: " + item.file);
    assert.ok(isInside(realpathSync(file), realReviewDir), "review evidence symlink escapes reviews/: " + item.file);
    assert.ok(statSync(file).isFile(), "review evidence is not a regular file: " + item.file);
    const bytes = readFileSync(file);
    assert.equal(sha256(bytes), item.sha256, "review evidence SHA drift: " + item.file);
    const text = bytes.toString("utf8");
    assert.ok(text.includes(boundVideoSha), "review evidence does not mention its script SHA: " + item.file);
    assert.match(text, /\bPASS\b/u, "review evidence does not record PASS: " + item.file);
    return { role: item.role, file: item.file, sha256: item.sha256 };
  });
}

/** Read-only checks for both the immutable genesis and the subsequently reviewed audio edits. */
export function verifyPreviewReviewLineage({ projectDir, currentVideoSha, seriesSha }) {
  assert.match(currentVideoSha, /^[a-f0-9]{64}$/);
  assert.match(seriesSha, /^[a-f0-9]{64}$/);
  const originalReceiptFile = path.join(projectDir, "reviews", "lexicon-bootstrap.json");
  const original = readJsonBytes(originalReceiptFile);
  const bootstrap = original.value;
  assert.equal(bootstrap.schema_version, 1);
  assert.equal(bootstrap.kind, "manual_story_lexicon_bootstrap_review");
  assert.equal(bootstrap.decision, "pin_unspoken_manual_draft");
  assert.equal(bootstrap.slug, "story-everyday-netflix-x03");
  assert.match(bootstrap.video_json_sha256, /^[a-f0-9]{64}$/);
  assert.equal(bootstrap.series_json_sha256, seriesSha, "historical bootstrap series SHA drift");
  const originalEvidence = verifyEvidence({ projectDir, entries: bootstrap.evidence, expected: ORIGINAL_EVIDENCE, boundVideoSha: bootstrap.video_json_sha256 });

  const pointer = readJsonBytes(path.join(projectDir, "story-lexicon", "current.json")).value;
  assert.equal(pointer.slug, bootstrap.slug);
  const immutableFile = path.join(projectDir, "story-lexicon", "manual-bootstraps", `${pointer.head_event_sha256}.json`);
  const immutable = readJsonBytes(immutableFile);
  const genesis = immutable.value;
  assert.equal(genesis.event_sha256, pointer.head_event_sha256, "manual bootstrap event SHA drift");
  assert.equal(genesis.lexicon_sha256, pointer.lexicon_sha256, "manual bootstrap lexicon SHA drift");
  assert.equal(genesis.video_json_sha256, bootstrap.video_json_sha256, "immutable genesis script SHA drift");
  assert.equal(genesis.series_json_sha256, bootstrap.series_json_sha256, "immutable genesis series SHA drift");
  assert.equal(genesis.review_receipt_sha256, original.sha256, "immutable genesis review receipt SHA drift");
  assert.deepEqual(genesis.evidence, bootstrap.evidence, "immutable genesis review evidence drift");

  const revisedReceiptFile = path.join(projectDir, "reviews", "audio-revision-review.json");
  const revised = readJsonBytes(revisedReceiptFile);
  const review = revised.value;
  assert.equal(review.schema_version, 1);
  assert.equal(review.kind, "story_audio_revision_review");
  assert.equal(review.slug, bootstrap.slug);
  assert.equal(review.decision, "reviewed_script_revision_pass");
  assert.equal(review.scope, "text_only");
  assert.equal(review.video_json_sha256, currentVideoSha, "current audio-revision script SHA drift");
  assert.equal(review.previous_video_json_sha256, bootstrap.video_json_sha256, "audio revision is not based on the pinned script");
  assert.equal(review.bootstrap_review_sha256, original.sha256, "audio revision references a different bootstrap receipt");
  assert.deepEqual(review.changed_line_ids, CHANGED_AUDIO_LINE_IDS, "audio revision changed-line set");
  const revisedEvidence = verifyEvidence({ projectDir, entries: review.evidence, expected: REVISED_EVIDENCE, boundVideoSha: currentVideoSha });

  return {
    historical_bootstrap: {
      video_json_sha256: bootstrap.video_json_sha256,
      review_receipt_sha256: original.sha256,
      immutable_sidecar_sha256: immutable.sha256,
      evidence: originalEvidence,
    },
    current_revision: {
      video_json_sha256: review.video_json_sha256,
      review_receipt_sha256: revised.sha256,
      changed_line_ids: review.changed_line_ids,
      evidence: revisedEvidence,
      scope: review.scope,
    },
  };
}
